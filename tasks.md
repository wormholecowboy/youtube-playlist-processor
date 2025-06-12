# Development To-Do List: YouTube Transcript Idea Extraction and Emailing App

This document outlines specific tasks for building the "YouTube Transcript Idea Extraction and Emailing" application, following the enhanced project plan. Each step is designed to be a clear, actionable item.

---

## 1. Setup and Configuration

### 1.1 Initialize Project Structure
- [x] Create the main project directory: `youtube_ideas_extractor/`
- [x] Inside, create the following directories:
  - `src/`
  - `tests/`
  - `scripts/`
  - `docs/`
- [x] Add empty `__init__.py` files to `src/` and `tests/`

### 1.2 Set up Python Environment
- [x] Create a Python virtual environment:
  ```bash
  python -m venv venv
  ```

- [x] Activate the virtual environment:
  - **Linux/macOS**: `source venv/bin/activate`

### Define Dependencies
- [x] Add initial core dependencies to `requirements.txt`:
  ```
  python-dotenv
  google-api-python-client
  google-auth-oauthlib
  google-auth-httplib2
  youtube-transcript-api
  supabase-py
  requests
  jinja2
  pydantic
  pydantic-ai  # or specific LLM client like google-generativeai
  ```

### 1.3 Configuration Setup
- [x] Create `src/config.py` with:
  - Config class using `os.getenv()`
  - Constants for configuration:
    - `TRANSCRIPT_CHUNK_SIZE_TOKENS`
    - `NUM_IDEAS_TO_EXTRACT_PER_VIDEO`
    - `LOG_FILE`
    - `LOG_LEVEL`

- [x] Create `.env.example` with required environment variables:
  ```env
  # API Keys
  YOUTUBE_API_KEY=your_youtube_api_key_here
  MAILGUN_API_KEY=your_mailgun_api_key_here
  SUPABASE_URL=your_supabase_url_here
  SUPABASE_KEY=your_supabase_key_here
  LLM_API_KEY=your_llm_api_key_here
  
  # App Settings
  LOG_LEVEL=INFO
  LOG_FILE=app.log
  ```

### 1.4 Configure Structured Logging
- [x] Set up `logging.basicConfig` in the main script or a dedicated logging module:
  ```python
  import logging
  from logging.handlers import RotatingFileHandler
  
  # Configure root logger
  logging.basicConfig(
      level=Config.LOG_LEVEL,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      handlers=[
          RotatingFileHandler(
              Config.LOG_FILE,
              maxBytes=5*1024*1024,  # 5MB
              backupCount=3
          ),
          logging.StreamHandler()
      ]
  )
  
  # Set log level for external libraries
  logging.getLogger('urllib3').setLevel(logging.WARNING)
  logging.getLogger('googleapiclient').setLevel(logging.INFO)
  ```

- [x] Add logger instances in all modules:
  ```python
  import logging
  logger = logging.getLogger(__name__)
  ```

## 2. Core Components Development

### 2.1 YouTubeFetcher (`src/youtube_fetcher.py`)

#### 2.1.1 Initialization
- [ ] Implement `__init__`:
  - Initialize `googleapiclient.discovery` for YouTube Data API
  - Initialize `youtube_transcript_api` client

#### 2.1.2 Video Retrieval
- [ ] Implement `get_playlist_video_ids(self, playlist_id: str) -> list[str]`:
  - Use YouTube Data API to fetch video IDs from the given playlist
  - Handle pagination to retrieve all videos
  - Log progress and completion

#### 2.1.3 Transcript Management
- [ ] Implement `fetch_transcript(self, video_id: str) -> dict`:
  - Use `youtube-transcript-api` to fetch the transcript
  - Include try-except blocks to handle `NoTranscriptFound` or other API errors
  - Return a dictionary with `text`, `language`, and `status` (available, unavailable, error)
  - Log warnings for unavailable transcripts

#### 2.1.4 Google Docs Integration
- [ ] Implement `store_raw_transcript_in_google_docs(self, video_id: str, transcript_text: str) -> str`:
  - Authenticate with Google Drive/Docs API using credentials
  - Create a new Google Doc with the transcript text
  - Set appropriate permissions for the document
  - Return the public URL or ID of the created Google Doc
  - Log success or failure of storing the transcript

### 2.2 DataManager (`src/data_manager.py`)

#### 2.2.1 Initialization
- [ ] Implement `__init__`:
  - Initialize the Supabase client using `Config.SUPABASE_URL` and `Config.SUPABASE_KEY`

#### 2.2.2 Video Metadata Management
- [ ] Implement `save_video_metadata(self, video_id: str, title: str, url: str, playlist_id: str, google_doc_link: str)`:
  - Perform an upsert operation into the `youtube_videos` table
  - Fields: `id`, `playlist_id`, `title`, `url`, `transcript_doc_id`, `created_at` (set once), `last_processed_at` (initially null or timestamp)

#### 2.2.3 Video Processing
- [ ] Implement `get_unprocessed_videos(threshold_days: int = 7) -> list[dict]`:
  - Query `youtube_videos` for videos where `last_processed_at` is null or older than threshold
  - Return list of video records

#### 2.2.4 Idea Management
- [ ] Implement `save_extracted_idea(video_id: str, idea: dict) -> None`:
  - Insert idea dictionary into `extracted_ideas` table
  - Ensure schema matches: `title`, `summary`, `keywords`, `confidence_score`
  - Link to `video_id` via foreign key

- [ ] Implement `get_ideas_from_last_week() -> list[dict]`:
  - Query `extracted_ideas` for entries from the past week
  - Return list of idea dictionaries

- [ ] Implement `update_video_processed_status(video_id: str) -> None`:
  - Update `last_processed_at` to current UTC timestamp
  - Log the update

### 2.3 PydanticAIExtractor (`src/ai_extractor.py`)

#### 2.3.1 Initialization
- [ ] Implement `__init__`:
  - Initialize PydanticAI agent with LLM configuration
  - Set up retry mechanism for API calls

#### 2.3.2 Data Models
- [ ] Define Pydantic Idea Model:
  ```python
  from pydantic import BaseModel
  from typing import List, Optional
  
  class Idea(BaseModel):
      title: str
      summary: str
      keywords: List[str] = []
      confidence_score: Optional[float] = None
  ```

#### 2.3.3 Transcript Processing
- [ ] Implement `chunk_transcript(text: str) -> list[str]`:
  - Split text based on `TRANSCRIPT_CHUNK_SIZE_TOKENS`
  - Use overlap of `TRANSCRIPT_CHUNK_OVERLAP_TOKENS`
  - Prefer token-based splitting over word count

#### 2.3.4 Idea Extraction
- [ ] Implement `extract_ideas(transcript_chunk: str) -> list[dict]`:
  - Craft LLM prompt with clear definition of "key idea"
  - Include few-shot examples for better quality
  - Use Pydantic model for response validation
  - Handle API errors and implement retries
  - Log extraction results

#### 2.3.5 Deduplication
- [ ] Implement idea deduplication:
  - Compare new ideas against existing ones
  - Options:
    - Simple string matching on titles/summaries
    - Vector embeddings with pgvector (if available)
  - Query Supabase for existing ideas within timeframe

### 2.4 EmailGenerator (`src/email_generator.py`)

#### 2.4.1 Initialization
- [ ] Implement `__init__`:
  - Set up Jinja2 environment
  - Configure template directory (e.g., `templates/`)

#### 2.4.2 Template Management
- [ ] Create template directory structure:
  ```
  templates/
  └── weekly_summary.html
  ```

- [ ] Design HTML template with:
  - Clean, responsive layout
  - Placeholders for ideas and video links
  - CSS styling for readability

#### 2.4.3 Email Generation
- [ ] Implement `generate_email_html(ideas: list[dict]) -> str`:
  - Load and render template with provided ideas
  - Include error handling for template rendering
  - Return generated HTML content

  - Load the `weekly_summary.html` template
  - Render with ideas list and current date
  - Log HTML generation status

### 2.5 MailgunSender (`src/mailgun_sender.py`)

#### 2.5.1 Initialization
- [ ] Implement `__init__`:
  - Basic logging setup
  - No special initialization required

#### 2.5.2 Email Sending
- [ ] Implement `send_email(recipient_email: str, subject: str, html_content: str) -> bool`:
  - Make POST request to Mailgun API endpoint
  - Set authentication using `Config.MAILGUN_API_KEY`
  - Include required fields:
    - `from`: Sender email from config
    - `to`: Recipient email
    - `subject`: Email subject
    - `html`: Rendered HTML content
  - Add error handling and retries
  - Log success/failure
  - Return boolean indicating success

## 3. Automation and Deployment

### 3.1 Main Orchestration Script
- [ ] Create/Update `src/main_orchestrator.py`:
  - Integrate all components in sequence
  - Add comprehensive error handling
  - Implement video processing loop with failure tolerance
  - Skip already processed videos using `DataManager.get_unprocessed_videos()`
  - Add detailed logging at each major step

### 3.2 Deployment Scripts
- [ ] Create `scripts/run_weekly_job.sh`:
  ```bash
  #!/bin/bash
  set -e  # Exit on error
  
  # Activate virtual environment
  source venv/bin/activate
  
  # Run the orchestrator and log output
  python src/main_orchestrator.py >> app.log 2>&1
  
  # Check exit status and handle errors
  if [ $? -ne 0 ]; then
      echo "[ERROR] Orchestrator failed"
      exit 1
  fi
  ```
  - Make executable: `chmod +x scripts/run_weekly_job.sh`

### 3.3 Containerization
- [ ] Create `Dockerfile`:
  ```dockerfile
  FROM python:3.9-slim-buster
  
  WORKDIR /app
  
  # Install dependencies
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  
  # Copy application code
  COPY src/ ./src/
  COPY scripts/ ./scripts/
  
  # Set up entrypoint
  ENTRYPOINT ["/bin/bash", "scripts/run_weekly_job.sh"]
  ```

- [ ] Create `.dockerignore`:
  ```
  __pycache__/
  venv/
  .env
  *.log
  ```

### 3.4 Monitoring and Error Reporting
- [ ] Set up error tracking:
  - Integrate Sentry for error monitoring
  - Configure email alerts for critical errors
  - Implement healthcheck.io ping on successful runs

### 3.5 Scheduling
- [ ] Example crontab entry:
  ```
  # Run every Monday at 9:00 AM
  0 9 * * 1 /path/to/youtube_ideas_extractor/scripts/run_weekly_job.sh
  ```

## 4. Testing and Refinement

### 4.1 Unit Testing
- [ ] Create test suite in `tests/` directory:
  - Test each component in isolation
  - Mock all external API calls
  - Include test cases for edge cases and error conditions

### 4.2 Integration Testing
- [ ] Test component interactions:
  - YouTubeFetcher → DataManager
  - PydanticAIExtractor → DataManager
  - EmailGenerator → MailgunSender

### 4.3 End-to-End Testing
- [ ] Create test fixtures:
  - Sample playlist with known videos
  - Mock transcripts
  - Expected idea outputs

- [ ] Test workflow:
  1. Process test playlist
  2. Verify Supabase records
  3. Check Google Docs creation
  4. Validate email content

### 4.4 LLM Evaluation
- [ ] Set up evaluation framework:
  - Manual review process for ideas
  - Quality metrics (relevance, uniqueness, clarity)
  - Version tracking for prompts

- [ ] Continuous improvement:
  - Regular prompt refinement
  - A/B testing of prompt variations
  - Performance tracking over time

## 5. Database Schema

### 5.1 Setup Script
- [ ] Create `scripts/setup_db.py`:
  ```python
  import os
  from supabase import create_client, Client
  from dotenv import load_dotenv
  
  load_dotenv()
  
  # Initialize Supabase client
  supabase: Client = create_client(
      os.getenv('SUPABASE_URL'),
      os.getenv('SUPABASE_KEY')
  )
  
  # Enable required extensions
  supabase.rpc('create_extension', {'extname': 'uuid-ossp'}).execute()
  
  # Create tables
  supabase.rpc('execute_sql', {
      'query': """
      CREATE TABLE IF NOT EXISTS youtube_videos (
          id TEXT PRIMARY KEY,
          playlist_id TEXT,
          title TEXT NOT NULL,
          url TEXT NOT NULL,
          transcript_doc_id TEXT,
          last_processed_at TIMESTAMP WITH TIME ZONE,
          created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
      );
      
      CREATE INDEX IF NOT EXISTS idx_youtube_videos_last_processed_at 
      ON youtube_videos (last_processed_at);
      
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
      
      CREATE INDEX IF NOT EXISTS idx_extracted_ideas_video_id 
      ON extracted_ideas (video_id);
      
      CREATE INDEX IF NOT EXISTS idx_extracted_ideas_extracted_at 
      ON extracted_ideas (extracted_at DESC);
      """
  }).execute()
  ```

### 5.2 Schema Documentation
- **youtube_videos**: Tracks video metadata and processing status
- **extracted_ideas**: Stores AI-extracted ideas with source references
- **Indexes**: Optimized for common query patterns

### 5.3 Maintenance
- [ ] Set up database backups
- [ ] Monitor query performance
- [ ] Plan for schema migrations if needed
