from pathlib import Path

ROOT_DIR = Path('.')

EXPECTED_N = None
PREFIX  = None
POSTFIX = None

def main():
    clean_all()

def clean_all():
    bib_dir = ROOT_DIR / 'clean_anystyle_bibs'
    for bib_file in bib_dir.glob('*.md'):
        with bib_file.open('r+') as f:
            count_entries(f)
            attempts = 5
            for _ in range(attempts):
                clean_up(f)

def clean_up(f):
    """remove a round of line breaks"""
    f.seek(0)
    lines = f.readlines()
    items = find_items(lines)
    items = check_items(items)
    lines = clean_line_breaks(lines, items)
    f.seek(0)
    f.writelines(lines)
    f.truncate()

def clean_line_breaks(lines, items):
    """ remove line breaks"""
    for n in items:
        lines[n] = lines[n].replace("\n", "")
    return lines

def check_items(items):
    """remove completed items"""
    remove_list = []
    for i,j in zip(items[:-1], items[1:]):
        if j-i == 1:
            remove_list.append(i)
    new_items = [x for x in items if x not in remove_list]
    return new_items

def find_items(lines):
    """find the lines on which the items begin"""
    check_str = make_check_str()
    item_lines = []
    c = 0
    for n, line in enumerate(lines):
        if line[:len(check_str[c])] == check_str[c]:
            item_lines.append(n)
            if c < EXPECTED_N-1:
                c += 1
    return item_lines

def make_check_str():
    """make a list of strings to look for at starts of lines"""
    itemize = list(range(1, EXPECTED_N+1))
    for i, num in enumerate(itemize):
        itemize[i] = PREFIX + str(num) + POSTFIX
    return itemize

def prefix_postfix(lines):
    """determine brackets for enumeration"""
    global PREFIX, POSTFIX
    one = lines[0].split()[0]
    pref_post = one.replace('1', ' ').split()
    if len(pref_post) == 1:
        pref_post = [''] + pref_post
    elif len(pref_post) == 0:
        pref_post = ['', '']
    PREFIX = pref_post[0]
    POSTFIX = pref_post[1]

def count_entries(f):
    """try to count number of entries"""
    global EXPECTED_N
    lines = f.readlines()
    prefix_postfix(lines)
    
    c = 1
    for line in lines:
        check_char = PREFIX + str(c) + POSTFIX + ' '
        if line[:len(check_char)] == check_char:
            c += 1

    EXPECTED_N = c-1

if __name__ == '__main__':
    main()