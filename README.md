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

git clone https://github.com/your-username/action-repo.git
git clone https://github.com/your-username/webhook-repo.git

2. Install dependencies:

cd webhook-repo
pip install -r requirements.txt

3. Set up MongoDB:
   - Install MongoDB locally or use a cloud service like MongoDB Atlas.
   - Update the MongoDB connection URL in `app.py` with your database credentials.

4. Configure GitHub webhooks:
   - In the action-repo settings, add webhook URLs pointing to the Flask endpoint (`/webhook`) of webhook-repo.
   - Select the events to trigger the webhook (e.g., "Push", "Pull Request", "Merge").

5. Run the Flask backend:

python app.py or flask run by setting up (export FLASK_APP=app.py) in command and then call the "flask run"

6. Open the frontend UI:
   - Access `index.html` in your browser.
   - You should see the latest repository events displayed in the UI.

## Usage

- The frontend UI automatically fetches and updates events every 15 seconds.
- Events are displayed with a light background color based on their action type.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for any improvements or bug fixes.
