
if 'clise' in __file__:
	from clise.jsontool import cc
	import clise.tabletool as tt
	import clise.plottool as pt
else:
	from jsontool import cc
	import tabletool as tt
	import plottool as pt

from collections import OrderedDict

from astropy.io import fits
from astropy    import units as un
# from pint import UnitRegistry

import numpy as np
import matplotlib.pyplot as plt
# import matplotlib.colors as colors
import scipy.optimize as opt
from scipy.interpolate import interp1d

# import matplotlib.cm as cm
import math

from scipy import ndimage
# from mpl_toolkits.axes_grid1 import make_axes_locatable
# from matplotlib import rc
# from matplotlib.patches import Circle

from IPython	import embed
import subprocess

# un = UnitRegistry()
qu = un.Quantity
PSC = 206265  # plate scale convertor in arcsec

def mirror_formula(r0=31.697, z0=1005.805, l=87.86, xi=1.0):

	# Wolter-I formula
	a   = math.atan(r0 / z0) / 4.0
	tps = 2. * xi / (1. + xi) * a
	p   = z0 * math.tan(4. * a) * math.tan(tps)
	ths = 2. * (1. + 2. * xi) / (1. + xi ) * a
	d   = z0 * math.tan(4. * a) * math.tan(4. * a - ths)
	e   = math.cos(4. * a) * (1. + math.tan(4. * a) * math.tan(ths))

	p0 = 4 * e**2 * p * d / (e**2 - 1) + p**2
	p1 = p * 2

	h0 = e**2 * d**2
	h1 = e**2 * d * 2
	h2 = e**2 - 1

	print('p:', p0, p1)
	print('h:', h0, h1, h2)
	print('sanity check for IRT  ---------------------------------------------')
	z = z0 + l
	print('P end     ', z, math.sqrt(p1 * z + p0))
	z = z0
	print('inflection', z, math.sqrt(p1 * z + p0))
	z = z0
	print('inflection', z, math.sqrt(h2 * z**2 + h1 * z + h0))
	z = z0 - l
	print('H end     ', z, math.sqrt(h2 * z**2 + h1 * z + h0))
	print

	# convert Suzanne's
	Rp = p1 / 2
	Rh = h1 / 2 + h2 * z0
	Kh = -1 - h2

	r0p = math.sqrt(p1 * z0 + p0)
	r0h = math.sqrt(h2 * z0**2 + h1 * z0 + h0)
	print('sanity check for Suzanne ----------------------------------------------')
	print('ro:', r0p, r0h, r0p - r0h)
	print('Rp:', Rp, 'Kp:', 0.0)
	print('Rh:', Rh, 'Kh:', Kh)
	z = l
	print('P end     ', z, math.sqrt(2 * Rp * z + r0p**2))
	z = 0.0
	print('inflection', z, math.sqrt(2 * Rp * z + r0p**2))
	z = 0.0
	print('inflection', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + r0h**2))
	z = -l
	print('H end     ', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + r0h**2))

	# Ed's formula
	print('sanity check for Ed ----------------------------------------------')
	Rp = p1 / 2
	z0p = -p0 / p1

	z0h = (-h1 + math.sqrt(h1**2 - 4 * h2 * h0)) / 2 / h2
	Kh = -h2 - 1
	Rh = h2 * z0h + h1 / 2

	print('Rp:', Rp, 'Kp:', p1 * z0p + p0 - 1)
	print('Rh:', Rh, 'Kh:', Kh)
	res = h2 * z0p**2 + h1 * z0p + h0
	print('z0p:', z0p, 'z0h:', z0h, 'res:', res)

	z = z0 - z0p + l
	print('P end     ', z, math.sqrt(2 * Rp * z))
	z = z0 - z0p
	print('inflection', z, math.sqrt(2 * Rp * z))

	z = z0 - z0h
	print('inflection', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2))
	z = z0 - z0h - l
	print('H end     ', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2))
	print('z0p-z0h', z0p, z0h, z0p - z0h)

	print('    ', 2 * Rh / (Kh + 1))
	print
	# Rh = +0.7490674261976 - 1 + 0.001129
	# Kh = -0.0004964139768
	Kh = -h2 - 1
	Rh = h2 * z0p + h1 / 2
	print('sanity check')
	print('Rh:', Rh, 'Kh:', Kh, Rh + 1)
	z = z0 - z0p
	print('inflection', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + res))
	z = z0 - z0p - l
	print('H end     ', z, math.sqrt(2 * Rh * z - (Kh + 1) * z**2 + res))

def q2s(each, format=""):
	return f"{each.value:{format}} {str(each.unit).replace(' ','')}"

def plate_scale_raw(focal=1, pix=10):
	um2as = PSC / focal / 1000000
	print('plate scale for focal length:', focal, 'm', pix, 'um/pix')
	print('\t', um2as,	      'arcsec/um' )
	print('\t', 1. / um2as,	      'um/srcsec' )
	print('\t', pix * um2as,      'arcsec/pix')
	print('\t', 1. / um2as / pix, 'pix/srcsec')
	return um2as, pix * um2as

def plate_scale(focal='1m', pix=None, format=".4f"):
	"""calculate plate scale of the telescope
		-focal : focal length
		-pix   : pixel size
		-format: printing format
		e.g., -focal 1m -pix 10um
	"""

	focal = qu(focal)
	um2as = PSC * un.arcsec / focal.to(un.um)
	print('plate scale for focal length:', q2s(focal))
	for each in [um2as, 1. / um2as]: print("\t" + q2s(each, format))

	if pix is None: return um2as

	pix    = qu(pix + '/pix')
	pix2as = pix * um2as
	print('for pixel:', q2s(pix))
	for each in [pix2as, 1. / pix2as]: print("\t" + q2s(each, format))
	return um2as, pix2as

def twoD_Gaussian(coords, amplitude, x0, y0, sig_x, sig_y, theta, offset):
	x, y = coords

	a =  (np.cos(theta)**2 ) / (2 * sig_x**2) + (np.sin(theta)**2 ) / (2 * sig_y**2)
	b = -(np.sin(2 * theta)) / (4 * sig_x**2) + (np.sin(2 * theta)) / (4 * sig_y**2)
	c =  (np.sin(theta)**2 ) / (2 * sig_x**2) + (np.cos(theta)**2 ) / (2 * sig_y**2)

	g = offset + amplitude * \
		np.exp(-(a * ((x - x0)**2) + 2 * b * (x - x0) * (y - y0) + c * ((y - y0)**2)))

	return g.ravel()

def twoD_Gaussian_fit(data):
	# fits a 2D gaussian to the data and uses the fit to find the FWHM
	x, y       = np.meshgrid(*[np.arange(v) for v in data.shape])
	max_pixel  = np.unravel_index(np.argmax(data), data.shape)
	max_val    = data[max_pixel]
	guess      = [max_val, max_pixel[1], max_pixel[0], 5, 5, 0, 0]
	popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), data.ravel(), p0=guess)

	twoD_Gaussian((x, y), *popt).reshape(len(x), len(y))

	# fwhm_x = 2 * np.sqrt(2 * np.log(2)) * popt[3]
	# fwhm_y = 2 * np.sqrt(2 * np.log(2)) * popt[4]
	return popt

def multiples_to_single_image(img, options='mean'):
	# usually 10 images
	if   options == 'mean'  : img = np.mean(img, axis=0)
	elif options == 'sum'   : img = np.sum(img, axis=0)
	elif options == 'single': img = img[0, :, :]  # just use the first image
	elif options == 'roll'  :
		ishape = img.shape
		for idx in range(ishape[0]):
			img[idx, :, :] = np.roll(img[idx, :, :], -idx, axis=1)
		img = np.mean(img, axis=0)
	return img

def read_img(infile, hdu=0, filter=None, options=None):
	with fits.open(infile) as hdul:
		img = hdul[0].data

	img = multiples_to_single_image(img, options=options)

	if filter is not None:
		# x y swapped?
		img[filter[1]:filter[3], filter[0]:filter[2]] = 0
	return img

# ---------------------------------------------------------------------------
class xray_mirror:

	pix   = 1.35e-5   # in meters
	focal = 0.7		# in meters

	max_range = 300  	# max range in pixel
	plateau   = 150  	# plateau region
	center    = None  # peak location of the image or center of the image

	isImage   = None  #
	verbose   = 0

	# for event data
	x     = 'x_as'  	# x column
	y     = 'y_as'  	# x column
	bin   = 1		# bin size for radial distribution in pixels
	sigma = 0		# bin size for gaussian smoothing parameter

	# how to handle multiple images
	multiples = 'mean'

	# for bkgnd sub by matching outer section
	max_var     = 1.0
	max_iter    = 1000  	# maximum iterations
	start_ratio = 1.0		# starting ratio

	# image center search method and parameter
	# img_center_search = 'gaussian_fit'
	img_center_search = 'median'
	filter_sigma = 5.0

	# generic plotting options
	rcParams = OrderedDict()
	rcParams["figure.figsize"  ] = [6.8, 6]
	rcParams["figure.dpi"	   ] = 150
	rcParams["xtick.top"	   ] = False
	rcParams["ytick.right"	   ] = False
	rcParams["axes.grid"	   ] = False
	rcParams["xtick.direction" ] = "out"
	rcParams["ytick.direction" ] = "out"

	# annotate HPD, FWHM or center
	mark		= []
	calc_psf	= False
	color_hpd	= 'orange'
	color_fwhm	= 'yellow'
	alpha_hpd	= 0.8
	alpha_fwhm	= 0.8

	# plotting options
	zlog    = False
	zmin    = 0.0
	zmax    = None
	filter  = None
	flip_x  = swap   = False
	title   = ""
	x_med	  = y_med  = None
	xhist   = yhist  = None
	xslice  = yslice = None
	despine = None
	cmap    = 'gnuplot2_r'
	aspect  = 'equal'
	xlabel  = 'x offset in arcsec'
	ylabel  = 'y offset in arcsec'
	cb_off  = None

	do_radial = False
	aper    = 60.0

	# debugging options
	verbose = 1
	debug   = 0
	hold    = False

	# for reuse
	img    = None
	psf    = None
	radial = None

	def __init__(self, **kwpars):
		self.set_kwpars(kwpars)

	def set_kwpars(self, kwargs):
		ignored = []
		for key, val in kwargs.items():
			if hasattr(self, key): setattr(self, key, val)
			else:			     ignored.append(key)
		if len(ignored) > 0:
			print(cc.err, 'Followings are not defined, so ignored, so double check:', cc.reset)
			print(cc.err, ignored, cc.reset)

		# automatic setting
		if self.yhist:
			if self.cb_off is None: self.cb_off = -0.18

		if self.zlog:
			if self.zmin <= 0: self.zmin = 1.e-3

		for each in ['HPD', 'FWHM']:
			if each in self.mark:
				self.calc_psf = True
				break

		if type(self.focal) is str:
			self.focal = qu(self.focal).to('m').value
		if type(self.pix) is str:
			self.pix = qu(self.pix).to('m').value
		if type(self.aper) is str:
			self.aper = qu(self.aper).to('arcsec').value

		return 1

	def plate_scale(self, focal=None, pix=None):
		return plate_scale(str(self.focal) + 'm', str(self.pix) + 'm')

	def pix_to_arcsec(self, pixels):
		return 7200.0 * np.degrees(np.arctan(pixels * self.pix / (2 * self.focal)))

	def arcsec_to_pix(self, arcsec):
		return 2 * self.focal / self.pix * np.tan(np.radians(arcsec / 7200.0))

	def is_image(self, data):
		if type(data) is np.ndarray: self.isImage = True
		else:				     self.isImage = False

	def find_center(self, data, center=None):
		# it's given, just use it
		if center is None:
			self.center = center
			return

		if self.isImage:
			self.center = np.unravel_index(np.argmax(data), data.shape)
		else:
			self.center = [np.median(data[self.x]), np.median(data[self.y])]

	def find_center_event(self, data, center=None, x=None, y=None):
		# it's given, just use it
		if center is None:
			self.recenter = False
			return  center

		self.recenter = True
		return [np.median(data[x]), np.median(data[y])]

	def find_center_img(self, img, center=None):
		# it's given, just use it
		if center is not None:
			return center

		if self.img_center_search == 'gaussian_fit':
			# find max_pixel from gaussian fit if not specified
			# now only used for finding the centroid
			fit    = twoD_Gaussian_fit(img)
			center = [fit[1], fit[2]]

		elif self.img_center_search == 'peak':
			center = np.unravel_index(np.argmax(img), img.shape)

		elif self.img_center_search == 'median':
			medhigh = np.where(img > 0.5 * np.max(img))
			center  = np.median(medhigh[1]), np.median(medhigh[0])

		elif self.img_center_search == 'gaussian_filter':
			# if only one value is given, use gaussian_filter
			# this must be inherited from other program
			medimg = np.median(img)
			img_   = img - medimg
			img_[img_ < 0] = 0
			img_ = ndimage.gaussian_filter(img_, sigma=self.filter_sigma)

			center = np.unravel_index(np.argmax(img_), img_.shape)

		if self.verbose >= 2: print(f"peak position from {self.img_center_search}: {center[0]:.1f} {center[1]:.1f} in pixels")
		return center

	def radial_distribution(self, data):
		center = self.center

		if self.isImage:
			offset = np.arange(self.max_range).astype('float')
			radial = np.zeros_like(offset)
			x, y   = np.meshgrid(*[np.arange(v) for v in data.shape])
			r      = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)

			for i in np.arange(self.max_range): radial[i] = np.sum(data[r < i])
		else:
			bins   = int(self.max_range / self.bin)
			radial = np.zeros_like(np.arange(bins).astype('float'))

			data['offset'] = np.sqrt((data[self.x] - center[0])**2 + (data[self.y] - center[1])**2)
			offset = []
			total  = len(data.index)
			for i in np.arange(bins):
				radial[i] = data[data['offset'] < (self.bin * i)].count()['offset'] / total
				offset.append(self.bin * i)

		return radial, offset

	def bkgsub_by_mean(self, data):
		"""subtract the average value of the masked-out image
		"""
		# mask off focal spot to find & subtract mean of bg
		x, y = np.meshgrid(*[np.arange(v) for v in data.shape])
		r =  np.sqrt((x - self.center[1]) ** 2 + (y - self.center[0]) ** 2)
		masked = np.ma.masked_where(r < self.max_range, data)
		mean   = masked.mean()
		data  -= mean
		return data

	def bkgsub_by_match(self, src, bkg):
		"""iteratively subtract the background image by keeping the plateau region flat
		"""

		radial_src, _ = self.radial_distribution(src)
		radial_bkg, _ = self.radial_distribution(bkg)
		# ax_radial = np.arange(self.max_range - 1)

		# starting point of ratio is [0.9,1.1]
		itr = 0
		ratio = self.start_ratio
		# initial ratio is set to zero, then guess first
		if self.start_ratio == 0:
			x, y = np.meshgrid(*[np.arange(v) for v in src.shape])
			r =  np.sqrt((x - self.center[1]) ** 2 + (y - self.center[0]) ** 2)
			masked_src = np.ma.masked_where(r < self.max_range, src)
			masked_bkg = np.ma.masked_where(r < self.max_range, bkg)
			ratio = masked_src.mean() / masked_bkg.mean()

		# set the search range
		upper = 1.1 * ratio
		lower = 0.9 * ratio
		if self.debug == 2: pt.embed()
		# ann_src = radial_src[self.max_range - 1] - radial_src[self.plateau]
		# ann_bkg = radial_bkg[self.max_range - 1] - radial_bkg[self.plateau]

		# to ensure at least one iteration
		var_plateau = self.max_var + 1.0

		# now search the correct ratio to match the outer section of the images
		while abs(var_plateau) > self.max_var:
			radial = radial_src - ratio * radial_bkg
			dr = np.diff(radial)
			var_plateau = np.sum(dr[self.plateau:self.max_range - 1])
			itr += 1
			if itr >= self.max_iter: break
			if var_plateau < 0:
				upper = ratio
				ratio = 0.5 * (lower + ratio)
			else:
				lower = ratio
				ratio = 0.5 * (upper + ratio)

		if self.debug == 4: pt.embed()
		return radial, ratio, var_plateau, itr

	def find_HPD(self, radial, fraction=0.5):
		radial /= np.max(radial)  # sum of ALL cts
		hpd_pix = 2 * np.interp(fraction, radial, np.arange(radial.size))
		return self.pix_to_arcsec(hpd_pix)

	def find_ECF(self, radial, radius=30.0):
		radial /= np.max(radial)  # sum of ALL cts
		radius_pix = self.arcsec_to_pix(radius)
		ecf = np.interp(radius_pix, np.arange(radial.size), radial)
		return ecf

	def find_FWHM(self, data):
		"""
		Finds the FWHM in x and y directions using linear interpolation.
		This routine only works when the PSF shape is well defined peak with high statistics.
		"""

		center  = self.center
		max_val = data[center[1], center[0]]

		x       = data[center[0], :] / max_val
		x_left  = np.interp(0.5, x[:center[1]],	       np.arange(center[1])	         )
		x_right = np.interp(0.5, x[-1:center[1] - 1:-1], np.arange(len(x), center[1], -1))

		y       = data[:, center[1]] / max_val
		y_left  = np.interp(0.5, y[:center[0]],          np.arange(center[0])	         )
		y_right = np.interp(0.5, y[-1:center[0] - 1:-1], np.arange(len(y), center[0], -1))

		if self.verbose > 1: print(x_left, x_right, y_left, y_right)
		return self.pix_to_arcsec((x_right - x_left + y_right - y_left) / 2.)

	def find_FWHM2(self, data, recenter=True):
		"""
		Find the FWHM by finding the section above the half of the peak.
		This routine works more robustly even when the PSF shape is irregular
		slightly more prone to pixellation scale.
		"""

		if recenter: half_val = np.amax(data) * 0.5
		else:
			center   = [int(self.center[0]), int(self.center[1])]
			half_val = data[center[1], center[0]] * 0.5

		npix = np.count_nonzero(data >= half_val)

		fwhm_p = 2 * np.sqrt(float(npix) / math.pi)
		return self.pix_to_arcsec(fwhm_p)

	def find_FWHM3(self, data, max_pixel=None, recenter=True):
		"""
		Find the FWHM by finding the section above the half of the peak.
		This routine works more robustly even when the PSF shape is irregular
		get the widest FWHM possible.
		"""
		if recenter: half_val = np.amax(data) * 0.5
		else:
			center   = [int(self.center[0]), int(self.center[1])]
			half_val = data[center[1], center[0]] * 0.5

		indices = np.argwhere(data >= half_val)
		dx = np.max(indices[:, 0]) - np.amin(indices[:, 0])
		dy = np.max(indices[:, 1]) - np.amin(indices[:, 1])

		fwhm_p = np.sqrt(dx * dx + dy * dy)
		return self.pix_to_arcsec(fwhm_p)

	def calc_HPD_FWHM(self, radial, img=None):
		if not self.calc_psf: return None

		# find HPD and FWHM from gaussian fit
		psf = OrderedDict()

		psf['HPD']    = self.find_HPD(radial)
		psf['Aper']   = 60.0
		psf['HPDpix'] = self.arcsec_to_pix(psf['HPD'])

		psf['ECF_Aper'] = self.find_ECF(radial, radius=psf['Aper'] / 2.)
		psf['ECF_HPD']  = 0.5

		for each in self.mark:
			if each[-1] != "%": continue
			psf['ECF_' + each] = float(each[:-1]) * 0.01
			psf[each] = self.find_HPD(radial, fraction=psf['ECF_' + each])

		if img is not None:
			# find FWHM
			psf['FWHM_l'] = self.find_FWHM2(img)
			psf['FWHM_m'] = self.find_FWHM3(img)
			psf['FWHM'  ] = psf['FWHM_m'] if psf['FWHM_m'] > psf['FWHM_l'] else psf['FWHM_l']

			psf['ECF_FWHM'] = self.find_ECF(radial, radius=psf['FWHM'] / 2.0)

		if self.verbose >= 1:
			if img is not None:
				print(f"\tHPD = {psf['HPD']:0.1f}\" {psf['HPDpix']:0.1f}p, FWHM = {psf['FWHM_l']:0.1f} - {psf['FWHM_m']:0.1f}\"")
			else:
				print(f"\tHPD = {psf['HPD']:0.1f}\" {psf['HPDpix']:0.1f}p")
			print("\tECF = %0.1f" % (psf['ECF_Aper'] * 100.) + "% for 1' dia. aperture")

		return psf

	def clip_img(self, img, xr, yr, center=None):
		xr  = np.array(xr)
		yr  = np.array(yr)
		xpr = self.arcsec_to_pix(xr)
		ypr = self.arcsec_to_pix(yr)

		xii = int(center[0] + xpr[0])
		xfi = math.ceil(center[0] + xpr[1])

		yii = int(center[1] + ypr[0])
		yfi = math.ceil(center[1] + ypr[1])

		xr  = [self.pix_to_arcsec(xii - center[0] - 0.0), self.pix_to_arcsec(xfi - center[0] + 0.0)]
		yr  = [self.pix_to_arcsec(yii - center[1] - 0.0), self.pix_to_arcsec(yfi - center[1] + 0.0)]

		if self.verbose >= 3:
			print(xii, xfi, yii, yfi, xpr, ypr, center[0] - xpr[0], center[1] + xpr[1])

		# why is this so mixed up?
		clip = img[yii:yfi, xii:xfi]
		if self.hold: embed()
		clip[clip < 0] = 0

		ny  = len(img[0])
		nx  = len(img)
		ncy = len(clip[0])
		ncx = len(clip)

		if xii < 0:
			for ii in range(-xii):
				clip = np.r_[[np.zeros(ncy)], clip]
		if xfi >= nx:
			for ii in range(xfi - nx + 1):
				clip = np.r_[clip, [np.zeros(ncy)]]
		if yii < 0:
			for ii in range(-yii):
				clip = np.c_[np.zeros(ncx), clip]
		if yfi >= ny:
			for ii in range(yfi - yii + 1):
				clip = np.c_[clip, np.zeros(ncx)]

		return clip

	def annotate_psf(self, plt, center, xr, yr, psf=None):
		if 'center' in self.mark:
			plt.plot(center[1], center[0], color='white', marker='+', markersize=2.0, alpha=0.8)

		if not self.calc_psf: return

		ax = plt.gca()
		tp = np.arange(1000) / 1000.
		if 'HPD' in self.mark:
			# likely focused images
			# alpha=0.3
			hpd = psf['HPD']
			xp  = hpd / 2 * np.cos(tp * math.pi * 2) + center[1]
			yp  = hpd / 2 * np.sin(tp * math.pi * 2) + center[0]
			plt.plot(xp, yp, color=self.color_hpd, linewidth=3, alpha=self.alpha_hpd)
			plt.xlim(xr)
			plt.ylim(yr)
			plt.text(0.95, 0.05, 'HPD: %.1f"' % hpd,
				transform=ax.transAxes, color=self.color_hpd, alpha=1.0, ha='right')

		if 'FWHM' in self.mark:
			fwhm = psf['FWHM']
			xp = fwhm / 2 * np.cos(tp * math.pi * 2) + center[1]
			yp = fwhm / 2 * np.sin(tp * math.pi * 2) + center[0]
			plt.plot(xp, yp, color=self.color_fwhm, linewidth=2, alpha=self.alpha_fwhm)
			plt.text(0.05, 0.05, 'FWHM: %.1f"' % fwhm,
				transform=ax.transAxes, color=self.color_fwhm, alpha=1.0, ha='left')

		if 'offset' in self.mark:
			offset = np.sqrt(center[0]**2 + center[1]**2) / 60.
			plt.text(0.05, 0.05, "Offset: %.1f'" % offset,
				transform=ax.transAxes, color=self.color_fwhm, alpha=1.0, ha='left')

	def plot_radial_distribution(self, radial, outfile=None, xscale='linear', psf=None, rdfile=None):
		if outfile is None: return

		rplot = pt.scatter()

		rcParams = OrderedDict()
		rcParams["legend.loc"]	= "center right"

		ax_radial_pix = np.arange(self.max_range)
		if xscale == 'linear':
			ax_radial = self.pix_to_arcsec(ax_radial_pix) / 60.0  # in arcmin
			xr = [-0.5, max(ax_radial)]
			xlabel = 'radius (arcmin)'
			arcsec_to_xaxis = 1. / 60.0
			xr2 = self.arcsec_to_pix(np.array(xr) / arcsec_to_xaxis)
		else:
			ax_radial = self.pix_to_arcsec(ax_radial_pix)  	# in arcsec
			xr = [1., max(ax_radial)]
			xlabel = 'radius (arcsec)'
			arcsec_to_xaxis = 1.0
			xr2 = self.arcsec_to_pix(np.array(xr) / arcsec_to_xaxis)

		if rdfile is not None:
			import pandas as pd
			col1 = pd.DataFrame({'radius': ax_radial})
			col2 = pd.DataFrame({'distribution': radial / max(radial)})
			dataFrame = pd.concat([col1, col2], axis=1)
			tt.to_csv_or_fits(rdfile, dataFrame, overwrite=True)

		yr = [-0.1, 1.1]
		# accumulative plot
		rplot.collect_data(xdata=ax_radial, ydata=radial / max(radial),
			label='accumulative', color="blue",
			marker='', linestyle='solid',
			rcParams=rcParams, bbox_to_anchor=[0.9, 0.55],
			add_ax2=True, xr2=xr2,
			title=self.title, grid=True, dolegend=False)

		# differential plot
		diff = np.diff(radial)
		rplot.collect_data(xdata=ax_radial[1:], ydata=diff / max(diff),
			marker='', linestyle='solid',
			label='differential', color="red")

		# plot
		ax, ax2, ay2 = rplot.mplot1d(xr=xr, xscale=xscale, yr=yr,
							xlabel=xlabel, ylabel='relative',
							xlabel2='radius (pixels)')
		ax.text(0.95, 0.95, 'accumulative', color='blue', ha='right', va='center', transform=ax.transAxes)
		ax.text(0.95, 0.05, 'differential', color='red',  ha='right', va='center', transform=ax.transAxes)

		color = 'orange'
		alpha = 0.5
		if psf is not None:

			text = OrderedDict()

			for each in self.mark:
				if each          not in psf: continue
				if 'ECF_' + each not in psf: continue
				y = psf['ECF_' + each]

				if   each     == "HPD": text[each] = '%-5s %5.1f"' % (each,  psf[each])
				elif each[-1] == "%"  : text[each] = '%-5s %5.1f"' % ('%i%%' % (y * 100), psf[each])
				else:                   text[each] = '%-5s %5.1f" %4.1f' % (each, psf[each], y * 100) + "%"

				radius = psf[each] / 2. * arcsec_to_xaxis
				ax.plot([xr[0],  radius], [y,     y], alpha=alpha, color=color)
				ax.plot([radius, radius], [yr[0], y], alpha=alpha, color=color)

			# for each in [self.max_range, self.plateau]:
			for each in [self.plateau]:
				radius = self.pix_to_arcsec(each) * arcsec_to_xaxis
				ax.plot([radius, radius], yr, alpha=alpha, color=color)

			if xscale == "log":
				for each in self.mark:
					if each          not in psf: continue
					if 'ECF_' + each not in psf: continue
					y = psf['ECF_' + each]
					ax.text(xr[0], y, " " + text[each], ha='left', va='center', family='monospace')

			else:
				ax.text(0.4, 0.5, "\n".join(text.values()), transform=ax.transAxes,
					ha='left', va='center', family='monospace')

			if self.debug == 5: pt.embed()

		plt.savefig(outfile)
		plt.clf()

	def get_psf_info_from_image(self, infile, outfile, xr, yr,
			bkgfile=None, fitsfile=None, radialplot=None, rdfile=None,
			hdu_src=0, hdu_bkg=0, reuse=False, center=None,
			**kwpars):

		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		if reuse:
			if self.img is None:
				reuse = False

		if not reuse:
			self.center = center
			if self.verbose >= 3: print('reading the image')
			img = read_img(infile, hdu=hdu_src, options=self.multiples, filter=self.filter)
			self.is_image(img)

			# search the center of the image
			# from here: somehow merge with self.set_center above
			if self.verbose >= 3: print('finding the center')
			self.center = self.find_center_img(img, center=self.center)

			if self.debug == 1: pt.embed()
			# now bkgnd subtraction using radial distribution if bkgnd img given
			if bkgfile is not None:
				if self.verbose >= 2: print('with bkg')
				bkg = read_img(bkgfile, hdu=hdu_src, options=self.multiples, filter=self.filter)

				radial, ratio, var, itr = self.bkgsub_by_match(img, bkg)
				if self.verbose >= 3: print('iterations done', ratio, var, itr)
				if abs(var) > self.max_var: print('iterations failed:', var)

				img -= bkg * ratio

				# save processed data into new fits file
				if fitsfile is not None:
					hdu = fits.PrimaryHDU(img)
					hdu.writeto(fitsfile + '.fits.gz', overwrite=True)
			else:
				if self.verbose >= 2: print('no bkg')
				medimg = np.median(img)
				img   -= medimg
				if self.verbose >= 3: print('getting the radial distribution')
				# print(end='getting the radial distribution\n' if self.verbose >= 3 else '')
				radial, offset = self.radial_distribution(img)
				if self.verbose >= 3: print('bkg subtraction by the mean')
				img   = self.bkgsub_by_mean(img)

			if self.verbose >= 1:
				print(f"{self.title}:")
				print(f"\timage center = {self.center[0]:.1f}, {self.center[1]:.1f}")

			# save img, psf and reuse them?
			if self.verbose >= 3: print('calculating PSF if requested')
			self.psf    = self.calc_HPD_FWHM(radial, img)
			self.img    = img
			self.radial = radial

		# clip the image and plot the main 2-d image
		clip = self.clip_img(self.img, xr, yr, center=self.center)

		if self.sigma > 0:
			import scipy.ndimage as ndimage
			clip = ndimage.gaussian_filter(clip, sigma=self.sigma)

		image, xedges, yedges = pt.dplot(image=clip / np.max(clip),
				xr=xr, yr=yr, title=self.title,
				xlabel=self.xlabel, ylabel=self.ylabel,
				cmap=self.cmap, zlog=self.zlog,
				zmin=self.zmin, zmax=self.zmax,
				xhist=self.xhist, yhist=self.yhist, despine=self.despine,
				xslice=self.xslice, yslice=self.yslice,
				cb_off=self.cb_off,
				aspect=self.aspect,
				rcParams=self.rcParams, display=False, hold=self.hold)

		# annotate the image and save
		halfpix = self.pix_to_arcsec(0.5)
		self.annotate_psf(plt, [halfpix, halfpix], xr, yr, psf=self.psf)
		plt.savefig(outfile)
		plt.clf()

		# plot radial distribution
		if self.zlog:
			# self.plot_radial_distribution(radial, outfile=re.sub('.png$','_log.png',radialplot), xscale='log' ,    psf=psf)
			self.plot_radial_distribution(self.radial, outfile=radialplot, xscale='log' ,   psf=self.psf, rdfile=rdfile)
		else:
			self.plot_radial_distribution(self.radial, outfile=radialplot, xscale='linear', psf=self.psf, rdfile=rdfile)

	# this assumes the unit is in mm
	def get_psf_info_from_event(self, infile, outfile, xr, yr,
			x='X_mm', y='Y_mm',
			bkgfile=None, fitsfile=None, radialplot=None,
			hdu_src=0, hdu_bkg=0, **kwpars):

		self.set_kwpars(kwpars)
		if self.verbose >= 2: print(infile)

		self.pix = 1.e-3

		evt = tt.from_csv_or_fits(infile)
		self.isImage = False

		if self.flip_x:
			evt[x] = -evt[x]

		if self.swap:
			evt['y_as'] = self.pix_to_arcsec(evt[x])  # since each pix is 1 mm...
			evt['x_as'] = self.pix_to_arcsec(evt[y])
		else:
			evt['x_as'] = self.pix_to_arcsec(evt[x])
			evt['y_as'] = self.pix_to_arcsec(evt[y])

		self.center = self.find_center_event(evt, center=self.center, x='x_as', y='y_as')

		if self.verbose >= 1:
			print(f"{self.title}:")
			print(f"\timage center = {self.center[0]:.1f}, {self.center[1]:.1f}")

		# get HPD
		radial, offset = self.radial_distribution(evt)

		# now make 2d histogram
		xr = np.array(xr)
		yr = np.array(yr)

		xr = xr + self.center[0]
		yr = yr + self.center[1]

		# data cut within the window
		evt = evt.loc[evt['x_as'] >= xr[0]]
		evt = evt.loc[evt['x_as'] <= xr[1]]
		evt = evt.loc[evt['y_as'] >= yr[0]]
		evt = evt.loc[evt['y_as'] <= yr[1]]

		if self.recenter: self.center = self.find_center_event(evt, x='x_as', y='y_as')

		image, xedges, yedges = pt.dplot(xdata=evt['x_as'], ydata=evt['y_as'], binsize=self.bin,
				xr=xr, yr=yr, title=self.title,
				xlabel=self.xlabel, ylabel=self.ylabel,
				cmap=self.cmap, zlog=self.zlog, zmin=self.zmin,
				xhist=self.xhist, yhist=self.yhist, despine=self.despine,
				xslice=self.xslice, yslice=self.yslice,
				cb_off=self.cb_off,
				aspect=self.aspect,
				rcParams=self.rcParams, display=False, hold=self.hold)

		# npix = np.count_nonzero(image >= 0.5)
		psf  = self.calc_HPD_FWHM(radial, image)
		self.annotate_psf(plt, self.center, xr, yr, psf=psf)

		plt.savefig(outfile)
		plt.clf()
		plt.close("all")

# this is getting too many input parameters....
def get_EA_from_line(srcfile, bkgfile,
	out='csv',
	xr=None,
	ch2e=None,  # channel to energy conversion
	c4ea=1.0,   # conversion to effective area
	id="", idhdr='id',
	verbose=0, hold=False):

	src = tt.from_csv_or_fits(srcfile)
	bkg = tt.from_csv_or_fits(bkgfile)

	if xr is None: xr = [0, len(src) - 1]
	if ch2e is not None:
		xr[0] = round(xr[0] / ch2e)
		xr[1] = round(xr[1] / ch2e)

	srctot = float(np.sum(src[xr[0]:xr[1]]))
	bkgtot = float(np.sum(bkg[xr[0]:xr[1]]))

	err_srctot = np.sqrt(srctot)
	err_bkgtot = np.sqrt(bkgtot)

	EA = float(srctot / bkgtot * c4ea)
	err_EA = EA * np.sqrt((err_srctot / srctot)**2 + (err_bkgtot / bkgtot)**2)

	if out == 'csv':
		if verbose > 0:
			for each in ['EA', 'err_EA', 'src', 'bkg', 'ch2e', 'c4ea', 'xlow', 'xhigh']:
				print(each, end=',')
			print(idhdr)
		for each in [EA, err_EA, srctot, bkgtot, ch2e, c4ea, xr[0], xr[1]]:
			print(each, end=',')
		print(id)
	else:
		if verbose > 1:
			print('channel->energy:', ch2e, 'conversion 4 EA:', c4ea)
			print('xr:', xr)
			print('src:', srctot, 'bkgtot:', bkgtot)
		if verbose > 0:
			print('srcfile:', srcfile)
		print('id', id)
		print('EA:', EA, '+/-', err_EA)

	if hold: pt.embed()



# ---------------------------------------------------------------------------
# SAORT output summary
# read *.dat
# apply reflectivity correction if needed
# generate plot and table fits

def from_saort_to_fits(infile, outfile, refile=None, rehdu=1, max_rescale=1.2,
		verbose=1, debug=0):

	pdt = tt.from_saort(infile)

	if refile is not None:
		rescale = tt.from_csv_or_fits(refile, hdu=rehdu)
		rescale['Ratio'] = np.clip(rescale['Ratio'], None, max_rescale)
		interpol = interp1d(rescale['Energy'], rescale['Ratio'])

	overwrite = True
	for each in pdt:
		if refile is not None:
			each['Effective_Area'] = interpol(each['Energy']) * each['Effective_Area']
		tt.to_fits(outfile, each, overwrite=overwrite)
		overwrite = False

	subprocess.check_output(['gzip -f ' + outfile], shell=True).decode()

def comsol_tank_deposit(infile, outfile=None, azfile=None, mapfile=None,
	zmin=None, zmax=None, zstep=0.1,
	tmin=None, tmax=None, tstep=1,
	savgol=[11, 2],
	margin=None, verbose=1, debug=0, **kwpars):

	dp = tt.from_csv_or_fits(infile)
	dp = dp[dp['Total'] > 0]

	if zmin is None: zmin = np.min(dp['Z'])
	else:		     dp   = dp[dp['Z'] >= zmin]
	if zmax is None: zmax = np.max(dp['Z'])
	else:		     dp   = dp[dp['Z'] <= zmax]

	# ---------------------------------------------------------------
	# plot axial variation
	z_  = np.arange(zmin, zmax + zstep, zstep)
	t   = []
	z   = []
	t25 = []
	t75 = []
	for ez in z_:
		sel = dp[(dp['Z'] >= ez - zstep * 0.5) & (dp['Z'] < ez + zstep * 0.5)]
		t_  = np.median(sel['Total'])
		if not np.isfinite(t_): continue
		t.append(t_)
		z.append(np.median(sel['Z']))
		t25.append(np.quantile(sel['Total'], 0.75))
		t75.append(np.quantile(sel['Total'], 0.25))

	t = np.array(t)
	t25 = np.array(t25)
	t75 = np.array(t75)
	# pt.plot1d(dp['Z'],dp['Total'])
	# pt.plot1d(xdata=z, ydata=t, linestyle='solid', marker='')

	rplot = pt.scatter()
	rplot.collect_data(xdata=dp['Z'], ydata=dp['Total'],
		label='raw', color="tab:blue", zorder=5,
		marker='.', linestyle='None',
		margin=margin, grid=True, dolegend=False, display=True)
	rplot.collect_data(xdata=z, ydata=t,
		ylowdata=t25, yhighdata=t75,
		zorder=6, errzorder=7, smzorder=8,
		label='smoothed', color="red",
		smooth='overlay', smcolor='orange', smlinewidth=3, savgol=savgol,
		marker='+', linestyle='None')
	rplot.mplot1d(outfile=outfile, xlabel='axial (inches)', ylabel='thickness ($\mu$m)', **kwpars)

	# ---------------------------------------------------------------
	# plot azimuthal variation
	x = dp['X']
	y = dp['Y']
	theta = []
	for ex, ey in zip(x, y):
		theta.append(math.atan2(ey, ex) * 180 / math.pi)

	dp['theta'] = theta

	if tmin is None: tmin = np.min(theta)
	if tmax is None: tmax = np.max(theta)

	theta_ = np.arange(tmin, tmax + tstep, tstep)
	thick = []
	theta = []
	t25   = []
	t75   = []
	for et in theta_:
		sel = dp[(dp['theta'] >= et - tstep * 0.5) & (dp['theta'] < et + tstep * 0.5)]
		t_ = np.median(sel['Total'])
		if not np.isfinite(t_): continue
		thick.append(t_)
		theta.append(np.median(sel['theta']))
		t25.append(np.quantile(sel['Total'], 0.75))
		t75.append(np.quantile(sel['Total'], 0.25))
	t = np.array(t)
	t25 = np.array(t25)
	t75 = np.array(t75)

	rplot = pt.scatter()
	rplot.collect_data(xdata=dp['theta'], ydata=dp['Total'],
		label='raw', color="tab:blue", zorder=5,
		marker='.', linestyle='None',
		margin=margin, grid=True, dolegend=False, display=True)
	rplot.collect_data(xdata=theta, ydata=thick,
		ylowdata=t25, yhighdata=t75,
		zorder=6, errzorder=7, smzorder=8,
		label='smoothed', color="red",
		smooth='overlay', smcolor='orange', smlinewidth=3, savgol=savgol,
		marker='+', linestyle='None')
	rplot.mplot1d(outfile=azfile, xlabel='$\\theta$ (degrees)', ylabel='thickness ($\mu$m)', **kwpars)

	xnp = dp['theta'].to_numpy()
	ynp = dp['Z'].to_numpy()
	znp = dp['Total'].to_numpy()

	# ynp,xnp,znp = zip(*sorted(zip(ynp,xnp,znp)))

	# pt.plot1d(xdata=xnp, ydata=ynp, marker='.', linestyle='solid', outfile='test.png')
	# pt.plot1d(xdata=xnp, ydata=ynp, zdata=znp, margin=0.05, marker='.', linestyle='None', attr='color', outfile='test.png')

	if 'yr' in kwpars:
		ymin = kwpars['yr'][0]
		ymax = kwpars['yr'][1]
	else:
		ymin = None
		ymax = None

	znp, xnp, ynp = pt.dplot(xdata=xnp, ydata=ynp, zdata=znp,
		xlabel='$\\theta$ (degrees)' , ylabel='axial (inches)',
		zmin=ymin, zmax=ymax,
		nbin=400,
		# noplot=True,
		cmap='turbo', outfile=mapfile)

	# pt.plot1d(xdata=xnp, ydata=ynp, zdata=znp, margin=0.05, marker='.', linestyle='None', attr='color', outfile='test2.png')
