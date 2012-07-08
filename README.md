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

For example, if if if, I have a font file called *kevin.ttf*, the tex to
define that font command that I would need to add would look like:

```latex
\newcommand\kevin[1]{{\usefont{T1}{kevin}{m}{n} #1 }}
```

I would then use the font later in the tex document like this:


```latex
\kevin{some text here that I want in this font}
```

If you have both of those lines in your tex file, you should see the font
in the rendered pdf file.


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
