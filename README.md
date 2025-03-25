# BOT-ME: AI Assistant

BOT-ME is a chatbot that answers questions based on predefined data from a PDF. 
This project uses Streamlit for the frontend, with a backend API that processes the user's query. 
The backend can be configured to use either GPT or Gemini for responses.

## Requirements

### Dependencies

To run the project locally, you need to install the following dependencies:

- Python 3.x

### Dependencies Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. In the `config.py` file, set your API key for the backend. The API key will be used for either GPT or Gemini depending on your choice.

2. In the `backend/app.py`, select which API (GPT or Gemini) to use by commenting/uncommenting the relevant section of code:
    - For **GPT**:
        ```python
        # Uncomment the GPT API Code on Line 102
        response = generate_chatgpt_response(question, user_data)  # OpenAI GPT Response
        ```
    - For **Gemini**:
        ```python
        # Uncomment the Gemini API Code on Line 103
        response = generate_gemini_response(question, user_data)   # Google Gemini Response
        ```

## Running the Project Locally

### Step 1: Start the Backend

1. Open a terminal window and navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2. Start the backend server with **Uvicorn**:
    ```bash
    uvicorn app:app --reload
    ```

   This will start the backend server on `http://localhost:8000`. The `--reload` option ensures the server reloads automatically if you make changes to the code.

### Step 2: Start the Frontend

1. Open a second terminal window and navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

   This will open the frontend in your browser, typically at `http://localhost:8501`.

## Usage

1. **Ask a Question:** Enter a question in the input field at the bottom of the screen and click "Send."
2. **Response:** The chatbot will answer your question based on the predefined data from the PDF.
3. **Text-to-Speech:** The bot's response will also be read aloud using pyttsx3.
4. **Scroll History:** You can scroll through the chat history to review previous conversations.

## Contributing

Feel free to contribute by forking the repository and submitting a pull request with your changes.

---

Enjoy using BOT-ME! 🤖
