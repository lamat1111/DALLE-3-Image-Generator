import os
import sys
import requests
import json
import random
import string
import time  # For adding delays between requests if needed

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
    lines = user_input.strip().split("\n")
    flags = {"size": DEFAULT_SIZE, "quality": DEFAULT_QUALITY, "style": DEFAULT_STYLE}
    base_prompt = ""
    variations = {}
    num_variations = 1  # Default to single if not specified

    # Split at -variations
    if "-variations" in user_input:
        base_part, variations_part = user_input.split("-variations", 1)
        # Check if there's a number after -variations
        variations_number = variations_part.strip().split("\n")[0].strip()
        try:
            num_variations = int(variations_number) if variations_number.isdigit() else 1
        except ValueError:
            print(f"Warning: Invalid number of variations '{variations_number}', defaulting to 1")
            num_variations = 1

        base_lines = base_part.strip().split("\n")
        variation_lines = [line.strip() for line in variations_part.strip().split("\n")[1:] if line.strip()]
    else:
        base_lines = lines
        variation_lines = []

    # Parse base prompt and flags
    base_input = " ".join(line.strip() for line in base_lines if line.strip())
    base_prompt = base_input

    # Parse flags from base prompt
    if " -" in base_prompt:
        prompt_part, flag_part = base_prompt.split(" -", 1)
        base_prompt = prompt_part.strip()
        for part in flag_part.split(" -"):
            if part.strip():  # Skip empty parts
                try:
                    key, value = part.split(" ", 1)
                    if key.lower().strip() == "variations":
                        # Skip -variations, already handled above
                        continue
                    flags[key.lower().strip()] = value.strip().lower()
                except ValueError:
                    print(f"Warning: Ignoring malformed flag in '{part}'")

    # Parse variations, handling trailing commas or empty options
    for line in variation_lines:
        if line and "(" in line and ")" in line:
            category, options_str = line.split("(", 1)
            options = [opt.strip().rstrip(',') for opt in options_str.rstrip(")").split(",") if opt.strip().rstrip(',')]
            if options:  # Only add if there are valid options
                variations[category.strip()] = options
            else:
                print(f"Warning: No valid options found for category '{category.strip()}'")

    return base_prompt, variations, num_variations, flags

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

def generate_variation_prompts(base_prompt, variations, num_variations):
    if not variations:  # Single prompt case
        return [base_prompt], ["single"]

    # Map variations to specific combinations
    full_prompts = []
    variation_labels = []
    categories = list(variations.keys())
    
    # Generate combinations (simplified for num_variations)
    combos = [
        (0, 0, 0, 0),  # First option from each category
        (1, 1, 1, 1),  # Second option from each category
        (2, 0, 1, 2),  # Mix for third
        (3, 1, 0, 3),  # Mix for fourth
    ][:num_variations]  # Limit to requested number

    for i, combo in enumerate(combos):
        details = []
        label_parts = []
        for j, idx in enumerate(combo[:len(categories)]):
            category = categories[j]
            option = variations[category][idx % len(variations[category])]  # Cycle if fewer options
            # Enhance prompt clarity with descriptive language
            if "camera angle" in category.lower():
                details.append(f"viewed from a {option} perspective")
            elif "background intensity" in category.lower():
                details.append(f"set against a {option} background")
            elif "circuit detail" in category.lower():
                details.append(f"featuring {option} circuit patterns")
            elif "mood" in category.lower():
                mood_style = {
                    "sacred": "with ethereal, divine lighting",
                    "mysterious": "with shadowy, enigmatic tones",
                    "corporate": "with sleek, professional lighting",
                    "cyberpunk": "with neon, futuristic accents"
                }.get(option.lower(), "")
                details.append(f"evoking a {option} mood {mood_style}")
            label_parts.append(f"{category.lower().replace(' ', '-')}-{option.replace(' ', '-')}")
        full_prompt = f"{base_prompt}, {', '.join(details)}"
        variation_label = "_".join(label_parts)
        full_prompts.append(full_prompt)
        variation_labels.append(variation_label)

    return full_prompts, variation_labels

def show_help():
    print("\n--- HELP ---")
    print("Enter your prompt in this format:")
    print("<base prompt> [flags] -variations <number>")
    print("<Category> (<option1>, <option2>, ...)")
    print("\nExample:")
    print("a glowing 3D capital Q made of data streams, with fuchsia and orange gradients, floating in space -quality hd -variations 3")
    print("Camera angle (straight-on, low-angle, top-down)")
    print("Background intensity (subtle stars, dense data nebulae)")
    print("Circuit detail (minimalist, highly complex Celtic mandalas)")
    print("Mood (sacred, mysterious, cyberpunk)")
    print("\nFor a single image, omit -variations:")
    print("A sunset over the mountains -quality hd")
    print("Flags: -size <square|portrait|landscape>, -quality <standard|hd>, -style <vivid|natural>")
    print("Defaults: square, standard, vivid")
    print("Type 'h' for help, 'e' to exit at any prompt.")
    print("----------------\n")

def get_next_image_filename(variation_label="single"):
    existing = [f for f in os.listdir(OUTPUT_FOLDER) if f.startswith(f"dalle3-{SESSION_CODE}_") and f.endswith(".png")]
    next_number = len(existing) + 1
    base_name = f"dalle3-{SESSION_CODE}_{next_number:03}"
    if variation_label != "single":
        base_name += f"_{variation_label}"
    return os.path.join(OUTPUT_FOLDER, base_name + ".png"), os.path.join(OUTPUT_FOLDER, base_name + ".txt")

def generate_image(prompt, flags, variation_label="single"):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,  # Ensure only one image per request
        "size": SIZES[flags["size"]],
        "quality": flags["quality"],
        "style": flags["style"]
    }
    print(f"\nGenerating image for variation '{variation_label}'...")
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        image_url = response.json()["data"][0]["url"]

        image_path, txt_path = get_next_image_filename(variation_label)
        image_response = requests.get(image_url, timeout=30)
        with open(image_path, "wb") as file:
            file.write(image_response.content)

        print(f"✅ Image saved as: {image_path}\n")
        return image_path, txt_path
    except requests.exceptions.RequestException as e:
        print(f"❌ Error generating image for '{variation_label}': {e}")
        return None, None
    except Exception as e:
        print(f"❌ Unexpected error for '{variation_label}': {e}")
        return None, None

def save_prompt_to_file(txt_path, prompt, flags):
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(f"Prompt: {prompt}\n")
        file.write(f"Size: {flags['size']}\n")
        file.write(f"Quality: {flags['quality']}\n")
        file.write(f"Style: {flags['style']}\n")
    print(f"✅ Prompt saved to: {txt_path}\n")

def main():
    print("\n===== DALLE3 IMAGE GENERATOR =====\n")
    prompt = None

    while True:
        if not prompt:
            print("Enter your prompt (type 'h' for help, 'e' to exit):")
            first_line = input().strip().lower()  # Get first line separately

            if first_line == 'e':
                break
            elif first_line == 'h':
                show_help()
                continue

            # If first line isn't a command, assume it's part of a multi-line prompt
            user_input = first_line + "\n"
            if "-variations" in first_line.lower():
                while True:
                    line = input().strip()
                    if not line:  # Blank line signals end
                        break
                    user_input += line + "\n"
            user_input = user_input.strip()

            base_prompt, variations, num_variations, flags = parse_input(user_input)
            validate_flags(flags)
            full_prompts, variation_labels = generate_variation_prompts(base_prompt, variations, num_variations)

            image_paths = []
            txt_paths = []
            # Generate images sequentially, one after the other, with detailed feedback
            for i, (p, label) in enumerate(zip(full_prompts, variation_labels), 1):
                print(f"\nProcessing variation {i} of {len(full_prompts)}: {p}")
                img_path, txt_path = generate_image(p, flags, label)
                if img_path and txt_path:
                    image_paths.append(img_path)
                    txt_paths.append(txt_path)
                else:
                    print(f"Warning: Failed to generate image for variation {label}. Continuing with remaining variations...")
                    continue  # Continue even if one image fails, instead of breaking
                # Add a small delay to ensure sequential processing and avoid API rate limits
                time.sleep(2)  # 2-second delay between requests

            if not image_paths:  # If no images were generated due to errors
                print("No images were generated due to errors. Please try again or check your API key.")
                continue

        # Post-generation options
        while True:
            print("What do you want to do next?\n")
            print("1 - Regenerate (same prompt, same parameters)")
            print("2 - Modify the prompt (describe a tweak)")
            print("3 - Change size/quality/style only")
            print("4 - Start over with a new prompt")
            print("5 - Save prompt(s) to .txt file(s)")
            print("e - Exit\n")

            choice = input("Choose an option: ").strip().lower()

            if choice == 'e':
                return
            elif choice == '1':
                break
            elif choice == '2':
                tweak = input("Describe your modification: ").strip()
                base_prompt = f"{base_prompt}, {tweak}"
                full_prompts, variation_labels = generate_variation_prompts(base_prompt, variations, num_variations)
                break
            elif choice == '3':
                new_flags_input = input("Enter new flags (like: -size landscape -quality hd -style natural): ").strip()
                _, _, _, new_flags = parse_input(f"dummy -variations {num_variations}\n{new_flags_input}")
                validate_flags(new_flags)
                flags.update(new_flags)
                break
            elif choice == '4':
                prompt = None
                break
            elif choice == '5':
                for p, txt_path in zip(full_prompts, txt_paths):
                    save_prompt_to_file(txt_path, p, flags)
            else:
                print("❌ Invalid choice, try again.\n")

    if os.name == 'nt':
        os.system('pause')

if __name__ == "__main__":
    main()
