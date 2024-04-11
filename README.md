# GitHub Webhook Integration 
This repository contains code for integrating GitHub webhooks with a Flask backend and MongoDB database. It captures events such as "Push", "Pull Request", and "Merge" actions and displays them in a user-friendly UI.

## Overview

The project consists of two main components:

1. **Flask Backend (webhook-repo):**
   - Receives webhook payloads from GitHub.
   - Parses and stores events in a MongoDB database.
   - Provides endpoints to fetch and format events for the frontend.

2. **Frontend UI:**
   - Fetches events from the Flask backend using AJAX requests.
   - Displays events in a clean and minimalistic UI.
   - Automatically updates every 15 seconds to show the latest events.

## Installation

1. Clone the repository:
   
git clone https://github.com/aminuaminaldo/action-repo
git clone https://github.com/aminuaminaldo/webhook-repo
3. Install dependencies:
cd webhook-repo
pip install -r requirements.txt


4. Set up MongoDB:
   - Install MongoDB locally or use a cloud service like MongoDB Atlas.
   - Update the MongoDB connection URL in `app.py` with your database credentials.

5. Expose Flask backend using ngrok:
   - Download and install ngrok from https://ngrok.com/download.
   - Run ngrok to expose your local server:
ngrok http http://127.0.0.1:5000
Copy the generated ngrok URL in the forwarded url (e.g., `https://<ngrok_subdomain>.ngrok.io`).
and you can see the UI

6. Configure GitHub webhooks:
   - In the action-repo settings, add webhook URLs pointing to the Flask endpoint (`/webhook`) of webhook-repo.
   - Select the events to trigger the webhook (e.g., "Push", "Pull Request", "Merge").

7. Run the Flask backend:
python app.py or flask run by setting up (export FLASK_APP=app.py) in command and then call the "flask run"

8. Open the frontend UI:
   - Access `index.html` in your browser.
   - You should see the latest repository events displayed in the UI.
   - you can make changes (e.g., "Push", "Pull Request", "Merge"). to the action-repo https://github.com/aminuaminaldo/action-repo to add the events or data in MongoDB.

## Usage

- The frontend UI automatically fetches and updates events every 15 seconds.
- Events are displayed with a light background color based on their action type.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for any improvements or bug fixes.
