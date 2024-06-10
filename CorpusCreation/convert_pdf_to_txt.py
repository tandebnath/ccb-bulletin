import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    doc.close()
    return text

def save_text_to_txt(text, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

input_folder = 'PDFs'  
output_folder = 'TXTs' 

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith('.pdf'):
        pdf_path = os.path.join(input_folder, file_name)
        txt_output_path = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.txt')
        
        # Extract text from PDF and save it as a text file
        extracted_text = extract_text_from_pdf(pdf_path)
        save_text_to_txt(extracted_text, txt_output_path)
        print(f'Text extracted from {file_name} and saved to {txt_output_path}')
