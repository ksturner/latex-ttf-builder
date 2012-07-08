#!/usr/bin/env python
'''
Simple python script to automate using ttf fonts with a latex document to
generate pdf files.

The core concepts for using one-off ttf fonts without installing them to the
system was adapted from the work of jyzhao at:
    http://math.stanford.edu/~jyzhao/latexfonts.php

Author: Kevin Turner
        @ksturner

'''
import argparse
import logging
import os
import sys

files = {
        't1.fd': '''
\ProvidesFile{t1%%%.fd}
\DeclareFontFamily{T1}{%%%}{}
\DeclareFontShape{T1}{%%%}{m}{n}{ <-> %%%}{}
\pdfmapline{+%%%\space <%%%.ttf\space <T1-WGL4.enc}
        ''',
        'T1-WGL4.enc': '''% T1-WGL4.enc
%
%
% This is LaTeX T1 encoding for WGL4 encoded TrueType fonts
% (e.g. from Windows 95)
%
%
% Note that /hyphen appears twice (for the T1 code points `hyphen' 0x2d
% and `hyphenchar' 0x7f).
%
%
% LIGKERN space l =: lslash ;
% LIGKERN space L =: Lslash ;
% LIGKERN question quoteleft =: questiondown ;
% LIGKERN exclam quoteleft =: exclamdown ;
% LIGKERN hyphen hyphen =: endash ;
% LIGKERN endash hyphen =: emdash ;
% LIGKERN quoteleft quoteleft =: quotedblleft ;
% LIGKERN quoteright quoteright =: quotedblright ;
% LIGKERN comma comma =: quotedblbase ;
% LIGKERN less less =: guillemotleft ;
% LIGKERN greater greater =: guillemotright ;
%
% LIGKERN f i =: fi ;
% LIGKERN f l =: fl ;
% LIGKERN f f =: ff ;
% LIGKERN ff i =: ffi ;
% LIGKERN ff l =: ffl ;
%
%   We blow away kerns to and from spaces (TeX doesn't have a
%   space) and also remove any kerns from the numbers.
%
% LIGKERN space {} * ; * {} space ;
% LIGKERN zero {} * ; * {} zero ;
% LIGKERN one {} * ; * {} one ;
% LIGKERN two {} * ; * {} two ;
% LIGKERN three {} * ; * {} three ;
% LIGKERN four {} * ; * {} four ;
% LIGKERN five {} * ; * {} five ;
% LIGKERN six {} * ; * {} six ;
% LIGKERN seven {} * ; * {} seven ;
% LIGKERN eight {} * ; * {} eight ;
% LIGKERN nine {} * ; * {} nine ;

/T1Encoding [          % now 256 chars follow
% 0x00
  /grave /acute /circumflex /tilde
  /dieresis /hungarumlaut /ring /caron
  /breve /macron /dotaccent /cedilla
  /ogonek /quotesinglbase /guilsinglleft /guilsinglright
% 0x10
  /quotedblleft /quotedblright /quotedblbase /guillemotleft
  /guillemotright /endash /emdash /compwordmark
  /perthousandzero /dotlessi /dotlessj /ff
  /fi /fl /ffi /ffl
% 0x20
  /visualspace /exclam /quotedbl /numbersign
  /dollar /percent /ampersand /quoteright
  /parenleft /parenright /asterisk /plus
  /comma /hyphen /period /slash
% 0x30
  /zero /one /two /three
  /four /five /six /seven
  /eight /nine /colon /semicolon
  /less /equal /greater /question
% 0x40
  /at /A /B /C
  /D /E /F /G
  /H /I /J /K
  /L /M /N /O
% 0x50
  /P /Q /R /S
  /T /U /V /W
  /X /Y /Z /bracketleft
  /backslash /bracketright /asciicircum /underscore
% 0x60
  /quoteleft /a /b /c
  /d /e /f /g
  /h /i /j /k
  /l /m /n /o
% 0x70
  /p /q /r /s
  /t /u /v /w
  /x /y /z /braceleft
  /bar /braceright /asciitilde /hyphen
% 0x80
  /Abreve /Aogonek /Cacute /Ccaron
  /Dcaron /Ecaron /Eogonek /Gbreve
  /Lacute /Lcaron /Lslash /Nacute
  /Ncaron /Eng /Odblacute /Racute
% 0x90
  /Rcaron /Sacute /Scaron /Scedilla
  /Tcaron /Tcedilla /Udblacute /Uring
  /Ydieresis /Zacute /Zcaron /Zdot
  /IJ /Idot /dmacron /section
% 0xA0
  /abreve /aogonek /cacute /ccaron
  /dcaron /ecaron /eogonek /gbreve
  /lacute /lcaron /lslash /nacute
  /ncaron /eng /odblacute /racute
% 0xB0
  /rcaron /sacute /scaron /scedilla
  /tcaron /tcedilla /udblacute /uring
  /ydieresis /zacute /zcaron /zdot
  /ij /exclamdown /questiondown /sterling
% 0xC0
  /Agrave /Aacute /Acircumflex /Atilde
  /Adieresis /Aring /AE /Ccedilla
  /Egrave /Eacute /Ecircumflex /Edieresis
  /Igrave /Iacute /Icircumflex /Idieresis
% 0xD0
  /Eth /Ntilde /Ograve /Oacute
  /Ocircumflex /Otilde /Odieresis /OE
  /Oslash /Ugrave /Uacute /Ucircumflex
  /Udieresis /Yacute /Thorn /Germandbls
% 0xE0
  /agrave /aacute /acircumflex /atilde
  /adieresis /aring /ae /ccedilla
  /egrave /eacute /ecircumflex /edieresis
  /igrave /iacute /icircumflex /idieresis
% 0xF0
  /eth /ntilde /ograve /oacute
  /ocircumflex /otilde /odieresis /oe
  /oslash /ugrave /uacute /ucircumflex
  /udieresis /yacute /thorn /germandbls
] def

% eof''',
        }

cleanup_files = []
required_lines = []


def setup_parser():
    p = argparse.ArgumentParser(description="Convert a TTF font for TeX",
                                epilog='')
    p.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                   default=sys.stdin)

    # Optional, keyword arguments
    p.add_argument('--ttfs', nargs='*')
    p.add_argument('--force', action='store_false',
                   help='whether to force file updates')
    p.add_argument('--loglevel', type=str,
                   help='one of: DEBUG, INFO, WARNING, ERROR, CRITICAL',
                   default='DEBUG')
    return p.parse_args()


def setup_logger(args):
    numeric_level = getattr(logging, args.loglevel, None)
    fmt = '%(levelname)s %(asctime)s: %(message)s'
    logging.basicConfig(level=numeric_level, format=fmt)
    logging.info('Using logging level: {0}; use --loglevel to change'.format(args.loglevel))


def handle_ttfs(args):
    ''' Takes ttf fonts and creates the files necessary for TeX to use. '''
    global cleanup_files, required_lines
    # NOTE: This is a big shell script essentially, but we do some neat things
    # like storing additional, temporary files inside the source code here so
    # that we can use them, and delete them afterwards but always know that we
    # have what we need to do what we want to do.

    # ensure enc file exists.
    fn = 'T1-WGL4.enc'
    cleanup_files.append(fn)
    if not os.path.exists(fn) or args.force:
        fout = open(fn, 'w')
        fout.write(files[fn])
        fout.close()

    for ttf in args.ttfs:
        (basename, ext) = os.path.splitext(ttf)
        logging.info("reading %s", ttf)

        if not os.path.exists(ttf):
            logging.warning('skipping {}; does not exist'.format(ttf))
            continue

        # We really want the ttf to be lowercase, so rename the file if we
        # need to.
        if basename != basename.lower():
            newttf = '{}{}'.format(basename.lower(), ext)
            logging.warning('renaming {} to {}'.format(ttf, newttf))
            os.rename(ttf, newttf)
            ttf = newttf
            basename = basename.lower()
            return

        # ensure the t1<BLAH>.fd file exists
        fn = 't1{}.fd'.format(basename)
        cleanup_files.append(fn)
        if not os.path.exists(fn) or args.force:
            fout = open(fn, 'w')
            fout.write(files['t1.fd'].replace('%%%', basename))
            fout.close()

        # ensure the tfm file exists.
        fn = '{}.tfm'.format(basename)
        cleanup_files.append(fn)
        if not os.path.exists(fn) or args.force:
            os.system('ttf2tfm {} -p T1-WGL4.enc'.format(ttf))

        if os.path.exists(fn):
            logging.info("created {} file for use.".format(fn))
            m = "\\newcommand\\%%%[1]{{\\usefont{T1}{%%%}{m}{n} #1 }}"
            m = m.replace('%%%', basename)
            required_lines.append(m)
            logging.info('add: '+m)
            logging.info('then use: \\%%%{blah blah}'.replace('%%%',basename))
        else:
            logging.warn("could NOT create {} file".format(fn))


def main(args):
    '''
    Assumes ttf files have been converted and if so, generates the
    pdf file for the tex document.
    '''
    global cleanup_files, required_lines
    data = args.infile.read()
    for line in required_lines:
        if not line in data:
            logging.error("please add '%s' to file %s",
                          line, args.infile.name)
            return

    (basename, ext) = os.path.splitext(args.infile.name)
    cmd = 'pdflatex {}'.format(args.infile.name)
    logging.info("running: {}".format(cmd))
    os.system(cmd)

    for suffix in ['.aux', '.out', '.log', '.toc']:
        fn = '{}{}'.format(basename, suffix)
        if os.path.exists(fn):
            cleanup_files.append(fn)


def cleanup_temp_files(args):
    ''' Cleans up any temporary files. '''
    global cleanup_files
    for fn in cleanup_files:
        (basename, ext) = os.path.splitext(fn)
        if not ext in ['.tex', '.png', '.ttf']:
            logging.debug('deleting {}'.format(fn))
            os.unlink(fn)
        else:
            logging.warning("skipping {} from cleanup process".format(fn))


if __name__ == '__main__':
    args = setup_parser()
    setup_logger(args)
    handle_ttfs(args)
    main(args)
    cleanup_temp_files(args)
