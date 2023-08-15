#!/usr/bin/env python3
#
# (c) 2022 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import sys, os

import  pfdo.__main__       as pfdo_main
import  pfdo
from pfdo_mgz2image.pfdo_mgz2image import pfdo_mgz2image
from pfdo_mgz2image import __pkg, __version__

from    argparse            import RawTextHelpFormatter
from    argparse            import ArgumentParser
import  pudb

import  pfmisc
from    pfmisc._colors      import Colors
from    pfmisc              import other

str_desc = Colors.CYAN + """
        __    _                             _____ _
       / _|  | |                           / __  (_)
 _ __ | |_ __| | ___   _ __ ___   __ _ ____`' / /'_ _ __ ___   __ _  __ _  ___
| '_ \|  _/ _` |/ _ \ | '_ ` _ \ / _` |_  /  / / | | '_ ` _ \ / _` |/ _` |/ _ \\
| |_) | || (_| | (_) || | | | | | (_| |/ / ./ /__| | | | | | | (_| | (_| |  __/
| .__/|_| \__,_|\___/ |_| |_| |_|\__, /___|\_____/_|_| |_| |_|\__,_|\__, |\___|
| |               ______          __/ |                              __/ |
|_|              |______|        |___/                              |___/


                          Path-File Do mgz2image

        Recursively walk down a directory tree and perform a 'mgz2image'
        on files in each directory (optionally filtered by some simple
        expression). Results of each operation are saved in output tree
        that  preserves the input directory structure.


                             -- version """ + \
             Colors.YELLOW + __version__ + Colors.CYAN + """ --

        'pfdo_mgz2image' demonstrates how to use ``pftree`` to transverse
        directory trees and execute a ``mgz2image`` analysis at each directory
        level (that optionally contains files of interest).

        As part of the "pf*" suite of applications, it is geared to IO as
        directories. Nested directory trees within some input directory
        are reconstructed in an output directory, preserving directory
        structure.


""" + Colors.NO_COLOUR

package_CLI = '''
        [--saveImages]                                              \\
        [--label <prefixForLabelDirectories>]                       \\
        [-n|--normalize]                                            \\
        [-l|--lookupTable <LUTfile>]                                \\
        [--skipAllLabels]                                           \\
        [-s|--skipLabelValueList <ListOfVoxelValuesToSkip>]         \\
        [-f|--filterLabelValueList <ListOfVoxelValuesToInclude>]    \\
        [-w|--wholeVolume <wholeVolDirName>]                        \\'''+\
        pfdo_main.package_CLIfull

package_argSynopsis = pfdo_main.package_argsSynopsisFull + '''
        [--saveImages]
        If specified as True(boolean), will save the slices of the mgz file as
        ".png" image files along with the numpy files.

        [--label <prefixForLabelDirectories>]
        Prefixes the string <prefixForLabelDirectories> to each filtered
        directory name. This is mostly for possible downstream processing,
        allowing a subsequent operation to easily determine which of the output
        directories correspond to labels.

        [-n|--normalize]
        If specified as True(boolean), will normalize the output image pixel values to
        0 and 1, otherwise pixel image values will retain the value in
        the original input volume.

        [-l|--lookupTable <LUTfile>]
        Need to pass a <LUTfile> (eg. FreeSurferColorLUT.txt)
        to perform a looktup on the filtered voxel label values
        according to the contents of the <LUTfile>. This <LUTfile> should
        conform to the FreeSurfer lookup table format (documented elsewhere).

        Note that the special <LUTfile> string ``__val__`` can be passed only when
        running the docker image (fnndsc/pl-mgz2imageslices) of this utility which
        effectively means "no <LUTfile>". In this case, the numerical voxel
        values are used for output directory names. This special string is
        really only useful for scripted cases of running this application when
        modifying the CLI is more complex than simply setting the <LUTfile> to
        ``__val__``.

        While running the docker image, you can also pass ``__fs__`` which will use
        the FreeSurferColorLUT.txt from within the docker container to perform a
        looktup on the filtered voxel label values according to the contents of
        the FreeSurferColorLUT.txt

        [--skipAllLabels]
        Skips all labels and converts only the whole mgz volume to png/jpg images.

        [-s|--skipLabelValueList <ListOfLabelNumbersToSkip>]
        If specified as a comma separated string of label numbers,
        will not create directories of those label numbers.

        [-f|--filterLabelValues <ListOfVoxelValuesToInclude>]
        The logical inverse of the [skipLabelValueList] flag. If specified,
        only filter the comma separated list of passed voxel values from the
        input volume.

        The detault value of "-1" implies all voxel values should be filtered.

        [-w|--wholeVolume <wholeVolDirName>]
        If specified, creates a diretory called <wholeVolDirName> (within the
        outputdir) containing PNG/JPG images files of the entire input.

        This effectively really creates a PNG/JPG conversion of the input
        mgz file.

        Values in the image files will be the same as the original voxel
        values in the ``mgz``, unless the [--normalize] flag is specified
        in which case this creates a single-value mask of the input image.

'''

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis =  """
    NAME

        pfdo_mgz2image

    SYNOPSIS

        pfdo_mgz2image """ + package_CLI + """

    BRIEF EXAMPLE

        pfdo_mgz2image                                                          \\
            -I /var/www/html/data --filter mgz                                  \\
            -O /var/www/html/jpg                                                \\
            -t jpg                                                              \\
            --threads 0 --printElapsedTime
    """

    description =  '''
    DESCRIPTION

        ``pfdo_mgz2image`` runs ``mgz2image`` at each path/file location in an
        input tree. The CLI space is the union of ``pfdo`` and ``mgz2image``.

    ARGS ''' + package_argSynopsis + '''

    EXAMPLES

    Perform a `pfdo_mgz2image` down some input directory:

        pfdo_mgz2image                                      \\
            -I /var/www/html/data --filter nii              \\
            -O /var/www/html/jpg                            \\
            -t jpg                                          \\
            --threads 0 --printElapsedTime

    The above will find all files in the tree structure rooted at
    /var/www/html/data that also contain the string "nii" anywhere
    in the filename. For each file found, a `mgz2image` conversion
    will be called in the output directory, in the same tree location as
    the original input.

    Finally the elapsed time and a JSON output are printed.

    '''

    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description



parser              = pfdo_main.parserSA
parser.description  = str_desc

# mgz2image additional CLI flags
parser.add_argument("-o", "--outputFileStem",
                    help    = "output file",
                    default = "output.jpg",
                    dest    = 'outputFileStem')
parser.add_argument("-t", "--outputFileType",
                    help    = "output image type",
                    dest    = 'outputFileType',
                    default = '')
parser.add_argument('--saveImages',
                    help='store png images for each slice of mgz file',
                    dest='saveImages',
                    action= 'store_true',
                    default = False
                    )
parser.add_argument('--label',
                    help='prefix a label to all the label directories',
                    dest='label',
                    default = 'label'
                    )
parser.add_argument('-n', '--normalize',
                    help='normalize the pixels of output image files',
                    dest='normalize',
                    action= 'store_true',
                    default = False
                    )
parser.add_argument('-l', '--lookupTable',
                    help='file contain text string lookups for voxel values',
                    dest='lookupTable',
                    default = '__none__'
                    )
parser.add_argument('--skipAllLabels',
                    help='skip all labels and create only whole Volume images',
                    dest='skipAllLabels',
                    action='store_true',
                    default=False)
parser.add_argument('-s', '--skipLabelValueList',
                    help='Comma separated list of voxel values to skip',
                    dest='skipLabelValueList',
                    default = ''
                    )
parser.add_argument('--filterLabelValueList',
                    help='Comma separated list of voxel values to include',
                    dest='filterLabelValueList',
                    default = "-1"
                    )
parser.add_argument('-w', '--wholeVolume',
                    help='Converts entire mgz volume to png/jpg instead of individually masked labels',
                    dest='wholeVolume',
                    default = 'wholeVolume'
                    )
parser.add_argument('-a', '--args',
                    help='pass args for individually for each mgz file mentioned in filterExpression',
                    dest='args',
                    default='')

def main(argv = None):
    args = parser.parse_args()

    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        sys.exit(1)

    if args.b_version:
        print("Name:    %s\nVersion: %s" % (__pkg.name, __version__))
        sys.exit(1)

    args.str_version    = __version__
    args.str_desc       = synopsis(True)

    pf_do_mgz2image     = pfdo_mgz2image(vars(args))

    # And now run it!
    # pudb.set_trace()
    d_pfdo_mgz2image    = pf_do_mgz2image.run(timerStart = True)

    if args.printElapsedTime:
        pf_do_mgz2image.dp.qprint(
                "Elapsed time = %f seconds" %
                d_pfdo_mgz2image['runTime']
        )

    sys.exit(0)

if __name__ == "__main__":
    sys.exit(main())
