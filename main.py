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

def main():
    """Main function to test YouTubeFetcher with example playlists."""
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting YouTube Fetcher demonstration")
    
    # Example YouTube playlist URLs that would be useful for idea extraction
    example_playlists = [
        "https://www.youtube.com/playlist?list=PLgBzZN2MBL00NGEQqQ_ORvigykKJJCIBm"
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
    
    # Demonstrate functionality with the first playlist
    demo_playlist_url = example_playlists[0]
    demo_playlist_id = extract_playlist_id(demo_playlist_url)
    logger.info(f"Testing with playlist URL: {demo_playlist_url}")
    logger.info(f"Extracted playlist ID: {demo_playlist_id}")
    
    try:
        # Get video IDs from playlist
        video_ids = fetcher.get_playlist_video_ids(demo_playlist_id)
        logger.info(f"Found {len(video_ids)} videos in playlist")
        
        # Test transcript fetching with first few videos (limit to avoid API quota)
        test_videos = video_ids[:3]  # Only test first 3 videos
        
        for i, video_id in enumerate(test_videos, 1):
            logger.info(f"Testing transcript fetch for video {i}/{len(test_videos)}: {video_id}")
            
            # Fetch transcript
            transcript_result = fetcher.fetch_transcript(video_id)
            
            if transcript_result['status'] == 'available':
                text_length = len(transcript_result['text'])
                language = transcript_result['language']
                logger.info(f"✓ Transcript available: {text_length} characters, language: {language}")
                
                # Test Google Docs storage (placeholder implementation)
                doc_url = fetcher.store_raw_transcript_in_google_docs(video_id, transcript_result['text'])
                if doc_url:
                    logger.info(f"✓ Transcript stored in Google Docs: {doc_url}")
                
            else:
                logger.warning(f"✗ Transcript not available: {transcript_result['status']}")
        
        logger.info("YouTubeFetcher demonstration completed successfully")
        
        # Print summary of all example playlists
        print("\n" + "="*60)
        print("EXAMPLE PLAYLISTS FOR IDEA EXTRACTION")
        print("="*60)
        for i, playlist_url in enumerate(example_playlists, 1):
            playlist_id = extract_playlist_id(playlist_url)
            print(f"\n📚 Playlist {i}")
            print(f"   URL: {playlist_url}")
            print(f"   ID:  {playlist_id}")
        
        print(f"\n💡 To use these playlists, update your configuration with the playlist URLs above.")
        print(f"   The current demo used: {demo_playlist_url}")
        
    except Exception as e:
        logger.error(f"Error during demonstration: {e}")
        raise

if __name__ == "__main__":
    main()
