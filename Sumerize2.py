import warnings
from transformers import pipeline
import os
from tqdm import tqdm


print('Starting Summarization....')

# Define the model and its configuration
model_name = "sshleifer/distilbart-cnn-12-6"  # Replace with the model name you want to use

# Create the summarization pipeline with your specified model
summarization = pipeline("summarization", model=model_name)

# Specify the name of the file containing articles
file_name = 'Articles.txt'  # Replace with the actual filename

# Define the encoding to use when reading the file
file_encoding = 'utf-8'  # Change to the appropriate encoding if needed

# Maximum sequence length for chunking
max_seq_length = 1024  # Maximum sequence length for the model

# Specify the output file name
output_file_name = 'Summarized_Articles.txt'  # Replace with your desired output file name

try:
    # Check if the file exists
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding=file_encoding) as file:
            lines = file.readlines()

        # Initialize variables to store article titles and content
        article_titles = []
        article_contents = []
        current_article = ""

        # Initialize a tqdm progress bar with total size as the unit
        with tqdm(total=len(lines), unit='line', dynamic_ncols=True) as pbar:
            # Iterate through the lines in the file
            for line in lines:
                if line.startswith("Title:"):
                    # If a line starts with "Title:", it indicates the start of a new article
                    if current_article:
                        if len(current_article) > max_seq_length:
                            # Chunk the current article into segments
                            text_chunks = [current_article[i:i+max_seq_length] for i in range(0, len(current_article), max_seq_length)]
                            chunked_summaries = []

                            # Summarize each chunk
                            for chunk in text_chunks:
                                with warnings.catch_warnings():
                                    warnings.filterwarnings("ignore", category=UserWarning)  # Ignore specific warnings
                                    summary = summarization(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
                                chunked_summaries.append(summary)

                            # Combine chunked summaries
                            combined_summary = '\n'.join(chunked_summaries)
                            article_titles.append(current_title)
                            article_contents.append(combined_summary)
                        else:
                            # Summarize the current article as is
                            with warnings.catch_warnings():
                                warnings.filterwarnings("ignore", category=UserWarning)  # Ignore specific warnings
                                summary = summarization(current_article, max_length=300, min_length=30, do_sample=False)[0]['summary_text']
                            article_titles.append(current_title)
                            article_contents.append(summary)

                    # Extract the title for the new article
                    current_title = line[len("Title:"):].strip()
                    current_article = ""
                else:
                    # Append the line to the current article content
                    current_article += line

                # Update the progress bar
                pbar.update(1)

        # Write the summaries to an output file
        with open(output_file_name, 'w', encoding=file_encoding) as output_file:
            for i in range(len(article_titles)):
                output_file.write(f"Title: {article_titles[i]}\n")
                output_file.write("Summary:\n")
                output_file.write(article_contents[i] + "\n\n")

        print("Articles have been Sumerized")

    else:
        print(f"File '{file_name}' not found in the current directory.")

except UnicodeDecodeError:
    print(f"Skipping file '{file_name}' due to decoding error.")