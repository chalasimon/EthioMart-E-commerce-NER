import os
import csv
import asyncio
from datetime import datetime
from telethon import TelegramClient, errors
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv('.env')

# Configuration
API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')
PHONE = os.getenv('PHONE')
SESSION_NAME = 'ethiomart_scraper'
DATA_DIR = 'data'
RAW_DIR = os.path.join(DATA_DIR, 'raw')
MEDIA_DIR = os.path.join(DATA_DIR, 'media')
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

# Amharic e-commerce channels to monitor
CHANNELS = [
    '@ZemenExpress',
    '@qnashcom',
    '@AwasMart',
    '@marakibrand',
    '@ethio_brand_collection'
]


async def scrape_channel(client, channel_username, writer):
    """Scrape messages from a Telegram channel with enhanced error handling"""
    try:
        print(f"\nScraping {channel_username}...")
        entity = await client.get_entity(channel_username)
        channel_title = entity.title  # Extract the channel's title
        async for message in client.iter_messages(entity, limit=1000):
            try:
                # Skip service messages
                if not message.message and not message.media:
                    continue
                
                # Extract text and media
                text_content = message.message or ""
                media_path = None
                ocr_text = ""
                
                if message.media:
                    filename = f"{channel_username}_{message.id}.jpg"
                    media_path = os.path.join(MEDIA_DIR, filename)
                    
                    try:
                        await client.download_media(message.media, file=media_path)
                    except Exception as e:
                        print(f"Media processing failed for {message.id}: {e}")
                
                # Write to CSV
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
                print(f"Error processing message {message.id}: {e}")
                continue
                
    except errors.FloodWaitError as fwe:
        print(f"Flood wait required: {fwe} seconds")
        await asyncio.sleep(fwe.seconds)
    except Exception as e:
        print(f"Fatal error scraping {channel_username}: {e}")

async def main():
    """Main scraping function"""
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    
    # Prepare data file with headers
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(RAW_DIR, f'telegram_data_{timestamp}.csv')
    
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Channel Title',
            'Channel Username',
            'ID',
            'Message',
            'Date',
            'Media Path',
            'Views'
        ])
        
        # Scrape all channels with rate limiting
        for channel in CHANNELS:
            await scrape_channel(client, channel, writer)
            await asyncio.sleep(5)  # Be gentle with Telegram servers
    
    print(f"\nScraping complete! Data saved to {output_file}")
    await client.disconnect()

if __name__ == "__main__":
    # Run with asyncio
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    finally:
        loop.close()