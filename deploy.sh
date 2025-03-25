#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting deployment..."

# Navigate to backend and deploy
echo "Deploying Backend..."
cd backend
pip install -r requirements.txt
gunicorn -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000 --daemon
cd ..

# Navigate to frontend and deploy
echo "Deploying Frontend..."
cd frontend

# If using Streamlit
if [ -f "app.py" ]; then
    pip install -r requirements.txt
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.enableCORS false
else
    npm install
    npm run build
    npm start
fi

cd ..

echo "Deployment completed successfully!"
