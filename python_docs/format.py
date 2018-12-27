import pytablewriter
import inspect
import parse as pa
import extract as ext
import re


def format_class(cl):

    writer = pytablewriter.MarkdownTableWriter()

    docs = cl[1].__doc__

    # skip undocumented classes
    if(docs == None):
        return False

    docs = re.sub(' +', ' ', str(docs)).strip()

    # General hig-level class docs
    print('# ', cl[0])
    print(docs)

    # Docs for __init__
    docs = inspect.getdoc(cl[1].__init__)
    docs = inspect.cleandoc(docs)
    clex = ext.PyBindExtract(docs)

    match = clex.extract("__init__")

    for ima, ma in enumerate(match):
        print('## ', cl[0], 'constructor [' + str(ima + 1) + ']')
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
                print(gd['text'], '\n')

        writer.header_list = ["Field", "Type", "Description"]
        writer.value_matrix = value_matrix
        writer.write_table()
        if(has_example):
            print('### Examples')
            print(examples, '\n')
    return True


def format_function(func):
    writer = pytablewriter.MarkdownTableWriter()
    value_matrix = []

    docs = inspect.getdoc(func[1])
    docs = inspect.cleandoc(docs)
    clex = ext.PyBindExtract(docs)
    match = clex.extract(func[0])
    print(match)
    # value_matrix.append([prop[0], type_name, docs])

    # writer.header_list = ["Property", "Type", "Description"]
    # writer.value_matrix = value_matrix
    # writer.write_table()


def format_properties(properties):
    writer = pytablewriter.MarkdownTableWriter()
    value_matrix = []

    for prop in properties:
        docs = inspect.getdoc(prop[1])
        docs = inspect.cleandoc(docs)
        semic = docs.find(":")
        type_name = ''
        if(semic != -1):
            type_name = docs[: semic]
            docs = docs[semic + 1:]

        value_matrix.append([prop[0], type_name, docs])

    writer.header_list = ["Property", "Type", "Description"]
    writer.value_matrix = value_matrix
    print('## Properties')
    writer.write_table()
