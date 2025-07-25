
# Installation:
sudo apt update
sudo apt install -y antiword tesseract-ocr
source /home/kamal/Documents/venvs/bin/activate
pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
python3 -m nltk.downloader punkt stopwords

pip list
antiword -v
tesseract --version

