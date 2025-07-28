import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from mcp import McpServer, Tool
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, SMTP_SERVER, SMTP_PORT

tasks = []

@Tool
def add_task(task: str) -> str:
    """Adds a task to the list."""
    tasks.append(task)
    return f"Task '{task}' added."

@Tool
def list_tasks() -> list:
    """Lists all tasks."""
    return tasks

@Tool
def check_emails_and_add_tasks():
    """Checks for new emails and adds tasks."""
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select("inbox")

        # Search for unseen emails
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            return "No new messages."

        for num in messages[0].split():
            status, data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            # Parse the email
            msg = email.message_from_bytes(data[0][1])
            subject = msg["subject"]
            sender = msg["from"]

            # Add task from email subject
            if "New Task:" in subject:
                task = subject.split("New Task:")[1].strip()
                add_task(task)
                send_confirmation_email(sender, task)

        mail.logout()
        return "Email check complete."

    except Exception as e:
        return f"Error: {e}"

def send_confirmation_email(recipient, task):
    """Sends a confirmation email."""
    try:
        msg = MIMEText(f"The task '{task}' has been added to your to-do list.")
        msg["Subject"] = f"Task Added: {task}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = recipient

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    server = McpServer(tools=[add_task, list_tasks, check_emails_and_add_tasks])
    server.run()
