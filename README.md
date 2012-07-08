LaTeX TTF Builder
=================

Description
-----------

Maker script for generating pdfs from latex that need to use one-off ttf fonts
that you don't want to hassle with going through the error-prone process of
adding to your latex system.

Credit for the core concepts for this belong to jyzhao at:
    http://math.stanford.edu/~jyzhao/latexfonts.php

Example
-------

In general, this script can be run like the following:

```bash
python make.py test.tex --ttf custom1.ttf custom2.ttf
```

The script will generate the necessary tfm files for the ttf fonts, build
the tex file and then clean up all temporary files such that you should be
left with the ttf files and tex file.

The script should fail the first time you use it because it checks to see
if you have defined the command to use the font within your tex file.

That command will be printed in the output just above the failure. It begins
with a \newcommand..  Copy this line, add it to your tex file and rerun. You
can of course use the new font with the custom font command that the line just
defined for you.


Dependencies
------------

 * Python 2.7+
 * pdflatex
 * ttf2tfm (which usually comes with most latex packages)
 * latex package, such as texmf, etc.


Author
------

 * Kevin Turner
 * @ksturner
