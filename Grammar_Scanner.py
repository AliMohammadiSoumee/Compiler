from Production import Production

def scan_grammar() :
	file = open("Grammar.txt")
	lines = file.read()
	lines = lines.split('\n')
	lines = list(filter(lambda a: a != '', lines))

	productions = list()

	for line in lines :
		l, r = line.split('->')
		l = l.strip()
		r = r.split('|')
		for i in range(len(r)) :
			r[i] = r[i].strip()

		for i in r :
			productions.append(Production(l, i.split()))

	file.close()

	return productions

scan_grammar()