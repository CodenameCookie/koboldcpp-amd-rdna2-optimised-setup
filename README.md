# KoboldCpp AMD RDNA2 Optimised Setup

This repository contains optimised settings for running KoboldCpp with AMD GPUs, specifically tested with the AMD Radeon RX 6700 XT and Llama 2 7B model.

## GPU Architecture Compatibility

This setup was specifically developed and tested with an AMD Radeon RX 6700 XT (RDNA2 architecture). Whilst newer RDNA3 and RDNA4 GPUs might handle dual GPU setups better with Vulkan, RDNA2 GPUs can experience issues when running alongside NVIDIA GPUs. This solution provides a reliable way to:

- Ensure stable operation on RDNA2 GPUs
- Avoid Vulkan-related conflicts in dual GPU setups
- Provide consistent performance regardless of GPU architecture

## Dual GPU Setup Benefits

This setup is particularly useful for systems with multiple GPUs, especially when you have both AMD and NVIDIA GPUs installed. In such configurations, other applications might try to use both GPUs with Vulkan, which can lead to conflicts and failures. By using the ROCm version of KoboldCpp, we ensure that:

- The application specifically targets the AMD GPU
- Avoids conflicts with NVIDIA GPU operations
- Prevents Vulkan-related issues in dual GPU setups
- Provides stable performance on the AMD GPU

## Prerequisites

- AMD GPU with ROCm support (tested with RX 6700 XT)
- Windows 10/11
- Python 3.x
- KoboldCpp ROCm version

## Installation

1. Check if ROCm is already installed:
   - Open PowerShell and run `rocm-smi` to check if ROCm is installed
   - If the command is recognized, ROCm is already installed
   - If not, proceed with ROCm installation

2. Install ROCm for Windows (if not already installed):
   - Download and install ROCm from [AMD's official website](https://rocm.docs.amd.com/en/latest/deploy/windows/quick_start.html)
   - Follow the installation guide for Windows
   - Make sure your GPU is supported by the installed ROCm version

3. Download KoboldCpp ROCm:
   - Download the latest release from [YellowRoseCx/koboldcpp-rocm](https://github.com/YellowRoseCx/koboldcpp-rocm/releases)
   - For Windows: Download `koboldcpp_rocm.exe` (single file) or `koboldcpp_rocm_files.zip`
   - If using the zip file, extract it to your desired location
   - Place `koboldcpp_rocm.exe` in the root directory of this project

4. Download the Llama 2 7B Chat model:
   - Create a models directory if it doesn't exist:
   ```powershell
   mkdir -Force models
   ```
   - Download the GGUF version of Llama 2 7B Chat using PowerShell:
   ```powershell
   Invoke-WebRequest -Uri "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf" -OutFile "models\llama-2-7b-chat.gguf"
   ```
   - Note: The download is approximately 4GB and may take some time depending on your internet connection
   - Alternative: You can manually download the model from [TheBloke's HuggingFace repository](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF) and place it in the `models` folder

## Model Information

- Model: Llama 2 7B Chat
- Format: GGUF
- Size: 3.80 GiB
- Context Size: 2048
- Total Layers: 32

## Performance Optimization

After testing various configurations, we found the optimal settings for the RX 6700 XT:

```powershell
.\koboldcpp_rocm.exe --model .\models\llama-2-7b-chat.gguf --host 127.0.0.1 --port 5001 --contextsize 2048 --gpulayers 30 --blasbatchsize 2048 --blasthreads 4 --highpriority --usecublas mmq
```

### Key Parameters Explained

- `--gpulayers 30`: Offloads 30 layers to GPU (optimal for 32-layer model)
- `--blasbatchsize 2048`: Maximum batch size for better GPU utilization
- `--blasthreads 4`: Reduced thread count to prevent CPU bottlenecks
- `--highpriority`: Improves CPU allocation
- `--usecublas mmq`: Enables Matrix Multiplication Quantization through hipBLAS

### Performance Results

Previous configurations:
- 43 layers: 17.69s, 2.94 tokens/s
- 27 layers: 15.76s, 3.05 tokens/s
- 20 layers: 16.54s, 3.14 tokens/s

Optimized configuration:
- 30 layers with MMQ: 6.29s, 7.79 tokens/s

## Usage

1. Stop any existing KoboldCpp processes:
```powershell
Get-Process -Name koboldcpp_rocm -ErrorAction SilentlyContinue | Stop-Process -Force
```

2. Start KoboldCpp with optimized settings:
```powershell
.\koboldcpp_rocm.exe --model .\models\llama-2-7b-chat.gguf --host 127.0.0.1 --port 5001 --contextsize 2048 --gpulayers 30 --blasbatchsize 2048 --blasthreads 4 --highpriority --usecublas mmq
```

3. Test the performance:
```powershell
python test_inference.py
```

## Notes

- The model requires approximately 3.80 GiB of VRAM
- The optimised settings use hipBLAS for better GPU utilisation
- High priority mode is recommended for better CPU allocation
- The context size of 2048 provides a good balance between performance and memory usage 

## Contributing

We welcome contributions to improve this setup! Here's how you can help:

### Reporting Issues
- Please check if the issue has already been reported
- Include your system specifications (GPU model, ROCm version, etc.)
- Provide detailed steps to reproduce the issue
- Include any error messages or logs

### Pull Requests
1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly with your AMD GPU setup
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style
- Follow the existing code style
- Use UK English spelling in documentation
- Keep code comments clear and concise
- Update documentation for any new features

### Testing
- Test changes with different AMD GPU models
- Verify performance improvements
- Check compatibility with different ROCm versions
- Ensure no regressions in existing functionality

### License
By contributing, you agree that your contributions will be licensed under the same terms as the project. 