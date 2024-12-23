# Medical Facility Management Bot API

This project offers an API for managing interactions in a medical facility. It utilizes a language model to understand and process natural language commands and provide structured JSON responses.

## Requirements

Before getting started, ensure the following prerequisites are met:

- Python 3.8+
- MongoDB running and accessible at `mongodb://localhost:27017`

## Installation Guide

Follow these steps to set up and install the API:

### 1. Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/management-bot-api.git
cd management-bot-api
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Ensure MongoDB is Running

Make sure MongoDB is active and accessible at `mongodb://localhost:27017`.

## Running the API Server

Start the API server by running the following command:

```bash
uvicorn bot_api:app --host 0.0.0.0 --port 6000
```

The API will now be live at `http://localhost:6000`.

## API Endpoints Overview

### Create a New Conversation

- **Method:** `GET`
- **Endpoint:** `/generate_conversation_id`
- **Description:** Initializes a new conversation and returns a unique conversation ID.
- **Response:**
    ```json
    {
        "conversation_id": "unique-conversation-id"
    }
    ```

### Process User Input

- **Method:** `POST`
- **Endpoint:** `/conversation`
- **Description:** Accepts user input and returns the bot's response, identifying the intent and extracting key entities.
- **Request Example:**
    ```json
    {
        "conversation_id": "unique-conversation-id",
        "user_input": "Add a new patient Mickel jhon, male, 50 years old, with hypertension."
    }
    ```
- **Response Example:**
    ```json
    {
        "intent": "add_patient",
        "entities": {
            "name": "Mickel jhon",
            "gender": "male",
            "age": 50,
            "condition": "Hypertension"
        },
        "message": "Patient Mickel Jhon successfully added. Profile created with the provided details."
    }
    ```

## Sample API Interactions

### Adding a New Patient

1. To generate a conversation ID, send a GET request to:
    ```bash
    curl -X GET "http://localhost:6000/generate_conversation_id"
    ```

2. After receiving the conversation ID, use it to add a new patient with the following POST request:
    ```bash
    curl -X POST "http://localhost:6000/conversation" -H "Content-Type: application/json" -d '{
        "conversation_id": "unique-conversation-id",
        "user_input": "Add a new patient Mickel jhon, male, 50 years old, with hypertension."
    }'
    ```

### Assigning Medication

1. To assign medication, use the conversation ID in this POST request:
    ```bash
    curl -X POST "http://localhost:6000/conversation" -H "Content-Type: application/json" -d '{
        "conversation_id": "unique-conversation-id",
        "user_input": "Assign medication Paracetamol 500mg twice a day for Mickel Jhon."
    }'
    ```

### Scheduling a Follow-Up

1. To schedule a follow-up, use the conversation ID for the following POST request:
    ```bash
    curl -X POST "http://localhost:6000/conversation" -H "Content-Type: application/json" -d '{
        "conversation_id": "unique-conversation-id",
        "user_input": "Schedule a follow-up for Mickel jhon on December 20th."
    }'
    ```

## Testing the API

To run tests for the API, simply execute the following:

```bash
pytest
```
