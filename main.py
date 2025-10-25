import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from dotenv import load_dotenv

from utils.shortener_manager import (
    add_shortener,
    list_shorteners,
    toggle_shortener,
    remove_shortener
)
from utils.uploader_manager import (
    add_uploader,
    list_uploaders,
    toggle_uploader,
    remove_uploader
)
from utils.api_handler import upload_to_platforms, shorten_urls
from utils.formatter import format_result
from utils.permissions import is_admin
from utils.logger import log_upload

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
ADD_SHORT_NAME, ADD_SHORT_BASE, ADD_SHORT_API = range(3)
ADD_UPLOAD_NAME, ADD_UPLOAD_ENDPOINT, ADD_UPLOAD_API = range(3, 6)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message"""
    welcome_msg = (
        "👋 **Welcome to MultiUploaderX Pro**\n\n"
        "Use /upload <drive_link> to start.\n"
        "Use /help for all commands."
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all available commands"""
    help_text = (
        "📚 **Available Commands:**\n\n"
        "**General:**\n"
        "/start - Welcome message\n"
        "/help - Show this help\n"
        "/upload <link> - Upload and shorten a link\n\n"
        "**Shortener Management (Admin):**\n"
        "/addshort - Add new shortener\n"
        "/listshort - List all shorteners\n"
        "/toggleshort <index> - Pause/Resume shortener\n"
        "/removeshort <index> - Remove shortener\n\n"
        "**Uploader Management (Admin):**\n"
        "/addupload - Add new uploader\n"
        "/listupload - List all uploaders\n"
        "/toggleupload <index> - Pause/Resume uploader\n"
        "/removeupload <index> - Remove uploader"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

# Upload command
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle file upload and shortening"""
    user_id = update.effective_user.id
    username = update.effective_user.username or "Unknown"
    
    # Check if link provided
    if not context.args:
        await update.message.reply_text("⚠️ Please provide a link.\nUsage: /upload <link>")
        return
    
    original_link = context.args[0]
    
    # Validate link format
    if not (original_link.startswith('http://') or original_link.startswith('https://')):
        await update.message.reply_text("⚠️ Invalid or unsupported link format.")
        return
    
    await update.message.reply_text("⏳ Processing your request...")
    
    try:
        # Upload to all active platforms
        upload_results = upload_to_platforms(original_link)
        
        if not upload_results:
            await update.message.reply_text("⚠️ No active upload platforms configured.")
            return
        
        # Shorten original link
        original_shortened = shorten_urls(original_link)
        
        # Format result
        result_text = format_result(original_link, original_shortened, upload_results)
        
        # Log upload
        log_upload(username, user_id, original_link)
        
        await update.message.reply_text(result_text)
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        await update.message.reply_text("⚠️ An error occurred during processing.")

# Add shortener conversation
async def add_short_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start add shortener conversation"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You don't have permission to use this command.")
        return ConversationHandler.END
    
    await update.message.reply_text("Please enter the shortener name:")
    return ADD_SHORT_NAME

async def add_short_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive shortener name"""
    context.user_data['short_name'] = update.message.text
    await update.message.reply_text(
        "Please enter the base API URL (example: https://gplinks.in/api?api=):"
    )
    return ADD_SHORT_BASE

async def add_short_base(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive shortener base URL"""
    context.user_data['short_base'] = update.message.text
    await update.message.reply_text("Please enter your API key:")
    return ADD_SHORT_API

async def add_short_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive API key and save shortener"""
    api_key = update.message.text
    name = context.user_data['short_name']
    base = context.user_data['short_base']
    
    success = add_shortener(name, base, api_key)
    
    if success:
        await update.message.reply_text(f"✅ Shortener '{name}' added successfully!")
    else:
        await update.message.reply_text("⚠️ Failed to add shortener. Please try again.")
    
    context.user_data.clear()
    return ConversationHandler.END

# List shorteners
async def list_short(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all shorteners"""
    shorteners = list_shorteners()
    await update.message.reply_text(shorteners)

# Toggle shortener
async def toggle_short(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle shortener status"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /toggleshort <index>")
        return
    
    try:
        index = int(context.args[0]) - 1
        result = toggle_shortener(index)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("⚠️ Invalid index. Please provide a number.")

# Remove shortener
async def remove_short(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove shortener"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /removeshort <index>")
        return
    
    try:
        index = int(context.args[0]) - 1
        result = remove_shortener(index)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("⚠️ Invalid index. Please provide a number.")

# Add uploader conversation
async def add_upload_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start add uploader conversation"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You don't have permission to use this command.")
        return ConversationHandler.END
    
    await update.message.reply_text("Enter upload platform name:")
    return ADD_UPLOAD_NAME

async def add_upload_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive uploader name"""
    context.user_data['upload_name'] = update.message.text
    await update.message.reply_text(
        "Enter API endpoint (example: https://filepress.in/api/upload):"
    )
    return ADD_UPLOAD_ENDPOINT

async def add_upload_endpoint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive uploader endpoint"""
    context.user_data['upload_endpoint'] = update.message.text
    await update.message.reply_text("Enter API key:")
    return ADD_UPLOAD_API

async def add_upload_api(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receive API key and save uploader"""
    api_key = update.message.text
    name = context.user_data['upload_name']
    endpoint = context.user_data['upload_endpoint']
    
    success = add_uploader(name, endpoint, api_key)
    
    if success:
        await update.message.reply_text(f"✅ Uploader '{name}' added successfully!")
    else:
        await update.message.reply_text("⚠️ Failed to add uploader. Please try again.")
    
    context.user_data.clear()
    return ConversationHandler.END

# List uploaders
async def list_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all uploaders"""
    uploaders = list_uploaders()
    await update.message.reply_text(uploaders)

# Toggle uploader
async def toggle_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggle uploader status"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /toggleupload <index>")
        return
    
    try:
        index = int(context.args[0]) - 1
        result = toggle_uploader(index)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("⚠️ Invalid index. Please provide a number.")

# Remove uploader
async def remove_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove uploader"""
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("🚫 You don't have permission to use this command.")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /removeupload <index>")
        return
    
    try:
        index = int(context.args[0]) - 1
        result = remove_uploader(index)
        await update.message.reply_text(result)
    except ValueError:
        await update.message.reply_text("⚠️ Invalid index. Please provide a number.")

# Cancel conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation"""
    await update.message.reply_text("❌ Operation cancelled.")
    context.user_data.clear()
    return ConversationHandler.END

# Unknown command handler
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands"""
    await update.message.reply_text("❌ Unknown command. Type /help for options.")

def main():
    """Start the bot"""
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logger.error("BOT_TOKEN not found in .env file")
        return
    
    # Create application
    app = Application.builder().token(token).build()
    
    # Add shortener conversation handler
    add_short_conv = ConversationHandler(
        entry_points=[CommandHandler('addshort', add_short_start)],
        states={
            ADD_SHORT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_short_name)],
            ADD_SHORT_BASE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_short_base)],
            ADD_SHORT_API: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_short_api)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Add uploader conversation handler
    add_upload_conv = ConversationHandler(
        entry_points=[CommandHandler('addupload', add_upload_start)],
        states={
            ADD_UPLOAD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_upload_name)],
            ADD_UPLOAD_ENDPOINT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_upload_endpoint)],
            ADD_UPLOAD_API: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_upload_api)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Add handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('upload', upload))
    
    app.add_handler(add_short_conv)
    app.add_handler(CommandHandler('listshort', list_short))
    app.add_handler(CommandHandler('toggleshort', toggle_short))
    app.add_handler(CommandHandler('removeshort', remove_short))
    
    app.add_handler(add_upload_conv)
    app.add_handler(CommandHandler('listupload', list_upload))
    app.add_handler(CommandHandler('toggleupload', toggle_upload))
    app.add_handler(CommandHandler('removeupload', remove_upload))
    
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    # Start bot
    logger.info("Bot started!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()