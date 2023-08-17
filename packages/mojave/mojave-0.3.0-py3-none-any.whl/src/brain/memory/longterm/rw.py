import extract
import PyPDF2
import os
from extract import pdf_files

# print(pdf_files)
instructs = extract.pdf_files
# print(instructs)

# define a function to iterate through the list of pdf files and extract the text from each file, storing them in a dictionary of key value pairs where the key is the file name and the value is the text extracted from the file.


def write(instructs):
    instructions = {}  # Dictionary to store file name -> extracted text pairs

    for file in instructs:
        try:
            # Open the PDF file
            with open(file, "rb") as pdf:
                pdf_reader = PyPDF2.PdfFileReader(pdf)

                # Extract text from each page
                text = ""
                for page_num in range(pdf_reader.numPages):
                    page = pdf_reader.getPage(page_num)
                    text += page.extractText()

                # Store extracted text in the dictionary
                file_name = os.path.basename(file)
                instructions[file_name] = text

        except Exception as e:
            print(f"Error processing {file}: {e}")

    return instructions


# Call the function and get the text dictionary
pdf_text_dict = write(instructs)

# Print the dictionary
for file_name, text in pdf_text_dict.items():
    print(f"File: {file_name}\nText: {text}\n")
