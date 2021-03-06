import os
import hnswlib
from random import randint
from util import helper
from flask import url_for

# Constants
DIM = None
HNSW = None
TOTAL_NUM_ELEMENTS = None
metadata = {}
embedding = {}
index_to_uid = []
diff_keys = []


# Main Function
def gen_random(uid, pageNumber=1):
    global DIM, TOTAL_NUM_ELEMENTS, HNSW, index_to_uid
    index = randint(0, TOTAL_NUM_ELEMENTS)
    class_label = None

    if uid is None:
        uid = index_to_uid[index]

    if uid not in index_to_uid:
        return False, False

    features = embedding[uid]

    res = []
    k = 20 * pageNumber
    # https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md
    # ef needs to be between k and dataset.size()
    ef = 2 * k
    HNSW.set_ef(ef)
    print(f"Querying {k} docs from [{uid}]")
    labels, distances = HNSW.knn_query(features, k=k)
    srcDoc = None
    for index, dist in zip(labels[0], distances[0]):
        uid = index_to_uid[index]
        if srcDoc is None:
            srcDoc = uid
        res.append({
            'distance': str(dist),
            'uid': uid,
            'url': gen_metadata_from_uid(uid, 'url'),
            'title': gen_metadata_from_uid(uid, 'title'),
            'refURL': get_reference_url(uid),
            'authors': gen_metadata_from_uid(uid, 'authors'),
            'journal': gen_metadata_from_uid(uid, 'journal'),
            'publish_time': gen_metadata_from_uid(uid, 'publish_time'),
            'abstract': gen_metadata_from_uid(uid, 'abstract'),
        })

    return srcDoc, res

def gen_random_diff(uid, pageNumber=1):
    global DIM, TOTAL_NUM_ELEMENTS, HNSW, index_to_uid, diff_keys
    index = randint(0, TOTAL_NUM_ELEMENTS)
    class_label = None

    if uid is None:
        uid = index_to_uid[index]

    if uid not in index_to_uid:
        return False, False

    features = embedding[uid]
    source = {
        'uid': uid,
        'title': gen_metadata_from_uid(uid, 'title'),
        'doi': gen_metadata_from_uid(uid, 'doi'),
    }

    res = []
    k = 100 * pageNumber
    # https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md
    # ef needs to be between k and dataset.size()
    ef = 2 * k
    HNSW.set_ef(ef)
    print(f"Querying {k} docs from [{uid}]")
    labels, distances = HNSW.knn_query(features, k=k)
    for index, dist in zip(labels[0], distances[0]):
        uid = index_to_uid[index]
        if uid not in diff_keys:
            continue

        res.append({
            'distance': str(dist),
            'uid': uid,
            # 'url': gen_metadata_from_uid(uid, 'url'),
            'title': gen_metadata_from_uid(uid, 'title'),
            'doi': gen_metadata_from_uid(uid, 'doi'),
            # 'refURL': get_reference_url(uid),
            # 'authors': gen_metadata_from_uid(uid, 'authors'),
            # 'journal': gen_metadata_from_uid(uid, 'journal'),
            # 'publish_time': gen_metadata_from_uid(uid, 'publish_time'),
            # 'abstract': gen_metadata_from_uid(uid, 'abstract'),
        })

    if len(res) < 100:
        return gen_random_diff(source['uid'], pageNumber+1)

    return source, res[0:100]


def loadHNSW():
    global DIM, TOTAL_NUM_ELEMENTS, HNSW
    print('>> [Loading HNSW] hnswlib indexing')
    HNSW = hnswlib.Index(space='l2', dim=DIM)
    HNSW.load_index(f'./data/cord19-hnsw.bin',
                    max_elements=TOTAL_NUM_ELEMENTS)
    HNSW.set_ef(50)

    print('<< [Loading HNSW] done')


def loadMetadata():
    global diff_keys, metadata, index_to_uid, TOTAL_NUM_ELEMENTS, embedding, DIM

    metadata = helper.loadMetadata()
    embedding, DIM = helper.loadEmbedding()
    index_to_uid = helper.loadIndexToUidFile()
    TOTAL_NUM_ELEMENTS = len(index_to_uid)
    diff_keys = helper.loadKeys("./data/diff_keys.txt")
    print(f'>> [Loading Metadata] Detected {TOTAL_NUM_ELEMENTS} elements')


# Utils Functions
def gen_url_from_uid(uid):
    return gen_metadata_from_uid(uid, 'url')


def gen_title_from_uid(uid):
    return gen_metadata_from_uid(uid, 'title')


def gen_metadata_from_uid(uid, field):
    global metadata

    if uid in metadata:
        item = metadata[uid]
        return item[field]

    return None

def get_reference_url(uid):
    return url_for('serveReact', path=uid, _external=True)
