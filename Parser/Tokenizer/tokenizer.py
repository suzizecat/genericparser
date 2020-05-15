import typing as T

from .toktypes import TokenType
from .token import Token

class Tokenizer :

	def __init__(self, skip_space : bool = True):
		self.types : T.Dict[str,TokenType] = dict()
		self.tokens: T.List[Token] = list()
		self.__skiplist: T.Set[TokenType] = set()
		self.__default: T.Set[TokenType] = set()

		self.__data: str = None
		self.__read_ptr : int = 0

		if skip_space :
			self.ignore(TokenType("Spaces",lambda x : x.isspace()))

	def read(self,text : str):
		self.__data = text
		self.__read_ptr = 0

	def eat(self) -> str:
		if self.__data is None :
			raise RuntimeError("Reading empty data")
		if self.__read_ptr >= len(self.__data) :
			return "EOF"
		ret = self.__data[self.__read_ptr]
		self.__read_ptr += 1
		return ret

	def back(self):
		if self.__read_ptr > 0:
			self.__read_ptr -= 1

	def add_type(self, t : TokenType):
		self.types[t.name] = t

	def ignore(self,t : TokenType):
		if t.name not in self.types :
			self.add_type(t)
		self.__skiplist.add(t)

	def default(self,t : TokenType):
		if t.name not in self.types :
			self.add_type(t)
		self.__default.add(t)

	def tokenize(self, text : T.Optional[str] = None):
		if text is not None :
			self.read(text)

		c = None

		while c != "EOF":
			valid_toktype_list = list(self.types.values())
			tok_content = ""

			while len(valid_toktype_list) > 0 :
				c = self.eat()
				tok_content += c
				if c == "EOF":
					break

				new_valid = [x for x in valid_toktype_list if x.match(tok_content)]

				if len(new_valid) == 0 :
					break

				valid_toktype_list = new_valid

			without_defaults = [x for x in valid_toktype_list if x not in self.__default]
			if len(valid_toktype_list) > 0 and len(valid_toktype_list) < len(self.types) :
				if c == "EOF":
					tok_content = tok_content[:-3]
				else:
					tok_content = tok_content[:-1]
				self.back()

				if len(valid_toktype_list) == 1 :
					if valid_toktype_list[0] not in self.__skiplist :
						self.tokens.append(Token(tok_content,valid_toktype_list[0]))

				elif len(without_defaults) == 1 :
					if without_defaults[0] not in self.__skiplist :
						self.tokens.append(Token(tok_content,without_defaults[0]))
				else :
					raise Exception(f"Confusing token {tok_content}, cannot decide between {', '.join([x.name for x in valid_toktype_list])}")

			elif len(valid_toktype_list) == len(self.types) :
				raise Exception(f"Token not handled : {tok_content}")



if __name__ == "__main__" :

	def chk_operator(txt : str):
		return txt in ["=","+","-","/","*"]

	def chk_ident(txt : str):
		return txt.isidentifier()

	def chk_txt(txt : str):
		return " " not in txt

	def chk_litt_num(txt : str):
		return txt.isnumeric()

	def chk_spaces(txt : str):
		return txt.isspace()

	test = "a = 1 - 12 &"

	operators 	= TokenType("Operator",chk_operator)
	identifiers = TokenType("Identifier", chk_ident)
	numeric		= TokenType("Numeric",chk_litt_num)
	text 		= TokenType("Generic", chk_txt)
	spaces		= TokenType("Space",chk_spaces)

	tokenizer = Tokenizer()
	tokenizer.add_type(operators)
	tokenizer.add_type(identifiers)
	tokenizer.add_type(numeric)
	tokenizer.ignore(spaces)
	tokenizer.default(text)

	tokenizer.tokenize(test)

	print(" ".join([str(x) for x in tokenizer.tokens]))





