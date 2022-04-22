from pathlib import Path

ROOT_DIR = Path('.')

def main():
    file_dir = 'src_test_and_extras/test_pile/'
    file_name = 'Mediano 2021'
    output_dir = '/home/doomgutt/.obsidian/new_ref_dump/'

    ref_sort()

# ----------------------------------------------------------
def ref_sort():
    """ asdf"""
    bib_dir = ROOT_DIR / 'bibs'
    output_dir = ROOT_DIR / 'output'
    bib_files = []
    for bib_file in bib_dir.glob('*.bib'):
        entries = bib_entries(bib_file)

        # testing
        print(entries[0]['filename'])

# writing entries ------------------------------------------
def testing_writing(entries, output_dir):
    for entry in entries:
        with entry['filename'].open() as f:
            for x in f:
                x = 'aaa'




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

    filename = author + date + title + '.md'
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
    
    print('mismatched brackets')
    return None

def find_entries(lines):
    """finds bib entries using @"""
    entry_lines = []
    for n, line in enumerate(lines):
        if line[0] == "@":
            entry_lines.append(n)
    return entry_lines



# ==============================


def extract_refs(ref_file):
    # ref dict sample
    refs = []
    ref_d = {'title'     : '',
             'authors'   : [],
             'date'      : '',
             'publisher' : ''}

    # read refs
    with open(ref_file, 'r') as f:
        for n, line in enumerate(f):

            # new entry
            t_str = 'Title:'
            if line[:len(t_str)] == t_str:
                refs.append(ref_d.copy())
                refs[-1]['authors'] = []
                refs[-1]['title'] = line[len(t_str)+1:].rstrip('\n')
            
            # authors
            a_str = 'Author:'
            if line[:len(a_str)] == a_str:
                refs[-1]['authors'].append(line[len(a_str)+1:].rstrip('\n'))

            # date
            d_str = 'Publication date:'
            if line[:len(d_str)] == d_str:
                refs[-1]['date'] = line[len(d_str)+1:].rstrip('\n')
            
            # publisher
            p_str = 'Journal title:'
            if line[:len(p_str)] == p_str:
                refs[-1]['publisher'] = line[len(p_str)+1:].rstrip('\n')
    
    # print test 
    if False:
        for x in refs:
            print(f"title    : {x['title']}")
            print(f"date     : {x['date']}")
            print(f"publisher: {x['publisher']}")
            for y in x['authors']:
                print(f"author   : {y}")
            print()

    return refs

def write_refs(references, output_dir):
    # write references
    for ref in references:
        # make title
        author_str = ref['authors'][0].split()
        author_str.sort(key=len, reverse=True)
        author_str = author_str[0].rstrip(',.') + ' '
        # print(author_str)
        date_str = f"({ref['date']}) - "
        et_al = ('et al. ' if len(ref['authors']) > 1 else '')
        title = author_str + et_al + date_str + ref['title']

        # add info
        with open(output_dir + title + '.md', 'w') as f:
            write_str = f"# {ref['title']}\n\n\n\n\n\n\n\n"
            write_str += f"[[date:{ref['date']}]]\n"
            for author in ref['authors']:
                write_str += f"[[author:{author}]]\n"
            write_str += f"[[publishery:{ref['publisher']}]]\n"

            f.write(write_str)
    
    # add file with all references
    with open(output_dir + '---original_paper---' + '.md', 'w') as f:
        write_str = '# ___\n\n\n[[date:]]\n[[author:]]\n[[publisher:]]\n\n\n\n\n\n\n\n### References\n'
        for ref in references:
            write_str += '- [[' + ref['title'] + ']]\n'
        f.write(write_str)



if __name__ == "__main__":
    main()