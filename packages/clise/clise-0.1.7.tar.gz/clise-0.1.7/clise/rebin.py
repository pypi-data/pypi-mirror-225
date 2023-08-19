import numpy as np

def one(arr, bin=2, mean=False):
	shape = arr.shape

	mod = shape[0] % bin
	if mod > 0:
		add = bin - mod
		arr = np.append(arr, np.zeros(add))
		shape = arr.shape

	nx = shape[0] // bin
	if mean: return np.mean(arr.reshape([nx, bin]), axis=1)
	else:    return np.sum(arr.reshape([nx, bin]), axis=1)

def two(arr, binx=2, biny=2):
	shape = arr.shape

	modx = shape[0] % binx
	mody = shape[1] % biny

	if (modx > 0) | (mody > 0):
		if modx > 0: addx = binx - modx
		else: addx = 0
		if mody > 0: addy = biny - mody
		else: addy = 0
		arr = np.pad(arr, ((0, addx), (0, addy)), 'constant', constant_values=((0, 0), (0, 0)) )
		shape = arr.shape

	nx = shape[0] // binx
	ny = shape[1] // biny

	return np.sum(np.sum(arr.reshape([nx, binx, ny, biny]), axis=3), axis=1)
