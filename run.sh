conda activate flask
cd src/cac/data/pubs/
git pull
cd -
cd src
python freeze.py -d www
cp -r www/* ../
