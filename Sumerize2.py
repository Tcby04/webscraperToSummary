import os
from transformers import pipeline
import time
from tqdm import tqdm

print(time)
start = time.time()

# using pipeline API for summarization task
summarization = pipeline("summarization")

# Specify the folder where your text files are located
folder_path = '/Volumes/@2TB/Programs/Programs  python/2023-09-22'  # Replace with the actual folder path

# Initialize an empty string to store the summarized text
summary_text = ""

# Define the encoding to use when reading files
file_encoding = 'utf-8'  # Change to the appropriate encoding if needed

# List of files in the folder
files = [filename for filename in os.listdir(folder_path) if filename.endswith('.txt') and not filename.startswith('._')]

# Create a tqdm progress bar
with tqdm(total=len(files)) as pbar:
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding=file_encoding) as file:
                text = file.read()

            # Summarize the file content and append it to summary_text
            summary = summarization(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            summary_text += summary + '\n\n'  # Add a newline between summarized files
        except UnicodeDecodeError:
            print(f"Skipping file {filename} due to decoding error.")

        pbar.update(1)  # Update the progress bar

print("Summary:",'\n\n', summary_text)

end = time.time()
print("Time taken:", end - start)
print(time)