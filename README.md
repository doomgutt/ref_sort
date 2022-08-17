## Intention

I was thinking it would be interesting to be able to pull references from bibliography of a paper and create maps out of them. The idea has sort of been implemented by [ResearchRabbit](https://www.researchrabbit.ai/) and [Connected Papers](https://www.connectedpapers.com/), but I felt it wasn't quite what I was looking for.

For most papers it seems that [citationchaser](https://estech.shinyapps.io/citationchaser/) does the job of pulling the information. For papers on arXiv and things that are harder to reach I use [Anystyle](https://anystyle.io) or [Cermine](http://cermine.ceon.pl/i).

I transform these into markdown files to use with [Obsidian](https://obsidian.md) as I build up my collection of references.

Citationchaser already offers a network view, but it is only on the web, doesn't include all papers and I prefer to have notes in my nodes as well as the reference network.

--------------------
## How to use

texts  
├── paper1_citationchaser  
│  ├── self.ris  
│  ├── refs.ris  
│  └── cits.ris  
└── paper2_anystyle  
   ├── self.bib  
   └── refs.bib  

In the texts folder, make a folder for each bibliography item you want to use/include.

 - 'self' file contains bib info about the text
 - 'refs' file contains references cited in the text
 - 'cits' file containts bib info about texts that cite this text

Each folder should contain at least the 'self' file, and ideally a 'refs' file. If using [citationchaser](https://estech.shinyapps.io/citationchaser/) then you should be able to get the cits file quit easily.

[citationchaser](https://estech.shinyapps.io/citationchaser/) exports with .ris format and [Anystyle](https://anystyle.io) exports with .bib format, but the script should (hopefully) work no matter which formats you put.

There is a script called 'clean_bib_items.py' which takes a copy-pasta of references from a paper and removes extra line breaks so that it can be pasted into anystyle. It only works with enumerated bibliographies for now.


RIS reference
https://en.wikipedia.org/wiki/RIS_(file_format)
