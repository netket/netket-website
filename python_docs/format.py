import pytablewriter
import parse as pa
import extract as ext
import re
import inspect
import io


def format_class(cl):
    f = io.StringIO("")
    docs = cl[1].__doc__

    # skip undocumented classes
    if(docs == None):
        return f.getvalue()

    # # remove excess spaces
    docs = " ".join(docs.split())

    # General hig-level class docs
    f.write('# ' + cl[0] + '\n')
    f.write(docs + '\n')

    # Docs for __init__
    docs = (cl[1].__init__).__doc__
    clex = ext.PyBindExtract(docs)

    match = clex.extract("__init__")

    if(isinstance(match, list)):
        for ima, ma in enumerate(match):
            f.write(format_function(ma, 'Constructor [' + str(ima + 1) + ']'))
    else:
        f.write(format_function(match, 'Constructor'))

    # properties
    properties = inspect.getmembers(cl[1], lambda o: isinstance(o, property))
    f.write(format_properties(properties))
    return f.getvalue()


def format_function(ma, name):
    f = io.StringIO("")
    f.write('## ' + name)
    value_matrix = []
    signature = ma["signature"]

    gds = pa.GoogleDocString(ma["docstring"]).parse()

    sigp = pa.parse_signature(signature)

    has_example = False
    for gd in gds:
        if(gd['header'] == 'Args'):
            for arg in gd['args']:
                field = arg['field']

                # # remove excess spaces
                descr = " ".join(arg['description'].split())

                sig = sigp[field]
                value_matrix.append([arg['field'], sig, descr])
        elif(gd['header'].startswith("Example")):
            examples = (gd['text'])
            has_example = True
        else:
            f.write(gd['text'] + '\n')

    writer = pytablewriter.MarkdownTableWriter()
    writer.header_list = ["Field", "Type", "Description"]
    writer.value_matrix = value_matrix
    writer.stream = f
    writer.write_table()
    if(has_example):
        f.write('### Examples' + '\n')
        f.write(examples + '\n')
    return f.getvalue()


def format_properties(properties):
    writer = pytablewriter.MarkdownTableWriter()
    value_matrix = []

    for prop in properties:
        docs = prop[1].__doc__
        semic = docs.find(":")
        type_name = ''
        if(semic != -1):
            type_name = docs[: semic]
            docs = docs[semic + 1:]

        value_matrix.append([prop[0], type_name, docs])

    f = io.StringIO("")
    writer.header_list = ["Property", "Type", "Description"]
    writer.value_matrix = value_matrix
    writer.stream = f

    f.write('## Properties' + '\n')
    writer.write_table()
    return f.getvalue()
