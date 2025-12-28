import json
import base64
from googleapiclient import discovery

def auto_remediate_iam(event, context):
    """
    Triggered by a Pub/Sub message when a suspicious delete event 
    is detected in a GCP Storage Bucket.
    """
    # 1. Decode the log data from the Pub/Sub message
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    log_entry = json.loads(pubsub_message)
    
    # 2. Identify the 'Actor' (the user doing the suspicious activity)
    user_email = log_entry['protoPayload']['authenticationInfo']['principalEmail']
    project_id = "your-gcp-project-id"
    
    print(f"ALERT: Suspicious activity detected by {user_email}. Initiating containment...")

    # 3. Initialize the IAM API
    service = discovery.build('cloudresourcemanager', 'v1')

    # 4. Get the current IAM policy for the project
    policy = service.projects().getIamPolicy(resource=project_id).execute()

    # 5. REMOVAL LOGIC: Remove the user from all roles in the policy
    new_bindings = [
        binding for binding in policy.get('bindings', [])
        if user_email not in binding.get('members', [])
    ]
    policy['bindings'] = new_bindings

    # 6. Push the updated 'clean' policy back to GCP
    body = {'policy': policy}
    service.projects().setIamPolicy(resource=project_id, body=body).execute()

    print(f"SUCCESS: {user_email} has been stripped of all permissions.")
