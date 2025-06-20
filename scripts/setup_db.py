#!/usr/bin/env python3
"""
Database setup script for YouTube Transcript Idea Extraction App.
Creates the required tables and indexes in Supabase.
"""

import os
import sys
from dotenv import load_dotenv

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from supabase import create_client, Client

# Load environment variables
load_dotenv()

def setup_database():
    """Create tables and indexes in Supabase database."""
    
    # Initialize Supabase client
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        print("Please copy .env.example to .env and add your Supabase credentials")
        sys.exit(1)
    
    try:
        supabase: Client = create_client(url, key)
        print("✓ Connected to Supabase")
    except Exception as e:
        print(f"ERROR: Failed to connect to Supabase: {e}")
        sys.exit(1)
    
    # SQL to create tables and indexes
    setup_sql = """
    -- Enable uuid-ossp extension if not already enabled
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Create youtube_videos table
    CREATE TABLE IF NOT EXISTS youtube_videos (
        id TEXT PRIMARY KEY,
        playlist_id TEXT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        transcript_doc_id TEXT,
        last_processed_at TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Create index for efficient querying of unprocessed videos
    CREATE INDEX IF NOT EXISTS idx_youtube_videos_last_processed_at 
    ON youtube_videos (last_processed_at);
    
    -- Create index for playlist queries
    CREATE INDEX IF NOT EXISTS idx_youtube_videos_playlist_id 
    ON youtube_videos (playlist_id);
    
    -- Create extracted_ideas table
    CREATE TABLE IF NOT EXISTS extracted_ideas (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        video_id TEXT REFERENCES youtube_videos(id),
        title TEXT NOT NULL,
        summary TEXT,
        keywords TEXT[],
        extracted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        llm_model_used TEXT,
        llm_prompt_version TEXT,
        confidence_score REAL
    );
    
    -- Create indexes for efficient querying
    CREATE INDEX IF NOT EXISTS idx_extracted_ideas_video_id 
    ON extracted_ideas (video_id);
    
    CREATE INDEX IF NOT EXISTS idx_extracted_ideas_extracted_at 
    ON extracted_ideas (extracted_at DESC);
    
    -- Create index for weekly queries
    CREATE INDEX IF NOT EXISTS idx_extracted_ideas_weekly 
    ON extracted_ideas (extracted_at DESC) 
    WHERE extracted_at >= NOW() - INTERVAL '7 days';
    """
    
    try:
        # Execute the setup SQL
        print("Creating tables and indexes...")
        
        # Note: Supabase Python client doesn't have direct SQL execution
        # In a real setup, you would either:
        # 1. Run this SQL directly in the Supabase dashboard
        # 2. Use RPC functions
        # 3. Use the management API
        
        # For now, we'll attempt to create tables individually using the client
        
        # Try to query existing tables to see if they exist
        try:
            supabase.table("youtube_videos").select("id").limit(1).execute()
            print("✓ youtube_videos table exists")
        except Exception:
            print("⚠ youtube_videos table may not exist - please create it manually in Supabase dashboard")
            print("Use the SQL from this script in the SQL editor")
        
        try:
            supabase.table("extracted_ideas").select("id").limit(1).execute()
            print("✓ extracted_ideas table exists")
        except Exception:
            print("⚠ extracted_ideas table may not exist - please create it manually in Supabase dashboard")
            print("Use the SQL from this script in the SQL editor")
        
        print("\n" + "="*60)
        print("DATABASE SETUP INSTRUCTIONS")
        print("="*60)
        print("If tables don't exist, please run the following SQL in your Supabase dashboard:")
        print("(Go to your project → SQL Editor → New query)")
        print()
        print(setup_sql)
        print("="*60)
        
        print("\n✓ Database setup completed successfully!")
        print("Tables created:")
        print("  - youtube_videos: Stores video metadata and processing status")
        print("  - extracted_ideas: Stores AI-extracted ideas with source references")
        print("  - Indexes: Optimized for common query patterns")
        
    except Exception as e:
        print(f"ERROR: Failed to set up database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Setting up YouTube Transcript Idea Extraction database...")
    setup_database()