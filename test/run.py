'''
Created on 2011.05.07.

@author: Zozzz
'''

import os, sys, time

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIR, "../src"))

import jsmagick
import traceback


BREAK_ON_ERROR = True
DEBUG = True

TEST_NUMBER = 0
SUCCESS = 0
FAILED = 0
TOTAL_TIME = 0.0

def terminal_width():
    width = 0

    try:
        import struct, fcntl, termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]

    except IOError:
        if width <= 0:
            try:
                width = int(os.environ['COLUMNS'])
            except:
                pass
        if width <= 0:
            width = 80

    except ImportError:
        try:
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12) #@UndefinedVariable
            csbi = create_string_buffer(22)
            res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi) #@UndefinedVariable

            if res:
                import struct
                (bufx, bufy, curx, cury, wattr, #@UnusedVariable
                 left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw) #@UnusedVariable
                width = right - left + 1
            else:
                width = 80
        except ImportError:
            pass

    return width

CHR_WIDTH = terminal_width() - 1

def runTest(dir, file):
    global TEST_NUMBER, SUCCESS, FAILED, TOTAL_TIME

    TEST_NUMBER += 1
    (head, tail) = os.path.split(dir)

    print "=" * CHR_WIDTH
    print "Test: %s/%s" % (tail, file)

    try:
        c = time.clock()

        if DEBUG:
            jsmagick.Parser.parseFile(os.path.join(dir, file)).dump()
        else:
            jsmagick.Parser.parseFile(os.path.join(dir, file))

        t = time.clock() - c
        TOTAL_TIME += t
        SUCCESS += 1
        print "OK, finished in: %f" % (t)
    except:
        FAILED += 1
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "FAIL"
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)

        if BREAK_ON_ERROR:
            raise StopIteration

    print
    #print "=" * CHR_WIDTH

_all_failed = False
for sub in os.listdir(DIR):
    _path = os.path.normpath(DIR + "/" + sub)
    if not os.path.isdir(_path):
        continue

    jsmagick.PathResolver.addSearchPath(_path)

    for _file in os.listdir(_path):
        if os.path.isfile(os.path.join(_path, _file)):
            ext = _file.split(os.path.extsep).pop()
            if ext.lower() == "py":
                try:
                    runTest(_path, _file)
                except StopIteration:
                    _all_failed = True
                    break

if _all_failed is False:
    print "=" * CHR_WIDTH
    print "SUMM: succ %d/%d, fail: %d/%d" % (TEST_NUMBER, SUCCESS, TEST_NUMBER, FAILED)
