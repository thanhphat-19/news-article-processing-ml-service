from celery import Celery
import logging
from typing import List, Dict, Any, Optional
from src.modules.model_factory import LLMClient
from src.modules.text_processing_services import TextProcessingService
from src.schemas.model import Status
from src.configs.app import settings, app_settings
from src.schemas.ioSchema import summarizeResult, categoryResults,  extract_keywordsResults, processResults

import time

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Celery
app = Celery(
    "text_processing",
    broker=settings.get_celery_broker_url(),
    backend=settings.get_celery_result_backend()
)

# Celery configuration
app.conf.task_track_started = True
app.conf.task_routes = {
    "app.worker.summarize": {"queue": "summarize"},
    "app.worker.categorize": {"queue": "category"},
    "app.worker.extract_keywords": {"queue": "extract_keywords"},
    "app.worker.process": {"queue": "process"},
    "app.worker.test": {"queue": "test"},
}

# Function to get a shared LLMClient instance to avoid re-initialization
def get_llm_client():
    provider = app_settings.LLM_PROVIDER
    logger.info(f"Creating LLMClient with provider: {provider}")
    return LLMClient()  # No need to pass provider, it's read from app_settings

# Simple test task to verify Celery is working
@app.task(name="app.worker.test", bind=True)
def test_task(self, message: str = "Hello, Celery!") -> Dict[str, Any]:
    """
    Simple test task to verify Celery is working
    
    Args:
        message (str): Test message
        
    Returns:
        Dict: Result with timestamp
    """
    import socket
    
    hostname = socket.gethostname()
    logger.info("Test task running on host: " + hostname)
    logger.info("Test message: " + message)
    
    # Simulate some work
    time.sleep(2)
    
    return {
        "message": message,
        "hostname": hostname,
        "timestamp": time.time(),
        "status": {
            "Status ": True,
            "Status Message": "Test task completed successfully"
        }
    }

# Task definitions
@app.task(name="app.worker.summarize")
def summarize(text: str) -> summarizeResult:
    """
    Celery task to generate a summary of the article.
    
    Args:
        text (str): The article text to summarize
        
    Returns:
        str: str of the result
    """
    try:
        logger.info("Starting summarize task")
        logger.info(f"Input text length: {len(text)}")

        llm_client = get_llm_client()
        logger.info(f"LLM Provider: {llm_client.provider}, Model: {llm_client.model_name}")
        
        service = TextProcessingService(llm_client)
        result = service.summarize(text)
        
      
        logger.info(f"Summary generated successfully. Length: {len(result.summary)}")
        return {
            "summary": result.summary,
            "status": {
                "Status": Status.SUCCESS,
                "Status Message": "Successfully generated summary"
            }
        }
    except Exception as e:
        logger.error(f"Error in summarize task: {str(e)}")
        return {
            "summary": "",
            "status": {
                "Status ": Status.ERROR,
                "Status Message": f"Error: {str(e)}"
            }
        }

@app.task(name="app.worker.categorize")
def categorize(text: str) -> categoryResults:
    """
    Celery task to categorize the article.
    
    Args:
        text (str): The article text to categorize
        
    Returns:
        Dict: Dictionary representation of the result
    """
    try:
        logger.info("Starting categorize task")
        
        llm_client = get_llm_client()
        service = TextProcessingService(llm_client)
        result = service.categorize(text)
        
    
        logger.info(f"Category generated: {result.category}")
        return {
            "category": result.category,
            "status": {
                "Status ": Status.SUCCESS,
                "Status Message": "Successfully categorized text"
            }
        }
    except Exception as e:
        logger.error(f"Error in categorize task: {str(e)}")
        
        return {
            "category": "",
            "status": {
                "Status": Status.ERROR,
                "Status Message": f"Error: {str(e)}"
            }
        }

@app.task(name="app.worker.extract_keywords")
def extract_keywords(text: str) -> extract_keywordsResults:
    """
    Celery task to extract keywords from the article.
    
    Args:
        text (str): The article text to extract keywords from
        
        
    Returns:
        Dict: Dictionary representation of the result
    """
    try:
        logger.info("Starting extract_keywords task")
        
        llm_client = get_llm_client()
        service = TextProcessingService(llm_client)
        result = service.extract_keywords(text,)
        logger.info(f"Keywords extracted: {result.keywords}")
        return {
            "keywords": result.keywords,
            "status": {
                "Status": Status.SUCCESS,
                "Status Message": "Successfully extracted keywords"
            }
        }
    except Exception as e:
        logger.error(f"Error in extract_keywords task: {str(e)}")
        return {
            "keywords": [],
            "status": {
                "Status ": Status.ERROR,
                "Status Message": f"Error: {str(e)}"
            }
        }

@app.task(name="app.worker.process")
def process(text: str) -> processResults:
    """
    Celery task to process the article comprehensively.
    
    Args:
        text (str): The article text to process
    Returns:
        Dict: Dictionary representation of the result
    """
    try:
        logger.info("Starting process task")
        
        llm_client = get_llm_client()
        service = TextProcessingService(llm_client)
        result = service.process(text)
        
        # Validate the result
        if result.status == Status.SUCCESS:
            # Make sure we have actual content
            if not result.summary or not result.category or not result.keywords:
                logger.warning("Process completed but with incomplete data")
                return {
                    "summary": result.summary,
                    "category": result.category,
                    "keywords": result.keywords,
                    "status": {
                        "Status ": Status.ERROR,
                        "Status Message": f"Error: {str(e)}"
                    }
                }
            
            logger.info(f"Process completed successfully - Summary length: {len(result.summary)}, " +
                       f"Category: {result.category}, Keywords count: {len(result.keywords)}")
            
            return {
                "summary": result.summary,
                "category": result.category,
                "keywords": result.keywords,
                "status": {
                    "Status": Status.SUCCESS,
                    "Status Message": "Successfully processed text"
                }
            }
    except Exception as e:
        logger.error(f"Error in process task: {str(e)}")
        return {
            "summary": "",
            "category": "",
            "keywords": [],
            "status": {
                "Status ": Status.ERROR,
                "Status Message": f"Error: {str(e)}"
            }
        }

if __name__ == "__main__":
    app.start()
