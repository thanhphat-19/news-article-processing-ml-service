# LLM Models
The Text Processing API supports multiple Large Language Model (LLM) providers to power its text processing capabilities. This page outlines the supported providers and how to configure them.

## Supported Providers
The system currently supports the following LLM providers:

| Provider | Description | Configuration Key |
|----------|-------------|------------------|
| Anthropic | Claude models known for their context understanding and safety features | `anthropic` |
| OpenAI | GPT models offering powerful text generation capabilities | `openai` |
| Google Gemini | Google's multimodal AI models | `gemini` |
| Ollama | Self-hosted open-source models | `ollama` |

## Current Implementation
**Our system currently uses Google's Gemini 2.0 Flash model**, which offers an excellent balance of performance and efficiency. We've specifically designed our prompting strategy to optimize for this model's capabilities. For details on our prompting approach, see the [Prompting Strategy Documentation](promting-strategy.md).

## Configuration
You can configure which LLM provider to use via environment variables. Set the `LLM_PROVIDER` environment variable to one of the supported provider keys.

```bash
# Example: Using Anthropic Claude
LLM_PROVIDER=anthropic
```

### Provider-Specific Configuration
Each provider requires specific configuration:

#### Anthropic
```bash
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-5-sonnet
```

Available models:

- `claude-3-5-sonnet` - Latest model balancing performance and efficiency
- `claude-3-opus` - Most powerful Claude model for complex tasks
- `claude-3-sonnet` - Strong performance with faster response times
- `claude-3-haiku` - Fastest Claude model for quick responses

#### OpenAI
```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo
```

Available models:

- `gpt-4-turbo` - Latest GPT-4 model with good performance/cost balance
- `gpt-4` - Base GPT-4 model
- `gpt-3.5-turbo` - Faster and more cost-effective GPT model

#### Google Gemini
```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

Available models:

- `gemini-2.0-flash` - Latest Gemini model optimized for speed and efficiency (currently used)
- `gemini-pro-vision` - Multimodal Gemini model (if supported in the application)

#### Ollama (Self-hosted)
```bash
OLLAMA_HOST=http://host.docker.internal:11434
OLLAMA_MODEL=llama3
```

Available models depend on what you've pulled to your Ollama instance. Examples include:

- `llama3` - Meta's Llama 3 model
- `mistral` - Mistral model
- `mixtral` - MoE-based Mixtral model
- `phi` - Microsoft's Phi models
- And many more open-source models

## Timeout Configuration
All providers support a timeout configuration to prevent long-running requests:

```bash
LLM_REQUEST_TIMEOUT=60  # Timeout in seconds
```

## Prompting Strategy
Our text processing service uses a hybrid guided thinking approach specifically optimized for the Gemini 2.0 Flash model. This approach balances thorough analysis with efficient processing, focusing on:

- Implicit reasoning guidance without requiring verbose step documentation
- Clear output formatting instructions for consistent results
- Task-appropriate depth of analysis

For complete details on our prompting approach and implementation, refer to our [Prompting Strategy Documentation](prompting_strategy.md).

## Adding New Providers
To add support for additional LLM providers:
1. Update the `LLMClient` class in `text-services/src/modules/model_factory.py`

## Best Practices
1. **API Keys**: Never commit API keys to your code repository. Use environment variables or secrets management.
2. **Model Selection**: Choose models appropriate for your task. More powerful models often incur higher costs.
3. **Timeout Handling**: Implement proper error handling for timeout cases, especially for longer inputs.
4. **Fallback Mechanisms**: Consider configuring fallback models if your primary model is unavailable.
5. **Prompt Optimization**: Different models respond differently to prompting strategies. Consider model-specific prompt engineering for best results.
