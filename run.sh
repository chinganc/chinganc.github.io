# conda activate flask
cd src/cac/data/pubs/
git pull
cp cv.pdf ../../docs/ching-an-cheng-cv.pdf
cd -
cd src
python freeze.py -d www
cp -r www/* ../
