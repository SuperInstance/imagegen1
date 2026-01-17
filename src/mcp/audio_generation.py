class AudioGenerationHandler:
    def __init__(self, audio_generator):
        self.generator = audio_generator

    async def handle_generate_audio(self, params):
        result = self.generator.generate(
            text=params.get('text', ''),
            model_name=params.get('model', 'tts-1'),
            voice=params.get('voice', 'alloy'),
            speed=params.get('speed', 1.0)
        )
        return {'result': result, 'success': True}

    async def get_models(self):
        return {'models': self.generator.get_available_models()}