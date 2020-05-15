import typing as T
from .toktypes import TokenType


class Token :
	def __init__(self,data : str, toktype : TokenType, priority : int = None):
		self.data : str = data
		self.type : TokenType = toktype
		self.priority : int = priority

	def __str__(self):
		return f'<{self.type.name}:"{self.data}">'

