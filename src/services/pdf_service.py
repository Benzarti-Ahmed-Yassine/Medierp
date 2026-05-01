"""
MediERP Professional - PDF Generation Service
Génération d'ordonnances avec QR Code et signature digitale
"""

import os
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import cm
import qrcode

class PDFService:
    """
    Service de génération de documents PDF (Ordonnances, Factures, Rapports).
    """

    def __init__(self, output_dir: str = "./docs/exports"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configuration des styles personnalisés pour un look médical pro"""
        self.styles.add(ParagraphStyle(
            name='MedicalHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor("#2c3e50"),
            spaceAfter=10
        ))
        self.styles.add(ParagraphStyle(
            name='PatientInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            leading=14
        ))

    def generate_prescription(self, prescription_data: Dict[str, Any], 
                            patient: Dict[str, Any], 
                            doctor: Dict[str, Any]) -> str:
        """
        Génère une ordonnance PDF professionnelle.
        """
        filename = f"ORD_{prescription_data.get('id', 'TMP')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path = os.path.join(self.output_dir, filename)
        
        doc = SimpleDocTemplate(file_path, pagesize=A4, 
                                rightMargin=2*cm, leftMargin=2*cm, 
                                topMargin=2*cm, bottomMargin=2*cm)
        
        story = []

        # 1. EN-TÊTE DOCTEUR
        doc_info = f"<b>Dr. {doctor.get('full_name', 'Inconnu')}</b><br/>" \
                   f"{doctor.get('specialty', 'Médecin Généraliste')}<br/>" \
                   f"RPPS: {doctor.get('rpps_number', '0000000000')}<br/>" \
                   f"Tél: {doctor.get('phone', 'Non renseigné')}"
        story.append(Paragraph(doc_info, self.styles['MedicalHeader']))
        story.append(Spacer(1, 1*cm))

        # 2. INFOS PATIENT & DATE
        now = datetime.now().strftime("%d/%m/%Y")
        patient_info = [
            [Paragraph(f"<b>Patient:</b> {patient.get('first_name')} {patient.get('last_name')}", self.styles['PatientInfo']),
             Paragraph(f"<b>Date:</b> {now}", self.styles['PatientInfo'])]
        ]
        t = Table(patient_info, colWidths=[12*cm, 5*cm])
        story.append(t)
        story.append(Spacer(1, 1*cm))

        story.append(Paragraph("<u>ORDONNANCE</u>", self.styles['Heading2']))
        story.append(Spacer(1, 0.5*cm))

        # 3. MÉDICAMENTS
        medications = prescription_data.get('medications', [])
        for med in medications:
            med_para = f"<b>• {med.get('name')}</b> ({med.get('dosage')})<br/>" \
                       f"<i>Pendant {med.get('duration_days')} jours</i><br/>" \
                       f"Note: {med.get('instructions', 'Selon posologie usuelle')}"
            story.append(Paragraph(med_para, self.styles['Normal']))
            story.append(Spacer(1, 0.4*cm))

        if not medications:
            story.append(Paragraph("Aucun médicament prescrit.", self.styles['Italic']))

        story.append(Spacer(1, 2*cm))

        # 4. QR CODE POUR VÉRIFICATION
        qr_path = self._generate_qr_code(prescription_data.get('id', 0))
        if qr_path:
            qr_img = Image(qr_path, width=2.5*cm, height=2.5*cm)
            qr_img.hAlign = 'LEFT'
            
            # Signature area next to QR
            sig_data = [
                [qr_img, Paragraph("<b>Signature & Cachet:</b>", self.styles['Normal'])]
            ]
            sig_table = Table(sig_data, colWidths=[4*cm, 13*cm])
            story.append(sig_table)

        # 5. GÉNÉRATION FINALE
        doc.build(story)
        
        # Nettoyage QR temporaire
        if os.path.exists("temp_qr.png"):
            try: os.remove("temp_qr.png")
            except: pass
            
        return file_path

    def _generate_qr_code(self, prescription_id: int) -> str:
        """Génère un QR code temporaire pointant vers la validation de l'ordonnance"""
        try:
            # En production, ce lien pointerait vers un portail de vérification MediERP
            verify_url = f"https://medierp.ai/verify/rx/{prescription_id}"
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(verify_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save("temp_qr.png")
            return "temp_qr.png"
        except Exception as e:
            print(f"[PDF] Erreur QR: {e}")
            return ""

# Instance globale
pdf_service = PDFService()
