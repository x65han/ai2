import glob,csv

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

def process(path, metadata):
    uids = []

    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            tokens = line.split(' ')
            uids.append(tokens[2])

    print(uids)
    
    output_path = path[:-4] + '.txt'
    with open(output_path, 'w+') as f:
        for uid in uids:
            title = metadata[uid]['title']
            doi = metadata[uid]['doi']
            f.write(f"title: {title}\n")
            f.write(f"UID: {uid}\n")
            f.write(f"doi: {doi}\n")
            f.write('\n')
            f.write('\n')


if __name__=='__main__':
    metadata = loadMetadata('../data/metadata.csv')
    for path in glob.glob('*.out'):
        process(path, metadata)