# 🚀 MultiUploaderX Pro

A powerful Telegram bot that uploads files to multiple platforms and shortens links using multiple URL shorteners.

## ✨ Features

- 📤 Upload files to multiple platforms (FilePress, StreamX, etc.)
- 🔗 Shorten URLs using multiple shorteners (GPLinks, ShrinkMe, Droplink, etc.)
- ⚙️ Dynamic shortener and uploader management
- 👥 Admin-only management commands
- 📊 Automatic logging of all uploads
- 🔄 Pause/Resume shorteners and uploaders
- 🛡️ Error handling and validation

## 📁 Project Structure

```
MultiUploaderX-Pro/
│
├── main.py                      # Main bot entry file
├── .env                         # Bot token & admin ID (create this)
├── requirements.txt             # Dependencies
│
├── shorteners.json              # Stores shortener data (auto-created)
├── uploads.json                 # Stores upload site data (auto-created)
├── logs.json                    # Upload logs (auto-created)
│
├── utils/
│   ├── __init__.py
│   ├── shortener_manager.py    # Shortener management
│   ├── uploader_manager.py     # Uploader management
│   ├── formatter.py            # Output formatting
│   ├── api_handler.py          # API calls
│   ├── permissions.py          # Admin checks
│   └── logger.py               # Upload logging
│
└── README.md                    # This file
```

## 🔧 Installation

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd MultiUploaderX-Pro
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_ID=123456789
```

**How to get your Bot Token:**
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions
4. Copy the token provided

**How to get your Admin ID:**
1. Search for [@userinfobot](https://t.me/userinfobot) on Telegram
2. Start the bot
3. Copy your user ID

**Note:** You can add multiple admin IDs separated by commas:
```env
ADMIN_ID=123456789,987654321
```

### 4. Create utils Package

Create an empty `__init__.py` file in the `utils` folder:

```bash
mkdir utils
touch utils/__init__.py
```

### 5. Run the Bot

```bash
python main.py
```

## 📖 Usage

### For All Users

#### Upload a File
```
/upload https://drive.google.com/file/d/abc123
```

The bot will:
1. Upload the file to all active platforms
2. Shorten both the original and uploaded links
3. Return formatted results

**Example Output:**
```
Drive link - https://drive.google.com/file/d/abc123
Drive Shortner Link - ["https://gplinks.in/xyz","https://droplink.co/pqr"]

FilePress - https://filepress.in/file/456xyz
FilePress Shortner Link - ["https://gplinks.in/lmn","https://droplink.co/uvw"]
```

#### Get Help
```
/start - Welcome message
/help - Show all commands
```

### For Admins Only

#### Shortener Management

**Add a Shortener:**
```
/addshort
```
The bot will guide you through:
1. Enter shortener name (e.g., "GP Link")
2. Enter base API URL (e.g., `https://gplinks.in/api?api=`)
3. Enter your API key

**List All Shorteners:**
```
/listshort
```

**Toggle Shortener (Pause/Resume):**
```
/toggleshort 1
```

**Remove a Shortener:**
```
/removeshort 2
```

#### Uploader Management

**Add an Uploader:**
```
/addupload
```
The bot will guide you through:
1. Enter platform name (e.g., "FilePress")
2. Enter API endpoint (e.g., `https://filepress.in/api/upload`)
3. Enter your API key

**List All Uploaders:**
```
/listupload
```

**Toggle Uploader (Pause/Resume):**
```
/toggleupload 1
```

**Remove an Uploader:**
```
/removeupload 1
```

## 🎯 Complete Setup Example

### Step 1: Add Your First Shortener

```
You: /addshort
Bot: Please enter the shortener name:
You: GP Link
Bot: Please enter the base API URL (example: https://gplinks.in/api?api=):
You: https://gplinks.in/api?api=
Bot: Please enter your API key:
You: your_api_key_here
Bot: ✅ Shortener 'GP Link' added successfully!
```

### Step 2: Add Your First Uploader

```
You: /addupload
Bot: Enter upload platform name:
You: FilePress
Bot: Enter API endpoint (example: https://filepress.in/api/upload):
You: https://filepress.in/api/upload
Bot: Enter API key:
You: your_filepress_api_key
Bot: ✅ Uploader 'FilePress' added successfully!
```

### Step 3: Upload a File

```
You: /upload https://drive.google.com/file/d/abc123
Bot: ⏳ Processing your request...
Bot: Drive link - https://drive.google.com/file/d/abc123
     Drive Shortner Link - ["https://gplinks.in/xyz"]
     
     FilePress - https://filepress.in/file/456xyz
     FilePress Shortner Link - ["https://gplinks.in/lmn"]
```

## 🔒 Security

- Only users with IDs in `ADMIN_ID` can add/remove/toggle shorteners and uploaders
- All other users can only use the `/upload` command
- Invalid commands return helpful error messages

## 📝 Logging

All uploads are automatically logged to `logs.json`:

```json
[
  {
    "user": "john_doe",
    "user_id": 123456789,
    "link": "https://drive.google.com/file/d/abc123",
    "timestamp": "2025-10-24T18:45:00Z"
  }
]
```

## ⚠️ Error Handling

The bot handles various error scenarios:

| Error | Message |
|-------|---------|
| Invalid link format | ⚠️ Invalid or unsupported link format. |
| No active shorteners | ⚠️ Please add at least one active shortener. |
| No active uploaders | ⚠️ No active upload platforms configured. |
| Upload failed | ⚠️ Upload failed for \<platform\>. Check API key or URL. |
| Shortener failed | ⚠️ Shortener \<name\> failed. Skipped. |
| Non-admin access | 🚫 You don't have permission to use this command. |
| Unknown command | ❌ Unknown command. Type /help for options. |

## 🔌 API Integration

### Shortener API Format

Most URL shorteners follow this pattern:
```
https://api.example.com/api?api=YOUR_KEY&url=URL_TO_SHORTEN
```

The bot automatically handles common response formats:
- `{"shortenedUrl": "..."}`
- `{"shorturl": "..."}`
- `{"short_url": "..."}`
- `{"url": "..."}`
- `{"link": "..."}`

### Uploader API Format

Upload platforms typically accept:
```
POST https://api.example.com/upload
Headers: Authorization: Bearer YOUR_KEY
Body: url=FILE_URL
```

Common response formats:
- `{"url": "..."}`
- `{"link": "..."}`
- `{"download_url": "..."}`
- `{"file_url": "..."}`

## 🛠️ Troubleshooting

### Bot doesn't respond
- Check if `BOT_TOKEN` in `.env` is correct
- Ensure the bot is running (`python main.py`)
- Check console for error messages

### Upload fails
- Verify your uploader API key is valid
- Check if the API endpoint is correct
- Ensure the file URL is accessible

### Shortener fails
- Verify your shortener API key is valid
- Check if the base API URL includes `?api=` at the end
- Some shorteners have rate limits

### Permission denied
- Ensure your user ID is in `ADMIN_ID` in `.env`
- Restart the bot after changing `.env`

## 📊 Config Files

### shorteners.json
```json
[
  {
    "name": "GP Link",
    "base": "https://gplinks.in/api?api=",
    "api": "YOUR_API_KEY",
    "status": "active"
  }
]
```

### uploads.json
```json
[
  {
    "name": "FilePress",
    "endpoint": "https://filepress.in/api/upload",
    "api": "YOUR_API_KEY",
    "status": "active"
  }
]
```

## 🚀 Advanced Features

### Multiple Shorteners
Add as many shorteners as you want. Each link will be shortened using all active shorteners.

### Multiple Uploaders
Add multiple upload platforms. Files will be uploaded to all active platforms.

### Pause/Resume
Temporarily disable shorteners or uploaders without removing them:
```
/toggleshort 1
/toggleupload 2
```

## 📜 License

This project is open source and available for personal and commercial use.

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review console logs for error messages
3. Verify all API keys are valid
4. Ensure config files are properly formatted

## 🎉 Credits

Developed with ❤️ for efficient file management and sharing.

---

**Happy Uploading! 🚀**