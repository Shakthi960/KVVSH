from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# =====================================================
# MYSQL CONFIGURATION
# =====================================================

app.config['MYSQL_HOST'] = os.environ.get(
    'MYSQL_HOST',
    'kvvsh1.mysql.database.azure.com'
)

app.config['MYSQL_USER'] = os.environ.get(
    'MYSQL_USER',
    'kvvsh1'
)

app.config['MYSQL_PASSWORD'] = os.environ.get(
    'MYSQL_PASSWORD',
    'ksakthi960@#'
)

app.config['MYSQL_DATABASE'] = os.environ.get(
    'MYSQL_DATABASE',
    'kvvshdb'
)

# =====================================================
# MAIL CONFIGURATION
# =====================================================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = os.environ.get(
    'MAIL_USERNAME',
    'kvvshcustomercare@gmail.com'
)

app.config['MAIL_PASSWORD'] = os.environ.get(
    'MAIL_PASSWORD',
    'YOUR_GMAIL_APP_PASSWORD'
)

mail = Mail(app)

# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_db_connection():

    try:

        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE'],
            ssl_disabled=False
        )

        return connection

    except Error as e:

        print(f"Database connection error: {e}")

        return None


# =====================================================
# DATABASE INITIALIZATION
# =====================================================

def initialize_database():

    connection = get_db_connection()

    if connection:

        cursor = connection.cursor()

        # CONTACT TABLE

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ContactMessages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(50),
            purpose VARCHAR(255),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # JOB APPLICATIONS TABLE

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(255),
            email VARCHAR(255),
            phone VARCHAR(50),
            job_position VARCHAR(255),
            experience VARCHAR(100),
            location VARCHAR(255),
            resume_file VARCHAR(255),
            cover_letter TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        connection.commit()

        cursor.close()
        connection.close()


initialize_database()

# =====================================================
# TEST ROUTE
# =====================================================

@app.route('/test')
def test():
    return "Flask Working"

# =====================================================
# MAIN WEBSITE ROUTES
# =====================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/business')
def business():
    return render_template('business.html')


@app.route('/channels')
def channels():
    return render_template('channels.html')


@app.route('/leadership')
def leadership():
    return render_template('leadership.html')


@app.route('/career')
def career():
    return render_template('career.html')


@app.route('/internship')
def internship():
    return render_template('internship.html')


@app.route('/jobs')
def jobs():
    return render_template('job.html')


@app.route('/news')
def news():
    return render_template('news.html')


@app.route('/sustainability')
def sustainability():
    return render_template('sustainability.html')


@app.route('/global-presence')
def global_presence():
    return render_template('globalpresence.html')


@app.route('/subbrands')
def subbrands():
    return render_template('subbrands.html')


@app.route('/legal')
def legal():
    return render_template('legal.html')


@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms-and-conditions')
def terms():
    return render_template('termsandcon.html')


# =====================================================
# IMAGE ROUTE
# =====================================================

@app.route('/image/<path:filename>')
def image(filename):
    return send_from_directory('image', filename)


# =====================================================
# ERROR PAGES
# =====================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# =====================================================
# GROUP PAGES
# =====================================================

@app.route('/group1')
def group1():
    return render_template('group1.html')


@app.route('/group2')
def group2():
    return render_template('group2.html')


@app.route('/group3')
def group3():
    return render_template('group3.html')


@app.route('/group4')
def group4():
    return render_template('group4.html')


@app.route('/group5')
def group5():
    return render_template('group5.html')


@app.route('/group6')
def group6():
    return render_template('group6.html')


@app.route('/group7')
def group7():
    return render_template('group7.html')


@app.route('/group8')
def group8():
    return render_template('group8.html')


@app.route('/group9')
def group9():
    return render_template('group9.html')


@app.route('/group10')
def group10():
    return render_template('group10.html')

# =====================================================
# CONTACT FORM
# =====================================================

@app.route('/contact', methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':

        fullname = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phoneno', '')
        purpose = request.form.get('purpose', '')
        message_text = request.form.get('textarea', '')

        # VALIDATION

        if not fullname or not email or not phone or not message_text:
            return redirect(
                url_for(
                    'contact',
                    status='empty'
                )
            )

        connection = get_db_connection()

        if connection is None:
            return redirect(
                url_for(
                    'contact',
                    status='db_error'
                )
            )

        try:

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO ContactMessages
                (
                    fullname,
                    email,
                    phone,
                    purpose,
                    message
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """,
            (
                fullname,
                email,
                phone,
                purpose,
                message_text
            ))

            connection.commit()

            cursor.close()
            connection.close()

            # EMAIL NOTIFICATION

            email_body = f"""
New Contact Form Submission

Name: {fullname}
Email: {email}
Phone: {phone}
Purpose: {purpose}

Message:
{message_text}

------------------------------------
Submitted from KVVSH Website
"""

            msg = Message(
                subject='New Contact Form - KVVSH Website',
                sender=app.config['MAIL_USERNAME'],
                recipients=[
                    app.config['MAIL_USERNAME']
                ],
                body=email_body
            )

            mail.send(msg)

            return redirect(
                url_for(
                    'contact',
                    status='success'
                )
            )

        except Error as e:

            print(f"Database Error: {e}")

            return redirect(
                url_for(
                    'contact',
                    status='error'
                )
            )

        except Exception as e:

            print(f"Mail Error: {e}")

            return redirect(
                url_for(
                    'contact',
                    status='email_error'
                )
            )

    return render_template('contact.html')

# =====================================================
# JOB APPLICATION FORM
# =====================================================

@app.route('/submit_job', methods=['POST'])
def submit_job():

    name = request.form.get('name', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    job_position = request.form.get('job_position', '')

    if not name or not email or not phone or not job_position:
        return redirect(url_for('jobs', status='empty'))

    try:

        connection = get_db_connection()

        if connection is None:
            return redirect(url_for('jobs', status='db_error'))

        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO job_applications
            (
                name,
                email,
                phone,
                job_position
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
        """,
        (
            name,
            email,
            phone,
            job_position
        ))

        connection.commit()

        cursor.close()
        connection.close()

        email_body = f"""
New Job Application

Name: {name}
Email: {email}
Phone: {phone}

Position Applied:
{job_position}
"""

        msg = Message(
            subject=f'New Job Application - {job_position}',
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']],
            body=email_body
        )

        mail.send(msg)

        return redirect(url_for('jobs', status='success'))

    except Exception as e:

        print(f"Job Form Error: {e}")

        return redirect(url_for('jobs', status='error'))
    
    # =====================================================
# APPLICATION START
# =====================================================

if __name__ == '__main__':

    print("=" * 50)
    print("KVVSH GROUP WEBSITE STARTED")
    print("=" * 50)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )