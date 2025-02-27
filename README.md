# DALL-E 3 Image Generator Script

This is a Python script that interacts with OpenAI's DALL-E 3 API to generate images directly from text prompts.

## Features

- Supports different image sizes: square, portrait, landscape
- Choose between standard or hd quality
- Select your preferred style: vivid or natural
- Easy-to-use prompt format with optional flags
- Generate single images or multiple variations with the `-variations` flag
- After generating an image(s), you can:
    - Regenerate the same prompt(s)
    - Modify the prompt(s) for variations
    - Change size/quality/style
    - Start fresh with a new prompt
- Optionally save the prompt(s) to `.txt` file(s)

---

## Setup

### 1. Install Dependencies

You'll need Python 3.8+ and the `requests` library. Install with:

```sh
pip install requests
```

### 2. Get Your OpenAI API Key

- Go to [OpenAI Signup](https://platform.openai.com/signup) if you don't have an account.
- After logging in, visit [OpenAI API Keys](https://platform.openai.com/api-keys).
- Generate a new secret key and copy it.
- Paste the key into this line of the script:

```python
API_KEY = "YOUR_OPENAI_API_KEY"
```

---

### 3. Launch the Script

To start the script, open a terminal (or command prompt on Windows), navigate to the folder where you placed the script, and run:

**For Linux/macOS:**

```sh
python3 dalle3_image_gen.py
```

**For Windows:**

```sh
python dalle3_image_gen.py
```

⚠️ Make sure you are in the same folder where the script is located, or provide the full path when launching.

---

### Optional: Create a .bat File (Windows Only)

To make it easier to launch, create a file named `run-dalle3.bat` in the same folder as the script. Inside the `.bat` file, add:

```bat
@echo off
python dalle3_image_gen.py
pause
```

Double-click the `.bat` file to launch the script directly.

---

## Usage

### Basic Example

```text
A futuristic city at sunset -size landscape -quality hd -style vivid
```

This generates a `1792x1024` vivid image in HD quality.

---

### Available Flags

| Flag        | Options                               | Default  |
|-------------|---------------------------------------|----------|
| `-size`     | square, portrait, landscape          | square   |
| `-quality`  | standard, hd                         | standard |
| `-style`    | vivid, natural                       | vivid    |
| `-variations N` | N = number of variations           | none     |

You can omit flags to use defaults (square, standard, vivid).

---

## Advanced Features

### Generating Multiple Variations with `-variations N`

The `-variations N` flag allows you to create multiple distinct images from a single base prompt by specifying different characteristics. This is useful for exploring variations of a concept, such as different perspectives, styles, or details.

To use it, include `-variations N` in your prompt (where `N` is the number of variations you want, e.g., 3), followed by a list of variation categories and their options. Each category should be on a new line, with options listed in parentheses and separated by commas.

Example:

```text
a glowing 3D capital Q made of data streams, with fuchsia and orange gradients, floating in space -quality hd -variations 3
Camera angle (straight-on, low-angle, top-down)
Background intensity (subtle stars, dense data nebulae)
Circuit detail (minimalist, highly complex Celtic mandalas)
Mood (sacred, mysterious, cyberpunk)
```

This generates 3 unique images, each combining one option from each category (e.g., a straight-on view with subtle stars, minimalist circuits, and a sacred mood for one image).

The script automatically creates descriptive prompts for each variation, ensuring distinct outputs, and saves them sequentially with filenames like:

```
dalle3-abc12_001_camera-angle-straight-on...
```

The script picks a set number of combinations (up to 4 by default, cycling through options if needed), so ensure your categories have enough options to cover the requested number of variations.

You can adjust size, quality, and style with additional flags as needed.

---

## Menu Options

After generating image(s), you can choose:

1️⃣ Regenerate (same prompt(s) & parameters)  
2️⃣ Modify the prompt(s) (add a tweak to the prompt)  
3️⃣ Change size/quality/style only  
4️⃣ Start over with a new prompt  
5️⃣ Save the prompt(s) to `.txt` file(s) (with the same name as the image(s))

---

## Compatibility

✅ Works on:

- Linux (Ubuntu, Debian, etc.)
- macOS
- Windows (with automatic UTF-8 terminal fix applied)

⚠️ Requires:

- Python 3.8+
- Internet connection

---

## Example Output

Files will be saved in an output folder, like:

```
output/dalle3-abc12_001.png
output/dalle3-abc12_001.txt  (if you choose to save the prompt)
```

For variations, filenames include details, e.g.:

```
output/dalle3-abc12_001_camera-angle-straight-on_background-intensity-subtle-stars_circuit-detail-minimalist_mood-sacred.png
output/dalle3-abc12_001.txt  (for each variation, if saved)
```

