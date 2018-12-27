import netket as nk
import format
import inspect


classes = inspect.getmembers(nk.graph, inspect.isclass)

for cl in classes:

    if(not format.format_class(cl)):
        # skip undocumented classes
        continue

    methods = inspect.getmembers(cl[1], inspect.isfunction)
    properties = inspect.getmembers(cl[1], lambda o: isinstance(o, property))

    # methods and functions
    for method in methods:
        format.format_function(method)

    # properties
    format.format_properties(properties)
