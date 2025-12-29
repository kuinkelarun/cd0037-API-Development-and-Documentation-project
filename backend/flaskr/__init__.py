from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    with app.app_context():
        db.create_all()

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=["GET"])
    def get_categories():
        categories = Category.query.all()
        categories_list = {category.id: category.type for category in categories}
        return jsonify({ "categories": categories_list }), 200

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            page = request.args.get("page", 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            questions_query = Question.query.order_by(Question.id).all()
            formatted_questions = [
                {
                    "id": q.id,
                    "question": q.question,
                    "answer": q.answer,
                    "difficulty": q.difficulty,
                    "category": q.category,
                }
                for q in questions_query
            ]

            paginated = formatted_questions[start:start + QUESTIONS_PER_PAGE]

            if len(paginated) == 0 and page != 1:
                abort(404)

            categories = {c.id: c.type for c in Category.query.order_by(Category.id).all()}

            return jsonify({
                "success": True,
                "questions": paginated,
                "total_questions": len(formatted_questions),
                "categories": categories,
                "current_category": None
            }), 200
        except Exception:
            abort(422)

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)
            question.delete()
            return jsonify({"success": True, "deleted": question_id}), 200
        except Exception:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def add_question():
        try:
            data = request.get_json()
            question_text = data.get("question", None)
            answer_text = data.get("answer", None)
            category = data.get("category", None)
            difficulty = data.get("difficulty", None)

            if not all([question_text, answer_text, category, difficulty]):
                abort(400)

            new_question = Question(
                question=question_text,
                answer=answer_text,
                category=category,
                difficulty=difficulty
            )
            new_question.insert()

            return jsonify({"success": True, "created": new_question.id}), 201
        except Exception:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        try:
            data = request.get_json()
            search_term = data.get("searchTerm", "")

            if search_term == "":
                abort(400)

            results = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            formatted_results = [q.format() for q in results]

            return jsonify({
                "success": True,
                "questions": formatted_results,
                "total_questions": len(formatted_results),
                "current_category": None
            }), 200
        except Exception:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        try:
            category = Category.query.get(category_id)
            if category is None:
                abort(404)

            questions = Question.query.filter(Question.category == str(category_id)).all()
            formatted_questions = [q.format() for q in questions]

            return jsonify({
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(formatted_questions),
                "current_category": category.type
            }), 200
        except Exception:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            data = request.get_json()
            previous_questions = data.get("previous_questions", [])
            quiz_category = data.get("quiz_category", None)

            if quiz_category is None:
                abort(400)

            if quiz_category['id'] == 0:
                questions_query = Question.query
            else:
                questions_query = Question.query.filter(Question.category == str(quiz_category['id']))

            available_questions = questions_query.filter(~Question.id.in_(previous_questions)).all()

            if not available_questions:
                return jsonify({
                    "success": True,
                    "question": None
                }), 200

            next_question = random.choice(available_questions)

            return jsonify({
                "success": True,
                "question": next_question.format()
            }), 200
        except Exception:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable entity"
        }), 422
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500
    
    return app

