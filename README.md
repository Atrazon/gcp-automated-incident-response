# GCP Automated Incident Response Pipeline
This project demonstrates an automated Security Operations Center (SOC) workflow.

## Scenario
A compromised service account begins deleting critical objects in a production GCS bucket. 

## Solution
1. **Detection**: GCP Audit Logs capture the activity.
2. **Routing**: A Log Sink sends these events to a Pub/Sub topic.
3. **Response**: A Python Cloud Function (this code) is triggered, parses the user ID, and instantly removes the user from the Project IAM Policy.

## Skills Demonstrated
- Incident Containment (GCP IAM)
- Cloud Automation (Python, Google Cloud SDK)
- Security Monitoring (Audit Logs/Pub/Sub)
