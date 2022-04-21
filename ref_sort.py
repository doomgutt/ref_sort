def main():
    file_dir = 'src_test_and_extras/test_pile/'
    file_name = 'Mediano 2021'
    output_dir = '/home/doomgutt/.obsidian/new_ref_dump/'

    refs = extract_refs(file_dir + file_name)
    write_refs(refs, output_dir)


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