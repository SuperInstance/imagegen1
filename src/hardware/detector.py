import subprocess
import os
import re
from pathlib import Path

class HardwareDetector:
    def detect_specs(self):
        specs = {
            'gpu': self._detect_gpu(),
            'cpu': self._detect_cpu(),
            'memory': self._detect_memory(),
            'storage': self._detect_storage()
        }
        return specs

    def _detect_gpu(self):
        gpu_info = {
            'available': False,
            'cuda_available': False,
            'memory_mb': 0,
            'name': '',
            'driver_version': '',
            'compute_capability': 0
        }

        # Try to detect NVIDIA GPU first
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,driver_version,compute_cap', '--format=csv,noheader,nounits'],
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    parts = [p.strip() for p in output.split(',')]
                    if len(parts) >= 3:
                        gpu_info['name'] = parts[0]
                        gpu_info['memory_mb'] = int(parts[1].split()[0])  # Convert " MiB" to number
                        gpu_info['driver_version'] = parts[2]
                        try:
                            gpu_info['compute_capability'] = int(float(parts[3])) if len(parts) > 3 else 0
                        except (ValueError, IndexError):
                            gpu_info['compute_capability'] = 0
                        gpu_info['available'] = True

                    # Check CUDA availability
                    try:
                        cuda_result = subprocess.run(['nvcc', '--version'], capture_output=True, text=True)
                        gpu_info['cuda_available'] = cuda_result.returncode == 0
                    except:
                        gpu_info['cuda_available'] = False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # If no NVIDIA GPU, try AMD ROCm
        if not gpu_info['available']:
            try:
                result = subprocess.run(['rocm-smi'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    # Parse ROCm output to get GPU info
                    output = result.stdout
                    if 'GPU' in output:
                        gpu_info['available'] = True
                        gpu_info['name'] = 'AMD GPU'  # Default, can be enhanced
                        # Extract memory info if available
                        mem_match = re.search(r'Memory.*?(\d+)', output)
                        if mem_match:
                            gpu_info['memory_mb'] = int(mem_match.group(1))
                        gpu_info['cuda_available'] = False  # ROCm != CUDA but has similar capabilities
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass

        return gpu_info

    def _detect_cpu(self):
        cpu_info = {'cores': 0, 'frequency_mhz': 0, 'name': ''}

        # Get CPU info from /proc/cpuinfo
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()

            # Extract model name
            model_match = re.search(r'model name\s*:\s*(.+)', cpuinfo)
            if model_match:
                cpu_info['name'] = model_match.group(1).strip()

            # Get number of cores
            core_matches = re.findall(r'processor\s*:\s*\d+', cpuinfo)
            cpu_info['cores'] = len(core_matches)

            # Get maximum frequency
            freq_match = re.search(r'cpu MHz\s*:\s*(\d+)', cpuinfo)
            if freq_match:
                cpu_info['frequency_mhz'] = int(freq_match.group(1))
            else:
                # Fallback: get current frequency
                try:
                    result = subprocess.run(['lscpu'], capture_output=True, text=True)
                    if result.returncode == 0:
                        freq_match = re.search(r'MHz\s*:\s*([\d.]+)', result.stdout)
                        if freq_match:
                            cpu_info['frequency_mhz'] = int(float(freq_match.group(1)))
                except:
                    pass

        except FileNotFoundError:
            pass

        return cpu_info

    def _detect_memory(self):
        memory_info = {'total_gb': 0, 'available_gb': 0}

        try:
            # Try free command first
            result = subprocess.run(['free', '-g'], capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if line.startswith('Mem:'):
                        parts = line.split()
                        if len(parts) >= 2:
                            memory_info['total_gb'] = int(parts[1])
                            memory_info['available_gb'] = int(parts[3])
                            break
            else:
                # Fallback to reading /proc/meminfo
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()

                total_match = re.search(r'MemTotal:\s*(\d+)\s*kB', meminfo)
                if total_match:
                    memory_info['total_gb'] = int(total_match.group(1)) // (1024 * 1024)

                avail_match = re.search(r'MemAvailable:\s*(\d+)\s*kB', meminfo)
                if avail_match:
                    memory_info['available_gb'] = int(avail_match.group(1)) // (1024 * 1024)

        except FileNotFoundError:
            pass

        return memory_info

    def _detect_storage(self):
        storage_info = {'total_gb': 0, 'available_gb': 0, 'type': 'Unknown'}

        try:
            # Try df command
            result = subprocess.run(['df', '-h', '--output=source,size,avail,target'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 3 and parts[3] == '/':  # Root filesystem
                        # Convert human-readable size to GB
                        size_str = parts[1]
                        avail_str = parts[2]

                        def convert_to_gb(size_str):
                            if size_str.endswith('G'):
                                return int(size_str[:-1])
                            elif size_str.endswith('T'):
                                return int(size_str[:-1]) * 1024
                            elif size_str.endswith('M'):
                                return int(size_str[:-1]) // 1024
                            return 0

                        storage_info['total_gb'] = convert_to_gb(size_str)
                        storage_info['available_gb'] = convert_to_gb(avail_str)

                        # Detect filesystem type
                        if parts[0].startswith('/dev/'):
                            storage_info['type'] = 'HDD' if 'nvme' not in parts[0].lower() else 'NVMe'
                        break

        except FileNotFoundError:
            pass

        return storage_info