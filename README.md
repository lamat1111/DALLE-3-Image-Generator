# DALL-E 3 Image Generator Script

This is a Python script that interacts with **OpenAI's DALL-E 3 API** to generate images directly from text prompts.

## Features

- Supports different image sizes: `square`, `portrait`, `landscape`
- Choose between `standard` or `hd` quality
- Select your preferred style: `vivid` or `natural`
- Easy-to-use prompt format with optional flags
- After generating an image, you can:
    - Regenerate the same prompt
    - Modify the prompt for variations
    - Change size/quality/style
    - Start fresh with a new prompt
    - Optionally save the prompt to a `.txt` file

---

## Setup

### 1. Install Dependencies
You'll need Python 3.8+ and `requests` library. Install with:
```sh
pip install requests
```

### 2. Get Your OpenAI API Key
- Go to [https://platform.openai.com/signup](https://platform.openai.com/signup) if you don't have an account.
- After logging in, visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
- Generate a new secret key and copy it.

Paste the key into this line of the script:
```python
API_KEY = "YOUR_OPENAI_API_KEY"
```

### 3. Launch the Script

To start the script, open a terminal (or command prompt on Windows), navigate to the folder where you placed the script, and run:

For Linux/macOS:
```sh
python3 dalle3_image_gen.py
```

For Windows:
```sh
python dalle3_image_gen.py
```

⚠️ Make sure you are **in the same folder** where the script is located, or provide the full path when launching.

### Optional: Create a `.bat` File (Windows Only)

To make it easier to launch, you can create a file named something like `run-dalle3.bat` in the same folder as the script. Inside the `.bat` file, add:

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
This generates a 1792x1024 vivid image in HD quality.

### Available Flags
- `-size`: square, portrait, landscape
- `-quality`: standard, hd
- `-style`: vivid, natural

You can omit flags to use defaults (square, standard, vivid).

---

## Menu Options

After each image, you can choose:

1️⃣ Regenerate (same prompt & parameters)  
2️⃣ Modify the image (add a tweak to the prompt)  
3️⃣ Change size/quality/style only  
4️⃣ Start over with a new prompt  
5️⃣ Save the prompt to a `.txt` file (with same name as the image)


## Compatibility

✅ Works on:
- Linux (Ubuntu, Debian, etc.)
- macOS
- Windows (with automatic UTF-8 terminal fix applied)

⚠️ Requires:
- Python 3.8+
- Internet connection

## Example Output

Files will be saved in an `output` folder, like:
```
output/dalle3-abc12_001.png
output/dalle3-abc12_001.txt  (if you choose to save the prompt)
```
