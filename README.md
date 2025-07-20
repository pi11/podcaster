# YouTube to Telegram Podcast Manager

An application for automating YouTube video downloads and publishing them as audio files to Telegram channels. This project was created for easing publishing to telegram channel - https://t.me/mp3dreams

## Features

### Core Capabilities
- **Automatic downloading** of YouTube channel videos in MP3 format
- **Telegram bot** for automated podcast publishing
- **Content filtering** by keywords and categories
- **Channel and source management** via web interface
- **Statistics** and publication monitoring
- **Automatic tagging** with hashtag extraction
- **Web panel** for content management

### Technical Features
- **Audio compression** for files larger than 50 MB
- **Metadata embedding** and cover art in MP3 files
- **Publication scheduler** (not used for now)
- **Video duration filtering**
- **Thumbnail support**
- **CLI interface** for automation


## Installation

### Requirements
- Python 3.12+
- PostgreSQL
- yt-dlp
- ffmpeg (for compression)

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file:
```env
DB_URL=postgres://username:password@localhost:5432/podcaster
TG_TOKEN=your_telegram_bot_token
TG_CHANNEL=@your_channel_name
DEBUG=False
MEDIA_DIR=media
```

### Database Initialization
```bash
aerich init -t app.config.TORTOISE_ORM
aerich init-db
aerich migrate
aerich upgrade
```

## Usage

### CLI Commands

#### Content Download
```bash
# Download from all sources
poetry run podcast download

# Download from specific source
poetry run podcast download --source-id 1

# Download specific video
poetry run podcast download --url "https://youtube.com/watch?v=..." --tg-channel 1

```

### Run Web Interface
```bash
python web.py
# Available at http://localhost:8000
```

### Run Telegram Bot
```bash
python tg_bot.py
```

## Data Models

### Podcast
- `url` - YouTube video URL
- `yt_id` - YouTube video ID
- `name` - Title
- `description` - Description
- `source` - Source (YouTube channel)
- `tg_channel` - Telegram channel for publishing
- `publication_date` - Publication date
- `is_active` - Whether podcast is active
- `is_posted` - Whether posted
- `is_processed` - Whether processed
- `is_downloaded` - Whether downloaded
- `file` - File path
- `filesize` - File size
- `duration` - Duration
- `categories` - Categories

### Source (YouTube Channels)
- `url` - Channel URL
- `name` - Name
- `min_duration` / `max_duration` - Duration filter
- `only_related` - Theme-related videos only
- `tg_channel` - Associated Telegram channel
- `max_videos_per_channel` - Video limit
- `extract_tags` - Extract tags

### TgChannel
- `name` - Channel name
- `tg_id` - Telegram ID
- `auto_post` - Auto-posting enabled

### Category
- `name` - Category name

### CategoryIdentification
- Keywords for automatic categorization

### BannedWords
- Banned words for filtering

## Features

### Audio Compression
Files larger than 50 MB are automatically compressed: (Telegram limit for media size for bots)
- First to 96 kbps
- If needed, to 64 kbps

### Tags and Hashtags
- Automatic extraction from titles and descriptions
- Maximum 8 hashtags per post
- Telegram formatting


### Migrations
```bash
# Create migration
aerich migrate --name "description"

# Apply migrations
aerich upgrade
```

## License

WTFPL - Do What The F*ck You Want To Public License

## Author

webii (webii@pm.me)
