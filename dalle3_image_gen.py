import os
import sys
import requests
import json
import random
import string

# Set your OpenAI API Key here
API_KEY = "API_KEY_HERE"

# Base URL for OpenAI DALL-E 3 generation
API_URL = "https://api.openai.com/v1/images/generations"

# Output folder setup
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Ensure UTF-8 encoding for Windows terminal
if os.name == 'nt':
    import ctypes
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)

# Defaults
DEFAULT_SIZE = "square"
DEFAULT_QUALITY = "standard"
DEFAULT_STYLE = "vivid"

# Supported options
SIZES = {"square": "1024x1024", "portrait": "1024x1792", "landscape": "1792x1024"}
QUALITIES = {"standard", "hd"}
STYLES = {"vivid", "natural"}

# Session image identifier (random 5-char code)
SESSION_CODE = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))

def parse_input(user_input):
    flags = {"size": DEFAULT_SIZE, "quality": DEFAULT_QUALITY, "style": DEFAULT_STYLE}
    parts = user_input.split(" -")
    prompt = parts[0].strip()
    for part in parts[1:]:
        key, value = part.split(" ", 1)
        flags[key.lower().strip()] = value.strip().lower()
    return prompt, flags

def validate_flags(flags):
    if flags["size"] not in SIZES:
        print(f"Invalid size '{flags['size']}', using default '{DEFAULT_SIZE}'")
        flags["size"] = DEFAULT_SIZE
    if flags["quality"] not in QUALITIES:
        print(f"Invalid quality '{flags['quality']}', using default '{DEFAULT_QUALITY}'")
        flags["quality"] = DEFAULT_QUALITY
    if flags["style"] not in STYLES:
        print(f"Invalid style '{flags['style']}', using default '{DEFAULT_STYLE}'")
        flags["style"] = DEFAULT_STYLE

def show_help():
    print("\n--- HELP ---")
    print("Prompt format: <your prompt> -size <square|portrait|landscape> -quality <standard|hd> -style <vivid|natural>")
    print("Example: A sunset over the mountains -size landscape -quality hd -style natural")
    print("Flags are optional — defaults: square, standard, vivid")
    print("----------------\n")

def get_next_image_filename():
    existing = [f for f in os.listdir(OUTPUT_FOLDER) if f.startswith(f"dalle3-{SESSION_CODE}_") and f.endswith(".png")]
    next_number = len(existing) + 1
    base_name = f"dalle3-{SESSION_CODE}_{next_number:03}"
    return os.path.join(OUTPUT_FOLDER, base_name + ".png"), os.path.join(OUTPUT_FOLDER, base_name + ".txt")

def generate_image(prompt, flags):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": SIZES[flags["size"]],
        "quality": flags["quality"],
        "style": flags["style"]
    }
    print("\nGenerating image, please wait...")
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    image_url = response.json()["data"][0]["url"]

    image_path, txt_path = get_next_image_filename()
    image_response = requests.get(image_url)
    with open(image_path, "wb") as file:
        file.write(image_response.content)

    print(f"✅ Image saved as: {image_path}\n")
    return image_path, txt_path

def save_prompt_to_file(txt_path, prompt, flags):
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(f"Prompt: {prompt}\n")
        file.write(f"Size: {flags['size']}\n")
        file.write(f"Quality: {flags['quality']}\n")
        file.write(f"Style: {flags['style']}\n")
    print(f"✅ Prompt saved to: {txt_path}\n")

def main():
    print("\n===== DALLE3 IMAGE GENERATOR =====\n")
    prompt, flags = None, None

    while True:
        if not prompt:
            user_input = input("Enter your prompt (with optional flags), 'h' for help or 'e' to exit: ").strip()
            if user_input.lower() == 'e':
                break
            elif user_input.lower() == 'h':
                show_help()
                continue
            prompt, flags = parse_input(user_input)
            validate_flags(flags)

        image_path, txt_path = generate_image(prompt, flags)

        while True:
            print("What do you want to do next?\n")
            print("1 - Regenerate (same prompt, same parameters)")
            print("2 - Modify the image (describe a tweak)")
            print("3 - Change size/quality/style only")
            print("4 - Start over with a new prompt")
            print("5 - Save prompt to .txt file")
            print("e - Exit\n")

            choice = input("Choose an option: ").strip().lower()

            if choice == 'e':
                return
            elif choice == '1':
                # Regenerate with same prompt and flags
                break
            elif choice == '2':
                tweak = input("Describe your modification: ").strip()
                prompt = f"{prompt}. {tweak}"
                break
            elif choice == '3':
                new_flags_input = input("Enter new flags (like: -size landscape -quality hd -style natural): ").strip()
                _, new_flags = parse_input(" " + new_flags_input)
                validate_flags(new_flags)
                flags.update(new_flags)
                break
            elif choice == '4':
                prompt, flags = None, None
                break
            elif choice == '5':
                save_prompt_to_file(txt_path, prompt, flags)
            else:
                print("❌ Invalid choice, try again.\n")

    if os.name == 'nt':
        os.system('pause')

if __name__ == "__main__":
    main()
