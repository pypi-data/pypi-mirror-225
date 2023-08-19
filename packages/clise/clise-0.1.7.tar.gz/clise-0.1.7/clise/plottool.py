
# Jaesub Hong (jhong@cfa.harvard.edu)
# to do
#     - log scale tick labeling
#     - multiplot for modeling fitting

if 'clise' in __file__:
	import clise.jsontool  as jt
	import clise.tabletool as tt
	# import clise.stattool  as st
else:
	import jsontool  as jt
	import tabletool as tt
	# import stattool  as st

from collections import OrderedDict

import pandas
import astropy
from   astropy.table import QTable
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from   matplotlib.colors import Normalize, LogNorm, ListedColormap
import matplotlib.cm     as cm
import matplotlib        as mpl
from matplotlib.dates import DateFormatter
# from matplotlib.patches           import Circle
# from matplotlib             import rcParams
# from matplotlib.ticker            import LogLocator
# from mpl_toolkits.axes_grid1  import make_axes_locatable
# from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import numpy as np
import math
import healpy as hp

from astropy.io import fits

# from scipy import optimize as opt
from scipy import interpolate

from os           import path
from functools    import wraps

# from IPython    import embed

# import subprocess
from scipy.signal import savgol_filter
from statsmodels.nonparametric.smoothers_lowess import lowess

import re
from pathlib      import Path

from datetime import datetime
from time import mktime, strptime
# ----------------------------------------------------------------------------------------
cc = jt.cc

# obsolete?
def help_rcParams():
	text = OrderedDict()
	text["figure.figsize"       ] = "changes the figure size; keeps the font size the same"
	text["figure.dpi"           ] = "changes the figure size; keep relative size of font to figure the same"
	text["font.size"            ] = "change the font size; keeps the figure size the same"

	text["axes.labelsize"       ] = "Fontsize of the x and y labels"
	text["axes.titlesize"       ] = "Fontsize of the axes title"
	text["figure.titlesize"     ] = "Size of the figure title (Figure.suptitle())"
	text["xtick.labelsize"      ] = "Fontsize of the tick labels"
	text["ytick.labelsize"      ] = "Fontsize of the tick labels"

	text["legend.fontsize"      ] = "Fontsize for legends (plt.legend(), fig.legend())"
	text["legend.title_fontsize"] = "Fontsize for legend titles, None sets to the same as the default axes."
	text["legend.facecolor"     ] = "Background color for legend"
	text["legend.edgecolor"     ] = "Edge color for legend"
	text["legend.framealpha"    ] = "Background alpha for legend: 0.5"
	text["legend.labelspacing"  ] = "Vertical spacing for legend: 0.5"
	text["legend.frameon"       ] = "Legend frame: true"
	text["legend.loc"           ] = "Location for legend: best"

	text["axes.grid" ] = "Grid True or False"
	text["grid.alpha"] = "Grid transparency"
	text["grid.color"] = "Grid color"

	text["xtick.direction"] = "xtick direction"
	text["ytick.direction"] = "ytick direction"
	return text

# obsolete?
def help_text(param):
	if param is not None:
		if param == "mpl":
			print("rcParams:")
			jt.show(help_rcParams(), notype=True)
			print("e.g., -*#rcParams:figure.figsize '12,10'")
			print
			print("See also", mpl.matplotlib_fname())
		elif param == "1d":
			print("Parameters for 1-d plot")
		elif param == "2d":
			print("Parameters for 2-d plot")
		elif param == "m1d":
			print("Parameters for 1-d plot for multiple data sets")
		elif param == "m2d":
			print("Parameters for 2-d plot for multiple data sets")
		elif param == "overview":
			print("decorator:")
			print("     prep_data_deco")
			print("     prep_model_deco")
			print("for one data set:")
			print("     plot1d     : 1-D plot, scatter, histogram, line ")
			print("     dplot      : 2-D density plot with 1-D histograms")
			print("     hp2mollview: healpix to mollview conversion")
			print("     plotDMR    : plot data, model & residual, usually for spectral fits")
			print("for multiple data sets:")
			print("     mplot1d       : 1-D plot, scatter, histogram, line ")
			print("     rplot1d       : 1-D ratio plot against one reference data set ")
			print("     mdplot        : 2-D density plot with 1-d histograms")
			print("     mdplot_3color : 2-D density plot of up-to 3 sets using true 3 color composite")
			print("     scan_fits_cols: plot all the columns of a fits file hdu")
			print("     scan_fits_hdus: plot a column of all the hdus of a fits hdu")
		else:
			print("params: overview mpl 1d 2d m1d m2d")

		exit()

# ----------------------------------------------------------------------------------------
def get_embed():
	from traitlets.config import Config

	from IPython.terminal.embed import InteractiveShellEmbed

	from IPython.terminal.prompts import Prompts, Token

	class MyPrompt(Prompts):
		def in_prompt_tokens(self, cli=None):
			return [
				(Token.PromptNum, str(self.shell.execution_count)),
				(Token.Prompt, '> '),
			]
#        return [  "❯❯ " ]

	def out_prompt_tokens(self, cli=None):
		return []

	c = Config()
	c.InteractiveShell.separate_in = ''
	c.TerminalInteractiveShell.prompts_class = MyPrompt
	c.TerminalInteractiveShell.highlighting_style_overrides = {
		Token.PromptNum: '#ef8888',
		Token.Prompt:    '#ef8888',
	}
	# return InteractiveShellEmbed(config=c) #, banner1='hello\n')

	ipyshell = InteractiveShellEmbed(config=c, banner1='', header='', banner='')
	# ipyshell(msg, stack_depth=2)
	return ipyshell

# why is this so convoluted?
#     to get interactive matplotlib and
#     to provide the information of where it stops
embed_core = get_embed()
def embed():
	import inspect
	# frame = inspect.currentframe().f_back
	# msg   = 'Stopped at {0.f_code.co_filename}: line {0.f_lineno}'.format(frame)
	# print(msg)
	frame, filename, lineno, function, lines, index = inspect.stack()[1]
	print('Stopped at', cc.key + filename + cc.reset + ':' + cc.type,
		lineno, cc.reset + 'in' + cc.hl, function, cc.reset)
	global embed_core
	embed_core(stack_depth=2)

enable_mpl_for_ion = False
def check_ion(ion):
	if ion:
		global enable_mpl_for_ion
		if not enable_mpl_for_ion:
			enable_mpl_for_ion = True
			embed_core.enable_matplotlib()
		plt.ion()
	else: plt.close('all')

# ----------------------------------------------------------------------------------------
class LogNorm_mid(LogNorm):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		LogNorm.__init__(self, vmin=vmin, vmax=vmax, clip=clip)
		self.mid = mid

	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [np.log(self.vmin), np.log(self.mid), np.log(self.vmax)], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(np.log(value), x, y))

class Norm_mid(Normalize):
	def __init__(self, vmin=None, vmax=None, mid=None, clip=False):
		Normalize.__init__(self, vmin=vmin, vmax=vmax, clip=clip)
		self.mid = mid

	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.mid, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y))

# ----------------------------------------------------------------------------------------
def minmax(data, nonzero=False):
	if nonzero:
		data = np.array(data)
		return [np.min(data[np.nonzero(data)]), np.max(data)]
	else:       return [np.min(data), np.max(data)]

# ----------------------------------------------------------------------------------------
# regex for scientific number
scino = re.compile(r'[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?')
def get_number(array, istime=''):
	# need to vectorize this....
	# and implement this in tabletool to separate them out
	# if type(array[0]) is not str: return array
	if istime == '':
		ans = []
		tformat=''
		for each in array:
			# val=re.split('(\D|^\.)',each)
			# val=re.search('^\s*([-\+][0-9.]+)',each)
			val = re.findall(scino, each)
			try: ans.append(float(val[0]))
			except Exception:
				ans.append(0.0)
				print('cannot find a number in', each)
	else:
		if ':' in istime: _, tformat = istime.split(':')
		else:	tformat="%y/%m/%d"
		ans = [datetime.strptime(v,tformat) for v in array]
		ans = np.array(ans)

	return ans, tformat

# ----------------------------------------------------------------------------------------
def read_pars(par,  data=None, nopandas=True, dataset=None, infile=None, comment=None):
	ans = OrderedDict()
	if dataset is None: dataset = OrderedDict()
	for key, val in par.items():
		if type(val) is str:
			ans[key] = data[val]
		else:
			if 'file' not in val: file = infile
			else:			    file = val['file']
			if not path.isfile(file):
				print("cannot read the file:", file)
				return None

			if file not in dataset:
				dataset[file] = tt.from_csv_or_fits(file, ftype=val.get('ftype', None),
										hdu=val.get('hdu', 1), nopandas=nopandas, comment=comment)
			ans[key] = dataset[file][val['column']]
	return ans

def read(infile, x="", y="", hdu=1, data=None,
		xlabel=None, ylabel=None,
		ftype=None, nopandas=True, attr='', columns=None, comment=None):
	if data is None:
		if infile is None:
			print(cc.err + "input data or file is required.", cc.reset)
			return None, None, None, None, None

		if not path.isfile(infile):
			print(cc.err + "cannot read the file:", infile, cc.reset)
			return None, None, None, None, None

		data = tt.from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas, columns=columns, comment=comment)

	if x == "" or y == "":
		if   type(data) is pandas.core.frame.DataFrame: colnames = data.columns.values.tolist()
		elif type(data) is   astropy.table.table.Table: colnames = data.colnames
		else: print('need to know column names or provide -x and -y')

		if x == "":
			if len(colnames) == 1: x = '_auto_'
			else:                  x = colnames[0]
		if y == "":
			if len(colnames) == 1: y = colnames[0]
			else:                  y = colnames[1]

	# default label
	if xlabel is None:
		if x != '_auto_' and x != '_range_' and x != '_range_log_':
			xlabel = x
			if hasattr(data[x], 'info'):
				if hasattr(data[x].info, 'unit'):
					xunit = data[x].info.unit
					if xunit is not None: xlabel = xlabel + ' (' + str(xunit) + ')'

	if ylabel is None:
		attrs = attr.split(',')
		if 'makehist' not in attrs:
			ylabel = y
			if hasattr(data[y], 'info'):
				if hasattr(data[y].info, 'unit'):
					yunit = data[y].info.unit
					if yunit is not None: ylabel = ylabel + ' (' + str(yunit) + ')'
		else:
			ylabel = 'counts'

	return data, x, y, xlabel, ylabel

def read_img(filename, hdu=None):
	filename = str(Path(filename).expanduser())
	basename = path.basename(filename)

	# regular image
	if bool(re.search(r'\.tif(|f)$', basename)):
		from PIL import Image
		return np.array(Image.open(filename))
	else:
		# otherwise assume it's a fits file
		# too presumptuous, but ...
		hdul = fits.open(filename)
		if hdu is None: hdu = 0
		# image=np.transpose(hdul[hdu].data)
		return hdul[hdu].data

def set_range(data, margin=None,
			dr=None,  # data range
			dmin=None, dmax=None,
			scale='linear', drawdown=None):

	if type(dr) is list:
		if dr[0] is None: dr = None

	if dr is None: dr = minmax(data, nonzero=scale != 'linear')

	if dmin is not None: dr[0] = dmin
	if dmax is not None: dr[1] = dmax

	if margin is not None:
		dr = add_margin(dr, margin=margin, scale=scale, drawdown=drawdown)

	return dr

def set_range_2D(xdata, ydata, margin=None, xr=None, yr=None,
			xmin=None, xmax=None, ymin=None, ymax=None,
			xlowdata=None, xhighdata=None, xerrdata=None,
			ylowdata=None, yhighdata=None, yerrdata=None,
			attr='', nbin=None, binsize=None,
			xscale='linear', yscale='linear', drawdown=None):

	if type(xr) is list:
		if xr[0] is None: xr = None
	if type(yr) is list:
		if yr[0] is None: yr = None

	ignore_xr = False
	ignore_yr = False
	if xr is None:
		ignore_xr = True
		if xlowdata is not None:
			xr = minmax(np.concatenate((np.array(xlowdata), np.array(xhighdata))), nonzero=xscale != 'linear')
		elif xerrdata is not None:
			xr = minmax(np.concatenate((np.array(xdata) - np.array(xerrdata), np.array(xdata) + np.array(xerrdata))), nonzero=xscale != 'linear')
		else:
			xr = minmax(xdata, nonzero=xscale != 'linear')

	if yr is None:
		ignore_yr = True
		if ylowdata is not None:
			yr = minmax(np.concatenate((np.array(ylowdata), np.array(yhighdata))), nonzero=yscale != 'linear')
		elif yerrdata is not None:
			yr = minmax(np.concatenate((np.array(ydata) - np.array(yerrdata), np.array(ydata) + np.array(yerrdata))), nonzero=yscale != 'linear')
		else:
			yr = minmax(ydata, nonzero=yscale != 'linear')

	if xmin is not None: xr[0] = xmin
	if xmax is not None: xr[1] = xmax
	if ymin is not None: yr[0] = ymin
	if ymax is not None: yr[1] = ymax

	edges = None
	attrs = attr.split(',')
	if 'makehist' in attrs:
		if ignore_xr or ignore_yr:
			if binsize is None: binsize = (xr[1] - xr[0]) / nbin
			else:               nbin = int((xr[1] - xr[0]) / binsize)

			edges = get_edges(xr, nbin, scale=xscale)
			new_y, *_ = np.histogram(xdata, bins=edges)
			xh, yh, new_x = hist2line(edges, new_y)

			if ignore_xr: xr = None
			if ignore_yr: yr = None
			xr, yr, edges = set_range_2D(new_x, new_y, xr=xr, yr=yr,
				xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
				margin=margin, drawdown=drawdown,
				xlowdata=xlowdata, xhighdata=xhighdata, xerrdata=xerrdata,
				ylowdata=ylowdata, yhighdata=yhighdata, yerrdata=yerrdata,
				xscale=xscale, yscale=yscale)
	else:
		if margin is not None:
			if type(margin) is not list:
				xr = add_margin(xr, margin=margin, scale=xscale, drawdown=drawdown)
				yr = add_margin(yr, margin=margin, scale=yscale, drawdown=drawdown)
			elif len(margin) == 2:
				xr = add_margin(xr, margin=margin[0], scale=xscale, drawdown=drawdown)
				yr = add_margin(yr, margin=margin[1], scale=yscale, drawdown=drawdown)
			elif len(margin) == 4:
				xr = add_margin(xr, margin=margin[0:2], scale=xscale, drawdown=drawdown)
				yr = add_margin(yr, margin=margin[2:4], scale=yscale, drawdown=drawdown)

	return xr, yr, edges

def get_log_edges(vr, nbin):
	logvr = [math.log(vr[0], 10), math.log(vr[1], 10)]
	logslope = logvr[1] - logvr[0]
	return [10.0**(logslope * v / nbin + logvr[0]) for v in range(0, nbin + 1)]

def get_edges(vr, nbin, scale='linear'):
	if scale == 'linear':
		step = (vr[1] - vr[0]) / nbin
		return [v * step + vr[0] for v in range(0, nbin + 1)]
	elif scale == 'log':
		logvr = [math.log(vr[0], 10), math.log(vr[1], 10)]
		logslope = logvr[1] - logvr[0]
		return [10.0**(logslope * v / nbin + logvr[0]) for v in range(0, nbin + 1)]

def get_low(low, scale='linear', range=None):
	if low <= 0:
		if scale == 'log':
			if len(range) == 2:
				if range[0] is not None: low = range[0]
	return low

def add_margin(prange, margin=None, scale='linear', drawdown=None):

	if   margin is None     : margin = [0.2,    0.2]
	elif np.isscalar(margin): margin = [margin, margin]
	if scale == 'linear':
		diff = prange[1] - prange[0]
		prange = [prange[0] - margin[0] * diff, prange[1] + margin[1] * diff]
	else:
		if prange[0] <= 0.0:
			if drawdown is None: drawdown = 1.e-5
			prange[0] = prange[1] * drawdown

		logpr  = [math.log(v, 10) for v in prange]
		diff   = logpr[1] - logpr[0]
		logpr  = [logpr[0] - margin[0] * diff, logpr[1] + margin[1] * diff]
		prange = [10.0**v for v in logpr]

	return prange

def filter_by_range(xdata, ydata, xr, yr, weights=None):
	# embed()
	# xdata=np.array(xdata)
	# ydata=np.array(ydata)
	mask = (xdata >= xr[0]) & (xdata <= xr[1]) & (ydata >= yr[0]) & (ydata <= yr[1])
	xdata = xdata[mask]
	ydata = ydata[mask]

	if weights is not None: weights = weights[mask]
	# if filter:
	#      data=data[data[x] >= xr[0]]
	#      data=data[data[x] <= xr[1]]
	#      data=data[data[y] >= yr[0]]
	#      data=data[data[y] <= yr[1]]

	return xdata, ydata, weights

def val2pix(val, vr=None, pr=None):
	# value to pixel
	slope = (pr[1] - pr[0]) / (vr[1] - vr[0])
	if type(val) is not list:
		return int(slope * (val - vr[1]) + pr[0])
	return [int(slope * (v - vr[1]) + pr[0]) for v in val]

def pix2val(pix, vr=None, pr=None):
	# pixel to value
	slope = (vr[1] - vr[0]) / (pr[1] - pr[0])
	if type(pix) is not list:
		return slope * (pix - pr[0]) + vr[0]
	return [slope * (p - pr[0]) + vr[0] for p in pix]

# ----------------------------------------------------------------------------------------
def set_rcParams(rcParams=None, verbose=0, force=False, name=None):
	# run only once unless forced
	if not force:
		if hasattr(set_rcParams, 'new'): return
	set_rcParams.new = False

	defaults = OrderedDict()
	if rcParams is None:
		if name is None: return
		elif name == "dplot":
			defaults["xtick.top"       ] = False
			defaults["ytick.right"     ] = False
			defaults["axes.grid"       ] = False
			defaults["xtick.direction" ] = "out"
			defaults["ytick.direction" ] = "out"
		else: return
		rcParams = OrderedDict()

	for key, val in rcParams.items():
		if verbose >= 2: print(key, val)
		plt.rcParams[key] = val

	for key in defaults.keys() - rcParams.keys():
		if verbose >= 2: print(key, defaults[key])
		plt.rcParams[key] = defaults[key]
	# embed()

# ----------------------------------------------------------------------------------------
def wrap(plt, xr=None, yr=None, xlabel=None, ylabel=None, fig=None,
		title="", xscale='linear', yscale='linear', outfile=None,
		y_title=1.0, rect=[0, 0, 1, 1],
		ax2=None, ay2=None, ax=None,
		xlabel2=None, ylabel2=None,
		xr2=None, yr2=None, tight=True,
		xticks=None, yticks=None,
		xtickv=None, ytickv=None, grid=None,
		text=None, text_kw=None,
		polygon=None, polygon_kw={},
		ellipse=None, ellipse_kw={},
		line=None, line_kw={},
		loc_ylabel='center',  # rcParams=None,
		xscale2=None, yscale2=None, gwhich='major',
		xtformat=None, ytformat=None,
		label=True, display=True, ion=False):

	# if rcParams is not None:
	# 	set_rcParams(rcParams, force=True, name=None)

	if label:
		if xlabel is not None: ax.set_xlabel(xlabel)
		if ax2 is not None:
			if xlabel2 is not None:
				# print(ax2, xlabel2)
				ax2.set_xlabel(xlabel2)

		if ylabel is not None: ax.set_ylabel(ylabel, loc=loc_ylabel)
		if ay2 is not None:
			if ylabel2 is not None:
				ay2.set_ylabel(ylabel2)
		# this needs a clean up
		plt.title(title, y=y_title)

	if xr is not None: ax.set_xlim(xr)
	if ax2 is not None:
		if xr2 is not None: ax2.set_xlim(xr2)

	if yr is not None: ax.set_ylim(yr)
	if ay2 is not None:
		if yr2 is not None: ay2.set_ylim(yr2)

	add_line(data=line, common_kwargs=line_kw, ax=ax)
	# if xscale is not None: plt.xscale(xscale)
	# if yscale is not None: plt.yscale(yscale)
	aux_xtick = False
	if xscale is not None and ax is not None:
		ax.set_xscale(xscale)
		if xscale == "log":
			xr = ax.get_xlim()
			if xr[1] / xr[0] < 100:
				aux_xtick = True
	if ax2 is not None:
		if xscale2 is None:
			if xscale is not None: ax2.set_xscale(xscale)
		else:                        ax2.set_xscale(xscale2)
	aux_ytick = False
	if yscale is not None and ax is not None:
		ax.set_yscale(yscale)
		if yscale == "log":
			yr = ax.get_ylim()
			if yr[1] / yr[0] < 100:
				aux_ytick = True
	if ay2 is not None:
		if yscale2 is None:
			if xscale is not None: ay2.set_yscale(yscale)
		else:                        ay2.set_yscale(yscale2)

	annotate    (data=text    , common_kwargs=text_kw    )
	add_polygon (data=polygon , common_kwargs=polygon_kw )
	add_ellipse (data=ellipse , common_kwargs=ellipse_kw, ax=ax)

	if xticks is not None and ax is not None:
		if xtickv is None: xtickv = [float(v) for v in xticks]
		ax.set_xticks(xtickv, xticks)
		# ax.set_xticks(xtickv)
	if yticks is not None and ax is not None:
		if ytickv is None: ytickv = [float(v) for v in yticks]
		ax.set_yticks(ytickv, yticks)

	if xtformat is not None:
		if xtformat != '':
			date_form = DateFormatter(xtformat)
			ax.xaxis.set_major_formatter(date_form)
	if ytformat is not None:
		if ytformat != '':
			date_form = DateFormatter(ytformat)
			ax.yaxis.set_major_formatter(date_form)

	if tight:
		plt.tight_layout(rect=rect)

	if grid is not None:
		if type(grid) is bool:
			if grid is True:
				ax.grid(True, which=gwhich)
				if ax2 is not None: ax2.grid(False, which=gwhich)
				if ay2 is not None: ay2.grid(False, which=gwhich)
			else:
				ax.grid(False, which=gwhich)
				if ax2 is not None: ax2.grid(False, which=gwhich)
				if ay2 is not None: ay2.grid(False, which=gwhich)
		else:
			if type(grid) is str: grid = [grid]
			if ax2 is not None and ay2 is not None:
				if 'ax2' in grid and 'ay2' in grid:
					ax2.grid(True, axis='x', which=gwhich)
					ay2.grid(True, axis='y', which=gwhich)
			elif ax2 is not None:
				if 'ax2' in grid:
					ax.grid(True, axis='y', which=gwhich)
					ax2.grid(True, axis='x', which=gwhich)
			elif ay2 is not None:
				if 'ay2' in grid:
					ax.grid(True, axis='x', which=gwhich)
					ax2.grid(True, axis='y', which=gwhich)
	if fig is not None:
		all_axes = fig.get_axes()
		for axis in all_axes:
			legend = axis.get_legend()
			if legend is not None:
				legend.remove()
				all_axes[-1].add_artist(legend)
	if not ion:
		if outfile is not None:
			plt.savefig(Path(outfile).expanduser())
			plt.close("all")
		else:
			if display: plt.show()

def colorbar_multivertical(im, ax, fig, label,
			rect=[1.01, 0.0, 0.03, 1], gap=0.03, ticklocation='right'):

	nbar = len(im)
	vsize = (rect[3] - gap * (nbar - 1)) / nbar
	ii = 0
	for key in im:
		cax = ax.inset_axes([rect[0], (vsize + gap) * ii + rect[1], rect[2], vsize])  # , transform=ax.transAxes)
		cb  = fig.colorbar(im[key], pad=0.01, label=label[key], cax=cax, ticklocation=ticklocation)
		cb.ax.tick_params(direction='out')
		cb.ax.tick_params(direction='out', which='minor')
		ii = ii + 1

def colorbar_multihorizontal(im, ax, fig, label,
			rect=[0.0, 1.01, 1.0, 0.05], gap=0.03, ticklocation='top'):

	nbar = len(im)
	hsize = (rect[2] - gap * (nbar - 1)) / nbar
	ii = 0
	for key in im:
		cax = ax.inset_axes([rect[0] + (hsize + gap) * ii, rect[1], hsize, rect[3]])  # , transform=ax.transAxes)
		cb  = fig.colorbar(im[key], pad=0.01, label=label[key], cax=cax,
					ticklocation=ticklocation, orientation='horizontal')
		cb.ax.tick_params(direction='out')
		cb.ax.tick_params(direction='out', which='minor')
		ii = ii + 1

def colorbar_multi(_im, ax, fig, _label,
			rect=[1.01, 0.0, 0.03, 1], gap=0.03, ticklocation='right', orientation='vertical'):
	if type(_im).__name__ == 'OrderedDict':
		im = _im
		label = _label
	else:
		im    = OrderedDict()
		im[0] = _im
		label = OrderedDict()
		label[0] = _label

	if orientation == 'vertical':
		colorbar_multivertical(im, ax, fig, label, rect=rect, gap=gap, ticklocation=ticklocation)
	else:
		colorbar_multihorizontal(im, ax, fig, label, rect=rect, gap=gap, ticklocation=ticklocation)

def tick_orientation(cbar, ticklocation=None, orientation=None):
	if orientation is None:
		if cbar[2] > cbar[3]: orientation = 'horizontal'
		else:                 orientation = 'vertical'
	if ticklocation is None:
		if orientation == 'vertical':
			if cbar[0] > 0.5: ticklocation = 'right'
			else:             ticklocation = 'left'
		else:
			if cbar[1] > 0.5: ticklocation = 'top'
			else:             ticklocation = 'bottom'
	return ticklocation, orientation

def colorbar(im, ax, fig, label,
			cbar=None, gap=None, ticklocation=None, orientation=None,
			hsize=0.0, xhist=False, yhist=False, loc_ylabel=None, y_title=None):

	if y_title is None: y_title = 1.0
	if xhist:
		yhsize  = 0.05 * hsize
		y_title = 1.0 + hsize
	else: yhsize  = 0.0

	if yhist: xhsize = 0.05 * hsize
	else:     xhsize = 0.0
	rect = [0, 0, 1. + xhsize, 1.0 + yhsize]

	if type(cbar) is bool:
		if cbar:
			if xhist and yhist:
				cbar = [-0.15, 0.0, 0.03, 0.6]
				if gap is None: gap = 0.02
				if loc_ylabel is None: loc_ylabel = 'top'
			elif yhist:
				cbar = [0.0, 1.01, 1.00, 0.03]
				if gap is None: gap = 0.03
			else:
				colorbar_multi(im, ax, fig, label)
				return rect, loc_ylabel, y_title

	if type(cbar) is list:
		cbar = [float(v) for v in cbar]

		ticklocation, orientation = tick_orientation(cbar,
									ticklocation=ticklocation, orientation=orientation)

		colorbar_multi(im, ax, fig, label,
					rect=cbar, gap=gap,
					ticklocation=ticklocation,
					orientation=orientation)

	return rect, loc_ylabel, y_title

def despine_axes(ax, despine):
	if despine is None: despine = False
	if type(despine) is bool:
		if despine:
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
	else:
		for each in despine.split(','):
			ax.spines[each].set_visible(False)

# ----------------------------------------------------------------------------------------
def hist2line(edges, values):
	edges = np.array(edges)
	values = np.array(values)
	x, y = [edges[0]], [values[0]]
	c = []
	for i in range(1, len(values)):
		x.append(edges[i])
		x.append(edges[i])
		y.append(values[i - 1])
		y.append(values[i])
		c.append((edges[i - 1] + edges[i]) * 0.5)
	x.append(edges[-1])
	y.append(values[-1])
	c.append((edges[-2] + edges[-1]) * 0.5)
	return x, y, c

# ----------------------------------------------------------------------------------------
# routines for addition to plots
def annotate(data=None, common_kwargs={}):
	if data is None: return

	for kwargs in data:
		kwargs_ = kwargs.copy()
		t = kwargs_.pop('t')
		x = kwargs_.pop('x')
		y = kwargs_.pop('y')
		for key in common_kwargs:
			if key not in kwargs_:
				kwargs_[key] = common_kwargs[key]
		plt.text(x, y, t, **kwargs_)

def add_polygon(data=None, common_kwargs={}):
	if data is None: return

	for kwargs in data:
		kwargs_ = kwargs.copy()
		x = kwargs_.pop('x')
		y = kwargs_.pop('y')
		for key in common_kwargs:
			if key not in kwargs_:
				kwargs_[key] = common_kwargs[key]
		plt.plot(x, y, **kwargs_)

def add_ellipse(data=None, common_kwargs={}, ax=None):
	if data is None: return
	from matplotlib.patches import Ellipse
	from matplotlib.transforms import ScaledTranslation

	for kwargs in data:
		kwargs_ = kwargs.copy()
		x0 = kwargs_.pop('x')
		y0 = kwargs_.pop('y')
		r = kwargs_.pop('w')
		try:
			s = kwargs_.pop('h')
			t = kwargs_.pop('t')
		except Exception:
			s = r
			t = 0.0

		for key in common_kwargs:
			if key not in kwargs_:
				kwargs_[key] = common_kwargs[key]

		# these are for log scale: does this work for linear scale as well? yes

		# use the axis scale tform to figure out how far to translate
		ell_offset = ScaledTranslation(x0, y0, ax.transScale)
		# construct the composite tform
		ell_tform = ell_offset + ax.transLimits + ax.transAxes

		try: _, h = ax.transScale.transform((x0, s[1])) - ax.transScale.transform((x0, s[0]))
		except Exception: h = s

		try: w, _ = ax.transScale.transform((r[1], y0)) - ax.transScale.transform((r[0], y0))
		except Exception: w = r

		ellipse = Ellipse((0, 0), width=w, height=h, angle=t, **kwargs_, transform=ell_tform)
		ax.add_patch(ellipse)

		# plt.plot(x, y, **kwargs_)

def add_line(data=None, common_kwargs={}, ax=None):
	if data is None: return

	x_ = ax.get_xbound()
	y_ = ax.get_ybound()
	for kwargs in data:
		kwargs_ = kwargs.copy()
		if 'x' in kwargs_:
			x = [kwargs_.pop('x')] * 2
			y = y_
		if 'y' in kwargs_:
			y = [kwargs_.pop('y')] * 2
			x = x_
		for key in common_kwargs.keys():
			if key not in kwargs_:
				kwargs_[key] = common_kwargs[key]
		plt.plot(x, y, **kwargs_)

# ----------------------------------------------------------------------------------------
# common core plotting routine for plot1d
def plot1d_core(x, y, z=None, attr=None,
			xscale='linear', yscale='linear',
			xlow=None, xhigh=None, ylow=None, yhigh=None,
			xerr=None, yerr=None, xlerr=None, ylerr=None,
			color=None, label=None, alpha=None,
			errcolor=None, erralpha=None, errzorder=None,
			marker=None, markersize=None, linestyle=None, linewidth=None,
			ax=None, ax2=None, ay2=None, cmap='turbo',
			binsize=None, nbin=None, edges=None,
			xr=None, yr=None, zorder=None, zlog=None, zlabel='',
			smooth=None, smpars=None,  smcolor=None, smlinewidth=None, smzorder=None,
			datfile=None, overwrite=True,
			colnames=['x', 'y'], units=['', ''], extname='Plottool',
			altx=False, alty=False, add_ax2=False, add_ay2=False):

	at = ax
	if alty or add_ay2:
		if ay2 is None:
			ay2 = ax.twinx()
			if alty:
				ay2.yaxis.label.set_color(color)
				ay2.tick_params(axis='y', colors=color)
				ay2.tick_params(axis='y', colors=color, which='minor')
				ay2.spines['right'].set_color(color)
				at = ay2

	elif altx or add_ax2:
		if ax2 is None:
			ax2 = ax.twiny()
			if altx:
				ax2.xaxis.label.set_color(color)
				ax2.tick_params(axis='x', colors=color)
				ax2.tick_params(axis='x', colors=color, which='minor')
				ax2.spines['top'].set_color(color)
				at = ax2

	# if len(x) == len(y) +1:
	attrs = attr.split(',')

	# check if the data is time
	# xtmat = [s for s in attrs if "xtime" in s]
	# ytmat = [s for s in attrs if "ytime" in s]
	# if len(xtmat) >0:
	# 	if ':' in xtmat[0]: _, tformat = xtmat[0].split(':')
	# 	else:	tformat="%y/%m/%d"
	# 	x = [datetime.strptime(v,tformat) for v in x]
	# 	x = np.array(x)
	# if len(ytmat) >0:
	# 	if ':' in ytmat[0]: _, tformat = ytmat[0].split(':')
	# 	else:	tformat="%y/%m/%d"
	# 	y = [datetime.strptime(v,tformat) for v in y]
	# 	y = np.array(y)
	#
	if 'hist' in attrs:
		# we assume this is for histogram
		if type(x).__name__ != 'ndarray': x = np.array(x)
		if type(y).__name__ != 'ndarray': y = np.array(y)
		if len(x) == len(y) + 1:
			xh, yh, xc = hist2line(x, y)
			x = xc
		elif len(x) == len(y):
			extend = np.concatenate([x[0] * 2 - x[1], x, x[-1] * 2 - x[-2]], axis=None)
			roll  = np.roll(extend, 1)
			edges = (extend + roll) / 2
			xh, yh, xc = hist2line(edges[1:], y)
		pid, = at.plot(xh, yh,
			color=color, label=label, alpha=alpha,
			marker=None, linestyle=linestyle, linewidth=linewidth)
		pid_, = at.plot(x, y,
			color=color,  alpha=alpha,
			marker=marker, linestyle='none')
		# print('here', len(x), len(y), len(xc), len(xh), len(yh))
		# x, y

	elif 'makehist' in attrs:
		# we assume this is to make a new histogram
		if edges is None:
			if binsize is None: binsize = (xr[1] - xr[0]) / nbin
			else:               nbin = int((xr[1] - xr[0]) / binsize)

			edges = get_edges(xr, nbin, scale=xscale)
			# y, *_ = np.histogram(x, bins=edges)

		xh, xedges, _ = at.hist(x, bins=edges, histtype='stepfilled',
					facecolor=color, label=label,
					# weights=weights,
					alpha=alpha)
		xh, xedges, _ = at.hist(x, bins=edges, histtype='step',
					# weights=weights,
					edgecolor=color)

		# xh, yh, x = hist2line(edges, y)
		# xedges, xh
		x = xedges[:-1]
		y = xh

		pid = at

	else:
		if zorder is None: zorder = 10

		if smooth is None:
			if errzorder is None: errzorder = zorder - 1
			if z is None:
				pid, = at.plot(x, y,
					color=color, label=label, alpha=alpha,
					marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth, zorder=zorder)
			else:
				# this needs more work: extend to size, colos & size, etc...
				# need pid for scatter.plot
				pid = None
				if 'color' in attr:
					norm = None
					if zlog: norm = mpl.colors.LogNorm()
					im_ = at.scatter(x, y,
						c=z, label=label, alpha=alpha, cmap=cmap,
						marker=marker,
						s=markersize,
						norm=norm,
						linestyle=linestyle, linewidth=linewidth, zorder=zorder)

					im = OrderedDict()
					im[0] = im_
					label = OrderedDict()
					label[0] = zlabel
					colorbar_multivertical(im, at, plt, label,
						rect=[1.01, 0.0, 0.03, 1], gap=0.03, ticklocation='right')
					# plt.colorbar(im, pad=0.01)

			# x, y, [xerr, yerr]

		else:
			if type(y) is list: y = np.array(y)
			if type(y) is pandas.core.series.Series: y_sm = y.copy()
			else: y_sm = np.array([v for v in y])
			finite = np.isfinite(y)

			# if savgol is None: savgol = [11, 2]
			# y_sm[finite] = savgol_filter(y[finite], savgol[0], savgol[1])
			if type(x[0]).__name__ == 'datetime':
				x0 = x[0].timestamp()
				x_sm = [v.timestamp() - x0 for v in x]
			else: 
				x0 = x[0]
				x_sm = x - x0
			if type(x_sm) is list: x_sm = np.array(x_sm)

			if 'savgol' in smooth:
				y_sm[finite] = savgol_filter(y[finite], smpars[0], smpars[1])
				x_sm = x_sm + x0

			elif 'lowess' in smooth:
				filtered = lowess(y[finite], x_sm[finite], **smpars)
				y_sm = filtered[:,1]
				# need to convert back to datetime if x is datetime
				# and change x below to x_sm
				if type(x[0]).__name__ == 'datetime':
					x_sm = [datetime.fromtimestamp(v + x0) for v in filtered[:,0]]
				else: 
					x_sm = filtered[:,0] + x0

			if smzorder is None: smzorder = zorder + 1

			if 'replace' in smooth:
				pid, = at.plot(x_sm, y_sm,
					color=color, label=label, alpha=alpha,
					marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth, zorder=zorder)
			elif 'overlay' in smooth:
				pid, = at.plot(x, y,
					color=color, label=label, alpha=alpha,
					marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth, zorder=zorder)
				if smcolor     is None: smcolor     = color
				if smlinewidth is None: smlinewidth = linewidth
				pid_, = at.plot(x_sm, y_sm,
					color=smcolor, label=smooth,
					linewidth=smlinewidth, linestyle='solid', zorder=smzorder)
			# x, y, y_sm
		if errcolor is None: errcolor = color
		if erralpha is None: erralpha = alpha

		if yerr is not None:
			if ylerr is None:
				for ex, ey, err in zip(x, y, yerr):
					low = get_low(ey - err, scale=yscale, range=yr)
					pid_, = at.plot([ex, ex], [low, ey + err],
						color=errcolor,  alpha=erralpha,
						marker=None, linestyle='solid', zorder=errzorder)
			else:
				for ex, ey, err, lerr in zip(x, y, yerr, ylerr):
					low = get_low(ey + lerr, scale=yscale, range=yr)
					pid_, = at.plot([ex, ex], [low, ey + err],
						color=errcolor,  alpha=erralpha,
						marker=None, linestyle='solid', zorder=errzorder)

		if xerr is not None:
			if xlerr is None:
				for ex, ey, err in zip(x, y, xerr):
					low = get_low(ex - err, scale=xscale, range=xr)
					pid_, = at.plot([low, ex + err], [ey, ey],
						color=errcolor,  alpha=erralpha,
						marker=None, linestyle='solid', zorder=errzorder)
			else:
				for ex, ey, err, lerr in zip(x, y, xerr, xlerr):
					low = get_low(ex + lerr, scale=xscale, range=xr)
					pid_, = at.plot([low, ex + err], [ey, ey],
						color=errcolor,  alpha=erralpha,
						marker=None, linestyle='solid', zorder=errzorder)

		if xlow is not None:
			for ex, ey, elow, ehigh in zip(x, y, xlow, xhigh):
				elow = get_low(elow, scale=xscale, range=xr)
				pid_, = at.plot([elow, ehigh], [ey, ey],
					color=errcolor,  alpha=erralpha,
					marker=None, linestyle='solid', zorder=errzorder)

		if ylow is not None:
			for ex, ey, elow, ehigh in zip(x, y, ylow, yhigh):
				elow = get_low(elow, scale=yscale, range=yr)
				pid_, = at.plot([ex, ex], [elow, ehigh],
					color=errcolor,  alpha=erralpha,
					marker=None, linestyle='solid', zorder=errzorder)

	if 'poisson_error' in attrs:
		for exc, ey in zip(x, y):
			err = math.sqrt(ey)
			pid_, = at.plot([exc, exc], [ey - err, ey + err],
				color=color,  alpha=alpha,
				marker=None, linestyle='solid')

	if datfile is not None:
		pdt = QTable([x, y], names=colnames, units=units, meta={'extname': extname})
		tt.to_fits(datfile, pdt, overwrite=overwrite)

	return pid, ax2, ay2

def plotDMR_core(xdata=None, ydata=None, mdata=None, rdata=None, pdata=None, data=None,
			mcxdata=None, mcdata=None, mcdeco=None,         # module component x, data
			xr=None, yr=None, rr=None,
			xerrdata=None, yerrdata=None,
			xlowdata=None, xhighdata=None,
			ylowdata=None, yhighdata=None,
			mx=None, my=None, mc=None,
			marker='None',   linestyle='None',   color='black',  # for data
			emarker='None', elinestyle='solid', ecolor='black',  # for data error or range
			mmarker='None', mlinestyle='solid', mcolor='red',    # for model
			rmarker='None', rlinestyle='None',  rcolor='black',  # for residual
			smarker='None', slinestyle='solid', scolor='black',  # for residual error or range
			rtype='relative',
			pfontsize=8, pfontfamily="monospace",
			ax=None, ax2=None, label=None):

	pcolor = ["green", "blue", "purple", "magenta", "brown", "orange"]
	icolor = 0
	lcolor = len(pcolor)

	label_statistic = ""
	if hasattr(data, 'meta'):
		header = data.meta
		if "RCHI2" in header:
			label_statistic = label_statistic + "$\chi_r^2$ = %.2f" % (header["RCHI2"])
		if "DOF" in header:
			label_statistic = label_statistic + "  DoF = %d" % (header["DOF"])

	else:
		header = {}

	# plot models
	if type(mdata).__name__ == 'Table':
		ncols = len(mdata.columns)
	else:
		ncols = len(mdata.shape)

	if ncols == 1:
		# plot the overall model
		ax.plot(xdata, mdata, color=mcolor, marker=mmarker, linestyle=mlinestyle)
	else:
		# plot the model components
		if (mx is not None) and (my is not None):
			ax.plot(mdata[mx], mdata[my], color=mcolor, marker=mmarker, linestyle=mlinestyle)
			idx = 1
			while True:
				try:
					mcdata = mdata[mc + str(idx)]
				except Exception:
					break
				ax.plot(mdata[mx], mcdata, color=pcolor[icolor], marker=mmarker, linestyle=mlinestyle)
				icolor = (icolor + 1) % lcolor
				idx = idx + 1

	# plot data
	pid, = ax.plot(xdata, ydata, color=color, marker=marker, linestyle=linestyle, label=label)

	# plot x and y error bars
	if xlowdata is None:
		xlowdata  = xdata - xerrdata
		xhighdata = xdata + xerrdata
	if ylowdata is None:
		ylowdata  = ydata - yerrdata
		yhighdata = ydata + yerrdata

	for ex, ey, exlow, exhigh in zip(xdata, ydata, xlowdata, xhighdata):
		ax.plot([exlow, exhigh], [ey, ey], color=ecolor, marker=emarker, linestyle=elinestyle)

	for ex, ey, eylow, eyhigh in zip(xdata, ydata, ylowdata, yhighdata):
		ax.plot([ex, ex], [eylow, eyhigh], color=ecolor, marker=emarker, linestyle=elinestyle)

	# add fit parameter labels
	# will add more options
	if pdata is not None:
		lineno = 0
		for row in pdata:
			if row['frozen']: continue
			color_ = mcolor
			if 'addcompno' in row.colnames:
				if row['addcompno'] > 0:
					color_ = pcolor[(row['addcompno'] - 1) % lcolor]
			t = ax.text(0.88, 0.95 - lineno * 0.04, row['aka'] + '.' + row['parameter'] + ': ',
				fontsize=pfontsize, fontfamily=pfontfamily, color=color_,
				horizontalalignment='right', transform=ax.transAxes)
			t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))
			lineno = lineno + 1
		lineno = 0
		addidx = 0
		for row in pdata:
			if row['frozen']: continue
			color_ = mcolor
			if 'addcompno' in row.colnames:
				if row['addcompno'] > 0:
					color_ = pcolor[ (row['addcompno'] - 1) % lcolor]
			t = ax.text(0.88, 0.95 - lineno * 0.04, "%.2e" % (row['value']),
				fontsize=pfontsize, fontfamily=pfontfamily, color=color_,
				horizontalalignment='left', transform=ax.transAxes)
			t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))
			lineno = lineno + 1

	# plot residuals
	ax2.plot(xdata, rdata, color=rcolor, marker=rmarker, linestyle=rlinestyle)

	# plot residual x range
	for ex, ey, exlow, exhigh in zip(xdata, rdata, xlowdata, xhighdata):
		ax2.plot([exlow, exhigh], [ey, ey], color=scolor, marker=smarker, linestyle=slinestyle)

	# plot residual y error range
	if rtype == 'relative':
		for ex, ey in zip(xdata, rdata):
			ax2.plot([ex, ex], [-1 + ey, 1 + ey], color=scolor, marker=smarker, linestyle=slinestyle)
	elif rtype == 'absolute':
		for ex, eylow, eyhigh in zip(xdata, ylowdata - ydata + rdata, yhighdata - ydata + rdata):
			ax2.plot([ex, ex], [eylow, eyhigh], color=scolor, marker=smarker, linestyle=slinestyle)

	t = ax2.text(0.03, 0.1, label_statistic, horizontalalignment='left', transform=ax2.transAxes)
	t.set_bbox(dict(alpha=0.5, facecolor="white", edgecolor="none", pad=0))

	return pid

# ----------------------------------------------------------------------------------------
# common core plotting routine for dplot
def get_bin(binsize, nbin, binr, nbinr, rr):

	if binsize is not None:  binr = binsize
	if nbin    is not None: nbinr = nbin

	if binr is None: binr  = (rr[1] - rr[0]) / nbinr
	else:            nbinr = int((rr[1] - rr[0]) / binr)

	return binr, nbinr

def edges_to_data(xedges, yedges,
				xr=None, binx=None, nbinx=None,
				yr=None, biny=None, nbiny=None):

	if type(xedges) is not list:
		xedges_ = [ii * binx + xr[0] + binx * 0.5 for ii in range(0, nbinx)]
	else:
		xedges_ = [(v + w) * 0.5 for v, w in zip(xedges[:-1:], xedges[1::])]

	xdata   = [[v]  * nbiny for v in xedges_]
	xdata   = np.array(xdata).flatten()
	# xdata   = xedges_ * nbiny

	if type(yedges) is not list:
		yedges_ = [ii * binx + yr[0] + binx * 0.5 for ii in range(0, nbiny)]
	else:
		yedges_ = [(v + w) * 0.5 for v, w in zip(yedges[:-1:], yedges[1::])]
	ydata   = yedges_ * nbinx

	return xdata, ydata

def get_norm(zlog=None, zmid=None, zmin=None, zmax=None, zr=None, zlthresh=None, zlscale=None):
	if zr is not None:
		zmin = zr[0]
		zmax = zr[1]
	if not zlog:

		if zmid is not None:
			norm = colors.CenteredNorm(zmid)  # , vmin=zmin, vmax=zmax)
		else:
			norm = colors.Normalize(vmin=zmin, vmax=zmax)

	else:
		# log, with negative

		zclip = True
		if zmin > 0:
			norm = colors.LogNorm(vmin=zmin, vmax=zmax, clip=zclip)
		elif zmin < 0:
			if zlthresh is None: zlthresh = -zmin
			if zlscale  is None: zlscale = -zmin / zmax
			norm = colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
		else:
			if zlthresh is None: zlthresh = zmax / 1.e3
			if zlscale  is None: zlscale = 0.2
			norm = colors.SymLogNorm(vmin=zmin, vmax=zmax, clip=zclip, linthresh=zlthresh, linscale=zlscale)
	return norm, zmin, zmax

def project_hist(_mdata, _adata, _image, _weights, _colors, edges,
			mr=None, ar=None, zlog=False,
			scale='linear', direction='x', grid=None,
			nbin=100, anbin=100, slice=False, hgap=0.04, hheight=0.15, halpha=0.1, hscale='linear',
			doimage=False, plt=None, ax=None, despine=False):

	if type(_mdata).__name__ == 'OrderedDict':
		mdata   = _mdata
		adata   = _adata
		image   = _image
		weights = _weights
		colors  = _colors
	else:
		mdata   = OrderedDict()
		adata   = OrderedDict()
		image   = OrderedDict()
		weights = OrderedDict()
		colors  = OrderedDict()

		mdata  [0] = _mdata
		adata  [0] = _adata
		image  [0] = _image
		weights[0] = _weights
		colors [0] = _colors

	mdata_   = mdata
	weights_ = weights

	mh    = OrderedDict()

	if direction == 'x':
		axis = 1
		rect = [0, 1. + hgap, 1, hheight]
		sxr0 = sxr1 = mr
		align = 'mid'
		orientation = 'vertical'
		mhax = ax.inset_axes(rect, transform=ax.transAxes, sharex=ax)
	else:
		axis = 0
		rect = [1. + hgap, 0.0, hheight, 1]
		syr0 = syr1 = mr
		align = 'mid'
		orientation = 'horizontal'
		mhax = ax.inset_axes(rect, transform=ax.transAxes, sharey=ax)

	if type(grid) is bool:
		if grid is True: mhax.grid()

	if slice is not None:
		if type(slice) is not list:
			p2v = pix2val([0, 1], vr=ar, pr=[0, nbin])
			p2v = p2v[1] - p2v[0]
			slice = [slice, slice + p2v]

		pix_slice = val2pix(slice, vr=ar, pr=[0, nbin])

		if pix_slice[0] == pix_slice[1]: pix_slice[1] = pix_slice[1] + 1

		if direction == 'x':
			syr0 = [slice[0], slice[0]]
			syr1 = [slice[1], slice[1]]
			for key in image:
				mh[key] = image[key][:, pix_slice[0]:pix_slice[1]].sum(axis=axis)
		else:
			sxr0 = [slice[0], slice[0]]
			sxr1 = [slice[1], slice[1]]
			for key in image:
				mh[key] = image[key][pix_slice[0]:pix_slice[1], :].sum(axis=axis)

		ax.plot(sxr0, syr0, linestyle='solid', clip_on=True, color='white', alpha=0.5)
		ax.plot(sxr1, syr1, linestyle='solid', clip_on=True, color='white', alpha=0.5)

		if not doimage:
			for key in adata:
				pick = (adata[key] >= slice[0]) & (adata[key] <= slice[1])
				mdata_  [key] = mdata[key][pick]
				weights_[key] = weights[key][pick]
	else:
		for key in adata:
			mh[key] = image[key].sum(axis=axis)

	for key in mdata_:
		if not doimage:
			sel  = mdata_[key]
			wsel = weights_[key]
		else:
			# note it is not tested whether this should be nbin or anbin
			if direction == 'x': sel = mdata_[key][::nbin]
			else:                sel = mdata_[key][:anbin]
			wsel = mh[key]

		mhax.hist(sel, weights=wsel, bins=edges, histtype='stepfilled', align=align,
				orientation=orientation, facecolor=colors[key], alpha=halpha)
		mhax.hist(sel, weights=wsel, bins=edges, histtype='step', align=align,
				orientation=orientation, edgecolor=colors[key])

	if hscale is None:
		if zlog: hscale = 'log'
		else:    hscale = 'linear'

	if direction == 'x':
		mhax.set_xlim(mr)
		mhax.set_xscale(scale)
		plt.setp(mhax.get_xticklabels(), visible=False)
		plt.setp(mhax.get_xlabel(),      visible=False)
		mhax.set_yscale(hscale)
	else:
		mhax.set_ylim(mr)
		mhax.set_yscale(scale)
		plt.setp(mhax.get_yticklabels(), visible=False)
		plt.setp(mhax.get_ylabel(),      visible=False)
		mhax.set_xscale(hscale)

	despine_axes(mhax, despine)

# ----------------------------------------------------------------------------------------
def set_header_for_wcs(header, x='X', y='Y'):
	done = 0
	for key in header:
		if header[key] == x:
			mat = re.search("TTYPE([0-9]+)", key)
			if bool(mat):
				header['CTYPE1'] = header['TCTYP' + mat[1]]
				header['CRPIX1'] = header['TCRPX' + mat[1]]
				header['CRVAL1'] = header['TCRVL' + mat[1]]
				header['CDELT1'] = header['TCDLT' + mat[1]]
				done = done + 1
				continue

		if header[key] == y:
			mat = re.search("TTYPE([0-9]+)", key)
			if bool(mat):
				header['CTYPE2'] = header['TCTYP' + mat[1]]
				header['CRPIX2'] = header['TCRPX' + mat[1]]
				header['CRVAL2'] = header['TCRVL' + mat[1]]
				header['CDELT2'] = header['TCDLT' + mat[1]]
				done = done + 10
				continue

		if done == 11: break

	return header

# ----------------------------------------------------------------------------------------
def prep_data_deco(func):
	"""
	decorator for data loader. Used for 1-d and 2-d data as well as 2-d images
	Some nontrivial parameters:
		attr:
				makehist: to make a histogram on the fly
				hist: data is a histogram
				poisson_error: add Poisson error
	"""

	def xdexpr(expr, x, y, vars=None):
		if vars is not None:
			for key, val in vars.items():
				locals()[key] = val
		if expr is not None: return eval(expr)
		else: return x

	def ydexpr(expr, x, y, vars=None):
		if vars is not None:
			for key, val in vars.items():
				locals()[key] = val
		if expr is not None: return eval(expr)
		else: return y

	def zdexpr(expr, x, y, vars=None):
		if vars is not None:
			for key, val in vars.items():
				locals()[key] = val
		if expr is not None: return eval(expr)
		else: return None

	def errexpr(expr, err, x, y, vars=None):
		if vars is not None:
			for key, val in vars.items():
				locals()[key] = val
		if expr is not None:
			ans = eval(expr)
			return ans.copy()
		else: return err

	def limexpr(expr, lim, x, y, vars=None):
		if vars is not None:
			for key, val in vars.items():
				locals()[key] = val
		if expr is not None:
			ans = eval(expr)
			return ans.copy()
		else: return lim

	@wraps(func)
	def prep_data(*args, xdata=None, ydata=None, weights=None,
				xexpr=None, yexpr=None, zexpr=None,
				xerr=None, yerr=None, xerrexpr=None, yerrexpr=None,
				xlerr=None, ylerr=None, xlerrexpr=None, ylerrexpr=None,
				xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None,
				xhighdata=None, xlowdata=None, xhigh=None, xlow=None,
				xlowexpr=None, xhighexpr=None,
				yhighdata=None, ylowdata=None, yhigh=None, ylow=None,
				ylowexpr=None, yhighexpr=None,
				data=None, image=None, flip=None,
				infile=None, x="", y="", z="",
				xlabel=None, ylabel=None, xr=None, yr=None,
				infile2=None, attr='', pars=None, nbin=100, binsize=None,
				xmin=None, xmax=None, ymin=None, ymax=None,
				margin=0.0, drawdown=None, filter=False,
				xscale=None, yscale=None, xlog=False, ylog=False,
				rcParams=None, clip=None,  # pixel coordinates
				comment=None,
				verbose=0, ftype=None, hdu=None, columns=None, help=None, **kwargs):

		help_text(help)

		loaded = None

		if infile is not None:
			infile = str(path.expanduser(infile))

		# try loading an image
		if type(image) is bool:
			if image:
				image = read_img(infile, hdu=hdu)

				# # read image
				# # assume fits image for now
				# hdul = fits.open(infile)
				# if hdu is None: hdu = 0
				# image = hdul[hdu].data

				loaded = 'image'
		elif image is not None: loaded = 'image'

		# make sure 2-d image and clip if requested
		if loaded == "image":
			# embed()
			ndim = image.ndim
			if ndim == 3:
				image = image.sum(axis=0)
			image = np.transpose(image)
			if flip is not None:
				image = np.flip(image, axis=flip)

			if type(clip) is list:
				# x and y seem to be swapped
				# image=image[clip[2]:clip[3],clip[0]:clip[1]]
				image = image[clip[0]:clip[1], clip[2]:clip[3]]

			nbinx, nbiny = image.shape
			if type(clip) is not list:
				if xr is None: xr = [0, nbinx]
				if yr is None: yr = [0, nbiny]
			else:
				if xr is None: xr = [clip[0], clip[1]]
				if yr is None: yr = [clip[2], clip[3]]

		xtformat = None
		ytformat = None
		# if there is no image then try loading a table
		if xdata is None and loaded is None:
			if hdu is None: hdu = 1
			if infile2 is None:
				data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data,
							xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu, attr=attr, columns=columns, comment=comment)
				if data is None:
					print('No data is read. Perhaps set ftype?')
					return False
				data2 = data
			else:
				data, x, y_, xlabel, ylabel_ = read(infile, x=x, y=None, data=data,
							xlabel=xlabel, ylabel=None, ftype=ftype, hdu=hdu, attr=attr, columns=columns, comment=comment)
				data2, x_, y, xlabel_, ylabel = read(infile2, x=None, y=y,
					xlabel=None, ylabel=ylabel, ftype=ftype, hdu=hdu, attr=attr, columns=columns, comment=comment)
			ydata = data2[y]

			if xerr  is not None: xerrdata  = data [xerr ]
			if yerr  is not None: yerrdata  = data2[yerr ]
			if xlow  is not None: xlowdata  = data [xlow ]
			if xhigh is not None: xhighdata = data [xhigh]
			if ylow  is not None: ylowdata  = data2[ylow ]
			if yhigh is not None: yhighdata = data2[yhigh]
			if xlerr is not None: xlerrdata = data [xlerr]
			if ylerr is not None: ylerrdata = data2[ylerr]

			if   x == '_auto_'     : xdata = np.arange(0, len(ydata))
			elif x == '_range_'    : xdata = (xlowdata + xhighdata) * 0.5
			elif x == '_range_log_': xdata = np.exp((np.log(xlowdata) + np.log(xhighdata)) * 0.5)
			else: xdata = data[x]

			attrs = attr.split(',')
			xtmat = [s for s in attrs if "xtime" in s]
			ytmat = [s for s in attrs if "ytime" in s]
			xtmat = '' if xtmat == [] else xtmat[0]
			ytmat = '' if ytmat == [] else ytmat[0]
			if type(xdata[0]) is str: xdata, xtformat = get_number(xdata, istime=xtmat)
			if type(ydata[0]) is str: ydata, ytformat = get_number(ydata, istime=ytmat)

			loaded = 'table'

		if xscale is None: xscale = 'log' if xlog else 'linear'
		if yscale is None: yscale = 'log' if ylog else 'linear'

		attrs = attr.split(',')
		if 'wcs' in attr:
			# try to grab wcs information from header, assume fits file
			from astropy.wcs import WCS
			header = tt.from_csv_or_fits(infile, ftype='fitshdr')
			header = set_header_for_wcs(header, x=x, y=y)
			wcs = WCS(header)
			kwargs['wcs'] = wcs

		# change xdata and ydata by expr
		if pars is not None: vars = read_pars(pars, data=data, infile=infile, comment=comment)
		else:                vars = None

		xdata_     = xdexpr (xexpr    ,            xdata, ydata, vars=vars)
		ydata_     = ydexpr (yexpr    ,            xdata, ydata, vars=vars)
		xerrdata_  = errexpr(xerrexpr , xerrdata,  xdata, ydata, vars=vars)
		yerrdata_  = errexpr(yerrexpr , yerrdata,  xdata, ydata, vars=vars)
		xlerrdata_ = errexpr(xlerrexpr, xlerrdata, xdata, ydata, vars=vars)
		ylerrdata_ = errexpr(ylerrexpr, ylerrdata, xdata, ydata, vars=vars)
		zdata_     = zdexpr (zexpr    ,            xdata, ydata, vars=vars)
		xlowdata_  = limexpr(xlowexpr , xlowdata,  xdata, ydata, vars=vars)
		xhighdata_ = limexpr(xhighexpr, xhighdata, xdata, ydata, vars=vars)
		ylowdata_  = limexpr(ylowexpr , ylowdata,  xdata, ydata, vars=vars)
		yhighdata_ = limexpr(yhighexpr, yhighdata, xdata, ydata, vars=vars)

		xdata     = xdata_
		ydata     = ydata_
		xerrdata  = xerrdata_
		yerrdata  = yerrdata_
		xlerrdata = xlerrdata_
		ylerrdata = ylerrdata_
		zdata     = zdata_
		xlowdata  = xlowdata_
		ylowdata  = ylowdata_
		xhighdata = xhighdata_
		yhighdata = yhighdata_

		xr, yr, edges =  set_range_2D(xdata, ydata, xr=xr, yr=yr,
					xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
					margin=margin, drawdown=drawdown,
					attr=attr, nbin=nbin, binsize=binsize,
					xlowdata=xlowdata, xhighdata=xhighdata, xerrdata=xerrdata,
					ylowdata=ylowdata, yhighdata=yhighdata, yerrdata=yerrdata,
					xscale=xscale, yscale=yscale)

		if filter:
			if xdata is not None:
				xdata, ydata, weights = filter_by_range(xdata, ydata, xr, yr, weights=weights)
				# need to clip the image

		set_rcParams(rcParams, verbose=verbose, name=func.__name__)

		if image     is not None: kwargs['image'      ] = image
		# if ftype     is not None: kwargs['ftype'      ] = ftype
		if xerrdata  is not None: kwargs['xerrdata'   ] = xerrdata
		if yerrdata  is not None: kwargs['yerrdata'   ] = yerrdata
		if xlerrdata is not None: kwargs['xlerrdata'  ] = xlerrdata
		if ylerrdata is not None: kwargs['ylerrdata'  ] = ylerrdata
		if xlowdata  is not None: kwargs['xlowdata'   ] = xlowdata
		if ylowdata  is not None: kwargs['ylowdata'   ] = ylowdata
		if xhighdata is not None: kwargs['xhighdata'  ] = xhighdata
		if yhighdata is not None: kwargs['yhighdata'  ] = yhighdata

		if weights   is not None: kwargs['weights'    ] = weights
		# if data      is not None: kwargs['data'       ] = data
		if xtformat  is not None: kwargs['xtformat'    ] = xtformat
		if ytformat  is not None: kwargs['ytformat'    ] = ytformat

		# this is for the modeling but plotting's collect data will complain?
		# technically this shouldn't be here. 2 decorators are cross-talking...
		if 'm' in kwargs:
			if infile    is not None: kwargs['infile'     ] = infile
			if hdu       is not None: kwargs['hdu'        ] = hdu

		if z != "":
			if zdata is not None: kwargs['zdata'] = data[z]

		# print('z',z, 'zdata' in kwargs)

		return func(*args, xdata=xdata, ydata=ydata,
			# weights=weights, drawdown=drawdown, data=data,
			# image=image,
			xlabel=xlabel, ylabel=ylabel, xr=xr, yr=yr,
			xscale=xscale, yscale=yscale,
			margin=margin, edges=edges,
			nbin=nbin, binsize=binsize,
			verbose=verbose, help=None, attr=attr, **kwargs)

	return prep_data

# two part reading
# combined model matching the regular data point to set up residual
# combined model and its components with high x-axis scaling
# the latter could be in a different HDU, while the former can be in the same HDU as the data
def prep_model_deco(func):

	def mdexpr(expr, m, x, y):
		if expr is not None: return eval(expr)
		else: return m

	def rdexpr(expr,  r, m, x, y):
		if expr is not None: return eval(expr)
		else: return r

	@wraps(func)
	def prep_data(*args, x=None, m=None, r=None,
				infile=None, ftype=None, hdu=None,
				xdata=None, ydata=None, mdata=None,
				rexpr=None, mexpr=None,
				rlabel=None, rr=None, rscale='linear',
				mlabel=None,
				xlabel=None, ylabel=None, xr=None, yr=None,
				xscale=None, yscale=None,
				margin=None, drawdown=None,
				rmin=None, rmax=None,
				rmargin=0.0, data=None,
				xerrdata=None, yerrdata=None,
				xlowdata=None, xhighdata=None,
				ylowdata=None, yhighdata=None,
				comment=None,
				verbose=0, attr='',
				mhdu=None, phdu=None,
				help=None, **kwargs):

		help_text(help)

		loaded = None

		# if there is no image then try loading a table
		if mdata is None and loaded is None:
			if hdu is None: hdu = 1
			data_, m_, r_, mlabel, rlabel = read(infile, x=m, y=r, data=data,
						xlabel=None, ylabel=rlabel, ftype=ftype, hdu=hdu, attr=attr, comment=comment)
			if data_ is None: return False

			if m is not None: mdata = data_[m]
			else:             mdata = None
			if r is not None: rdata = data_[r]
			else:             rdata = None

			loaded = 'table'

		# change xdata and ydata by expr
		mdata = mdexpr(mexpr, mdata, xdata, ydata)
		rdata = rdexpr(rexpr, rdata, mdata, xdata, ydata)

		rr =  set_range(rdata, dr=rr,
					dmin=rmin, dmax=rmax,
					margin=rmargin, drawdown=None,
					scale=rscale)

		# if mhdu is present replace mdata
		if mhdu is not None:
			toUnpack = read(infile, ftype=ftype, hdu=mhdu)
			mdata = toUnpack[0]

		# if phdu is present read parameter data
		if phdu is not None:
			toUnpack = read(infile, ftype=ftype, hdu=phdu)
			pdata = toUnpack[0]
		else:
			pdata = None

		return func(*args, xdata=xdata, ydata=ydata,
			mdata=mdata, rdata=rdata, pdata=pdata,
			xlabel=xlabel, ylabel=ylabel, xr=xr, yr=yr,
			xscale=xscale, yscale=yscale,
			margin=margin, drawdown=drawdown,
			data=data_, rlabel=rlabel, rr=rr, mlabel=mlabel,
			xerrdata=xerrdata, yerrdata=yerrdata,
			xlowdata=xlowdata, xhighdata=xhighdata,
			ylowdata=ylowdata, yhighdata=yhighdata,
			rmargin=rmargin, attr=attr,
			verbose=verbose, help=None, **kwargs)

	return prep_data
# ----------------------------------------------------------------------------------------
# 1-D plots from a single data set
@prep_data_deco
def plot1d(xdata=None, ydata=None, data=None,
		xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None, xerrdata=None, yerrdata=None,
		xr=None, yr=None, xlabel=None, ylabel=None,
		xr2=None, yr2=None, xlabel2=None, ylabel2=None,
		outfile=None, attr='', alpha=None,
		xscale='linear', yscale='linear',
		nbin=100, binsize=None, edges=None, weights=None, margin=None,  # for making a new histogram
		marker='.', markersize=None, linestyle='None', color=None, linewidth=None, errcolor=None,
		smpars=None, smooth=None, cmap=None,
		grid=None, zlog=None, zlabel='',
		text=None, text_kw=None, title=None,
		polygon=None, polygon_kw={},
		ellipse=None, ellipse_kw={},
		line=None, line_kw={}, gwhich='major',
		help=None, display=True, ion=False, hold=False, verbose=0, **kwargs):
	"""Plot 1-D from input table
	"""
	if 'zdata' in kwargs: zdata = kwargs['zdata']
	else:                 zdata = None
	if 'xtformat' in kwargs: xtformat = kwargs['xtformat']
	else:                    xtformat = None
	if 'ytformat' in kwargs: ytformat = kwargs['ytformat']
	else:                    ytformat = None

	def show(ion=True):
		check_ion(ion)

		nonlocal xdata, ydata, marker
		nonlocal binsize, nbin, edges, weights, yr, margin
		nonlocal zdata, cmap
		nonlocal xtformat, ytformat

		fig, ax = plt.subplots()

		pid, ax2, ay2 = plot1d_core(xdata, ydata, z=zdata, attr=attr, xscale=xscale, yscale=yscale,
			xlow=xlowdata, xhigh=xhighdata, ylow=ylowdata, yhigh=yhighdata, xerr=xerrdata, yerr=yerrdata,
			color=color, label=None, alpha=alpha, errcolor=errcolor,
			marker=marker, markersize=markersize, linestyle=linestyle, linewidth=linewidth,
			ax=ax, ax2=None, ay2=None,
			binsize=binsize, nbin=nbin, edges=edges,
			xr=xr, yr=yr, smpars=smpars, smooth=smooth,
			cmap=cmap, zlog=zlog, zlabel=zlabel,
			altx=False, alty=False,
			add_ax2=xr2 is not None,
			add_ay2=yr2 is not None)

		wrap(plt, xr=xr, yr=yr, xlabel=xlabel, ylabel=ylabel, fig=fig,
			xscale=xscale, yscale=yscale, outfile=outfile,
			ax=ax, grid=grid, title=title,
			text=text, text_kw=text_kw,
			polygon=polygon, polygon_kw=polygon_kw,
			ellipse=ellipse, ellipse_kw=ellipse_kw,
			line=line, line_kw=line_kw, gwhich=gwhich,
			xtformat=xtformat, ytformat=ytformat,
			display=display, ion=ion)

	show(ion=ion)
	if hold: embed()

	return plt

# 2-D plots from a single data set
@prep_data_deco
def dplot(xdata=None, ydata=None, zdata=None, image=None, data=None,
		xr=None, yr=None, zr=None,
		zmin=None, zmax=None, zoff=None, zmid=None,
		zlthresh=None, zlscale=None,
		outfile=None, attr='',
		xscale='linear', yscale='linear', xedges=None, yedges=None,
		xlabel=None, ylabel=None, title=None, loc_ylabel=None, y_title=None,
		xr2=None, yr2=None, xlabel2=None, ylabel2=None, zlabel=None,
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, cmap='Blues', aspect='auto',
		interpolation=None, weights=None,
		cbar=True, cb_orientation=None, cb_ticklocation=None, cb_outside=False,
		cb_off=None, cb_width=None, cb_length=None,
		cb_gap=0.03,
		zclip=False,
		xhist=False, xh_height=0.15, xh_scale=None,
		yhist=False, yh_height=0.15, yh_scale=None,
		xslice=None, yslice=None,  # data coordinateslike xr or yr (not necessarily pixels)
		halpha=0.3, hcolor="darkblue", hgap=0.04, hheight=0.15,
		despine=None, margin=0.0, drawdown=None,
		noplot=False, grid=None,
		text=None, text_kw=None,
		polygon=None, polygon_kw=None,
		ellipse=None, ellipse_kw=None,
		wcs=None,
		help=None, display=True, ion=False, hold=False, verbose=0, **kwargs):
	""" 2-d density plot
	"""

	if image is None:
		# data points
		binx, nbinx = get_bin(binsize, nbin, binx, nbinx, xr)
		biny, nbiny = get_bin(binsize, nbin, biny, nbiny, yr)
		doimage = False
	else:
		# image input
		if zmax is None: zmax = np.max(image)
		if zmin is None: zmin = np.min(image)

		nbinx, nbiny = image.shape
		binx = (xr[1] - xr[0]) / nbinx
		biny = (yr[1] - yr[0]) / nbiny
		doimage = True

	if xedges is None: xedges = get_edges(xr, nbinx, scale=xscale)
	if yedges is None: yedges = get_edges(yr, nbiny, scale=yscale)

	bins = [xedges, yedges]

	if not doimage:
		# to get zmax
		if zdata is None:
			heatmap, *_ = np.histogram2d(xdata, ydata, bins=bins, weights=weights)
			image = heatmap.T

			weights = np.ones(len(xdata))
		else:
			# heat map value is given for z
			# rbf = interpolate.Rbf(xdata, ydata, zdata, function='linear', mode='N-D')
			# need to make overal scale similar to get the proper interpolation
			# this part is not implemented in density.plot
			xmin, xmax = np.min(xdata), np.max(xdata)
			ymin, ymax = np.min(ydata), np.max(ydata)
			xs = xmax - xmin
			ys = ymax - ymin

			rbf = interpolate.RBFInterpolator(np.array([(xdata - xmin) / xs, (ydata - ymin) / ys]).T, zdata)
			flat = np.mgrid[0:1:nbinx * 1j, 0:1:nbiny * 1j].reshape(2, -1).T

			image = rbf(flat)
			xdata = flat[:, 0] * xs + xmin
			ydata = flat[:, 1] * ys + ymin

			weights = image.flatten()
	else:
		xdata, ydata = edges_to_data(xedges, yedges,
						xr=xr, binx=binx, nbinx=nbinx,
						yr=yr, biny=biny, nbiny=nbiny)

		weights = image.flatten()

	if noplot: return image, xdata, ydata
	if zmax is None: zmax = np.max(image)
	if zmin is None: zmin = np.min(image)

	def show(ion=True):

		check_ion(ion)

		nonlocal zmin, zmax, zoff
		nonlocal zmid
		nonlocal zlthresh, zlscale
		nonlocal zclip
		nonlocal xr, yr
		nonlocal loc_ylabel, y_title
		nonlocal wcs

		# attrs = attr.split(',')
		# if 'wcs' in attrs:
		if wcs is not None:
			fig = plt.figure()
			ax = fig.add_subplot(111, projection=wcs)
		else:
			fig, ax = plt.subplots()

		if ion: plt.ion()
		norm, zmin, zmax = get_norm(zlog=zlog, zmid=zmid, zmin=zmin, zmax=zmax,
						zr=zr, zlthresh=zlthresh, zlscale=zlscale)

		image, xedges, yedges, im = ax.hist2d(xdata, ydata, weights=weights,
											norm=norm, bins=bins,  cmap=cmap)
		ax.set_aspect(aspect)
		# if grid is not None:
		#     if grid:
		#           # why is this working with only xgrid?
		#           xgrid=ax.get_xgridlines()
		#           for each in xgrid: ax.plot(each.get_xdata(),each.get_ydata())

		if noplot: return image

		nonlocal cbar, despine, cb_outside, margin, xslice, yslice

		if xhist or yhist:
			if despine is None: despine = True
		despine_axes(ax, despine)

		if xhist:
			nonlocal xh_height, xh_scale
			project_hist(xdata, ydata, image, weights, hcolor, xedges,
						direction='x',
						mr=xr, ar=yr, zlog=zlog, grid=grid,
						scale=xscale, nbin=nbiny, anbin=nbinx, slice=yslice,
						hscale=xh_scale, hgap=hgap, hheight=hheight, halpha=halpha,
						doimage=doimage, plt=plt, ax=ax, despine=despine)

		if yhist:
			nonlocal yh_height, yh_scale
			project_hist(ydata, xdata, image, weights, hcolor, yedges,
						direction='y',
						mr=yr, ar=xr, zlog=zlog, grid=grid,
						scale=yscale, nbin=nbinx, anbin=nbiny, slice=xslice,
						hscale=yh_scale, hgap=hgap, hheight=hheight, halpha=halpha,
						doimage=doimage, plt=plt, ax=ax, despine=despine)

		rect, loc_ylabel, y_title = colorbar(im, ax, fig, zlabel,  cbar=cbar, gap=cb_gap,
						ticklocation=cb_ticklocation, orientation=cb_orientation,
						hsize=hheight + hgap, xhist=xhist, yhist=yhist,
						loc_ylabel=loc_ylabel, y_title=y_title)

		wrap(plt, xr=xr, yr=yr, xlabel=xlabel, ylabel=ylabel, fig=fig,
			title=title, label=not cb_outside,
			rect=rect, y_title=y_title,
			xscale=xscale, yscale=yscale, loc_ylabel=loc_ylabel,
			outfile=outfile,
			ax=ax, grid=grid,
			text=text, text_kw=text_kw,
			polygon=polygon, polygon_kw=polygon_kw,
			ellipse=ellipse, ellipse_kw=ellipse_kw,
			ion=ion, display=display)
		return image

	image = show(ion=ion)
	if hold: embed()

	return image, xedges, yedges

# ----------------------------------------------------------------------------------------
def hp2mollview(infile=None, hdu=1, outfile=None, xsize=800, title="",
			nest=False, min=None, max=None, cmap='turbo', gridcolor="white",
			hold=False, display=False, ion=False, **kwargs):
	map = hp.read_map(infile, hdu=hdu)
	print("title", title)
	hp.mollview(map, xsize=xsize, title=title, nest=nest, cmap=cmap,
				min=min, max=max, **kwargs)
	hp.graticule(color=gridcolor)
	wrap(plt, outfile=outfile,  title=title,
		display=display, ion=ion, tight=False)
	if hold: embed()

# ----------------------------------------------------------------------------------------
# multiple data set into a plot
# this will be replaced by class scatter, density, etc.
class plottool:

	key = 0
	maxkey = 0

	# data set: one for each
	xdata,     ydata     = OrderedDict(), OrderedDict()
	rexpr                = OrderedDict()
	xr,        yr        = OrderedDict(), OrderedDict()
	label,     marker    = OrderedDict(), OrderedDict()
	linestyle, linewidth = OrderedDict(), OrderedDict()
	alpha,     color     = OrderedDict(), OrderedDict()
	erralpha,  errcolor  = OrderedDict(), OrderedDict()
	altx,      alty      = OrderedDict(), OrderedDict()
	attr                 = OrderedDict()
	image                = OrderedDict()
	cmap                 = OrderedDict()
	smpars               = OrderedDict()
	smooth               = OrderedDict()
	xlowdata, xhighdata  = OrderedDict(), OrderedDict()
	ylowdata, yhighdata  = OrderedDict(), OrderedDict()
	xerrdata, yerrdata   = OrderedDict(), OrderedDict()
	xlerrdata, ylerrdata = OrderedDict(), OrderedDict()

	# common options
	xlabel  = ylabel  = None
	xscale  = yscale  = 'linear'
	title   = outfile = None
	display = ion     = hold     = False
	verbose = 1
	datfile = None
	xcol    = 'x'
	ycol    = 'y'
	xunit   = yunit   = ''
	xlabel2 = ylabel2 = ''
	xr2     = yr2     = None
	bbox_to_anchor    = None
	grid    = None

	binsize = None
	nbin    = 100
	edges   = None

	# for 2-D map
	doimage = False
	binx    = biny   = None
	nbinx   = nbiny  = None
	zmax    = zmin   = None
	xedges  = yedges = None
	zr      = None
	zlog    = None
	zoff    = None
	zmid    = None
	zlthresh = None
	zlscale = None
	zlclip  = None
	aspect  = 'auto'

	xhist   = yhist   = False
	despine = None

	# colormap for 2-d map
	cb_outside = False
	margin  = 0.00
	cbar    = False
	cb_orientation = None
	cb_ticklocation = None
	cb_outside = False
	cb_gap = 0.03

	cb_off = None
	cb_width = None
	cb_length = None
	zclip = False

	# projection histogram related
	xhist     = yhist     = False
	xh_height = yh_height = 0.15
	xh_scale  = yh_scale  = None
	xslice    = yslice    = None

	halpha    = 0.1
	hgap      = 0.04
	hheight   = 0.15
	hcolor    = "darkblue"
	noplot    = False

	loc_ylabel = None
	y_title   = None

	# annotation: text, ellipse, polygon
	text         = None
	text_kw      = {}
	ellipse      = None
	ellipse_kw   = {}
	polygon      = None
	polygon_kw   = {}

	invert       = False  # for mdplot_rgb

	# alternative axes
	add_ax2      = False
	add_ay2      = False
	dolegend     = True

	# 1-dplot with reference data set
	refkey      = 0  # for reference data
	refer       = False
	refset      = False

	# data save
	colnames    = ['x', 'y']
	units       = ['', '']

	# RGB
	dorgb       = False

	def __init__(self, **kwpars):
		self.set_kwpars(kwpars)
		self.xdata = OrderedDict()
		self.ydata = OrderedDict()

	def set_kwpars(self, kwargs):

		ignored = []
		for key, val in kwargs.items():
			if hasattr(self, key): setattr(self, key, val)
			else:                  ignored.append(key)
		if len(ignored) > 0:
			print(cc.err, 'Followings are not defined, so ignored, so double check:' + cc.reset)
			print(cc.err, ignored, cc.reset)

		return 1

	def wrap(self, plt, ax, **kwpars):
		wrap(plt, xlabel=self.xlabel, ylabel=self.ylabel, title=self.title,
			xscale=self.xscale, yscale=self.yscale, outfile=self.outfile,
			ax=ax, grid=self.grid,
			xlabel2=self.xlabel2, ylabel2=self.ylabel2, xr2=self.xr2, yr2=self.yr2,
			loc_ylabel=self.loc_ylabel, y_title=self.y_title,
			text=self.text, text_kw=self.text_kw,
			polygon=self.polygon, polygon_kw=self.polygon_kw,
			ellipse=self.ellipse, ellipse_kw=self.ellipse_kw,
			ion=self.ion, display=self.display, **kwpars)

	def set_default_range(self):

		pcolor = ["black", "red", "green", "blue", "purple", "magenta", "brown", "orange", "cyan"]
		icolor = 0
		lcolor = len(pcolor)

		pcmap = ["Blues", "Reds", "Greens", "Greys", "Purples", "Oranges"]
		icmap = 0
		lcmap = len(pcmap)

		for key in self.xdata:
			if 'xrf' not in locals(): xrf = self.xr[key]
			if 'yrf' not in locals(): yrf = self.yr[key]

			if xrf[0] > self.xr[key][0]: xrf[0] = self.xr[key][0]
			if xrf[1] < self.xr[key][1]: xrf[1] = self.xr[key][1]
			if yrf[0] > self.yr[key][0]: yrf[0] = self.yr[key][0]
			if yrf[1] < self.yr[key][1]: yrf[1] = self.yr[key][1]

			if self.color[key] is None:
				self.color[key] = pcolor[icolor]
				icolor = (icolor + 1) % lcolor

			if self.alpha[key] is None:
				self.alpha[key] = 1.0  # /self.key

			if self.cmap[key] is None:
				self.cmap[key] = pcmap[icmap]
				icmap = (icmap + 1) % lcmap

		if self.verbose > 1: print("range:", xrf, yrf)
		return xrf, yrf

	@prep_data_deco
	def collect_data(self, xdata=None, ydata=None, key=None,
				xlowdata=None, xhighdata=None, ylowdata=None, yhighdata=None,
				xerrdata=None, yerrdata=None, xlerrdata=None, ylerrdata=None,
				image=None, cmap=None,
				xr=None, yr=None, label=None,
				marker='.', linestyle='None', linewidth=1.5,
				color=None, alpha=None, errcolor=None, erralpha=None,
				altx=False, alty=False, rexpr=None, attr='',
				smpars=None, smooth=None,
#                 rcParams=None,
				help=None, hold=False, verbose: int = 0, **kwargs):
		"""
		collect multiple data set for plot
			-parameters are divided into two groups: one for each data
					set, and the other for common use
			-relies on the decorator for data load: see
					'(cjpy.)plottool.prep_data_deco'

			Some nontrivial parameters:
					altx, alty: 2ndary axes data
					rexpr: not used?
					attr:
						makehist: to make a histogram on the fly
						hist: data is a histogram
						poisson_error: add Poisson error
		"""

		if key is None: key = self.key

		self.xdata        [key] = xdata
		self.ydata        [key] = ydata
		self.xr           [key] = xr
		self.yr           [key] = yr
		self.marker       [key] = marker
		self.linestyle    [key] = linestyle
		self.linewidth    [key] = linewidth
		self.color        [key] = color
		self.alpha        [key] = alpha
		self.altx         [key] = altx
		self.alty         [key] = alty
		self.rexpr        [key] = rexpr
		self.attr         [key] = attr
		self.image        [key] = image
		self.cmap         [key] = cmap
		self.smpars       [key] = smpars
		self.smooth       [key] = smooth
		self.xlowdata     [key] = xlowdata
		self.ylowdata     [key] = ylowdata
		self.xhighdata    [key] = xhighdata
		self.yhighdata    [key] = yhighdata
		self.xerrdata     [key] = xerrdata
		self.yerrdata     [key] = yerrdata
		self.xlerrdata    [key] = xlerrdata
		self.ylerrdata    [key] = ylerrdata

		if errcolor is None: errcolor = color
		if erralpha is None: erralpha = alpha
		self.errcolor     [key] = errcolor
		self.erralpha     [key] = erralpha

		if label is None: self.label[key] = str(key)
		else:             self.label[key] = label

		# in order to set options any time
		# in this way one time options can be set in the -main options
		# but it becomes redundantly repeated when collect_data is
		# repeatedly called as -main
		# should go either class initialization or
		# the -post routine, but that would make the -option setting a bit deeper
		self.set_kwpars(kwargs)
		if len(self.xdata.keys()) == 1:
			self.verbose = kwargs.get('verbose', verbose)
#                 set_rcParams(rcParams, verbose=verbose)
		# print(self.verbose)

		if self.refer:
			self.refkey = key
			self.refer = False

		# self.key = key + 1
		self.maxkey = self.maxkey + 1
		self.key = self.maxkey

		if self.verbose > 2:
			print(xdata)
			print(ydata)
		return 1

	def composite_data(self, key=None, inkeys=None,
				xexpr=None, yexpr=None,
				varx=None, vary=None, defkey=None, **kwpars):
		if type(inkeys).__name__ is None: return
		if key is None:
			self.maxkey = self.maxkey + 1
			key = self.maxkey

		nkeys_ = len(inkeys)

		if varx is None:
			varx = []
			for idx_, each_ in enumerate(inkeys):
				varx.append('x' + str(idx_))

		if vary is None:
			vary = []
			for idx_, each_ in enumerate(inkeys):
				vary.append('y' + str(idx_))

		for idx_, each_ in enumerate(inkeys):
			if each_ not in self.xdata:
				print(cc.err + 'No data found for', each_, cc.reset)
				return

			locals()[varx[idx_]] = self.xdata[each_]
			locals()[vary[idx_]] = self.ydata[each_]

		xdata = eval(xexpr)
		ydata = eval(yexpr)

		self.collect_data(xdata=xdata, ydata=ydata, key=key)
		self.set_prop(key, **kwpars)

	def set_prop(self, key, **kwpars):
		for k, v in kwpars.items():
			x = getattr(self, k)
			x[key] = v
			setattr(self, k, x)

	def scan_fitsfile_moot(self, infile=None, hdu="", x=None):
		if infile is None:
			return None
		hdul = fits.open(infile)
		tasks = OrderedDict()
		loops = []
		for each in hdul:
			if hdu != "":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new = False
				if bool(re.search('A', str(subeach.format))):
					continue
				if x is not None:
					if x != subeach.name:
						if hdu != "":
							loopid = subeach.name
						else:
							loopid = each.name + ' ' + subeach.name
						new = True
				else:
					x = subeach.name
				if new:
					loops.append(loopid)
					task = OrderedDict()
					task['infile']    = infile
					task['hdu']       = each.name
					task['x']         = x
					task['y']         = subeach.name
					task['label']     = loopid

					tasks['-loop==' + loopid] = task

		tasks['-loop'] = loops
		return tasks

	def scan_fits_cols(self, infile=None, hdu="", x=None):
		if infile is None:
			return None
		hdul = fits.open(infile)
		tasks = OrderedDict()
		for each in hdul:
			if hdu != "":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new = False
				if bool(re.search('A', str(subeach.format))):
					continue
				if x is not None:
					if x != subeach.name:
						if hdu != "":
							loopid = subeach.name
						else:
							loopid = each.name + ' ' + subeach.name
						new = True
				else:
					x = subeach.name
				if new:
					task = OrderedDict()
					task['infile']    = infile
					task['hdu']       = each.name
					task['x']         = x
					task['y']         = subeach.name
					task['label']     = loopid

					tasks[loopid] = task
		return tasks

	def scan_fits_hdus(self, infile=None, x=None, y=None, hdu="", verbose=0, tolist=False, seed=None):
		if infile is None:
			return None

		infile = str(Path(infile).expanduser())
		hdul = fits.open(infile)
		tasks = OrderedDict()
		for each in hdul:

			if not hasattr(each, 'columns'): continue

			if hdu != "":
				if not bool(re.search(hdu, each.name)): continue
			if int(verbose) > 0: print(each.name)

			ind = []
			for idx, subeach in enumerate(each.columns):
				if bool(re.search('A', str(subeach.format))): continue
				ind.append(idx)
			if x is None or x == "": x = each.columns[ind[0]].name
			if y is None or y == "": y = each.columns[ind[1]].name

			x_bingo = False
			y_bingo = False
			for subeach in each.columns:
				if x == subeach.name: x_bingo = True
				if y == subeach.name: y_bingo = True

			if not x_bingo * y_bingo: continue

			task = OrderedDict()
			task['infile']    = infile
			task['hdu']       = each.name
			task['x']         = x
			task['y']         = y
			task['label']     = each.name

			if seed is not None:
				for key in seed:
					if key not in task: task[key] = seed[key]

			tasks[each.name] = task

		if tolist:
			idx = 1
			for key, val in tasks.items():
				val['-id'] = f"{idx:02}:" + key
				idx = idx + 1

			tasks = list(tasks.values())

		return tasks

	def mplot1d(self, xr=None, yr=None, keys=None, rcParams=None, lncols=1, **kwpars):
		"""Multiple Plot 1-D from input table
		"""

		if len(self.rexpr) == list(self.rexpr.values()).count(None):
			xrf, yrf = self.set_default_range()
			xref = yref = None
		else:
			if not self.refset:
				xref = self.xdata.pop(self.refkey)
				yref = self.ydata.pop(self.refkey)
				self.xref = xref
				self.yref = yref
				self.refset = True
			else:
				xref = self.xref
				yref = self.yref

			xrf  = self.xr[self.refkey]
			yrf  = self.yr[self.refkey]
			_, _ = self.set_default_range()

		self.set_kwpars(kwpars)
		if xr is not None: xrf = xr
		if yr is not None: yrf = yr

		def show(ion=True):
			if self.ion: plt.ion()

			plt.close('all')
			fig, ax = plt.subplots()
			ax2     = None
			ay2     = None

			nonlocal xrf, yrf
			nonlocal xref, yref
			nonlocal keys

			if self.datfile is not None: pdt = OrderedDict()

			pids = []
			overwrite = True
			if keys is None: keys = self.xdata.keys()
			for key in keys:

				if key not in self.xdata:
					print(cc.err + 'No data found for', key, cc.reset)
					continue

				x = self.xdata[key]
				y = self.ydata[key]

				if self.rexpr[key] is not None: x, y = eval(self.rexpr[key])

				pid, ax2, ay2 = plot1d_core(x, y, attr=self.attr[key],
					xlow=self.xlowdata[key], xhigh=self.xhighdata[key],
					ylow=self.ylowdata[key], yhigh=self.yhighdata[key],
					xerr=self.xerrdata[key], yerr=self.yerrdata[key],
					xlerr=self.xlerrdata[key], ylerr=self.ylerrdata[key],
					xscale=self.xscale,  marker=self.marker[key],
					label=self.label[key],
					color=self.color[key], alpha=self.alpha[key],
					errcolor=self.errcolor[key], erralpha=self.erralpha[key],
					linestyle=self.linestyle[key], linewidth=self.linewidth[key],
					ax=ax, ax2=ax2, ay2=ay2, binsize=self.binsize, nbin=self.nbin,
					xr=xrf, yr=yrf,
					smooth=self.smooth[key], smpars=self.smpars[key],
					altx=self.altx[key], alty=self.alty[key],
					add_ax2=self.add_ax2, add_ay2=self.add_ay2,
					datfile=self.datfile, overwrite=overwrite,
					colnames=self.colnames, units=self.units, extname=self.label[key])

				overwrite = False

				if self.label[key] != "": pids.append(pid)

			if self.noplot: return ax, ax2, ay2
			if self.dolegend:
				plt.legend(labelcolor='linecolor',
						bbox_to_anchor=self.bbox_to_anchor,
						ncol=lncols, handles=pids)

			if self.verbose > 1: print('outfile', self.outfile)

			self.wrap(plt, ax, xr=xrf, yr=yrf, ax2=ax2, ay2=ay2, rcParams=rcParams)
			return ax, ax2, ay2

		ax, ax2, ay2 = show(ion=False)
		if self.hold: embed()

		return ax, ax2, ay2

	def mdplot(self, xr=None, yr=None, **kwpars):
		"""
		2-d density plot for multiple data set
			- use this with plottool.plottool.collect_data for data load
			- best used with white color for low values (or low density)
				the color map is auto alpha corrected for low values
					- alpha: sets the minimum transparency for each image
					- halpha: sets transparency for x and y histograms
			- in principle, there is no limit for the number of data sets:
				an alternative approach is using true 3 color composition, which
				is limited to 3 separate data sets

		"""

		xrf, yrf = self.set_default_range()

		self.set_kwpars(kwpars)
		if xr is not None: xrf = xr
		if yr is not None: yrf = yr

		if self.doimage is False:
			# data points
			self.binx, self.nbinx = get_bin(self.binsize, self.nbin, self.binx, self.nbinx, xrf)
			self.biny, self.nbiny = get_bin(self.binsize, self.nbin, self.biny, self.nbiny, yrf)
		else:
			# image input
			# assume xr, and yr is given, and probably no log scale for x and y axes?
			zmax = None
			zmin = None

			for key in self.image:
				zmax_ = np.max(self.image[key])
				if zmax is None: zmax = zmax_
				elif zmax < zmax_: zmax = zmax_

				zmin_ = np.min(self.image[key])
				if zmin is None: zmin = zmin_
				elif zmin > zmin_: zmin = zmin_

				# assume everything is identical for now
				nbinx, nbiny = self.image[key].shape
				binx = (xrf[1] - xrf[0]) / nbinx
				biny = (yrf[1] - yrf[0]) / nbiny

			if self.zmax is None: self.zmax = zmax
			if self.zmin is None: self.zmin = zmin

		if self.xedges is None: self.xedges = get_edges(xrf, self.nbinx, scale=self.xscale)
		if self.yedges is None: self.yedges = get_edges(yrf, self.nbiny, scale=self.yscale)

		bins = [self.xedges, self.yedges]

		zmax = None
		zmin = None
		if not self.doimage:
			# to get zmax
			self.weights = OrderedDict()
			image = OrderedDict()

			for key in self.xdata:
				heatmap, *_ = np.histogram2d(self.xdata[key], self.ydata[key], bins=bins)  # , weights=weights)
				image[key] = heatmap.T

				zmax_ = np.max(image[key])
				if zmax is None: zmax = zmax_
				elif zmax < zmax_: zmax = zmax_

				zmin_ = np.min(image[key])
				if zmin is None: zmin = zmin_
				elif zmin > zmin_: zmin = zmin_

				self.weights[key] = np.ones(len(self.xdata[key]))

		else:
			xdata, ydata = edges_to_data(self.xedges, self.yedges,
							xr=self.xr, binx=self.binx, nbinx=self.nbinx,
							yr=self.yr, biny=self.biny, nbiny=self.nbiny)

			image = copy(self.image)
			self.weights = OrderedDict()
			for key in self.image:
				self.weights[key] = image[key].flatten()
				zmax_ = np.max(self.weights[key])
				if zmax is None: zmax = zmax_
				elif zmax < zmax_: zmax = zmax_

				zmin_ = np.min(self.weights[key])
				if zmin is None: zmin = zmin_
				elif zmin > zmin_: zmin = zmin_

				if self.alpha[key] is None:
					self.alpha[key] = 1.0  # /self.key

		if self.dorgb:
			self.image = np.zeros((self.nbinx, self.nbiny, 3))
			if not self.invert:
				for key in self.xdata:
					if self.color[key] == "red":
						self.image[:, :, 0] = image[key]
					elif self.color[key] == "green":
						self.image[:, :, 1] = image[key]
					elif self.color[key] == "blue":
						self.image[:, :, 2] = image[key]
			else:
				for key in self.xdata:
					if self.color[key] == "red":
						self.image[:, :, 1] = image[key] / 2. + self.image[:, :, 1]
						self.image[:, :, 2] = image[key] / 2. + self.image[:, :, 2]
					elif self.color[key] == "green":
						self.image[:, :, 0] = image[key] / 2. + self.image[:, :, 0]
						self.image[:, :, 2] = image[key] / 2. + self.image[:, :, 2]
					elif self.color[key] == "blue":
						self.image[:, :, 0] = image[key] / 2. + self.image[:, :, 0]
						self.image[:, :, 1] = image[key] / 2. + self.image[:, :, 1]

		if self.noplot: return self.image, self.xedges, self.yedges
		if self.zmax is None: self.zmax = zmax
		if self.zmin is None: self.zmin = zmin

		def show(ion=True):

			plt.close('all')
			fig, ax = plt.subplots()

			if ion: plt.ion()
			norm, self.zmin, self.zmax = get_norm(zlog=self.zlog, zmid=self.zmid,
												zmin=self.zmin, zmax=self.zmax, zr=self.zr,
												zlthresh=self.zlthresh, zlscale=self.zlscale)

			im = OrderedDict()
			if not self.dorgb:
				for key in self.xdata:
					# cmap_N=20
					cmap             = plt.get_cmap(self.cmap[key])  # ,cmap_N)
					cmap_alpha       = cmap(np.arange(cmap.N))
					cmap_alpha[:, 3] = np.linspace(0, self.alpha[key], cmap. N)
					cmap             = ListedColormap(cmap_alpha)
					cmap.set_under((1, 1, 1, 0))

					image[key], xedges, yedges, im[key] = ax.hist2d(self.xdata[key], self.ydata[key],
									bins=bins, norm=norm, cmap=cmap, weights=self.weights[key])
			else:

				if not self.zlog:
					self.image = norm(self.image)
					# this will lose correct normalization factor
					if self.invert:
						diff = np.max(self.image) - np.min(self.image)
						self.image = 1. - self.image / diff
				else:
					self.image = norm(self.image.flatten()).reshape(self.nbinx, self.nbiny, 3)
					if self.invert: self.image = 1. - self.image

				for key in self.color:
					if not self.invert:
						if self.color[key] == 'red':
							colors_ = [(c, 0, 0, 1) for c in np.linspace(0, 1, 256)]
						elif self.color[key] == 'green':
							colors_ = [(0, c, 0, 1) for c in np.linspace(0, 1, 256)]
						elif self.color[key] == 'blue':
							colors_ = [(0, 0, c, 1) for c in np.linspace(0, 1, 256)]
						else:
							continue
					else:
						if self.color[key] == 'red':
							colors_ = [(1, 1 - c, 1 - c, 1) for c in np.linspace(0, 0.5, 256)]
						elif self.color[key] == 'green':
							colors_ = [(1 - c, 1, 1 - c, 1) for c in np.linspace(0, 0.5, 256)]
						elif self.color[key] == 'blue':
							colors_ = [(1 - c, 1 - c, 1, 1) for c in np.linspace(0, 0.5, 256)]
						else:
							continue

					cmap = colors.LinearSegmentedColormap.from_list('mycmap', colors_, N=256)
					im[key] = cm.ScalarMappable(norm=norm, cmap=cmap)

				xedges = self.xedges
				yedges = self.yedges

				ax.imshow(self.image, extent=[xrf[0], xrf[1], yrf[0], yrf[1]])

			ax.set_aspect(self.aspect)

			if self.noplot: return self.image

			if self.xhist or self.yhist:
				if self.despine is None: self.despine = True
			despine_axes(ax, self.despine)

			if self.xhist:
				project_hist(self.xdata, self.ydata, image, self.weights, self.color, xedges,
							direction='x',
							mr=xrf, ar=yrf, zlog=self.zlog, grid=self.grid,
							scale=self.xscale, nbin=self.nbiny, anbin=self.nbinx,
							slice=self.yslice, hscale=self.xh_scale,
							hgap=self.hgap, hheight=self.hheight, halpha=self.halpha,
							doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)

			if self.yhist:
				project_hist(self.ydata, self.xdata, image, self.weights, self.color, yedges,
							direction='y',
							mr=yrf, ar=xrf, zlog=self.zlog, grid=self.grid,
							scale=self.yscale, nbin=self.nbinx, anbin=self.nbiny,
							slice=self.xslice, hscale=self.yh_scale,
							hgap=self.hgap, hheight=self.hheight, halpha=self.halpha,
							doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)

			rect, self.loc_ylabel, self.y_title = colorbar(im, ax, fig, self.label,
						cbar=self.cbar, gap=self.cb_gap,
						ticklocation=self.cb_ticklocation, orientation=self.cb_orientation,
						hsize=self.hheight + self.hgap, xhist=self.xhist, yhist=self.yhist,
						loc_ylabel=self.loc_ylabel, y_title=self.y_title)

			self.wrap(plt, ax, xr=xrf, yr=yrf, label=not self.cb_outside, rect=rect)

			return self.image

		image = show(ion=False)
		if self.hold: embed()

		return image, self.xedges, self.yedges

# ----------------------------------------------------------------------------------------
class dbase:
	xdata,     ydata     = None, None
	xr,        yr        = None, None
	altx,      alty      = False, False
	alpha,     color     = None, None
	attr                 = ''
	label                = None

class dscatter(dbase):
	rexpr                = None
	marker, markersize   = ".", None
	linestyle, linewidth = 'None', 1.5
	zorder               = None
	erralpha,  errcolor  = None, None
	errzorder            = None
	smpars               = None
	smooth               = None
	smcolor, smlinewidth = None, None
	smzorder             = None
	xlowdata, xhighdata  = None, None
	ylowdata, yhighdata  = None, None
	xerrdata, yerrdata   = None, None
	xlerrdata, ylerrdata = None, None
	cmap                 = None
	zdata                = None
	zlog                 = None
	zlabel               = ''
	fillstyle            = None
	facecolors           = None

# class dhist(dbase):
#     rexpr                = None
#     linestyle, linewidth = None, None
#     erralpha,  errcolor  = None, None
#     xlowdata, xhighdata  = None, None
#     ylowdata, yhighdata  = None, None
#     xerrdata, yerrdata   = None, None
#     xlerrdata, ylerrdata = None, None

class ddensity(dbase):
	image   = None
	cmap    = None

class dspectral(dbase):
	mdata   , rdata   = None, None
	pdata   , data    = None, None
	mcxdata , mcydata = None, None
	mx      , my      = None, None
	mc = None
	rr = None

	marker,       linestyle,    color,    alpha = 'None', 'None' , 'black', 1.0  # for data error or range
	errmarker, errlinestyle, errcolor, erralpha = 'None', 'solid', 'black', 1.0  # for data error or range
	modmarker, modlinestyle, modcolor, modalpha = 'None', 'solid', 'red'  , 1.0  # for model
	resmarker, reslinestyle, rescolor, resalpha = 'None', 'None' , 'black', 1.0  # for residual
	rdemarker, rdelinestyle, rdecolor, rdealpha = 'None', 'solid', 'black', 1.0  # for residual error or range

# ----------------------------------------------------------------------------------------
class base:

	# these really should be in __init__?
	key = 0

	xlabel  = ylabel  = None
	xscale  = yscale  = 'linear'
	title   = outfile = None
	display = ion     = hold     = False
	verbose = 1

	datfile = None
	xcol    = 'x'
	ycol    = 'y'
	xunit   = yunit   = ''
	xlabel2 = ylabel2 = ''
	xr2     = yr2     = None
	bbox_to_anchor    = None
	grid    = None
	margin  = 0.00

	# annotation: text, ellipse, polygon
	text         = None
	text_kw      = {}
	ellipse      = None
	ellipse_kw   = {}
	polygon      = None
	polygon_kw   = {}

	# alternative axes
	add_ax2      = False
	add_ay2      = False
	dolegend     = True

	# data save
	colnames    = ['x', 'y']
	units       = ['', '']

	noplot     = False
	loc_ylabel = None
	y_title    = None

	binsize = None
	nbin    = 100
	edges   = None

	rcParams = None
	gwhich = 'major'

	xtformat = None
	ytformat = None

	def __init__(self, **kwpars):
		self.data = OrderedDict()
		self.set_kwpars(kwpars)

	def set_kwpars(self, kwargs):

		ignored = []
		for key, val in kwargs.items():
			if hasattr(self, key): setattr(self, key, val)
			else:                  ignored.append(key)
		if len(ignored) > 0:
			print(cc.err, 'Followings are not defined, so ignored, so double check:' + cc.reset)
			print(cc.err, ignored, cc.reset)

		if self.rcParams is not None:
			set_rcParams(self.rcParams, force=True, name=None)

		return 1

	def set_prop(self, key, **kwpars):
		for k, v in kwpars.items():
			# x = getattr(self.data, k)
			# x[key] = v
			setattr(self.data[key], k, v)

	def wrap(self, plt, ax, **kwpars):
		wrap(plt, xlabel=self.xlabel, ylabel=self.ylabel, title=self.title,
			xscale=self.xscale, yscale=self.yscale, outfile=self.outfile,
			ax=ax, grid=self.grid,
			xlabel2=self.xlabel2, ylabel2=self.ylabel2, xr2=self.xr2, yr2=self.yr2,
			loc_ylabel=self.loc_ylabel, y_title=self.y_title,
			text=self.text, text_kw=self.text_kw,
			polygon=self.polygon, polygon_kw=self.polygon_kw,
			ellipse=self.ellipse, ellipse_kw=self.ellipse_kw,
			ion=self.ion, display=self.display,
			gwhich=self.gwhich, 
			xtformat=self.xtformat, ytformat=self.ytformat, 
			**kwpars)

	def set_default_range(self):

		for key, data in self.data.items():

			if 'xrf' not in locals(): xrf = data.xr
			if 'yrf' not in locals(): yrf = data.yr

			if xrf[0] > data.xr[0]: xrf[0] = data.xr[0]
			if xrf[1] < data.xr[1]: xrf[1] = data.xr[1]
			if yrf[0] > data.yr[0]: yrf[0] = data.yr[0]
			if yrf[1] < data.yr[1]: yrf[1] = data.yr[1]

		if self.verbose > 1: print("range:", xrf, yrf)
		return xrf, yrf

	def collect_data(self, key=None,
				help=None, hold=False, verbose: int = 0, **kwargs):

		if 'label'    not in kwargs: kwargs['label'   ] = str(key)

		# set the parameters unique to each data set
		for each in [v for v in dir(self.data[key]) if v[0] != '_']:
			if each in kwargs: val = kwargs.pop(each)
			else:              val = None
			setattr(self.data[key], each, val)

		# set the parameters common to all the data set
		self.set_kwpars(kwargs)

		self.key = self.key + 1

		return 1

	def composite_data(self, key=None, inkeys=None,
					xexpr=None, yexpr=None,
					varx=None, vary=None, defkey=None, **kwpars):
		if inkeys is None: return
		if key is None:
			self.key = self.key + 1
			key = self.key

		nkeys_ = len(inkeys)

		if varx is None:
			varx = []
			for idx_, each_ in enumerate(inkeys):
				varx.append('x' + str(idx_))

		if vary is None:
			vary = []
			for idx_, each_ in enumerate(inkeys):
				vary.append('y' + str(idx_))

		for idx_, each_ in enumerate(inkeys):
			if each_ not in self.data:
				print(cc.err + 'No data found for', each_, cc.reset)
				return

			locals()[varx[idx_]] = self.data[each_].xdata
			locals()[vary[idx_]] = self.data[each_].ydata

		xdata = eval(xexpr)
		ydata = eval(yexpr)

		self.collect_data(key=key, xdata=xdata, ydata=ydata)
		self.set_prop(key, **kwpars)

	def rebin_data(self, keys=None, inkeys=None,
			method='fixed', bin=2):
		if inkeys is None: return
		if keys is None: keys=inkeys # replace

		import rebin
		for key, inkey in zip(keys, inkeys):
			self.data[key].xdata = rebin.one(np.array(self.data[inkey].xdata), bin=bin, mean=True)
			self.data[key].ydata = rebin.one(np.array(self.data[inkey].ydata), bin=bin)

class scatter(base):

	# 1-dplot with reference data set
	refkey      = None  # for reference data
	refer       = False
	refset      = False

	def set_default_color(self):

		pcolor = ["black", "red", "green", "blue", "purple", "magenta", "brown", "orange", "cyan"]
		icolor = 0
		lcolor = len(pcolor)

		for key, data in self.data.items():
			if data.color is None:
				data.color = pcolor[icolor]
				icolor = (icolor + 1) % lcolor

			if data.alpha is None:
				data.alpha = 1.0  # /self.key

	@prep_data_deco
	def collect_data(self, key=None, help=None, hold=False, verbose: int = 0, **kwargs):
		"""
		collect data set for scatter
			-parameters are divided into two groups: one for each data
					set, and the other for common use
			-relies on the decorator for data load: see
					'(cjpy.)plottool.prep_data_deco'

			Some nontrivial parameters:
					altx, alty: 2ndary axes data
					rexpr: not used?
					attr:
						makehist: to make a histogram on the fly
						hist: data is a histogram
						poisson_error: add Poisson error
		"""

		if key is None: key = self.key
		if key not in self.data: self.data[key] = dscatter()

		if 'errcolor' not in kwargs: kwargs['errcolor'] = kwargs.get('color', None)
		if 'erralpha' not in kwargs: kwargs['erralpha'] = kwargs.get('alpha', None)

		base.collect_data(self, key, help=help, hold=hold, verbose=verbose, **kwargs)

		if self.refer:
			self.refkey = key
			self.refer  = False

		return 1

	def scan_fitsfile_moot(self, infile=None, hdu="", x=None):
		if infile is None:
			return None
		hdul  = fits.open(infile)
		tasks = OrderedDict()
		loops = []
		for each in hdul:
			if hdu != "":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new = False
				if bool(re.search('A', str(subeach.format))):
					continue
				if x is not None:
					if x != subeach.name:
						if hdu != "":
							loopid = subeach.name
						else:
							loopid = each.name + ' ' + subeach.name
						new = True
				else:
					x = subeach.name
				if new:
					loops.append(loopid)
					task = OrderedDict()
					task['infile']    = infile
					task['hdu']       = each.name
					task['x']         = x
					task['y']         = subeach.name
					task['label']     = loopid

					tasks['-loop==' + loopid] = task

		tasks['-loop'] = loops
		return tasks

	def scan_fits_cols(self, infile=None, hdu="", x=None,
				tolist=False, colors=None, seed=None):

		if infile is None:
			return None

		infile = str(Path(infile).expanduser())
		hdul   = fits.open(infile)
		tasks = OrderedDict()

		# ndata = 0
		for each in hdul:
			if hdu != "":
				if hdu != each.name: continue
			if not hasattr(each, 'columns'): continue
			for subeach in each.columns:
				new = False
				if bool(re.search('A', str(subeach.format))):
					continue
				if x is not None:
					if x != subeach.name:
						if hdu != "":
							loopid = subeach.name
						else:
							loopid = each.name + ' ' + subeach.name
						new = True
				else:
					x = subeach.name
				if new:
					task = OrderedDict()
					task['infile']    = infile
					task['hdu']       = each.name
					task['x']         = x
					task['y']         = subeach.name
					task['label']     = loopid

					# if colors is not None:
					# 	task['color'] = colors[ndata]
					# ndata = ndata + 1

					tasks[loopid] = task
					if seed is not None:
						for key in seed:
							if key not in task: task[key] = seed[key]
		if tolist:
			idx = 1
			for key, val in tasks.items():
				val['-id'] = f"{idx:02}:" + key
				idx = idx + 1

			tasks = list(tasks.values())
		return tasks

	def scan_fits_hdus(self, infile=None, x=None, y=None, hdu="", verbose=0,
				tolist=False, seed=None):
		if infile is None:
			return None

		infile = str(Path(infile).expanduser())
		hdul   = fits.open(infile)
		tasks  = OrderedDict()
		for each in hdul:

			if not hasattr(each, 'columns'): continue

			if hdu != "":
				if not bool(re.search(hdu, each.name)): continue
			if int(verbose) > 0: print(each.name)

			ind = []
			for idx, subeach in enumerate(each.columns):
				if bool(re.search('A', str(subeach.format))): continue
				ind.append(idx)
			if x is None or x == "": x = each.columns[ind[0]].name
			if y is None or y == "": y = each.columns[ind[1]].name

			x_bingo = False
			y_bingo = False
			for subeach in each.columns:
				if x == subeach.name: x_bingo = True
				if y == subeach.name: y_bingo = True

			if not x_bingo * y_bingo: continue

			task = OrderedDict()
			task['infile']    = infile
			task['hdu']       = each.name
			task['x']         = x
			task['y']         = y
			task['label']     = each.name

			if seed is not None:
				for key in seed:
					if key not in task: task[key] = seed[key]

			tasks[each.name] = task

		if tolist:
			idx = 1
			for key, val in tasks.items():
				val['-id'] = f"{idx:02}:" + key
				idx = idx + 1

			tasks = list(tasks.values())

		return tasks

	def mplot1d(self, xr=None, yr=None, keys=None, lncols=1, **kwpars):
		"""Multiple Plot 1-D from input table
		"""

		if self.refkey is None:
			try:
				xrf, yrf    = self.set_default_range()
			except Exception:
				print("cannot set x, y range: perhaps no data?")
				exit()

			xref = yref = None
		else:
			if not self.refset:
				self.ref = self.data.pop(self.refkey)
				self.refset = True

			xref = self.ref.xdata
			yref = self.ref.ydata
			xrf  = self.ref.xr
			yrf  = self.ref.yr
			_, _ = self.set_default_range()

		self.set_default_color()
		self.set_kwpars(kwpars)

		if xr is not None: xrf = xr
		if yr is not None: yrf = yr

		def show():
			check_ion(self.ion)

			fig, ax = plt.subplots()
			ax2     = None
			ay2     = None

			nonlocal xrf, yrf
			nonlocal xref, yref
			nonlocal keys

			if self.datfile is not None: pdt = OrderedDict()

			pids = []
			overwrite = True
			if keys is None: keys = self.data.keys()
			for key in keys:

				if key not in self.data:
					print(cc.err + 'No data found for', key, cc.reset)
					continue

				data = self.data[key]

				x = data.xdata
				y = data.ydata

				if data.rexpr is not None:
					x, y = eval(data.rexpr)
					# embed()

				pid, ax2, ay2 = plot1d_core(x, y, attr=data.attr,
					xlow=data.xlowdata, xhigh=data.xhighdata,
					ylow=data.ylowdata, yhigh=data.yhighdata,
					xerr=data.xerrdata, yerr=data.yerrdata,
					xlerr=data.xlerrdata, ylerr=data.ylerrdata,
					marker=data.marker, markersize=data.markersize,
					label=data.label, color=data.color, alpha=data.alpha,
					smooth=data.smooth, smpars=data.smpars,
					smcolor=data.smcolor, smlinewidth=data.smlinewidth,
					zorder=data.zorder, smzorder=data.smzorder, errzorder=data.errzorder,
					altx=data.altx, alty=data.alty,
					errcolor=data.errcolor, erralpha=data.erralpha,
					linestyle=data.linestyle, linewidth=data.linewidth,
					ax=ax, ax2=ax2, ay2=ay2, xr=xrf, yr=yrf, overwrite=overwrite,
					z=data.zdata, cmap=data.cmap, zlog=data.zlog, zlabel=data.zlabel,
					xscale=self.xscale,  yscale=self.yscale,
					binsize=self.binsize, nbin=self.nbin,
					add_ax2=self.add_ax2, add_ay2=self.add_ay2,
					datfile=self.datfile,
					colnames=self.colnames, units=self.units,
					extname=data.label)

				overwrite = False

				if data.label != "":
					if pid is not None: pids.append(pid)

			if self.noplot: 
				if self.verbose > 1: print('no plot requested')
				return ax, ax2, ay2
			if self.dolegend:
				if len(pids) > 0:
					ax.legend(labelcolor='linecolor',
						bbox_to_anchor=self.bbox_to_anchor,
						ncol=lncols, handles=pids)

			if self.verbose > 1: print('outfile', self.outfile)

			self.wrap(plt, ax, fig=fig, xr=xrf, yr=yrf, ax2=ax2, ay2=ay2)
			return ax, ax2, ay2

		ax, ax2, ay2 = show()
		if self.hold: embed()

		return ax, ax2, ay2

class density(base):

	doimage = False
	binx    = biny   = None
	nbinx   = nbiny  = None
	zmax    = zmin   = None
	xedges  = yedges = None
	zr      = None
	zlog    = None
	zoff    = None
	zmid    = None
	zlscale = None
	zlclip  = None
	aspect  = 'auto'
	zlthresh = None

	xhist   = yhist   = False
	despine = None

	# colormap for 2-d map
	cb_outside = False
	cbar       = False
	cb_outside = False
	cb_gap     = 0.03
	cb_orientation  = None
	cb_ticklocation = None

	cb_off    = None
	cb_width  = None
	cb_length = None
	zclip     = False

	# projection histogram related
	xhist     = yhist     = False
	xh_height = yh_height = 0.15
	xh_scale  = yh_scale  = None
	xslice    = yslice    = None

	halpha    = 0.1
	hgap      = 0.04
	hheight   = 0.15
	hcolor    = "darkblue"

	invert    = False  # for mdplot_rgb

	# RGB
	dorgb       = False

	def set_default_color(self):

		pcmap = ["Blues", "Reds", "Greens", "Greys", "Purples", "Oranges"]
		icmap = 0
		lcmap = len(pcmap)

		for key, data in self.data.items():
			if data.cmap is None:
				data.cmap = pcmap[icmap]
				icmap = (icmap + 1) % lcmap

	@prep_data_deco
	def collect_data(self, key=None, help=None, hold=False, verbose: int = 0, **kwargs):
		"""
		collect data set for scatter
			-parameters are divided into two groups: one for each data
					set, and the other for common use
			-relies on the decorator for data load: see
					'(cjpy.)plottool.prep_data_deco'

			Some nontrivial parameters:
					altx, alty: 2ndary axes data
					rexpr: not used?
					attr:
						makehist: to make a histogram on the fly
						hist: data is a histogram
						poisson_error: add Poisson error
		"""

		if key is None: key = self.key
		if key not in self.data: self.data[key] = ddensity()

		base.collect_data(self, key, help=help, hold=hold, verbose=verbose, **kwargs)

		return 1

	def mdplot(self, xr=None, yr=None, **kwpars):
		"""
		2-d density plot for multiple data set
			- use this with plottool.plottool.collect_data for data load
			- best used with white color for low values (or low density)
					the color map is auto alpha corrected for low values
					- alpha: sets the minimum transparency for each image
					- halpha: sets transparency for x and y histograms
			- in principle, there is no limit for the number of data sets:
					an alternative approach is using true 3 color composition, which
					is limited to 3 separate data sets
		"""

		self.set_default_color()
		xrf, yrf = self.set_default_range()

		self.set_kwpars(kwpars)
		if xr is not None: xrf = xr
		if yr is not None: yrf = yr

		if not self.doimage:
			# data points
			self.binx, self.nbinx = get_bin(self.binsize, self.nbin, self.binx, self.nbinx, xrf)
			self.biny, self.nbiny = get_bin(self.binsize, self.nbin, self.biny, self.nbiny, yrf)
		else:
			# image input
			# assume xr, and yr is given, and probably no log scale for x and y axes?
			zmax = None
			zmin = None

			for key, data in self.data.items():
				zmax_ = np.max(data.image)
				if zmax is None: zmax = zmax_
				elif zmax < zmax_: zmax = zmax_

				zmin_ = np.min(data.image)
				if zmin is None: zmin = zmin_
				elif zmin > zmin_: zmin = zmin_

				# assume everything is identical for now
				nbinx, nbiny = data.image.shape
				binx = (xrf[1] - xrf[0]) / nbinx
				biny = (yrf[1] - yrf[0]) / nbiny

			if self.zmax is None: self.zmax = zmax
			if self.zmin is None: self.zmin = zmin

		if self.xedges is None: self.xedges = get_edges(xrf, self.nbinx, scale=self.xscale)
		if self.yedges is None: self.yedges = get_edges(yrf, self.nbiny, scale=self.yscale)

		bins = [self.xedges, self.yedges]

		zmax = None
		zmin = None
		if not self.doimage:
			# to get zmax
			self.weights = OrderedDict()
			image = OrderedDict()

			for key, data in self.data.items():
				heatmap, *_ = np.histogram2d(data.xdata, data.ydata, bins=bins)  # , weights=weights)
				image[key] = heatmap.T

				zmax_ = np.max(image[key])
				if zmax is None: zmax = zmax_
				elif zmax < zmax_: zmax = zmax_

				zmin_ = np.min(image[key])
				if zmin is None: zmin = zmin_
				elif zmin > zmin_: zmin = zmin_

				data.weights = np.ones(len(data.xdata))

		else:
			xdata, ydata = edges_to_data(self.xedges, self.yedges,
							xr=self.xr, binx=self.binx, nbinx=self.nbinx,
							yr=self.yr, biny=self.biny, nbiny=self.nbiny)

			for key, data in self.data.items():
				data.weights = data.image.flatten()
				zmax_ = np.max(data.weights)
				if zmax is None: zmax = zmax_
				elif zmax < zmax_: zmax = zmax_

				zmin_ = np.min(data.weights)
				if zmin is None: zmin = zmin_
				elif zmin > zmin_: zmin = zmin_

				if data.alpha is None:
					data.alpha = 1.0  # /self.key

		if self.dorgb:

			image = np.zeros((self.nbinx, self.nbiny, 3))
			if not self.invert:
				for key, data in self.data.items():
					if   data.color == "red"   : image[:, :, 0] = data.image
					elif data.color == "green" : image[:, :, 1] = data.image
					elif data.color == "blue"  : image[:, :, 2] = data.image
			else:
				for key,  data in self.data.items():
					if data.color[key] == "red":
						image[:, :, 1] = data.image / 2. + image[:, :, 1]
						image[:, :, 2] = data.image / 2. + image[:, :, 2]
					elif data.color[key] == "green":
						image[:, :, 0] = data.image / 2. + image[:, :, 0]
						image[:, :, 2] = data.image / 2. + image[:, :, 2]
					elif data.color[key] == "blue":
						image[:, :, 0] = data.image / 2. + image[:, :, 0]
						image[:, :, 1] = data.image / 2. + image[:, :, 1]
		else:
			# nkeys = len(self.data.keys())
			image = OrderedDict()
			for key, data in self.data.items():
				image[key] = data.image

		if self.noplot: return image, self.xedges, self.yedges
		if self.zmax is None: self.zmax = zmax
		if self.zmin is None: self.zmin = zmin

		def show():

			check_ion(self.ion)
			fig, ax = plt.subplots()

			if self.ion: plt.ion()
			norm, self.zmin, self.zmax = get_norm(zlog=self.zlog, zmid=self.zmid,
									zmin=self.zmin, zmax=self.zmax, zr=self.zr,
									zlthresh=self.zlthresh, zlscale=self.zlscale)

			im = OrderedDict()
			if not self.dorgb:
				for key, data in self.data.items():
					# cmap_N=20
					cmap             = plt.get_cmap(data.cmap)  # ,cmap_N)
					cmap_alpha       = cmap(np.arange(cmap.N))
					cmap_alpha[:, 3] = np.linspace(0, data.alpha, cmap.N)
					cmap             = ListedColormap(cmap_alpha)
					cmap.set_under((1, 1, 1, 0))

					data.image, xedges, yedges, im[key] = ax.hist2d(data.xdata, data.ydata,
									bins=bins, norm=norm, cmap=cmap, weights=data.weights)
			else:

				if not self.zlog:
					image = norm(image)
					# this will lose correct normalization factor
					if self.invert:
						diff = np.max(image) - np.min(image)
						image = 1. - image / diff
				else:
					image = norm(image.flatten()).reshape(self.nbinx, self.nbiny, 3)
					if self.invert: image = 1. - image

				for key, data in self.data.items():
					if not self.invert:
						if   data.color == 'red'   : colors_ = [(c, 0, 0, 1) for c in np.linspace(0, 1, 256)]
						elif data.color == 'green' : colors_ = [(0, c, 0, 1) for c in np.linspace(0, 1, 256)]
						elif data.color == 'blue'  : colors_ = [(0, 0, c, 1) for c in np.linspace(0, 1, 256)]
						else: continue
					else:
						if   data.color == 'red'   : colors_ = [(1, 1 - c, 1 - c, 1) for c in np.linspace(0, 0.5, 256)]
						elif data.color == 'green' : colors_ = [(1 - c, 1, 1 - c, 1) for c in np.linspace(0, 0.5, 256)]
						elif data.color == 'blue'  : colors_ = [(1 - c, 1 - c, 1, 1) for c in np.linspace(0, 0.5, 256)]
						else: continue

					cmap = colors.LinearSegmentedColormap.from_list('mycmap', colors_, N=256)
					im[key] = cm.ScalarMappable(norm=norm, cmap=cmap)

				xedges = self.xedges
				yedges = self.yedges

				ax.imshow(image, extent=[xrf[0], xrf[1], yrf[0], yrf[1]])

			ax.set_aspect(self.aspect)

			if self.xhist or self.yhist:
				if self.despine is None: self.despine = True
			despine_axes(ax, self.despine)

			if self.xhist or self.yhist:
				xdata   = OrderedDict()
				ydata   = OrderedDict()
				image   = OrderedDict()
				weights = OrderedDict()
				color   = OrderedDict()
				for key, data in self.data.items():
					xdata[key]   = data.xdata
					ydata[key]   = data.ydata
					image[key]   = data.image
					weights[key] = data.weights
					color[key]   = data.color

			if self.xhist:
				project_hist(xdata, ydata, image, weights, color,
							xedges, direction='x',
							mr=xrf, ar=yrf, zlog=self.zlog, grid=self.grid,
							scale=self.xscale, nbin=self.nbiny, anbin=self.nbinx,
							slice=self.yslice, hscale=self.xh_scale,
							hgap=self.hgap, hheight=self.hheight, halpha=self.halpha,
							doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)

			if self.yhist:
				project_hist(ydata, xdata, image, weights, color,
							yedges, direction='y',
							mr=yrf, ar=xrf, zlog=self.zlog, grid=self.grid,
							scale=self.yscale, nbin=self.nbinx, anbin=self.nbiny,
							slice=self.xslice, hscale=self.yh_scale,
							hgap=self.hgap, hheight=self.hheight, halpha=self.halpha,
							doimage=self.doimage, plt=plt, ax=ax, despine=self.despine)

			label  = OrderedDict()
			for key, data in self.data.items(): label[key] = data.label

			rect, self.loc_ylabel, self.y_title = colorbar(im, ax, fig, label,
						cbar=self.cbar, gap=self.cb_gap,
						ticklocation=self.cb_ticklocation, orientation=self.cb_orientation,
						hsize=self.hheight + self.hgap, xhist=self.xhist, yhist=self.yhist,
						loc_ylabel=self.loc_ylabel, y_title=self.y_title)

			self.wrap(plt, ax, xr=xrf, yr=yrf, label=not self.cb_outside, rect=rect)

			return image

		image = show()
		if self.hold: embed()

		return image, self.xedges, self.yedges

class spectral(base):
	ratio       = [3, 1]
	rtype       = 'relative'
	pfontsize   = 8
	pfontfamily = "monospace"
	display     = True
	xticks      = None
	yticks      = None
	xtickv      = None
	ytickv      = None

	def set_default_color(self):

		pcolor = ["black", "red", "green", "blue", "purple", "magenta", "brown", "orange", "cyan"]
		icolor = 0
		lcolor = len(pcolor)

		for key, data in self.data.items():
			if data.color is None:
				data.color = pcolor[icolor]
				icolor = (icolor + 1) % lcolor

			if data.alpha is None:
				data.alpha = 1.0  # /self.key

	def set_default_range(self):

		for key, data in self.data.items():

			if 'rrf' not in locals(): rrf = data.rr

			if rrf[0] > data.rr[0]: rrf[0] = data.rr[0]
			if rrf[1] < data.rr[1]: rrf[1] = data.rr[1]

		if self.verbose > 1: print("range:", rrf)

		xrf, yrf = base.set_default_range()
		return xrf, yrf, rrf

	@prep_data_deco
	def collect_data(self, key=None, help=None, hold=False, verbose: int = 0, **kwargs):
		"""
		collect data set for scatter
			-parameters are divided into two groups: one for each data
					set, and the other for common use
			-relies on the decorator for data load: see
					'(cjpy.)plottool.prep_data_deco'

			Some nontrivial parameters:
					altx, alty: 2ndary axes data
					rexpr: not used?
					attr:
						makehist: to make a histogram on the fly
						hist: data is a histogram
						poisson_error: add Poisson error
		"""

		if key is None: key = self.key
		if key not in self.data: self.data[key] = dspectral()

		for src in ['color', 'alpha']:
			for trg in ['err', 'mod', 'res', 'rde']:
				if trg + src not in kwargs: kwargs[trg + src] = kwargs.get(src, None)

		base.collect_data(self, key, help=help, hold=hold, verbose=verbose, **kwargs)

		if self.refer:
			self.refkey = key
			self.refer = False

		return 1

	def plot(self, xr=None, yr=None, rr=None, keys=None, lncols=1, **kwpars):
		"""Multiple Plot 1-D from input table
		"""

		if self.refkey is None:
			xrf, yrf, rrf  = self.set_default_range()
			xref = yref = None
		else:
			if not self.refset:
				self.ref = self.data.pop(self.refkey)
				self.refset = True

			xref = self.ref.xdata
			yref = self.ref.ydata
			xrf  = self.ref.xr
			yrf  = self.ref.yr
			rrf  = self.ref.rr
			_, _, _ = self.set_default_range()

		self.set_default_color()
		self.set_kwpars(kwpars)
		if xr is not None: xrf = xr
		if yr is not None: yrf = yr
		if rr is not None: rrf = rr

		def show():
			check_ion(self.ion)

			if not self.ion: plt.close('all')
			fig = plt.figure()
			gs  = fig.add_gridspec(2, hspace=0, height_ratios=self.ratio)
			ax, ax2 = gs.subplots(sharex=True)

			nonlocal xrf, yrf, rrf
			nonlocal xref, yref
			nonlocal keys

			if self.datfile is not None: pdt = OrderedDict()

			pids = []
			overwrite = True
			if keys is None: keys = self.data.keys()
			for key in keys:

				if key not in self.data:
					print(cc.err + 'No data found for', key, cc.reset)
					continue

				data = self.data[key]

				x = data.xdata
				y = data.ydata

				if data.rexpr is not None: x, y = eval(data.rexpr)

				pid = plotDMR_core(xdata=x, ydata=y, mdata=data.mdata, rdata=data.rdata, data=data.data,
					# don't clutter the plot with the details of each component
					# pdata=data.pdata,
					# mx=data.mx, my=data.my, mc=data.mc,
					mcxdata=data.mcxdata, mcdata=data.mcdata,  # mcdeco=data.mcdeco,        # module component x, data
					xr=xrf, yr=yrf, rr=rrf,
					xerrdata=data.xerrdata, yerrdata=data.yerrdata,
					xlowdata=data.xlowdata, xhighdata=data.xhighdata,
					ylowdata=data.ylowdata, yhighdata=data.yhighdata,
					marker=data.marker,    linestyle=data. linestyle,  color=data. color,  # for data
					emarker=data.emarker, elinestyle=data.elinestyle, ecolor=data.ecolor,  # for data error or range
					mmarker=data.mmarker, mlinestyle=data.mlinestyle, mcolor=data.mcolor,  # for model
					rmarker=data.rmarker, rlinestyle=data.rlinestyle, rcolor=data.rcolor,  # for residual
					smarker=data.smarker, slinestyle=data.slinestyle, scolor=data.scolor,  # for residual error or range
					rtype=self.rtype,
					pfontsize=self.pfontsize, pfontfamily=self.pfontfamily,
					ax=ax, ax2=ax2)

				overwrite = False

				if data.label != "": pids.append(pid)

			if self.noplot: return ax, ax2
			if self.dolegend:
				plt.legend(labelcolor='linecolor',
						bbox_to_anchor=self.bbox_to_anchor,
						ncol=lncols, handles=pids)

			if self.verbose > 1: print('outfile', self.outfile)

			self.wrap(plt, ax=ax, ax2=ax2, ay2=ax2,
					xr=xrf, yr=yrf, yr2=rrf, yscale2='linear',
					xticks=self.xticks, yticks=self.yticks,
					xtickv=self.xtickv, ytickv=self.ytickv)
			return ax, ax2

		ax, ax2 = show()
		if self.hold: shell()

		return ax, ax2, ay2

# for compatibility
scatter.plot = scatter.mplot1d
density.plot = density.mdplot
# ----------------------------------------------------------------------------------------
# plot Data Model Residual; e.g., spectral fit
@prep_data_deco
@prep_model_deco
def plotDMR(xdata=None, ydata=None, mdata=None, rdata=None, pdata=None, data=None,
			mcxdata=None, mcdata=None, mcdeco=None,         # module component x, data
			xr=None, yr=None, rr=None,
			xerrdata=None, yerrdata=None,
			xlowdata=None, xhighdata=None,
			ylowdata=None, yhighdata=None,
			mx=None, my=None, mc=None,
			marker='None',   linestyle='None',   color='black',  # for data
			emarker='None', elinestyle='solid', ecolor='black',  # for data error or range
			mmarker='None', mlinestyle='solid', mcolor='red',    # for model
			rmarker='None', rlinestyle='None',  rcolor='black',  # for residual
			smarker='None', slinestyle='solid', scolor='black',  # for residual error or range
			xlabel=None, ylabel=None,  ylabel2=None, rlabel=None,
			ratio=[3, 1],                                   # data portion, error portion = 1.- data portion
			outfile=None,
			rtype='relative',
			xscale='log', yscale='log',                     # often used for spectral analysis
			pfontsize=8, pfontfamily="monospace",
			xticks=None, yticks=None, xtickv=None, ytickv=None,
			help=None, display=True, ion=False, hold=False, verbose: int = 0, **kwargs):

	def show(ion=True):
		check_ion(ion)

		nonlocal xdata, ydata, mdata, rdata, data
		nonlocal xerrdata, xlowdata, xhighdata
		nonlocal yerrdata, ylowdata, yhighdata

		if not ion: plt.close('all')
		fig = plt.figure()
		gs  = fig.add_gridspec(2, hspace=0, height_ratios=ratio)
		ax, ax2 = gs.subplots(sharex=True)

		plotDMR_core(xdata=xdata, ydata=ydata, mdata=mdata, rdata=rdata, pdata=pdata, data=data,
					mcxdata=mcxdata, mcdata=mcdata, mcdeco=mcdeco,        # module component x, data
					xr=xr, yr=yr, rr=rr,
					xerrdata=xerrdata, yerrdata=yerrdata,
					xlowdata=xlowdata, xhighdata=xhighdata,
					ylowdata=ylowdata, yhighdata=yhighdata,
					mx=mx, my=my, mc=mc,
					marker=marker,    linestyle=linestyle,   color=color,   # for data
					emarker=emarker, elinestyle=elinestyle, ecolor=ecolor,  # for data error or range
					mmarker=mmarker, mlinestyle=mlinestyle, mcolor=mcolor,  # for model
					rmarker=rmarker, rlinestyle=rlinestyle, rcolor=rcolor,  # for residual
					smarker=smarker, slinestyle=slinestyle, scolor=scolor,  # for residual error or range
					rtype=rtype,
					pfontsize=pfontsize, pfontfamily=pfontfamily,
					ax=ax, ax2=ax2)

		wrap(plt, xr=xr, yr=yr, xlabel2=xlabel, ylabel=ylabel, fig=fig,
			xscale=xscale, yscale=yscale, outfile=outfile,
			ax=ax, ax2=ax2,
			ay2=ax2,  yr2=rr, yscale2='linear',
			ylabel2=ylabel2,
			xticks=xticks, yticks=yticks,
			xtickv=xtickv, ytickv=ytickv,
			display=display, ion=ion)

	show(ion=ion)
	if hold: embed()

# ----------------------------------------------------------------------------------------
# image merge for multipanel plots
def mergepdf(infile, layout=None, outfile=None,
			align=[0.5, 0.5],  # not used yet
			firstdir='x', text=None,
			verbose=0, debug=0, hold=False):
	""" merge multiple images in pdf into one page pdf file
	"""

	from PyPDF2 import PdfReader, PdfWriter, Transformation
	from PyPDF2.generic import RectangleObject

	ncol, nrow = [int(v) for v in layout.split('x')]

	images = OrderedDict()
	xsizes = np.zeros((ncol, nrow))  # , dtype=int)
	ysizes = np.zeros((ncol, nrow))  # , dtype=int)

	icol = OrderedDict()
	irow = OrderedDict()

	# figure out the size of each image
	new = True
	first = 0
	for idx, each in enumerate(infile):
		images[idx] = None

		if each is None: continue
		if each == ""  : continue

		ifile = PdfReader(each)
		images[idx] = ifile.pages[0]

		if firstdir == 'x':
			icol[idx] = int(idx % ncol)
			irow[idx] = int(idx / ncol)
		else:
			icol[idx] = int(idx / nrow)
			irow[idx] = int(idx % nrow)

		mdbox = images[idx].mediabox
		xsizes[icol[idx], irow[idx]] = mdbox.right - mdbox.left
		ysizes[icol[idx], irow[idx]] = mdbox.top   - mdbox.bottom

		if verbose > 1: print("\t", idx, icol[idx], irow[idx], xsizes[icol[idx], irow[idx]], ysizes[icol[idx], irow[idx]])
		if new:
			first = idx
			new = False

	widths  = [max(xsizes[i, :]) for i in range(0, ncol)]
	heights = [max(ysizes[:, j]) for j in range(0, nrow)]
	if verbose > 1:
		print("\twidths: ",  widths)
		print("\theights: ", heights)

	twidth  = np.sum(widths)
	theight = np.sum(heights)

	if verbose > 0: print(f"total size: {twidth} x {theight}")

	# now merge
	for key in images:
		if images[key] is None: continue
		image = images[key]
		swidth   = np.sum(widths  [:icol[key]    ])
		sheight  = np.sum(heights [:irow[key]    ])
		sheight2 = np.sum(heights [:irow[key] + 1])
		image.mediabox = RectangleObject((0, 0, twidth, theight - sheight))  # this assumes each image starts at 0,0, if not....
		transformation = Transformation().translate(tx=swidth, ty=theight - sheight2)
		if verbose > 1: print("\tshift", key, icol[key], irow[key], swidth, theight - sheight2, theight - sheight)
		image.add_transformation(transformation)

		if key == first:
			base = image
		else:
			base.merge_page(image)

	if text is not None:
		import io
		from reportlab.pdfgen.canvas import Canvas
		packet = io.BytesIO()
		c = Canvas(packet, pagesize=(twidth, theight))
		for each in text:
			x = int(each.pop('x') * twidth)
			y = theight - int(each.pop('y') * theight)
			t = each.pop('t')
			c.drawString(x, y, t)
		c.save()
		packet.seek(0)
		overlay_pdf = PdfReader(packet)
		overlay = overlay_pdf.pages[0]
		base.merge_page(overlay)

	if outfile is not None:
		writer = PdfWriter()
		base.compress_content_streams()
		writer.add_page(base)
		with open(outfile, "wb") as fp:
			writer.write(fp)

def mergepng(infile, layout=None, outfile=None, align=[0.5, 0.5],
			bgcolor='white', firstdir='x', text=None,
			verbose=0, debug=0, hold=False):
	""" merge multiple images in pdf into one page pdf file
	"""

	from PIL import Image, ImageDraw, ImageFont

	ncol, nrow = [int(v) for v in layout.split('x')]

	images = OrderedDict()
	xsizes = np.zeros((ncol, nrow), dtype=int)
	ysizes = np.zeros((ncol, nrow), dtype=int)

	icol = OrderedDict()
	irow = OrderedDict()

	# figure out the size of each image
	new = True
	first = 0
	for idx, each in enumerate(infile):
		images[idx] = None

		if each is None: continue
		if each == ""  : continue

		images[idx] = Image.open(each)

		icol[idx] = int(idx % ncol)
		irow[idx] = int(idx / ncol)

		xsizes[icol[idx], irow[idx]] = images[idx].width
		ysizes[icol[idx], irow[idx]] = images[idx].height

		if verbose > 1: print("\t", idx, icol[idx], irow[idx], xsizes[icol[idx], irow[idx]], ysizes[icol[idx], irow[idx]])
		if new:
			first = idx
			new = False

	widths  = [max(xsizes[i, :]) for i in range(0, ncol)]
	heights = [max(ysizes[:, j]) for j in range(0, nrow)]
	if verbose > 1:
		print("\twidths: ", widths)
		print("\theights: ", heights)

	twidth  = np.sum(widths)
	theight = np.sum(heights)

	if verbose > 0: print(f"total size: {twidth} x {theight}")

	# if firstdir =='x':
	#     base = Image.new('RGBA', size=(theight, twidth), color=bgcolor)
	# else:
	base = Image.new('RGBA', size=(twidth, theight), color=bgcolor)

	# now merge
	for key in images:
		if images[key] is None: continue
		image = images[key]
		if firstdir == 'x':
			i = icol[key]
			j = irow[key]
			y = sum(widths[:i]) + int((widths[i] - image.width) * align[0])
			x = sum(heights [:j]) + int((heights [j] - image.height ) * align[1])
			base.paste(image, (y, x))
		else:
			i = icol[key]
			j = irow[key]
			y = sum(heights[:i]) + int((heights[i] - image.height) * align[1])
			x = sum(widths [:j]) + int((widths [j] - image.width ) * align[0])
			base.paste(image, (x, y))

	if text is not None:
		font = ImageFont.truetype("/usr/share/fonts/truetype/Helvetica/Helvetica.ttf", 40)
		draw = ImageDraw.Draw(base)
		for each in text:
			x = int(each.pop('x') * twidth)
			y = int(each.pop('y') * theight)
			t = each.pop('t')
			draw.text((x, y), t, font=font, fill='black', align='left')

	if outfile is not None: base.save(outfile)
