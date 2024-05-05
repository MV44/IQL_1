# Quantitative Linguistics Project

This project aims to analyze various aspects of different languages using quantitative linguistics methods.

## Project Structure

- `assets/`: Contains the original, fixed, and converted text files for various languages.
- `processed/`: Contains the tokenized text files and test results.
- `r_results/`: Contains the results from the R data analysis.
- `*.py`: Python scripts for various tasks such as text conversion, preprocessing, tokenizing, and model downloading.

## Key Scripts

- [`converter.py`](converter.py): Converts the pdf files to text files.
- [`preprocess.py`](preprocess.py): Preprocesses the chinese text file.
- [`tokenizer.py`](tokenizer.py): Tokenizes the text files using different models for different languages.
- [`model_download.py`](model_download.py): Downloads the necessary models for tokenization.
- [`rename.py`](rename.py): Renames the files according to a predefined dictionary.

## How to Run

### Before tokenizing

The assets I used where mostly pdf files, so I had to convert them to text files. The txt converted files are stored in the `assets/converted/` directory and are already in this repository. If you want to convert your own files, you can add them to the `assets/original/` directory and run the following command:

```bash
python converter.py
```

note: You will have to modify the other scripts to use the new languages you added, notably the dictionnaries in the scripts that help them to find the good models to use.

To tokenize the text files, you need to download the necessary models for tokenization. To do this, run:

```bash
python model_download.py
```

It is likely that there is an issue with the arabic language because at the time of writing, the arabic model wasn't available for the latest SpaCy version. I fixed this issue by tokenizing all the other languages first and then installed an older version of SpaCy to use the arabic model. 

For the chinese language, there were an issue with the format of the asset text file, the preprocessing script was used to fix this issue.


### Tokenizing

Tokenzation results are csv files stored in the specificied out_folder.

To tokenize all text files in the `assets/fixed/` directory, run:

```bash
python tokenizer.py
```

To tokenize a specific text file, run:

```bash
python tokenizer.py <path_to_text_file> (optional: <new_file_name>)
```

### Data Analysis

The data analysis was done using R. The results are stored in the `r_results/` directory.




