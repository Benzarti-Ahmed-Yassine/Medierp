"""
Smart Medical AI - Patient View (Real CRUD)
"""

from ..utils.qt_compat import QtWidgets, QtCore, uic
from ..core.app import SmartMedicalApp
import os

class PatientListView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = SmartMedicalApp.get_instance()
        
        # Charger le UI
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "patient_list.ui")
        uic.loadUi(ui_path, self)
        
        self._connect_signals()
        self.refresh_list()

    def _connect_signals(self):
        # Branchement des boutons s'ils existent dans le .ui
        if hasattr(self, "btnRefresh"):
            self.btnRefresh.clicked.connect(self.refresh_list)
        if hasattr(self, "btnSearch"):
            self.btnSearch.clicked.connect(self.refresh_list)
        if hasattr(self, "txtSearch"):
            self.txtSearch.textChanged.connect(self.refresh_list)
        # btnAdd est le nom dans patient_list.ui
        if hasattr(self, "btnAdd"):
            self.btnAdd.clicked.connect(self._on_add_patient)
        elif hasattr(self, "btnAddPatient"):
            self.btnAddPatient.clicked.connect(self._on_add_patient)
        if hasattr(self, "tablePatients"):
            self.tablePatients.cellDoubleClicked.connect(self._on_patient_double_clicked)


    def _on_patient_double_clicked(self, row, column):
        """Action déclenchée au double-clic sur un patient"""
        if hasattr(self, "tablePatients"):
            item = self.tablePatients.item(row, 0) # L'ID est supposé être dans la colonne 0
            if item:
                patient_id = int(item.text())
                main_window = self.window()
                if hasattr(main_window, "open_patient_dossier"):
                    main_window.open_patient_dossier(patient_id)

    def refresh_list(self):
        """Récupération réelle des données depuis la DB"""
        search_term = self.txtSearch.text() if hasattr(self, "txtSearch") else ""
        
        if search_term:
            query = "SELECT * FROM patients WHERE last_name LIKE ? OR first_name LIKE ? AND is_active = 1"
            params = (f"%{search_term}%", f"%{search_term}%")
        else:
            query = "SELECT * FROM patients WHERE is_active = 1"
            params = ()
            
        patients = self.app.db.fetch_all(query, params)
        
        if hasattr(self, "tablePatients"):
            self.tablePatients.setRowCount(0)
            self.tablePatients.verticalHeader().setDefaultSectionSize(40)
            for row, p in enumerate(patients):
                self.tablePatients.insertRow(row)
                self.tablePatients.setItem(row, 0, QtWidgets.QTableWidgetItem(str(p['id'])))
                self.tablePatients.setItem(row, 1, QtWidgets.QTableWidgetItem(p['last_name']))
                self.tablePatients.setItem(row, 2, QtWidgets.QTableWidgetItem(p['first_name']))
                self.tablePatients.setItem(row, 3, QtWidgets.QTableWidgetItem(p['cin']))
                self.tablePatients.setItem(row, 4, QtWidgets.QTableWidgetItem(p['phone']))
                
                # Column 5: Actions
                actions_widget = QtWidgets.QWidget()
                actions_layout = QtWidgets.QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(4, 0, 4, 0)
                
                btn_edit = QtWidgets.QPushButton("✏️ Modifier")
                btn_edit.setFixedHeight(28)
                btn_edit.setStyleSheet("background-color: #e6f7ff; color: #1890ff; font-size: 9pt; border: 1px solid #91d5ff; border-radius: 4px; padding: 0 8px;")
                btn_edit.clicked.connect(lambda checked, pid=p['id']: self._on_edit_patient(pid))
                
                btn_delete = QtWidgets.QPushButton("🗑️ Supprimer")
                btn_delete.setFixedHeight(28)
                btn_delete.setStyleSheet("background-color: #fff1f0; color: #ff4d4f; font-size: 9pt; border: 1px solid #ffa39e; border-radius: 4px; padding: 0 8px;")
                btn_delete.clicked.connect(lambda checked, pid=p['id']: self._on_delete_patient(pid))
                
                actions_layout.addWidget(btn_edit)
                actions_layout.addWidget(btn_delete)
                actions_layout.addStretch()
                
                self.tablePatients.setCellWidget(row, 5, actions_widget)
            
            # Update stats label
            if hasattr(self, "lblStats"):
                self.lblStats.setText(f"{len(patients)} patient(s) trouvé(s)")
                self.lblStats.setStyleSheet("color: #8c8c8c; font-size: 9pt;")


    def _on_add_patient(self):
        # Afficher la vraie boîte de dialogue d'ajout
        dialog = AddPatientDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            new_id = self.app.db.insert("patients", data)
            if new_id:
                QtWidgets.QMessageBox.information(self, "Succès", f"Patient {data['first_name']} {data['last_name']} ajouté avec succès !")
                self.refresh_list()
            else:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible d'ajouter le patient.")

    def _on_edit_patient(self, patient_id):
        patient_data = self.app.db.get_by_id("patients", patient_id)
        if not patient_data:
            QtWidgets.QMessageBox.warning(self, "Erreur", "Patient introuvable.")
            return

        dialog = AddPatientDialog(self, patient_data)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if self.app.db.update("patients", patient_id, data):
                QtWidgets.QMessageBox.information(self, "Succès", "Patient mis à jour avec succès !")
                self.refresh_list()
            else:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de mettre à jour le patient.")

    def _on_delete_patient(self, patient_id):
        reply = QtWidgets.QMessageBox.question(
            self, "Confirmation", 
            "Voulez-vous vraiment supprimer ce patient ?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
            QtWidgets.QMessageBox.StandardButton.No
        )
        if reply == QtWidgets.QMessageBox.StandardButton.Yes:
            if self.app.db.delete("patients", patient_id, hard=False): # soft delete
                QtWidgets.QMessageBox.information(self, "Succès", "Patient supprimé avec succès.")
                self.refresh_list()
            else:
                QtWidgets.QMessageBox.warning(self, "Erreur", "Impossible de supprimer le patient.")


class AddPatientDialog(QtWidgets.QDialog):
    """Boîte de dialogue pour l'ajout/édition d'un patient"""
    def __init__(self, parent=None, patient_data=None):
        super().__init__(parent)
        self.patient_data = patient_data
        self.setWindowTitle("Modifier le Patient" if patient_data else "Nouveau Patient")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: #ffffff; border-radius: 8px;")
        self._setup_ui()

    def _setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        lbl_title = QtWidgets.QLabel("Modifier le Patient" if self.patient_data else "Ajouter un Patient")
        lbl_title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #1890ff;")
        layout.addWidget(lbl_title)

        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)

        self.txt_prenom = QtWidgets.QLineEdit()
        self.txt_prenom.setPlaceholderText("Prénom")
        form_layout.addRow("Prénom:", self.txt_prenom)

        self.txt_nom = QtWidgets.QLineEdit()
        self.txt_nom.setPlaceholderText("Nom")
        form_layout.addRow("Nom:", self.txt_nom)

        self.txt_cin = QtWidgets.QLineEdit()
        self.txt_cin.setPlaceholderText("CIN")
        form_layout.addRow("CIN:", self.txt_cin)

        self.txt_phone = QtWidgets.QLineEdit()
        self.txt_phone.setPlaceholderText("Téléphone")
        form_layout.addRow("Téléphone:", self.txt_phone)

        # Pré-remplir si édition
        if self.patient_data:
            self.txt_prenom.setText(self.patient_data.get('first_name', ''))
            self.txt_nom.setText(self.patient_data.get('last_name', ''))
            self.txt_cin.setText(self.patient_data.get('cin', ''))
            self.txt_phone.setText(self.patient_data.get('phone', ''))

        layout.addLayout(form_layout)
        layout.addStretch()

        btn_layout = QtWidgets.QHBoxLayout()
        btn_cancel = QtWidgets.QPushButton("Annuler")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save = QtWidgets.QPushButton("Mettre à jour" if self.patient_data else "Enregistrer")
        btn_save.setStyleSheet("background-color: #1890ff; color: white; font-weight: bold;")
        btn_save.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)

    def get_data(self) -> dict:
        return {
            "first_name": self.txt_prenom.text().strip(),
            "last_name": self.txt_nom.text().strip(),
            "cin": self.txt_cin.text().strip(),
            "phone": self.txt_phone.text().strip(),
            "is_active": 1
        }
