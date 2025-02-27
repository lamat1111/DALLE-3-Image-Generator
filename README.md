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

## How to Use

1. Set your OpenAI API key inside the script (`API_KEY`).
2. Run the script:

    ```bash
    python3 dalle3_image_gen.py
    ```

3. Enter your prompt with optional flags:

    ```
    A magical forest at sunset -size landscape -quality hd -style natural
    ```

   Flags are optional — defaults are `square`, `standard`, and `vivid`.

4. Follow the menu to generate, tweak, or save the prompt after generation.

---

## Example Prompts

```text
A futuristic city skyline -size landscape -quality hd -style vivid
A peaceful Zen garden -size portrait -quality standard -style natural

