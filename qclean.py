from pathlib import Path

def main():
    texts = Path('./texts')
    folders = [x for x in texts.iterdir() if x.is_dir()]
    for folder in folders:
        for ris_file in folder.glob('*.ris'):
            clean(ris_file)

def clean(ris_file):
    if   ris_file.name[:9]  == 'articles-':
        ref_self(ris_file)
        ris_file.rename(ris_file.parent / 'self.ris')
    elif ris_file.name[:11] == 'references-':
        refs(ris_file)
        ris_file.rename(ris_file.parent / 'refs.ris')
    elif ris_file.name[:10] == 'citations-':
        cits(ris_file)
        ris_file.rename(ris_file.parent / 'cits.ris')

def ref_self(ris_file):
    with ris_file.open('r+') as rf:
        lines = rf.readlines()
        remove = ['"1" "\n', '\n', '"\n']
        new_lines = [l for l in lines if l not in remove]
        rf.seek(0)
        rf.writelines(new_lines)
        rf.truncate()

def refs(ris_file):
    with ris_file.open('r+') as rf:
        lines = rf.readlines()
        remove = ['"1" "\n', 'ER  - "\n']
        new_lines = [l for l in lines if l not in remove]
        new_lines.append('ER  - ')
        rf.seek(0)
        rf.writelines(new_lines)
        rf.truncate()

def cits(ris_file):
    with ris_file.open('r+') as rf:
        lines = rf.readlines()
        remove = ['"1" "\n', 'ER  - "\n']
        new_lines = [l for l in lines if l not in remove]
        new_lines.append('ER  - ')
        rf.seek(0)
        rf.writelines(new_lines)
        rf.truncate()

if __name__ == ('__main__'):
    main()
