from Token import Token

keywords = [
	    'int', 'double', 'bool', 'void', 'char',
	    'for', 'while', 'do', 
	    'if', 'else', 
	    'and', 'or', 
	    'def', 'return'
]

symbols = [
        ':', ';', ',', '\'',
        '+', '-', '*', '/', '%', 
        '(', ')', '[', ']', '{', '}', 
        '<', '>', '=', '==', '<=', '>=', '!=', '!',
        '//', '/*', '*/'
]

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']



class Scanner :

	def __init__(self) :

		self.src = open('Code.txt').read()
		self.src += '#'
		
		self.line_pos = 1
		self.char_pos = -1
		self.c = ''
		self.next_char()

		# print(self.src) 
		# print('--------------------------------')

	def next_line(self) :
		self.line_pos += 1

	def next_char(self) :
		self.char_pos += 1

		if self.char_pos >= len(self.src) :
			self.c = '#'
		else :
			self.c = self.src[self.char_pos]
		# print('c = ', self.c)

	def get_number(self) :
		temp_token = self.c
		has_dot = False

		while True :
			self.next_char()
			if not self.c in digits :
				break

		if self.c == '.' :
			self.next_char()
			if not self.c in digits :
				print("Erorr in line " + self.line_pos + " ---> not valid float type")

			else :
				while True :
					self.next_char()
					if not self.c in digits :
						break

			return 'float_number'		

		return 'int_number'


		if has_dot :
			return double_number
		return int_number

	def get_keyword(self) :
		temp = ''
		while self.is_potential_identifier_char(self.c) :
			temp += self.c
			self.next_char()
		if temp in keywords :
			return temp
		else :
			return 'id'


	def skip_comment(self, is_one_line) :
		if is_one_line :
			while self.c != '\n' and self.c != '#' :
				self.next_char()
			self.next_char()
			self.next_line()

		else :
			while self.c != '/' :
				while self.c != '*' :
					if self.c == '\n' :
						self.next_line()
					self.next_char()
				self.next_char()
			self.next_char()


	def skip_white_space(self) :
		while self.c == '\t' or self.c == '\n' or self.c == ' ' :
			if self.c == '\n' :
				self.next_line()
			self.next_char()

	def get_token(self) :
		temp_token = Token('', 0)

		if self.c == '#' :
			return Token('$', self.line_pos)

		elif self.c == '\t' or self.c == '\n' or self.c == ' ' :
			self.skip_white_space()
			temp_token = self.get_token()

		elif self.c in digits :
			temp_token = Token(self.get_number(), self.line_pos)

		elif self.c in symbols :
			temp_symbol = self.c
			self.next_char()

			temp_symbol += self.c

			if temp_symbol in symbols :
				self.next_char()
				if temp_symbol == '//' :
					self.skip_comment(True)
					temp_token = self.get_token()
				elif temp_symbol == '/*' :
					self.skip_comment(False)
					temp_token = self.get_token()
				else :
					temp_token = Token(temp_symbol, self.line_pos)

			else :
				temp_token = Token(temp_symbol[ : -1], self.line_pos)

		elif self.is_potential_identifier_start(self.c) :
			temp_token = Token(self.get_keyword(), self.line_pos)

		else :
			print('Error in scanner, invalid character {} in line {}'.format(self.c, self.line_pos)) 
			self.next_char()
			temp_token = self.get_token()

		return temp_token

	def is_potential_identifier_start(self, ch) :
		if  (ord(ch) >= ord('a') and ord(ch) <= ord('z')) or (ord(ch) >= ord('A') and ord(ch) <= ord('Z')) or (ch == '_') :
			return True
		return False

	def is_potential_identifier_char(self, ch) :
		if  (ord(ch) >= ord('a') and ord(ch) <= ord('z')) or (ord(ch) >= ord('A') and ord(ch) <= ord('Z')) or (ch == '_') or (ord(ch) >= ord('0') and ord(ch) <= ord('9')) :
			return True
		return False		