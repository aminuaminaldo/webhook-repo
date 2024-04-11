from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://aminuashraf198:Ud097ZRLvkefM3f5@githubcluster.bf6kgwk.mongodb.net/")
db = client["webhook_db"]
collection = db["repository_events"]

@app.route('/')
def home():
    return 'Welcome to Webhook Repo with GitHub!'

@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    # Verify that the request contains JSON data
    if request.is_json:
        # Parse the JSON payload
        payload = request.json

        # Extract relevant data from the payload
        try:
            action_type = request.headers.get('X-Github-Event')

            # Format the message based on the action type
            if action_type == 'push':
                action = 'PUSH'
                author = payload['pusher']['name']
                to_branch = payload['ref'].split('/')[-1]  # Extract the branch name from the ref
                request_id = payload['head_commit']['id']
                timestamp = payload['head_commit']['timestamp']
                message = f'"{author}" pushed to "{to_branch}" on {timestamp}'
                from_branch = to_branch  # For push events, from_branch and to_branch are the same
            elif action_type == 'pull_request':
                action = payload['action']
                request_id = payload['pull_request']['id'] # We use PR id for pull request events
                if action == 'opened' or action == 'reopened':
                    action = 'PULL_REQUEST'
                    author = payload['pull_request']['user']['login']
                    from_branch = payload['pull_request']['head']['ref']
                    to_branch = payload['pull_request']['base']['ref']
                    timestamp = payload['pull_request']['created_at']
                    message = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}'
                elif action == 'closed' and payload['pull_request']['merged']:
                    action = 'MERGE'
                    author = payload['pull_request']['user']['login']
                    from_branch = payload['pull_request']['head']['ref']
                    to_branch = payload['pull_request']['base']['ref']
                    timestamp = payload['pull_request']['merged_at']
                    message = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp}'
            else:
                message = f'Unknown action type: {action_type}'
                action = 'UNKNOWN'

            # Print the formatted message
            print('---------', message, '--------')

            # Format the timestamp to UTC
            # timestamp_utc = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S')
            

            # Prepare the document to be inserted into MongoDB
            message = {
                "request_id": request_id if 'request_id' in locals() else None,
                "author": author,
                "action": action,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp
            }

            # Insert data into MongoDB
            collection.insert_one(message)

            # Return a success response to GitHub
            return 'Webhook received successfully!', 200
        except KeyError as e:
            # If any key is missing in the payload, return an error response
            return f'Missing key {e} in webhook payload', 400
    else:
        # Return an error response if the request does not contain JSON data
        return 'Invalid webhook payload format', 400

if __name__ == '__main__':
    app.run(debug=True)
