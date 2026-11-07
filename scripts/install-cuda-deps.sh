#!/bin/bash

# Install CUDA-specific PyTorch and related packages
echo "Installing CUDA-enabled PyTorch..."

# Install PyTorch with CUDA support
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other ML packages
uv pip install diffusers transformers accelerate safetensors
uv pip install Pillow opencv-python
uv pip install librosa soundfile pydub
uv pip install huggingface-hub requests tqdm psutil

echo "ML dependencies installed successfully!"