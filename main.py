#!/usr/bin/env python3
"""
Main script to demonstrate YouTubeFetcher functionality.
"""

import os
import sys
from dotenv import load_dotenv

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.logging_config import setup_logging
from src.youtube_fetcher import YouTubeFetcher

# Load environment variables
load_dotenv()

def fetch_and_process_videos(fetcher, playlist_url: str, logger):
    """Fetch and process videos from a playlist."""
    def extract_playlist_id(url: str) -> str:
        """Extract playlist ID from YouTube playlist URL."""
        if "list=" in url:
            return url.split("list=")[1].split("&")[0]
        else:
            raise ValueError(f"Invalid playlist URL: {url}")

    playlist_id = extract_playlist_id(playlist_url)
    logger.info(f"Processing playlist URL: {playlist_url}")
    logger.info(f"Extracted playlist ID: {playlist_id}")

    # Get video IDs from playlist
    video_ids = fetcher.get_playlist_video_ids(playlist_id)
    logger.info(f"Found {len(video_ids)} videos in playlist")

    # Process all videos in the playlist
    for i, video_id in enumerate(video_ids, 1):
        logger.info(f"Processing video {i}/{len(video_ids)}: {video_id}")

        # Fetch transcript
        transcript_result = fetcher.fetch_transcript(video_id)

        if transcript_result['status'] == 'available':
            text_length = len(transcript_result['text'])
            language = transcript_result['language']
            logger.info(f"✓ Transcript available: {text_length} characters, language: {language}")

            # Store transcript in Google Docs (placeholder implementation)
            doc_url = fetcher.store_raw_transcript_in_google_docs(video_id, transcript_result['text'])
            if doc_url:
                logger.info(f"✓ Transcript stored in Google Docs: {doc_url}")

        else:
            logger.warning(f"✗ Transcript not available: {transcript_result['status']}")

    logger.info("Playlist processing completed successfully")


def main():
    """Main function to process transcripts from all example playlists."""

    # Setup logging
    logger = setup_logging()
    logger.info("Starting YouTube Fetcher for all example playlists")

    # Example YouTube playlist URLs that would be useful for idea extraction
    example_playlists = [
        "https://www.youtube.com/playlist?list=PLgBzZN2MBL00NGEQqQ_ORvigykKJJCIBm",
        "https://www.youtube.com/playlist?list=PL0ccfwBkWtNNoJqDb-F0pWm74VGsJ1FGk",
        "https://www.youtube.com/playlist?list=PL0ccfwBkWtNPF5QRysBXJf8pqhDoUW5aY"
    ]

    def extract_playlist_id(url: str) -> str:
        """Extract playlist ID from YouTube playlist URL."""
        if "list=" in url:
            return url.split("list=")[1].split("&")[0]
        else:
            raise ValueError(f"Invalid playlist URL: {url}")

    # Check if YouTube API key is configured
    if not os.getenv('YOUTUBE_API_KEY'):
        logger.error("YOUTUBE_API_KEY not found in environment variables")
        logger.info("Please copy .env.example to .env and add your YouTube API key")
        return

    # Initialize YouTubeFetcher
    try:
        fetcher = YouTubeFetcher()
        logger.info("YouTubeFetcher initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize YouTubeFetcher: {e}")
        return

    # Process all example playlists
    try:
        for i, playlist_url in enumerate(example_playlists, 1):
            playlist_id = extract_playlist_id(playlist_url)
            logger.info(f"Processing playlist {i}/{len(example_playlists)}: {playlist_id}")
            fetch_and_process_videos(fetcher, playlist_url, logger)
            logger.info(f"Completed playlist {i}/{len(example_playlists)}")
        
        logger.info("All playlists processed successfully")
        
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise

if __name__ == "__main__":
    main()
