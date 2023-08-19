import os
from PyPDF2 import PdfReader
import tiktoken

# Get the path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory containing the current file
current_dir_path = os.path.dirname(current_file_path)

# Construct the path to the instructions folder relative to the current file
folder_path = os.path.join(current_dir_path, "instructions")


def extract(folder_path):
    pdf_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(folder_path, file))
    return pdf_files


pdf_files = extract(folder_path)


def split_text_into_chunks(text, chunk_size=400):
    chunks = []
    token_count = 0
    current_chunk = ""

    # Tokenize the text using tiktoken and split into chunks
    for token in tiktoken.tokenize(text):
        token_count += 1
        if token_count > chunk_size:
            chunks.append(current_chunk)
            current_chunk = ""
            token_count = 0
        current_chunk += token + " "

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def load(pdf_files, chunk_size=400):
    instructions = {}

    for file in pdf_files:
        try:
            pdf_reader = PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            # Split text into chunks of approximately 400 tokens using tiktoken
            chunks = split_text_into_chunks(text, chunk_size)

            file_name = os.path.basename(file)
            instructions[file_name] = chunks
        except Exception as e:
            print(f"Error processing {file}: {e}")
    return instructions


# Call the function and get the text dictionary
chunk_size = 400  # Set the desired chunk size
pdf_text_dict = load(pdf_files, chunk_size)

# Print the dictionary
for file_name, chunks in pdf_text_dict.items():
    print(f"File: {file_name}")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}: {chunk}\n")
