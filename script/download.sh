# Make data/ Folder
rm -rf data/
mkdir data/
cd data/

# Download metadata.csv
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/metadata.csv &

# Download SPECTER embedding
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/cord_19_embeddings_5_1.tar.gz -O cord_19_embeddings.tar.gz

# untar SPECTER embedding
mkdir temp/
tar -xvzf cord_19_embeddings.tar.gz -C temp/
mv temp/cord_19_embeddings*.csv specter.csv
