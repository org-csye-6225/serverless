# Cloud Function for User Verification

This Cloud Function is triggered by messages on a Cloud Pub/Sub topic. It sends an email with a verification link to the user's email address using the Mailgun API and updates the `emailSentAt` field in the `users` table of a MySQL database hosted on Cloud SQL.

## Prerequisites

- Google Cloud Platform account with permissions for Cloud Functions, Cloud Pub/Sub, and Cloud SQL.
- Mailgun API credentials for sending emails.
- Environment variables set for database connection details (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).

## Deployment

0. This repository can be zipped and stored in bucket on GCP 
    OR
1. Clone this repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables.
4. Deploy the Cloud Function: `gcloud functions deploy hello_pubsub --runtime python39 --trigger-topic YOUR_PUBSUB_TOPIC_NAME`
5. Test the function by publishing a message to the Cloud Pub/Sub topic with the required data (email and token).
