from crypt import methods
from flask import Flask, render_template, request, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

RESPONSE_KEY = "responses"

@app.route('/')
def display_survey_start():
    '''Display Home page with Title of Survey and Instructions'''
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('begin_survey.html', title=title, instructions=instructions)

@app.route('/begin', methods=["POST"])
def begin_survey():
    session[RESPONSE_KEY] = []

    return redirect('/questions/0')

@app.route('/answer', methods=["POST"])
def handle_question():
    
    choice = request.form['answer']

    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thankyou')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:page>')
def show_question(page):
    responses = session.get(RESPONSE_KEY)

    if (responses is None):
        return redirect('/')

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/thankyou')
    
    if (len(responses) != page):
        return redirect(f'/questions/{len(responses)}')

    question = satisfaction_survey.questions[page]
    return render_template('questions.html', 
        question=question,
        page=page)

@app.route('/thankyou')
def show_thanks():
    '''Display Thank You page'''
    return render_template('thankyou.html')
