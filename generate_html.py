import dominate
from dominate.tags import *
import bibtexparser
import os

# Load the bib file with the papers
with open('papers.bib') as bibtex_file:
    bib_papers = bibtexparser.load(bibtex_file)

# Load the meta-data bib file with description, project page and etc.
with open('meta-papers.bib') as bibtex_file:
    meta_papers = bibtexparser.load(bibtex_file)

# image source (local / webfolder, should exist prior to execution) - image files are jpg
img_root = 'imgs/'

# bib file export folder (should exist prior to execution)
bib_export_fld = 'bib_files/'

doc = dominate.document(title='Papers')

with doc.head:
    link(rel='stylesheet', href='style.css')
    style("""\
         body {
             background-color: #F5F5F5;
             color: #2F4F4F;
             font-family: Arial;
             font-size: 0.9em;
             margin: 2em 2em;
         }
     """)

with doc:
    with div(cls='container'):
        with table(id='main', cls='table table-striped'):
            with tbody():
                for bib, meta_data in zip(bib_papers.entries, meta_papers.entries):
                    with tr(style="height: 15px;"):
                        with td(style="width: 165px; height: 15px;"):

                            # Path for the thumbnail image (stored as jpg). The thumbnail name should be the bib entry id.
                            # use lexis.jpg if there is not available thumbnail
                            img_path = img_root + bib['ID'] + '.jpg'
                            if not os.path.exists(img_path):
                                img_path = img_root + 'lexis.jpg'
                            div(img(src=img_path, width="160", height="160", style="display: block; margin-left: auto; margin-right: auto;"), _class='photo')

                        with td(style="width: 390px; height: 15px;"):
                            # Authors, Title, Conference / Journal, Year
                            if "booktitle" in bib:
                                p('%s, <b>%s</b>, %s, %s.' % (bib['author'].replace(' and', ','), bib['title'], bib['booktitle'].replace('\&', '&'), bib['year']))
                            else:
                                p('%s, <b>%s</b>, %s, %s.' % (bib['author'].replace(' and', ','), bib['title'], bib['journal'].replace('\&', '&'), bib['year']))
                            
                            # Short Description
                            if 'note' in meta_data and meta_data['note']:
                                p('TLDR: %s' % meta_data['note'])

                            # Extra Links (if available and not empty)
                            def check_field(field_name, current_dict):
                                if field_name in current_dict and current_dict[field_name]:
                                    return True
                            
                            list_of_links = ['preprint', 'publication', 'project', 'code', 'data', 'video', 'bib']
                            list_of_labels = ['Pre-print', 'Publication', 'Project', 'Code', 'Data', 'Video'] 

                            for li, la in zip(list_of_links,list_of_labels):
                                if check_field(li, meta_data):
                                    a(la, href=meta_data[li], target="_blank", rel="noopener")

                            # export invdividual bib files
                            bib_export = bibtexparser.bwriter.BibTexWriter()
                            bib_path = bib_export_fld + bib['ID'] + '.bib'

                            with open(bib_path, 'w') as bibfile:
                                db = bibtexparser.bibdatabase .BibDatabase()
                                db.entries = [bib]
                                bibtexparser.dumps(db)
                                bibfile.write(bib_export.write(db))

                            #add link to the webpage
                            a('Bib File', href=bib_path, target="_blank", rel="noopener")

with open('papers.html', 'wb') as file:
        file.write(doc.render(pretty=True).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>').encode())