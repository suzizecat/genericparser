import typing as T
from . import Word
from .Tokenizer import Token


class Statement:
	def __init__(self, id : str):
		self.name = id
		self.pattern : T.List[Word] = list()

	def add_word(self,aWord : Word):
		self.pattern.append(aWord)

	def __str__(self):
		return f"<STMT {self.name}:{' '.join([str(x) for x in self.pattern])}>"

	def __len__(self):
		return len(self.pattern)

	def match(self,data : T.List[Token]) -> bool:
		if len(data) < len(self) :
			return False

		index = 0
		for tok in data :
			if not self.pattern[index].match(tok) :
				return False
			index += 1
		return True


