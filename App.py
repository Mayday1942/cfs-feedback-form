from flask import Flask, request, render_template_string, redirect
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Email config (use environment variables for security)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USER')

mail = Mail(app)

review_form = '''
<h2>Rate your experience with Campos Family Services</h2>
<form method="POST" action="/review">
  <select name="rating" required>
    <option value="">--Choose--</option>
    <option value="5">★★★★★</option>
    <option value="4">★★★★</option>
    <option value="3">★★★</option>
    <option value="2">★★</option>
    <option value="1">★</option>
  </select><br><br>
  <button type="submit">Submit</button>
</form>
'''

complaint_form = '''
<h2>We're sorry to hear that. Please tell us what went wrong:</h2>
<form method="POST" action="/submit_complaint">
  <textarea name="complaint" rows="5" cols="40" required></textarea><br>
  <input type="hidden" name="rating" value="{{ rating }}">
  <button type="submit">Send Feedback</button>
</form>
'''

@app.route('/')
def home():
    return render_template_string(review_form)

@app.route('/review', methods=['POST'])
def review():
    rating = int(request.form['rating'])
    if rating >= 4:
        return redirect("https://g.page/r/CdbWV_Z9kaEgEAE/review")
    return render_template_string(complaint_form, rating=rating)

@app.route('/submit_complaint', methods=['POST'])
def submit_complaint():
    complaint = request.form['complaint']
    rating = request.form['rating']
    msg = Message(
        subject=f"New Complaint (Rating: {rating} star)",
        recipients=["Admin@camposfamilyservices.com"],
        body=f"A client left {rating} star(s).\n\nComplaint:\n{complaint}"
    )
    mail.send(msg)
    return "<h3>Thank you for your feedback. We'll work to improve your experience.</h3>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
