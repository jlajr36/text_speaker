import asyncio
import edge_tts
from pathlib import Path
import re


def preprocess_text(text):
    """
    Preprocess technical text for clearer speech:
    - Replace code blocks with a short placeholder
    - Add pauses between paragraphs
    - Expand common technical acronyms
    """

    # Replace triple-backtick code blocks with placeholder
    text = re.sub(
        r"```.*?```",
        "[code block skipped]",
        text,
        flags=re.DOTALL
    )

    # Add small pause for paragraphs
    text = text.replace("\n\n", ".\n\n")

    # Expand acronyms commonly found in technical content
    replacements = {
        "API": "A P I",
        "HTTP": "H T T P",
        "SQL": "sequel",
        "JSON": "Jay Son"
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    return text


async def text_to_speech(text, output_file):
    voice = "en-US-JennyNeural"

    communicate = edge_tts.Communicate(
        text,
        voice,
        rate="-10%",
        volume="+0%"
    )

    await communicate.save(str(output_file))


async def main():
    current_dir = Path(__file__).parent
    text_files = list(current_dir.glob("*.txt"))

    if not text_files:
        print("No text files found in the directory.")
        return

    for txt_file in text_files:
        output_file = txt_file.with_suffix(".mp3")

        if output_file.exists():
            print(f"Skipping {txt_file.name} (MP3 already exists)")
            continue

        print(f"Processing {txt_file.name}...")

        text = txt_file.read_text(encoding="utf-8")
        processed_text = preprocess_text(text)

        await text_to_speech(processed_text, output_file)

        print(f"Created: {output_file.name}")

    print("All files processed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
