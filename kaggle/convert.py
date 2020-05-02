import glob,json


def convert(path, res):
    related = res['sample']

    with open(path, 'w+') as f:
        for rank, item in enumerate(related):
            uid = item['uid']
            dist = item['distance']
            score = 1/(float(dist) + 1)
            f.write(f"0 Q0 {uid} {rank} {score} tag")
            f.write("\n")



if __name__=='__main__':
    for path in glob.glob('*.json'):
        print('Processing', path)
        res = json.load(open(path, 'r'))
        uid = path[:-5]
        output_path = uid + '.txt'
        convert(output_path, res)
