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
# gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000 --daemon
uvicorn app:app --host 0.0.0.0 --port 8000
cd ..

# Wait for backend to be available
echo "⏳ Waiting for backend to start..."
for i in {1..10}; do
  if curl -s http://localhost:8000/docs > /dev/null; then
    echo "✅ Backend is up!"
    break
  fi
  echo "⌛ Still waiting..."
  sleep 1
done

# Deploy Frontend (Gradio)
echo "🎨 Launching Gradio Frontend..."
cd frontend
python run.py
cd ..

echo "✅ Deployment completed successfully!"
