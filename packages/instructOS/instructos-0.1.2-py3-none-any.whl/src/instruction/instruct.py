# List of instruction in pdf file and their corresponding instruction in the source code

# define a function to get pdf files from a folder and store them in a python list with their file paths.

def get_pdf_files(folder_path):
    pdf_files = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(folder_path, file))
    return pdf_files