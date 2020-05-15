import typing as T
from .Tokenizer import Token
from . import Statement

class ParseError(Exception):
	pass

class Parser:
	def __init__(self):
		self.statement_list : T.List[Statement] = list()
		self.lenmap_stmt_list: T.Dict[int,T.List[Statement]] = dict()
		self.triggers : T.Dict[str,T.Callable[[T.List[Token]],bool]] = dict()
		self.max_stmtlen: int = 0

		self.__token_list : T.List[Token] = list()
		self.__current_tok_list : T.List[Token] = list()


	def register(self,stmt : Statement,fct : T.Callable[[T.List[Token]],bool]):
		if stmt not in self.statement_list :
			self.statement_list.append(stmt)
		self.triggers[stmt.name] = fct
		self.max_stmtlen = max(self.max_stmtlen,len(stmt))

		if len(stmt) not in self.lenmap_stmt_list :
			self.lenmap_stmt_list[len(stmt)] = list()
		self.lenmap_stmt_list[len(stmt)].append(stmt)

	def load(self,tok_list : T.List[Token]):
		self.__token_list.extend(tok_list)

	def __eat(self) -> bool:
		if len(self.__token_list) > 0:
			self.__current_tok_list.append(self.__token_list[0])
			self.__token_list = self.__token_list[1:]
			return True
		else:
			return False

	def __lunch(self) -> bool:
		for i in range(len(self.__current_tok_list),self.max_stmtlen) :
			if not self.__eat() :
				return False
		return True

	def __digest(self):
		for length in sorted(self.lenmap_stmt_list,reverse=True) :
			if length > len(self.__current_tok_list) :
				continue
			for stmt in self.lenmap_stmt_list[length] :
				if stmt.match(self.__current_tok_list[:length]) :
					if self.triggers[stmt.name](self.__current_tok_list[:length]) :
						self.__current_tok_list = self.__current_tok_list[length:]
						return
		raise ParseError(f"Failed to digest {[' '.join([str(t) for t in self.__current_tok_list])]}")

	def run(self):
		while len(self.__token_list) + len(self.__current_tok_list) >= min(self.lenmap_stmt_list.keys()) :
			self.__lunch()
			self.__digest()




