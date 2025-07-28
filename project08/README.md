# Project 8: Task Manager Agent

This project demonstrates how to create a task manager agent that can add tasks based on incoming emails.

## How to run

1.  **Enable less secure app access** for your Google account or use an **App Password**.
2.  Update `config.py` with your email address and app password.
3.  Start the server: `python server.py`
4.  In a separate terminal, run the client: `python client.py`
5.  Send an email to your configured email address with the subject "New Task: [Your Task]". The agent will add the task and send a confirmation email.

## Expected Output

The client will periodically check for emails and print the status. When a new task email is found, the server will add the task and send a confirmation email.
