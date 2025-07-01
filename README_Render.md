
# Discord Trade Alert Bot (Render Version)

## What It Does:
- Logs in to your Discord via browser emulation
- Monitors Brando and Shoof in specific channels
- Sends SMS alert via Twilio when "BOUGHT" or "SOLD" is detected

## How to Deploy on Render

### 1. Create a Twilio Account
Go to https://www.twilio.com/
- Get your SID, Auth Token, and trial number

### 2. Prepare Your Environment
- Fill in `.env.example` with your Discord login and Twilio info
- Rename it to `.env`

### 3. Create a New Web Service on Render
- Go to https://render.com/
- Click “New” → “Web Service”
- Connect to a GitHub repo or manually upload this project
- Set Build Command: `pip install -r requirements.txt`
- Set Start Command: `python main.py`
- Add your environment variables from `.env`

### 4. Deploy
- Render will spin up the service and keep it running
- You’ll get texts when alerts hit
