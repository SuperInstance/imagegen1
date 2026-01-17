class ModelManager:
    def __init__(self, hardware_detector):
        self.detector = hardware_detector
        self.downloaded_models = {}

    def check_compatibility(self, model_spec, hardware):
        gpu = hardware.get('gpu', {})

        # Check VRAM requirements
        vram_gb = gpu.get('memory_mb', 0) / 1024
        if model_spec['min_vram_gb'] > vram_gb:
            return False, f"Insufficient VRAM: need {model_spec['min_vram_gb']}GB, have {vram_gb:.1f}GB"

        # Check CUDA requirement
        if model_spec['requires_cuda'] and not gpu.get('cuda_available', False):
            return False, "CUDA required but not available"

        return True, "Compatible"

    def download_model(self, model_name):
        # Placeholder for actual download logic
        pass

    def get_available_models(self):
        # Return list of models compatible with current hardware
        pass