from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, TestForm
from app.models import User, Test, Question, Attempt, Response
import csv
import os
import csv
from io import TextIOWrapper

bp = Blueprint('routes', __name__)

@bp.route("/")
@bp.route("/home")
def home():
    return render_template('home.html')

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@bp.route("/dashboard")
@login_required
def dashboard():
    tests = Test.query.filter_by().all()
    return render_template('dashboard.html', title='Dashboard', tests=tests)

@bp.route("/test/new", methods=['GET', 'POST'])
@login_required
def new_test():
    form = TestForm()
    if form.validate_on_submit():
        test = Test(title=form.title.data, description=form.description.data, allow_retake=form.allow_retake.data, author=current_user)
        db.session.add(test)
        db.session.commit()
        flash('Your test has been created!', 'success')
        return redirect(url_for('routes.upload_questions', test_id=test.id))
    return render_template('create_test.html', title='New Test', form=form)

@bp.route("/test/<int:test_id>")
@login_required
def test_detail(test_id):
    test = Test.query.get_or_404(test_id)
    questions_exist = test.questions
    if questions_exist:
        questions_exist = True
    else:
        questions_exist = False
    attempts = Attempt.query.filter_by(test_id=test.id).all()

    return render_template('test_detail.html', title=test.title, test=test, questions_exist=questions_exist, attempts=attempts)

@bp.route('/test/<int:test_id>/upload', methods=['GET', 'POST'])
@login_required
# def upload_questions(test_id):
#     test = Test.query.get_or_404(test_id)
    
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and file.filename.endswith('.csv'):
#             try:
#                 file_content = file.read().decode('utf-8')
#                 csv_reader = csv.reader(file_content.splitlines())
#                 for row in csv_reader:
#                     if len(row) == 6:
#                         question_text, option1, option2, option3, option4, answer = row
#                         question = Question(
#                             question=question_text,
#                             option1=option1,
#                             option2=option2,
#                             option3=option3,
#                             option4=option4,
#                             answer=int(answer),
#                             test_id=test.id
#                         )
#                         db.session.add(question)
#                 db.session.commit()
#                 flash('Questions uploaded successfully!', 'success')
#                 return redirect(url_for('routes.test_detail', test_id=test.id))
#             except Exception as e:
#                 flash(f'Error uploading questions: {e}', 'danger')
#         else:
#             flash('Please upload a valid CSV file.', 'danger')
    
#     return render_template('upload_questions.html', title='Upload Questions', test=test)
def upload_questions(test_id):
    test = Test.query.get_or_404(test_id)

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and file.filename.endswith('.csv'):
            try:
                csv_reader = csv.reader(TextIOWrapper(file, 'utf-8'))
                next(csv_reader)  # Skip header row
                
                for row in csv_reader:
                    print(row)
                    if len(row) == 6:
                        question = Question(
                            question_text=row[0],
                            option1=row[1],
                            option2=row[2],
                            option3=row[3],
                            option4=row[4],
                            answer=int(row[5]),
                            test_id=test.id
                        )
                        db.session.add(question)
                
                db.session.commit()
                flash('Questions uploaded successfully!', 'success')
                return redirect(url_for('routes.test_detail', test_id=test.id))
            
            except ValueError as e:
                flash(f'Error uploading questions: {e}', 'danger')
            
            except Exception as e:
                flash(f'Error uploading questions: {e}', 'danger')
        
        else:
            flash('Please upload a valid CSV file.', 'danger')

    return render_template('upload_questions.html', title='Upload Questions', test=test)

# @bp.route("/test/<int:test_id>/attempt", methods=['GET', 'POST'])
# @login_required
# def attempt_test(test_id):
#     test = Test.query.get_or_404(test_id)
#     questions = test.questions
#     if request.method == 'POST':
#         score = 0
#         responses = []
#         for question in questions:
#             selected_option = request.form.get(str(question.id))
#             if selected_option and int(selected_option) == question.answer:
#                 score += 1
#             response = Response(question_id=question.id, selected_option=int(selected_option), attempt_id=attempt.id)
#             responses.append(response)
#         attempt = Attempt(user_id=current_user.id, test_id=test.id, score=score)
#         db.session.add(attempt)
#         db.session.commit()
#         for response in responses:
#             response.attempt_id = attempt.id
#             db.session.add(response)
#         db.session.commit()
#         flash('Your test has been submitted!', 'success')
#         return redirect(url_for('routes.attempt_detail', attempt_id=attempt.id))
#     return render_template('attempt_test.html', title=test.title, test=test, questions=questions)

@bp.route("/test/<int:test_id>/attempt", methods=['GET', 'POST'])
@login_required
def attempt_test(test_id):
    test = Test.query.get_or_404(test_id)
    questions = test.questions

    if request.method == 'POST':
        score = 0
        responses = []
        
        attempt = Attempt(user_id=current_user.id, test_id=test.id, score=score)
        db.session.add(attempt)
        db.session.commit()

        for question in questions:
            selected_option = request.form.get(str(question.id))
            if selected_option and int(selected_option) == question.answer:
                score += 1
            
            response = Response(
                question_id=question.id,
                selected_option=int(selected_option) if selected_option else None,
                attempt_id=attempt.id
            )
            responses.append(response)
        
        db.session.bulk_save_objects(responses)
        db.session.commit()

        attempt.score = score
        db.session.commit()

        flash('Your test has been submitted!', 'success')
        return redirect(url_for('routes.attempt_detail', attempt_id=attempt.id))
    
    return render_template('attempt_test.html', title=test.title, test=test, questions=questions)

# @bp.route("/attempt/<int:attempt_id>")
# @login_required
# def attempt_detail(attempt_id):
#     attempt = Attempt.query.get_or_404(attempt_id)
#     return render_template('attempt_detail.html', title='Attempt Detail', attempt=attempt)
@bp.route("/attempt/<int:attempt_id>", methods=['GET'])
@login_required
def attempt_detail(attempt_id):
    attempt = Attempt.query.get_or_404(attempt_id)
    responses = Response.query.filter_by(attempt_id=attempt.id).all()

    questions = []
    for response in responses:
        question = Question.query.get(response.question_id)
        questions.append(question)
        if response.selected_option == 1:
            response.selected_option = question.option1
        elif response.selected_option == 2:
            response.selected_option = question.option2
        elif response.selected_option == 3:
            response.selected_option = question.option3
        elif response.selected_option == 4:
            response.selected_option = question.option4
        else:
            response.selected_option = "None"

        if question.answer == 1:
            question.answer = question.option1
        elif question.answer == 2:
            question.answer = question.option2
        elif question.answer == 3:
            question.answer = question.option3
        elif question.answer == 4:
            question.answer = question.option4
    # Pre-zip responses and questions
    response_question_pairs = zip(responses, questions)

    return render_template('attempt_detail.html', title='Attempt Detail', attempt=attempt, response_question_pairs=response_question_pairs)

@bp.route("/test/<int:test_id>/previous_attempts")
@login_required
def previous_attempts(test_id):
    test = Test.query.get_or_404(test_id)
    attempts = Attempt.query.filter_by(test_id=test.id, user_id=current_user.id).all()
    return render_template('previous_attempts.html', title='Previous Attempts', attempts=attempts)

@bp.route("/test/<int:test_id>/view_answers")
@login_required
def view_answers(test_id):
    test = Test.query.get_or_404(test_id)
    questions = test.questions
    return render_template('view_answers.html', title=f'Answers for {test.title}', test=test, questions=questions)
