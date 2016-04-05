import os
import hashlib
import argparse


class Dedupifier(object):

    block_size = 65536

    def __init__(self, path):
        self.path = path

    def hash_file(self, path):
        _hash = hashlib.md5()
        with open(path, 'rb') as _file:
            while True:
                data = _file.read(self.block_size)
                if not data:
                    break
                _hash.update(data)
        return _hash.hexdigest()

    def get_items(self, use_hash=False):
        self.items = {}

        for root, subdirs, files in os.walk(self.path):
            for filename in files:
                full_path = os.path.join(root, filename)

                if use_hash:
                    key = self.hash_file(full_path)
                else:
                    key = filename

                if not key in self.items:
                    self.items[key] = []

                self.items[key].append(full_path)

        return self.items


def main():
    parser = argparse.ArgumentParser(description='Dedupifier')
    parser.add_argument('-p', '--path', help='Path to directory to dedupe')
    args = parser.parse_args()

    print(args.path)



if __name__ == "__main__":
    main()