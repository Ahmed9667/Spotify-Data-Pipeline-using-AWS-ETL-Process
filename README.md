# 🎵 Spotify Data Pipeline using AWS (Serverless ETL)

## 💡 Technologies Used:
- Python (Spotify API integration & data handling)

- Spotify Web API (via spotipy or requests)

- AWS Lambda (serverless compute for ETL steps)

- Amazon S3 (raw and transformed data storage)

- Amazon CloudWatch (automated Lambda scheduling)

- AWS Glue (schema inference & cataloging)

- Amazon Athena (SQL-based data exploration)



## 🚀 Project Overview:
The goal of this project is to create a cloud-based, event-driven data pipeline that fetches data from Spotify, processes it, and stores it for analytics — using only AWS services and Python.
This setup is ideal for real-time or scheduled music data analysis, reporting, and machine learning pipelines.

## 🔍 Architecture Breakdown:
Data Extraction

### `1.Data Extraction:`

- A Python script interacts with the Spotify API to fetch music metadata (e.g. playlists, tracks, artist info).

- AWS Lambda handles the extraction logic, triggered daily by Amazon CloudWatch.

- Raw data is stored in Amazon S3.

### `2.Data Transformation:`

- An S3 event triggers another AWS Lambda function once new data lands in the S3 bucket.

- The Lambda function cleans, flattens, and transforms JSON data.

- Transformed data is saved to a separate S3 bucket for downstream analysis.

  ### `3.Data Loading and Querying:`

- AWS Glue Crawlers automatically scan and infer the schema of the transformed data.

- The schema is stored in the AWS Glue Data Catalog.

- Amazon Athena enables serverless SQL queries on the processed data, allowing for flexible analysis and reporting.

  
![DataVidhya+Projects+(1)_page-0001](https://github.com/user-attachments/assets/468bbf31-06f2-478b-adf5-4f2738220814)

`------------------------------------------------------------------------------------------------------------------------------------`
## `Steps in Depth:`
#### Create Extraction Lambda Function:

![image](https://github.com/user-attachments/assets/b3849909-e020-485b-9b03-092b502a0108)

#### Create Spotify Layer of Spotify Library on Python

![image](https://github.com/user-attachments/assets/c4da61ff-3b03-4b40-9edb-2e29b2793b8c)

#### Add Spotify Layer to Lambda Function

![image](https://github.com/user-attachments/assets/52064541-2b97-4afa-aa52-8bf99e85b255)

#### Deploy the original data extracted from API to the raw data bucket
```python
import pandas as pd
import json
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3 #to communicate with AWS services


def lambda_handler(event, context):
    # Replace these with your actual credentials
    load_dotenv()
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')

    # Set up authentication
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    data = sp.playlist_tracks(play_list_url)
    print(data)

    client = boto3.client('s3')
    client.put_object(Bucket='spotify-etl-project-ahmed-eraki'  #S3 Bucket name we use
      ,Key= 'raw_data/to_process/' #the path where I put the output of lambda code function
      ,Body=json.dumps(data))
```

![image](https://github.com/user-attachments/assets/4ffbf43c-8192-48d3-aa86-0bd494888453)

#### Create transformation lambda function and check for the extracted data from json

`python
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
`

![image](https://github.com/user-attachments/assets/fb7d65b5-c9c7-40ff-9f12-91870a6b4fea)


#### Creating Transformed DataFrame:

```python
import json
import boto3
import pandas as pd

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
    print(df)
    

```

![image](https://github.com/user-attachments/assets/243b5c43-124d-4836-a228-30a7f9477445)
![image](https://github.com/user-attachments/assets/f2a15d48-d6fd-49ae-afd6-f6fa0a232043)
![image](https://github.com/user-attachments/assets/97208172-43d7-43a8-ab94-085cabed752e)

####  saving the transformed dataframe:

```python
data_frame_key = 'transformed_data/transformed_data'+ '.csv'

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Save CSV to S3
    s3.put_object(
        Bucket=Bucket,
        Key=data_frame_key,
        Body=csv_buffer.getvalue()
    )
```

![image](https://github.com/user-attachments/assets/2600dba5-1b60-4534-89d3-1b1b78ad1a01)












