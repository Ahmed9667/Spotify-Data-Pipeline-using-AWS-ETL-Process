import json
import boto3
import pandas as pd
from io import StringIO

def my_data(data):
    name =[]
    popularity = []
    album_link = []
    added_at = []

    for i in range(len(data['items'])):
        if i :
            name.append(data['items'][i]['track']['name'])
            popularity.append(data['items'][i]['track']['popularity'])
            album_link.append(data['items'][i]['added_by']['external_urls']['spotify'])
            added_at.append(data['items'][i]['added_at'])

        else:
            name.append('-')
            popularity.append('-')
            album_link.append('-')
            added_at.append('-')   
    return name, popularity, album_link, added_at

spotify_data = []
spotify_keys = []
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket='spotify-etl-project-ahmed-eraki'
    my_key= "raw_data/to_process/"
    for file in s3.list_objects(Bucket=Bucket, Prefix=my_key)['Contents']:
        file_key = file['Key']
        if file_key.split('.')[-1] == 'json':
            response = s3.get_object(Bucket=Bucket,Key=file_key )
            content = response['Body']
            object = json.loads(content.read())
            spotify_data.append(object)
            spotify_keys.append(file_key)

    if spotify_data:
            all_names = []
            all_popularity = []
            all_album_links = []
            all_added_at = []

            for data in spotify_data:
                name, popularity, album_link, added_at = my_data(data)
                all_names.extend(name)
                all_popularity.extend(popularity)
                all_album_links.extend(album_link)
                all_added_at.extend(added_at)

            #  Create a DataFrame
            df = pd.DataFrame({
                'song': all_names,
                'popularity': all_popularity,
                'date': all_added_at,
                'url': all_album_links
            })
    
    #transformation
    df['date'] = df['date'] .replace('-','')
    df['date'] = pd.to_datetime(df['date'] , errors ='coerce')
    df['date_only'] = df['date'].dt.date
    # Drop rows where 'album_id' equals '-'
    df = df[df['song'] != '-']
    
    data_frame_key = 'transformed_data/transformed_data'+ '.csv'

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Save CSV to S3
    s3.put_object(
        Bucket=Bucket,
        Key=data_frame_key,
        Body=csv_buffer.getvalue()
    )


    



        
        
        

