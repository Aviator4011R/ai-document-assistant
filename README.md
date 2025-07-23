# AI Document Assistant - Deployment Package

## Overview

This package contains the complete AI Document Assistant application ready for deployment. The application is designed to ingest aviation manuals and provide intelligent Q&A functionality with voice input/output capabilities.

## Package Contents

```
ai-document-assistant-deploy/
├── backend/                    # Backend Flask application
│   ├── src/                   # Source code
│   ├── data/                  # Processed document data
│   ├── static/                # Frontend build files
│   ├── documents/             # Document storage
│   ├── app.py                 # Production Flask app
│   ├── requirements.txt       # Python dependencies
│   └── Procfile              # Deployment configuration
├── USER_MANUAL.md            # User documentation
└── README.md                 # This file
```

## Quick Deployment

### Option 1: Heroku Deployment

1. Install Heroku CLI
2. Navigate to the `backend` directory
3. Initialize git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   ```
4. Create Heroku app:
   ```bash
   heroku create your-app-name
   ```
5. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set SECRET_KEY=your_secret_key
   ```
6. Deploy:
   ```bash
   git push heroku main
   ```

### Option 2: Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SECRET_KEY`: A secure secret key
3. Deploy from the `backend` directory

### Option 3: Vercel Deployment

1. Install Vercel CLI: `npm i -g vercel`
2. Navigate to the `backend` directory
3. Run: `vercel`
4. Follow the prompts to deploy

## Environment Variables

The following environment variables are required:

- `OPENAI_API_KEY`: Your OpenAI API key for AI functionality
- `SECRET_KEY`: Flask secret key for session management
- `PORT`: Port number (automatically set by most platforms)

## Local Development

To run locally for testing:

1. Navigate to the `backend` directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   export SECRET_KEY=your_secret_key
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Document Replacement

To replace the current POH document:

1. Replace the PDF file in the `documents/` directory
2. Update the document processing script
3. Re-run the document ingestion process
4. Redeploy the application

## Features Included

- ✅ Complete POH document ingestion (1967 Piper Cherokee PA-32-300)
- ✅ Text-based Q&A functionality
- ✅ Voice input capability (browser-based)
- ✅ ElevenLabs text-to-speech integration
- ✅ Professional Red Raven branding
- ✅ Responsive design for desktop and mobile
- ✅ Document-only knowledge source
- ✅ Aviation-grade interface design

## Support

For deployment assistance or technical support:
- Email: support@redravenllc.ai
- Documentation: USER_MANUAL.md

## License

© 2025 Red Raven LLC | AI SOFTWARE | Version 1.0.0

