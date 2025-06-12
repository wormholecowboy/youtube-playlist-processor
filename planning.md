# YouTube Transcript Idea Extraction and Emailing

## Project Overview

The aim of this project is to automate the extraction of key ideas from YouTube playlist transcripts and deliver them to your email inbox on a weekly basis. This process involves several critical stages:

- Data ingestion
- AI-driven idea extraction
- Structured and unstructured data storage
- Email delivery
- Automated scheduling

## Technology Choices & Integration

### Core Technologies

- **PydanticAI (AI Agent Framework)**: Core for intelligent processing, enabling structured idea extraction with predefined schemas.
- **youtube-transcript-api**: Handles direct transcript access from YouTube video IDs.
- **Mailgun**: Ensures consistent and formatted email delivery.
- **Cron**: Provides weekly automation for the entire process.
- **Supabase**: PostgreSQL database for structured data storage.
- **Google Docs**: For storing raw, full transcripts in a human-readable format.

## High-Level Project Plan

### 1. Setup and Configuration

- **Environment Setup**: Initialize Python development environment.
- **API Key Acquisition**: Obtain necessary API keys:
  - Mailgun
  - Google (for Google Docs API)
  - LLM (e.g., Google Gemini for PydanticAI)
- **Supabase Project Setup**: Create project and define tables.
- **Environment Variables**: Configure all sensitive information.

### 2. Core Components Development

#### YouTube Playlist & Transcript Fetcher
- Retrieve video IDs from playlists
- Fetch transcripts using youtube-transcript-api
- Handle missing/multi-language transcripts

#### PydanticAI Idea Extractor
- Define Pydantic model for idea schema
- Create agent for processing transcript text
- Implement chunking strategy
- Add error handling and validation
- Store extracted ideas in Supabase with metadata from Youtube video

#### Weekly Email Generator
- Query Supabase for weekly ideas
- Format ideas into readable summary
- Generate HTML email content
- Integrate with Mailgun for delivery

### 3. Automation and Deployment

- **Main Orchestration Script**: Single script to run all components
- **Cron Job Setup**: Weekly automation
- **Monitoring**: Logging and error handling
- **Containerization**: Optional Docker setup

### 4. Testing and Refinement

- Component testing
- LLM evaluation

## Data Storage Details (Supabase)

### Database Schema

#### extracted_ideas
- id (PK)
- video_id
- video_title
- video_url
- summary
- keywords (array/text)
- extracted_at
- confidence_score (optional)

## Project Structure

```
youtube_ideas_extractor/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── youtube_fetcher.py
│   ├── ai_extractor.py
│   ├── data_manager.py
│   ├── email_generator.py
│   ├── mailgun_sender.py
│   └── main_orchestrator.py
├── tests/
│   ├── __init__.py
│   ├── test_youtube_fetcher.py
│   ├── test_ai_extractor.py
│   ├── test_data_manager.py
│   └── test_email_generator.py
├── scripts/
│   ├── run_weekly_job.sh
│   └── setup_db.py
├── docs/
│   └── architecture.md
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
```

