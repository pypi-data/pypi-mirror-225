
# Jaesub Hong (jhong@cfa.harvard.edu)

# import csv
# import gzip
import re
import subprocess
# import pandas		as pd
# import astropy.units	as u

# from collections  import OrderedDict
from os		import path, remove
from os		import rename as os_rename
from pathlib	import Path
from datetime	import datetime

if 'clise' in __file__:
	from clise.jsontool import cc, show, simplify
	from clise.rabbit   import timestr2stamp, sizestr2size
else:
	from jsontool import cc, show, simplify
	from rabbit   import timestr2stamp, sizestr2size

skip_job = '_skip_job_'
skip_par = '_skip_par_'

# run command script like HEASOFT or CIAO tools
def cmdscript(cmd, pars, basedir,
		ungzip=[], gzip=[],
		pre=[], post=[],
		skip_job=skip_job, skip_par=skip_par,
		script=True, execute=False, out=False,
		missing=None,
		verbose: int = 0, hold=False):
	"""run generic commands like HEASOFT or CIAO tools
	"""

	skip = False
	cmdscript = []
	if basedir is not None: cmdscript = ["cd " + basedir]

	# pre processing
	if type(pre) is str: pre = [pre]
	for each in pre: cmdscript.append(each)

	# handle if there is no file
	# update gzip list accordingly
	mod_ungzip = [v for v in ungzip]
	mod_gzip   = [v for v in gzip]
	if pars is not None:
		mod_pars = pars.copy()
		for key, val in pars.items():
			if type(val) is not str: continue

			try:
				re.match(skip_par, val)
			except Exception:
				from IPython import embed
				embed()

			if bool(re.match(skip_par, val)):
				mod_pars.pop(key)
			elif bool(re.match(skip_job, val)):
				skip = True
				mod_pars[key] = cc.err + mod_pars[key] + cc.hl
			elif val in ["", "\"\"", "None"]: pass
			else: continue

			if key in ungzip: mod_ungzip.remove(key)
			if key in   gzip: mod_gzip  .remove(key)

	# gzip -d
	for each in mod_ungzip:
		cmdscript.append('gzip -f -d ' + pars[each])
	for each in mod_gzip:
		mod_pars[each] = re.sub(r'\.gz$', '', pars[each])

	display = [v for v in cmdscript]

	# main
	curscript = [cmd]
	if pars is not None:
		for k, v in mod_pars.items():
			# skip parameter
			curscript.append(" " +  k + "=" + str(v))
	cmdscript.append( "".join(curscript))
	display  .append(" \\\n      ".join(curscript))

	# re-gzip
	for each in mod_gzip:
		cmdscript.append('gzip -f ' + mod_pars[each])
		display  .append('gzip -f ' + mod_pars[each])

	# post processing
	if type(post) is str: post = [post]
	for each in post:
		cmdscript.append(each)
		display  .append(each)

	if script :
		if not skip: print("\n".join(display))
		else:        print(cc.hl + "\n".join(display), cc.reset)
		if missing is not None:
			for each in missing:
				print(cc.err + each, cc.reset)

	output = None
	if execute:
		if not skip:
			try:
				output = subprocess.check_output([";".join(cmdscript)], shell=True).decode()
			except subprocess.CalledProcessError as errors:
				print(errors.output)

			if out: print(output)
	else:
		if verbose >= 1: print("No execution requested")

	return output is not None

# recursive search files based on the time and size
def search(infile, refile,
		basedir=None,
		after=None, before=None,
		larger=None, smaller=None,
		hold=False, all=False, feed=False):
	"""Usage: search 'file expr' [-after time|file] [-before time|file]
				[-larger size|file] [-smaller size|file]

	recursively search files based on the time and size
		designed for a command line tool

	e.g.,  search '(.*).txt' -after readme.txt

		lists all the files with the txt extenstion modified
		after readme.txt was lasted modified.
		Note the '' and () in the file expr.
		The wild character should be in () and '.' is needed."""

	infile = str(Path(infile ).expanduser())

	instat = Path(infile).stat()
	intime = instat.st_mtime
	insize = instat.st_size

	cc_time = cc.reset
	cc_size = cc.reset
	cc_name = cc.reset
	cc_sel  = cc.key
	cc_ref  = cc.type

	refile = False

	bingo = True
	compared = False
	if after is not None:
		retime = timestr2stamp(after)
		if retime is not None:
			if retime == intime: refile = True
			if intime <= retime: bingo  = False
			compared = True

	if before is not None:
		retime = timestr2stamp(before)
		if retime is not None:
			if retime == intime: refile = True
			if intime >= retime: bingo  = False
			compared = True

	if smaller is not None:
		resize = sizestr2size(smaller)
		if resize < 0 or insize == resize: refile = True
		if insize >= resize: bingo = False
		compared = True

	if larger is not None:
		resize = sizestr2size(larger)
		if resize < 0 or insize == resize: refile = True
		if insize <= resize: bingo = False
		compared = True

	if bingo:
		if after  is not None or before  is not None: cc_time = cc_sel
		if larger is not None or smaller is not None: cc_size = cc_sel

	if refile:
		cc_size = cc_ref
		cc_time = cc_ref
		cc_name = cc_ref

	if all or bingo or (not compared):
		if feed: print(infile)
		else:    print(cc_time + str(datetime.fromtimestamp(intime))[2:19:],
					cc_size + simplify(insize).rjust(6),
					cc_name + infile + cc.reset)

	return bingo

def search_heron(infile, refile,
		after=None, before=None,
		larger=None, smaller=None,
		hold=False, all=False, feed=False):
	"""Usage: search 'file expr' [-after time|file] [-before time|file]
			[-larger size|file] [-smaller size|file]

	recursively search files based on the time and size
		designed for a command line tool

	e.g.,  search '(.*).txt' -after readme.txt

		lists all the files with the txt extenstion modified
		after readme.txt was lasted modified.
		Note the '' and () in the file expr.
		The wild character should be in () and '.' is needed."""

	infile = str(Path(infile ).expanduser())

	instat = Path(infile).stat()
	intime = instat.st_mtime
	insize = instat.st_size

	cc_time = cc.reset
	cc_size = cc.reset
	cc_name = cc.reset
	cc_sel  = cc.key
	cc_ref  = cc.type

	refile = False

	bingo = True
	compared = False
	if after is not None:
		retime = timestr2stamp(after)
		if retime is not None:
			if retime == intime: refile = True
			if intime <= retime: bingo  = False
			compared = True

	if before is not None:
		retime = timestr2stamp(before)
		if retime is not None:
			if retime == intime: refile = True
			if intime >= retime: bingo  = False
			compared = True

	if smaller is not None:
		resize = sizestr2size(smaller)
		if resize < 0 or insize == resize: refile = True
		if insize >= resize: bingo = False
		compared = True

	if larger is not None:
		resize = sizestr2size(larger)
		if resize < 0 or insize == resize: refile = True
		if insize <= resize: bingo = False
		compared = True

	if bingo:
		if after  is not None or before  is not None: cc_time = cc_sel
		if larger is not None or smaller is not None: cc_size = cc_sel

	if refile:
		cc_size = cc_ref
		cc_time = cc_ref
		cc_name = cc_ref

	if all or bingo or (not compared):
		if feed: print(infile)
		else:    print(cc_time + str(datetime.fromtimestamp(intime))[2:19:],
					cc_size + simplify(insize).rjust(6),
					cc_name + infile + cc.reset)

	return bingo

def rename(infile, outfile, verbose: int = 1, overwrite=False):
	"""Usage: rename infile -outfile outfile [-overwrite]
	rename multiple files using cjson.py

		infile   : only needs a partial expression of the file name
		outfile  : needs the full expression
		overwrite: overwrite even if the file exists

	e.g.,  rename '(.*)(h)(ere)' -outfile '{1}{2}...{3}.txt'
		will rename files:
		here.txt   -> h...ere.txt
		there.txt  -> th...ere.txt

	each {#} corresponds to the text in () in order.
	wild keys are based on rudimentary regex: e.g.,
		(.*)    : 0 or more characters
		(.)     : 1 character
		([0-9]+): 1 or more numbers
	"""
	infile  = str(Path(infile ).expanduser())
	outfile = str(Path(outfile).expanduser())
	if verbose >= 1: print(infile, '->', cc.key + outfile + cc.err, end='')

	if path.isdir(outfile):
		if verbose >= 1: print('...'.rjust(5), outfile, 'is a directory: skip' + cc.reset)
		return False

	if not path.isfile(outfile):
		os_rename(infile, outfile)
		print(cc.reset)
		return True
	else:
		if overwrite:
			print(cc.hl + '...'.rjust(5), outfile, ' exists, but now overwritten by', infile + cc.reset)
			os_rename(infile, outfile)
			return True
		else:
			if verbose >= 1: print('...'.rjust(5), outfile, 'exists: skip' + cc.reset)
			return False

def summary(success, summary=False, overview=False):
	if success is None: return
	if overview:
		show(success, notype=True)
	if summary:
		# from IPython import embed; embed()
		try:    success = success.values()
		except: pass
		# print(sum([v for v in success if v != None]),'out of',len(success))
		print(sum(success), 'out of', len(success))

def delete(infile, verbose=1):
	"""delete infile
	"""
	infile = str(Path(infile).expanduser())
	if path.isfile(infile):
		if verbose >= 1: print('deleting', infile)
		remove(infile)
