"""
Generate PDF version of QMRA User Manual
Converts USER_MANUAL.md to professional PDF document
"""

import os
from pathlib import Path
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.platypus import ListFlowable, ListItem
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  ReportLab not installed. Install with: pip install reportlab")

def convert_markdown_to_pdf(md_file, pdf_file):
    """Convert markdown user manual to PDF."""

    if not REPORTLAB_AVAILABLE:
        print("❌ Cannot generate PDF - ReportLab not installed")
        print("   Install with: pip install reportlab")
        return False

    # Read markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create PDF
    doc = SimpleDocTemplate(
        str(pdf_file),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4e79'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#666666'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4e79'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d7dd2'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#333333'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#d63384'),
        backColor=colors.HexColor('#f8f9fa'),
        spaceAfter=6
    )

    # Add title page
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph("NIWA QMRA Assessment Toolkit", title_style))
    elements.append(Paragraph("User Manual", subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("Professional Quantitative Microbial Risk Assessment Software", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Version 2.0", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("NIWA Earth Sciences, New Zealand", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    elements.append(PageBreak())

    # Process markdown content
    lines = content.split('\n')
    i = 0
    in_code_block = False
    code_lines = []
    in_list = False
    list_items = []

    while i < len(lines):
        line = lines[i].strip()

        # Skip title (already added to title page)
        if i < 10 and line.startswith('#'):
            i += 1
            continue

        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                # End code block
                code_text = '\n'.join(code_lines)
                elements.append(Paragraph(f"<font face='Courier' size='9'>{code_text}</font>", code_style))
                elements.append(Spacer(1, 0.1*inch))
                code_lines = []
                in_code_block = False
            else:
                # Start code block
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            code_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue

        # Headers
        if line.startswith('# '):
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False
            elements.append(Paragraph(line[2:], h1_style))
            elements.append(Spacer(1, 0.1*inch))

        elif line.startswith('## '):
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False
            elements.append(Paragraph(line[3:], h2_style))
            elements.append(Spacer(1, 0.1*inch))

        elif line.startswith('### '):
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False
            elements.append(Paragraph(line[4:], h3_style))
            elements.append(Spacer(1, 0.05*inch))

        elif line.startswith('#### '):
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False
            elements.append(Paragraph(f"<b>{line[5:]}</b>", body_style))
            elements.append(Spacer(1, 0.05*inch))

        # Horizontal rules
        elif line.startswith('---'):
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Table([['']], colWidths=[6.5*inch], rowHeights=[2],
                                style=TableStyle([('LINEABOVE', (0,0), (-1,-1), 1, colors.grey)])))
            elements.append(Spacer(1, 0.1*inch))

        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            in_list = True
            list_items.append(ListItem(Paragraph(line[2:], body_style)))

        elif line.startswith('  - ') or line.startswith('  * '):
            in_list = True
            list_items.append(ListItem(Paragraph(line[4:], body_style), leftIndent=20))

        # Numbered lists
        elif len(line) > 2 and line[0].isdigit() and line[1:3] in ['. ', ') ']:
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False
            elements.append(Paragraph(line, body_style))

        # Bold/Italic inline code
        elif line:
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False

            # Process inline formatting
            processed_line = line
            processed_line = processed_line.replace('**', '<b>').replace('**', '</b>')
            processed_line = processed_line.replace('`', '<font face="Courier" color="#d63384">')
            processed_line = processed_line.replace('`', '</font>')

            elements.append(Paragraph(processed_line, body_style))

        else:
            # Empty line
            if in_list:
                elements.append(ListFlowable(list_items, bulletType='bullet'))
                list_items = []
                in_list = False
            elements.append(Spacer(1, 0.1*inch))

        i += 1

    # Add footer with page numbers
    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(7.5*inch, 0.5*inch, text)
        canvas.drawString(1*inch, 0.5*inch, "NIWA QMRA Toolkit - User Manual v2.0")
        canvas.restoreState()

    # Build PDF
    try:
        doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
        print(f"✅ PDF generated successfully: {pdf_file}")
        return True
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

def main():
    """Main function to generate PDF manual."""

    # Paths
    base_dir = Path(__file__).parent
    md_file = base_dir / "docs" / "USER_MANUAL.md"
    pdf_file = base_dir / "docs" / "USER_MANUAL.pdf"

    # Check if markdown file exists
    if not md_file.exists():
        print(f"❌ User manual not found: {md_file}")
        return

    print("📄 Generating PDF version of User Manual...")
    print(f"   Input:  {md_file}")
    print(f"   Output: {pdf_file}")
    print()

    # Convert to PDF
    success = convert_markdown_to_pdf(md_file, pdf_file)

    if success:
        print()
        print("=" * 60)
        print("✅ PDF User Manual Generated Successfully!")
        print("=" * 60)
        print(f"   Location: {pdf_file}")
        print(f"   Size: {pdf_file.stat().st_size / 1024:.1f} KB")
        print()
        print("📧 Distribution Options:")
        print("   - Email to users")
        print("   - Upload to SharePoint/intranet")
        print("   - Include in project deliverables")
        print("   - Print for offline reference")
    else:
        print()
        print("=" * 60)
        print("❌ PDF Generation Failed")
        print("=" * 60)
        print("   Please check error messages above")
        print()
        print("💡 Alternative: Use the Markdown version")
        print(f"   {md_file}")

if __name__ == "__main__":
    main()
