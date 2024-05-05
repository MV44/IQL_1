import sys

import spacy
import re


converted_file = 'assets/converted/txt/chn.txt'
preprocessed_file = 'assets/preprocessed/chn.txt'

# remove the useless spaces introduced by the conversion from pdf to text & place the new file the preprocessed folder
def zh_preprocess_text_file():
    with open(converted_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        new_lines = []
        for line in lines:
            new_line = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', line)
            new_lines.append(new_line)
    with open(preprocessed_file, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# 


if __name__ == '__main__':
    if sys.argv[1] == 'zh':
        zh_preprocess_text_file()
