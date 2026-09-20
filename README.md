# Quiz API Server

A Django and Django REST Framework based backend for the JNTUH Results App's Quiz and Updates modules.

## Features
- **Quizzes**: Serve multiple quizzes to users. Ensures users complete quizzes in order or get the latest one.
- **Results**: Securely validate and store user answers and calculate scores on the server side.
- **Updates/Announcements**: Serve announcements and updates to the mobile application.

## Endpoints

### 1. Latest Quiz
`GET /api/latest_quiz/?user_token=<token>`
Fetches the latest available quiz for the user that hasn't been completed yet.

### 2. Save Results
`POST /api/save_results/`
Saves the user's answers and calculates their score.
**Payload:**
```json
{
  "quizId": 1,
  "user_token": "string",
  "user_name": "string",
  "results": [
    {
      "question_id": 1,
      "user_answer": "string"
    }
  ]
}
```

### 3. Updates
`GET /api/updates/`
Fetches a list of the latest announcements.

## Installation

1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate` (Mac/Linux)
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`
