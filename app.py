from flask import Flask, request, render_template_string, redirect
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Email configuration using environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USER')

# Optional: limit upload size (e.g., 5 MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

mail = Mail(app)

# Review form HTML
review_form = '''
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Campos Family Services – Feedback</title>
</head>
<body style="margin:0; padding:0; font-family:sans-serif; background-color:#f4f4f4;">
  <div style="max-width:600px; margin:40px auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); text-align:center;">
    <img src="https://i.imgur.com/0Bh810c.jpeg" style="width:120px; height:120px; object-fit:cover; border-radius:50%; margin-bottom:20px;">
    <h2 style="color:#2a6f97;">We appreciate the opportunity to transform your yard.</h2>
    <p style="font-size:16px; color:#333;">
      As a family business, reviews mean everything to us—they help us grow, build trust, and continue providing top-quality service.
      A 5-star ⭐⭐⭐⭐⭐ review would mean the world to us.
      <br><br>
      But if we fell short of expectations in any way, we genuinely welcome honest feedback. It gives us the opportunity to reach out, make things right, and improve wherever we can. Your voice helps us grow.
      Thank you for your support!
    </p>
    <form method="POST" action="/review">
      <label for="rating" style="font-size:16px;">How would you rate our service?</label><br><br>
      <select name="rating" required style="font-size:18px; padding:8px; width:60%;">
        <option value="">-- Choose --</option>
        <option value="5">★★★★★</option>
        <option value="4">★★★★</option>
        <option value="3">★★★</option>
        <option value="2">★★</option>
        <option value="1">★</option>
      </select><br><br>
      <button type="submit" style="padding:12px 24px; font-size:16px; background:#2a6f97; color:white; border:none; border-radius:5px;">Submit</button>
    </form>
  </div>
</body>
</html>
'''

# Complaint form with file upload
complaint_form = '''
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Campos Family Services – Feedback</title>
</head>
<body style="margin:0; padding:0; font-family:sans-serif; background-color:#f4f4f4;">
  <div style="max-width:600px; margin:40px auto; background:white; padding:30px; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); text-align:center;">
    <h2 style="color:#c0392b;">We're sorry to hear that!</h2>
    <p style="font-size:15px; color:#333;">Please let us know what went wrong and how we can do better.</p>
    <form method="POST" action="/submit_complaint" enctype="multipart/form-data" style="text-align:left;">
      <label>Contact Info (Name or Email):</label><br>
      <input type="text" name="contact" style="width:100%; padding:10px; margin-bottom:15px; border-radius:5px; border:1px solid #ccc;" required><br>

      <label>Feedback:</label><br>
      <textarea name="complaint" rows="5" style="width:100%; padding:10px; border-radius:5px; border:1px solid #ccc;" required></textarea><br><br>

      <label>Upload a Photo (optional):</label><br>
      <input type="file" name="photo" accept="image/*" style="margin-bottom:15px;"><br>

      <input type="hidden" name="rating" value="{{ rating }}">
      <button type="submit" style="padding:12px 24px; font-size:16px; background:#c0392b; color:white; border:none; border-radius:5px;">Send Feedback</button>
    </form>
  </div>
</body>
</html>
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
    contact = request.form['contact']
    complaint = request.form['complaint']
    rating = request.form['rating']
    uploaded_file = request.files.get('photo')

    msg = Message(
        subject=f"New Complaint (Rating: {rating} star)",
        recipients=["Admin@camposfamilyservices.com"],
        body=f"A client left {rating} star(s).\n\nContact Info: {contact}\n\nComplaint:\n{complaint}"
    )

    # If an image is uploaded, attach it to the email
    if uploaded_file and uploaded_file.filename:
        filename = secure_filename(uploaded_file.filename)
        msg.attach(
            filename=filename,
            content_type=uploaded_file.content_type,
            data=uploaded_file.read()
        )

    mail.send(msg)

    return "<h3 style='font-family:sans-serif; text-align:center;'>Thank you for your feedback. We'll work to improve your experience.</h3>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
