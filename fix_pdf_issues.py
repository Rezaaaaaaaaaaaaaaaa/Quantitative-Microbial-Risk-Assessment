#!/usr/bin/env python3
"""
Extract content from the current PDF to understand what's in it and identify issues
"""

import pdfplumber
import os

def extract_pdf_content(pdf_path):
    """Extract and display the full content of the PDF."""
    if not os.path.exists(pdf_path):
        print(f"PDF file {pdf_path} not found")
        return

    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"CONTENT EXTRACTION FROM: {pdf_path}")
            print("=" * 80)

            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\n--- PAGE {page_num} ---")
                text = page.extract_text()
                if text:
                    print(text)
                else:
                    print("[No text content on this page]")

                # Check for tables
                tables = page.extract_tables()
                if tables:
                    print(f"\n[TABLES FOUND: {len(tables)}]")
                    for i, table in enumerate(tables):
                        print(f"\nTable {i+1}:")
                        for row in table:
                            print("  " + " | ".join([str(cell) if cell else "" for cell in row]))

    except Exception as e:
        print(f"Error extracting PDF content: {e}")

def main():
    """Extract content from the PDF to see what's actually in it."""
    pdf_path = "SIP_QMRA.pdf"
    extract_pdf_content(pdf_path)

if __name__ == "__main__":
    main()