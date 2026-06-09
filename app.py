from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_mail import Mail, Message
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# MySQL Configuration from Azure Environment Variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'your-mysql-server.mysql.database.azure.com')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'your_username')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'your_password')
app.config['MYSQL_DATABASE'] = os.environ.get('MYSQL_DATABASE', 'kvvsh_database')

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'kvvshcustomercare@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'YOUR_GMAIL_APP_PASSWORD')

mail = Mail(app)

def get_db_connection():
    """Create MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route('/test')
def test():
    return "Flask Working"

# Home
@app.route('/')
def home():
    return render_template('index.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Business
@app.route('/business')
def business():
    return render_template('business.html')

# Channels
@app.route('/channels')
def channels():
    return render_template('channels.html')

# Leadership
@app.route('/leadership')
def leadership():
    return render_template('leadership.html')

# Careers
@app.route('/career')
def career():
    return render_template('career.html')

# Internship
@app.route('/internship')
def internship():
    return render_template('internship.html')

# Jobs
@app.route('/jobs')
def jobs():
    return render_template('job.html')

# News
@app.route('/news')
def news():
    return render_template('news.html')

# Sustainability
@app.route('/sustainability')
def sustainability():
    return render_template('sustainability.html')

# Global Presence
@app.route('/global-presence')
def global_presence():
    return render_template('globalpresence.html')

# Sub Brands
@app.route('/subbrands')
def subbrands():
    return render_template('subbrands.html')

# Legal
@app.route('/legal')
def legal():
    return render_template('legal.html')

# Privacy Policy
@app.route('/privacy-policy')
def privacy():
    return render_template('privacy.html')

# Terms & Conditions
@app.route('/terms-and-conditions')
def terms():
    return render_template('termsandcon.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/image/<path:filename>')
def image(filename):
    return send_from_directory('image', filename)

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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        fullname = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phoneno', '')
        purpose = request.form.get('purpose', '')
        message_text = request.form.get('textarea', '')
        
        # Validation
        if not fullname or not email or not phone or not message_text:
            return redirect(url_for('contact', status='empty'))
        
        connection = get_db_connection()
        
        if connection is None:
            return redirect(url_for('contact', status='db_error'))
        
        try:
            cursor = connection.cursor()
            
            # Insert into ContactMessages table
            cursor.execute("""
                INSERT INTO ContactMessages 
                (fullname, email, phone, purpose, message)
                VALUES (%s, %s, %s, %s, %s)
            """, (fullname, email, phone, purpose, message_text))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Send email notification
            email_body = f"""
New Contact Form Submission

Name: {fullname}
Email: {email}
Phone: {phone}
Purpose: {purpose}

Message:
{message_text}

---
This message was sent from your KVVSH website contact form.
"""
            
            msg = Message(
                subject='New Contact Form - KVVSH Website',
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],
                body=email_body
            )
            
            mail.send(msg)
            
            return redirect(url_for('contact', status='success'))
            
        except Error as e:
            print(f"Database error: {e}")
            return redirect(url_for('contact', status='error'))
        except Exception as e:
            print(f"Email error: {e}")
            return redirect(url_for('contact', status='email_error'))
    
    return render_template('contact.html')

@app.route('/submit_job', methods=['POST'])
def submit_job():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        job_position = request.form.get('job_position', '')
        
        # Validation
        if not name or not email or not phone or not job_position:
            return redirect(url_for('jobs', status='empty'))
        
        if '@' not in email or '.' not in email:
            return redirect(url_for('jobs', status='email'))
        
        connection = get_db_connection()
        
        if connection is None:
            return redirect(url_for('jobs', status='db_error'))
        
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                INSERT INTO job_applications 
                (name, email, phone, job_position, application_date)
                VALUES (%s, %s, %s, %s, NOW())
            """, (name, email, phone, job_position))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            # Send email notification for job application
            email_body = f"""
New Job Application Received

Position: {job_position}
Name: {name}
Email: {email}
Phone: {phone}

---
This application was submitted through the KVVSH careers page.
"""
            
            msg = Message(
                subject=f'New Job Application - {job_position}',
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],
                body=email_body
            )
            
            mail.send(msg)
            
            return redirect(url_for('jobs', status='success'))
            
        except Error as e:
            print(f"Database error: {e}")
            return redirect(url_for('jobs', status='error'))
        except Exception as e:
            print(f"Email error: {e}")
            return redirect(url_for('jobs', status='email_error'))
    
    return redirect(url_for('jobs'))

if __name__ == '__main__':
    app.run(debug=True)