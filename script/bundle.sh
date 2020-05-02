# Download New Dataset
sh script/download.sh

# Index HNSW
python util/index-hnsw.py

# Bundle
NAME=cord19-hnsw
DATE=2020-05-01
FULL=${NAME}-index-${DATE}
TAR=${FULL}.tar.gz

cd data/
rm -rf ${FULL}
rm ${TAR}
mkdir ${FULL}
cp metadata.csv ${FULL}
cp specter.csv ${FULL}
cp ${NAME}.bin ${FULL}
cp ${NAME}.txt ${FULL}
tar -cvzf ${TAR} ${FULL}/

mv ${TAR} ../
