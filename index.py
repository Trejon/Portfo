import os
from flask import Flask, render_template, url_for, request, redirect
import csv
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
app = Flask(__name__)
print(__name__)

load_dotenv()

@app.route('/')
def my_home():
  print(os.environ.get('EMAIL_PASSWORD'))
  return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
  return render_template(page_name)

def write_to_file(data):
  with open('database.txt', mode="a") as database:
    email = data["email"]
    name = data["name"]
    message = data["message"]
    file = database.write(f'\n{email},{name},{message}')

def write_to_csv(data):
  with open('database.csv', mode="a", newline='') as database2:
    email = data["email"]
    name = data["name"]
    message = data["message"]
    csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([email,name,message])

def email_alert(subject, body, to):
  email = body["email"]
  name = body["name"]
  message = body["message"]
  msg = EmailMessage()
  msg.set_content(f"You've got a new message from {name} at {email}: {message}")
  msg['subject'] = subject
  msg['to'] = to

  user = os.environ.get('EMAIL_VALUE')
  msg['From'] = user
  password = os.environ.get('EMAIL_PASSWORD')

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(user, password)
  server.send_message(msg)
  return server.quit()

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
  if request.method == 'POST':
    data = request.form.to_dict()
    email_alert('Website notification', data, os.environ.get('EMAIL_RECIPIENT'))
    email_alert('Website notification', data, os.environ.get('PHONE_RECIPIENT'))
    write_to_csv(data)
    return redirect('/thankyou.html')
  else:
    return 'Something went wrong, try again'
