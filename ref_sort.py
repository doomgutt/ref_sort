from pathlib import Path

ROOT_DIR = Path('.')
REF_SORT_TAG = '#---ref-sort---------------------'
# === === === === ===
CUSTOM_OUTPUT = Path('/home/doomgutt/.obsidian/Personal/phd/texts/')



def main():
    ref_sort()

# ----------------------------------------------------------
def ref_sort():
    """ref_sort"""
    bib_dir = ROOT_DIR / 'bibs'
    output_dir = CUSTOM_OUTPUT
    # output_dir = ROOT_DIR / 'output'
    for bib_file in bib_dir.glob('*.bib'):
        entries = bib_entries(bib_file)
        make_ref_files(entries, output_dir)


# writing entries ------------------------------------------
def make_ref_files(entries, output_dir):
    for entry in entries:
        fname = entry['filename'] + '.md'
        filepath = output_dir / fname

        # if self=true make bilbiography
        bibliography = None
        if entry['self']:
            bibliography = make_bibliography(entries)

        # if there is a file, look for it
        if filepath.exists() and filepath.is_file():
            with filepath.open('r+') as f:
                
                # check if ref_sort already altered the file
                pos = check_ref_sort(f)
                if pos == None:
                    f.seek(0, 2)
                    f.write(write_ref(entry, bibliography))
                    f.truncate()
                else:
                    # ask permission to rewrite
                    answer = input(f"Rewrite ref_sort data for: \n{entry['filename']}?\n y/n? ")
                    if answer.lower() in ["y","yes"]:
                        f.seek(pos)
                        f.write(write_ref(entry, bibliography))
                        f.truncate()
        # make new file if no file
        else:
            with filepath.open('w') as f:
                f.write(write_ref(entry, bibliography))


def check_ref_sort(open_file):
    """checks whether ref_sort altered the document"""
    lines = open_file.readlines()
    pos = 0
    for line in lines:
        if REF_SORT_TAG in line:
            return pos
        pos += len(line)
    return None

def write_ref(entry, bibliography=None):
    """Makes the string to write"""

    w_str = REF_SORT_TAG + '\n'
    w_str += '## ' + entry['title']
    w_str += '\n\n\n\n\n\n\n'
    w_str += '##### Metadata\n\n'
    for author in entry['author']:
        w_str += f"[[phd/authors/{author}]]\n"
    w_str += f"\n[[phd/publishers/{entry['publisher']}]]\n\n"
    w_str += f"#date_{entry['date']}\n"
    w_str += f"#text_{entry['type']}\n"

    if bibliography is not None:
        w_str += '\n\n\n'
        w_str += '##### Bibliography\n\n'
        for item in bibliography:
            w_str += f"[[{item}]]\n"
    return w_str

def make_bibliography(entries):
    """makes bibliography from entries"""
    bibliography = []
    for entry in entries:
        bibliography.append(entry['filename'])
    return bibliography

    
# getting entries ------------------------------------------
def bib_entries(bib_file):
    """returns a list of dictionary bib entries"""
    entries = []
    with bib_file.open() as f:
        f_lines = f.readlines()
        for line_n in find_entries(f_lines):
            dict_entry = entry_to_dict(determine_entry(f_lines, line_n))
            dict_entry['filename'] = make_filename(dict_entry)
            entries.append(dict_entry)
    return entries

# organising entries ---------------------------------------
def entry_to_dict(entry):
    """turns the list of strings into a dictionary"""
    entry_dict = {
        'filename'  : '',
        'id'        : '',
        'type'      : '',
        'title'     : '',
        'author'    : '',
        'date'      : '',
        'publisher' : '',
        'self'      : False}
    for line in entry:
        checkline = line.replace(' ', '').lower()
        if checkline[0] == '@':
            br = line.find('{')
            entry_dict['type'] = line[1:br]
            entry_dict['id'] = line[br+1:-2]
        if 'title=' in checkline:
            entry_dict['title'] = get_brackets(line)
        if 'author=' in checkline:
            author_string = get_brackets(line).split(' and ')
            entry_dict['author'] = author_string
        if any(x in checkline for x in ['date=', 'year=']):
            entry_dict['date'] = get_brackets(line)
        if any(x in checkline for x in ['publisher=', 'journal=']):
            entry_dict['publisher'] = get_brackets(line)
        if 'self=true' in checkline:
            entry_dict['self'] = True

    return entry_dict

def get_brackets(line):
    """returns only the string within curly bracers"""
    bounds = [1, 0]
    bounds[0] += line.find('{')
    bounds[1] += line.find('}')
    return line[bounds[0]:bounds[1]]

def make_filename(entry):
    """ make filename in format 'author (date) - title'"""
    
    # author
    et_al = ''
    authors = entry['author']
    if len(authors) == 0 or authors[0] == '':
        authors = ['???, ???']
    elif len(authors) > 1:
        et_al = 'et al. '    
    
    # get last name of first author
    author = authors[0].split()[0].replace(',', '') + ' ' + et_al

    # title and date
    title = entry['title'].replace(':', ',')
    date = f"({entry['date']}) - "

    filename = author + date + title
    return filename


# finding entries ------------------------------------------
def determine_entry(lines, line_n):
    """uses @ and {} to determine and return a bib entry"""
    bracket_counter = 0
    temp = []
    for i in range(1000):
        line = lines[line_n+i].strip('\n')
        temp.append(line)
        bracket_counter += line.count('{') - line.count('}')
        if bracket_counter == 0:
            return temp
    
    assert bracket_counter == 0, "mismatched brackets"
    return None

def find_entries(lines):
    """finds bib entries using @"""
    entry_lines = []
    for n, line in enumerate(lines):
        if line[0] == "@":
            entry_lines.append(n)
    return entry_lines

# ------------------------------------------------
if __name__ == "__main__":
    main()