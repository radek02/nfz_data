# Deploying getData.py to GCP Cloud Run

## Prerequisites
- GCP account with billing enabled
- gcloud CLI installed ([install here](https://cloud.google.com/sdk/docs/install))
- Docker installed locally (optional, Cloud Build can build for you)

## Steps

### 1. Set up GCP project
```bash
# Set your project ID
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable storage.googleapis.com
```

### 2. Create a Cloud Storage bucket for output
```bash
export BUCKET_NAME="${PROJECT_ID}-drug-data"
gcloud storage buckets create gs://${BUCKET_NAME} --location=us-central1
```

### 3. Build and deploy with Cloud Build
```bash
# Build the container using Cloud Build (no local Docker needed)
gcloud builds submit --tag gcr.io/${PROJECT_ID}/drug-data-scraper

# Deploy to Cloud Run Jobs
gcloud run jobs create drug-data-job \
  --image gcr.io/${PROJECT_ID}/drug-data-scraper \
  --set-env-vars GCS_BUCKET_NAME=${BUCKET_NAME} \
  --max-retries 1 \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --task-timeout 3600
```

### 4. Run the job
```bash
# Execute the job
gcloud run jobs execute drug-data-job --region us-central1

# Check job status
gcloud run jobs executions list --job drug-data-job --region us-central1

# View logs
gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=drug-data-job" --limit 50 --format json
```

### 5. Download the CSV
```bash
# Download from Cloud Storage
gcloud storage cp gs://${BUCKET_NAME}/drug_costs_czerniak_no_age_groups.csv .
```

## Alternative: Local Docker Build
If you prefer to build Docker locally:
```bash
# Build
docker build -t gcr.io/${PROJECT_ID}/drug-data-scraper .

# Push to Google Container Registry
docker push gcr.io/${PROJECT_ID}/drug-data-scraper

# Then continue with step 3 (deploy)
```

## Cleanup
```bash
# Delete the job
gcloud run jobs delete drug-data-job --region us-central1

# Delete the bucket
gcloud storage rm -r gs://${BUCKET_NAME}
```

## Notes
- The job will timeout after 1 hour (3600 seconds), adjust `--task-timeout` if needed
- Cloud Run Jobs are billed per execution time
- The CSV will be automatically uploaded to your Cloud Storage bucket
