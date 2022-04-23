from pathlib import Path

ROOT_DIR = Path('./clean_bib_items/')
FILENAME = 'dirty.md'
OUTPUT_FILENAME = 'clean.md'

filepath = ROOT_DIR / FILENAME
output_filepath = ROOT_DIR / OUTPUT_FILENAME

EXPECTED_N = 63
PREFIX  = ''
POSTFIX = '. '

def main():
    with filepath.open('r+') as f:
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

    # for item in new_items

def make_check_str():
    """make a list of strings to look for at starts of lines"""
    itemize = list(range(1, EXPECTED_N+1))
    for i, num in enumerate(itemize):
        itemize[i] = PREFIX + str(num) + POSTFIX
    return itemize

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

if __name__ == '__main__':
    main()