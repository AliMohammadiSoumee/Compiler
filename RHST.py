from Grammar_Scanner import scan_grammar
from Non_Terminal import Non_Terminal

class RHST :
	

	def __init__(self) :
		self.non_terminals = dict()
		self.table = scan_grammar()

		for production in self.table :
			name = production.get_head()
			self.non_terminals[name] =  Non_Terminal(name)

		# update firsts
		for name in self.non_terminals :
			lst = self.list_for_production_with_head(name)

			for num in lst :
				self.non_terminals[name].update_first(self.first(num))

		# update follows
		self.non_terminals['Program'].update_follow(['$'])
		for non_terminal in self.non_terminals :
			self.follow(non_terminal)
		
		#update predicts
		for index in range(len(self.table)) :
			production = self.table[index]
			production.update_predict(self.predict(index))
			
		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^FOLLOW & FIRST^^^^^^^^^^^^^^^^^^^^^')
		for name in self.non_terminals :
                        print(name)
                        print("follows:  ", self.non_terminals[name].get_follow())
                        print("firsts:  ", self.non_terminals[name].get_first())
                        print("---------------------------------")

		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Predict^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
		for name in self.table :
			print(name.head, name.get_predict())
		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

	def get_table(self) :
		return self.table

	def list_for_production_with_head(self, head) :
		ary = list()
		for i in range(len(self.table)) :
			if self.table[i].get_head() == head :
				ary.append(i)
		return ary

	def list_of_productions_contain(self, name) :
		ary = list()
		for i in range(len(self.table)) :
			if (name in self.table[i].get_body()) :
				ary.append(i)
		return ary


	def first(self, num) :
		production = self.table[num]
		head = production.get_head()
		body = production.get_body()
		first_list = list()

		# print(head) 

		if not (ord(body[0][0]) >= ord('A') and ord(body[0][0]) <= ord('Z')) :
			first_list.append(body[0]) 
			body = []

		has_lambda = True
		while len(body) > 0 and has_lambda :

			temp_list = list()
			for i in self.list_for_production_with_head(body[0]) :
				temp_list.extend(self.first(i))
				
			if 'lambda' in temp_list :
				has_lambda = True
				temp_list.remove('lambda')
				if len(body) == 1 :
					temp_list.append('lambda')

			else :
				has_lambda = False

			first_list.extend(temp_list)
			
			body = body[1 : ]

		return first_list

	def follow(self, name) :
		# print(name)
		follow_list = list()
		
		for production in self.table :
			body = production.get_body()
			head = production.get_head()

			if not name in body :
				continue

			index = len(body) - 1
			while index > 0 :
				if body[index] == name :
					break
				index -= 1
			body = body[index + 1 : ]

			has_lambda = True
			while len(body) > 0 and has_lambda :
				first_item = body[0]

				if not (ord(first_item[0]) >= ord('A') and ord(first_item[0]) <= ord('Z')) :
					follow_list.append(first_item)
					break

				first_list = self.non_terminals[first_item].get_first()

				if 'lambda' in first_list :
					first_list.remove('lambda') 
					has_lambda = True
					body = body[1 : ]
				else :
					has_lambda = False

				follow_list.extend(first_list)

			if len(body) == 0 and head != name and has_lambda :
				if not self.non_terminals[head].mark :
					# temp_list = self.list_of_productions_contain(head)
					# for i in range(len(temp_list)) :
					follow_list.extend(self.follow(head))
				else :
					follow_list.extend(self.non_terminals[head].get_follow())
		self.non_terminals[name].update_follow(follow_list)
		return follow_list


	def get_first_of(self, name) :
		ch = name[0]
		if  not (ord(ch) >= ord('A') and ord(ch) <= ord('Z')) :
			return [name]
		return self.non_terminals[name].get_first()


	def predict(self, index) :
		production = self.table[index]
		head = production.get_head()
		body = production.get_body()
		predict_list = list() 

		has_lambda = False
		for i in body :
			predict_list.extend(self.get_first_of(i))

			if 'lambda' in predict_list :
				has_lambda = True
				predict_list.remove('lambda')
			else :
				has_lambda = False
				break

		if has_lambda :
			predict_list.extend(self.non_terminals[head].get_follow())

		return predict_list


