# Make data/ Folder
rm -rf data/
mkdir data/
cd data/

# Download metadata.csv
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/metadata.csv

# Download SPECTER embedding
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/cord_19_embeddings_4_24.tar.gz
tar -xvzf cord_19_embeddings_4_24.tar.gz
rm cord_19_embeddings_4_24.tar.gz
mv cord_19_embeddings_4_24.csv specter.csv
