import re
import json
from pathlib import Path
from PyPDF2 import PdfReader
from numpy import number

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    reader = PdfReader(str(file_path))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
    
def extract_parent_title(full_text, parent_number):
    parent_title_match=re.search(rf"^{parent_number}\s+(.+)", full_text, re.MULTILINE)
    return parent_title_match.group(1).strip() if parent_title_match else ""

def parse_sections(text):
    heading_pattern=re.compile(r"^(\d+(?:\.\d+)*)\s+([A-Za-z].+)", re.MULTILINE)
    sections=[]

    for match in heading_pattern.finditer(text):
        number=match.group(1)
        title=match.group(2).strip()
        start_index=match.start()

        if "." in number:
            # Subsection
            parent=number.split(".")[0]
            parent_title=extract_parent_title(text, parent)
            sections.append({
                "section": parent_title,
                "subsection": f"{number} {title}",
                "start": start_index
            })
        else:
            # Only main section
            sections.append({
                "section": title,
                "start": start_index
            })

    return sections

def find_abstract_section(text):
    abstract_match=re.search(r"\bAbstract\b",text)  
    if abstract_match:
        return {
            "section": "Abstract",
            "start": abstract_match.start()
        }
    return None


def extract_pdf_sections(full_text):
    sections=parse_sections(full_text)
    abstract=find_abstract_section(full_text)
    if abstract:
        sections.insert(0, abstract)
    return sections