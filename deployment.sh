#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Starting deployment..."

echo "🔄 Activating virtual environment..."
source venv/bin/activate
pip install --upgrade pip

echo "📦 Installing common requirements..."
pip install -r requirements.txt

# Deploy Backend
echo "🚀 Deploying Backend..."
cd backend
gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000 --daemon
cd ..

# Deploy Frontend (Gradio)
echo "🎨 Launching Gradio Frontend..."
cd frontend
python run.py
cd ..

echo "✅ Deployment completed successfully!"
