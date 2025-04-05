# Wellcome to Text Processing services

# Text Processing API

Welcome to the official documentation for the Text Processing API. This service provides powerful natural language processing capabilities through a simple and intuitive RESTful interface.

## Features

- **Text Summarization**: Generate concise summaries of long text
- **Text Categorization**: Classify content into meaningful categories
- **Keyword Extraction**: Identify the most important terms in your text
- **Comprehensive Processing**: Complete analysis combining all features



## Quick Example

```python
import requests
import time

# Submit text for processing
response = requests.post(
    "http://your-api-host:8000/summarize",
    json={"text": "Your long text goes here..."}
)
task_id = response.json()["task_id"]

# Retrieve results
while True:
    result = requests.get(f"http://your-api-host:8000/tasks/{task_id}").json()
    if result["status"] != "PENDING":
        break
    time.sleep(1)

print(result["result"])
```


## Getting Started

New to the Text Processing API? Our **[Getting Started](getting-started.md)** guide provides a comprehensive introduction to get you up and running quickly with examples and best practices.

## API Reference

The **API Reference** section provides detailed documentation of all available endpoints and their functionality. Here you'll find:

- **[Overview](api/overview.md)**: Learn about the API's capabilities, architecture, and basic usage patterns
- **[Endpoints](api/endpoints.md)**: Comprehensive documentation of each endpoint, including request formats, response structures, and examples

## LLM Models

The **[LLM Models](llm-models.md)** page explains the various language models supported by the Text Processing API, including configuration options and capabilities for each provider.

## Prompting Strategy

The **[Prompting Strategy](promting-strategy.md)** guide offers techniques and best practices for crafting effective prompts to get optimal results from the underlying language models.
