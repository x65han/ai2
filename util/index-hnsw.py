# Constants
DATA_FOLDER = './data/'
METADATA_PATH = path.join(DATA_FOLDER, 'metadata.csv')
SPECTER_PATH = path.join(DATA_FOLDER, 'specter.csv')

# TOTAL_NUM_ELEMENTS = 0
# ELEMENTS = []
# HNSW = None
# PROCESSED = []

def initializeIndex():
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW, PROCESSED

    # Declaring index
    # possible options are l2, cosine or ip
    HNSW = hnswlib.Index(space='l2', dim=DIM)

    # Initing index - the maximum number of elements should be known beforehand
    # For more configuration, see: https://github.com/nmslib/hnswlib/blob/master/ALGO_PARAMS.md
    HNSW.init_index(max_elements=TOTAL_NUM_ELEMENTS, ef_construction=200, M=16)


def addAndSaveIndex(data, data_labels, index):
    print('>> [Pre-process] hnswlib indexing', index)
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW
    # Element insertion (can be called several times):
    HNSW.add_items(data, data_labels)
    # Save Phase 1
    output_path = f'./bin/{index}.bin'
    removeIfExist(output_path)
    HNSW.save_index(output_path)
    # Save Phase 2
    output_path = f'./bin/{index}.txt'
    removeIfExist(output_path)
    output = open(output_path, "w")
    for i in PROCESSED:
        output.write(i + '\n')
    output.close()


def main(loadFromIndex=None):
    global DIM, PATH, TOTAL_NUM_ELEMENTS, ELEMENTS, HNSW, PROCESSED
    print('>> [Pre-process] starting')
    data = np.empty((0, DIM))
    data_labels = []

    inputfile = open(PATH, 'r')
    ELEMENTS = ['img/'+p.strip() for p in inputfile.readlines()]
    TOTAL_NUM_ELEMENTS = len(ELEMENTS)
    print(f'>> [Pre-process] Detected {TOTAL_NUM_ELEMENTS} elements')

    initializeIndex()
    if loadFromIndex is not None:
        loadIndex(loadFromIndex)
    else:
        print("Fresh Start")

    for index, path in enumerate(ELEMENTS):
        if loadFromIndex is not None and index < loadFromIndex:
            continue

        if index % 10000 == 0:
            print(f'>> [Pre-process][{index}/{TOTAL_NUM_ELEMENTS}]')

        if index % 10000 == 0 and len(data_labels) > 0:
            # save progress
            addAndSaveIndex(data, data_labels, index)
            # reset
            data = np.empty((0, DIM))
            data_labels = []

        current_vector = extract_features_by_path(path)
        prediction = predict_by_path(path)
        data = np.concatenate((data, current_vector))
        data_labels.append(index)
        PROCESSED.append(path[4:])  # remove "img/" prefix

    if len(data_labels) > 0:
        addAndSaveIndex(data, data_labels, index)

    print('<< [Pre-process] done')


if __name__ == '__main__':
    main()
