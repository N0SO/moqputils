#!/usr/bin/env python
"""
Update History - See __init__.py 
"""

from pypdf import PdfReader, PdfWriter
from __init__ import VERSION
import os, sys, csv


class htmlCerts():

    def __init__(self):
        """
        Splits a PDF file into individual pages, saving each page as a new PDF.

        Args:
            input_pdf_path (str): The path to the input PDF file.
            output_fname (str): file name for output PDF file.
            page_list (list): List of page numbers (1 based) to extract.
            output_folder (str): The folder where the split pages will be saved.

        # Example usage:
        # Assuming 'your_document.pdf' is in the same directory as your script
        # split_pdf_into_pages("missouri-2025-merged.pdf")
        """
        self.TABLESTARTS = \
"""
<table>
<tr><th>STATION</th><th>OPERATORS</th><th>AWARD DOWNLOAD LINK</th></tr>
"""

        self.TABLEROWS = \
"""
<tr><td>{}</td><td>{}</td><td><a href="./downloads/{}">{} DOWNLOAD</a></td></tr> 
"""

        self.TABLESTARTC = \
"""
<table>
<tr><th>AWARD</th><th>STATION</th><th>OPERATORS</th><th>AWARD DOWNLOAD LINK</th></tr>
"""

        self.TABLEROWC = \
"""
<tr><td>{}</td><td>{}</td><td>{}</td><td><a href="./{}">{} DOWNLOAD</a></td></tr> 
"""


    def split_pdf_into_pages(self,
			    input_pdf_path,
                            output_fname, 
                            page_list=[1], 
                            output_folder="output_pages"):
        reader = PdfReader(input_pdf_path)
        num_pages = len(page_list)

        # Create the output folder if it doesn't exist
        # import os
        os.makedirs(output_folder, exist_ok=True)

        for i in page_list:
            writer = PdfWriter()
            writer.add_page(reader.pages[i-1])

            output_filename = os.path.join(output_folder, output_fname)
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)


    def find_pages(self, pdf_file, search_term):
        reader = PdfReader(pdf_file)
        found_pages = []

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if search_term.lower() in text.lower():
                found_pages.append(page_num + 1) # Page numbers are 1-indexed
        return found_pages

    def Appmain(self, call_list, file_path):
        print(self.TABLESTARTS)
        """
        Open the .csv file that contains list of callsigns
        """
        with open(call_list, mode='r', newline='') as fname:
            csv_reader = csv.DictReader(fname, delimiter='\t')
            for row in csv_reader:
                if (row['OPERATORS'] == None or
                        row['OPERATORS'].strip() == '' or
                        len(row['OPERATORS']) == 0 ):
                    #Single-op - look for station call in text
                    search_term = row['CALL']
                else:
                    """
                    Multi-op - look for op name in text 
                    search for op name.
                    """
                    search_term = row['NAME'].strip()
                #Extract the one file for this line.
                pages = self.find_pages( pdf_file=file_path, 
                            search_term=search_term)
                if pages:
                    #print(f"Extracting {row['FILE']}, page {pages} for {row['CALL']} op {search_term}") 
                    self.split_pdf_into_pages(   file_path, 
                                    row['FILE'],
                                    page_list=[pages[0]], 
                                    output_folder='downloads')
                    print(self.TABLEROWS.format(\
                          row['CALL'],
                          row['OPERATORS'],
                          row['FILE'],
                          row['FILE']))

        print('</table>') 


class htmlAwards(htmlCerts):
    def __init__(self):
        self.TABLESTARTS = \
"""
<table>
<tr><th>AWARD</th><th>STATION</th><th>OPERATORS</th><th>AWARD DOWNLOAD LINK</th></tr>
"""

        self.TABLEROWS = \
"""
<tr><td>{}</td><td>{}</td><td>{}</td><td><a href="./downloads/{}">{}</a></td></tr> 
"""

        self.TABLESTARTC = \
"""
<table>
<tr><th>AWARD</th><th>STATION</th><th>OPERATORS</th><th>AWARD DOWNLOAD LINK</th></tr>
"""

        self.TABLEROWC = \
"""
<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><a href='downloads./{}'>{}</a></td></tr> 
"""
    def Appmain(self, call_list, file_path):
        print(self.TABLESTARTS)
        """
        Open the .csv file that contains list of callsigns
        """
        with open(call_list, mode='r', newline='') as fname:
            csv_reader = csv.DictReader(fname, delimiter='\t')
            certfile = 'award_'
            cf_index = 1
            for row in csv_reader:
                thisCertfile = f'certfile{cf_index}.pdf'
                self.split_pdf_into_pages(\
                                    file_path, 
                                    thisCertfile,
                                    page_list=[cf_index], 
                                    output_folder='downloads')
                awardplace = f"{row['RANK']} {row['AWARD']}"                     
                print(self.TABLEROWS.format(\
                          awardplace,
                          row['STATION'],
                          row['OPERATORS'],
                          thisCertfile,
                          row['NAME']))
                cf_index += 1

        print('</table>') 
    
