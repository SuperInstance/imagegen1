# Usage Documentation

## Table of Contents
- [Basic Usage](#basic-usage)
- [MCP Integration](#mcp-integration)
- [Configuration](#configuration)
- [Model Management](#model-management)
- [Examples](#examples)

## Basic Usage

### Starting the Server

```bash
# Start with default configuration
python main.py

# Start with custom configuration
python main.py --config custom.yaml

# Start and automatically download compatible models
python main.py --download-models
```

### Hardware Detection

The server automatically detects:
- **GPU**: CUDA availability, VRAM size
- **CPU**: Cores, architecture
- **RAM**: Total available memory
- **Storage**: Available disk space

This information is used to select the optimal models for your system.

### Command Line Options

```bash
usage: main.py [-h] [--config CONFIG] [--download-models] [--host HOST] [--port PORT]

Local Generation Server with automatic hardware detection and model management

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to configuration file (default: config.yaml)
  --download-models    Automatically download compatible models
  --host HOST          Server host (default: 0.0.0.0)
  --port PORT          Server port (default: 8000)
```

## MCP Integration

The server exposes Model Context Protocol (MCP) endpoints for easy integration with applications.

### Image Generation

Generate images using Stable Diffusion models.

**Parameters:**
- `prompt` (string): Text description of the image
- `model` (string, optional): Specific model to use
- `width` (int, optional): Image width (default: 512)
- `height` (int, optional): Image height (default: 512)
- `steps` (int, optional): Generation steps (default: 20)
- `guidance_scale` (float, optional): Guidance scale (default: 7.5)

**Example:**
```python
# Using MCP client
response = mcp_client.call("image_generation", {
    "prompt": "A beautiful landscape with mountains and lakes",
    "width": 768,
    "height": 512,
    "steps": 25
})
```

### Text Generation

Generate text using Ollama-integrated models.

**Parameters:**
- `prompt` (string): Text prompt
- `model` (string, optional): Specific model (default: auto-detected)
- `max_tokens` (int, optional): Maximum tokens (default: 1000)
- `temperature` (float, optional): Temperature (default: 0.7)

**Example:**
```python
response = mcp_client.call("text_generation", {
    "prompt": "Write a short story about a robot learning to paint",
    "max_tokens": 500,
    "temperature": 0.8
})
```

### Audio Generation

Generate audio using Text-to-Speech (TTS).

**Parameters:**
- `text` (string): Text to convert to speech
- `voice` (string, optional): Voice selection
- `speed` (float, optional): Speech speed (default: 1.0)
- `pitch` (float, optional): Speech pitch (default: 1.0)

**Example:**
```python
response = mcp_client.call("audio_generation", {
    "text": "Hello, this is a text-to-speech example.",
    "voice": "default",
    "speed": 1.2
})
```

## Configuration

### Configuration File Structure

```yaml
# config.yaml
server:
  host: "0.0.0.0"
  port: 8000

models:
  image:
    default: "stable-diffusion-xl-base-1.0"
    auto_download: true
  text:
    default: "llama2"
    auto_download: true
  audio:
    default: "tts-1"
    auto_download: true

hardware:
  gpu_check: true
  min_vram: 4  # GB
  prefer_gpu: true

logging:
  level: "INFO"
  file: "server.log"
```

### Environment Variables

You can also configure the server using environment variables:

```bash
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8000
export MODEL_DOWNLOAD_AUTO=true
export LOG_LEVEL=DEBUG
```

## Model Management

### Automatic Model Selection

The server automatically selects the best model based on:
- Available hardware (GPU/CPU)
- Model compatibility
- Performance requirements
- Storage space

### Manual Model Download

```bash
# Download specific models
python main.py --download-models --models image,text,audio

# Download only image models
python main.py --download-models --models image

# Force re-download existing models
python main.py --download-models --force
```

### Model Storage

Models are stored in the `models/` directory:
- `models/image/` - Stable Diffusion models
- `models/text/` - Text generation models
- `models/audio/` - TTS models

## Examples

### Simple Python Client

See `examples/simple_client.py` for a complete example of using the MCP server.

### Command Line Testing

You can test the server endpoints using curl:

```bash
# Test image generation
curl -X POST "http://localhost:8000/generate/image" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A cute cat", "width": 512, "height": 512}'

# Test text generation
curl -X POST "http://localhost:8000/generate/text" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms"}'

# Test audio generation
curl -X POST "http://localhost:8000/generate/audio" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test message."}'
```

### Web Interface Integration

The server can be integrated with web applications using the REST API:

```javascript
// JavaScript example
async function generateImage(prompt) {
  const response = await fetch('/generate/image', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt: prompt,
      width: 768,
      height: 512
    })
  });

  const data = await response.json();
  return data.image_url;
}
```

## Troubleshooting

### Common Issues

1. **Model Download Fails**
   - Check internet connection
   - Verify sufficient disk space
   - Check model URLs in configuration

2. **GPU Not Detected**
   - Ensure CUDA drivers are installed
   - Check GPU compatibility
   - Verify Python CUDA packages

3. **Memory Issues**
   - Reduce batch size in configuration
   - Use CPU fallback mode
   - Increase available RAM or swap space

### Logs

Check the log files for detailed information:
- Server logs: `server.log`
- Model download logs: `models/download.log`
- Error logs: `error.log`

### Support

For additional support:
- Check the GitHub issues
- Review the troubleshooting section
- Submit a new issue with system information and error logs