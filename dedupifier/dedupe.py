import os
import sys
import hashlib
import argparse
import itertools
import logging
from distutils.util import strtobool

spinner = itertools.cycle(['-', '/', '|', '\\'])
logger = logging.getLogger()

class Dedupifier(object):

    block_size = 65536

    def __init__(self, path, verbosity=0, use_hash=False, log_file=None):
        self.path = path
        self.verbosity = verbosity
        self.use_hash = use_hash
        self.log_file = log_file

    def spin(self):
        sys.stdout.write('{}\b'.format(spinner.__next__()))
        sys.stdout.flush()

    def write_to_log(self):
        with self.log_file as f:
            for item in self.items:
                f.write('{}\n'.format(item))
                for file in self.items[item]:
                    f.write('  {}\n'.format(file))

    def hash_file(self, path):
        _hash = hashlib.md5()
        with open(path, 'rb') as _file:
            while True:
                data = _file.read(self.block_size)
                if not data:
                    break
                _hash.update(data)
        return _hash.hexdigest()

    def get_items(self):
        self.items = {}
        sys.stdout.write('Processing items\n')

        num_files = 0
        num_keys = 0

        for root, subdirs, files in os.walk(self.path):
            if self.verbosity > 1:
                sys.stdout.write('Entering {}\n'.format(root))

            for filename in files:

                num_files += 1
                key = None

                if self.verbosity < 2:
                    self.spin()

                full_path = os.path.join(root, filename)

                if self.use_hash:
                    try:
                        key = self.hash_file(full_path)
                    except (FileNotFoundError, OSError) as exc:
                        logger.error("{}: '{}'".format(exc.strerror, exc.filename))

                else:
                    key = filename

                if key:
                    if not key in self.items:
                        num_keys += 1
                        if self.verbosity > 1:
                            sys.stdout.write('Adding new item {} from {}\n'.format(key, full_path))
                        self.items[key] = []
                    else:
                        if self.verbosity > 1:
                            sys.stdout.write('Adding file {} to {}\n'.format(full_path, key))

                    self.items[key].append(full_path)

        sys.stdout.write('Found {} items in {} files\n'.format(num_keys, num_files))

        if self.log_file:
            sys.stdout.write('Writing results to {}\n'.format(self.log_file.name))
            self.write_to_log()

        return self.items

    def remove_duplicates(self):
        for item in self.items:
            for file in self.items[item][1:]:
                if self.verbosity > 1:
                    sys.stdout.write('Removing file {}\n'.format(file))
                os.remove(file)


def main():
    parser = argparse.ArgumentParser(description='Dedupifier')
    parser.add_argument('path', help='directory to dedupe')
    # warning: twisted logic
    parser.add_argument('-x', dest='use_hash', action='store_false', default=True,
        help='use filename as a key instead of hash')
    parser.add_argument('-l', dest='log_file', default='dedupe.log',
        type=argparse.FileType('w'), help='name of logfile to save output to [dedupe.log]')
    parser.add_argument('-v', dest='verbosity', default=0, action='count',
        help='verbosity')
    parser.add_argument('-r', '--remove', dest='remove', action='store_true', default=False,
        help='Remove duplicate files')
    args = parser.parse_args()

    dedupifier = Dedupifier(args.path, verbosity=args.verbosity, use_hash=args.use_hash, log_file=args.log_file)
    dedupifier.get_items()

    if args.remove:
        sys.stdout.write('Are you sure you want to remove duplicate files? ')
        while True:
            try:
                if strtobool(input().lower()):
                    dedupifier.remove_duplicates()
                return True
            except ValueError:
                sys.stdout.write('Please respond with y or n.\n')


if __name__ == "__main__":
    main()
