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
            self.drawString(54, 750, "AI-Powered Network Attack Detection System — Complete Beginner's Guide")
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
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
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
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=0
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("AI-Powered Network Attack Detection System", title_style))
    story.append(Paragraph("Complete Beginner's Guide: What It Is, How It Works, UI Controls & Data Flow", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#0284c7"), spaceAfter=15))

    # Executive Overview Callout Box
    overview_html = """
    <b>WELCOME TO THE PROJECT GUIDE!</b><br/>
    This guide explains the <i>AI-Powered Network Attack Detection System</i> in simple, non-technical terms. 
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
    story.append(Spacer(1, 15))

    # SECTION 1: WHAT IS THIS PROJECT & WHY IS IT USED?
    story.append(Paragraph("1. What is this Project & Why is it Used?", h1_style))
    story.append(Paragraph(
        "<b>Simple Analogy:</b> Imagine a high-security office building with hundreds of people entering every minute. "
        "A traditional security guard checks physical ID badges against a list of known criminals. But what if a criminal dresses up in a custom suit "
        "or uses a brand-new fake ID? The traditional guard is fooled. "
        "<br/><br/>"
        "Our project is an <b>AI-Powered Digital Security Guard</b> for computer networks. Instead of just looking at known signatures, "
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
        "<br/>• <b>Deep Learning Engine (Neural Network):</b> Learns complex traffic sequences over time to catch high-volume flooding attacks (DoS, DDoS, Port Scans, Brute-Force). "
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

    t_glossary = Table(glossary_data, colWidths=[100, 234, 170])
    t_glossary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
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
         Paragraph("Contains quick links: Dashboard, MITRE ATT&CK, Simulator, Alerts, Metrics.", table_body_style), 
         Paragraph("Smoothly scrolls the browser window to the selected panel section.", table_body_style)],
        
        [Paragraph("<b>Pause / Resume Stream Button</b>", table_body_style), 
         Paragraph("Clicking toggles between pausing and resuming the live dashboard feed.", table_body_style), 
         Paragraph("<b>When Clicked:</b> Temporarily suspends JavaScript SSE DOM updates. Background Python engine continues processing and saving events silently.", table_body_style)],

        [Paragraph("<b>Stat Cards Bar</b>", table_body_style), 
         Paragraph("Displays 4 live counters: Total Packets, Benign Traffic, Intercepted Attacks, Current Threat Index (0-100).", table_body_style), 
         Paragraph("Updates every 1 second via Server-Sent Events (SSE) stream from Flask backend server.", table_body_style)],

        [Paragraph("<b>DoS Attack Button (T1499)</b>", table_body_style), 
         Paragraph("Clicking injects a single-source high-volume Denial of Service attack.", table_body_style), 
         Paragraph("<b>Background Action:</b> Triggers `simulator.set_manual_attack('DoS')`. Generator injects 800-4,000 forward packets/sec with high SYN/RST flags. Deep Learning model flags DoS with ~99% confidence. Threat score rises to ~85.", table_body_style)],

        [Paragraph("<b>DDoS Attack Button (T1498)</b>", table_body_style), 
         Paragraph("Clicking injects a coordinated multi-source botnet Distributed DoS attack.", table_body_style), 
         Paragraph("<b>Background Action:</b> Injects 5,000-15,000 packets/sec flood from random botnet IPs. Flow model flags DDoS. Threat score jumps to ~98 (Critical). MITRE T1498 card glows red.", table_body_style)],

        [Paragraph("<b>Port Scan Button (T1046)</b>", table_body_style), 
         Paragraph("Clicking injects a rapid port probing reconnaissance attack.", table_body_style), 
         Paragraph("<b>Background Action:</b> Injects short duration packet bursts targeted across random destination ports (1-65535). Model identifies PortScan. Threat score set to ~45 (Medium).", table_body_style)],

        [Paragraph("<b>Brute-Force Button (T1110)</b>", table_body_style), 
         Paragraph("Clicking injects repeated failed authentication attempts on SSH/FTP/RDP.", table_body_style), 
         Paragraph("<b>Background Action:</b> Injects flow with 25-120 authentication failure attempts on port 22/21/3389. Model flags BruteForce. Maps to OWASP A07 Auth Failure.", table_body_style)],

        [Paragraph("<b>ARP Spoof / MITM Button (T1557)</b>", table_body_style), 
         Paragraph("Clicking injects a protocol-level Man-in-the-Middle spoofing attack.", table_body_style), 
         Paragraph("<b>Background Action:</b> Injects unsolicited ARP reply flood (25-120 replies/sec) and MAC binding conflicts. Random Forest Anomaly Detector intercepts protocol anomaly. Threat score set to ~95.", table_body_style)],

        [Paragraph("<b>Timeline & Doughnut Charts</b>", table_body_style), 
         Paragraph("Visual graphs showing danger score over time and category breakdown percentages.", table_body_style), 
         Paragraph("Chart.js re-renders line and doughnut data in real time as new SSE events arrive.", table_body_style)],

        [Paragraph("<b>MITRE ATT&CK Matrix Grid</b>", table_body_style), 
         Paragraph("5 interactive cards representing T1046, T1110, T1557, T1499, T1498.", table_body_style), 
         Paragraph("Flashes neon red for 1.8 seconds whenever an attack matching that technique is intercepted.", table_body_style)],

        [Paragraph("<b>Inspect Button (Alert Row)</b>", table_body_style), 
         Paragraph("Clicking opens a pop-up modal showing deep technical packet metrics.", table_body_style), 
         Paragraph("<b>When Clicked:</b> Displays raw Elastic Common Schema (ECS) JSON, exact feature vectors, detection engine name, CAPEC ID, and OWASP recommendations.", table_body_style)],

        [Paragraph("<b>Model Performance Panel</b>", table_body_style), 
         Paragraph("Shows accuracy, precision, recall, F1, and FPR for both AI models.", table_body_style), 
         Paragraph("Fetches verified evaluation metrics from `/api/metrics` JSON file.", table_body_style)]
    ]

    t_ui = Table(ui_guide_data, colWidths=[120, 184, 200])
    t_ui.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_ui)

    story.append(Spacer(1, 15))

    # SECTION 4: COMPLETE SYSTEM WORKFLOW & DATA FLOW
    story.append(Paragraph("4. How the Complete Process Works (Step-by-Step)", h1_style))
    story.append(Paragraph(
        "Here is the complete end-to-end data pipeline from raw network packet to visual dashboard alert:",
        body_style
    ))

    workflow_steps = [
        "<b>Step 1: Network Traffic Capture / Simulation</b><br/>"
        "Live network packets (or simulated traffic flows) are continuously captured. Each flow contains timing, packet count, byte rate, port numbers, and protocol headers.",

        "<b>Step 2: Dual-Path Feature Extraction</b><br/>"
        "The <i>Feature Extractor</i> converts raw traffic into two numerical feature vectors:<br/>"
        "• <i>Flow Vector (12 features):</i> Duration, fwd/bwd packet count, bytes/sec, SYN/RST/ACK flags, failed auth count.<br/>"
        "• <i>ARP Vector (5 features):</i> ARP request rate, reply rate, reply/req ratio, MAC change rate, conflict count.",

        "<b>Step 3: Dual AI Engine Evaluation</b><br/>"
        "• <b>Deep Learning Model (MLP/LSTM):</b> Evaluates the Flow Vector and outputs probabilities for Normal, DoS, DDoS, PortScan, and BruteForce.<br/>"
        "• <b>Random Forest Anomaly Detector:</b> Evaluates the ARP Vector and outputs anomaly score for ARP Spoofing / MITM.",

        "<b>Step 4: Ensemble Correlation & Conflict Resolution</b><br/>"
        "The <i>Ensemble Correlation Engine</i> fuses both predictions. If the ARP anomaly score > 60%, it prioritizes ARP Spoofing. Otherwise, it uses the Deep Learning prediction. It computes a unified Threat Score (0 - 100).",

        "<b>Step 5: Threat Framework Mapping</b><br/>"
        "The event is tagged with its MITRE ATT&CK ID (e.g., T1498), Cyber Kill Chain stage (e.g., Actions on Objectives), CAPEC reference (e.g., CAPEC-125), and OWASP Top 10 category.",

        "<b>Step 6: ELK Stack Normalization & Export</b><br/>"
        "The <i>ELK Exporter</i> converts the alert into Elastic Common Schema (ECS 8.x) JSON, writes it to `logs/network_security_events.json`, and forwards it to Logstash / Elasticsearch.",

        "<b>Step 7: Real-Time Web Dashboard Push</b><br/>"
        "The Flask backend streams the event via Server-Sent Events (SSE) to the browser, updating live charts, incrementing counters, flashing the MITRE matrix, and appending the alert to the live table."
    ]

    for step in workflow_steps:
        story.append(Paragraph(f"• {step}", bullet_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # SECTION 5: REAL-WORLD USE CASE SCENARIOS
    story.append(Paragraph("5. Real-World Use Case Examples", h1_style))

    story.append(Paragraph("<b>Scenario A: E-Commerce Store on Black Friday (DDoS Attack)</b>", h2_style))
    story.append(Paragraph(
        "A competitor hires a botnet to launch a 10,000 packet/sec flood against an e-commerce website during a sale. "
        "Our Deep Learning Flow Model detects the massive packet rate surge and high SYN/RST flags within 1 second, "
        "flags a <b>Critical DDoS Attack (T1498)</b> with a 98.0 Threat Score, and alerts the network team to block the botnet IPs before the store crashes.",
        body_style
    ))

    story.append(Paragraph("<b>Scenario B: Wi-Fi Eavesdropper in a Corporate Office (ARP Spoofing MITM)</b>", h2_style))
    story.append(Paragraph(
        "A rogue contractor plugs a laptop into an office Wi-Fi network and sends fake ARP replies to trick executive laptops into sending passwords through the contractor's device. "
        "Because ARP spoofing uses low traffic volume, traditional volumetric filters miss it. "
        "Our <b>Random Forest Anomaly Detector</b> detects the sudden spike in ARP reply/request ratio and MAC address conflict rate (100% precision), "
        "flagging an <b>ARP Spoofing / MITM (T1557)</b> alert immediately.",
        body_style
    ))

    story.append(Spacer(1, 15))

    # Summary Callout Box
    summary_html = """
    <b>SUMMARY FOR EXAMINERS & ANALYSTS:</b><br/>
    This system provides end-to-end automated protection: from raw network packet ingestion to AI classification, 
    framework correlation, ELK indexing, and real-time SOC Analyst visual dashboard monitoring.
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
    return filename

if __name__ == "__main__":
    output_pdf = create_beginner_guide_pdf()
