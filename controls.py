from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Controls:
    def __init__(self, mainwin):
        self.mainwin = mainwin
        self.table = self.mainwin.ui.TrackTable
        self.playlist = []
        self.curlist = []
        self.curplaying = 0
        self.hook_ui()

    def hook_ui(self):
        self.table.itemSelectionChanged.connect(self.chose_tracks)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)

    def chose_tracks(self):
        self.curlist = []
        arr = self.table.selectedItems()
        for i in range(len(arr)):
            a = arr[i]
            if a.column() == 0:
                path = self.table.item(a.row(), 6).text()
                self.curlist.append(path)

    def open_menu(self, position):
        menu = QMenu()
        act = QAction('Play', self.mainwin)
        act.triggered.connect(self.context_play)
        menu.addAction(act)
        menu.exec_(self.table.viewport().mapToGlobal(position))

    def context_play(self):
        self.playlist = self.curlist[:]
        self.curplaying = 0
        # Start playing through self.playlist
