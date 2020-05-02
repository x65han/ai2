sudo add-apt-repository universe
sudo apt update
sudo apt install python-pip -y
sudo apt install python3-pip -y
apt-get install -y python-setuptools python-pip
pip3 install pybind11 numpy setuptools
pip3 install -r requirements.txt

git clone https://github.com/x65han/ai2.git
cd ai2
./download.sh &
