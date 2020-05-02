import hnswlib
import numpy as np
import helper

# Constants
metadata = {}
embedding = {}
HNSW = None
DIM = None
TOTAL_NUM_ELEMENTS = None


# Utils
def loadData():
    global metadata, embedding, DIM, TOTAL_NUM_ELEMENTS
    metadata = helper.loadMetadata()
    print('Metadata Length:', len(metadata))
    embedding, DIM = helper.loadEmbedding()
    print('Number of Embedding:', len(embedding))
    print('Embedding Dimension:', DIM)

    assert len(metadata) == len(embedding), "Data Size Mismatch"
    TOTAL_NUM_ELEMENTS = len(metadata)
    print('Total Elements:', TOTAL_NUM_ELEMENTS)


def initializeIndex():
    global HNSW, DIM

    # Declaring index
    # possible options are l2, cosine or ip
    HNSW = hnswlib.Index(space='l2', dim=DIM)

    # Initing index - the maximum number of elements should be known beforehand
    # For more configuration, see: https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md
    HNSW.init_index(max_elements=TOTAL_NUM_ELEMENTS, ef_construction=200, M=16)


def addAndSaveIndex(data, data_labels, index_to_uid, index, save=False):
    print('>> [Pre-process] adding hnswlib index', index)
    global DIM, TOTAL_NUM_ELEMENTS, HNSW
    # Element insertion (can be called several times):
    HNSW.add_items(data, data_labels)
    # Save index bin file
    if save is True:
        print('>> [Pre-process] saving hnswlib index', index)
        final_path = './data/cord19-hnsw'
        output_path =f'{final_path}.bin'
        helper.removeIfExist(output_path)
        HNSW.save_index(output_path)
        # Save index to uid file
        helper.saveIndexToUidFile(index_to_uid, index, f'{final_path}.txt')


# Main Function
def main(loadFromIndex=None):
    global DIM, TOTAL_NUM_ELEMENTS, HNSW
    print('>> [Pre-process] starting')
    data = np.empty((0, DIM))
    data_labels = []
    index_to_uid = []

    for index, uid in enumerate(embedding):
        if index % 100 == 0:
            print(f'>> [Pre-process][{index}/{TOTAL_NUM_ELEMENTS}]')

        if index % 1000 == 0 and len(data_labels) > 0:
            # save progress
            addAndSaveIndex(data, data_labels, index_to_uid, index)
            # reset
            data = np.empty((0, DIM))
            data_labels = []

        vector = embedding[uid]
        assert len(vector) == DIM, "Vector Dimension Mismatch"
        data = np.concatenate((data, [vector]))
        data_labels.append(index)
        index_to_uid.append(uid)

    if len(data_labels) > 0:
        addAndSaveIndex(data, data_labels, index_to_uid, index, save=True)
        print(f'>> [Pre-process][{index}/{TOTAL_NUM_ELEMENTS}]')

    print('<< [Pre-process] done')


# Trigger
if __name__ == '__main__':
    loadData()
    initializeIndex()
    main()
