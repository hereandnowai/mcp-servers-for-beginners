# Project 6: Google Drive Tool

This project demonstrates how to create an MCP server that can list files from a user's Google Drive.

## How to run

1.  Enable the Google Drive API and create credentials: https://developers.google.com/drive/api/v3/quickstart/python
2.  Download the `credentials.json` file and place it in the same directory as the server.
3.  Start the server: `python server.py`
4.  The first time you run the server, you will be prompted to authorize access to your Google Drive account.
5.  In a separate terminal, run the client: `python client.py`

## Expected Output

A list of the first 10 files in your Google Drive.
