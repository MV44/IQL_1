import os
import sys

import spacy
import spacy.lang.zh
import spacy_transformers

from model_download import downloaded_models
from model_download import matching_dict


out_folder = 'processed/tokenized'
out_test_folder = 'processed/test'


def tokenize_text(text_file, nlp):
    # Open the text file
    txt = open(f'{text_file}', 'r', encoding='utf-8')
    text = txt.read()
    txt.close()

    # Tokenize the text
    doc = nlp(text)

    tokens = {}

    # Iterate through all tokens
    for token in doc:
        if token.is_alpha:
            # Convert the token to lowercase if it starts with a capital letter
            if token.text[0].isupper() and not token.pos_ == 'PROPN':
                token_text = token.text.lower()
            else:
                token_text = token.text

            if tokens.get(token_text):
                tokens[token_text] += 1
            else:
                tokens[token_text] = 1
    # Return the list of tokens
    return tokens

# Replace with your actual folder path (use backslashes)
text_files = os.listdir('assets/fixed')

def order_prepare_tokens(tokens):
    ordered_prepared_tokens = []
    for token, count in tokens.items():
        ordered_prepared_tokens.append([token, count])
    ordered_prepared_tokens.sort(key=lambda x: x[1], reverse=True)
    for token in ordered_prepared_tokens:
        token.append(len(token[0]))
    return ordered_prepared_tokens

# Tokenize a text file
def tokenize_text_file(text_file, res_file, nlp):
    print("nlp used: ", nlp)


    tokens = tokenize_text(text_file, nlp)
    ordered_prepared_tokens = order_prepare_tokens(tokens)
    file_name = res_file.split('/')[-1]
    out_file = open(f'{out_folder}/{file_name.replace(".txt", ".csv")}', 'w', encoding='utf-8')
    out_file.write("type count length\n")
    for token in ordered_prepared_tokens:
        out_file.write(f'{token[0]} {token[1]} {token[2]}\n')
    out_file.close()

# Iterate through all text files, tokenizer them and output the token list in the out_folder
def tokenize_text_files():
    for text_file in text_files:
        if os.path.exists(f'{out_folder}/{text_file.replace(".txt", ".csv")}'):
            print(f'{text_file} is already tokenized. Skipping...')
            continue
        print(f'Tokenizing {text_file}...')

        # chinese model with jieba as segmenter (word tokenizer)
        if text_file == "chn.txt":
            cfg = {"segmenter": "jieba"}
            nlp = spacy.lang.zh.Chinese().from_config({"nlp": {"tokenizer": cfg}})
            
        # mdeium non official turkish model
        elif text_file == "trk.txt":
            nlp = spacy.load(f'{matching_dict[text_file[:3]]}_core_news_md')

        # model for arabic
        elif text_file == "ara.txt":
            nlp = spacy.blank('ar')
            cfg = {
                "model": {
                    "@architectures": "spacy-transformers.TransformerModel.v3",
                    "name": "aubmindlab/bert-base-arabertv02"
                }
            }
            nlp.add_pipe("transformer", config=cfg)
            nlp.initialize()


        # all other languages
        else:
            try:
                nlp = spacy.load(f'{matching_dict[text_file[:3]]}_core_web_sm')
            except:
                nlp = spacy.load(f'{matching_dict[text_file[:3]]}_core_news_sm')

        tokenize_text_file(f'assets/fixed/{text_file}', f'{out_folder}/{text_file}', nlp)



# download_models()
# download_models()

# Tokenize all text files

if __name__ == '__main__':
    print("Tokenizing...")
    if len(sys.argv) == 1:
        print('Tokenizing all text files...')
        tokenize_text_files()
    elif len(sys.argv) == 3:
        print(f'Tokenizing {sys.argv[1]} into {sys.argv[2]}...')
        tokenize_text_file(sys.argv[1], sys.argv[2], nlp)
    elif len(sys.argv) == 2: 
        print(f'Tokenizing {sys.argv[1]}...')
        tokenize_text_file(sys.argv[1], sys.argv[1], "en_core_web_sm")




