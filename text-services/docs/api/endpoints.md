# API Endpoints

This document provides detailed information about all endpoints available in the Text Processing API.

## Base URL

All endpoints are relative to the API base URL:

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## Response Format

All API responses are in JSON format with appropriate HTTP status codes.

## Status Endpoints

### Root Endpoint

Check if the API is running.

```http
GET /
```

#### Response (200 OK)

```json
{
  "message": "Text Processing API is running. Visit /docs for API documentation."
}
```

### Health Check

Get the current health status of the API.

```http
GET /health
```

#### Response (200 OK)

```json
{
  "status": "healthy",
  "service": "text-processing-api",
  "version": "1.0.0"
}
```

### Test Connectivity

Test the API and Celery worker connectivity.

```http
POST /test
```

#### Request Body

```json
{
  "message": "Hello from API!"  // Optional, default provided
}
```

#### Response 

```json
{
  "task_id": "task-uuid-here",
  "message": "Test task submitted successfully",
  "status": "PENDING"
}
```

#### Example

```bash
curl -X POST "http://localhost:8000/test" \
  -H "Content-Type: application/json" \
  -d '{"message": "Testing the API connection"}'
```

## Processing Endpoints

### Text Summarization

Creates a task to summarize the provided text.

```http
POST /summarize
```

#### Request Body

```json
{
  "text": "Your long text to be summarized goes here."
}
```

#### Response 

```json
{
  "task_id": "task-uuid-here"
}
```

#### Example

```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Climate change is the long-term alteration of temperature and typical weather patterns in a place. Climate change could refer to a particular location or the planet as a whole. Climate change may cause weather patterns to be less predictable. These unexpected weather patterns can make it difficult to maintain and grow crops in regions that rely on farming because expected temperature and rainfall levels can no longer be relied on."
  }'
```

### Text Categorization

Creates a task to categorize the provided text.

```http
POST /categorize
```

#### Request Body

```json
{
  "text": "Text to categorize goes here."
}
```

#### Response 

```json
{
  "task_id": "task-uuid-here"
}
```

#### Example

```bash
curl -X POST "http://localhost:8000/categorize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple Inc. reported strong quarterly earnings, exceeding analysts' expectations. The technology giant saw increased sales in their iPhone and services divisions, while Mac sales remained stable."
  }'
```

### Keyword Extraction

Creates a task to extract keywords from the provided text.

```http
POST /extract-keywords
```

#### Request Body

```json
{
  "text": "Text from which to extract keywords goes here."
}
```

#### Response 

```json
{
  "task_id": "task-uuid-here"
}
```

#### Example

```bash
curl -X POST "http://localhost:8000/extract-keywords" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Machine learning is a field of inquiry devoted to understanding and building methods that 'learn', that is, methods that leverage data to improve performance on some set of tasks. It is seen as a part of artificial intelligence."
  }'
```

### Comprehensive Text Processing

Creates a task to comprehensively process the provided text (includes summarization, categorization, and keyword extraction).

```http
POST /process
```

#### Request Body

```json
{
  "text": "Text to process comprehensively goes here."
}
```

#### Response 

```json
{
  "task_id": "task-uuid-here"
}
```

#### Example

```bash
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Quantum computing is an area of computing focused on developing computer technology based on the principles of quantum theory. Quantum computers perform calculations based on the probability of an object's state before it is measured, instead of just 1s or 0s, which means they have the potential to process exponentially more data compared to classical computers."
  }'
```

## Task Management Endpoints

### Retrieve Task Results

Retrieves the result of a previously submitted task.

```http
GET /tasks/{task_id}
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | string | Yes | The ID of the task to retrieve results for |

#### Response States

##### For a Completed Task (200 OK)

```json
{
  "summary": "Artificial intelligence is revolutionizing industries by automating tasks, analyzing data, and generating unprecedented insights. Advances in machine learning, especially deep learning, are fueling this rapid transformation. Companies are heavily investing in AI research and development to secure a competitive advantage.",
  "status": {
    "Status": "SUCCESS",
    "Status Message": "Successfully generated summary"
  }
}
```

##### For a Failed Task (200 OK)

```json
{
  "status": "FAILURE",
  "error": "Error message here"
}
```

##### For a Pending Task (200 OK)

```json
{
  "status": "PENDING"
}
```

#### Example

```bash
curl -X GET "http://localhost:8000/tasks/3fa85f64-5717-4562-b3fc-2c963f66afa6"
```

## Response Examples by Processing Type

Below are examples of typical successful responses for each processing type.

### Summarization Response

```json
{
  "summary": "Artificial intelligence is revolutionizing industries by automating tasks, analyzing data, and generating unprecedented insights. Advances in machine learning, especially deep learning, are fueling this rapid transformation. Companies are heavily investing in AI research and development to secure a competitive advantage.",
  "status": {
    "Status": "SUCCESS",
    "Status Message": "Successfully generated summary"
  }
}
```

### Categorization Response

```json
{
  "result": {
    "category": "Technology",
    "status": {
      "Status": "SUCCESS",
      "Status Message": "Successfully categorized text"
    }
  }
}
```

### Keywords Response

```json
{
  "result": {
    "keywords": [
      "Artificial Intelligence",
      "AI transformation",
      "machine learning",
      "deep learning",
      "AI research and development",
      "healthcare",
      "finance"
    ],
    "status": {
      "Status": "SUCCESS",
      "Status Message": "Successfully extracted keywords"
    }
  }
}
```

### Comprehensive Process Response

```json
{
  "result": {
    "summary": "Artificial Intelligence is revolutionizing industries globally by automating tasks and providing unprecedented data analysis. Advances in machine learning, especially deep learning, are driving this rapid transformation. Businesses are heavily investing in AI research and development to secure a competitive advantage.",
    "category": "Technology",
    "keywords": [
      "Artificial Intelligence",
      "AI transformation",
      "Machine Learning",
      "Deep Learning",
      "Healthcare",
      "Finance",
      "Automation",
      "Data Analysis",
      "Competitive Edge"
    ],
    "status": {
      "Status": "SUCCESS",
      "Status Message": "Successfully processed text"
    }
  }
}
```



## Rate Limiting

The API currently does not implement rate limiting, but excessive requests might affect performance. Implementation of rate limiting is planned for future releases.
