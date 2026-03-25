# Telegram Keyword Monitor Bot

A Python-based Telegram moderation bot that monitors chats for suspicious keywords and automatically warns users.

## Features

- **Keyword Monitoring**: Detects keywords like 'scam', 'airdrop', 'fake', 'pump', 'dump', 'rug pull', 'phishing', and 'malware'
- **Automatic Warnings**: Sends warning messages when suspicious keywords are detected
- **Logging**: Full logging to both file and console for audit trails
- **Statistics**: Tracks keyword detection statistics
- **Chat Management**: Add/remove chats from monitoring list dynamically
- **Error Handling**: Robust error handling with logging
- **2FA Support**: Handles two-factor authentication

## Prerequisites

- Python 3.7+
- pip (Python package manager)
- Telegram account with API credentials

## Installation

### 1. Get Telegram API Credentials

1. Go to [https://my.telegram.org/apps](https://my.telegram.org/apps)
2. Log in with your Telegram account
3. Click "Create a new application"
4. Fill in the required details (app name, short name, etc.)
5. Get your `API_ID` and `API_HASH`

### 2. Install Dependencies

```bash
pip install telethon python-dotenv
```

### 3. Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_PHONE_NUMBER=+1234567890
   ```

## Usage

### Basic Usage

```bash
python telegram_keyword_monitor.py
```

On first run, you'll be prompted to enter your phone number and verification code.

### Adding Chats to Monitor

Edit the `MONITORED_CHATS` list in the script:

```python
MONITORED_CHATS = [123456789, 'mychannel', -1001234567890]
```

Get chat IDs:
- **Group chats**: Forward a message from the group to [@userinfobot](https://t.me/userinfobot)
- **Private chats**: Use the sender ID
- **Channels**: Add `-100` prefix to the channel ID

### Customizing Keywords

Edit the `SUSPICIOUS_KEYWORDS` list:

```python
SUSPICIOUS_KEYWORDS = [
    'scam',
    'airdrop',
    'fake',
    # Add more keywords as needed
]
```

### Customizing Warning Message

Edit the `WARNING_MESSAGE` template:

```python
WARNING_MESSAGE = """
⚠️ **KEYWORD ALERT** ⚠️
Your custom warning text here
"""
```

## Advanced Features

### Running as Background Service (Linux/Mac)

Create a systemd service file:

```ini
[Unit]
Description=Telegram Keyword Monitor Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/script
ExecStart=/usr/bin/python3 /path/to/telegram_keyword_monitor.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable telegram_monitor
sudo systemctl start telegram_monitor
```

### Monitoring Logs

```bash
tail -f telegram_monitor.log
```

## Security Considerations

- **Keep API credentials private**: Never commit `.env` to version control
- **Use strong passwords**: Especially if using 2FA
- **Session file**: `telegram_monitor_session.session` contains your session. Protect it well
- **Rate limiting**: Telegram has rate limits; avoid rapid message sending
- **Permissions**: Ensure bot has permission to send messages in monitored chats

## File Structure

```
.
├── telegram_keyword_monitor.py    # Main bot script
├── .env.example                   # Environment variables template
├── .env                          # Your actual credentials (don't commit)
├── telegram_monitor.log          # Bot activity log
└── telegram_monitor_session*     # Session file (don't commit)
```

## Troubleshooting

### "Invalid API ID" error
- Verify your API_ID and API_HASH are correct
- Make sure they match your Telegram app

### "Phone number invalid" error
- Use international format: +CountryCode + number
- Example: +1 for US, +44 for UK

### Bot not receiving messages
- Check if you have permission to read messages in the chat
- Verify chat IDs are correct
- Bot needs to be a member of the group/channel

### Rate limiting errors
- Reduce frequency of API calls
- Increase delay between messages
- Don't monitor too many chats simultaneously

## Performance Tips

- Monitor only essential chats
- Keep keyword list focused
- Use longer keywords to reduce false positives
- Implement cooldown between warnings for the same chat

## Legal Notice

This tool is for personal use and moderation purposes. Ensure you comply with:
- Telegram's Terms of Service
- Local laws regarding message monitoring
- Privacy regulations (GDPR, CCPA, etc.)
- Chat/group rules and permissions

## Support

For issues with:
- **Telethon library**: [Telethon documentation](https://docs.telethon.dev/)
- **Telegram API**: [Telegram Bot API docs](https://core.telegram.org/)
- **Python async**: [Python asyncio docs](https://docs.python.org/3/library/asyncio.html)

## License

For personal use only.
