class TextGenerationHandler:
    def __init__(self, text_generator):
        self.generator = text_generator

    async def handle_generate_text(self, params):
        result = self.generator.generate(
            prompt=params.get('prompt', ''),
            model_name=params.get('model', 'gpt-3.5-turbo'),
            max_tokens=params.get('max_tokens', 100)
        )
        return {'result': result, 'success': True}

    async def get_models(self):
        return {'models': self.generator.get_available_models()}