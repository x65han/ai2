import os
import csv
from typing import List


def removeIfExist(path):
    if os.path.exists(path):
        os.remove(path)


def mkdirIfNotExist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def saveKeys(path, keys: List[str]) -> None:
    removeIfExist(path)

    with open(path, 'w+') as f:
        for key in keys:
            f.write(f"{key}\n")

    print(f'[Saved] {len(keys)} keys -> {path}')


def loadKeys(path) -> List[str]:
    res = []
    with open(path, 'r') as f:
        while True:
            line = f.readline().strip()
            if line is None or len(line) == 0:
                break
            res.append(line)

    return res


def loadMetadata(path='./data/metadata.csv'):
    res = {}
    headers = None

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if headers is None:
                headers = row
                continue

            item = {}
            uid = row[0]
            for index, token in enumerate(row):
                if index != 0:
                    item[headers[index]] = token

            res[uid] = item

    return res


def loadEmbedding():
    res = {}
    path = './data/specter.csv'
    vectorDimension = None

    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            uid = row[0]
            vector = row[1:]
            res[uid] = vector

            if vectorDimension is None:
                vectorDimension = len(vector)
            else:
                assert vectorDimension == len(
                    vector), "Embedding Dimension Mismatch"

    return res, vectorDimension


def saveIndexToUidFile(index_to_uid, index, path=None):
    if path is None:
        path = f'./data/{index}.txt'
    removeIfExist(path)

    with open(path, 'w') as f:
        for index, uid in enumerate(index_to_uid):
            f.write(f"{index} {uid}\n")


def loadIndexToUidFile(index):
    res = []
    path = f'./data/{index}.txt'

    with open(path, 'r') as f:
        for line in f:
            parsed_line = line.strip().split(' ')
            i, uid = parsed_line
            res.append(uid)

    return res
