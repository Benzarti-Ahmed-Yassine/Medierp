"""
Smart Medical AI - Point d'entrée de production
"""

import sys
import os
from src.utils.qt_compat import QtWidgets, QtCore
from src.core.app import create_app
from src.views.login_view import LoginDialog
from src.views.main_window import MainWindow

def main():
    # 1. Initialisation Application
    app = create_app()
    
    # 2. Lancement du Login MediERP
    login = LoginDialog()
    if login.exec() == QtWidgets.QDialog.DialogCode.Accepted:
        # Authentification réussie
        user = login.get_user()
        app.set_current_user(user)
        
        # 3. Lancement Main Window (RBAC activé)
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
    else:
        # Annulation ou échec
        print("[Main] Connexion annulée ou échouée.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[FATAL] Crash au démarrage: {e}")
        import traceback
        traceback.print_exc()
