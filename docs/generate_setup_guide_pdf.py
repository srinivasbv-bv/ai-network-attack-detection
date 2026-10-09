import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

def create_setup_guide_pdf():
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Complete_Project_Setup_Guide.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=0.5*inch, leftMargin=0.5*inch,
        topMargin=0.5*inch, bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        alignment=TA_CENTER,
        spaceAfter=10
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0284c7"),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6,
        alignment=TA_LEFT
    )
    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e293b")
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []

    # Title Banner
    story.append(Paragraph("AI POWERED THREAT DETECTION SYSTEM", title_style))
    story.append(Paragraph("Complete Project Setup & Deployment Guide for External Users", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=15))

    # Executive Overview
    story.append(Paragraph("1. Purpose of This Setup Guide", h1_style))
    story.append(Paragraph(
        "This document provides step-by-step instructions to download, configure, run, and troubleshoot the <b>AI Powered Threat Detection System</b> on any standard Windows, macOS, or Linux computer. It is designed so that a student, evaluator, external reviewer, or teammate receiving the project zip folder via Google Drive can run the complete application seamlessly without prior technical knowledge.",
        body_style
    ))

    # Minimum & Recommended System Requirements
    story.append(Paragraph("2. System Requirements", h1_style))
    sys_req_data = [
        [Paragraph("Resource / Requirement", table_header_style), Paragraph("Minimum Specs", table_header_style), Paragraph("Recommended Specs", table_header_style)],
        [Paragraph("Operating System", table_cell_style), Paragraph("Windows 10/11, macOS 11+, or Ubuntu 20.04+", table_cell_style), Paragraph("Windows 11 or Ubuntu 22.04 LTS", table_cell_style)],
        [Paragraph("Processor (CPU)", table_cell_style), Paragraph("Dual-Core 2.0 GHz", table_cell_style), Paragraph("Quad-Core 2.5 GHz or higher", table_cell_style)],
        [Paragraph("System Memory (RAM)", table_cell_style), Paragraph("4 GB RAM", table_cell_style), Paragraph("8 GB RAM or higher", table_cell_style)],
        [Paragraph("Disk Storage", table_cell_style), Paragraph("500 MB free space", table_cell_style), Paragraph("1 GB free SSD space", table_cell_style)],
        [Paragraph("Python Environment", table_cell_style), Paragraph("Python 3.9, 3.10, 3.11, or 3.12", table_cell_style), Paragraph("Python 3.10 or 3.11", table_cell_style)],
        [Paragraph("Web Browser", table_cell_style), Paragraph("Chrome, Edge, Firefox, or Safari", table_cell_style), Paragraph("Google Chrome (Latest)", table_cell_style)]
    ]
    t_sys = Table(sys_req_data, colWidths=[130, 180, 194])
    t_sys.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_sys)
    story.append(Spacer(1, 10))

    # Step-by-Step Installation
    story.append(Paragraph("3. Step-by-Step Project Setup Instructions", h1_style))

    story.append(Paragraph("Step 1: Download & Extract Project Files from Google Drive", h2_style))
    story.append(Paragraph("• Open the shared Google Drive folder link in your web browser.", bullet_style))
    story.append(Paragraph("• Click the <b>Download All</b> button (or right-click the zip archive <code>ai_network_attack_detection.zip</code> and select Download).", bullet_style))
    story.append(Paragraph("• Once downloaded, extract the zip file to a clean local directory (e.g. <code>C:\\Projects\\ai_network_attack_detection</code> on Windows or <code>~/projects/ai_network_attack_detection</code> on macOS/Linux).", bullet_style))

    story.append(Paragraph("Step 2: Install Python (If Not Already Installed)", h2_style))
    story.append(Paragraph("• Download Python 3.10+ from official website: <b>https://www.python.org/downloads/</b>", bullet_style))
    story.append(Paragraph("• <b>CRITICAL STEP (Windows):</b> During installation, check the box that says <b>'Add Python to PATH'</b> before clicking Install Now.", bullet_style))
    story.append(Paragraph("• Verify installation by opening Terminal / PowerShell and running:", bullet_style))
    story.append(Paragraph("python --version", code_style))

    story.append(Paragraph("Step 3: Open Terminal & Navigate to Project Folder", h2_style))
    story.append(Paragraph("• Open Command Prompt, PowerShell, or Terminal.", bullet_style))
    story.append(Paragraph("• Navigate to the extracted project folder using the <code>cd</code> command:", bullet_style))
    story.append(Paragraph("cd C:\\Projects\\ai_network_attack_detection", code_style))

    story.append(Paragraph("Step 4: Create & Activate Virtual Environment (Recommended)", h2_style))
    story.append(Paragraph("• Creating a Python virtual environment ensures package dependencies do not conflict with existing software:", bullet_style))
    story.append(Paragraph("# On Windows:\npython -m venv venv\nvenv\\Scripts\\activate\n\n# On macOS / Linux:\npython3 -m venv venv\nsource venv/bin/activate", code_style))

    story.append(Paragraph("Step 5: Install Project Dependencies", h2_style))
    story.append(Paragraph("• Install all required libraries using <code>pip</code>:", bullet_style))
    story.append(Paragraph("pip install -r requirements.txt", code_style))
    story.append(Paragraph("<i>Required packages installed automatically:</i> Flask, scikit-learn, joblib, numpy, pandas, matplotlib, reportlab, python-pptx, scapy.", body_style))

    story.append(Paragraph("Step 6: Launch the Master Application", h2_style))
    story.append(Paragraph("• Execute the single master entrypoint script:", bullet_style))
    story.append(Paragraph("python main.py", code_style))
    story.append(Paragraph("• The script performs auto-verification: It checks for pre-trained model weights (<code>dl_flow_model.joblib</code> and <code>rf_arp_model.joblib</code>). If weights are missing, it automatically generates synthetic training datasets and trains models in ~10 seconds.", body_style))

    story.append(Paragraph("Step 7: Access the SOC Analyst Web Console", h2_style))
    story.append(Paragraph("• Open your web browser (Chrome recommended) and navigate to:", bullet_style))
    story.append(Paragraph("http://127.0.0.1:5000", code_style))
    story.append(Paragraph("• The live dashboard will load with continuous simulated network traffic feed, interactive Attack Vector Simulator, live AI predictions, threat score graph, and security events table.", body_style))

    story.append(Spacer(1, 10))

    # Troubleshooting Section
    story.append(Paragraph("4. Common Errors & Troubleshooting Solutions", h1_style))
    err_data = [
        [Paragraph("Error Description", table_header_style), Paragraph("Root Cause", table_header_style), Paragraph("Resolution / Fix", table_header_style)],
        [
            Paragraph("<code>'python' is not recognized as an internal command</code>", table_cell_style),
            Paragraph("Python was installed without adding Python executable to OS PATH variable.", table_cell_style),
            Paragraph("Re-run Python installer, select 'Modify', and check 'Add Python to environment variables'. Or use <code>py main.py</code>.", table_cell_style)
        ],
        [
            Paragraph("<code>ModuleNotFoundError: No module named 'flask'</code>", table_cell_style),
            Paragraph("Dependencies were not installed into active Python environment.", table_cell_style),
            Paragraph("Ensure virtual environment is activated and run <code>pip install -r requirements.txt</code>.", table_cell_style)
        ],
        [
            Paragraph("<code>OSError: [Errno 98] Address already in use: 5000</code>", table_cell_style),
            Paragraph("Port 5000 is occupied by another local server (e.g. AirPlay on macOS or existing Flask app).", table_cell_style),
            Paragraph("Kill process using port 5000 or edit <code>web/app.py</code> to change port to <code>port=5050</code>.", table_cell_style)
        ],
        [
            Paragraph("<code>FileNotFoundError: dl_flow_model.joblib missing</code>", table_cell_style),
            Paragraph("Model files deleted or corrupt.", table_cell_style),
            Paragraph("Run <code>python models/train_models.py</code> to re-generate datasets and retrain weights automatically.", table_cell_style)
        ]
    ]
    t_err = Table(err_data, colWidths=[140, 160, 204])
    t_err.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_err)

    doc.build(story)
    print(f"[PDF Generator] Successfully generated: {pdf_path}")

if __name__ == "__main__":
    create_setup_guide_pdf()
