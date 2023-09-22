from transformers import pipeline
import time
from tqdm import tqdm  # Import tqdm for the progress bar

start = time.time()

# using pipeline API for summarization task
summarization = pipeline("summarization")

# Read text from a file
with open('scraped_text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Split the text into paragraphs (assuming paragraphs are separated by empty lines)
paragraphs = text.split('\n\n')

# Initialize an empty list to store the summarized paragraphs
summary_paragraphs = []

# Create a tqdm progress bar
with tqdm(total=len(paragraphs)) as pbar:
    for paragraph in paragraphs:
        summary = summarization(paragraph, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        summary_paragraphs.append(summary)
        pbar.update(1)  # Update the progress bar

# Combine the summarized paragraphs into a single string
summary_text = '\n\n'.join(summary_paragraphs)

print("Summary:", summary_text)

end = time.time()
print("Time taken:", end - start)
