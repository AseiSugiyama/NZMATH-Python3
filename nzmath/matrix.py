class Matrix:

	def __init__(self, m, n):
		self.m = m
		self.n = n
		self.compo = {}
		for i in range(self.m):
			for j in range(self.n):
				self.compo[(i,j)] = 0

	def __add__(self, other):
		if (self.m != other.m) or (self.n != other.n): 
			raise "Matrix size error"

		sum = Matrix(self.m, self.n)

		for i in range(self.m):
			for j in range(self.n):
				sum.compo[(i,j)] = self.compo[(i,j)] + other.compo[(i,j)]

		return sum

	def __mul__(self, other):
		if self.n != other.m:
			raise "Matrix size error"

		product = Matrix(self.m, other.n)

		for i in range(self.m):
			for j in range(other.n):
				for k in range(self.n):
					product.compo[(i,j)] += self.compo[(i,k)] * other.compo[(k,j)]

		return product

	def set(self, list):
		for i in range(self.m):
			for j in range(self.n):
				self.compo[(i,j)] = list[self.n * i + j]

	def __str__(self):
		result = ""
		for i in range(self.m):
			for j in range(self.n):
				result += str(self.compo[(i,j)]) + " "
			result = result[:-1] + "\n"
		return result

	def __getitem__(self, ij):
		return self.compo[ij]

if __name__ == "__main__":
	a = Matrix(2,2)
	b = Matrix(2,2)
	a.set([1,2,3,4])
	b.set([-3,2,0,1])
	print a
	print b
	c = a+b
	print c
	d = a*b
	# below is the same with "print d"
	print d[0,0], d[0,1]
	print d[1,0], d[1,1]

