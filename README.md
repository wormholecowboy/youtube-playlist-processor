# YouTube Transcript Idea Extraction and Emailing App

This application automatically extracts key ideas from YouTube playlist transcripts and delivers them to your email inbox on a weekly basis.

## Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/macOS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment template and configure your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```

4. Set up the database schema:
   ```bash
   python scripts/setup_db.py
   ```

## Configuration

The application requires the following API keys and configuration:

- **YOUTUBE_API_KEY**: YouTube Data API v3 key
- **MAILGUN_API_KEY**: Mailgun API key for email delivery
- **SUPABASE_URL** and **SUPABASE_KEY**: Supabase project credentials
- **LLM_API_KEY**: API key for your chosen LLM provider

## Usage

Run the main orchestrator to process videos and send weekly summaries:

```bash
python src/main_orchestrator.py
```

## Project Structure

- `src/`: Main application code
- `tests/`: Unit and integration tests
- `scripts/`: Utility scripts for setup and deployment
- `docs/`: Documentation files

## License

See LICENSE file for details.
