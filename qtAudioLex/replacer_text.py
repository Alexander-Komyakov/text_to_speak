#!/bin/python


import os
import re


class ReplacerText:
	def __init__(self):
		self.symbols_reg = ("\s", "^", "\.", "\,", "\:", "\-", "\n", '\"', "\'")
		self.symbols = (" ", "", ".", ",", ":", "-", "\n", '"', "'")

	def replace(self, text, word_in, word_out):
		find_word_in = 0
		text_out = text
		for k in range(0, len(text)):
			for i in range(0, len(self.symbols_reg)):
				for j in range(0, len(self.symbols_reg)):
					text_out = re.sub(self.symbols_reg[i]+word_in+self.symbols_reg[j],
										self.symbols[i]+word_out+self.symbols[j],
										text_out)
		return text_out
	
	def replace_dictonary(self, text, dictonary_path, reverse=0):
		dictonary = self.read_all_file(dictonary_path)
		if dictonary == -1 or self.is_dictonary(dictonary) != 0:
			return -1
		for k in range(len(text.split(" "))):
			for i in dictonary.split("\n"):
				if len(i.split(" ")) != 2:
					continue
				word_in, word_out = i.split(" ")[0], i.split(" ")[1]
				if reverse == 1:
					word_in, word_out = i.split(" ")[1], i.split(" ")[0]
				text = self.replace(text, word_in, word_out)
		return text

	#test is realy dictonary; complies with rules
	def is_dictonary(self, dictonary):
		return 0

	def read_all_file(self, text_file):
		if not os.path.isfile(text_file):
			return -1
		with open(text_file, "r") as f:
			text = f.read()
		return text


	def replace_word(self, text, dictonary):
		text_out = text
		for i in dictonary.split("\n"):
			source, final = i.split(" ")[0], i.split(" ")[1]
			for j in range(0, len(self.symbols_reg)):
				for k in range(0, len(self.symbols_reg)):
					text_out = re.sub(self.symbols_reg[j]+source+self.symbols_reg[k],
									self.symbols[j]+final+self.symbols[k],
									text_out)
		return text_out
