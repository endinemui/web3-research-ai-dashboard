"""
Telegram Keyword Monitor Bot
Monitors chats for suspicious keywords and automatically warns users.
Uses Telethon library for Telegram API access.
"""

import logging
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')
SESSION_NAME = 'telegram_monitor_session'

# Keywords to monitor
SUSPICIOUS_KEYWORDS = [
    'scam',
    'airdrop',
    'fake',
    'pump',
    'dump',
    'rug pull',
    'phishing',
    'malware'
]

# Warning message template
WARNING_MESSAGE = """
⚠️ **KEYWORD ALERT** ⚠️
Detected suspicious keyword in chat: `{keyword}`

This message may contain a scam, phishing attempt, or fraudulent offer.
Please verify the sender's identity before interacting.

Common scam indicators:
• Unsolicited offers
• Requests for personal information
• Pressure to act quickly
• Too-good-to-be-true promises
"""

# Chats to monitor (chat IDs or usernames)
MONITORED_CHATS = []  # Add chat IDs here, e.g., [123456789, 'username']


class TelegramKeywordMonitor:
    """Telegram bot for monitoring and warning about suspicious keywords."""
    
    def __init__(self):
        self.client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        self.keyword_count = {}
        
    async def start(self):
        """Initialize and start the bot."""
        try:
            await self.client.start(phone=PHONE_NUMBER)
            logger.info("Bot started successfully")
            
            # Display current user info
            me = await self.client.get_me()
            logger.info(f"Logged in as: {me.first_name}")
            
            # Set up event handlers
            self.client.add_event_handler(
                self.handle_new_message,
                events.NewMessage(chats=MONITORED_CHATS if MONITORED_CHATS else None)
            )
            
            logger.info(f"Monitoring {len(SUSPICIOUS_KEYWORDS)} keywords: {', '.join(SUSPICIOUS_KEYWORDS)}")
            
        except SessionPasswordNeededError:
            password = input("2FA password required: ")
            await self.client.sign_in(password=password)
            logger.info("2FA authentication successful")
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
    
    async def handle_new_message(self, event):
        """Handle incoming messages and check for suspicious keywords."""
        try:
            message_text = event.message.text
            
            if not message_text:
                return
            
            message_lower = message_text.lower()
            
            # Check for suspicious keywords
            detected_keywords = []
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword.lower() in message_lower:
                    detected_keywords.append(keyword)
            
            if detected_keywords:
                await self.process_warning(event, detected_keywords)
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    async def process_warning(self, event, keywords):
        """Process and send warning for detected keywords."""
        try:
            chat_id = event.chat_id
            message_id = event.message.id
            sender_id = event.sender_id
            
            # Log the detection
            keyword_str = ', '.join(keywords)
            logger.warning(
                f"Suspicious keywords detected in chat {chat_id} "
                f"(Message ID: {message_id}, Sender: {sender_id}): {keyword_str}"
            )
            
            # Update keyword statistics
            for keyword in keywords:
                self.keyword_count[keyword] = self.keyword_count.get(keyword, 0) + 1
            
            # Send warning to the chat
            for keyword in keywords:
                warning = WARNING_MESSAGE.format(keyword=keyword.upper())
                await event.reply(warning, parse_mode='markdown')
                logger.info(f"Warning sent for keyword: {keyword}")
                
                # Small delay between replies to avoid rate limiting
                await asyncio.sleep(0.5)
        
        except Exception as e:
            logger.error(f"Error sending warning: {e}")
    
    async def get_statistics(self):
        """Return keyword detection statistics."""
        return self.keyword_count
    
    async def add_chat(self, chat_id):
        """Add a chat to the monitoring list."""
        MONITORED_CHATS.append(chat_id)
        logger.info(f"Added chat {chat_id} to monitoring list")
    
    async def remove_chat(self, chat_id):
        """Remove a chat from the monitoring list."""
        if chat_id in MONITORED_CHATS:
            MONITORED_CHATS.remove(chat_id)
            logger.info(f"Removed chat {chat_id} from monitoring list")
    
    async def stop(self):
        """Stop the bot gracefully."""
        await self.client.disconnect()
        logger.info("Bot stopped")


async def main():
    """Main entry point."""
    monitor = TelegramKeywordMonitor()
    
    try:
        await monitor.start()
        
        # Keep the bot running
        await monitor.client.run_until_disconnected()
    
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await monitor.stop()


if __name__ == '__main__':
    asyncio.run(main())
