from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from celery.result import AsyncResult

import uvicorn
from src.app.worker.task import summarize, categorize, extract_keywords, process, test_task
import logging
from src.schemas.task import (
    TextRequest,
    TaskResponse,
    TaskResult
)
from src.configs.app import settings

# Configure logging
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text Processing API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)



# Routes
@app.get("/")
async def root():
    return {"message": "Text Processing API is running. Visit /docs for API documentation."}

@app.post("/test", response_model=Dict[str, Any])
async def run_test(message: Optional[str] = "Hello from API!"):
    """Test the API and Celery worker connectivity"""
    task = test_task.delay(message)
    return {
        "task_id": task.id,
        "message": "Test task submitted successfully",
        "status": "PENDING"
    }

@app.post("/summarize", response_model=TaskResponse)
async def create_summary_task(request: TextRequest):
    """
    Create a task to summarize text with optional structured output
    
    - **text**: The text to summarize
    """
    try:
        task = summarize.apply_async(kwargs={
            "text": request.text,
        })
        return TaskResponse(task_id=task.id)
    except Exception as e:
        logger.error(f"Error creating summary task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/categorize", response_model=TaskResponse)
async def create_category_task(request: TextRequest):
    """
    Create a task to categorize text with optional structured output
    
    - **text**: The text to categorize
    """
    try:
        task = categorize.apply_async(kwargs={
            "text": request.text,
        })
        return TaskResponse(task_id=task.id)
    except Exception as e:
        logger.error(f"Error creating category task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract-keywords", response_model=TaskResponse)
async def create_keywords_task(request: TextRequest):
    """
    Create a task to extract keywords with optional structured output
    
    - **text**: The text to extract keywords from
    """
    try:
        task = extract_keywords.apply_async(kwargs={
            "text": request.text,
        })
        return TaskResponse(task_id=task.id)
    except Exception as e:
        logger.error(f"Error creating keywords task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process", response_model=TaskResponse)
async def create_process_task(request: TextRequest):
    """
    Create a task to process text comprehensively with optional structured output
    
    - **text**: The text to process
    """
    try:
        task = process.apply_async(kwargs={
            "text": request.text,
        })
        return TaskResponse(task_id=task.id)
    except Exception as e:
        logger.error(f"Error creating process task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{task_id}", response_model=TaskResult)
async def get_task_result(task_id: str):
    """
    Get the result of a task by its ID
    
    - Returns structured or standard output based on the original request
    - Includes task status and error information if applicable
    """
    try:
        task_result = AsyncResult(task_id)
        
        if task_result.ready():
            if task_result.successful():
                result = task_result.get()
                return TaskResult(
                    status="SUCCESS",
                    result=result
                )
            else:
                error = str(task_result.get(propagate=False))
                return TaskResult(
                    status="FAILURE",
                    error=error
                )
        else:
            return TaskResult(status="PENDING")
            
    except Exception as e:
        logger.error(f"Error getting task result: {e}")
        return TaskResult(
            status="ERROR",
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "text-processing-api",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
