import os
from pathlib import Path


def write_web_doc(folder_name, file_name):
    file_head = os.path.splitext(file_name)[0]

    header = "---\n"
    title = file_head
    permalink = "/docs/" + folder_name + "_" + file_head + '/'

    header += "title: " + title + "\n"
    header += "permalink: " + permalink + "\n"
    header += "---\n"

    outdir = '../_docs/'

    fileout = outdir + '/' + folder_name + "_" + file_name
    with open(fileout, 'w') as fout:
        fout.write(header)
        with open(folder_name + "/" + file_name, 'r') as f:
            fout.write(str(f.read()))


folders = (next(os.walk('.'))[1])

for folder in folders:
    if(folder.startswith('__')):
        continue
    sub_files = (next(os.walk(folder))[2])
    for sub_file in sub_files:
        write_web_doc(folder, sub_file)
