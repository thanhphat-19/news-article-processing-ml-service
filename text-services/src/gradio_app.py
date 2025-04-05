import gradio as gr
import requests
import json
import time
from typing import Dict, Any, Tuple, List
from src.app.worker.task import summarize, categorize, extract_keywords, process
from src.schemas.task import TextRequest, TaskResponse, TaskResult
from src.configs.app import settings

# Update API URL to use Docker service name
API_BASE_URL = "http://text_service:8000"  # Changed from localhost to service name

def check_task_status(task_id: str, max_wait: int = 60) -> Dict[str, Any]:
    """Check the status of a task and wait for completion if necessary"""
    status_url = f"{API_BASE_URL}/tasks/{task_id}"
    
    # Poll for result with timeout
    start_time = time.time()
    while True:
        try:
            response = requests.get(status_url)
            if response.status_code == 200:
                result = response.json()
                
                # If task is complete, return the result
                if result["status"] in ["SUCCESS", "FAILURE"]:
                    return result
        except requests.exceptions.RequestException as e:
            print(f"Error checking task status: {e}")
            time.sleep(1)
                
        # Check timeout
        if time.time() - start_time > max_wait:
            return {"status": "TIMEOUT", "result": "Task processing timed out"}
            
        # Wait before polling again
        time.sleep(1)

def submit_test_task(message: str = "Hello from Gradio!") -> str:
    """Submit a test task to verify service functionality"""
    try:
        response = requests.post(f"{API_BASE_URL}/test", params={"message": message})
        if response.status_code == 200:
            task_data = response.json()
            result = check_task_status(task_data["task_id"])
            return json.dumps(result, indent=2)
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def submit_task(endpoint: str, text: str) -> str:
    """Submit a text processing task and wait for the result"""
    if not text or len(text.strip()) < 10:
        return "Error: Text is too short (minimum 10 characters)"
    
    try:
        # Submit task
        response = requests.post(
            f"{API_BASE_URL}/{endpoint}",
            json={"text": text}
        )
        
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
            
        task_data = response.json()
        task_id = task_data["task_id"]
        
        # Show initial status
        status_message = f"Task submitted (ID: {task_id}). Processing..."
        
        # Wait for result
        result = check_task_status(task_id)
        
        # Format the result nicely
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return f"Error: {str(e)}"

def submit_summarize(text: str) -> str:
    """Submit a summarization task"""
    return submit_task("summarize", text)

def submit_categorize(text: str) -> str:
    """Submit a categorization task"""
    return submit_task("categorize", text)

def submit_extract_keywords(text: str) -> str:
    """Submit a keyword extraction task"""
    return submit_task("extract-keywords", text)

def submit_process(text: str) -> str:
    """Submit a complete text processing task"""
    return submit_task("process", text)

def create_ui():
    """Create the Gradio UI"""
    # Define sample text
    sample_text = """
    Artificial Intelligence is transforming industries around the world. 
    From healthcare to finance, AI systems are being deployed to automate tasks, 
    analyze data, and provide insights that were previously impossible. 
    Recent advances in machine learning, particularly deep learning, have accelerated this transformation. 
    Companies are investing billions in AI research and development, 
    hoping to gain a competitive edge in their respective markets.
    """
    
    # Create Gradio interface
    with gr.Blocks(title="Text Processing Service") as demo:
        gr.Markdown("# Text Processing Service Demo")
        gr.Markdown("This demo allows you to test various text processing features using LLMs.")
        
        with gr.Tab("Test Connection"):
            test_input = gr.Textbox(label="Test Message", value="Hello from Gradio!")
            test_button = gr.Button("Run Test")
            test_output = gr.Textbox(label="Test Result", lines=10)
            test_button.click(submit_test_task, inputs=test_input, outputs=test_output)
        
        with gr.Tab("Text Processing"):
            text_input = gr.Textbox(label="Input Text", lines=10, value=sample_text)
            
            with gr.Row():
                summarize_button = gr.Button("Summarize")
                categorize_button = gr.Button("Categorize")
                keywords_button = gr.Button("Extract Keywords")
                process_button = gr.Button("Process All")
            
            result_output = gr.Textbox(label="Result", lines=15)
            
            summarize_button.click(submit_summarize, inputs=text_input, outputs=result_output)
            categorize_button.click(submit_categorize, inputs=text_input, outputs=result_output)
            keywords_button.click(submit_extract_keywords, inputs=text_input, outputs=result_output)
            process_button.click(submit_process, inputs=text_input, outputs=result_output)
            
    return demo

if __name__ == "__main__":
    # Create and launch the UI
    demo = create_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860) 
