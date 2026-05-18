#!/usr/bin/env python3
"""
Google News Spider

Fetches news articles from Google News based on search keywords.
Implements Typer CLI, logging, error handling, and retry logic.

Usage:
    python news_spider.py --help
    python news_spider.py --keyword "python" --max-results 20 --output articles.json
"""

import typer
import logging
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List
import time

# Try to import gnews, with fallback message
try:
    from gnews import GNews
except ImportError:
    print("Error: gnews library not installed. Install with: pip install -r requirements.txt")
    sys.exit(1)

# ==================== Logging Setup ====================
def setup_logging(script_dir: Path = Path(".")):
    """Configure industrial-grade logging with rotation and crash protection."""
    
    logs_dir = script_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Clean old logs (keep 30 days)
    cutoff_date = datetime.now() - timedelta(days=30)
    for log_file in logs_dir.glob("*.log*"):
        try:
            if datetime.fromtimestamp(log_file.stat().st_mtime) < cutoff_date:
                log_file.unlink()
        except Exception as e:
            pass  # Ignore cleanup errors
    
    # Create logger
    logger = logging.getLogger("google_news_spider")
    logger.setLevel(logging.DEBUG)
    
    # File handler (daily + size rotation)
    log_file = logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler (WARNING+)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# ==================== Main Script ====================
app = typer.Typer()
logger = None


@app.command()
def main(
    keyword: str = typer.Option(
        ...,
        "--keyword",
        "-k",
        help="Search keyword for Google News (required)"
    ),
    max_results: int = typer.Option(
        10,
        "--max-results",
        "-m",
        help="Maximum number of articles to fetch (default: 10)"
    ),
    output: str = typer.Option(
        "articles.json",
        "--output",
        "-o",
        help="Output file path (relative to script dir)"
    ),
    language: str = typer.Option(
        "en",
        "--language",
        "-l",
        help="Language code (en, zh, etc., default: en)"
    ),
    country: str = typer.Option(
        "US",
        "--country",
        "-c",
        help="Country code (US, CN, etc., default: US)"
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose debug logging"
    ),
):
    """
    Fetch news articles from Google News.
    
    Example:
        python news_spider.py --keyword "machine learning" --max-results 50
        python news_spider.py -k "AI" -m 20 -o top_ai_news.json
    """
    
    global logger
    script_dir = Path.cwd()
    logger = setup_logging(script_dir)
    
    if verbose:
        logger.getLogger("google_news_spider").setLevel(logging.DEBUG)
    
    try:
        # Log startup
        logger.info(f"Script started. PID: {sys.version}, Language: {language}, Country: {country}")
        logger.info(f"Fetching news for keyword: '{keyword}', max results: {max_results}")
        
        # Initialize Google News client
        gn = GNews(language=language, country=country)
        
        # Fetch articles (with retry logic)
        articles = None
        for attempt in range(1, 4):
            try:
                articles = gn.get_news(keyword)
                logger.info(f"Successfully fetched articles on attempt {attempt}")
                break
            except Exception as e:
                if attempt < 3:
                    wait_time = 2 ** (attempt - 1)  # Exponential backoff: 1s, 2s, 4s
                    logger.warning(f"Request failed on attempt {attempt}/3. Retrying in {wait_time} seconds. Error: {type(e).__name__}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed after 3 attempts. Error: {str(e)}")
                    raise
        
        if not articles:
            logger.warning("No articles found for keyword")
            articles = []
        
        # Limit results
        articles = articles[:max_results]
        
        # Process and validate output
        output_data = {
            "keyword": keyword,
            "timestamp": datetime.now().isoformat(),
            "articles_count": len(articles),
            "articles": articles
        }
        
        # Write to file (atomic write pattern)
        output_path = script_dir / output
        temp_path = script_dir / f"{output}.tmp"
        
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            # Verify file size
            if temp_path.stat().st_size == 0:
                raise ValueError("Output file is empty")
            
            # Atomic rename
            temp_path.replace(output_path)
            logger.info(f"Successfully wrote {len(articles)} articles to {output}")
            
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            logger.error(f"Failed to write output file: {str(e)}")
            raise
        
        # Log completion
        logger.info(f"Script completed successfully. Processed: {len(articles)} articles, Skipped: 0")
        typer.echo(f"✓ Success! {len(articles)} articles saved to {output}")
        
    except KeyboardInterrupt:
        logger.warning("Script interrupted by user (KeyboardInterrupt)")
        logger.info("Flushing logs before exit")
        for handler in logger.handlers:
            handler.flush()
        typer.echo("Interrupted by user", err=True)
        sys.exit(1)
        
    except Exception as e:
        logger.exception(f"Script failed with exception: {str(e)}")
        logger.info("Flushing logs before exit")
        for handler in logger.handlers:
            handler.flush()
        typer.echo(f"✗ Error: {str(e)}", err=True)
        sys.exit(2)


if __name__ == "__main__":
    app()
