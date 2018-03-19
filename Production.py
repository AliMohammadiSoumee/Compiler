import copy

class Production :

	def __init__(self, head = '', body = []) :
		self.head = head
		self.body = body
		self.predict = list()
 
	def get_head(self) :
		return self.head

	def get_body(self) :
		return copy.deepcopy(self.body)

	def get_predict(self) :
		return copy.deepcopy(self.predict)

	def update_predict(self, lst) :
		self.predict.extend(lst)
