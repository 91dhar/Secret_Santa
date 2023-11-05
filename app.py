from flask import Flask, render_template, request
import random
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

participants_emails = {
    "Souvik": "souvik@example.com",
    "Divakar": "divakar@example.com",
    # Add more participants and their emails here
}

# Function to send an email
def send_email(sender, receiver):
    sender_email = "your_email@gmail.com"  # Replace with your email address
    sender_password = "your_password"  # Replace with your email password

    message = EmailMessage()
    message.set_content(f"Hello {sender}, you're the Secret Santa for {receiver}!")

    message['Subject'] = 'Secret Santa Assignment'
    message['From'] = sender_email
    message['To'] = participants_emails[sender]  # Use associated email address for sender

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

@app.route('/')
def secret_santa_page():
    participants = list(participants_emails.keys())
    random.shuffle(participants)
    assignments = {}

    for i in range(len(participants)):
        giver = participants[i]
        receiver = participants[(i + 1) % len(participants)]  # Ensure last person gets the first person
        assignments[giver] = receiver

    return render_template('secretsanta.html', assignments=assignments)

@app.route('/send_email', methods=['POST'])
def send_secret_santa_email():
    giver = request.form['giver']
    receiver = request.form['receiver']
    send_email(giver, receiver)
    return "Email sent to " + giver

if __name__ == '__main__':
    app.run(debug=True)
