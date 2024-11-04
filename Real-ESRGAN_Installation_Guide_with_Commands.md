
# Guide to Installing Real-ESRGAN with CUDA Support

## Prerequisites
- Ensure you have an NVIDIA GPU that supports CUDA.
- Update your GPU drivers to the latest version.
- Download and install Miniconda from [Miniconda Downloads](https://docs.conda.io/en/latest/miniconda.html).

---

## Step 1: Create a Conda Environment
1. Open a terminal or command prompt.
2. Run the following command:
   ```bash
   conda create -n realesrgan python=3.8 -y
   ```
3. Activate the environment:
   ```bash
   conda activate realesrgan
   ```

---

## Step 2: Install PyTorch with CUDA Support
- Use the appropriate command for your CUDA version:

  **For CUDA 11.8:**
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

  **For CUDA 11.7:**
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
  ```

  **For CUDA 11.6:**
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu116
  ```

---

## Step 3: Install Other Dependencies
```bash
pip install basicsr facexlib gfpgan
pip install -r https://raw.githubusercontent.com/xinntao/Real-ESRGAN/master/requirements.txt
```

---

## Step 4: Clone the Real-ESRGAN Repository
1. Navigate to the directory where you want to store Real-ESRGAN:
   ```bash
   cd path/to/your/directory
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/xinntao/Real-ESRGAN.git
   cd Real-ESRGAN
   ```

---

## Step 5: Download Pre-trained Models
- Download the pre-trained models from the [Real-ESRGAN Model Zoo](https://github.com/xinntao/Real-ESRGAN#model-zoo).
- Place the models in the `weights` folder of the Real-ESRGAN directory.

---

## Step 6: Verify CUDA Support
1. Run the following script in Python:
   ```python
   import torch
   print(torch.cuda.is_available())  # Should return True
   print(torch.cuda.get_device_name(0))  # Should display your GPU name
   ```

---

## Step 7: Run Real-ESRGAN
- Use the following command to test Real-ESRGAN:
  ```bash
  python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/your_image.jpg --outscale 4 --tile 400 --tile_pad 10 --face_enhance
  ```
- Replace `your_image.jpg` with the path to your image.

---

## Step 8: Fix for Import Error (if needed)
- If you encounter an error related to `functional_tensor`, edit `basicsr/data/degradations.py`:
  ```python
  from torchvision.transforms.functional_tensor import rgb_to_grayscale
  ```
- Change it to:
  ```python
  from torchvision.transforms.functional import rgb_to_grayscale
  ```

---

## Quick Guide for Real-ESRGAN Commands
1. **Basic Image Upscaling**:
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/your_image.jpg --outscale 2
   ```
   - `--outscale`: Specifies the upscaling factor (e.g., 2, 4).

2. **Upscaling with Face Enhancement**:
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/your_image.jpg --outscale 4 --face_enhance
   ```
   - `--face_enhance`: Enhances facial details if the image contains faces.

3. **Using a Custom Tile Size** (to manage GPU memory):
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/your_image.jpg --tile 200 --tile_pad 10
   ```
   - `--tile`: Sets the tile size for processing large images to avoid memory issues.
   - `--tile_pad`: Adds padding to reduce visible seams between tiles.

4. **Output Directory**:
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/your_image.jpg -o outputs/
   ```
   - `-o`: Specifies the output directory for the upscaled images.

---

## Useful Links
- **PyTorch Installation**: [PyTorch Get Started](https://pytorch.org/get-started/locally/)
- **CUDA Downloads**: [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- **Real-ESRGAN GitHub**: [Real-ESRGAN Repository](https://github.com/xinntao/Real-ESRGAN)
