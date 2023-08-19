
def sum_and_diff(x, y, _heron_):
	""" add them up """
	print( f"sum: {x} + {y} = {x + y}")
	print(f"diff: {x} - {y} = {x - y}")
	return x + y, x - y

def square(x):
	""" square it """
	if type(x) is list:
		print("square for list")
		ans = 0
		for each in x:
			print(f"\t{each}^2 = {each*each}")
			ans = ans + each * each
		print(f"\tsquare sum: {ans}")

	else:
		ans = x * x
		print(f"square: {x}^2 = {ans}")
	return ans

def show(x, y, name="receiving"):
	""" show what you got """
	print(name)
	if x is not None: print('\tx', type(x).__name__, x)
	if y is not None: print('\ty', type(y).__name__, y)

def check_file(infile, outfile=None):
	""" check file names"""
	from os import path

	if outfile is not None:
		if path.isfile(outfile):
			print(f"{infile:20} >> {outfile:20} is already present.")
		else:
			print(f"{infile:20} >> {outfile:20} is ok.")
	else:
		print(f"{infile:20} ok?")

	return infile, outfile
