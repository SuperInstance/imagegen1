class HardwareDetector:
    def detect_specs(self):
        # Basic implementation - will be enhanced
        return {
            'gpu': {'available': False},
            'cpu': {'cores': 0, 'frequency_mhz': 0},
            'memory': {'total_gb': 0},
            'storage': {'total_gb': 0}
        }