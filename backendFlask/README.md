# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server for Windows, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Reference

### Getting Started

- Backend Base URL: `http://127.0.0.1:5000/`
- Frontend Base URL: `http://127.0.0.1:3000/`
- Authentication: Authentication or API keys are not used in the project yet.

### Error Handling

Errors are returned in the following json format:

```json
{
  "success": "False",
  "error": 404,
  "message": "Resource not found"
}
```

The error codes currently returned are:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error

### Endpoints

#### GET /categories

- General:

  - Returns all the categories.

- Sample: `curl http://127.0.0.1:5000/categories`

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### GET /questions

- General:

  - Returns all questions
  - Returns all categories
  - questions are paginated so we list first 10 questions.
  - pages could be requested by a query string

- Sample: `curl http://127.0.0.1:5000/questions`<br>

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### DELETE /questions/<int:id\>

- General:

  - Deletes a question by id form the url parameter.

- Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`

```json
{
  "success": "True",
  "message": "Question successfully deleted"
}
```

#### POST /questions

- General:

  - Creates a new question based on a payload.

- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "new question", "answer": "new answer", "difficulty": 3, "category": "4" }'`

```json
{
  "message": "Question successfully created!",
  "success": true
}
```

#### POST /questions/search

- General:

  - returns questions that has the search substring

- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "author"}'`

```json
{
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true
}
```

#### GET /categories/<int:id\>/questions

- General:
  - Gets questions by category using the id from the url parameter.
- Sample: `curl http://127.0.0.1:5000/categories/5/questions`<br>

```json
{
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "success": true
}
(env)
Mr Saher@Saher MINGW64 /d/codes/python/flask/02_trivia_apiMySubmission (master)
$ curl http://127.0.0.1:5000/categories/5/questions
{
  "categories": "Entertainment",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "new",
      "category": 5,
      "difficulty": 4,
      "id": 24,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 26,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "totalQuestions": 4
}
```

#### POST /quizzes

- General

  - Takes the category and previous questions in the request.
  - Return random question not in previous questions.

- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [4, 9], "quiz_category": {"type": "History", "id": "4"}}'`

```json
{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  "success": true
}
```

## Authors

- Saher AbdElaziz worked on the APIs and test suite to integrate with the frontend

- Udacity provided the starter files for the project including the frontend
