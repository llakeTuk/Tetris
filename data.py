import sys, random
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

class Tetris(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tboard = board(self)
        self.setCentralWidget(self.tboard)
        self.statusbar = self.statusBar()
        self.tboard.msg2statusbar[str].connect(self.statusbar.showMessage)
        self.tboard.start()
        self.resize(180, 380)
        self.center()
        self.setWindowTitle('Tetris')
        self.show

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.wigth()) / 2, (screen.height() - size.height()) / 2)

class Board(QFrame):

    msg2Statusbar = pyqtSignal(str)
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300
    
    def __init__(self, parent):
        
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []
        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()

    def shapeAt(self, x, y):

        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):

        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        
        return self.contentsRect().width() // Board.BoardWidth
    
    def squareHeight(self):
        
        return self.contentsRect().height() // Board.BoardHeight
    
    def start(self):
        
        if self.isPaused:
            return
        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()
        self.msg2Statusbar.emit(str(self.numLinesRemoved))
        self.newPiece()
        self.timer.start(Board.Speed, self)

    def pause(self):

        if not self.isStarted:
            return
        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
            self.msg2statusbar.emit('Paused')
        else:
            self.timer.start(Board.Speed, self)
            self.msg2statusbar.emit(str(self.numLinesRemoved))
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        rect = self.contentsRect()
        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()
        for i in range (Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i -1)
                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter, rect.left() + j * self.squareWidth(), boardTop + i * self.squareHeight(), shape)
        
