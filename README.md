# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

## API Endpoints

Base URL: `http://127.0.0.1:5000`

---

### GET /categories
- Description: Fetches all categories as a dictionary of `id: type`.
- Request args: None
- Response (200):

```json
{
	"success": true,
	"categories": {
		"1": "Science",
		"2": "Art",
		"3": "Geography",
		"4": "History",
		"5": "Entertainment",
		"6": "Sports"
	}
}
```

---

### GET /questions
- Description: Fetches paginated questions (10 per page), list of categories and total count.
- Request args:
	- `page` (optional, integer) — page number, default `1`
- Response (200):

```json
{
	"success": true,
	"questions": [
		{
			"id": 1,
			"question": "What is H2O?",
			"answer": "Water",
			"difficulty": 1,
			"category": "1"
		}
		// up to 10 items
	],
	"total_questions": 30,
	"categories": {
		"1": "Science",
		"2": "Art"
	},
	"current_category": null
}
```
- Errors:
	- `404` if requested page has no results (page > available pages)
	- `422` on other failures

---

### DELETE /questions/{question_id}
- Description: Deletes the question with the given id.
- Request args: `question_id` (path)
- Response (200):

```json
{
	"success": true,
	"deleted": 5
}
```
- Errors:
	- `404` if question not found
	- `422` on failure

---

### POST /questions
- Description: Adds a new question.
- Request body (JSON):

```json
{
	"question": "What is the capital of France?",
	"answer": "Paris",
	"category": "3",
	"difficulty": 2
}
```
- Response (201/200):

```json
{
	"success": true,
	"created": 27
}
```
- Errors:
	- `400` for missing fields
	- `422` on failure

---

### POST /questions/search
- Description: Searches questions by a search term (case-insensitive substring match).
- Request body (JSON):

```json
{ "searchTerm": "H2O" }
```
- Response (200):

```json
{
	"success": true,
	"questions": [ /* matching questions */ ],
	"total_questions": 1,
	"current_category": null
}
```

---

### GET /categories/{category_id}/questions
- Description: Fetches questions for the given category.
- Request args: `category_id` (path)
- Response (200):

```json
{
	"success": true,
	"questions": [ /* category questions */ ],
	"total_questions": 1,
	"current_category": "History"
}
```

---

### POST /quizzes
- Description: Returns a random question for quizzes, respecting `previous_questions` and optional category filter.
- Request body (JSON):

```json
{
	"previous_questions": [5,9],
	"quiz_category": { "id": 1, "type": "Science" }
}
```
- Response (200) when a question is available:

```json
{
	"success": true,
	"question": { "id": 12, "question": "What is H2O?", "answer": "Water", "difficulty": 1, "category": "1" }
}
```
- Response (200) when no questions remain:

```json
{ "success": true, "question": null }
```

---

### Error responses (format for 400/404/422/500)

```json
{
	"success": false,
	"error": 404,
	"message": "Resource not found"
}
```

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.
