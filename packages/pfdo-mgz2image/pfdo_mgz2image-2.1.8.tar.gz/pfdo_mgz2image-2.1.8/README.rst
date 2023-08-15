pfdo_mgz2image 2.1.8
=====================

.. image:: https://badge.fury.io/py/pfdo_mgz2image.svg
    :target: https://badge.fury.io/py/pfdo_mgz2image

.. image:: https://travis-ci.org/FNNDSC/pfdo_mgz2image.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfdo_mgz2image

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pfdo_mgz2image

.. contents:: Table of Contents


Quick Overview
--------------

-  ``pfdo_mgz2image`` demonstrates how to use ``pftree`` to transverse directory trees and execute a ``med2image`` analysis at each directory level (that optionally contains files of interest).

Overview
--------

``pfdo_mgz2image`` leverages the ``pfree`` callback coding contract to target a specific directory with specific files in an arbitrary file tree. At each target directory, an appropriate ``med2image`` call is executed on the files contents at that nested target directory.

For example, imagine a nested tree of ``NIfTI`` image files that need to be converted to ``JPG`` in an output directory tree that preserves the structure of the input tree. In such a case, ``pfdo_mgz2image`` is a useful tool since it connects ``med2image`` to the ``pftree`` processing machinery.

Installation
------------

Dependencies
~~~~~~~~~~~~

The following dependencies are installed on your host system/python3 virtual env (they will also be automatically installed if pulled from pypi):

-  ``pfmisc`` (various misc modules and classes for the pf* family of objects)
-  ``pftree`` (create a dictionary representation of a filesystem hierarchy)
-  ``pfdo``   (the base module that does the core interfacing with ``pftree``)

Using ``PyPI``
~~~~~~~~~~~~~~

The best method of installing this script and all of its dependencies is
by fetching it from PyPI

.. code:: bash

        pip3 install pfdo_mgz2image

Command line arguments
----------------------

.. code:: html


        -I|--inputDir <inputDir>
        Input base directory to traverse.

        -O|--outputDir <outputDir>
        The output root directory that will contain a tree structure identical
        to the input directory, and each "leaf" node will contain the analysis
        results.

        [-i|--inputFile <inputFile>]
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.

        [--fileFilter <someFilter1,someFilter2,...>]
        An optional comma-delimated string to filter out files of interest
        from the <inputDir> tree. Each token in the expression is applied in
        turn over the space of files in a directory location, and only files
        that contain this token string in their filename are preserved.
        
        [--dirFilter <someFilter1,someFilter2,...>]
        Similar to the `fileFilter` but applied over the space of leaf node
        in directory paths. A directory must contain at least one file
        to be considered.
        
        If a directory leaf node contains a string that corresponds to any of
        the filter tokens, a special "hit" is recorded in the file hit list,
        "%d-<leafnode>". For example, a directory of
        
                            /some/dir/in/the/inputspace/here1234
                            
        with a `dirFilter` of `1234` will create a "special" hit entry of
        "%d-here1234" to tag this directory for processing.
        
        In addition, if a directory is filtered through, all the files in
        that directory will be added to the filtered file list. If no files
        are to be added, passing an explicit file filter with an "empty"
        single string argument, i.e. `--fileFilter " "`, is advised.

        [--analyzeFileIndex <someIndex>]
        An optional string to control which file(s) in a specific directory
        to which the analysis is applied. The default is "-1" which implies
        *ALL* files in a given directory. Other valid <someIndex> are:
            'm':   only the "middle" file in the returned file list
            "f":   only the first file in the returned file list
            "l":   only the last file in the returned file list
            "<N>": the file at index N in the file list. If this index
                   is out of bounds, no analysis is performed.
            "-1" means all files.

        [--outputLeafDir <outputLeafDirFormat>]
        If specified, will apply the <outputLeafDirFormat> to the output
        directories containing data. This is useful to blanket describe
        final output directories with some descriptive text, such as
        'anon' or 'preview'.

        This is a formatting spec, so

            --outputLeafDir 'preview-%%s'

        where %%s is the original leaf directory node, will prefix each
        final directory containing output with the text 'preview-' which
        can be useful in describing some features of the output set.

        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        [-o|--outputFileStem <outputFileStem>]
        The output file stem to store image conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.

        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.

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

        [--threads <numThreads>]
        If specified, break the innermost analysis loop into <numThreads>
        threads.

        [-x|--man]
        Show full help.

        [-y|--synopsis]
        Show brief help.

        [--json]
        If specified, output a JSON dump of final return.

        [--followLinks]
        If specified, follow symbolic links.

        -v|--verbosity <level>
        Set the app verbosity level.

            0: No internal output;
            1: Run start / stop output notification;
            2: As with level '1' but with simpleProgress bar in 'pftree';
            3: As with level '2' but with list of input dirs/files in 'pftree';
            5: As with level '3' but with explicit file logging for
                    - read
                    - analyze
                    - write


Examples
--------

Run down a directory tree and process all the files in the input tree that are ``nii``, converting them to ``jpg`` at corresponding locations in the output directory:

.. code:: bash

        pfdo_mgz2image                                      \
            -I /var/www/html/data --filter mgz              \
            -O /var/www/html/mgz                            \
            --threads 0 --printElapsedTime


The above will find all files in the tree structure rooted at /var/www/html/data that also contain the string "mgz" anywhere in the filename. For each file found, an `mgz2imgslices` conversion will be called in the output directory, in the same tree location as the original input.

Finally the elapsed time and a JSON output are printed.

