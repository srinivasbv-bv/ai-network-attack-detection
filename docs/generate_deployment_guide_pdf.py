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

def create_deployment_guide_pdf():
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RealTime_Deployment_Guide.pdf")
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
    story.append(Paragraph("Real-World Production Deployment & Infrastructure Guide", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=15))

    # Architecture Overview
    story.append(Paragraph("1. Enterprise Production Architecture", h1_style))
    story.append(Paragraph(
        "Deploying the <b>AI Powered Threat Detection System</b> into live enterprise networks requires dual-mode operation: (1) Cloud Web Console Tier deployed on Vercel Serverless / AWS for global SOC monitoring, and (2) On-Premise Packet Capture Taps deployed on network switches / gateways using physical network socket interfaces.",
        body_style
    ))

    # Option A: Vercel Cloud Serverless Deployment
    story.append(Paragraph("2. Option A: Vercel Serverless Cloud Deployment", h1_style))
    story.append(Paragraph("• <b>Step 1: Code Repository Preparation</b><br/>Ensure <code>api/index.py</code>, <code>vercel.json</code>, and <code>package.json</code> are present in project root directory.", bullet_style))
    story.append(Paragraph("• <b>Step 2: Connect GitHub to Vercel</b><br/>Log into Vercel Dashboard, click <b>Import Project</b>, and select the GitHub repository <code>ai-network-attack-detection</code>.", bullet_style))
    story.append(Paragraph("• <b>Step 3: Serverless Runtime Configuration</b><br/>Vercel automatically detects <code>@vercel/python</code> runtime and builds WSGI handler in <code>api/index.py</code>.", bullet_style))
    story.append(Paragraph("• <b>Step 4: Custom Subdomain / Alias Assignment</b><br/>In Vercel Project Settings ➔ General ➔ Rename project to <code>ai-powered-threat-detection-system</code> to bind to target domain URL.", bullet_style))

    # Option B: Physical Hardware Live Packet Capture Deployment
    story.append(Paragraph("3. Option B: Physical Network Hardware Capture Deployment (On-Premise)", h1_style))
    story.append(Paragraph("• <b>Step 1: Network Tap / SPAN Port Mirroring</b><br/>Configure switch port mirroring (SPAN port) on core router to mirror incoming raw traffic to dedicated network interface card (e.g. <code>eth0</code> or <code>wlan0</code>).", bullet_style))
    story.append(Paragraph("• <b>Step 2: Enable Live Socket Capture Module</b><br/>Run <code>traffic/live_capture.py</code> with administrative privileges (root/sudo):", bullet_style))
    story.append(Paragraph("sudo python3 -c \"from traffic.live_capture import LiveNetworkCapture; from engine.correlation_engine import EnsembleCorrelationEngine; eng = EnsembleCorrelationEngine('models'); cap = LiveNetworkCapture(eng, interface='eth0'); cap.start_capture()\"", code_style))
    story.append(Paragraph("• <b>Step 3: Hardware Promiscuous Mode</b><br/>Ensure interface is in promiscuous mode (<code>sudo ip link set eth0 promisc on</code>) to capture all enterprise subnet packet frames.", bullet_style))

    # Active Mitigation Scripting
    story.append(Paragraph("4. Automated Active Mitigation Firewall Integration", h1_style))
    story.append(Paragraph(
        "The system generates executable shell mitigation commands tailored to each attack classification:",
        body_style
    ))

    cmd_data = [
        [Paragraph("Attack Classification", table_header_style), Paragraph("Target Threat", table_header_style), Paragraph("Automated Active Firewall Command", table_header_style)],
        [Paragraph("<b>DoS Attack</b>", table_cell_style), Paragraph("Single-Source Volumetric Flood", table_cell_style), Paragraph("<code>sudo iptables -A INPUT -s {src_ip} -p tcp --dport 80 -m limit --limit 25/min -j ACCEPT && sudo iptables -A INPUT -s {src_ip} -j DROP</code>", table_cell_style)],
        [Paragraph("<b>DDoS Attack</b>", table_cell_style), Paragraph("Multi-Source Botnet Flood", table_cell_style), Paragraph("<code>sudo ip route add blackhole {src_ip}/32 && sudo iptables -I INPUT -s {src_ip}/24 -j DROP</code>", table_cell_style)],
        [Paragraph("<b>PortScan</b>", table_cell_style), Paragraph("Reconnaissance Scanning", table_cell_style), Paragraph("<code>sudo iptables -A INPUT -s {src_ip} -m recent --name portscan --set -j DROP</code>", table_cell_style)],
        [Paragraph("<b>BruteForce</b>", table_cell_style), Paragraph("SSH/FTP Credential Flood", table_cell_style), Paragraph("<code>sudo fail2ban-client set sshd banip {src_ip} && sudo iptables -A INPUT -s {src_ip} -p tcp --dport 22 -j DROP</code>", table_cell_style)],
        [Paragraph("<b>ARP Spoofing / MITM</b>", table_cell_style), Paragraph("MAC Poisoning", table_cell_style), Paragraph("<code>sudo arptables -A INPUT --source-ip {src_ip} -j DROP && sudo ip neighbor flush all</code>", table_cell_style)]
    ]
    t_cmd = Table(cmd_data, colWidths=[100, 110, 294])
    t_cmd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")])
    ]))
    story.append(t_cmd)
    story.append(Spacer(1, 10))

    # ELK Stack Production Integration
    story.append(Paragraph("5. ELK Stack (Elasticsearch, Logstash, Kibana) Integration", h1_style))
    story.append(Paragraph("• Every detection payload is formatted into Elastic Common Schema (ECS 8.x) JSON by <code>elk/elk_exporter.py</code>.", bullet_style))
    story.append(Paragraph("• Configure Logstash pipeline by starting Logstash with <code>elk/logstash.conf</code>:", bullet_style))
    story.append(Paragraph("logstash -f elk/logstash.conf", code_style))
    story.append(Paragraph("• Events are automatically indexed into Elasticsearch under <code>network-security-events-*</code> for long-term SOC audit trails and Kibana visual analytics.", bullet_style))

    doc.build(story)
    print(f"[PDF Generator] Successfully generated: {pdf_path}")

if __name__ == "__main__":
    create_deployment_guide_pdf()
