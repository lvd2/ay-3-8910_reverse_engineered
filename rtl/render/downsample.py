#!/usr/bin/python3

# (c) 2019 lvd

""" A quick and dirty downsampler for AY dump values written by render.v at 1.75 MHz AY clock.
    It mixes and downsamples the dump to 48 kHz .flac file.

    usage: downsample.py fileprefix

    The tool expects files fileprefix_a, fileprefix_b and fileprefix_c
    and outputs fileprefix.flac
"""

""" This file is part of AY-3-8910 restoration and preservation project.

    AY-3-8910 restoration and preservation project is free software: you
    can redistribute it and/or modify it under the terms of the
    GNU General Public License as published by the Free Software Foundation,
    either version 3 of the License, or (at your option) any later version.

    AY-3-8910 restoration and preservation project is distributed in the
    hope that it will be useful, but WITHOUT ANY WARRANTY; without even
    the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
    PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
"""


import os,sys
from scipy import signal
import numpy
import soundfile as sf

def main():

	if( len(sys.argv)!=2 ):
		sys.stderr.write("Usage: downsample <basename>\n, where <basename>_a, <basename>_b, <basename>_c -- ay channel renders, <basename>.flac -- result (48kHz)\n")
		sys.exit(1)

	common_fname = sys.argv[1]

	fname_a = common_fname+"_a"
	fname_b = common_fname+"_b"
	fname_c = common_fname+"_c"


	with open(fname_a,"rb") as f_a:
		orig_a = numpy.fromfile( f_a, dtype=numpy.uint16 )
	with open(fname_b,"rb") as f_b:
		orig_b = numpy.fromfile( f_b, dtype=numpy.uint16 )
	with open(fname_c,"rb") as f_c:
		orig_c = numpy.fromfile( f_c, dtype=numpy.uint16 )



	resmpld_a = signal.resample_poly( orig_a, 192, 875 ) # 218750/48000 = 875/192
	resmpld_b = signal.resample_poly( orig_b, 192, 875 )
	resmpld_c = signal.resample_poly( orig_c, 192, 875 )


	a_left  = 1.0
	a_right = 0.333

	b_left  = 0.666
	b_right = 0.666

	c_left  = 0.333
	c_right = 1.0


	left  =                   numpy.multiply( resmpld_a, a_left  )
	left  = numpy.add( left , numpy.multiply( resmpld_b, b_left  ) )
	left  = numpy.add( left , numpy.multiply( resmpld_c, c_left  ) )

	right =                   numpy.multiply( resmpld_a, a_right )
	right = numpy.add( right, numpy.multiply( resmpld_b, b_right ) )
	right = numpy.add( right, numpy.multiply( resmpld_c, c_right ) )


	(b,a) = signal.iirdesign(10,2.5,0.1,60,fs=48000,ftype='ellip')

	left  = signal.lfilter(b,a,left )
	right = signal.lfilter(b,a,right)


	max_value = max( max(left), max(right) )
	min_value = min( min(left), min(right) )
	abs_max = max( abs(max_value), abs(min_value) )


	left  = numpy.multiply(left ,1.0/abs_max)
	right = numpy.multiply(right,1.0/abs_max)



	flac_fname = common_fname+".flac"

	with sf.SoundFile(flac_fname,samplerate=48000,channels=2,format='FLAC',mode='w') as flac:
		flac.write(numpy.column_stack((left,right)))
		

	





if __name__=='__main__':
	main()

