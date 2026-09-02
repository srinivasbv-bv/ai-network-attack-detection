import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and display total page count.
    Adds professional running headers and footers to every page.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (Skip on Page 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "AI POWERED THREAT DETECTION SYSTEM — Complete Beginner's Guide")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_str)
        self.drawString(54, 30, "KSOU Final Year Project • Academic & Technical Guide")
        self.restoreState()

def create_beginner_guide_pdf(filename="AI_Network_Attack_Detection_Beginners_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#0f172a"),
        alignment=0,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("AI POWERED THREAT DETECTION SYSTEM", title_style))
    story.append(Paragraph("Complete Beginner's Guide: What It Is, How It Works, UI Controls & Data Flow", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0284c7"), spaceAfter=15))

    # Executive Overview Callout Box
    overview_html = """
    <b>WELCOME TO THE PROJECT GUIDE!</b><br/>
    This guide explains the <i>AI POWERED THREAT DETECTION SYSTEM</i> in simple, non-technical terms. 
    It is designed for students, examiners, and security analysts to understand <b>what</b> the system does, 
    <b>why</b> it is needed, <b>how</b> each button and screen works, and <b>what happens behind the scenes</b> when actions are performed.
    """
    callout_data = [[Paragraph(overview_html, callout_style)]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0f9ff")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#bae6fd")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 12))

    # SECTION 1: WHAT IS THIS PROJECT & WHY IS IT USED?
    story.append(Paragraph("1. What is this Project & Why is it Used?", h1_style))
    story.append(Paragraph(
        "<b>Simple Analogy:</b> Imagine a high-security office building with hundreds of people entering every minute. "
        "A traditional security guard checks physical ID badges against a list of known criminals. But what if a criminal dresses up in a custom suit "
        "or uses a brand-new fake ID? The traditional guard is fooled. "
        "<br/><br/>"
        "Our project is an <b>AI Digital Security Guard</b> for computer networks. Instead of just looking at known signatures, "
        "it monitors the <i>behavior, timing, traffic volume, and protocol patterns</i> of all data entering the system. If it spots suspicious behavior "
        "(like someone trying 1,000 door handles a second, or impersonating a trusted coworker), it immediately flags an alert, blocks the attack, "
        "and shows security analysts exactly what is happening on a real-time dashboard.",
        body_style
    ))

    story.append(Paragraph("What Problem Does it Solve?", h2_style))
    story.append(Paragraph(
        "<b>The Problem:</b> Conventional Intrusion Detection Systems (IDS) rely on static rules. "
        "Hackers can easily bypass old systems by slightly altering their attack code, varying packet timing, or launching low-volume attacks. "
        "Furthermore, old systems trigger hundreds of false alarms, overwhelming security staff.<br/><br/>"
        "<b>The Solution:</b> This project uses a <b>Dual-Engine AI Architecture</b>: "
        "<br/>• <b>Deep Learning Engine (CNN + LSTM / Deep MLP):</b> Learns complex traffic sequences over time to catch high-volume flooding attacks (DoS, DDoS, Port Scans, Brute-Force). "
        "<br/>• <b>Machine Learning Anomaly Engine (Random Forest):</b> Monitors network protocol rules to catch sneaky, low-volume eavesdropping attacks (ARP Spoofing / Man-in-the-Middle).",
        body_style
    ))

    story.append(Paragraph("Business & Practical Value", h2_style))
    story.append(Paragraph("• <b>Prevents Expensive Server Downtime:</b> Protects online businesses from crashing during heavy cyberattacks.", bullet_style))
    story.append(Paragraph("• <b>Protects Sensitive Data:</b> Prevents hackers from intercepting passwords, credit card numbers, or corporate secrets.", bullet_style))
    story.append(Paragraph("• <b>Standardized Threat Context:</b> Automatically maps every attack to global standards (MITRE ATT&CK & Cyber Kill Chain) so analysts can react instantly.", bullet_style))
    story.append(Paragraph("• <b>Zero Cost (Open Source):</b> Built entirely using free tools (Python, Scikit-Learn, Flask, ELK Stack), eliminating commercial SIEM software licensing costs.", bullet_style))

    story.append(Spacer(1, 10))

    # SECTION 2: TECHNICAL & BUSINESS TERMS GLOSSARY
    story.append(Paragraph("2. Technical & Business Terms Made Simple", h1_style))

    glossary_data = [
        [Paragraph("Term", table_header_style), Paragraph("Simple Plain-English Definition", table_header_style), Paragraph("Real-World Analogy", table_header_style)],
        [Paragraph("<b>Network Flow</b>", table_body_style), Paragraph("A sequence of digital data packets sent between two computers during a conversation.", table_body_style), Paragraph("A series of letters mailed back and forth between two pen pals.", table_body_style)],
        [Paragraph("<b>DoS / DDoS</b>", table_body_style), Paragraph("Denial of Service. Flooding a server with fake traffic until it slows down or crashes.", table_body_style), Paragraph("10,000 fake customers crowding into a small coffee shop so real customers can't buy coffee.", table_body_style)],
        [Paragraph("<b>Port Scanning</b>", table_body_style), Paragraph("A hacker probing all computer ports to discover open services and weak points.", table_body_style), Paragraph("A burglar walking down a street checking every house door handle to find unlocked ones.", table_body_style)],
        [Paragraph("<b>Brute-Force</b>", table_body_style), Paragraph("Automated bot guessing passwords repeatedly at high speed until it gets in.", table_body_style), Paragraph("Someone trying every possible 4-digit code combination on a bike lock until it opens.", table_body_style)],
        [Paragraph("<b>ARP Spoofing / MITM</b>", table_body_style), Paragraph("Man-in-the-Middle attack. Hacker tricks the local network into routing target traffic through the hacker's laptop.", table_body_style), Paragraph("An eavesdropper rerouting a target's physical mail to their mailbox first, reading it, then re-mailing it.", table_body_style)],
        [Paragraph("<b>MITRE ATT&CK</b>", table_body_style), Paragraph("A world-standard cybersecurity matrix cataloging known adversary tactics and techniques.", table_body_style), Paragraph("A dictionary of known crime methods used by police detectives worldwide.", table_body_style)],
        [Paragraph("<b>ELK Stack</b>", table_body_style), Paragraph("Elasticsearch, Logstash, Kibana. A big-data search engine for centralizing and visualizing security logs.", table_body_style), Paragraph("A digital library index system that lets librarians find any security log in milliseconds.", table_body_style)]
    ]

    t_glossary = Table(glossary_data, colWidths=[95, 239, 170])
    t_glossary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_glossary)

    story.append(PageBreak())

    # SECTION 3: STEP-BY-STEP USER INTERFACE (UI) & BUTTON GUIDE
    story.append(Paragraph("3. Complete User Interface (UI) & Button Guide", h1_style))
    story.append(Paragraph(
        "This section explains every screen element, navigation item, button, metric card, and interactive control in the SOC Analyst Web Dashboard.",
        body_style
    ))

    # UI Components Table
    ui_guide_data = [
        [Paragraph("UI Component / Button", table_header_style), Paragraph("What It Shows / What Happens When Clicked", table_header_style), Paragraph("Background Action & Technical Result", table_header_style)],
        
        [Paragraph("<b>Sidebar: Navigation Menu</b>", table_body_style), 
         Paragraph("Contains quick links: Dashboard, Live Prediction, Simulator, MITRE ATT&CK, Alerts, Architecture, Metrics, Limitations.", table_body_style), 
         Paragraph("Smoothly scrolls the browser window to the selected panel section.", table_body_style)],
        
        [Paragraph("<b>Start / Stop Demo Mode Button</b>", table_body_style), 
         Paragraph("Toggles between active Demo simulation mode and passive stream mode.", table_body_style), 
         Paragraph("<b>When Clicked:</b> Calls `/api/toggle_demo`. Updates system status indicator badge (`Demo Mode` vs `Online`).", table_body_style)],

        [Paragraph("<b>Live AI Prediction Card</b>", table_body_style), 
         Paragraph("Shows latest source, destination, protocol, classification, confidence, threat score, severity, and feature reasoning.", table_body_style), 
         Paragraph("Displays feature-based reasoning explanation ('Why Was This Detected?') and key traffic feature chips in real time.", table_body_style)],

        [Paragraph("<b>Stat Cards Bar</b>", table_body_style), 
         Paragraph("Displays 4 live counters: Total Packets, Benign Traffic, Intercepted Attacks, Current Threat Index (0-100).", table_body_style), 
         Paragraph("Updates every 1 second via Server-Sent Events (SSE) or HTTP polling fallback.", table_body_style)],

        [Paragraph("<b>Attack Simulator & Intensity</b>", table_body_style), 
         Paragraph("Allows selecting Attack Type (DoS, DDoS, PortScan, BruteForce, MITM) and Intensity (Low, Medium, High).", table_body_style), 
         Paragraph("<b>Background Action:</b> Calls `/api/trigger_attack`. Injects synthetic flow metrics. Deep Learning / Anomaly Detector classifies attack and updates live dashboard.", table_body_style)],

        [Paragraph("<b>Security Events Table & Filters</b>", table_body_style), 
         Paragraph("Interactive events table with Search Input, Severity Filter (Low, Medium, High, Critical), Category Filter, and Investigate button.", table_body_style), 
         Paragraph("Filters events dynamically in DOM without page reload.", table_body_style)],

        [Paragraph("<b>Investigate Button (Alert Drawer)</b>", table_body_style), 
         Paragraph("Opens Incident Investigation Drawer modal.", table_body_style), 
         Paragraph("<b>When Clicked:</b> Shows 5-stage Alert Lifecycle (`Detected` ➔ `Classified` ➔ `Investigated` ➔ `Recommended Response` ➔ `Verified`), Feature Reasoning, Recommended Response, and Raw ECS JSON.", table_body_style)],

        [Paragraph("<b>AI Architecture & Pipeline</b>", table_body_style), 
         Paragraph("Flow diagram explaining CNN+LSTM flow model, Random Forest ARP anomaly detector, and Ensemble Fusion.", table_body_style), 
         Paragraph("Provides clear explanation for examiners on how inputs map to predictions.", table_body_style)],

        [Paragraph("<b>Model Evaluation & Confusion Matrix</b>", table_body_style), 
         Paragraph("Shows measured Accuracy, Precision, Recall, F1, FPR, FNR, and Confusion Matrix tables.", table_body_style), 
         Paragraph("Fetches real benchmark evaluation metrics from `/api/metrics` JSON file.", table_body_style)],

        [Paragraph("<b>System Drawbacks & Limitations</b>", table_body_style), 
         Paragraph("Documents 6 key limitations: Dataset Dependency, False Positives/Negatives, Explainability, Real-time Simulation vs Live Hardware Capture, Response Action Validation, Zero-Day Limits.", table_body_style), 
         Paragraph("Provides transparent, defensible documentation for academic viva review.", table_body_style)]
    ]

    t_ui = Table(ui_guide_data, colWidths=[115, 184, 205])
    t_ui.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_ui)

    story.append(Spacer(1, 12))

    # SECTION 4: COMPLETE SYSTEM WORKFLOW & DATA FLOW
    story.append(Paragraph("4. How the Complete Process Works (Step-by-Step)", h1_style))
    story.append(Paragraph(
        "Here is the complete end-to-end data pipeline from raw network packet to visual dashboard alert:",
        body_style
    ))

    workflow_steps = [
        "<b>Step 1: Network Traffic Ingestion / Simulation</b><br/>"
        "Live network packets (or simulated traffic flows) are continuously captured. Each flow contains timing, packet count, byte rate, port numbers, and protocol headers.",

        "<b>Step 2: Dual-Path Feature Extraction</b><br/>"
        "The <i>Feature Extractor</i> converts raw traffic into two numerical feature vectors:<br/>"
        "• <i>Flow Vector (12 features):</i> Duration, fwd/bwd packet count, bytes/sec, SYN/RST/ACK flags, failed auth count.<br/>"
        "• <i>ARP Vector (5 features):</i> ARP request rate, reply rate, reply/req ratio, MAC change rate, conflict count.",

        "<b>Step 3: Dual AI Engine Evaluation</b><br/>"
        "• <b>Deep Learning Model (CNN+LSTM / Deep MLP):</b> Evaluates the Flow Vector and outputs probabilities for Normal, DoS, DDoS, PortScan, and BruteForce.<br/>"
        "• <b>Random Forest Anomaly Detector:</b> Evaluates the ARP Vector and outputs anomaly score for ARP Spoofing / MITM.",

        "<b>Step 4: Ensemble Correlation & Feature Reasoning</b><br/>"
        "The <i>Ensemble Correlation Engine</i> fuses predictions, calculates Threat Score (0 - 100), and generates feature-based reasoning ('Why Was This Detected?').",

        "<b>Step 5: Threat Framework Mapping</b><br/>"
        "The event is tagged with its MITRE ATT&CK ID (e.g., T1498), Cyber Kill Chain stage (e.g., Actions on Objectives), CAPEC reference (e.g., CAPEC-125), OWASP category, and Recommended Analyst Response.",

        "<b>Step 6: ELK Stack Normalization & Export</b><br/>"
        "The <i>ELK Exporter</i> converts the alert into Elastic Common Schema (ECS 8.x) JSON, writes it to `logs/network_security_events.json`, and forwards it to Logstash / Elasticsearch.",

        "<b>Step 7: Real-Time Web Dashboard Push</b><br/>"
        "The Flask backend streams the event via SSE or HTTP polling fallback to the browser, updating live charts, Live AI Prediction Card, MITRE matrix, and security events table in real time."
    ]

    for step in workflow_steps:
        story.append(Paragraph(f"• {step}", bullet_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # Summary Callout Box
    summary_html = """
    <b>SUMMARY FOR EXAMINERS & ANALYSTS:</b><br/>
    The AI POWERED THREAT DETECTION SYSTEM delivers end-to-end automated security monitoring: 
    from feature extraction to dual AI classification, threat framework correlation, ELK indexing, and real-time SOC Analyst visual dashboard monitoring.
    """
    summary_table = Table([[Paragraph(summary_html, callout_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f0fdf4")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#86efac")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(summary_table)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF Generator] Successfully generated beginner guide PDF: {filename}")

    # Copy PDF to docs folder
    docs_pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "AI_Network_Attack_Detection_Beginners_Guide.pdf")
    try:
        import shutil
        shutil.copy(filename, docs_pdf_path)
    except Exception:
        pass

    return filename

if __name__ == "__main__":
    output_pdf = create_beginner_guide_pdf()
