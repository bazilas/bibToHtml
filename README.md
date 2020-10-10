# Creat an HTML piece of code from bib files with Python

The script loads publications from the bib file *papers.bib*. In addition, the bib file  *meta-papers.bib* includes a short description and addititional links for source code, dataset, video and etc.. The entries on both files should have the same id. Finally, image thumbnails should be provided for each publication. The thumbnails should have the name of the id file.

## Dependencies
To run the code the following Python modules are required: [bibtexparser](https://bibtexparser.readthedocs.io/en/master/) and [dominate](https://pypi.org/project/dominate/).

## Execution
The file *generate_html.py* is executed to produce the html file *papers.html*. The html code from this file can be integrated later in another web-page.

