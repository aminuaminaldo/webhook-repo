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

