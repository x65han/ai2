import os
import csv


def removeIfExist(path):
    if os.path.exists(path):
        os.remove(path)


def mkdirIfNotExist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def loadMetadata():
    res = {}
    headers = None
    path = './data/metadata.csv'

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


def saveIndexToUidFile(index_to_uid, index):
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
