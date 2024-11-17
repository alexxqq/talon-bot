# Telegram Bot Script

This project is a Telegram bot that interacts with users, manages parsing task, and allows users to update credentials through bot commands. The bot can be controlled to start, stop, and check the status of task.

## Prerequisites

Before running the bot, ensure you have the following:

- **Python 3.7+** installed.
- A **Telegram Bot Token** from the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.

## Installation

### Step 1: Clone the repository

If you haven't already cloned the project, clone it from your preferred version control system (e.g., GitHub):

```bash
git clone https://github.com/yourusername/telegram-bot.git
cd talon-bot
```

### Step 2: Install dependencies with ```pipenv```

Make sure you have ```pipenv``` installed. If not, you can install it using:

```bash
pip install pipenv
```
Once ```pipenv``` is installed, run the following to install the dependencies:
```bash
pipenv install
```
This will create a virtual environment and install all dependencies defined in the Pipfile.

### Step 3: Set up environment variables
You need to set up the required environment variables for the bot to function properly. Create a ```.env``` file in the root directory of the project and add the following variables:

BOT_TOKEN=
CHAT_ID=
COOKIES=_
CSRF_TOKEN=

### Step 4: Run the bot
To run the bot, activate the ```pipenv``` shell:

```bash
pipenv shell
```
Then start the bot with:
```bash
python3 main.py
```

The bot should now be running and ready to accept commands.

## Docker Setup for Telegram Bot

### Step 1: Build the Docker image

Build the Docker image using the following command:

```bash
docker build -t telegram-bot .
```
### Step 2: Run the Docker container
Run the bot inside a Docker container, passing the required environment variables:

```bash
docker run -e BOT_TOKEN=<your-telegram-bot-token> -e CHAT_ID=<your-chat-id> -e COOKIES=<your-cookies> -e CSRF_TOKEN=<your-csrf-token> telegram-bot
```