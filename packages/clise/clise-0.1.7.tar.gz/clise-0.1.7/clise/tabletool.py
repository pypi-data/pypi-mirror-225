
# Jaesub Hong (jhong@cfa.harvard.edu)

if 'clise' in __file__:
	from clise.jsontool import cc
else:
	from jsontool import cc

import pandas as pd
# import numpy as np
import astropy
import subprocess

from astropy.io	 import fits, ascii
from collections   import OrderedDict
from astropy.table import Table, QTable
from os		 import path
# from colorama      import Fore
from statistics	 import mean, median
from IPython	 import embed
from datetime      import datetime
from pathlib       import Path

import re
import gzip
# import csv

from bs4 import BeautifulSoup

def to_num(candidate):
	"""parse string to number if possible
	work equally well with negative and positive numbers, integers and floats.

	Args:
		candidate (str): string to convert

	Returns:
		float | int | None: float or int if possible otherwise None
	"""
	try:
		float_value = float(candidate)
	except ValueError:
		return None

	# optional part if you prefer int to float when decimal part is 0
	if float_value.is_integer():
		return int(float_value)

	return float_value

scino = re.compile(r'[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?')
def get_val_err(array, strip=False):
	# need to vectorize this....
	# and implement this in tabletool to separate them out
	ans  = []
	err  = []
	lerr = []
	# if type(array[0]) is not str: return array
	doerr  = False
	dolerr = False
	for each in array:
		# val=re.split('(\D|^\.)',each)
		# val=re.search('^\s*([-\+][0-9.]+)',each)
		if strip: each = each.strip().replace(" ", "")
		val = re.findall(scino, each)
		if   len(val) == 0:
			ans.append(0.0)
			err.append(0.0)
			lerr.append(0.0)
			print('cannot find a number in', each)
		elif len(val) == 1:
			ans.append(float(val[0]))
			err.append(0.0)
			lerr.append(0.0)
		elif len(val) == 2:
			ans.append(float(val[0]))
			err.append(float(val[1]))
			lerr.append(-float(val[1]))
			# lerr.append(0.0)
			doerr = True
		elif len(val) >= 3:
			ans.append(float(val[0]))
			e1 = float(val[1])
			e2 = float(val[2])
			if e2 < 0:
				lerr.append(e2)
				err.append(e1)
			else:
				lerr.append(e1)
				err.append(e2)
			dolerr = True
			if len(val) > 3:
				print(each, val)
	if not doerr:   err = None
	if not dolerr: lerr = None
	return ans, err, lerr
# ----------------------------------------------------------------------------
# pandas to astro
def pd_to_ast(table):
	ans = Table.from_pandas(table)
	for each in table:
		stype = str(table[each].dtype)
		if bool(re.match('Float', stype)):
			ans[each] = ans[each].astype(float)
		elif bool(re.match('Int', stype)):
			ans[each] = ans[each].astype(int)
	return ans

# astro to panda
def ast_to_pd(data, nopandas=False):
	data.convert_bytestring_to_unicode()
	if nopandas:
		# import plottool as pt
		# pt.embed()
		return data
	try:
		return data.to_pandas()
	except ValueError:
		# this is when some columns are multi-dimensional
		return data

# ----------------------------------------------------------------------------
# write the table to a fits file; handle gzip compression
def to_fits(filename, table, overwrite=True, allstring=False):
	filename = str(Path(filename).expanduser())
	ft = table
	if type(table) is pd.core.frame.DataFrame:
		ft = pd_to_ast(table)
		if allstring:
			for key in ft.keys(): ft[key] = ft[key].astype('str')

	if overwrite: ft.write(filename, overwrite=overwrite, format='fits')
	else:
		uz_filename = filename
		if bool(re.search(r'\.gz$', filename)):
			uz_filename = re.sub(r'\.gz$', '', filename)

		if uz_filename != filename:
			if path.exists(filename):
				subprocess.check_output(['gzip -f -d ' + filename], shell=True).decode()

		ft.write(uz_filename, append=True, format='fits')

		if uz_filename != filename:
			subprocess.check_output(['gzip -f  ' + uz_filename], shell=True).decode()

# write the table to a csv or fits file
def to_csv_or_fits(filename, table, overwrite=True, index=False, allstring=False):
	filename = str(Path(filename).expanduser())
	basename = path.basename(filename)
	if   bool(re.search(r'\.csv(|\.gz)$', basename)):
		if type(table) is astropy.table.table.Table: table = Table.to_pandas(table)
		table.to_csv (filename, index=index)
	elif bool(re.search(r'\.fits(|\.gz)$', basename)):
		to_fits(filename, table, overwrite=overwrite, allstring=allstring)

def read_mca(filename, columns=None):
	if columns is None: columns = ['data']
	with open(filename, encoding='utf-8', errors='ignore') as f:
		lines = f.readlines()

	data = []
	start = False
	for line in lines:
		if bool(re.search(r'<<END>>',  line)): break
		if start:
			data.append(int(line))
		if bool(re.search(r'<<DATA>>', line)): start = True

	return pd.DataFrame(data, columns=columns)

# read the table from a csv or fits file or a few other formats
def from_csv_or_fits(filename, index=False, ftype=None, hdu=1, nopandas=False, fill=-1, columns=None, comment=None):
	filename = str(Path(filename).expanduser())
	basename = path.basename(filename)

	if ftype is not None:
		if   ftype == "json": return pd.read_json(filename)
		elif ftype == "csv" : return pd.read_csv (filename, index_col=index, comment=None)
		elif ftype == "mca" : return read_mca (filename, columns=columns)
		# elif ftype == "tiff": return read_img (filename)
		elif ftype == "fits": return ast_to_pd(Table.read(filename, format='fits', hdu=hdu), nopandas)
		elif ftype == "fitshdr": return fits.open(filename)[hdu].header
		else:
			try:    return ast_to_pd(Table.read(filename, format=ftype), nopandas)
			except Exception: pass

	if   bool(re.search(r'\.fits(|\.gz)$', basename)): return ast_to_pd(Table.read(filename, format='fits', hdu=hdu), nopandas)
	elif bool(re.search( r'\.mrt(|\.gz)$', basename)): return ast_to_pd(Table.read(filename, format='ascii.mrt'),     nopandas)
	elif bool(re.search( r'\.csv(|\.gz)$', basename)): return pd.read_csv (filename, index_col=index, comment=comment)
	elif bool(re.search( r'\.mca(|\.gz)$', basename)): return read_mca    (filename, columns=columns)
	# elif bool(re.search(r'\.tiff(|\.gz)$', basename)): return read_img    (filename)
	elif bool(re.search( r'\.xml(|\.gz)$', basename)): return pd.read_xml (filename)
	elif bool(re.search(r'\.json(|\.gz)$', basename)): return pd.read_json(filename)

# read fits as astropy
def readfits(infile, hdu=1, hold=True):
	infile = str(Path(infile).expanduser())
	data = Table.read(infile, format='fits', hdu=hdu)

	if hold: embed()
	return data

# read SAORT output
def from_saort(infile):
	infile = str(Path(infile).expanduser())
	data   = ascii.read(infile, delimiter=r'\s', comment='^;')
	header = data.meta['comments']

	mat = re.match(r'^(.+)\((.*)\)_for_(.+)\((.*)\)', header[0])

	ytit   = mat.group(1)
	yunit  = mat.group(2)
	if yunit == 'arcseconds': yunit = 'arcsec'

	coltit  = mat.group(3)
	colunit = mat.group(4)

	cols = header[1].split('\t')

	mat   = re.match(r'^(.+)\((.*)\)', cols[0])
	xtit  = mat.group(1)
	xunit = mat.group(2)

	pdt = []
	for idx, each in enumerate(cols[1:]):
		pdt.append(QTable([data['col1'], data['col' + str(idx + 2)]],
			names=[xtit, ytit], units=[xunit, yunit],
			meta={'extname': coltit + ':' + cols[idx + 1].strip() + colunit,
				'time': str(datetime.now())}))

	return pdt

def to_json(filename, cfg):
	import json
	file = open(path.expanduser(filename), "w")
	cfg_str = json.dumps(cfg)
	file.write(cfg_str.replace(',', ',\n\t'))
	file.close()

# ----------------------------------------------------------------------------
# list the properties of fits tables
def lsfits(infile, hdu=None, overview=True, full=False,
		column=None, header=None, stat=None,
		hold=False):
	"""list the properties of fits tables
	% lsfits filename [-full] [-column HDU] [-header HDU] [-stat HDU:column]
	e.g., lsfits example.fits """

	if infile is None:
		print("Need an input file. Try with -help")
		return

	hdul = fits.open(infile)
	if overview and column is None and header is None and stat is None:
		hdul.info()
	if full or column is not None:
		for each in hdul:
			if each.is_image:  continue
			if type(column) is str:
				if each.name != column: continue
			print(cc.key + each.name, cc.reset)
			print(each.columns)
			for subeach in each.columns:
				print(subeach)
				print(subeach.name)
				print(type(subeach))
	if header is not None:
		for each in hdul:
			if type(header) is str:
				if each.name != header: continue
			print(cc.key + each.name, cc.reset)
			hdr = str(each.header)
			for i in range(0, len(hdr), 80):
				line = hdr[i:i + 79]
				if line != ''.ljust(79): print(line)
				i = i + 80
	if stat is not None:
		hdu, column = stat.split(':')
		data = from_csv_or_fits(infile, index=False, ftype='fits', hdu=hdu)
		print(infile, hdu, column, min(data[column]), max(data[column]))

	if hold:
		from IPython import embed
		embed()
	hdul.close()

# list table columns
def list(infile, index=None, ftype=None, hdu=1, list=None, hold=False,
		maxrow=0, match=None, stat=None, wrap=False, verbose: int = 0):
	"""list table vertically, works for fits and csv tables
	% tab2list filename"""

	inp = from_csv_or_fits(infile, index=index, ftype=ftype, hdu=hdu)

	trows = len(inp)
	if match is not None:
		match = match.split(';')
		for each in match:
			each = each.strip()
			if verbose >= 2: print(each)
			if   '==' in each:
				column, value = each.split('==')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp = inp[inp[column] == value]
			elif '!=' in each:
				column, value = each.split('!=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp = inp[inp[column] != value]
			elif '~=' in each:
				column, value = each.split('~=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp = inp[inp[column].str.each(value)]
			elif '>=' in each:
				column, value = each.split('>=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp = inp[inp[column] >= value]
			elif '<=' in each:
				column, value = each.split('<=')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp = inp[inp[column] <= value]
			elif '>' in each:
				column, value = each.split('>')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp = inp[inp[column] > value]
			elif '<' in each:
				column, value = each.split('<')
				if inp[column].dtypes != 'object': value = to_num(value)
				inp = inp[inp[column] < value]

	if wrap: sep, rj = '\n', 9
	else:	   sep, rj = ', ', 0
	if stat is not None:
		stat  = stat.split(';')
		nrows = len(inp)
		if nrows == 0: print('No data left')
		else:
			for each in stat:
				each = each.strip()
				if inp[each].dtypes != 'object':
					print('column: '.rjust(rj) + each,
						'rows: '  .rjust(rj) + str(nrows) + ' (' + str(trows) + ')',
						'min: '   .rjust(rj) + '{0:.5}'.format(   min(inp[each])),
						'max: '   .rjust(rj) + '{0:.5}'.format(   max(inp[each])),
						'mean: '  .rjust(rj) + '{0:.5}'.format(  mean(inp[each])),
						'median: '.rjust(rj) + '{0:.5}'.format(median(inp[each])),
						'sum: '   .rjust(rj) + '{0:.5}'.format(   sum(inp[each])),
						sep=sep)
				else:
					print('column: '.rjust(rj) + each,
						'rows: '  .rjust(rj) + str(nrows) + ' (' + str(trows) + ')',
						'min: '   .rjust(rj) + '{0:.20}'.format(   min(inp[each])),
						'max: '   .rjust(rj) + '{0:.20}'.format(   max(inp[each])),
						sep=sep)
		if list is not True: return 0

	max_len = 0
	maxrow = int(maxrow)
	if type(inp) is pd.core.frame.DataFrame:
		# this one only for pandas
		new = True
		for idx, row in inp.iterrows():
			if new:
				new = False
				for key in row.keys():
					clen = len(key)
					if max_len < clen:
						max_len = clen
				max_len += 1

			for key, val in row.items():
				try:
					print(f'{key:>{max_len}} | {val:<}')
				except Exception:
					print(f'{key:>{max_len}} |', val)
			print()
			if maxrow > 0:
				if maxrow <= idx + 1: break
	else:
		# astropy Table
		for key in inp.colnames:
			clen = len(key)
			if max_len < clen:
				max_len = clen
		max_len += 1
		for  row in inp.iterrows():
			for key, val in zip(inp.colnames, row):
				if str(type(val)) == "<class 'numpy.ndarray'>":
					vals = []
					for each in val:
						if type(each) is bool or \
							str(type(each)) == "<class 'numpy.bool_'>":
							if each: vals.append('T')
							else:    vals.append('F')
						else: vals.append(str(each))
					val = ",".join(vals)
				print(key.rjust(max_len), '|', val)
			print()
			if maxrow > 0:
				if maxrow <= idx + 1: break

	return 0

# convert csv to fits and vice versa, based on extension
def csv2fits(infile, outfile, ftype=None, hdu=1):
	"""convert csv files to fits files and vice versa

	% csv2fits csv_file  -outfile fits_file
	% fits2csv fits_file -outfile csv_file [-hdu=HDU]

		-hdu: set HDU id """

	inp = from_csv_or_fits(infile, ftype=ftype, hdu=hdu)
	to_csv_or_fits(outfile, inp)

def tdat2csv(infile, outfile, verbose: int = 0, sort=None, slice=None):

	if verbose >= 2: print(infile)

	names = []
	dtype = OrderedDict()
	skiprows = 0

	# if gz compressed
	if bool(re.search(r'\.gz$', infile)):
		with gzip.open(infile, 'rt') as f:
			for line in f:
				skiprows = skiprows + 1
				mat = re.search(r'^field\[(.*)\][ ]*=[ ]*([a-z]+)[0-9]+', line)
				if bool(mat):
					cdtype = mat.group(2)
					if cdtype == 'char': cdtype = 'str'
					if verbose >= 3:
						print(mat.group(1), ' ', cdtype)
					names.append(mat.group(1))
					dtype[mat.group(1)] = cdtype
				if bool(re.match('^<DATA>$', line)):
					if verbose >= 3: print('done!')
					break
	else:
		with open(infile, 'rt') as f:
			for line in f:
				skiprows = skiprows + 1
				mat = re.search(r'^field\[(.*)\][ ]*=[ ]*([a-z]+)[0-9]+', line)
				if bool(mat):
					cdtype = mat.group(2)
					if cdtype == 'char': cdtype = 'str'
					if verbose >= 3:
						print(mat.group(1), ' ', cdtype)
					names.append(mat.group(1))
					dtype[mat.group(1)] = cdtype
				if bool(re.match('^<DATA>$', line)):
					if verbose >= 3: print('done!')
					break

	print(skiprows)

	if verbose >= 3: print(names)
	data = pd.read_csv(infile, names=names, sep='|',
# 		dtype=dtype,
		engine='c',
		index_col=False,
		na_filter=False,
		encoding='cp1252',  # to avoid failing after nrows=1716511
		skiprows=skiprows)

	if verbose >= 3:
		print(type(data))
		print(type(data['name']))
		print(data['name'])

	data = data[data.name != '<END>']

	if sort is not None:
		data = data.sort_values(by=sort)

	if slice is not None:
		sl = slice
		for key in sl:
			print(key, sl[key])
			data = data[data[key] == sl[key]]

	to_csv_or_fits(outfile, data, allstring=True)

def filter(infile, outfile=None, sl=None, ftype=None, hdu=1, sort=None, nopandas=False,
		hold=False, all=False, overwrite=True):
	"""Usage: filter file [-slice options]
		-hdu: set HDU id """

	data = from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if sl is not None:
		for k, v in sl.items():
			print(k, v)
			if   v[0] == '==': data = data[data[k] == v[1]]
			elif v[0] == '!=': data = data[data[k] != v[1]]
			elif v[0] == '~=': data = data[data[k].str.contains(v[1])]
			elif v[0] == '^=': data = data[~data[k].str.contains(v[1])]
			elif v[0] == '>=': data = data[data[k] >= v[1]]
			elif v[0] == '<=': data = data[data[k] <= v[1]]
			elif v[0] == '>' : data = data[data[k] >  v[1]]
			elif v[0] == '<' : data = data[data[k] <  v[1]]

	if sort is not None:
		if   type(data) is pd.core.frame.DataFrame  : data = data.sort_values(by=sort)
		elif type(data) is astropy.table.table.Table: data.sort(sort)

	if hold: embed()
	if outfile is not None: to_csv_or_fits(outfile, data, overwrite=overwrite)

def valerr(infile, outfile=None, cols=None, ftype=None, hdu=1, sort=None, nopandas=False, strip=False,
		hold=False, all=False, overwrite=True):
	"""Usage: valerr file [-cols column_names]

		-hdu: set HDU id """

	data = from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if cols is not None:
		for col in cols:
			val, err, lerr = get_val_err(data[col], strip=strip)
			data[col] = val
			if err  is not None: data[col + '_err' ] = err
			if lerr is not None: data[col + '_lerr'] = lerr

	if sort is not None:
		if   type(data) is pd.core.frame.DataFrame  : data = data.sort_values(by=sort)
		elif type(data) is astropy.table.table.Table: data.sort(sort)

	if hold: embed()
	if outfile is not None: to_csv_or_fits(outfile, data, overwrite=overwrite)

# ----------------------------------------------------------------------------
def html2csv(infile, outfile=None, header=None, start=0, meta=None,
		overwrite=True, hdu=None, units=None, dtype=None, verbose=0):

	# empty list
	data = []

	# for getting the header from
	# the HTML file
	soup = BeautifulSoup(open(infile, encoding="utf-8-sig"), 'html.parser')

	if header is None:
		list_header = []
		header = soup.find_all("table")[0].find("tr")
		for items in header:
			try: list_header.append(items.get_text().encode('utf-8'))
			except Exception: continue
		start = start + 1
	else:
		if type(header).__name__ == 'list':
			list_header = header
		else:
			list_header = header.keys()
			units  = []
			dtype_ = []
			for key, val in header.items():
				if type(val).__name__ == 'list':
					units.append(val[0])
					dtype_.append(val[1])
				else:
					units.append(val)

			if dtype is None:
				if len(dtype_) != 0:
					dtype = dtype_

	if units is None:
		list_units = []
		units = soup.find_all("table")[0].find("tr")[start:start + 1]
		for items in units:
			try:
				list_units.append(text=items.get_text().encode('utf-8'))
			except Exception:
				continue
		start = start + 1
	else:
		list_units = units

	ncol = len(list_header)
	# for getting the data
	HTML_data = soup.find_all("table")[0].find_all("tr")[start:]
	for element in HTML_data:
		sub_data = []
		k = 0
		for sub_element in element:
			try:
				inp = sub_element.get_text().encode('utf-8')
				if dtype is not None:
					if   dtype[k] == "int"  : inp = int(inp)
					# elif dtype[k] == "long" : inp = long(inp)
					elif dtype[k] == "float": inp = float(inp)
				sub_data.append(inp)
				k = k + 1
			except Exception:
				continue
		if len(sub_data) != ncol: continue
		data.append(sub_data)

	# Storing the data into Pandas
	# DataFrame

	if meta is None: meta = OrderedDict()
	if hdu is not None: meta['EXTNAME'] = hdu

	dataFrame = Table(rows=data, meta=meta,
			names=list_header, units=list_units)

	# Converting Pandas DataFrame
	# into CSV file
	if outfile is not None:
		to_csv_or_fits(outfile, dataFrame, overwrite=overwrite)
