
from RHST import RHST
from Scanner import Scanner

class Parser :
	def __init__(self) :
		self.rhst = RHST()
		self.table = self.rhst.get_table()
		self.parse_table = dict()
		self.parse_stack = Stack()
		self.sc = Scanner()
		self.line = 0

		self.create_parse_table()
		self.check_code()

	def push_list_to_stack(self, lst) :
		for i in range(len(lst) - 1, -1, -1) :
			if lst[i] != 'lambda' :
				self.parse_stack.push(lst[i])

	def push_body_to_stack(self, num) :
		self.push_list_to_stack(self.table[num].get_body())

	def check_code(self) :
		self.parse_stack.push('$')
		self.parse_stack.push('Program')

		token = self.sc.get_token()
		word = token.value

		while not self.parse_stack.is_empty() :
			top = self.parse_stack.top()
			ch = top[0]
			if word == top :
				token = self.sc.get_token()
				word = token.value
				self.parse_stack.pop()
			elif not (ord(ch) >= ord('A') and ord(ch) <= ord('Z')) :
				print('Error in line {} expected {} but got {}'.format(str(token.line), top, word))
				break
			elif word in self.parse_table[top] :
				self.parse_stack.pop()
				self.push_body_to_stack(self.parse_table[top][word])
			else :
				if ord(top[0]) >= ord('A') and ord(top[0]) <= ord('Z') :
					print('Error in line {} expected {} but got {}'.format(str(token.line), list(self.parse_table[top].keys()), word))  
				else :
					print('Error in line {} expected {} but got {}'.format(str(token.line), top, word))
				break
		if self.parse_stack.is_empty() :
			print('Successful')
		else :
			print('Unsuccessful')


	def create_parse_table(self) :
		for index in range(len(self.table)) :
			production = self.table[index]
			dic = dict()
			for terminal in production.get_predict() :
				dic[terminal] = index

			head = production.get_head()
			self.parse_table[head] = self.parse_table.get(head, dict())
			for i in dic :
				if i in self.parse_table[head] :
					print('predict error', head)
				self.parse_table[head][i] = dic[i]




class Stack:
	def __init__(self):
		self.items = []

	def is_empty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def top(self):
		return self.items[len(self.items)-1]

	def size(self):
		return len(self.items)

	def get_stack(self) :
		return self.items


p = Parser()
