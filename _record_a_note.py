
import asyncio
import edge_tts
import tkinter as tk
from tkinter import filedialog, messagebox
import os

VOICE = "en-US-JennyNeural"
RATE = "-10%"


async def speak(text, output_file):
    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate=RATE
    )

    await communicate.save(output_file)


def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a Text File",
        filetypes=[("Text Files", "*.txt")]
    )

    if not file_path:
        return

    try:
        # Read the text file
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        if not text.strip():
            messagebox.showwarning(
                "Empty File",
                "The selected text file is empty."
            )
            return

        # Create MP3 filename in the same folder
        output_file = os.path.splitext(file_path)[0] + ".mp3"

        status_label.config(text="Converting to MP3...")
        root.update()

        # Convert text to speech
        asyncio.run(speak(text, output_file))

        status_label.config(text="Conversion complete!")

        messagebox.showinfo(
            "Success",
            f"MP3 created successfully:\n{output_file}"
        )

    except Exception as e:
        status_label.config(text="Conversion failed.")
        messagebox.showerror("Error", str(e))


# Create Tkinter window
root = tk.Tk()
root.title("Text to MP3 Converter")
root.geometry("400x200")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Text File to MP3 Converter",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=20)

select_button = tk.Button(
    root,
    text="Select Text File",
    font=("Arial", 12),
    command=select_file,
    width=20,
    height=2
)
select_button.pack(pady=10)

status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 10)
)
status_label.pack(pady=10)

root.mainloop()
