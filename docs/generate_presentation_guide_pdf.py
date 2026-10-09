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

def create_presentation_guide_pdf():
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Project_Presentation_Guide.pdf")
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
    script_style = ParagraphStyle(
        'ScriptBlock',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#0284c7"),
        borderWidth=0.5,
        borderPadding=8,
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
    story.append(Paragraph("College Viva & Professional Presentation Guide with Speaker Script", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=15))

    # Introduction
    story.append(Paragraph("1. Presentation Strategy & Viva Overview", h1_style))
    story.append(Paragraph(
        "This guide equips you to present the <b>AI Powered Threat Detection System</b> during a final-year viva voce, academic evaluation, or professional technical presentation. It includes a slide-by-slide verbal presentation script, live demonstration steps, and defensible answers for anticipated examiner questions.",
        body_style
    ))

    # Slide Script Table
    story.append(Paragraph("2. Slide-by-Slide Presentation Script", h1_style))

    slide_data = [
        [Paragraph("Slide # & Topic", table_header_style), Paragraph("Key Slide Visuals / Points", table_header_style), Paragraph("Presenter Script (What to Say)", table_header_style)],
        [
            Paragraph("<b>Slide 1: Title & Overview</b>", table_cell_style),
            Paragraph("Project Title, Student Name, Guide Name, KSOU / University Logo", table_cell_style),
            Paragraph("<i>'Respected Examiners, good morning/afternoon. Today I present my final year project titled AI POWERED THREAT DETECTION SYSTEM. This system combines Deep Learning and Machine Learning to detect cyber-attacks in real time.'</i>", script_style)
        ],
        [
            Paragraph("<b>Slide 2: Problem Statement</b>", table_cell_style),
            Paragraph("Traditional IDS weaknesses, high False Positive rate, lack of zero-day coverage", table_cell_style),
            Paragraph("<i>'Traditional signature-based IDS fail against evolving cyber attacks like DoS, DDoS, Port Scans, and ARP Spoofing. They generate excessive false alarms and lack mathematical explainability.'</i>", script_style)
        ],
        [
            Paragraph("<b>Slide 3: Proposed Architecture</b>", table_cell_style),
            Paragraph("Dual AI Classifier Diagram: Deep MLP Flow Engine + Random Forest Protocol Engine", table_cell_style),
            Paragraph("<i>'Our proposed system introduces a dual AI architecture: A 3-layer Deep MLP Neural Network processes 12 flow features for volumetric attacks, while a Random Forest processes 5 ARP features for protocol tampering.'</i>", script_style)
        ],
        [
            Paragraph("<b>Slide 4: Real-Time Results & Metrics</b>", table_cell_style),
            Paragraph("Flow Model: 99.75% Acc | ARP Model: 100% Acc | 14,000 Samples", table_cell_style),
            Paragraph("<i>'Our model was evaluated on 14,000 benchmark samples modeled after CICIDS2017 and UNSW-NB15 datasets, achieving 99.75% accuracy on flow traffic and 100% on protocol anomalies.'</i>", script_style)
        ],
        [
            Paragraph("<b>Slide 5: MITRE & Active Mitigation</b>", table_cell_style),
            Paragraph("MITRE ATT&CK Matrix (T1499, T1498, T1046, T1110, T1557) & Firewall Rule Generator", table_cell_style),
            Paragraph("<i>'Every attack is mapped to standard MITRE ATT&CK techniques, and the system automatically generates actionable Linux IPTables and Fail2Ban firewall rules for instant threat blocking.'</i>", script_style)
        ]
    ]

    t_slide = Table(slide_data, colWidths=[100, 140, 264])
    t_slide.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_slide)
    story.append(Spacer(1, 10))

    # Live Demonstration Steps
    story.append(Paragraph("3. Recommended Live Demonstration Flow", h1_style))
    story.append(Paragraph("1. Open the live application at <b>https://ai-powered-threat-detection-system.vercel.app</b> in Chrome.", bullet_style))
    story.append(Paragraph("2. Point out the <b>Fixed Left Navigation Bar</b> and explain how it locks in place when scrolling.", bullet_style))
    story.append(Paragraph("3. Highlight the <b>Real-Time Threat Score Timeline</b> chart showing a steady flat line at 5.0 during normal stream.", bullet_style))
    story.append(Paragraph("4. Click the <b>DoS Attack (T1499)</b> simulator button at the top. Show the graph spike to 83.7 / High Risk immediately below the button.", bullet_style))
    story.append(Paragraph("5. Point out the <b>Live AI Prediction Card</b> showing classification, 98.5% confidence, and feature percentage reasoning ('+5,580% over baseline packet rate').", bullet_style))
    story.append(Paragraph("6. In the Security Events table, click <b>Investigate</b> on the DoS alert to display the 5-stage Alert Lifecycle, analyst guidance, and active <code>iptables</code> firewall blocking command.", bullet_style))
    story.append(Paragraph("7. Scroll to <b>Model Evaluation</b> section and present the measured 5x5 Flow Confusion Matrix and 2x2 ARP Confusion Matrix.", bullet_style))

    story.append(Spacer(1, 10))

    # Examiner Q&A Defense Script
    story.append(Paragraph("4. Examiner Q&A Defense Script (Anticipated Questions & Answers)", h1_style))
    qa_data = [
        [Paragraph("Anticipated Examiner Question", table_header_style), Paragraph("Defensible Viva Response", table_header_style)],
        [
            Paragraph("<b>Q1: What neural network model is actually implemented?</b>", table_cell_style),
            Paragraph("<i>'We implement a Deep Multi-Layer Perceptron (Deep MLP) with hidden layer structure (128, 64, 32), ReLU activation, and Adam optimizer using Scikit-Learn MLPClassifier. It processes 12 flow features extracted from network streams.'</i>", table_cell_style)
        ],
        [
            Paragraph("<b>Q2: How does the system handle zero-day attacks?</b>", table_cell_style),
            Paragraph("<i>'We implement a Statistical Outlier Distance Engine. If traffic features deviate more than 3 standard deviations from all known baseline classes, the system flags the flow as Zero-Day / Novel Anomaly (MITRE T1204).'</i>", table_cell_style)
        ],
        [
            Paragraph("<b>Q3: How does feature explainability work without black-box guessing?</b>", table_cell_style),
            Paragraph("<i>'The Ensemble Correlation Engine calculates exact feature percentage deltas relative to measured normal baselines (e.g. +5,100% over baseline packet rate of 50 pkts/s), grounding explanations strictly in empirical metrics.'</i>", table_cell_style)
        ],
        [
            Paragraph("<b>Q4: Why use Random Forest for ARP Spoofing instead of Neural Net?</b>", table_cell_style),
            Paragraph("<i>'ARP protocol poisoning is characterized by discrete rule violations (unsolicited reply ratio, MAC binding conflicts). Random Forest decision trees handle tabular protocol threshold boundaries with 100% precision.'</i>", table_cell_style)
        ]
    ]

    t_qa = Table(qa_data, colWidths=[170, 334])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_qa)

    doc.build(story)
    print(f"[PDF Generator] Successfully generated: {pdf_path}")

if __name__ == "__main__":
    create_presentation_guide_pdf()
