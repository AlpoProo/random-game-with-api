from PyQt5.QtCore import QPropertyAnimation, QRect, Qt, QEasingCurve, pyqtSignal
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import *

class AnimButton(QPushButton):
    entered = pyqtSignal()
    left = pyqtSignal()

    def __init__(self, text, parent=None):
        super(AnimButton, self).__init__(text, parent)
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.normal_rect = QRect()
        self.hover_rect = QRect()

        self.setMouseTracking(True)
        self.entered.connect(self.start_anim)
        self.left.connect(self.start_anim)

    def resizeEvent(self, event):
        super(AnimButton, self).resizeEvent(event)
        self.normal_rect = QRect(QRect(0, 0, self.width(), self.height()))
        self.hover_rect = QRect(QRect(-10, -10, self.width() + 20, self.height() + 20))

    def start_anim(self):
        if self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()

        if self.underMouse():
            self.animation.setStartValue(self.normal_rect)
            self.animation.setEndValue(self.hover_rect)
        else:
            self.animation.setStartValue(self.hover_rect)
            self.animation.setEndValue(self.normal_rect)

        self.animation.start()
