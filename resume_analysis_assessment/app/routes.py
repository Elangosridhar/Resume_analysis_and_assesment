from flask import json, render_template, request, redirect, url_for,session
import os
import spacy
from werkzeug.utils import secure_filename
from app import app
import fitz  # PyMuPDF to read PDF

# Load the spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user_type = request.form['user_type']
        
        # Redirect based on user type
        if user_type == 'student':
            return redirect(url_for('student_dashboard', username=username))
        elif user_type == 'experienced':
            return redirect(url_for('experienced_dashboard', username=username))
    
    return render_template('login.html')

# Define allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to analyze the resume
def analyze_resume(filepath):
    resume_text = extract_text_from_pdf(filepath)
    doc = nlp(resume_text)
    
    # Predefined list of skills for ATS scoring
    predefined_skills = {"Python", "Java", "SQL", "Machine Learning", "Data Analysis", "Project Management"}
    
    skills = set()
    ats_score = 0
    
    # Token-based skill extraction
    for token in doc:
        if token.text in predefined_skills:
            skills.add(token.text)
            ats_score += 10  # Add 10 points for each matching skill
    
    return resume_text, ats_score, list(skills)

# Function to extract text from a PDF
def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = "".join(page.get_text("text") for page in doc)
    return text

# Route to handle student dashboard
@app.route('/student_dashboard/<username>', methods=['GET', 'POST'])
def student_dashboard(username):
    if request.method == 'POST':
        if 'resume' not in request.files:
            return redirect(request.url)
        
        resume_file = request.files['resume']
        
        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(filepath)
            
            resume_text, ats_score, skills = analyze_resume(filepath)
            
            return render_template('results.html', 
                                   username=username, 
                                   resume_text=resume_text, 
                                   ats_score=ats_score, 
                                   skills=skills)
    return render_template('student_dashboard.html', username=username)

# Route for experienced candidate dashboard
@app.route('/experienced_dashboard/<username>', methods=['GET', 'POST'])
def experienced_dashboard(username):
    if request.method == 'POST':
        total_experience = request.form['total_experience']
        current_position = request.form['current_position']
        current_company = request.form['current_company']
        
        if 'resume' not in request.files:
            return redirect(request.url)
        
        resume_file = request.files['resume']
        
        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(filepath)
            
            resume_text, ats_score, skills = analyze_resume(filepath)
            
            return render_template('experienced_results.html', 
                                   username=username, 
                                   total_experience=total_experience, 
                                   current_position=current_position,
                                   current_company=current_company,
                                   resume_text=resume_text, 
                                   ats_score=ats_score, 
                                   skills=skills)
    
    return render_template('experienced_dashboard.html', username=username)

# Load the assessment questions from the JSON file
def load_assessment_questions():
    with open('app/static/data/questions.json', 'r') as f:
        return json.load(f)

# Route for skill assessment
@app.route('/start_assessment/<username>', methods=['POST', 'GET'])
def start_assessment(username):
    questions_data = load_assessment_questions()
    skills = ["Python", "Machine Learning"]  # Example skills extracted from resume
    assessment_questions = []
    for skill in skills:
        if skill in questions_data:
            assessment_questions.extend(questions_data[skill])
    
    # session['assessment_questions'] = assessment_questions
    # session['username'] = username  # Store username for result page
    
    if request.method == 'POST':
        answers = request.form.getlist('answers[]')
    
    return render_template('assessment_page.html', username=username, questions=assessment_questions)

@app.route('/assessment_result', methods=['POST'])
def assessment_result():
    questions = session.get('assessment_questions', [])
    username = session.get('username', 'User')

    user_answers = request.form.getlist('answers[]')
    score = 0

    for idx, question in enumerate(questions):
        correct_answer = question["answer"]
        if idx < len(user_answers) and user_answers[idx] == correct_answer:
            score += 1

    return render_template('assessment_result.html', username=username, score=score, questions=questions)

@app.route('/start_demo_interview/<username>', methods=['POST', 'GET'])
def start_demo_interview(username):
    return render_template('demo_interview.html', username=username)
