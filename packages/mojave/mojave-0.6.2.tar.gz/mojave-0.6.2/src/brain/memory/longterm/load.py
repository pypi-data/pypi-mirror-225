# define a function to get pdf files from a folder and store them in a python list with their file paths.
# define a function to extract text from pdf files and store them in a dictionary with their file names as keys and extracted text as values.
import os
from PyPDF2 import PdfReader

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


def load(pdf_files):
    instructions = {}  # Dictionary to store file name -> extracted text pairs

    for file in pdf_files:
        try:
            # Open the PDF file using PdfReader
            pdf_reader = PdfReader(file)

            # Extract text from each page
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            # Store extracted text in the dictionary
            file_name = os.path.basename(file)
            instructions[file_name] = text

        except Exception as e:
            print(f"Error processing {file}: {e}")

    return instructions


# Call the function and get the text dictionary
pdf_text_dict = load(pdf_files)
# print(pdf_text_dict)

# Print the dictionary
for file_name, text in pdf_text_dict.items():
    print(f"File: {file_name}\nText: {text}\n")
