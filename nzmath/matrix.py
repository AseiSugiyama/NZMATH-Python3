class Matrix:

	def __init__(self, m, n):
		self.m = m
		self.n = n
		self.compo = {}
		for i in range(self.m):
			for j in range(self.n):
				self.compo[(i,j)] = 0

	def display(self):
		for i in range(self.m):
			for j in range(self.n):
				print self.compo[(i,j)],
			print

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

if __name__ == "__main__":
	a = Matrix(2,2)
	b = Matrix(2,2)
	a.set([1,2,3,4])
	b.set([-3,2,0,1])
	c = a+b
	a.display()
	print
	b.display()
	print
	c.display()
	d = a*b
	d.display()
