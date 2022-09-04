# -*- coding: utf-8 -*-

import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
import resource_rc

from tkinter import filedialog

import player


class Ui_MainWindow(object):

	dir_path = ''
	playing = False
	paused = False
	player = player.MusicPlayer()
	music_list = tuple()
	music_list_idx = 0

	def setupUi(self, MainWindow):
		# MainWindow attributes
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(800, 600)
		MainWindow.setMinimumSize(QtCore.QSize(800, 600))

		# init main layout & central widget
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		MainWindow.setCentralWidget(self.centralwidget)
		self.mainLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.mainLayout.setObjectName("mainLayout")

		# init music frame & layout
		self.FR_musicFrame = QtWidgets.QFrame(self.centralwidget)
		self.FR_musicFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.FR_musicFrame.setFrameShadow(QtWidgets.QFrame.Plain)
		self.FR_musicFrame.setObjectName("FR_musicFrame")
		self.mainLayout.addWidget(self.FR_musicFrame, 0, 0, 1, 1)

		self.musicLayout = QtWidgets.QGridLayout(self.FR_musicFrame)
		self.musicLayout.setObjectName("musicLayout")
		# init widgets
		self.TREE_musicList = QtWidgets.QTreeWidget(self.FR_musicFrame)
		self.TREE_musicList.setObjectName("TREE_musicList")
		font = QtGui.QFont()
		font.setFamily("Segoe UI")
		self.TREE_musicList.headerItem().setFont(0, font)
		self.musicLayout.addWidget(self.TREE_musicList, 0, 1, 1, 1)

		self.BT_openFolder = QtWidgets.QPushButton(self.FR_musicFrame, clicked=self.openFolder)
		font = QtGui.QFont()
		font.setFamily("Segoe UI")
		font.setItalic(False)
		self.BT_openFolder.setFont(font)
		self.BT_openFolder.setObjectName("BT_openFolder")
		self.musicLayout.addWidget(self.BT_openFolder, 0, 0, 1, 1, QtCore.Qt.AlignTop)


		# init playback layout & frame
		self.FR_playback = QtWidgets.QFrame(self.centralwidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		sizePolicy.setHeightForWidth(self.FR_playback.sizePolicy().hasHeightForWidth())
		self.FR_playback.setSizePolicy(sizePolicy)
		self.FR_playback.setMinimumSize(QtCore.QSize(0, 100))
		self.FR_playback.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.FR_playback.setFrameShadow(QtWidgets.QFrame.Plain)
		self.FR_playback.setObjectName("FR_playback")
		self.mainLayout.addWidget(self.FR_playback, 1, 0, 1, 1)

		self.playbackLayout = QtWidgets.QGridLayout(self.FR_playback)
		self.playbackLayout.setObjectName("playbackLayout")
		# init widgets
		self.BT_nextTrack = QtWidgets.QPushButton(self.FR_playback, clicked=self.nextTrack)
		self.BT_nextTrack.setEnabled(False)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		self.BT_nextTrack.setSizePolicy(sizePolicy)
		self.BT_nextTrack.setMinimumSize(QtCore.QSize(60, 60))
		self.BT_nextTrack.setText("")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(":/playback/Imgs/next_icon_128295.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.BT_nextTrack.setIcon(icon)
		self.BT_nextTrack.setIconSize(QtCore.QSize(40, 40))
		self.BT_nextTrack.setObjectName("BT_nextTrack")
		self.playbackLayout.addWidget(self.BT_nextTrack, 2, 3, 1, 1, QtCore.Qt.AlignLeft)

		self.BT_prevTrack = QtWidgets.QPushButton(self.FR_playback, clicked=self.prevTrack)
		self.BT_prevTrack.setEnabled(False)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		self.BT_prevTrack.setMinimumSize(QtCore.QSize(60, 60))
		self.BT_prevTrack.setMouseTracking(False)
		self.BT_prevTrack.setLayoutDirection(QtCore.Qt.LeftToRight)
		self.BT_prevTrack.setText("")
		icon1 = QtGui.QIcon()
		icon1.addPixmap(QtGui.QPixmap(":/playback/Imgs/previous_icon_128297.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.BT_prevTrack.setIcon(icon1)
		self.BT_prevTrack.setIconSize(QtCore.QSize(40, 40))
		self.BT_prevTrack.setObjectName("BT_prevTrack")
		self.playbackLayout.addWidget(self.BT_prevTrack, 2, 1, 1, 1, QtCore.Qt.AlignRight)

		self.BT_play = QtWidgets.QPushButton(self.FR_playback, clicked=self.playTrack)
		self.BT_play.setEnabled(False)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
		self.BT_play.setSizePolicy(sizePolicy)
		self.BT_play.setMinimumSize(QtCore.QSize(60, 60))
		self.BT_play.setText("")
		icon2 = QtGui.QIcon()
		icon2.addPixmap(QtGui.QPixmap(":/playback/Imgs/pause-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.BT_play.setIcon(icon2)
		self.BT_play.setIconSize(QtCore.QSize(40, 40))
		self.BT_play.setObjectName("BT_play")
		self.playbackLayout.addWidget(self.BT_play, 2, 2, 1, 1)

		self.LB_trackName = QtWidgets.QLabel(self.FR_playback)
		self.LB_trackName.setMinimumSize(QtCore.QSize(0, 50))
		self.LB_trackName.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
		self.LB_trackName.setObjectName("LB_trackName")
		self.playbackLayout.addWidget(self.LB_trackName, 0, 0, 1, 5)

		self.SLIDER_volume = QtWidgets.QSlider(self.FR_playback)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
		self.SLIDER_volume.setSizePolicy(sizePolicy)
		self.SLIDER_volume.setMaximum(100)
		self.SLIDER_volume.setProperty("value", 80)
		self.SLIDER_volume.setOrientation(QtCore.Qt.Horizontal)
		self.SLIDER_volume.valueChanged.connect(self.changeVolume)
		self.SLIDER_volume.setObjectName("SLIDER_volume")
		self.playbackLayout.addWidget(self.SLIDER_volume, 2, 4, 1, 1)


		self.retranslateUi(MainWindow)
		self.changeVolume()
		QtCore.QMetaObject.connectSlotsByName(MainWindow)


	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowIcon(QtGui.QIcon("./Imgs/icon.ico"))
		MainWindow.setWindowTitle(_translate("MainWindow", "Music Player"))
		self.TREE_musicList.headerItem().setText(0, _translate("MainWindow", "Music Name"))
		self.BT_openFolder.setText(_translate("MainWindow", "Open Folder"))
		self.LB_trackName.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Music Name</span></p><p><span style=\" font-size:10pt;\">Artist Name</span></p></body></html>"))


	def openFolder(self):
		old = self.dir_path
		self.dir_path = filedialog.askdirectory()
		try:
			if os.path.exists(self.dir_path):
				self.music_list = tuple(file for file in os.listdir(self.dir_path) if file.endswith(".wav") or file.endswith(".mp3"))
				self.enablePlaybackBT()
				self.updateMusicTree()
		except TypeError:
			self.dir_path = old


	def enablePlaybackBT(self):
		state = bool(self.music_list)
		self.BT_prevTrack.setEnabled(state)
		self.BT_nextTrack.setEnabled(state)
		self.BT_play.setEnabled(state)


	def playTrack(self):
		if self.playing:
			self.player.pause()
			self.paused = True
		elif self.paused:
			self.player.unpause()
			self.paused = False
		else:
			self.player.play(self.dir_path + "/" + self.music_list[self.music_list_idx])
			self.paused = False
		self.playing = not self.playing
		self.updateTrackLabel()


	def nextTrack(self):
		self.music_list_idx = (self.music_list_idx + 1) % len(self.music_list)
		self.playing = False
		self.playTrack()


	def prevTrack(self):
		self.music_list_idx -= 1
		self.playing = False
		self.playTrack()


	def updateMusicTree(self):
		self.TREE_musicList.clear()
		for item in self.music_list:
			rowcount = self.TREE_musicList.topLevelItemCount()
			self.TREE_musicList.addTopLevelItem(QtWidgets.QTreeWidgetItem(1))
			self.TREE_musicList.topLevelItem(rowcount).setText(0, item)


	def updateTrackLabel(self):
		metadata = self.player.getFileMetadata()
		self.LB_trackName.setText(QtCore.QCoreApplication.translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">{}</span></p><p><span style=\" font-size:10pt;\">{}</span></p></body></html>".format(metadata["name"], metadata["artist"])))


	def changeVolume(self):
		self.player.change_volume(self.SLIDER_volume.value() / 100)


if __name__ == "__main__":
	app = QtWidgets.QApplication(["Music Player"] + sys.argv)
	ui = Ui_MainWindow()
	mainWindow = QtWidgets.QMainWindow()
	ui.setupUi(mainWindow)
	mainWindow.show()
	sys.exit(app.exec_())