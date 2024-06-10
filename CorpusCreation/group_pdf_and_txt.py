import os
import shutil

pdf_folder = 'PDFs'
txt_folder = 'TXTs'
grouped_folder = 'Grouped'

# Create the Grouped folder if it doesn't exist
os.makedirs(grouped_folder, exist_ok=True)

# Get the list of PDF files
pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith('.pdf')]

for pdf_file in pdf_files:
    base_name = os.path.splitext(pdf_file)[0]
    
    # Corresponding txt file name
    txt_file = base_name + '.txt'
    
    # Check if the corresponding txt file exists
    if txt_file in os.listdir(txt_folder):
        # Path for the new folder in 'Grouped' directory
        grouped_subfolder = os.path.join(grouped_folder, base_name)
        
        # Create the subfolder in 'Grouped' directory
        os.makedirs(grouped_subfolder, exist_ok=True)
        
        # Paths for the source PDF and TXT files
        src_pdf_path = os.path.join(pdf_folder, pdf_file)
        src_txt_path = os.path.join(txt_folder, txt_file)
        
        # Paths for the destination PDF and TXT files
        dest_pdf_path = os.path.join(grouped_subfolder, pdf_file)
        dest_txt_path = os.path.join(grouped_subfolder, txt_file)
        
        # Move the PDF and TXT files to the new folder
        shutil.move(src_pdf_path, dest_pdf_path)
        shutil.move(src_txt_path, dest_txt_path)
        print(f"Grouped: {pdf_file} and {txt_file} into {grouped_subfolder}")
    else:
        print(f"Warning: Corresponding TXT file for {pdf_file} not found.")
