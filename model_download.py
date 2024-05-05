import spacy
import os

matching_dict = {
    'chn': 'zh',
    'eng': 'en',
    'frn': 'fr',
    'ger': 'de',
    'hbr': '',
    'jpn': 'ja',
    'kkn': 'ko',
    'pql': 'pl',
    'rus': 'ru',
    'skt': '',
    'spn': 'es',
    # for es we use the same model as spanish, since esperanto is not supported and close to spanish
    'spr': 'es',
    # for swa and tgl we use the same model as english, since swahili and tagalog are not supported, 
    # but the language structure is only composed by entire words
    'swa': 'en',
    'tgl': 'en',
    'trk': 'tr',
    'cln': 'ca',
    'grk': 'el',
    'dut': 'nl',
    'fin': 'fi'
}

def download_models():
    for lang in matching_dict.values():
        if f'{lang}_core_web_sm' in spacy.util.get_installed_models() or f'{lang}_core_news_sm' in spacy.util.get_installed_models():
            print(f'{lang} model is already downloaded. Skipping...')
            continue
        elif lang == '':
            continue

        # skip chinese model because we use jieba
        if lang == 'zh':
            print(f'{lang} model is already downloaded. Skipping...')
            continue
        elif lang == 'tr':
            print(f'Downloading {lang}...')
            os.system('pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_md/resolve/main/tr_core_news_md-any-py3-none-any.whl')
        else:    
            print(f'Downloading {lang}...')
            os.system(f'python -m spacy download {lang}_core_web_sm')
            os.system(f'python -m spacy download {lang}_core_news_sm')


# models downloaded
dl_models = ['en', 'zh', 'fr', 'de', 'pl', 'ru', 'es', 'ca', 'el', 'nl']

# create a list called downloaded_model
downloaded_models = [key for key, value in matching_dict.items() if value in dl_models]

if __name__ == '__main__':
    download_models()
    print("Download complete!")

