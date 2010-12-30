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
__date__ = "30/12/2010"
__version__ = "0.4"

try:
    import sys
    import glob
    import os
    import platform
    import re
    from subprocess import Popen, PIPE, call
except ImportError:
    # Checks the installation of the necessary python modules 
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)

def best_unit_size(bytes_size):
    """Get a size in bytes & convert it to the best IEC prefix for readability.

    Return a dictionary with three pair of keys/values:

    's' -- (float) Size of path converted to the best unit for easy read
    'u' -- (str) The prefix (IEC) for s (from bytes(2^0) to YiB(2^80))

    """
    for exp in range(0, 90 , 10):
        bu_size = abs(bytes_size) / pow(2.0, exp)
        if int(bu_size) < 2 ** 10:
            unit = {0:'bytes', 10:'KiB', 20:'MiB', 30:'GiB', 40:'TiB', 50:'PiB',
                    60:'EiB', 70:'ZiB', 80:'YiB'}[exp]
            break
    return {'s':bu_size, 'u':unit}

def get_size(the_path):
    """Get size of a directory tree or a file in bytes."""
    path_size = 0
    for path, directories, files in os.walk(the_path):
        for filename in files:
            path_size += os.lstat(os.path.join(path, filename)).st_size
        for directory in directories:
            path_size += os.lstat(os.path.join(path, directory)).st_size
    path_size += os.path.getsize(the_path)
    return path_size

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

    # Get the original size of the images in bytes by type
    org_jpg_sz = sum((get_size(orig_jpg) for orig_jpg in jpg))
    org_png_sz = sum((get_size(orig_png) for orig_png in png))

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

    # Get the size of the processed images in bytes by type
    os.chdir(dest_path)
    prc_jpg = [j for j in glob.glob('*.jp[e|g]*') if j in jpg]
    prc_png = [p for p in glob.glob('*.png') if p in png]
    prc_jpg_sz = sum((get_size(new_j) for new_j in prc_jpg))
    prc_png_sz = sum((get_size(new_p) for new_p in prc_png))

    # Get a human readable size
    ojs, ops = best_unit_size(org_jpg_sz), best_unit_size(org_png_sz)
    pjs, pps = best_unit_size(prc_jpg_sz), best_unit_size(prc_png_sz)
    tot_org = best_unit_size(org_jpg_sz + org_png_sz)
    tot_prc = best_unit_size(prc_jpg_sz + prc_png_sz)
    sjs = best_unit_size(org_jpg_sz - prc_jpg_sz)
    sps = best_unit_size(org_png_sz - prc_png_sz)
    tts = best_unit_size((org_jpg_sz + org_png_sz) - (prc_jpg_sz + prc_png_sz))

    # print a little report    
    print('{0}{1}{0}{2:^80}{0}{1}'.format(os.linesep, '=' * 80, 'Summary'))
    print('         Original            Processed           Save' + os.linesep)
    print('.jpgs:   ({6:3}){0:>6.2f} {1:8}({7:3}){2:>6.2f} {3:8}{4:>6.2f} {5}'.
          format(ojs['s'], ojs['u'], pjs['s'], pjs['u'], sjs['s'], sjs['u'],
                 len(jpg), len(prc_jpg)))
    print('.pngs:   ({6:3}){0:>6.2f} {1:8}({7:3}){2:>6.2f} {3:8}{4:>6.2f} {5}'.
          format(ops['s'], ops['u'], pps['s'], pps['u'], sps['s'], sps['u'],
                 len(png), len(prc_png)))
    print('-' * 80)
    print('Total:   ({6:3}){0:>6.2f} {1:8}({7:3}){2:>6.2f} {3:8}{4:>6.2f} {5}'.
          format(tot_org['s'], tot_org['u'], tot_prc['s'], tot_prc['u'],
                 tts['s'], tts['u'],
                 (len(jpg) + len(png)), (len(prc_jpg) + len(prc_png))))

if __name__ == "__main__":
    WIN_EXECS, WIN_OS = check_execs_posix_win('jpegtran', 'pngcrush')
    main(WIN_EXECS, WIN_OS)
