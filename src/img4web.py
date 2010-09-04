#!/usr/bin/env python
# -*- coding: <utf8> -*-

"""
    img4web.py: optimize jpg and png images for the web
"""

#===============================================================================
# This Script optimices jpg and png images for the web.
#===============================================================================

#===============================================================================
#       Copyright 2009 joe di castro <joe@joedicastro.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#===============================================================================

__author__ = "joe di castro - joe@joedicastro.com"
__license__ = "GNU General Public License version 2"
__date__ = "19/05/2009"
__version__ = "0.1"

try:
    import sys
    import os
    import subprocess
    import glob
except ImportError:
    # Checks the installation of the necessary python modules 
    print('\n\n'.join(["An error found importing one or more modules:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)

def check_execs(*progs):
    """Check if the programs are installed."""
    for prog in progs:
        try:
            pipe = subprocess.PIPE
            subprocess.Popen([prog, '--help'], stdout=pipe, stderr=pipe)
        except OSError:
            msg = 'The {0} program is necessary to run this script'.format(prog)
            sys.exit(msg)
    return

def main():
    dest_path = os.path.join(os.getcwd(), 'processed')
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    jpg = glob.glob('*.jp[e|g]*')
    png = glob.glob('*.png')

    for jpg_img in jpg:
        jpg_cmd = ['jpegtran', '-copy', 'none', '-optimize', '-perfect',
                   '-outfile', os.path.join(dest_path, jpg_img), jpg_img]
        subprocess.call(jpg_cmd)
    for png_img in png:
        png_cmd = ['pngcrush', '-rem', 'alla', '-reduce', '-brute',
                    png_img, os.path.join(dest_path, png_img)]
        subprocess.call(png_cmd)

if __name__ == "__main__":
    check_execs('jpegtran', 'pngcrush')
    main()

