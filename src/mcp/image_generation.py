class ImageGenerationHandler:
    def __init__(self, image_generator):
        self.generator = image_generator

    async def handle_generate_image(self, params):
        result = self.generator.generate(
            prompt=params.get('prompt', ''),
            model_name=params.get('model', 'stable-diffusion-xl'),
            width=params.get('width', 512),
            height=params.get('height', 512)
        )
        return {'result': result, 'success': True}

    async def get_models(self):
        return {'models': self.generator.get_available_models()}