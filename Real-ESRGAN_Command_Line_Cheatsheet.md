
# Real-ESRGAN Command Line Arguments Cheatsheet

## Basic Structure
```bash
python inference_realesrgan.py -n <model_name> -i <input_path> [options]
```

---

## Required Arguments
1. **`-n <model_name>`**: Specifies the model to use.
   - Example: `-n RealESRGAN_x4plus`
   - Common Models:
     - `RealESRGAN_x4plus`: General-purpose upscaling model.
     - `RealESRGAN_x4plus_anime_6B`: Model for anime images.

2. **`-i <input_path>`**: Path to the input image or directory.
   - Example: `-i inputs/image.jpg`

---

## Optional Arguments

### 1. **Output Options**
- **`-o <output_path>`**: Path to the output directory.
  - Example: `-o outputs/`

### 2. **Upscaling Options**
- **`--outscale <factor>`**: Specifies the upscaling factor (default is 4).
  - Example: `--outscale 2` (for 2x upscaling)
- **`--face_enhance`**: Enhances facial details in images.
  - Example: `--face_enhance`

### 3. **Tile Options (for Memory Management)**
- **`--tile <size>`**: Sets the tile size for processing (default is 0, which means no tiling).
  - Example: `--tile 400` (useful for large images to prevent GPU memory issues)
- **`--tile_pad <padding>`**: Adds padding to each tile to reduce visible seams (default is 10).
  - Example: `--tile_pad 10`
- **`--pre_pad <padding>`**: Adds padding to the input image to avoid border artifacts (default is 0).
  - Example: `--pre_pad 5`

### 4. **GPU Options**
- **`--gpu-id <id>`**: Specifies the GPU to use (default is 0).
  - Example: `--gpu-id 1` (if you have multiple GPUs and want to use a specific one)

### 5. **Advanced Options**
- **`--suffix <suffix>`**: Adds a custom suffix to the output file name.
  - Example: `--suffix _upscaled`
- **`--ext <extension>`**: Specifies the extension of the output images (default is `auto`).
  - Options: `jpg`, `png`, `auto`
  - Example: `--ext png`

---

## Example Commands

1. **Basic Image Upscaling**
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/image.jpg --outscale 2
   ```

2. **Upscaling with Face Enhancement**
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/image.jpg --outscale 4 --face_enhance
   ```

3. **Using Tile Size to Manage Memory**
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/image.jpg --tile 200 --tile_pad 10
   ```

4. **Specify Output Directory and Add Suffix**
   ```bash
   python inference_realesrgan.py -n RealESRGAN_x4plus -i inputs/image.jpg -o outputs/ --suffix _enhanced
   ```

---

## Notes
- Adjust `--tile` and `--tile_pad` settings if you encounter memory issues on your GPU.
- Use `--face_enhance` if your image contains faces and you want to improve their quality.
