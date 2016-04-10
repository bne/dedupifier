import os
import sys
import hashlib
import argparse
import itertools


spinner = itertools.cycle(['-', '/', '|', '\\'])


class Dedupifier(object):

    block_size = 65536

    def __init__(self, path, verbosity=0, use_hash=False):
        self.path = path
        self.verbosity = verbosity
        self.use_hash = use_hash

    def spin(self):
        sys.stdout.write('{}\b'.format(spinner.__next__()))
        sys.stdout.flush()

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
        if self.verbosity < 2:
            sys.stdout.write('Processing items\n')

        num_files = 0
        num_keys = 0

        for root, subdirs, files in os.walk(self.path):
            if self.verbosity > 2:
                sys.stdout.write('Entering {}\n'.format(root))

            for filename in files:

                num_files += 1

                if self.verbosity < 2:
                    self.spin()

                full_path = os.path.join(root, filename)

                if self.use_hash:
                    key = self.hash_file(full_path)
                else:
                    key = filename

                if not key in self.items:
                    num_keys += 1
                    if self.verbosity > 1:
                        sys.stdout.write('Adding new item {} from {}\n'.format(key, full_path))
                    self.items[key] = []

                self.items[key].append(full_path)

        if self.verbosity < 2:
            sys.stdout.write('Found {} items in {} files\n'.format(num_keys, num_files))

        sys.stdout.write('\nDone\n')

        return self.items


def main():
    parser = argparse.ArgumentParser(description='Dedupifier')
    parser.add_argument('path', help='directory to dedupe')
    # warning: twisted logic
    parser.add_argument('-x', dest='hash', action='store_false', default=True,
        help='use filename as a key instead of hash')
    # parser.add_argument('-l', dest='logfile', default='dedupe.log',
    #     type=argparse.FileType('w'), help='save to logfile')
    parser.add_argument('-v', dest='verbosity', default=0, action='count', help='verbosity')
    args = parser.parse_args()

    dedupifier = Dedupifier(args.path, verbosity=args.verbosity, use_hash=args.hash)
    dedupifier.get_items()

    # for item in dedupifier.items:
    #     args.logfile.write('{}\n'.format(item))
    #     for file in dedupifier.items[item]:
    #         args.logfile.write('    {}\n'.format(file))

    # args.logfile.close()


if __name__ == "__main__":
    main()
