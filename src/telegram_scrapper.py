import os
import csv
import asyncio
from datetime import datetime
from telethon import TelegramClient, errors
from dotenv import load_dotenv
import io 

def load_config():
    # Loads configuration from environment variables.
    load_dotenv('.env')
    return {
        'API_ID': os.getenv('TG_API_ID'),
        'API_HASH': os.getenv('TG_API_HASH'),
        'PHONE': os.getenv('PHONE'), # Not directly used in the scraper but good for client setup
        'SESSION_NAME': 'ethiomart_scraper',
        'DATA_DIR': '../data',
        'RAW_DIR_NAME': 'raw',
        'MEDIA_DIR_NAME': 'media',
        'CHANNELS': [
            '@meneshayeofficial',
            '@qnashcom',
            '@AwasMart',
            '@marakibrand',
            '@ethio_brand_collection'
        ]
    }


def setup_directories(base_data_dir, raw_dir_name, media_dir_name):
    """Creates necessary data directories."""
    raw_dir = os.path.join(base_data_dir, raw_dir_name)
    media_dir = os.path.join(base_data_dir, media_dir_name)
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)
    return raw_dir, media_dir

def get_output_filepath(raw_dir):
    # Generates a timestamped path for the CSV output file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(raw_dir, f'telegram_data_{timestamp}.csv')

def write_csv_headers(writer):
    """Writes the CSV header row."""
    writer.writerow([
        'Channel Title',
        'Channel Username',
        'ID',
        'Message',
        'Date',
        'Media Path',
        'Views'
    ])

# --- Telegram Scraper Module (e.g., telegram_scraper.py) ---

async def download_media_if_exists(client, message, media_dir, channel_username):
    """Downloads media from a message if present, returns the path."""
    if message.media:
        filename = f"{channel_username}_{message.id}.jpg"
        media_path = os.path.join(media_dir, filename)
        try:
            await client.download_media(message.media, file=media_path)
            return media_path
        except Exception as e:
            print(f"Media download failed for message {message.id}: {e}")
            return None
    return None

async def scrape_channel(client, channel_username, writer, media_dir):
    """Scrapes messages from a single Telegram channel."""
    print(f"\nScraping {channel_username}...")
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title

        async for message in client.iter_messages(entity, limit=1000):
            try:
                # Skip service messages
                if not message.message and not message.media:
                    continue

                text_content = message.message or ""
                media_path = await download_media_if_exists(client, message, media_dir, channel_username)

                writer.writerow([
                    channel_title,
                    channel_username,
                    message.id,
                    text_content,
                    message.date,
                    media_path,
                    message.views or 0
                ])
            except Exception as e:
                print(f"Error processing message {message.id} in {channel_username}: {e}")
                continue

    except errors.FloodWaitError as fwe:
        print(f"Flood wait required for {channel_username}: {fwe.seconds} seconds")
        await asyncio.sleep(fwe.seconds)
    except Exception as e:
        print(f"Fatal error scraping {channel_username}: {e}")



async def main():
    """Orchestrates the scraping process."""
    config = load_config()

    api_id = config['API_ID']
    api_hash = config['API_HASH']
    session_name = config['SESSION_NAME']
    channels = config['CHANNELS']
    data_dir = config['DATA_DIR']
    raw_dir_name = config['RAW_DIR_NAME']
    media_dir_name = config['MEDIA_DIR_NAME']

    if not api_id or not api_hash:
        print("Error: TG_API_ID and TG_API_HASH must be set in your .env file.")
        return

    raw_dir, media_dir = setup_directories(data_dir, raw_dir_name, media_dir_name)
    output_file = get_output_filepath(raw_dir)

    client = TelegramClient(session_name, api_id, api_hash)
    await client.start()

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            write_csv_headers(writer)

            for channel in channels:
                await scrape_channel(client, channel, writer, media_dir)
                await asyncio.sleep(5) # Be gentle with Telegram servers
        print(f"\nScraping complete! Data saved to {output_file}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    # Run with asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    finally:
        if not loop.is_closed():
            loop.close()