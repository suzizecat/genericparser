import typing as T
from .Tokenizer import TokenType
from .Tokenizer import Token

class Word:
	def __init__(self,name,tokt : T.List[TokenType],tokfilter : T.Optional[T.List[T.Callable[[Token], bool]]] = None):
		self.name = name
		self.token_type: T.List[TokenType] = tokt
		self.nb_var = len(self.token_type)
		if tokfilter is None :
			self.token_filter: T.List[T.Callable[[Token], bool]] = []
		else :
			self.token_filter = tokfilter
		self.token_filter.extend([(lambda x : True) for i in range(len(self.token_filter),self.nb_var)])

	def __str__(self):
		return f"<{self.name}:[{','.join([x.name for x in self.token_type])}]>"

	def match(self,aTok : Token):
		for i in range(self.nb_var) :
			if self.token_type[i] == aTok.type and self.token_filter[i](aTok) :
				return True
		return False

