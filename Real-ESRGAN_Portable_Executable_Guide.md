
# Guide to Using Real-ESRGAN Portable Executable Files

## Overview
This guide provides instructions on how to download, set up, and use the portable executable files for Real-ESRGAN, which are ideal for users who do not wish to install Python or manage dependencies.

---

## Step 1: Download the Real-ESRGAN Executable Files
1. Visit the [Releases page of Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN/releases).
2. Download the latest version of the portable executable files for your operating system:
   - **Windows**: Look for a file like `realesrgan-ncnn-vulkan-xxxx-windows.zip`
   - **Linux**: Look for a file like `realesrgan-ncnn-vulkan-xxxx-linux.zip`
   - **macOS**: Look for a file like `realesrgan-ncnn-vulkan-xxxx-macos.zip`

---

## Step 2: Extract the Downloaded Archive
1. Locate the downloaded `.zip` file.
2. Extract the contents to a folder of your choice.

---

## Step 3: Prepare Your Images
1. Place the images you want to upscale in the same folder as the extracted executable files.
2. Alternatively, you can specify the path to your images when running the commands.

---

## Step 4: Using the Executable
### Basic Command
1. Open a command prompt (Windows) or terminal (Linux/macOS).
2. Navigate to the folder where you extracted the files:
   ```bash
   cd path/to/realesrgan-ncnn-vulkan
   ```
3. Run the basic command to upscale an image:
   ```bash
   realesrgan-ncnn-vulkan -i input.jpg -o output.png
   ```
   - **`-i input.jpg`**: Specifies the input image file.
   - **`-o output.png`**: Specifies the output image file.

---

## Step 5: Command Options
### Common Arguments
- **`-n <model_name>`**: Specifies the model to use.
  - Example: `-n realesrgan-x4plus` (default model for general upscaling)
  - Other options: `realesrgan-x4plus-anime` (for anime images)
- **`-s <scale>`**: Sets the upscaling factor (default is 4).
  - Example: `-s 2` (for 2x upscaling)
- **`-t <tile_size>`**: Sets the tile size for processing large images to avoid running out of GPU memory (default is 0, which means no tiling).
  - Example: `-t 200`
- **`-g <gpu_id>`**: Specifies the GPU to use (default is 0).
  - Example: `-g 1` (if you have multiple GPUs)

---

## Example Commands
1. **Upscale an Image with Default Settings**
   ```bash
   realesrgan-ncnn-vulkan -i input.jpg -o output.png
   ```

2. **Upscale with a Custom Model and Scale Factor**
   ```bash
   realesrgan-ncnn-vulkan -i input.jpg -o output.png -n realesrgan-x4plus-anime -s 2
   ```

3. **Use Tiling to Manage GPU Memory**
   ```bash
   realesrgan-ncnn-vulkan -i input.jpg -o output.png -t 100
   ```

---

## Notes
- Ensure your GPU drivers are up to date to make full use of Vulkan support.
- For large images, experiment with the `-t` (tile size) option to optimize performance and prevent memory issues.
- You do not need to install Python or any other dependencies to use these executables.

---

## Useful Links
- **Real-ESRGAN GitHub**: [Real-ESRGAN Repository](https://github.com/xinntao/Real-ESRGAN)
- **Releases Page**: [Download Executables](https://github.com/xinntao/Real-ESRGAN/releases)
- **Vulkan Documentation**: [Vulkan Info](https://vulkan.lunarg.com/)
