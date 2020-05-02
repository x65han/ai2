import sys
from helper import loadMetadata, removeIfExist, saveKeys


def usage():
    print("[Usage] python script/gen-diff.py old_metadata.csv new_metadata.csv")


def main(old_path, new_path):
    old = loadMetadata(old_path)
    saveKeys('data/old_keys.txt', old.keys())

    new = loadMetadata(new_path)
    saveKeys('data/new_keys.txt', new.keys())

    diff = []
    for item in new:
        if item not in old:
            diff.append(item)

    saveKeys('data/diff_keys.txt', diff)


if __name__ == '__main__':
    args = sys.argv

    if len(args) != 3:
        usage()
    else:
        main(args[1], args[2])
