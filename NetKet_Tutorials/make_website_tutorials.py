import nbformat as nbf
from nbconvert.exporters import MarkdownExporter
from IPython.display import Image
import os
import sys

md_exporter = MarkdownExporter()

if(len(sys.argv) != 2):
    print("Insert filename.ipynb to be converted")
    exit()
filename = str(sys.argv[1])

base_name = os.path.splitext(filename)[0].lower()

nb = nbf.read(filename, as_version=4)


(body, resources) = md_exporter.from_notebook_node(nb)

# save markdown
with open(base_name + '.md', 'w') as file:
    file.write(body)

# save images
for resource in resources['outputs'].keys():
    file_res = base_name + '_' + resource
    body.replace(resource, '/tutorials/img/' + file_res)
    with open(file_res, 'wb') as file:
        file.write(resources['outputs'][resource])
