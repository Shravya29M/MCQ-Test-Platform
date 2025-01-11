# MCQ Test Platform 

This is an MCQ (Multiple Choice Questions) Test Platform built with Flask. The platform allows users to register, log in, create tests, upload questions, attempt tests, and view previous attempts.

## Features

- User Registration and Login
- Create and manage tests
- Upload questions via CSV
- Attempt tests and view results
- View previous attempts

## Technologies Used

- Python 3.9
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Bootstrap 4 for UI styling
- MySQL for database

## Prerequisites

- Python 3.9
- Docker
- Docker Compose

## Local Setup

### 1. Clone the repository

bash
git clone https://github.com/yourusername/mcq-test-platform.git
cd mcq-test-platform


### 2. Create and activate a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


### 3. Install dependencies

bash
pip install -r requirements.txt


### 4. Configure the Database

Update the config.py file with your MySQL database configuration.

python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'


### 5. Initialize the Database

bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade


### 6. Run the Application

bash
flask run


## Docker Deployment

### 1. Build Docker Images

bash
docker-compose build


### 2. Run the Containers

bash
docker-compose up


### 3. Initialize the Database (Run these commands from another terminal)

bash
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "Initial migration"
docker-compose exec web flask db upgrade


## Usage

### Creating a Test

1. Log in or register a new account.
2. Go to the dashboard and click "Create New Test".
3. Fill in the test details and submit.
4. Upload questions in CSV format.

### Attempting a Test

1. Go to the dashboard.
2. Select a test and click "Begin Test".
3. Answer the questions and submit the test.
4. View your score and previous attempts.

### Viewing Previous Attempts

1. Go to the test detail page.
2. Click on "Previous Attempts".
3. View the list of previous attempts and click on any attempt to see detailed responses.

### Viewing Answers

1. Go to the test detail page.
2. Click on "View Answers".
3. View all the questions, options, and correct answers.

## File Structure

plaintext
mcq-test-platform/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   └── static/
│       └── styles.css
│
├── migrations/
│
├── venv/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config.py
└── README.md


