# Notification_Controller
import smtplib
from email.mime.text import MIMEText

class NotificationController:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587, email='', password=''):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, to_address, subject, body):
        try:
            msg = MIMEText(body)
            msg["From"] = self.email
            msg["To"] = to_address
            msg["Subject"] = subject

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, to_address, msg.as_string())
            server.quit()
            print(f"Email sent to {to_address}")
        except Exception as e:
            print(f"Failed to send mail: {e}")

    def notify_user_created(self, user):
        subject = "Welcome to Task Management System"
        body = f"Hello {user['name']},\nYour account has been created successfully!"
        self.send_email(user["email"], subject, body)

    # def notify_project_created(self,user,project):
    #     subject = "Welcome to Task Management System"
    #     body = f"hello {user['name']},\nYour {project['name']}Project created successfully"
    #     self.send_email(user['email'],subject,body)






    