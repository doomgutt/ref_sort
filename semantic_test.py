import s2

author = s2.api.get_author(authorId="144794037")

paperIds = [p.paperId for p in author.papers]
papers = []
for pid in paperIds:
    paper = s2.api.get_paper(
        paperId=pid,
        retries=2,
        wait=150,
        params=dict(include_unknown_references=True)
    )
    papers += [paper]
    print(paper.title)

n_citations = sorted([len(p.citations) for p in papers], reverse=True)
for n_papers, n_cited in enumerate(n_citations):
    if n_cited < n_papers:
        h_index = n_papers - 1
        break

print(h_index)