import re
import logging
from src.schemas.model import Status
from src.schemas.ioSchema import (
    summarizeResult,
    categoryResults,
    extract_keywordsResults,
    processResults
)
from src.configs._prompts import PromptsBank
from src.modules.model_factory import LLMClient

logger = logging.getLogger(__name__)

class TextProcessingService:
    def __init__(self, llm_client: LLMClient = None):
        self.llm_client = llm_client or LLMClient()
        self.prompts = PromptsBank()
        logger.info(f"TextProcessingService initialized with {self.llm_client.provider} provider")

    def _validate_text(self, text: str) -> str:
        if not text or len(text.strip()) < 10:
            raise ValueError("Text is too short to process")
        return text.strip()

    def summarize(self, text: str) -> summarizeResult:
        try:
            text = self._validate_text(text)
            logger.info("Preparing prompt for summarization")
            
            prompt = self.prompts.summarize_prompt.format(text=text)
            response = self.llm_client.query(prompt)
            
            summary = response.strip()
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', summary) if s.strip()]
            if len(sentences) > 3:
                summary = ' '.join(sentences[:3])
            
            logger.info(f"Generated summary: {summary}")
            return summarizeResult(
                summary=summary,
                status=Status.SUCCESS
            )
        except Exception as e:
            logger.error(f"Error in summarize: {str(e)}")
            return summarizeResult(
                summary="",
                status=Status.ERROR
            )

    def categorize(self, text: str) -> categoryResults:
        try:
            text = self._validate_text(text)
            prompt = self.prompts.category_prompt.format(text=text)
            response = self.llm_client.query(prompt)
            
            category = response.strip()
            return categoryResults(
                category=category,
                status=Status.SUCCESS
            )
        except Exception as e:
            logger.error(f"Error in categorize: {str(e)}")
            return categoryResults(
                category="",
                status=Status.ERROR
            )

    def extract_keywords(self, text: str) -> extract_keywordsResults:
        try:
            text = self._validate_text(text)
            prompt = self.prompts.extract_keywords_prompt.format(text=text)
            response = self.llm_client.query(prompt)
            
            # Clean up the response and split by commas
            response = response.strip()
            
            # Handle potential formatting issues
            # Remove any markdown bullet points, asterisks, or numbers
            response = response.replace('*', '').replace('#', '').replace('-', '')
            
            # Split by commas and clean each keyword
            keywords = [keyword.strip() for keyword in response.split(',') if keyword.strip()]
            
            # Remove any empty strings and limit to 10 keywords
            keywords = [k for k in keywords if k][:10]
            
            if not keywords:
                logger.warning("No keywords extracted from LLM response")
                logger.debug(f"Original response: {response}")
                return extract_keywordsResults(
                    keywords=[],
                    status=Status.ERROR
                )
                
            return extract_keywordsResults(
                keywords=keywords,
                status=Status.SUCCESS
            )
        except Exception as e:
            logger.error(f"Error in extract_keywords: {str(e)}")
            return extract_keywordsResults(
                keywords=[],
                status=Status.ERROR
            )

    def process(self, text: str) -> processResults:
        """
        Process text by calling summarize, categorize, and extract_keywords methods.
        
        Args:
            text (str): The text to process
            
        Returns:
            processResults: A combined result with summary, category, and keywords
        """
        try:
            text = self._validate_text(text)
            
            # Call individual methods instead of trying to do everything in one LLM call
            summary_result = self.summarize(text)
            category_result = self.categorize(text)
            keywords_result = self.extract_keywords(text)
            
            # Check if any of the individual calls failed
            if (summary_result.status == Status.ERROR or 
                category_result.status == Status.ERROR or 
                keywords_result.status == Status.ERROR):
                logger.warning("One or more sub-tasks failed during process")
                
                # Determine overall status (ERROR if any critical component failed)
                if summary_result.status == Status.ERROR:
                    raise ValueError("Failed to generate summary")
            
            # Combine results from all three methods
            return processResults(
                summary=summary_result.summary,
                category=category_result.category,
                keywords=keywords_result.keywords[:10],
                status=Status.SUCCESS
            )
        except Exception as e:
            logger.error(f"Error in process: {str(e)}")
            return processResults(
                summary="",
                category="",
                keywords=[],
                status=Status.ERROR
        )
