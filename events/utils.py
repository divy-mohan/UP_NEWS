from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import qrcode
from io import BytesIO
import os

def generate_id_card(registration):
    """Generate ID card PDF for event registration"""
    buffer = BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=(3.5*inch, 2.2*inch),  # ID card size
        rightMargin=0.1*inch,
        leftMargin=0.1*inch,
        topMargin=0.1*inch,
        bottomMargin=0.1*inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=10,
        textColor=HexColor('#fd8535'),
        alignment=TA_CENTER,
        spaceAfter=0.1*inch
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        spaceAfter=0.05*inch
    )
    
    # Content
    story = []
    
    # Title
    story.append(Paragraph("प्रांतीय युवा प्रकोष्ठ-उत्तर प्रदेश", title_style))
    story.append(Spacer(1, 0.05*inch))
    
    # Event name
    story.append(Paragraph(f"<b>{registration.event.title}</b>", normal_style))
    story.append(Spacer(1, 0.1*inch))
    
    # Participant details
    story.append(Paragraph(f"<b>नाम:</b> {registration.full_name}", normal_style))
    story.append(Paragraph(f"<b>रजिस्ट्रेशन नं:</b> {registration.registration_number}", normal_style))
    story.append(Paragraph(f"<b>जिला:</b> {registration.district.name}", normal_style))
    story.append(Paragraph(f"<b>फोन:</b> {registration.phone}", normal_style))
    
    # Generate QR code
    qr_data = f"REG:{registration.registration_number}|NAME:{registration.full_name}|EVENT:{registration.event.title}"
    qr = qrcode.QRCode(version=1, box_size=3, border=1)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    
    # Add QR code to PDF
    story.append(Spacer(1, 0.1*inch))
    from reportlab.platypus import Image as ReportLabImage
    qr_image = ReportLabImage(qr_buffer, width=0.8*inch, height=0.8*inch)
    story.append(qr_image)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer

def send_id_card_email(registration):
    """Send ID card via email"""
    try:
        # Generate ID card
        id_card_buffer = generate_id_card(registration)
        
        # Email content
        subject = f"आपका ID कार्ड - {registration.event.title}"
        message = f"""
        प्रिय {registration.full_name},
        
        आपका पंजीकरण सफल रहा है। कृपया संलग्न ID कार्ड को डाउनलोड करें।
        
        पंजीकरण विवरण:
        - कार्यक्रम: {registration.event.title}
        - रजिस्ट्रेशन नंबर: {registration.registration_number}
        - तिथि: {registration.event.event_date.strftime('%d/%m/%Y %H:%M')}
        - स्थान: {registration.event.venue}
        
        धन्यवाद,
        प्रांतीय युवा प्रकोष्ठ-उत्तर प्रदेश
        """
        
        # Create email
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='noreply@pranteeyyuva.org',
            to=[registration.email]
        )
        
        # Attach ID card
        email.attach(
            f'ID_Card_{registration.registration_number}.pdf',
            id_card_buffer.getvalue(),
            'application/pdf'
        )
        
        # Send email
        email.send()
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
