"""
Configuration module for Telegram Keyword Monitor Bot
Allows easy management of keywords, warning levels, and chat rules.
"""

# Keyword database with severity levels
KEYWORD_DATABASE = {
    # Severity: high, medium, low
    'scam': {
        'severity': 'high',
        'keywords': ['scam', 'scammed', 'scammer'],
        'description': 'Potential scam detected'
    },
    'airdrop': {
        'severity': 'medium',
        'keywords': ['airdrop', 'free tokens', 'free airdrop'],
        'description': 'Suspicious airdrop offer'
    },
    'fake': {
        'severity': 'high',
        'keywords': ['fake', 'counterfeit', 'bogus'],
        'description': 'Fake or counterfeit content detected'
    },
    'pump': {
        'severity': 'medium',
        'keywords': ['pump and dump', 'pump', 'dump signal'],
        'description': 'Potential pump and dump scheme'
    },
    'rug_pull': {
        'severity': 'high',
        'keywords': ['rug pull', 'rug-pull', 'rugged'],
        'description': 'Potential rug pull scheme'
    },
    'phishing': {
        'severity': 'high',
        'keywords': ['phishing', 'verify account', 'confirm identity'],
        'description': 'Potential phishing attempt'
    },
    'malware': {
        'severity': 'high',
        'keywords': ['malware', 'virus', 'trojan'],
        'description': 'Potential malware threat'
    }
}

# Warning messages for different severity levels
WARNING_TEMPLATES = {
    'high': """
🚨 **HIGH SEVERITY ALERT** 🚨
Detected potential: `{description}`

⚠️ **DANGER**: This may be a serious threat!

**DO NOT:**
• Click suspicious links
• Share personal information
• Send money or crypto
• Download files from unknown sources

**Actions to take:**
• Verify the sender's legitimacy
• Check official channels for confirmation
• Report to chat moderators
• Block suspicious accounts
""",
    'medium': """
⚠️ **MEDIUM SEVERITY ALERT** ⚠️
Detected suspicious activity: `{description}`

**Be cautious:**
• Verify offers from trusted sources
• Research before participating
• Ask moderators if unsure
• Don't trust unsolicited offers
""",
    'low': """
ℹ️ **INFORMATIONAL ALERT**
Detected keyword: `{description}`

Please verify information from official sources.
"""
}

# Chat-specific rules (override global settings)
CHAT_RULES = {
    # Example:
    # 123456789: {
    #     'enabled': True,
    #     'keywords': ['custom_keyword'],  # Additional keywords for this chat
    #     'ignore_keywords': ['legit_word'],  # Words to ignore in this chat
    #     'auto_delete': True,  # Auto-delete messages with keywords
    #     'auto_ban': False,    # Auto-ban users sending keywords
    # }
}

# Global moderation settings
MODERATION_CONFIG = {
    'auto_delete_message': False,  # Delete message with keyword
    'auto_ban_user': False,        # Ban user after threshold
    'ban_threshold': 3,            # Number of violations before ban
    'cooldown_period': 300,        # Seconds between warnings in same chat
    'enable_logging': True,        # Enable detailed logging
    'enable_statistics': True,     # Track keyword statistics
    'mention_user': False,         # Mention user in warning
    'dm_warning': False,           # Send warning via DM instead of chat
}

# Rate limiting
RATE_LIMIT_CONFIG = {
    'warnings_per_minute': 10,
    'messages_per_minute': 20,
    'delay_between_warnings': 0.5,  # seconds
}

# Whitelist for false positives
WHITELIST = {
    # Chat IDs to exclude from monitoring
    'excluded_chats': [],
    # User IDs that won't trigger warnings
    'trusted_users': [],
    # Exact phrases to ignore (case-insensitive)
    'safe_phrases': [
        'the scam happened in the movie',
        'avoiding scams',
        'reported a scam'
    ]
}

# Notification settings
NOTIFICATIONS = {
    'notify_on_detection': True,
    'notification_method': 'inline',  # 'inline', 'dm', or 'both'
    'admin_alerts': False,            # Alert admins of detections
    'admin_user_id': None,            # Admin user ID for alerts
}


def get_warning_template(severity):
    """Get warning template for severity level."""
    return WARNING_TEMPLATES.get(severity, WARNING_TEMPLATES['low'])


def get_keywords_for_chat(chat_id):
    """Get all keywords to monitor for a specific chat."""
    keywords = []
    
    # Add global keywords
    for category, config in KEYWORD_DATABASE.items():
        keywords.extend(config['keywords'])
    
    # Add chat-specific keywords
    if chat_id in CHAT_RULES:
        if 'keywords' in CHAT_RULES[chat_id]:
            keywords.extend(CHAT_RULES[chat_id]['keywords'])
    
    return keywords


def get_ignored_keywords_for_chat(chat_id):
    """Get keywords to ignore for a specific chat."""
    if chat_id in CHAT_RULES:
        return CHAT_RULES[chat_id].get('ignore_keywords', [])
    return []


def is_chat_excluded(chat_id):
    """Check if chat is excluded from monitoring."""
    return chat_id in WHITELIST['excluded_chats']


def is_user_trusted(user_id):
    """Check if user is in trusted list."""
    return user_id in WHITELIST['trusted_users']


def is_safe_phrase(text):
    """Check if text contains safe phrases that shouldn't trigger warning."""
    text_lower = text.lower()
    for phrase in WHITELIST['safe_phrases']:
        if phrase.lower() in text_lower:
            return True
    return False
