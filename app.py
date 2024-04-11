from flask import Flask, request, render_template, send_from_directory
from pymongo import MongoClient

app = Flask(__name__)

# Connection to MongoDB
client = MongoClient("mongodb+srv://aminuashraf198:Ud097ZRLvkefM3f5@githubcluster.bf6kgwk.mongodb.net/")
db = client["webhook_db"]
collection = db["repository_events"]

# Route to fetch repository events
@app.route('/get_events')
def get_events():
    # Retrieving the latest repository events from MongoDB
    events = collection.find().sort('timestamp', -1).limit(10)  # Get latest 10 events

    # Format events into HTML elements
    html_events = ''
    for event in events:
        # Determining the background color based on action type
        if event['action'] == 'PUSH':
            bg_color = 'lightblue'
        elif event['action'] == 'PULL_REQUEST':
            bg_color = 'lightgreen'
        elif event['action'] == 'MERGE':
            bg_color = 'lightyellow'
        else:
            bg_color = 'lightgrey'
        
        # Formating the event message
        if event['action'] == 'PUSH':
            message = f"{event['author']} pushed to {event['to_branch']} on {event['timestamp']}"
        elif event['action'] == 'PULL_REQUEST':
            message = f"{event['author']} submitted a pull request from {event['from_branch']} to {event['to_branch']} on {event['timestamp']}"
        elif event['action'] == 'MERGE':
            message = f"{event['author']} merged branch {event['from_branch']} to {event['to_branch']} on {event['timestamp']}"
        else:
            message = "Unknown action type"

        # Constructing HTML element for the event
        html_event = f'<div style="background-color: {bg_color}; padding: 10px; margin-bottom: 5px;">{message}</div>'
        html_events += html_event

    return html_events

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    # Verifying that the request contains JSON data
    if request.is_json:
        # Parse the JSON payload
        payload = request.json

        # Here we will extract relevant data from the payload
        try:
            action_type = request.headers.get('X-Github-Event')

            # Now format the message based on the action type
            if action_type == 'push':
                action = 'PUSH'
                author = payload['pusher']['name']
                to_branch = payload['ref'].split('/')[-1]  # Extracting the branch name from the ref
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

            # Printing the formatted message
            print('---------', message, '--------')

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
            # If any key is missing in the payload, we will return an error response
            return f'Missing key {e} in webhook payload', 400
    else:
        # Here we will Return an error response if the request does not contain JSON data
        return 'Invalid webhook payload format', 400

if __name__ == '__main__':
    app.run(debug=True)
