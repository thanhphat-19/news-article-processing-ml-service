from typing import Dict, Any
import json

# Revised prompts using a hybrid approach - guided thinking with clear output focus
SUMMARIZE_PROMPT = (
    "Create a concise summary of the following news article in EXACTLY 3 sentences. "
    "Focus on the main points, key facts, and central message. "
    "Think step-by-step before writing your summary: identify the main topic, key information, and most important conclusions. "
    "Ensure your final summary is clear, informative, and captures the essence of the article.\n\n"
    "Article: {text}\n\n"
    "3-Sentence Summary:"
)

CATEGORIZE_PROMPT = (
    "Analyze the following news article and categorize it into EXACTLY ONE of these categories: "
    "Technology, Sports, Health, Politics, Finance, Business.\n\n"
    "Before deciding, consider: the primary subject matter, key entities discussed, main events or concepts, "
    "and which category best represents the overall focus of the article.\n\n"
    "Choose the single most appropriate category that best represents the primary focus of the article. "
    "Return only the category name without additional explanation or commentary.\n\n"
    "Article: {text}\n\n"
    "Category:"
)

EXTRACT_KEYWORDS_PROMPT = (
    "Extract 5-10 relevant keywords or key phrases from the following news article. "
    "Focus on terms that best represent the main topics, entities, and themes of the content. "
    "To identify the most effective keywords: consider the central topic, recurring terminology, "
    "important entities (people, organizations, locations), and technical terms specific to the subject matter.\n\n"
    "Format requirements:\n"
    "- Return ONLY the keywords themselves\n"
    "- Each keyword should be separated by a comma (,)\n"
    "- Do NOT use bullet points, asterisks, or markdown formatting\n"
    "- Do NOT number the keywords\n"
    "- Do NOT add explanations or descriptions\n\n"
    "Article: {text}\n\n"
    "Keywords:"
)

# PROCESS_PROMPT = (
#     "Perform a comprehensive analysis of the following news article to extract structured information.\n\n"
    
#     "Analyze the article carefully to:\n"
#     "1. Summarize the main content in EXACTLY 3 sentences, focusing on the key information and central message.\n"
#     "2. Categorize the article into EXACTLY ONE category from: Technology, Sports, Health, Politics, Finance, Business.\n"
#     "3. Extract 5-10 relevant keywords that best represent the distinctive content and themes.\n\n"
    
#     "Before responding, think about the article's primary subject, key entities, important events, core message, and distinctive terminology.\n\n"
    
#     "Article: {text}\n\n"
    
#     "Provide your analysis as JSON with these fields: 'summary', 'category', and 'keywords'.\n\n"
    
#     "Expected output format:\n"
#     "```json\n"
#     "{\n"
#     "  \"summary\": \"First sentence of summary. Second sentence of summary. Third sentence of summary.\",\n"
#     "  \"category\": \"SelectedCategory\",\n"
#     "  \"keywords\": \"keyword1, keyword2, keyword3, keyword4, keyword5\"\n"
#     "}\n"
#     "```"
# )

SYSTEM_PROMPT = (
    "You are a precise and analytical text processing assistant. "
    "When working with texts, carefully consider all relevant aspects before providing your response. "
    "Your primary goal is to produce accurate, high-quality outputs that exactly match the requested format. "
    "Always follow the specified output requirements precisely. "
    "Focus on understanding the content thoroughly to extract the most relevant information. "
    "Do not speculate or add information not present in the original text."
)


class PromptsBank:
    def __init__(self):
        """
        Collection of prompts for different text processing tasks
        """
        self.summarize_prompt = SUMMARIZE_PROMPT
        self.category_prompt = CATEGORIZE_PROMPT
        self.extract_keywords_prompt = EXTRACT_KEYWORDS_PROMPT
        # self.process_prompt = PROCESS_PROMPT
        self.system_prompt = SYSTEM_PROMPT
