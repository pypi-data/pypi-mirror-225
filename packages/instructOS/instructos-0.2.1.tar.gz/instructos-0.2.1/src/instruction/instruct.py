# List of instruction in pdf file and their corresponding instruction in the source code

# define a function to get pdf files from a folder and store them in a python list with their file paths.
import os


# Get the path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory containing the current file
current_dir_path = os.path.dirname(current_file_path)

# Construct the path to the instructions folder relative to the current file
folder_path = os.path.join(current_dir_path, "instructions")
# print(folder_path)

# folder_path = (
#     "C:/Users/FLOW KEEY/Documents/GitHub/instruction/src/instruction/instructions"
# )


def extract(folder_path):
    pdf_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(folder_path, file))
    print(pdf_files)
    # return pdf_files


extract(folder_path)
