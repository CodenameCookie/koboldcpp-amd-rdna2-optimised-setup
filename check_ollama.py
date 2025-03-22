import requests
from datetime import datetime


def check_ollama_installation():
    try:
        # Attempt to connect to Ollama's default API endpoint
        response = requests.get('http://localhost:11434/api/version')
        
        if response.status_code == 200:
            print(f"[{datetime.now()}] Ollama is installed and running!")
            print(f"Version: {response.json().get('version', 'Unknown')}")
            return True
        else:
            print(f"[{datetime.now()}] Ollama is installed but not responding properly.")
            print(f"Status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"[{datetime.now()}] Ollama is not installed or not running.")
        print("Please install Ollama from https://ollama.ai/")
        return False
    except Exception as e:
        print(f"[{datetime.now()}] An error occurred while checking Ollama:")
        print(f"Error: {str(e)}")
        return False


if __name__ == "__main__":
    check_ollama_installation() 