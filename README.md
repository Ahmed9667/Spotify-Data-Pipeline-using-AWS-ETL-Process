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

