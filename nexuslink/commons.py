import sys
import urllib2
import os


def print_and_exit(message, code=-1024):
    def do_print():
        print message
        return
    def do_exit():
        if code == -1024:
            return
        else:
            sys.exit(code)
    map(lambda x: do_print() if type(x) is str else do_exit(), [message, code])


def print_and_call(message, function, *funargs):
    def do_print():
        print message
        return
    def do_exec():
        return function(*funargs)
    return [do_print(), do_exec()][1]


def getenv_or_exit(env):
    v = os.getenv(env)
    return v if v is not None else print_and_exit(write_log('No such param',
                                                            'e'),
                                                  3)

def getenv_or_none(env):
    return os.getenv(env)


def getenv_or_false(env):
    return os.getenv(env, False)


def get_or_none(l, idx):
    return l[idx] if idx < len(l) else None


def write_log(msg, lvl):
    if getenv_or_false('BATCH'):
        return ''
    return '%s %s' % (dict(d='[DEBUG]',
                           i='[INFO]',
                           w='[WARN]',
                           e='[ERROR]')[lvl],
                      msg)


def get_url(url):
    try:
        return urllib2.urlopen(url, timeout=5).read().strip()
    except urllib2.HTTPError, error:
        return print_and_exit(write_log(error, 'e'), -1)
    except urllib2.URLError, error:
        return print_and_exit(write_log(error, 'e'), -1)


def gid_to_uri(gid):
    return gid.replace('.', '/')


def filter_dict(d, f):
    return dict(filter(f, d.items()))
