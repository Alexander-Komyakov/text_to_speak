import argparse


if __name__ == "__main__":
	exit()


class ParserArg:
	def __init__(self, sys_argv):
		self.sys_argv = sys_argv
		self.parser = argparse.ArgumentParser(add_help=False)
		self.parser.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
							help=\
		"""
		Спикеры: aidar baya xenia kseniya eugene. С использованием GEN_MODEL только random. Некоторые спикеры работают с ошибками, например aidar""")
		self.parser.add_argument("-t", "--text", default="text.txt")
		self.parser.add_argument("-m", "--model", default="model.pt")
		self.parser.add_argument("-g", "--gen_model", default="")
		self.parser.add_argument("-s", "--speaker", default="eugene")
		self.parser.add_argument("-o", "--out_sound", default="sound.wav")
		self.parser.add_argument("-l", "--ssml", action=argparse.BooleanOptionalAction, default="0")
	def get_args(self):
		return self.parser.parse_args(self.sys_argv)
