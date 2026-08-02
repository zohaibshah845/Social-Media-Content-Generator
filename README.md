 Automated Social Media Content Generator

A full-stack application that generates 30 days of social media posts (captions and hashtags) using AI, automatically creates matching graphics with the Canva API, and schedules posts directly to Facebook, Instagram, and LinkedIn. Built for small businesses, it saves over 10 hours per week on content creation.

**Features**

AI Powered Content - Generate 30 days of engaging captions and hashtags using OpenAI GPT-4.

Automated Graphics - Create branded images via the Canva API or placeholders matching your brand colours.

Multi-Platform Scheduling - Publish to Facebook, Instagram, and LinkedIn with a single click.

Secure Authentication - Firebase Authentication for user management.

Post Management - View, edit, and track all generated posts in a calendar dashboard.

Fast and Scalable - Built with FastAPI (async) and React for a modern, high-performance experience.

**Tech Stack**

Frontend - React with Context API and React Router

Backend API - FastAPI with Python 3.10 or higher

AI Generation - OpenAI GPT-4o

Graphics - Canva API with placeholder fallback

Scheduling - Facebook Graph API, Instagram Graph API, LinkedIn API

Database - Firebase Firestore (NoSQL)

Authentication - Firebase Authentication with JWT tokens

Deployment - Docker and cloud-ready

**Getting Started**

Prerequisites

Python 3.10 or higher

Node.js 16 or higher and npm

Firebase account with Firestore and Authentication enabled

API keys for OpenAI, Canva, Facebook, Instagram, and LinkedIn if you want to enable those services

Clone the Repository

git clone https://github.com/yourusername/social-content-generator.git
cd social-content-generator

Backend Setup

cd backend
python -m venv venv
source venv/bin/activate
On Windows use venv\Scripts\activate
pip install -r requirements.txt

Create a .env file in the backend directory with your environment variables. Place your Firebase Admin SDK JSON key file at backend/credentials/firebase-adminsdk.json.

Run the server:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

The API will be available at http://localhost:8000 and interactive docs at http://localhost:8000/docs.

Frontend Setup

cd frontend
npm install

Create a .env file in frontend with REACT_APP_API_URL=http://localhost:8000/api/v1. Optionally add Firebase client SDK config if you want to use it directly on the frontend.

Start the development server:

npm start

The app will be available at http://localhost:3000.

**Environment Variables**

Backend .env

OPENAI_API_KEY=your_openai_key
CANVA_ACCESS_TOKEN=your_canva_token
FACEBOOK_PAGE_ACCESS_TOKEN=your_fb_token
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_ig_account_id
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_CREDENTIALS_PATH=credentials/firebase-adminsdk.json

Frontend .env

REACT_APP_API_URL=http://localhost:8000/api/v1

**API Endpoints**

All endpoints are prefixed with /api/v1.

POST /signup - Create a new user account. No authentication required.

POST /login - Message only. Token handled by Firebase. No authentication required.

POST /generate - Generate 30 days of posts. Requires Bearer token authentication.

POST /graphics/{post_id} - Generate a graphic for a specific post. Requires Bearer token authentication.

POST /schedule - Schedule a post to selected platforms. Requires Bearer token authentication.

GET /posts - List all posts for the current user. Requires Bearer token authentication.

Authentication: Include the Firebase ID token in the Authorization header as Bearer token.

**Project Structure**

social-content-generator/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── firebase.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── routes.py
│   │   └── services/
│   │       ├── openai.py
│   │       ├── canva.py
│   │       ├── social.py
│   │       └── firestore.py
│   ├── credentials/
│   │   └── firebase-adminsdk.json
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── .env
├── .gitignore
└── README.md

**Testing**

Backend with pytest

cd backend
pytest tests/

Frontend with Jest

cd frontend
npm test

**Deployment**

You can containerise the application with Docker. Create a docker-compose.yml file with backend and frontend services. Build and run both services using docker-compose up -d. For production, consider using a cloud platform like AWS, GCP, or Heroku with environment variables set securely.

**Contributing**

Contributions are welcome. Please open an issue or submit a pull request.

**License**

This project is licensed under the MIT License. See the LICENSE file for details.

**Acknowledgements**

OpenAI for the powerful GPT models

Firebase for authentication and database

FastAPI for the lightning-fast framework

Canva for design capabilities

**Contact**

For any questions or feedback, please open an issue on GitHub or reach out to zohaibshahnaqvi574@gmail.com.

Happy posting