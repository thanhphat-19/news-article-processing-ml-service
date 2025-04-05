import logging
import requests
from typing import Optional
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from src.configs.app import app_settings
from langchain_core.messages.base import BaseMessage

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, system_prompt: Optional[str] = None):
        self.provider = app_settings.LLM_PROVIDER
        self.system_prompt = system_prompt
        self.model_name = self._get_model_name()
        self.llm = self._initialize_llm()
        logger.info(f"Initialized LLM client with provider: {self.provider}, model: {self.model_name}")
        
    def _get_model_name(self) -> str:
        if self.provider == "ollama":
            return app_settings.OLLAMA_MODEL
        elif self.provider == "openai":
            return app_settings.OPENAI_MODEL
        elif self.provider == "anthropic":
            return app_settings.ANTHROPIC_MODEL
        elif self.provider == "gemini":
            return app_settings.GEMINI_MODEL
        else:
            logger.warning(f"Unknown provider: {self.provider}, falling back to Ollama")
            self.provider = "ollama"
            return app_settings.OLLAMA_MODEL
            
    def _initialize_llm(self):
        try:
            if self.provider == "ollama":
                logger.info(f"Initializing Ollama with host: {app_settings.OLLAMA_HOST}")
                return ChatOllama(
                    base_url=app_settings.OLLAMA_HOST,
                    model=self.model_name,
                    temperature=0,
                    timeout=app_settings.LLM_REQUEST_TIMEOUT,
                )
                
            elif self.provider == "openai":
                logger.info(f"Initializing OpenAI with model: {self.model_name}")
                if not app_settings.OPENAI_API_KEY:
                    raise ValueError("OpenAI API key not provided")
                return ChatOpenAI(
                    api_key=app_settings.OPENAI_API_KEY.get_secret_value(),
                    model=self.model_name,
                    temperature=0.7,
                    request_timeout=app_settings.LLM_REQUEST_TIMEOUT,
                )
                
            elif self.provider == "anthropic":
                logger.info(f"Initializing Anthropic with model: {self.model_name}")
                if not app_settings.ANTHROPIC_API_KEY:
                    raise ValueError("Anthropic API key not provided")
                return ChatAnthropic(
                    api_key=app_settings.ANTHROPIC_API_KEY.get_secret_value(),
                    model_name=self.model_name,
                    temperature=0.7,
                    max_tokens=4096,
                    timeout=app_settings.LLM_REQUEST_TIMEOUT,
                )
                
            elif self.provider == "gemini":
                logger.info(f"Initializing Gemini with model: {self.model_name}")
                if not app_settings.GEMINI_API_KEY:
                    raise ValueError("Gemini API key not provided")
                return ChatGoogleGenerativeAI(
                    api_key=app_settings.GEMINI_API_KEY.get_secret_value(),
                    model=self.model_name,
                    temperature=0.7,
                    convert_system_message_to_human=True,
                    timeout=app_settings.LLM_REQUEST_TIMEOUT,
                )
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
                
        except Exception as e:
            logger.error(f"Error initializing LLM: {str(e)}")
            raise

    def query(self, prompt: str) -> str:
        try:
            logger.info(f"Sending query to {self.provider} model: {self.model_name}")
            messages = []
            
            if self.system_prompt:
                messages.append(SystemMessage(content=self.system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            response = self.llm.invoke(messages)
            
            if isinstance(response, BaseMessage):
                content = str(response.content)
                logger.info(f"Received response: {content[:100]}...")
                return content
                
            raise ValueError(f"Unexpected response type from LLM: {type(response)}")
            
        except Exception as e:
            logger.error(f"Error in LLM query: {str(e)}")
            raise





