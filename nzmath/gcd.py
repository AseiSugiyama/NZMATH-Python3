def gcd(a, b):
	return extgcd(a, b)[0]
 
def extgcd(a, b):
	from matrix import Matrix
	tmp = Matrix(2,2)
	tmp.set([1,0,0,1])
	q = []
	while b:
		q += [a/b]
		a,b = b, a%b
	m = Matrix(2,2)
	for i in range(len(q)):
		m.set([0,1,1,-q[i]])
		tmp = m * tmp
	return [a, [tmp.compo[(0,0)], tmp.compo[(0,1)]]]

def gcd_of_list(list):
	answer = 0
	coeff = []
	for next in list:
		t = extgcd(answer, next)
		answer = t[0]
		for i in range(len(coeff)):
			coeff[i] *= t[1][0]
		coeff += [t[1][1]]
	return [answer, coeff]

if __name__ == "__main__":
	doc = """calculate the gcd of some integers
usage: gcd A B C ..."""

	import sys
	if len(sys.argv) < 3:
		print doc
		sys.exit()
	list = []
	for i in sys.argv[1:]:
		list += [int(i)]
	print gcd_of_list(list)
