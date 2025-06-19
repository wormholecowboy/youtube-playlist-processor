# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Transcript Idea Extraction and Emailing App that automatically extracts key ideas from YouTube playlist transcripts and delivers them via email weekly.

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with actual API keys

# Set up database (when implemented)
python scripts/setup_db.py
```

### Running the Application
```bash
# Main demonstration script
python main.py

# Main orchestrator (when implemented)
python src/main_orchestrator.py
```

## Architecture

The application is structured around modular components:

- **YouTubeFetcher** (`src/youtube_fetcher.py`): Core service for fetching playlist video IDs and transcripts using YouTube Data API v3 and youtube-transcript-api
- **Config** (`src/config.py`): Centralized configuration management with environment variable loading
- **Logging** (`src/logging_config.py`): Structured logging with rotating file handlers

### Key Configuration Constants
- `TRANSCRIPT_CHUNK_SIZE_TOKENS = 4000`: Token size for transcript processing chunks
- `TRANSCRIPT_CHUNK_OVERLAP_TOKENS = 200`: Overlap between chunks for continuity
- `NUM_IDEAS_TO_EXTRACT_PER_VIDEO = 5`: Target number of ideas per video

### Required Environment Variables
- `YOUTUBE_API_KEY`: YouTube Data API v3 key
- `MAILGUN_API_KEY`: Email delivery service
- `SUPABASE_URL` and `SUPABASE_KEY`: Database credentials
- `LLM_API_KEY`: AI service for idea extraction

### Data Flow
1. Fetch video IDs from YouTube playlists
2. Extract transcripts using youtube-transcript-api (prefers English, falls back to available languages)
3. Store raw transcripts in Google Docs (placeholder implementation)
4. Process transcripts for idea extraction (planned)
5. Weekly email delivery (planned)

The main entry point demonstrates functionality with example educational playlists (TED Talks, MIT OpenCourseWare, Stanford CS, Y Combinator, 3Blue1Brown).