# img4web

A python script to optimize [.jpg](http://en.wikipedia.org/wiki/Jpg),
[.png](http://en.wikipedia.org/wiki/Portable_Network_Graphics) and animated
[.gif](https://en.wikipedia.org/wiki/Graphics_Interchange_Format) images for the
web.

This follows the **"Yahoo Best Practices for Speeding Up Your Web Site"** about
[optimize images](http://developer.yahoo.com/performance/rules.html#opt_images).

After run it, you have a lossless optimization for the images. A small size
saving for each image, but speeds up the load of web pages and reduces the
bandwidth cost for a website.


## Pre-Requisites & Dependencies

Obviously, first we need is [python](http://www.python.org/). If we are in
Linux or Mac, usually is installed by default. If we are in Windows, download
it from [here](http://www.python.org/download/).

The python version needed for run both scripts is 2.6

img4web.py only uses python standard library modules, no needs any other module.

### External programs

Uses the program [pngcrush](http://pmt.sourceforge.net/pngcrush/), the
command **jpegtran** of the [libjpeg library](http://www.ijg.org/) and the
program [gifsicle](http://www.lcdf.org/gifsicle/).

In linux they are usually available in the most popular distribution
repositories, e.g.:
In debian, Ubuntu as these packages in their repositories: `pngcrush` &
`libjpeg-progs` & `gifsicle`

For install them:

    sudo aptitude install pngcrush
    sudo aptitude install libjpeg-progs
    sudo aptitude install gifsicle

In Windows pngcrush can be downloaded at
[here](http://sourceforge.net/projects/pmt/files/pngcrush-executables/),
libjpeg can be downloaded (as gnuwin32) at
[here](http://gnuwin32.sourceforge.net/downlinks/jpeg.php) and gifsicle can be
downloaded at [here](http://www.lcdf.org/gifsicle/)

This had been tested in linux and Windows. Sorry, I don't have a Mac.

## Using them

You need to run this script into the folder where are stored that images you
want to optimize.

Run the script is very simple,

_in linux_

    python img4web.py

_in windows_

    (path where you have installed python)\python.exe img4web.py

At the end, there's a new subdirectory called **processed** where are stored
the new processed images.

That's all! Simple, fun and fast!

## Features

After the execution it shows a little report about the image weight savings by
type.

It looks like that

    ============================================================================
                                        Summary
    ============================================================================
             Original            Processed           Save

    .jpgs:   ( 31)  2.12 MiB     ( 31)  1.82 MiB     301.28 KiB
    .pngs:   ( 10)489.46 KiB     ( 10)368.93 KiB     120.53 KiB
    .gifs:   (  4)952.71 KiB     (  4)796.06 KiB     156.66 KiB
    ----------------------------------------------------------------------------
    Total:   ( 45)  3.53 MiB     ( 45)  2.96 MiB     578.47 KiB


## How to get them

The code is hosted in a Git repository at GitHub, use this to get a clone:

    git clone git://github.com/joedicastro/img4web.git

## Contribution

Contributions and Feedback are most welcome.
To contribute to the improvement and development of this scripts, you can send
suggestions or bugs via the issues.

## License

The script is distributed under the terms of the
[GPLv3 license](http://www.gnu.org/licenses/gpl.html)

##### Apologies for any misspelling or syntax error, English isn't my mother tongue.
