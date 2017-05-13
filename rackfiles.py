#!/usr/bin/env python
# coding: utf-8

import os
import sys
import shlex
import logging
import argparse
import subprocess


__version__ = '0.2.0'


PY3 = sys.version_info >= (3,)

if PY3:
    xrange = range


lg = logging.getLogger('rackfiles')


class ENV:
    extra_args = 'RACKFILES_EXTRA_ARGS'


def main():
    # the `formatter_class` can make description & epilog show multiline
    parser = argparse.ArgumentParser(
        description="",
        epilog="",
        prog='rackfiles',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    # options
    parser.add_argument('-c', '--container', type=str,
                        help="container name")
    parser.add_argument('-l', '--list', action='store_true',
                        help="list files for container, if no container is specified, list containers")
    parser.add_argument('-u', '--upload', type=str, help="upload file")
    parser.add_argument('-d', '--download', type=str, help="download file")
    parser.add_argument('-D', '--delete', type=str, help="delete file")
    parser.add_argument('--debug', action='store_true',
                        help="debug mode")

    # --version
    parser.add_argument('--version', action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('* debug enabled')
        logging.debug('args: %s', args)
    else:
        logging.basicConfig(level=logging.INFO)

    extra_args = os.environ.get(ENV.extra_args, [])
    if extra_args:
        extra_args = shlex.split(extra_args)

    # logics
    if args.container:
        # list files
        if args.list:
            print('List files:')
            run_cmd_display([
                'rack', 'files', 'object', 'list',
                '--container', args.container,
            ] + extra_args)
        # upload
        elif args.upload is not None:
            fpath, fname = parse_file_path(args.upload)
            print('Uploading {}'.format(args.upload))
            run_cmd_display([
                'rack', 'files', 'object', 'upload',
                '--container', args.container,
                '--file', fpath,
                '--name', fname,
            ] + extra_args)
        # download
        elif args.download is not None:
            if os.path.exists(args.download):
                print('Warning: will overwrite the file `{}`'.format(args.download))
            print('Downloading {}'.format(args.download))
            run_cmd_display([
                'rack', 'files', 'object', 'download',
                '--container', args.container,
                '--name', args.download,
                '>', args.download,
            ] + extra_args, shell=True)
            print('Success!')
            run_cmd_display([
                'ls', '-l', args.download,
            ])
        # delete
        elif args.delete is not None:
            print('Deleting {}'.format(args.delete))
            run_cmd_display([
                'rack', 'files', 'object', 'delete',
                '--container', args.container,
                '--name', args.delete,
            ] + extra_args)
        else:
            quit_invalid_inputs()
    else:
        # list containers
        if args.list:
            print('List containers:')
            run_cmd_display([
                'rack', 'files', 'container', 'list',
            ] + extra_args, shell=True)
        else:
            quit_invalid_inputs()

    sys.stdout.flush()


def run_cmd(cmd, shell=False):
    kwargs = {}
    if shell:
        cmd = ' '.join(cmd)
        kwargs['shell'] = shell
    lg.debug('cmd: %s', cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    out, err = p.communicate()
    if PY3:
        out, err = out.decode(), err.decode()
    return p.returncode, out, err


def run_cmd_display(cmd, **kwargs):
    rc, out, err = run_cmd(cmd, **kwargs)
    if rc != 0:
        quit('Failed with {}, messages:\n{}\n{}'.format(rc, out, err), rc)
    else:
        _out = out.strip()
        _err = err.strip()
        if _out:
            print(_out)
        if _err:
            print(_err)


def quit(s, code=0):
    if s is not None:
        print(s)
    sys.exit(code)


def quit_invalid_inputs():
    return quit('Unknown operation, please check your inputs, or type `-h` to see help', 1)


def parse_file_path(filepath):
    return filepath, os.path.basename(filepath)

if __name__ == '__main__':
    main()
