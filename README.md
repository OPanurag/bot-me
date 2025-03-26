# BOT-ME: AI Assistant

BOT-ME is a chatbot that answers questions based on predefined data from a PDF. 
This project uses Streamlit for the frontend, with a backend API that processes the user's query. 
The backend can be configured to use either GPT or Gemini for responses.

## **Setup Instructions for Local Development**

Follow these steps to set up and run the project locally.

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/bot-me.git
cd bot-me
```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install --upgrade pip  # Ensure pip is up to date
pip install -r requirements.txt
```

### **4️⃣ Configure API Keys**
`backend/config.py` and add your API keys for OpenAI and Gemini.
```python
# backend/config.py
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR-OPENAI-API-KEY-HERE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR-GEMINI-API-KEY-HERE")
```

### **5️⃣ Run the Backend**
Open a terminal and run:
```bash
python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

### **6️⃣ Run the Frontend**
In a new terminal window, start the Streamlit app:
```bash
streamlit run frontend/app.py
```

Your chatbot will be accessible at **http://localhost:8501**.

---

## **Deployment on Render**

### **1️⃣ Backend Deployment on Render**
1. **Create a New Web Service** on [Render](https://render.com/).
2. **Connect your GitHub repo** and select the `bot-me` repository.
3. **Set Environment Variables:**
   - `OPENAI_API_KEY`: Your OpenAI API Key
   - `GEMINI_API_KEY`: Your Gemini API Key
4. **Set the Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt
   ```
5. **Set the Start Command:**
   ```bash
   python -m uvicorn backend.app:app --host 0.0.0.0 --port 8000
   ```
6. Click **Deploy** and wait for the backend to be deployed.

### **2️⃣ Frontend Deployment on Render**
1. Create a **New Static Site** on Render.
2. **Connect to the same GitHub repository.**
3. **Set the Build Command:**
   ```bash
   pip install --upgrade pip && pip install -r requirements.txt && streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
   ```
4. **Set the Publish Directory to `frontend/`.**
5. Click **Deploy** and wait for the frontend to be deployed.

Your chatbot will be accessible at the provided Render URL!

---

## **Notes**
- Ensure `backend/config.py` is added to `.gitignore` so that API keys are not pushed to GitHub.
- To update the deployment, push your changes to GitHub, and Render will automatically redeploy the app.
- If deployment fails, check the Render logs for debugging.

---

Now your chatbot is live and accessible on the web! 🚀
