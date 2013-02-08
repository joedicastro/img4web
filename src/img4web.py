#!/usr/bin/env python
# -*- coding: <utf8> -*-

"""
    img4web.py: optimize .jpg and .png images for the web
"""

#==============================================================================
# This Script optimizes .jpg and .png images for the web.
#
# This follows the "Yahoo Best Practices for Speeding Up Your Web Site" about
# optimize images.
# http://developer.yahoo.com/performance/rules.html#opt_images
#
# Uses the program pngcrush, the command jpegtran of the libjpeg library and
# the program gifsicle
#
# pngcrush, http://pmt.sourceforge.net/pngcrush/
# libjpg, http://www.ijg.org/
# gifsicle, http://www.lcdf.org/gifsicle/
#
# In linux they are usually available in the most popular distribution
# repositories, e.g.:
# In debian, Ubuntu as these packages:
# pngcrush
# libjpeg-progs
# gifsicle
#
# In Windows pngcrush can be downloaded at
# http://sourceforge.net/projects/pmt/files/pngcrush-executables/
# libjpeg can be downloaded (as gnuwin32) at
# http://gnuwin32.sourceforge.net/downlinks/jpeg.php
# and gifsicle can be downloaded at
# http://www.lcdf.org/gifsicle/
#
# How it runs?
#
# By default get a list of .jpg and .png images in the working directory (where
# script runs) and process all of them one by one. Store the processed images
# in a new subdirectory named 'processed' (I know, I didn't killed myself
# worrying about the name). Also you can specify the source & destination
# directories of the images.
#==============================================================================

#==============================================================================
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
#==============================================================================

__author__ = "joe di castro - joe@joedicastro.com"
__license__ = "GNU General Public License version 2"
__date__ = "13/06/2012"
__version__ = "0.7"

try:
    import os
    import glob
    import platform
    import re
    import sys
    from argparse import ArgumentParser
    from subprocess import Popen, PIPE, call
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def arguments():
    """Defines the command line arguments for the script."""
    cur_dir = os.path.curdir
    dest_dir = os.path.join(cur_dir, "processed")
    main_desc = """Optimize .jpg and .png images for the web"""

    parser = ArgumentParser(description=main_desc)
    parser.add_argument("-s", "--src", dest="src", default=cur_dir, help="the "
                        "source path. Current dir if none is provided")
    parser.add_argument("-d", "--dst", dest="dst", default=dest_dir,
                        help="the destination path. './processed/' if none is "
                        "provided")
    parser.add_argument("--exif", dest="exif", action="store_true",
                        help="preserve the EXIF data from jpeg files")
    parser.add_argument("--delete", dest="delete", action="store_true",
                        help="delete the original image files")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s {0}".format(__version__),
                        help="show program's version number and exit")
    return parser


def best_unit_size(bytes_size):
    """Get a size in bytes & convert it to the best IEC prefix for readability.

    Return a dictionary with three pair of keys/values:

    's' -- (float) Size of path converted to the best unit for easy read
    'u' -- (str) The prefix (IEC) for s (from bytes(2^0) to YiB(2^80))

    """
    for exp in range(0, 90, 10):
        bu_size = abs(bytes_size) / pow(2.0, exp)
        if int(bu_size) < 2 ** 10:
            unit = {0: 'bytes', 10: 'KiB', 20: 'MiB', 30: 'GiB', 40: 'TiB',
                    50: 'PiB', 60: 'EiB', 70: 'ZiB', 80: 'YiB'}[exp]
            break
    return {'s': bu_size, 'u': unit}


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


def check_execs_posix_win(progs):
    """Check if the program is installed.

    Returns one  dictionary with 1+n pair of key/values:

    A fixed key/value:

    "WinOS" -- (boolean) True it's a Windows OS, False it's a *nix OS

    for each program in progs a key/value like this:

    "program"  -- (str or boolean) The Windows executable path if founded else
                                   '' if it's Windows OS. If it's a *NIX OS
                                   True if founded else False

    """
    execs = {'WinOS':  True if platform.system() == 'Windows' else False}
    # get all the drive unit letters if the OS is Windows
    windows_drives = re.findall(r'(\w:)\\',
                                Popen('fsutil fsinfo drives', stdout=PIPE).
                                communicate()[0]) if execs['WinOS'] else None

    progs = [progs] if isinstance(progs, str) else progs
    for prog in progs:
        if execs['WinOS']:
            # Set all commands to search the executable in all drives
            win_cmds = ['dir /B /S {0}\*{1}.exe'.format(letter, prog) for
                        letter in windows_drives]
            # Get the first location (usually C:) where the executable exists
            for cmd in win_cmds:
                execs[prog] = (Popen(cmd, stdout=PIPE, stderr=PIPE, shell=1).
                               communicate()[0].split(os.linesep)[0])
                if execs[prog]:
                    break
        else:
            try:
                Popen([prog, '--help'], stdout=PIPE, stderr=PIPE)
                execs[prog] = True
            except OSError:
                execs[prog] = False
    return execs


def main():
    """Main section."""
    args = arguments().parse_args()

    # Check if exists the subdirectory for store the results, else create it
    src_path = os.path.abspath(args.src)
    dst_path = os.path.abspath(args.dst)
    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    # Get the list of all .png, .jpg and .gif images in the current folder by
    # type
    os.chdir(src_path)
    jpg = glob.glob('*.jp[e|g]*')
    png = glob.glob('*.png')
    gif = glob.glob('*.gif')

    # Get the original size of the images in bytes by type
    org_jpg_sz = sum((get_size(orig_jpg) for orig_jpg in jpg))
    org_png_sz = sum((get_size(orig_png) for orig_png in png))
    org_gif_sz = sum((get_size(orig_gif) for orig_gif in gif))

    # Get the executable's names (and path for windows) of the needed programs
    jpegtran = EXECS['jpegtran'] if EXECS['WinOS'] else 'jpegtran'
    pngcrush = EXECS['pngcrush'] if EXECS['WinOS'] else 'pngcrush'
    gifsicle = EXECS['gifsicle'] if EXECS['WinOS'] else 'gifsicle'
    exif = 'all' if args.exif else 'none'

    # Process all .jpg images
    for jpg_img in jpg:
        call([jpegtran, '-copy', exif, '-optimize', '-perfect', '-outfile',
              os.path.join(dst_path, jpg_img),
              os.path.join(src_path, jpg_img)])

    # Process all .png images
    for png_img in png:
        call([pngcrush, '-rem', 'alla', '-reduce', '-brute',
              os.path.join(src_path, png_img),
              os.path.join(dst_path, png_img)])

    # Process all .gif images (only optimize animated ones)
    for gif_img in gif:
        call([gifsicle, '-O2', os.path.join(src_path, gif_img), "--output",
              os.path.join(dst_path, gif_img)])

    # Get the size of the processed images in bytes by type
    os.chdir(dst_path)
    prc_jpg = [j for j in glob.glob('*.jp[e|g]*') if j in jpg]
    prc_png = [p for p in glob.glob('*.png') if p in png]
    prc_gif = [g for g in glob.glob('*.gif') if g in gif]
    prc_jpg_sz = sum((get_size(new_j) for new_j in prc_jpg))
    prc_png_sz = sum((get_size(new_p) for new_p in prc_png))
    prc_gif_sz = sum((get_size(new_g) for new_g in prc_gif))

    # Get a human readable size
    ojs = best_unit_size(org_jpg_sz)
    ops = best_unit_size(org_png_sz)
    ogs = best_unit_size(org_gif_sz)

    pjs = best_unit_size(prc_jpg_sz)
    pps = best_unit_size(prc_png_sz)
    pgs = best_unit_size(prc_gif_sz)

    tot_org = best_unit_size(org_jpg_sz + org_png_sz + org_gif_sz)
    tot_prc = best_unit_size(prc_jpg_sz + prc_png_sz + prc_gif_sz)

    sjs = best_unit_size(org_jpg_sz - prc_jpg_sz)
    sps = best_unit_size(org_png_sz - prc_png_sz)
    sgs = best_unit_size(org_gif_sz - prc_gif_sz)
    tts = best_unit_size((org_jpg_sz + org_png_sz + org_gif_sz) -
                         (prc_jpg_sz + prc_png_sz + prc_gif_sz))

    # Delete original image files if requested
    if args.delete:
        for to_trash_jpg in jpg:
            os.remove(os.path.join(src_path, to_trash_jpg))
        for to_trash_png in png:
            os.remove(os.path.join(src_path, to_trash_png))
        for to_trash_gif in gif:
            os.remove(os.path.join(src_path, to_trash_gif))

    # print a little report
    print('{0}{1}{0}{2:^80}{0}{1}'.format(os.linesep, '=' * 80, 'Summary'))
    print('         Original            Processed           Save' + os.linesep)
    print('.jpgs:   ({6:3}){0:>6.2f} {1:8}({7:3}){2:>6.2f} {3:8}{4:>6.2f} {5}'.
          format(ojs['s'], ojs['u'], pjs['s'], pjs['u'], sjs['s'], sjs['u'],
                 len(jpg), len(prc_jpg)))
    print('.pngs:   ({6:3}){0:>6.2f} {1:8}({7:3}){2:>6.2f} {3:8}{4:>6.2f} {5}'.
          format(ops['s'], ops['u'], pps['s'], pps['u'], sps['s'], sps['u'],
                 len(png), len(prc_png)))
    print('.gifs:   ({6:3}){0:>6.2f} {1:8}({7:3}){2:>6.2f} {3:8}{4:>6.2f} {5}'.
          format(ogs['s'], ogs['u'], pgs['s'], pgs['u'], sgs['s'], sgs['u'],
                 len(gif), len(prc_gif)))
    print('-' * 80)
    print('Total:   ({6:3}){0:>6.2f} {1:8}({7:3}){2:>6.2f} {3:8}{4:>6.2f} {5}'.
          format(tot_org['s'], tot_org['u'], tot_prc['s'], tot_prc['u'],
                 tts['s'], tts['u'],
                 (len(jpg) + len(png) + len(gif)),
                 (len(prc_jpg) + len(prc_png) + len(prc_gif))))

if __name__ == "__main__":
    EXECS = check_execs_posix_win(['jpegtran', 'pngcrush', 'gifsicle'])
    main()
