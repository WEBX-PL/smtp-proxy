# SMTP Proxy Application

This repository contains a comprehensive SMTP proxy application designed to intercept, store, and selectively forward emails based on user interaction. The application is ideal for managing and filtering outbound emails to prevent spam or for auditing purposes.

## Features

- **SMTP Server**: Built with `aiosmtpd`, this component acts as an intermediate SMTP server, intercepting emails from a specified source application (App A).
- **SQLite Database Integration**: Utilizes SQLite for efficient and reliable storage of intercepted emails, ensuring data persistence and easy retrieval.
- **Slack Notification**: Integrates with Slack via Incoming Webhooks to send real-time notifications about new emails captured by the system.
- **Flask Web Interface**: Provides a user-friendly web interface built with Flask, enabling users to view, manage, and manually forward emails.

## Components

1. **SMTP Server Module (`smtp_server.py`)**: Receives and processes incoming emails, storing them in the SQLite database.
2. **SQLite Database (`emails.db`)**: Stores email data, including sender, recipient, subject, and content, along with a status flag.
3. **Slack Notification Module (`your_slack_module.py`)**: Sends notifications to a designated Slack channel when a new email arrives.
4. **Flask Web Application (`app.py`)**: Offers a web-based UI for viewing stored emails and manually forwarding them as needed. The interface also displays email details such as the recipient, title, and content.

## Setup and Installation

- Requirements: Python 3.x, Flask, aiosmtpd, SQLite, and requests libraries.
- Installation instructions and dependencies are detailed in the `requirements.txt` file.
- Configuration steps for Slack webhook and SMTP settings are provided.

## Usage

1. Start the SMTP server to begin capturing emails.
2. View and manage emails via the Flask web interface.
3. Use the Slack integration for immediate alerts on new emails.

## License

This project is licensed under MIT

