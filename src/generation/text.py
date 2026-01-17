import subprocess
import json

class TextGenerator:
    def __init__(self):
        self.ollama_available = self._check_ollama()

    def _check_ollama(self):
        try:
            result = subprocess.run(['ollama', '--version'],
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def generate(self, prompt, model_name="llama2", max_length=200):
        if not self.ollama_available:
            return "Ollama not available"

        try:
            # Use Ollama for text generation
            result = subprocess.run([
                'ollama', 'run', model_name,
                '--prompt', prompt,
                '--max-length', str(max_length)
            ], capture_output=True, text=True)

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr}"

        except Exception as e:
            return f"Generation error: {str(e)}"

    def get_available_models(self):
        if not self.ollama_available:
            return []

        try:
            result = subprocess.run(['ollama', 'list'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Parse ollama list output
                models = []
                for line in result.stdout.split('\n')[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            models.append(parts[1])
                return models
        except:
            pass

        return []