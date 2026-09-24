import asyncio
import edge_tts

async def speak(text, output_file):
    voice = "en-US-JennyNeural"

    communicate = edge_tts.Communicate(
        text,
        voice,
        rate="-10%"
    )

    await communicate.save(output_file)

asyncio.run(speak("Hello, this is your voice note.", "test.mp3"))
