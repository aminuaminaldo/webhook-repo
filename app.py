from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome Webhook Repo with GitHub!'

@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    # Verify that the request contains JSON data
    if request.is_json:
        # Parse the JSON payload
        payload = request.json
        
        # Extract relevant data from the payload
        author = payload.get('author')
        branches = payload.get('branches')
        timestamp = payload.get('timestamp')
        action_type = payload.get('action_type')
        
        # Print the extracted data for testing
        print("Author:", author)
        print("Branches:", branches)
        print("Timestamp:", timestamp)
        print("Action Type:", action_type)
        
        # Here we can add code to store the extracted data to MongoDB or perform other actions
        
        # Return a success response to GitHub
        return 'Webhook received successfully!', 200
    else:
        # Return an error response if the request does not contain JSON data
        return 'Invalid webhook payload format', 400

if __name__ == '__main__':
    app.run(debug=True)
