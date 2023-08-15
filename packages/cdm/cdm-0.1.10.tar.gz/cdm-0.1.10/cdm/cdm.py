#!/usr/bin/python
import argparse
import json
import os
import sys

import subprocess
import time

from cdm.utils import read_queue, shift_queue, pop_queue, get_file_name, file_name_index, read_db, write_queue, \
    add_to_queue
from cdm.queue import add

parser = argparse.ArgumentParser(prog="cdm", description='Charzeh Download manager')
subparsers = parser.add_subparsers(help='sub-command help', dest="command")
subparsers.required = True

parser_start = subparsers.add_parser('start', help='start downloading')
parser_start.add_argument('-o', '--output', type=str, help='output folder', dest='output')
parser_start.add_argument('-w', '--watch', help='watch for new links', action='store_true', dest='watch')
parser_start.add_argument('-n', '--no_duplicate', help='don\'t download files with the same name', action='store_true',
                          dest='ndf')
parser_start.add_argument('-m', '--no_duplicate_url', help='don\'t download files with the same url',
                          action='store_true', dest='ndu')
parser_start.add_argument('--drop-failed', help='drop failed downloads after some attempts',
                          action='store_true', dest='drop')

parser_add = subparsers.add_parser('add', help='add to queue')
parser_add.add_argument('-f', '--file', type=str, help='file path to get links from', dest='file')
parser_add.add_argument('-a', '--all', help='add all links', action='store_true', dest='all')
parser_add.add_argument('-u', '--url', type=str, help='url', dest='url')
parser_add.add_argument('-n', '--name', type=str, help='file name', dest='name')
parser_add.add_argument('--extra-axel-args', type=str, help='extra axel arguments', dest='extra_axel_args')

parser_add = subparsers.add_parser('clear', help='clear queue')

parser_export_queue = subparsers.add_parser('exportQ', help='Export queue')
parser_import_queue = subparsers.add_parser('importQ', help='Import queue')

args = parser.parse_args()


def start(args):
    print("Starting ...")

    folder = '.'
    if args.output:
        folder = args.output
    folder = os.path.abspath(folder)
    if os.path.exists(folder):
        try:
            subprocess.call(['mkdir', '-p', folder])
        except:
            print("Can't make directory {}".format(folder))
            return 1

    tries = 0
    while True:
        db = read_db()
        queue = read_queue(db)
        if not queue:
            print("Nothing to do!")
            if args.watch:
                time.sleep(5)
                continue
            return 0

        url = queue[0]
        name = None
        if isinstance(url, dict):
            name = url.get('name')
            url = url['url']
        db.setdefault('urls', {}).setdefault(url, {'state': 'p'})

        if db['urls'][url]['state'] == 'f' and not args.ndu:
            pop_queue()
            continue

        if not name:
            name = get_file_name(url)

        should_continue = False
        file_name = name
        idx = 0
        fnd = True
        while fnd:
            file_name = file_name_index(name, idx)
            fnd = os.path.exists(file_name)
            if fnd:
                if args.ndf:
                    print("Duplicate file {}, ignoring".format(file_name))
                    pop_queue()
                    should_continue = True
                    break
                idx += 1

        if should_continue:
            continue

        db['urls'][url]['state'] = 'r'

        print('Starting to download {}'.format(file_name))
        filepath = os.path.join(folder, file_name)
        if os.path.isdir(filepath) and name:
            filepath = os.path.join(filepath, name)

        status = run_axel(url, filepath)

        if status != 0:
            print("Failed to download {} :(".format(queue[0]))

            db['urls'][url]['state'] = 'w'
            db['urls'][url].setdefault('tries', 0)
            db['urls'][url]['tries'] += 1

            if db['urls'][url]['tries'] > 30 and args.drop:
                pop_queue()
            else:
                tries += 1
                time.sleep(3)
                if tries > 10:
                    tries = 0
                    shift_queue()
        else:
            print("Downloaded {} :)!".format(queue[0]))

            db['urls'][url]['state'] = 'f'
            tries = 0
            pop_queue()
    return 0


def run_axel(url, filepath):
    cmd = "axel -an 10 '{}' --max-redirect=1000 -o '{}' ".format(url, filepath) \
          + args.extra_axel_args

    return subprocess.call(cmd, shell=True)


def main():
    try:
        status = 0
        db = read_db()
        if args.command == 'start':
            status = start(args)
        elif args.command == 'add':
            status = add(args, db)
        elif args.command == 'clear':
            write_queue(db, [])
        elif args.command == 'exportQ':
            for entry in read_queue(db):
                if isinstance(entry, str):
                    print(entry)
                else:
                    print(json.dumps(entry))
        elif args.command == 'importQ':
            for line in sys.stdin:
                l = line.strip()
                obj = l
                try:
                    obj = json.loads(l)
                except:
                    pass
                add_to_queue(obj)

    except KeyboardInterrupt:
        print("Exited")
        sys.exit(3)

    sys.exit(status)


if __name__ == "__main__":
    main()
