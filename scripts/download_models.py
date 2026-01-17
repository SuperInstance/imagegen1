#!/usr/bin/env python3
"""
Script for downloading compatible models for the generation server.
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.hardware.detector import HardwareDetector
from src.models.manager import ModelManager

def download_models():
    """Download compatible models based on hardware specifications."""
    print("Initializing hardware detector...")
    hardware_detector = HardwareDetector()

    print("Detecting hardware specifications...")
    hardware_specs = hardware_detector.detect_specs()
    print(f"Hardware specs: {hardware_specs}")

    print("Initializing model manager...")
    model_manager = ModelManager(hardware_detector)

    print("Finding compatible models...")
    compatible_models = model_manager.get_compatible_models()

    if not compatible_models:
        print("No compatible models found.")
        return

    print(f"\nFound {len(compatible_models)} compatible models:")
    for i, model in enumerate(compatible_models, 1):
        print(f"{i}. {model['name']} - {model['description']}")
        print(f"   Size: {model.get('size_mb', 'Unknown')} MB")
        print(f"   Compatible: {model.get('compatible', 'Unknown')}")
        print()

    # For now, just download the first model as an example
    if compatible_models:
        first_model = compatible_models[0]
        print(f"Downloading {first_model['name']}...")
        # TODO: Implement actual download logic
        print("Download would be implemented here...")
        print("Model download placeholder - actual implementation coming soon!")

def main():
    parser = argparse.ArgumentParser(description='Download compatible models for the generation server')
    parser.add_argument('--list-only', action='store_true', help='List compatible models without downloading')
    parser.add_argument('--model', help='Download specific model by name')

    args = parser.parse_args()

    if args.list_only:
        # List only mode
        hardware_detector = HardwareDetector()
        model_manager = ModelManager(hardware_detector)
        compatible_models = model_manager.get_compatible_models()

        print(f"Available compatible models:")
        for model in compatible_models:
            print(f"- {model['name']}: {model['description']}")
    else:
        download_models()

if __name__ == "__main__":
    main()