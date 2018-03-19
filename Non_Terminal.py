import copy


class Non_Terminal :

	def __init__(self, name) :
		self.name = name
		self.first = list()
		self.follow = set()
		self.mark = False

	def get_name(self) :
		return self.name

	def get_first(self) :
		return copy.deepcopy(self.first)

	def get_follow(self) :
		return copy.deepcopy(list(self.follow))

	def update_first(self, lst) :
		self.first.extend(lst)

	def update_follow(self, lst) :
		self.mark = True
		self.follow = self.follow.union(set(lst))
	