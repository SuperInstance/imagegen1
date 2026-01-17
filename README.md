# Local Generation Server

A local generation server that automatically detects hardware and downloads compatible models for text, image, and audio generation.

## Features

- Automatic hardware detection (GPU, CPU, RAM, Storage)
- Model compatibility checking
- Image generation with Stable Diffusion
- Text generation with Ollama integration
- Audio generation with TTS
- MCP server for easy app integration
- Configurable model selection

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Start the server
python main.py

# Download compatible models
python main.py --download-models

# Use custom config
python main.py --config custom.yaml
```

## MCP Integration

The server exposes MCP endpoints for:
- Image generation
- Text generation
- Audio generation

See `docs/usage.md` for details.