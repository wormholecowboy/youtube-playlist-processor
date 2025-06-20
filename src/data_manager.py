import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from supabase import create_client, Client
from .config import Config

logger = logging.getLogger(__name__)

class DataManager:
    """Handles all database operations with Supabase."""
    
    def __init__(self):
        """Initialize the Supabase client using configuration."""
        self.supabase: Client = create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_KEY
        )
        logger.info("DataManager initialized with Supabase client")
    
    def save_video_metadata(self, video_id: str, title: str, url: str, playlist_id: str, google_doc_link: str) -> None:
        """
        Save or update video metadata in the youtube_videos table.
        
        Args:
            video_id: YouTube video ID
            title: Video title
            url: Video URL
            playlist_id: Playlist ID the video belongs to
            google_doc_link: URL to the Google Doc containing the transcript
        """
        try:
            video_data = {
                "id": video_id,
                "playlist_id": playlist_id,
                "title": title,
                "url": url,
                "transcript_doc_id": google_doc_link,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Use upsert to handle both insert and update cases
            response = self.supabase.table("youtube_videos").upsert(video_data).execute()
            
            if response.data:
                logger.info(f"Successfully saved video metadata for {video_id}: {title}")
            else:
                logger.warning(f"No data returned when saving video metadata for {video_id}")
                
        except Exception as e:
            logger.error(f"Failed to save video metadata for {video_id}: {e}")
            raise
    
    def get_unprocessed_videos(self, threshold_days: int = 7) -> List[Dict]:
        """
        Get videos that haven't been processed or were last processed more than threshold_days ago.
        
        Args:
            threshold_days: Number of days after which a video is considered stale
            
        Returns:
            List of video records that need processing
        """
        try:
            threshold_date = datetime.utcnow() - timedelta(days=threshold_days)
            threshold_iso = threshold_date.isoformat()
            
            # Query for videos where last_processed_at is null or older than threshold
            response = self.supabase.table("youtube_videos").select("*").or_(
                f"last_processed_at.is.null,last_processed_at.lt.{threshold_iso}"
            ).execute()
            
            videos = response.data or []
            logger.info(f"Found {len(videos)} unprocessed videos (threshold: {threshold_days} days)")
            
            return videos
            
        except Exception as e:
            logger.error(f"Failed to get unprocessed videos: {e}")
            raise
    
    def save_extracted_idea(self, video_id: str, idea: Dict) -> None:
        """
        Save an extracted idea to the extracted_ideas table.
        
        Args:
            video_id: YouTube video ID the idea was extracted from
            idea: Dictionary containing idea data (title, summary, keywords, confidence_score)
        """
        try:
            idea_data = {
                "video_id": video_id,
                "title": idea.get("title", ""),
                "summary": idea.get("summary", ""),
                "keywords": idea.get("keywords", []),
                "confidence_score": idea.get("confidence_score"),
                "extracted_at": datetime.utcnow().isoformat(),
                "llm_model_used": idea.get("llm_model_used", "unknown"),
                "llm_prompt_version": idea.get("llm_prompt_version", "v1.0")
            }
            
            response = self.supabase.table("extracted_ideas").insert(idea_data).execute()
            
            if response.data:
                logger.info(f"Successfully saved idea '{idea_data['title']}' for video {video_id}")
            else:
                logger.warning(f"No data returned when saving idea for video {video_id}")
                
        except Exception as e:
            logger.error(f"Failed to save extracted idea for video {video_id}: {e}")
            raise
    
    def get_ideas_from_last_week(self) -> List[Dict]:
        """
        Get all ideas extracted in the last week.
        
        Returns:
            List of idea dictionaries from the past week
        """
        try:
            week_ago = datetime.utcnow() - timedelta(days=7)
            week_ago_iso = week_ago.isoformat()
            
            response = self.supabase.table("extracted_ideas").select(
                "*"
            ).gte("extracted_at", week_ago_iso).order("extracted_at", desc=True).execute()
            
            ideas = response.data or []
            logger.info(f"Found {len(ideas)} ideas from the last week")
            
            return ideas
            
        except Exception as e:
            logger.error(f"Failed to get ideas from last week: {e}")
            raise
    
    def update_video_processed_status(self, video_id: str) -> None:
        """
        Update the last_processed_at timestamp for a video to mark it as processed.
        
        Args:
            video_id: YouTube video ID to mark as processed
        """
        try:
            update_data = {
                "last_processed_at": datetime.utcnow().isoformat()
            }
            
            response = self.supabase.table("youtube_videos").update(update_data).eq("id", video_id).execute()
            
            if response.data:
                logger.info(f"Updated processed status for video {video_id}")
            else:
                logger.warning(f"No rows updated when marking video {video_id} as processed")
                
        except Exception as e:
            logger.error(f"Failed to update processed status for video {video_id}: {e}")
            raise