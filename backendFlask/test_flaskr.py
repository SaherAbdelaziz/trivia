import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    #database_name = "trivia"
    # database_path = "postgres://postgres:Password123!@{}/{}".format(
    # 'localhost:5432', database_name)

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://postgres:Password123!@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    '''
    test Categories get all ,  Get Questions Per Category , invalid id 
    '''

    def test_get_all_categories(self):
        """Test for get_all_categories

        Tests for the status code for success is true, and the length of
        the returned categories
        """

        # make request
        response = self.client().get('/categories')
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_get_guestions_per_category(self):
        """Test for getting questions Per category"""

        # make a request for the History category with id of 4
        response = self.client().get('/categories/4/questions')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['categories'], 'History')

    def test_invalid_category_id(self):
        """Test for invalid category id"""

        # request with invalid category id 100
        response = self.client().get('/categories/100/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')  # 404

    '''
    test Questions get all q and paginaion 10 , delete Question  , unsuccessful deletion of question id not exitst
    '''

    def test_get_paginated_questions(self):
        """
        Test for get all questions and they ar 10 q

        """
        # make request and process response
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 10)

    def test_success_ful_guestion_delete(self):
        """
        Test for deleting a question.

        create new q to test delete
        """

        # create new question and get id
        question = Question(
            question='new q',
            answer='new ans',
            difficulty=1,
            category='1')

        question.insert()

        response = self.client().delete(
            '/questions/{}'.format(question.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Question successfully deleted")

    def test_delete_question_id_not_exist(self):
        """
        unsuccessful deletion of question
        """

        # unsuccessful delete

        response = self.client().delete('/questions/9999999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    test Questions create new q , create new q with no data  ,search ,search not found ,  search no data
    '''

    def test_create_question(self):
        """
        Test for creating question
        """

        # simple q
        question = {
            'question': 'This is a simple question',
            'answer': 'this is a simple answer',
            'difficulty': 1,
            'category': 1,
        }

        # make request and process response
        response = self.client().post('/questions/new', json=question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question successfully created!')

    def test_create_cuestion_with_no_data(self):
        """
        Test for ensuring data with empty fields are not processed
        """
        request_data = {
            'question': 'qqqq',
            'answer': '',
            'difficulty': 1,
            'category': 1,
        }

        # make request and process response
        response = self.client().post('/questions/new', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    def test_search_questions(self):
        """
        Test for searching for a question.
        """

        request_data = {
            'searchTerm': 'Who discovered penicillin?',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_search_term_not_found(self):
        """
        Test for search term not found
        """

        request_data = {
            'searchTerm': 'dfjdtrertwfresyg346474yg',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_no_data(self):
        """
        Test for empty search term
        """

        request_data = {
            'searchTerm': '',
        }

        # make request and process response
        response = self.client().post('/questions/search', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    '''
    test page 
    '''

    def test_error_for_out_of_boundPage(self):
        """
        Test for out of bound page
        returns a 404 error
        """

        # make request and process response
        response = self.client().get('/questions?page=10000000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    '''
    test play game ok , no data 
    '''

    def test_play(self):
        """
        Test playing quiz questions
        """

        request_data = {
            'previous_questions': [4],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 5
            }
        }

        # make request and process response
        response = self.client().post('/quizzes/play', json=request_data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        # Ensures previous questions are not returned
        self.assertNotEqual(data['question']['id'], 4)

        # Ensures returned question is in the correct category
        self.assertEqual(data['question']['category'], 5)

    def test_no_data_play(self):
        """
        Test for the case where no data is sent
        """

        # process response from request without sending data
        response = self.client().post('/quizzes/play', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request error')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
