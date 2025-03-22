import requests
import json
import time
import wmi
import psutil


def get_gpu_utilization():
    try:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        gpu_info = w.Sensor()
        gpu_data = {}
        
        for sensor in gpu_info:
            if sensor.SensorType == 'Load' and 'GPU' in sensor.Name:
                gpu_data['load'] = sensor.Value
            elif sensor.SensorType == 'SmallData' and 'GPU' in sensor.Name:
                if 'Memory' in sensor.Name:
                    gpu_data['memory_used'] = sensor.Value
                elif 'Total' in sensor.Name:
                    gpu_data['memory_total'] = sensor.Value
        
        return gpu_data
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return None


def test_koboldcpp_inference():
    # KoboldCpp uses a different API than Ollama
    url = "http://localhost:5001/api/v1/generate"
    
    data = {
        "prompt": "Write a short story about a robot learning to paint. Keep it under 100 words.",
        "max_context_length": 2048,
        "max_length": 200,
        "temperature": 0.7,
        "top_p": 0.9,
        "n": 1,
        "stop": ["\n", "Human:", "AI:"],
        "stream": False,
        "use_gpu": True,
        "gpu_layers": 43  # Use most layers on GPU
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Check GPU utilization before request
        print("\nGPU Utilization before request:")
        gpu_info = get_gpu_utilization()
        if gpu_info:
            print("GPU Information:")
            print(f"  Load: {gpu_info.get('load', 'N/A')}%")
            print(f"  Memory: {gpu_info.get('memory_used', 'N/A')}MB / {gpu_info.get('memory_total', 'N/A')}MB")
        else:
            print("No GPU information available")
        
        # Make the request
        start_time = time.time()
        response = requests.post(url, json=data, headers=headers)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print("\nResponse from KoboldCpp:")
            print(result['results'][0]['text'])
            
            # Check GPU utilization after request
            print("\nGPU Utilization after request:")
            gpu_info = get_gpu_utilization()
            if gpu_info:
                print("GPU Information:")
                print(f"  Load: {gpu_info.get('load', 'N/A')}%")
                print(f"  Memory: {gpu_info.get('memory_used', 'N/A')}MB / {gpu_info.get('memory_total', 'N/A')}MB")
            
            # Print performance metrics
            generation_time = end_time - start_time
            tokens = len(result['results'][0]['text'].split())
            print(f"\nPerformance Metrics:")
            print(f"  Generation Time: {generation_time:.2f}s")
            print(f"  Tokens Generated: {tokens}")
            print(f"  Tokens per Second: {tokens/generation_time:.2f}")
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    test_koboldcpp_inference() 