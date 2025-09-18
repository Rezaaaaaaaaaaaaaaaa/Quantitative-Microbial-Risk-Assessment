#!/usr/bin/env python3
"""
Check PDF formatting and extract content to identify any issues
"""

import PyPDF2
import pdfplumber
import os

def check_pdf_formatting(pdf_path):
    """Check PDF formatting and extract content for review."""
    if not os.path.exists(pdf_path):
        print(f"PDF file {pdf_path} not found")
        return

    print(f"Checking PDF formatting: {pdf_path}")
    print("=" * 60)

    # Check file size
    file_size = os.path.getsize(pdf_path) / 1024  # KB
    print(f"File size: {file_size:.1f} KB")

    try:
        # Use pdfplumber for better text extraction
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total pages: {len(pdf.pages)}")
            print("\nPage-by-page analysis:")
            print("-" * 40)

            for page_num, page in enumerate(pdf.pages, 1):
                print(f"\nPage {page_num}:")

                # Get page dimensions
                print(f"  Dimensions: {page.width:.1f} x {page.height:.1f} points")

                # Extract text
                text = page.extract_text()
                if text:
                    lines = text.split('\n')
                    print(f"  Text lines: {len(lines)}")
                    print(f"  Characters: {len(text)}")

                    # Show first few lines for content verification
                    print("  Content preview:")
                    for i, line in enumerate(lines[:5]):
                        if line.strip():
                            print(f"    {i+1}: {line.strip()[:80]}...")
                else:
                    print("  ⚠️  No text found on this page")

                # Check for tables
                tables = page.extract_tables()
                if tables:
                    print(f"  Tables found: {len(tables)}")
                    for i, table in enumerate(tables):
                        print(f"    Table {i+1}: {len(table)} rows x {len(table[0]) if table else 0} columns")

                # Check for images
                if hasattr(page, 'images'):
                    images = page.images
                    if images:
                        print(f"  Images found: {len(images)}")

        # Extract full text for content analysis
        print("\n" + "=" * 60)
        print("CONTENT ANALYSIS")
        print("=" * 60)

        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"

            # Analyze content structure
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]

            print(f"Total text lines: {len(lines)}")
            print(f"Total characters: {len(full_text)}")

            # Look for key sections
            sections_found = []
            key_sections = [
                'Project Overview', 'Work programme', 'Technical approach',
                'System design', 'Budget', 'Expected impact'
            ]

            for section in key_sections:
                if any(section.lower() in line.lower() for line in lines):
                    sections_found.append(section)

            print(f"Key sections found: {', '.join(sections_found)}")

            # Check for potential formatting issues
            formatting_issues = []

            # Check for very long lines (might indicate wrapping issues)
            long_lines = [line for line in lines if len(line) > 150]
            if long_lines:
                formatting_issues.append(f"{len(long_lines)} very long lines (>150 chars)")

            # Check for repeated characters (might indicate formatting artifacts)
            repeated_chars = [line for line in lines if any(char * 5 in line for char in 'abcdefghijklmnopqrstuvwxyz')]
            if repeated_chars:
                formatting_issues.append(f"{len(repeated_chars)} lines with repeated characters")

            # Check for missing spaces (concatenated words)
            concatenated = [line for line in lines if any(
                word[0].islower() and word[1:].isupper() for word in line.split() if len(word) > 1
            )]
            if concatenated:
                formatting_issues.append(f"{len(concatenated)} lines with potential concatenated words")

            if formatting_issues:
                print("\n⚠️  POTENTIAL FORMATTING ISSUES:")
                for issue in formatting_issues:
                    print(f"  - {issue}")
            else:
                print("\n✅ No obvious formatting issues detected")

            # Show document structure
            print("\nDOCUMENT STRUCTURE:")
            headings = []
            for line in lines[:50]:  # Check first 50 lines for structure
                if any(keyword in line.lower() for keyword in ['overview', 'programme', 'technical', 'budget', 'impact']):
                    headings.append(line)

            for heading in headings:
                print(f"  • {heading}")

    except Exception as e:
        print(f"Error analyzing PDF: {e}")

def main():
    """Main function to check PDF formatting."""
    pdf_path = "SIP_QMRA.pdf"
    check_pdf_formatting(pdf_path)

if __name__ == "__main__":
    main()