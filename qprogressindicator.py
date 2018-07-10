import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QSizePolicy


class QProgressIndicator(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._angle = 0
        self._timerId = -1
        self._delay = 40
        self._displayedWhenStopped = False
        self._color = QtGui.QColor(Qt.black)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.NoFocus)

    def animationDelay(self):
        return self._delay

    def isAnimated(self):
        return self._timerId != -1

    def isDisplayedWhenStopped(self):
        return self._displayedWhenStopped

    def color(self):
        return self._color

    def sizeHint(self):
        return QtCore.QSize(20, 20)

    def heightForWidth(self, w):
        return w

    @pyqtSlot()
    def startAnimation(self):
        self._angle = 0

        if self._timerId == -1:
            self._timerId = self.startTimer(self._delay)

    @pyqtSlot()
    def stopAnimation(self):
        if self._timerId != -1:
            self.killTimer(self._timerId)

        self._timerId = -1

        self.update()

    @pyqtSlot(int)
    def setAnimationDelay(self, delay):
        if self._timerId != -1:
            self.killTimer(self._timerId)

        self._delay = delay

        if self._timerId != -1:
            self._timerId = self.startTimer(self._delay)

    @pyqtSlot(bool)
    def setDisplayedWhenStopped(self, state):
        self._displayedWhenStopped = state

        self.update()

    @pyqtSlot(QtGui.QColor)
    def setColor(self, color):
        self._color = color

        self.update()

    def timerEvent(self, event):
        self._angle = (self._angle + 30) % 360

        self.update()

    def paintEvent(self, event):
        if not self._displayedWhenStopped and not self.isAnimated():
            return

        width = min(self.width(), self.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        outerRadius = int((width-1)*0.5)
        innerRadius = int((width-1)*0.5*0.38)

        capsuleHeight = int(outerRadius - innerRadius)
        capsuleWidth = int(capsuleHeight * 0.23 if (width > 32)
                           else capsuleHeight * 0.35)
        capsuleRadius = int(capsuleWidth/2)

        for i in range(12):
            color = self._color
            color.setAlphaF(1.0 - (i/12.0))
            p.setPen(Qt.NoPen)
            p.setBrush(color)
            p.save()
            p.translate(self.rect().center())
            p.rotate(self._angle - i * 30.0)
            p.drawRoundedRect(-capsuleWidth*0.5,
                              -(innerRadius+capsuleHeight),
                              capsuleWidth,
                              capsuleHeight,
                              capsuleRadius,
                              capsuleRadius)
            p.restore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = QtWidgets.QMainWindow()

    pi = QProgressIndicator()

    frame = QtWidgets.QFrame()

    vbl = QtWidgets.QVBoxLayout()

    startPb = QtWidgets.QPushButton("start spin")
    startPb.clicked.connect(pi.startAnimation)

    stopPb = QtWidgets.QPushButton("stop spin")
    stopPb.clicked.connect(pi.stopAnimation)

    delaySlider = QtWidgets.QSlider()
    delaySlider.setRange(0, 100)
    delaySlider.setValue(pi.animationDelay())
    delaySlider.setOrientation(Qt.Horizontal)
    delaySlider.valueChanged.connect(pi.setAnimationDelay)

    vbl.addWidget(startPb)
    vbl.addWidget(stopPb)
    vbl.addWidget(delaySlider)

    hbl = QtWidgets.QHBoxLayout(frame)
    hbl.addWidget(pi)
    hbl.addLayout(vbl)

    pi.startAnimation()

    mw.setCentralWidget(frame)

    mw.show()
    sys.exit(app.exec_())
