import os
import subprocess
from google.cloud import storage

# Run the getData.py script
print("Starting data collection...")
subprocess.run(["python", "getData.py"], check=True)
print("Data collection completed!")

# Upload to Google Cloud Storage
bucket_name = os.environ.get("GCS_BUCKET_NAME")
output_file = "drug_costs_czerniak_no_age_groups.csv"

if bucket_name:
    print(f"Uploading {output_file} to gs://{bucket_name}/")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(output_file)
    blob.upload_from_filename(output_file)
    print(f"File uploaded successfully to gs://{bucket_name}/{output_file}")
else:
    print("GCS_BUCKET_NAME not set, skipping upload to Cloud Storage")
    print(f"CSV file saved locally as: {output_file}")
