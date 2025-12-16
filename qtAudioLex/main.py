#!/usr/bin/env python3


import os
import sys
import threading
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextBrowser, QLabel, QScrollArea, QComboBox, QLineEdit, QHBoxLayout, QTabWidget, QFileDialog, QDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer
from replacer_text import ReplacerText


class AudioEditor:
	def __init__(self, audio_widget):
		self.replacer = ReplacerText()

		self.audio_widget = audio_widget
		self.find_all_object_qt()
		self.rep_wid.hide()
		self.rep_show = False

		self.del_button.clicked.connect(self.delete)
		self.rep_button.clicked.connect(self.switch_show_replace)
		self.rep.clicked.connect(self.replace_text)
		self.rep_reverse.clicked.connect(lambda: self.replace_text(reverse=1))
		self.words_path.clicked.connect(self.get_patch)
		self.rep_words.clicked.connect(lambda: self.replace_words(0))
		self.rep_reverse_words.clicked.connect(lambda: self.replace_words(1))

	def find_all_object_qt(self):
		self.del_button = self.audio_widget.findChild(QPushButton, "delete_audio")
		self.text_brow = self.audio_widget.findChild(QTextBrowser, "txt_browser")
		self.rep_wid = self.audio_widget.findChild(QWidget, "widget_replace")
		self.replace_in = self.audio_widget.findChild(QLineEdit, "replace_in")
		self.replace_out = self.audio_widget.findChild(QLineEdit, "replace_out")
		self.rep_button = self.audio_widget.findChild(QPushButton, "replace")
		self.rep = self.audio_widget.findChild(QPushButton, "replace_button")
		self.rep_reverse = self.audio_widget.findChild(QPushButton, "replace_reverse_button")
		self.words_path = self.audio_widget.findChild(QPushButton, "words_patch")
		self.path_to_words = self.audio_widget.findChild(QLineEdit, "path_to_words")
		self.rep_words = self.audio_widget.findChild(QPushButton, "replace_words")
		self.rep_reverse_words = self.audio_widget.findChild(QPushButton, "replace_revers_words")

	def replace_words(self, reverse, path_to_words=0):
		if path_to_words == 0:
			path_to_words = self.path_to_words.text()
		new_text = self.replacer.replace_dictonary(self.text_brow.toPlainText(),
													path_to_words, reverse=reverse)
		if new_text == -1:
			self.error_message("Error dictonary")
			return -1
		self.text_brow.setPlainText(new_text)
	
	def error_message(self, text):
		dialog = QMessageBox(parent=self.audio_widget, text=text)
		dialog.setWindowTitle("Error")
		dialog.exec()

	def replace_text(self, reverse=0, word_in=0,
					word_out=0):
		if word_in == 0 or word_out == 0:
			word_in = self.replace_in.text()
			word_out = self.replace_out.text()
			if reverse != 0:
				word_in, word_out = word_out, word_in

		new_text = self.replacer.replace(self.text_brow.toPlainText(),
											word_in,
											word_out)
		self.text_brow.setPlainText(new_text)

	def get_patch(self):
		wd_patch = QFileDialog.getOpenFileName(self.audio_widget)[0]
		self.path_to_words.setText(wd_patch)

	def switch_show_replace(self):
		if self.rep_show:
			self.rep_wid.hide()
			self.rep_show = False
		else:
			self.rep_wid.show()
			self.rep_show = True

	def delete(self):
		self.audio_widget.deleteLater()

class Tab:
	def __init__(self, app, window, number):
		self.app = app
		self.window = window
		self.number_audio = 0
		self.audios = {}
		self.deletes = []

		self.replacer = ReplacerText()

		self.ui_tab = QFile("tab.ui")
		self.ui_tab.open(QFile.ReadOnly)
		self.wd_ui_tab = self.app.loader.load(self.ui_tab)
		self.find_all_object_qt()
		self.wd_tabs.addTab(self.wd_ui_tab, str(number))
		self.btn_add_text.clicked.connect(self.mgr_add_audio)
		self.btn_replace.clicked.connect(self.switch_show_replace)
		self.wd_replace.hide()
		self.rep_show = False

		self.rep.clicked.connect(self.replace_text)
		self.rep_reverse.clicked.connect(lambda: self.replace_text(reverse=1))
		self.words_path.clicked.connect(self.get_patch)
		self.rep_words.clicked.connect(lambda: self.replace_words(0))
		self.rep_reverse_words.clicked.connect(lambda: self.replace_words(1))


		self.mgr_add_audio()
	
	def find_all_object_qt(self):
		self.wd_tabs = self.window.findChild(QTabWidget, "tabWidget")
		self.vlayt_text = self.wd_ui_tab.findChild(QVBoxLayout, "vlayout_text")
		self.btn_add_text = self.wd_ui_tab.findChild(QPushButton, "add_text")
		self.btn_replace = self.wd_ui_tab.findChild(QPushButton, "replace_all_btn")
		self.btn_del_text = self.wd_ui_tab.findChild(QPushButton, "remove_text")
		self.wd_replace = self.wd_ui_tab.findChild(QWidget, "wd_replace")

		self.replace_in = self.wd_ui_tab.findChild(QLineEdit, "tab_replace_in")
		self.replace_out = self.wd_ui_tab.findChild(QLineEdit, "tab_replace_out")
		self.rep = self.wd_ui_tab.findChild(QPushButton, "tab_replace_button")
		self.rep_reverse = self.wd_ui_tab.findChild(QPushButton, "tab_replace_reverse_button")
		self.words_path = self.wd_ui_tab.findChild(QPushButton, "tab_words_patch")
		self.path_to_words = self.wd_ui_tab.findChild(QLineEdit, "tab_path_to_words")
		self.rep_words = self.wd_ui_tab.findChild(QPushButton, "tab_replace_words")
		self.rep_reverse_words = self.wd_ui_tab.findChild(QPushButton, "tab_replace_reverse_words")

	def get_patch(self):
		wd_patch = QFileDialog.getOpenFileName(self.window)[0]
		self.path_to_words.setText(wd_patch)
	
	def replace_words(self, reverse, path_to_words=0):
		if path_to_words == 0:
			path_to_words = self.path_to_words.text()

		for i in self.deletes:
			new_text = self.replacer.replace_dictonary(i.text_brow.toPlainText(),
													path_to_words, reverse=reverse)
			if new_text == -1:
				self.error_message("Не найден словарь")
				return -1
			i.text_brow.setPlainText(new_text)
		
	def replace_text(self, reverse=0, word_in=0,
					word_out=0):
		if word_in == 0 or word_out == 0:
			word_in = self.replace_in.text()
			word_out = self.replace_out.text()
			if reverse != 0:
				word_in, word_out = word_out, word_in

		for i in self.deletes:
			new_text = self.replacer.replace(i.text_brow.toPlainText(),
											word_in,
											word_out)
			i.text_brow.setPlainText(new_text)
	
	def error_message(self, text):
		dialog = QMessageBox(parent=self.window, text=text)
		dialog.setWindowTitle("Error")
		dialog.exec()

	def switch_show_replace(self):
		if self.rep_show:
			self.wd_replace.hide()
			self.rep_show = False
		else:
			self.wd_replace.show()
			self.rep_show = True

	def mgr_add_audio(self):
		self.ui_audio = QFile("onetxt.ui")
		self.ui_audio.open(QFile.ReadOnly)
		self.wd_ui_audio = self.app.loader.load(self.ui_audio)
		self.vlayt_text.addWidget(self.wd_ui_audio)
		self.deletes.append(AudioEditor(self.wd_ui_audio))

		self.audios[self.number_audio] = [self.wd_ui_audio,
							self.deletes[self.number_audio]]
		self.number_audio += 1

class Main:
	def __init__(self):
		self.app = QApplication([])

		self.ui_main = QFile("main.ui")
		self.ui_main.open(QFile.ReadOnly)
		self.loader = QUiLoader()
		self.window = self.loader.load(self.ui_main)
		self.find_all_object_qt()
		self.window.show()

		self.add_tab_button.clicked.connect(self.add_tab)

		self.del_tab_button.clicked.connect(self.del_tab)
		self.mv_tab_button.clicked.connect(self.mv_tab)
		self.tabs = []
		self.tabs.append(Tab(self, self.window, len(self.tabs)))

		self.ssml_button.clicked.connect(self.switch_show_ssml)

		self.ssml_pause_button.clicked.connect(self.add_pause)

		self.ssml_wd.hide()
		self.ssml_show = False
		self.window.focusNextPrevChild(True)

		sys.exit(self.app.exec())
	
	def find_all_object_qt(self):
		self.add_tab_button = self.window.findChild(QPushButton, "add_tab")
		self.del_tab_button = self.window.findChild(QPushButton, "del_tab")
		self.mv_tab_button = self.window.findChild(QPushButton, "mv_tab")
		self.name_tab_lbl = self.window.findChild(QLineEdit, "name_tab")
		self.wd_tabs = self.window.findChild(QTabWidget, "tabWidget")
		self.ssml_button = self.window.findChild(QPushButton, "ssml_btn")
		self.ssml_pause_button = self.window.findChild(QPushButton, "add_pause")
		self.ssml_wd = self.window.findChild(QWidget, "ssml_wd")

	def add_tab(self):
		self.tabs.append(Tab(self, self.window, len(self.tabs)))
	
	def mv_tab(self):
		self.wd_tabs.setTabText(self.wd_tabs.currentIndex(), self.name_tab_lbl.text())

	def del_tab(self):
		self.wd_tabs.removeTab(self.wd_tabs.currentIndex())
	
	def switch_show_ssml(self):
		if self.ssml_show:
			self.ssml_wd.hide()
			self.ssml_show = False
		else:
			self.ssml_wd.show()
			self.ssml_show = True
	
	def add_pause(self):
		widget = QApplication.focusWidget()
		print(widget)


if __name__ == "__main__":
	main = Main()
