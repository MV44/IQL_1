import os
import sys


name_dict = {
    'ara': 'Arabic',
    'chn': 'Chinese',
    'eng': 'English',
    'frn': 'French',
    'ger': 'German',
    'hbr': 'Hebrew',
    'jpn': 'Japanese',
    'kkn': 'Korean',
    'pql': 'Polish',
    'rus': 'Russian',
    'spn': 'Spanish',
    'spr': 'Esperanto',
    'swa': 'Swahili',
    'tgl': 'Tagalog',
    'trk': 'Turkish',
    'cln': 'Catalan',
    'grk': 'Greek',
    'dut': 'Dutch',
    'fin': 'Finnish'
}

family_dict = {
    'Arabic': 'Afro-Asiatic',
    'Chinese': 'Sino-Tibetan',
    'English': 'Indo-European',
    'French': 'Indo-European',
    'German': 'Indo-European',
    'Hebrew': 'Afro-Asiatic',
    'Japanese': 'Japonic',
    'Korean': 'Koreanic',
    'Polish': 'Indo-European',
    'Russian': 'Indo-European',
    'Spanish': 'Indo-European',
    'Esperanto': 'Indo-European',
    'Swahili': 'Niger-Congo',
    'Tagalog': 'Austronesian',
    'Turkish': 'Turkic',
    'Catalan': 'Indo-European',
    'Greek': 'Indo-European',
    'Dutch': 'Indo-European',
    'Finnish': 'Uralic'
}


def add_family():
    # add family column to csv files in 'r_results/data' folder as the second column
    # and for each line, add the corresponding family name
    for key, value in family_dict.items():
        try:
            print(f'r_results/data/{key}.csv')
            file = open(f'r_results/data/{key}.csv', 'r', encoding='utf-8')
            lines = file.readlines()
            file.close()
            
            # add family column after the "type" column
            line_0 = lines[0].strip().split(',')
            line_0.insert(2, '"family"')
            lines[0] = ','.join(line_0) + '\n'

            # add family name for each line
            for i in range(1, len(lines)):
                lines[i] = lines[i].strip().split(',')
                lines[i].insert(2, f'"{value}"')
                lines[i] = ','.join(lines[i]) + '\n'

                

            file = open(f'r_results/data/{key}.csv', 'w', encoding='utf-8')
            file.writelines(lines)
            print(f'{key}.csv has been modified.')
            file.close()

        except:
            print(f'{key}.csv does not exist. Skipping...')
            continue



def remove_first_column(path):
    # remove the first column in csv files in 'path' folder
    for key, value in family_dict.items():
        try:
            file = open(f'path/{key}.csv', 'r', encoding='utf-8')
            lines = file.readlines()
            file.close()
            
            # remove the first column
            for i in range(len(lines)):
                lines[i] = lines[i].strip().split(',')
                lines[i] = ','.join(lines[i][1:]) + '\n'

            file = open(f'path/{key}.csv', 'w', encoding='utf-8')
            file.writelines(lines)
            print(f'{key}.csv has been modified.')
            file.close()

        except:
            print(f'{key}.csv does not exist. Skipping...')
            continue

def rename_files():
    # rename the files to full language names in 'processed/csv_to_plot' folder
    for key, value in name_dict.items():
        try:
            os.rename(f'processed/csv_to_plot/{key}.csv', f'processed/csv_to_plot/{value}.csv')
        except:
            print(f'{key}.csv does not exist. Skipping...')
            continue

if __name__ == '__main__':
    # add_family()
    # rename_files()
    remove_first_column(sys.argv[1])
    print("Files renamed!")