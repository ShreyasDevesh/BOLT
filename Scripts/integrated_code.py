"""
PRIMARY REFERENCE : https://towardsdatascience.com/translate-long-pdf-reports-in-python-eab3be08ceb4
CAN ADD IF TIME PERMITS : https://www.ijraset.com/research-paper/automated-question-generator-using-nlp#:~:text=The%20input%20text%20is%20filtered,where%2C%20when%2C%20etc.)

library install commands:
- pip install nltk
- python -m nltk.downloader popular
- pip install pdfplumber
- pip install fpdf2
- pip install -U deep-translator

Deep translator has support for ChatGPT (docs:https://deep-translator.readthedocs.io/en/latest/README.html#when-you-should-use-it)

"""

#Necessary library imports
from functools import partial
import pdfplumber
from fpdf import FPDF
from deep_translator import GoogleTranslator
from nltk.tokenize import sent_tokenize

#Script imports
from translator import *
from pdf_reader import *

# Sample pdf document to be taken from website
pdf = pdfplumber.open("lect_1.pdf") 

# Writing to file
with pdfplumber.open("lect_1.pdf") as pdf:
    # Initialize FPDF file to write on
    fpdf = FPDF()
    fpdf.set_font("Helvetica", size = 7)

    # Treat each page individually
    for page in pdf.pages:
        # Extract Page
        extracted = extract(page)
        # Translate Page
        if extracted != "":
            # Translate paragraphs individually to keep breaks
            paragraphs = extracted.split("\n\n")
            translated = "\n\n".join([translate_extracted(paragraph) for paragraph in paragraphs])
        else:
            translated = extracted

        # Write Page
        fpdf.add_page()
        fpdf.multi_cell(w=0, h=5,
                    txt= translated.encode("latin-1",
                                            errors = "replace"
                                    ).decode("latin-1"))
# Save all FPDF pages
fpdf.output("lect_1_tr.pdf")
