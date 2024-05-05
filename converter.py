import os
import sys

import PyPDF2

def convert_pdf_to_txt(pdf_folder, txt_folder):
    # Get all files in the folder
    pdf_files = os.listdir(pdf_folder)
    
    # Iterate through all files
    for pdf_file in pdf_files:
        if os.path.exists(f'{txt_folder}/{pdf_file.replace(".pdf", ".txt")}'):
            print(f'{pdf_file} is already converted. Skipping...')
            continue
        # Convert one file at a time
        convert_single_pdf_to_txt(pdf_folder, txt_folder, pdf_file)

def convert_single_pdf_to_txt(pdf_folder, txt_folder, pdf_file):

    print(f'Converting {pdf_file}...')
    # Open the PDF file
    pdf_path = os.path.join(pdf_folder, pdf_file)
    pdf = open(pdf_path, 'rb')
    
    # Create a PDF file reader
    pdf_reader = PyPDF2.PdfReader(pdf)
    
    # Create a text file
    txt_file = pdf_file.replace('.pdf', '.txt')
    txt_path = txt_folder + '/' + txt_file
    txt = open(txt_path, 'w', encoding='utf-8')
    
    # Iterate through all pages
    for page_num in range(len(pdf_reader.pages)):
        # Get the page
        page = pdf_reader.pages[page_num]
        
        # Extract the text
        text = page.extract_text()
        
        # Write the text to the text file
        txt.write(text)
    
    # Close the text file
    txt.close()
    
    # Close the PDF file
    pdf.close()

pdf_folder = 'assets/original/pdf'
txt_folder = 'assets/converted/txt'
convert_pdf_to_txt(pdf_folder, txt_folder)
