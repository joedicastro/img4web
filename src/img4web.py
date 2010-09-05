#!/usr/bin/env python
# -*- coding: <utf8> -*-

"""
    img4web.py: optimize .jpg and .png images for the web
"""

#===============================================================================
# This Script optimizes .jpg and .png images for the web.
#
# This follows the "Yahoo Best Practices for Speeding Up Your Web Site" about
# optimize images. 
# http://developer.yahoo.com/performance/rules.html#opt_images
# 
# Uses the program pngcrush and the command jpegtran of the libjpeg library
# 
# pngcrush, http://pmt.sourceforge.net/pngcrush/
# libjpg, http://www.ijg.org/
#
# In linux they are usually available in the most popular distribution 
# repositories, e.g.: 
# In debian, Ubuntu as these packages:
# pngcrush
# libjpeg-progs
#
# In Windows pngcrush can be downloaded at 
# http://sourceforge.net/projects/pmt/files/pngcrush-executables/
# and libjpeg can be downloaded (as gnuwin32) at 
# http://gnuwin32.sourceforge.net/downlinks/jpeg.php
#
# How it runs?
#
# Get a list of .jpg and .png images in the working directory (where script 
# runs) and process all of them one by one. Store the processed images in a new
# subdirectory named 'processed' (I know, I didn't killed myself worrying about 
# the name)
#===============================================================================

#===============================================================================
#    Copyright 2009 joe di castro <joe@joedicastro.com>
#       
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#===============================================================================

__author__ = "joe di castro - joe@joedicastro.com"
__license__ = "GNU General Public License version 2"
__date__ = "19/05/2009"
__version__ = "0.2"

try:
    import glob
    import os
    import platform
    import re
    import sys
    from subprocess import Popen, PIPE, call
except ImportError:
    # Checks the installation of the necessary python modules 
    print('\n\n'.join(["An error found importing one or more modules:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)

def check_execs_posix_win(*progs):
    """Check if the programs are installed.
    
    Returns two values:
    
    (dict) windows_paths - a dictionary of executables/paths (keys/values)
    (boolean) is_windows - True it's a Windows OS, False it's a *nix OS
    
    """
    def not_found(app):
        """ If executable is not installed, exit and report."""
        msg = 'The {0} program is necessary to run this script'.format(app)
        sys.exit(msg)

    windows_paths = {}
    is_windows = True if platform.system() == 'Windows' else False
    # get all the drive unit letters if the OS is Windows
    windows_drives = re.findall(r'(\w:)\\',
                                Popen('fsutil fsinfo drives', stdout=PIPE).
                                communicate()[0]) if is_windows else None
    for prog in progs:
        if is_windows:
            # Set all commands to search the executable in all drives
            win_cmds = ['dir /B /S {0}\*{1}.exe'.format(letter, prog) for
                        letter in windows_drives]
            # Get the first location (usually in C:) of the all founded where 
            # the executable exists
            exe_paths = (''.join([Popen(cmd, stdout=PIPE, stderr=PIPE,
                                        shell=True).communicate()[0] for
                                        cmd in win_cmds])).split(os.linesep)[0]
            # Assign the path to the executable or report not found if empty
            windows_paths[prog] = exe_paths if exe_paths else not_found(prog)
        else:
            try:
                Popen([prog, '--help'], stdout=PIPE, stderr=PIPE)
            except OSError:
                not_found(prog)
    return windows_paths, is_windows


def main(execs, windows):
    """Main section."""
    # Check if exists the subdirectory for store the results, else create it
    dest_path = os.path.join(os.getcwd(), 'processed')
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
    # Get the list of all .png an .jpg images in the current folder by type
    jpg, png = glob.glob('*.jp[e|g]*'), glob.glob('*.png')
    # Get the executable's names (and path for windows) of the needed programs 
    jpegtran = execs['jpegtran'] if windows else 'jpegtran'
    pngcrush = execs['pngcrush'] if windows else 'pngcrush'
    # Process all .jpg images
    for jpg_img in jpg:
        call([jpegtran, '-copy', 'none', '-optimize', '-perfect', '-outfile',
              os.path.join(dest_path, jpg_img), jpg_img])
    # Process all .png images
    for png_img in png:
        call([pngcrush, '-rem', 'alla', '-reduce', '-brute',
              png_img, os.path.join(dest_path, png_img)])

if __name__ == "__main__":
    WIN_EXECS, WIN_OS = check_execs_posix_win('jpegtran', 'pngcrush')
    main(WIN_EXECS, WIN_OS)

