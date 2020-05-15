from Parser.Tokenizer import Tokenizer
from Parser.Tokenizer import TokenType
from Parser.Tokenizer import Token

from Parser import Statement

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

	def filter_equal(tk : Token):
		return tk.data == "="

	sttm = Statement("CommonOperation")

	sttm.add_word(identifiers)
	sttm.add_word(operators,filter=filter_equal)
	sttm.add_word(numeric)
	sttm.add_word(operators)
	sttm.add_word(numeric)

	print("Matching :",sttm.match(tokenizer.tokens))

