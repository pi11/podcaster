# Podcast Management CLI

A comprehensive command-line interface for managing your podcast application built with Sanic.

## Installation

```bash
# Install dependencies
poetry install

# Or install specific dependencies
poetry add click aiohttp yt-dlp pillow mutagen tortoise-orm
```

## Available Commands

### Core Management

#### `podcast status`
Show application and podcast statistics
```bash
# Basic status
poetry run podcast status

# Show only active podcasts
poetry run podcast status --active-only

# Show only downloaded podcasts  
poetry run podcast status --downloaded-only

# Output in different formats
poetry run podcast status --format json
poetry run podcast status --format csv
```

#### `podcast cleanup`
Clean up files for inactive podcasts
```bash
# Dry run (see what would be deleted)
poetry run podcast cleanup --dry-run

# Actually perform cleanup
poetry run podcast cleanup

# Verbose output
poetry run podcast cleanup --verbose

# Skip confirmation
poetry run podcast cleanup --force
```

#### `podcast list-inactive`
List inactive podcasts
```bash
# All inactive podcasts
poetry run podcast list-inactive

# Only inactive podcasts that are downloaded
poetry run podcast list-inactive --downloaded-only
```

#### `podcast delete`
Delete a specific podcast by ID
```bash
# Delete podcast with ID 123
poetry run podcast delete 123

# Skip confirmation
poetry run podcast delete 123 --force
```

### Content Processing

#### `podcast add-categories`
Add AI-generated categories to podcasts
```bash
# Process all podcasts
poetry run podcast add-categories

# Process only active podcasts
poetry run podcast add-categories --active-only

# Verbose output
poetry run podcast add-categories --verbose
```

#### `podcast process-files`
Process podcast files (compression + metadata embedding)
```bash
# Process all unprocessed files
poetry run podcast process-files

# Run continuously (every 20 seconds)
poetry run podcast process-files --watch

# Disable compression
poetry run podcast process-files --no-compress

# Set compression bitrate
poetry run podcast process-files --bitrate 32k

# Verbose output
poetry run podcast process-files --verbose
```

#### `podcast set-dates`
Set publication dates for podcasts
```bash
# Set publication dates
poetry run podcast set-dates

# Set current date first, then schedule
poetry run podcast set-dates --current-date

# Verbose output
poetry run podcast set-dates --verbose
```

### Content Download

#### `podcast download`
Download videos from YouTube channels
```bash
# Download from all sources
poetry run podcast download

# Download from specific source
poetry run podcast download --source-id 123

# Set maximum videos per channel
poetry run podcast download --max-videos 20

# Set audio quality
poetry run podcast download --quality 128

# Dry run (see what would be downloaded)
poetry run podcast download --dry-run

# Verbose output
poetry run podcast download --verbose
```

## Common Workflows

### Daily Content Processing
```bash
# 1. Download new content
poetry run podcast download --verbose

# 2. Process files (compress + metadata)
poetry run podcast process-files --verbose

# 3. Add categories
poetry run podcast add-categories --active-only

# 4. Set publication dates
poetry run podcast set-dates --verbose

# 5. Check status
poetry run podcast status
```

### Cleanup Old Content
```bash
# 1. See what would be cleaned
poetry run podcast cleanup --dry-run

# 2. Actually clean up
poetry run podcast cleanup --verbose

# 3. Check final status
poetry run podcast status
```

### Continuous Processing
```bash
# Run file processing continuously
poetry run podcast process-files --watch --verbose
```

## Configuration

### Environment Variables
```bash
export MEDIA_DIR="media"  # Directory for downloaded files
```

### Dependencies Required
- `yt-dlp` - for YouTube downloads
- `ffmpeg` - for audio compression
- `PIL/Pillow` - for image processing
- `mutagen` - for metadata embedding

### Installing External Dependencies
```bash
# Install yt-dlp
pip install yt-dlp

# Install ffmpeg (system level)
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

## Output Formats

### JSON Output Example
```bash
poetry run podcast status --format json
```
```json
{
  "summary": {
    "total": 150,
    "active": 120,
    "downloaded": 80,
    "inactive_downloaded": 5
  },
  "podcasts": [...]
}
```

### CSV Output Example
```bash
poetry run podcast status --format csv
```
```csv
id,name,is_active,is_downloaded,file
1,Episode 1,true,true,/path/to/file.mp3
2,Episode 2,true,false,
```

## Logging

All commands support verbose logging with the `-v` or `--verbose` flag. Logs are written to:
- Console (always)
- `logs/podcast_cli.log` (file)

## Error Handling

The CLI includes comprehensive error handling:
- Graceful database connection handling
- File operation error recovery
- Progress bars for long operations
- Detailed error messages
- Transaction rollback on failures

## Development

### Adding New Commands
1. Add your command function to `app/cli.py`
2. Use the `@cli.command()` decorator
3. Follow the existing patterns for async operations
4. Include proper error handling and logging

### Testing Commands
```bash
# Test with dry-run flags where available
poetry run podcast cleanup --dry-run
poetry run podcast download --dry-run

# Use verbose output for debugging
poetry run podcast [command] --verbose
```