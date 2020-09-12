import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

nOfQuestions = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    done
    '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        """ Set Access Control """

        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    done
    '''
    @app.route('/categories', methods=['GET'])
    def GetCategories():
        """
        This endpoint returns all categories or status code 500 if there is a server error
        """

        try:
            Allcategories = Category.query.all()

            categories = {}
            for category in Allcategories:
                categories[category.id] = category.type

            # return successful response
            return jsonify({
                'success': True,
                'categories': categories
            }), 200
        except Exception:
            abort(500)

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 
    done
    '''
    @app.route('/questions', methods=['GET'])
    def GetQuestions():
        """
        an endpoint to handle GET requests for questions, 
        including pagination (every 10 questions).  and returns a 404
        when the page is out of bound
        nOfQuestions is a global variable
        """

        questions = Question.query.order_by(Question.id).all()
        total_questions = len(questions)
        Allcategories = Category.query.order_by(Category.id).all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * nOfQuestions
        end = start + nOfQuestions

        questions = [question.format() for question in questions]
        current_questions = questions[start:end]

        # return 404 if there are no questions for the page number
        if (len(current_questions) == 0):
            abort(404)

        categories = {}
        for category in Allcategories:
            categories[category.id] = category.type

        # return values if there are no errors
        return jsonify({
            'success': True,
            'total_questions': total_questions,
            'categories': categories,
            'questions': current_questions
        }), 200
    '''

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    done

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def DeleteQuestion(id):
        '''
        An endpoint to DELETE question using an ID.
        if any erorr expet send 422
        '''
        try:
            question = Question.query.get(id)
            question.delete()

            return jsonify({
                'success': True,
                'message': "Question successfully deleted",
                'delete_id': id
            })
        except Exception:
            abort(422)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
    '''

    @app.route('/questions/new', methods=['POST'])
    def NewQuestion():
        '''
        An endpoint to POST a new question,retrurn 422 if data is not completed 
        '''
        # get data
        question = request.get_json().get('question', '')
        answer = request.get_json().get('answer', '')
        difficulty = request.get_json().get('difficulty', '')
        category = request.get_json().get('category', '')

        # validation
        if ((question == '') or (answer == '')
                or (difficulty == '') or (category == '')):
            abort(422)

        try:
            # Create a new question
            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category)

            # save question
            question.insert()

            # return success message
            return jsonify({
                'success': True,
                'message': 'Question successfully created!'
            }), 201  # ok created

        except Exception:
            abort(422)

    '''

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        '''
        Create a POST endpoint to get questions based on a search term 
        '''

        search_term = request.get_json().get('searchTerm', '')

        # Return 422 status code if empty search term is sent
        if search_term == '':
            abort(422)

        try:
            # get all questions that has the search term substring
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # if there are no questions for search term return 404
            if len(questions) == 0:
                abort(404)

            page = request.args.get('page', 1, type=int)
            start = (page - 1) * nOfQuestions
            end = start + nOfQuestions

            questions = [question.format() for question in questions]
            current_questions = questions[start:end]

            # return response if successful
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            }), 200

        except Exception:
            # This error code is returned when 404 abort
            # raises exception from try block
            abort(404)

    '''

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
