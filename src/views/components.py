"""
Smart Medical AI - Custom UI Components
Composants Senior pour une interface Premium
"""

from ..utils.qt_compat import QtWidgets, QtCore, QtGui

class AvatarLabel(QtWidgets.QLabel):
    """Widget pour afficher une photo de profil circulaire"""
    def __init__(self, size=40, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.size = size
        self.setStyleSheet("background-color: #e2e8f0; border-radius: %dpx;" % (size/2))

    def set_photo(self, image_path=None):
        if image_path and os.path.exists(image_path):
            pixmap = QtGui.QPixmap(image_path)
        else:
            # Placeholder par défaut
            pixmap = QtGui.QPixmap(self.size, self.size)
            pixmap.fill(QtGui.QColor("#1890ff")) # Bleu MediERP
            
        # Créer le masque circulaire
        target = QtGui.QPixmap(self.size, self.size)
        target.fill(QtCore.Qt.GlobalColor.transparent)
        
        painter = QtGui.QPainter(target)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, self.size, self.size)
        painter.setClipPath(path)
        
        painter.drawPixmap(0, 0, pixmap.scaled(self.size, self.size, 
                                             QtCore.Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
                                             QtCore.Qt.TransformationMode.SmoothTransformation))
        painter.end()
        self.setPixmap(target)

import os
