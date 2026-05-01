"""
Smart Medical AI - Patient Detail View (Dossier Médical)
Interface Haute Fidélité pour l'affichage complet d'un patient
"""

from ..utils.qt_compat import QtWidgets, QtCore, QtGui
from ..core.app import SmartMedicalApp

class PatientDetailView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = SmartMedicalApp.get_instance()
        self.current_patient_id = None
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 1. Header (Nom et Numéro de Dossier)
        self.header_frame = QtWidgets.QFrame()
        self.header_frame.setStyleSheet("background-color: white; border-radius: 12px; border: 1px solid #f0f0f0;")
        self.header_frame.setFixedHeight(100)
        h_layout = QtWidgets.QHBoxLayout(self.header_frame)
        h_layout.setContentsMargins(20, 20, 20, 20)

        self.lbl_patient_name = QtWidgets.QLabel("Nom du Patient")
        self.lbl_patient_name.setStyleSheet("font-size: 22pt; font-weight: bold; color: #001529;")
        
        self.lbl_dossier_id = QtWidgets.QLabel("N° Dossier: ---")
        self.lbl_dossier_id.setStyleSheet("font-size: 12pt; color: #8c8c8c;")
        
        v_header = QtWidgets.QVBoxLayout()
        v_header.addWidget(self.lbl_patient_name)
        v_header.addWidget(self.lbl_dossier_id)
        
        h_layout.addLayout(v_header)
        h_layout.addStretch()
        
        self.btn_back = QtWidgets.QPushButton("← Retour à la liste")
        self.btn_back.setStyleSheet("padding: 8px 16px; background-color: #f0f2f5; border-radius: 6px;")
        h_layout.addWidget(self.btn_back)

        main_layout.addWidget(self.header_frame)

        # 2. Tabs pour les différentes sections
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #f0f0f0; border-radius: 8px; background: white; }
            QTabBar::tab { background: #f0f2f5; padding: 10px 20px; margin-right: 5px; border-radius: 6px; }
            QTabBar::tab:selected { background: #1890ff; color: white; font-weight: bold; }
        """)

        # Tab: Informations
        self.tab_info = QtWidgets.QWidget()
        self._setup_info_tab()
        self.tabs.addTab(self.tab_info, "ℹ️ Informations")

        # Tab: Historique
        self.tab_history = QtWidgets.QWidget()
        self._setup_history_tab()
        self.tabs.addTab(self.tab_history, "📜 Historique")

        main_layout.addWidget(self.tabs)

    def _setup_info_tab(self):
        layout = QtWidgets.QFormLayout(self.tab_info)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.lbl_dob = QtWidgets.QLabel("---")
        self.lbl_phone = QtWidgets.QLabel("---")
        self.lbl_address = QtWidgets.QLabel("---")
        self.lbl_blood = QtWidgets.QLabel("---")

        style = "font-size: 11pt; color: #262626;"
        for lbl in [self.lbl_dob, self.lbl_phone, self.lbl_address, self.lbl_blood]:
            lbl.setStyleSheet(style)

        layout.addRow(QtWidgets.QLabel("<b>Date naissance :</b>"), self.lbl_dob)
        layout.addRow(QtWidgets.QLabel("<b>Téléphone :</b>"), self.lbl_phone)
        layout.addRow(QtWidgets.QLabel("<b>Adresse :</b>"), self.lbl_address)
        layout.addRow(QtWidgets.QLabel("<b>Groupe sanguin :</b>"), self.lbl_blood)

    def _setup_history_tab(self):
        layout = QtWidgets.QVBoxLayout(self.tab_history)
        self.table_history = QtWidgets.QTableWidget()
        self.table_history.setColumnCount(4)
        self.table_history.setHorizontalHeaderLabels(["Date", "Motif", "Risque IA", "Médecin"])
        self.table_history.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_history)

    def load_patient(self, patient_id):
        self.current_patient_id = patient_id
        patient = self.app.db.get_by_id("patients", patient_id)
        if patient:
            self.lbl_patient_name.setText(f"{patient['first_name']} {patient['last_name']}")
            self.lbl_dossier_id.setText(f"N° Dossier: PAT-{patient['id']:04d}")
            self.lbl_dob.setText(str(patient.get('date_of_birth', 'Non renseigné')))
            self.lbl_phone.setText(str(patient.get('phone', 'Non renseigné')))
            self.lbl_address.setText(str(patient.get('address', 'Non renseigné')))
            self.lbl_blood.setText(str(patient.get('blood_type', 'Non renseigné')))
            
            self._load_history()

    def _load_history(self):
        self.table_history.setRowCount(0)
        query = "SELECT * FROM consultations WHERE patient_id = ? ORDER BY start_time DESC"
        consultations = self.app.db.fetch_all(query, (self.current_patient_id,))
        for row, c in enumerate(consultations):
            self.table_history.insertRow(row)
            self.table_history.setItem(row, 0, QtWidgets.QTableWidgetItem(str(c['start_time'])))
            self.table_history.setItem(row, 1, QtWidgets.QTableWidgetItem(str(c['reason'])))
            
            risk_item = QtWidgets.QTableWidgetItem(f"{c['risk_score']}%")
            if c['risk_score'] and c['risk_score'] > 50:
                risk_item.setForeground(QtGui.QColor("#ff4d4f"))
            self.table_history.setItem(row, 2, risk_item)
            
            self.table_history.setItem(row, 3, QtWidgets.QTableWidgetItem(f"Dr. ID {c['doctor_id']}"))
