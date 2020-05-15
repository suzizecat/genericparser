import typing as T

class TokenType:
	def __init__(self,name,checker : T.Callable[[str],bool], priority : int = 0):
		self.name = name
		self.checker = checker
		self.priority = priority

	def __str__(self):
		return f"<{self.name}>"

	def match(self,data : str) -> bool :
		return self.checker(data)

	def __eq__(self, other):
		if isinstance(other,str) :
			return other == self.name
		if isinstance(other,TokenType):
			return other.name == self.name
		else :
			TypeError("Invalid type")

	def __hash__(self):
		return hash(self.name)