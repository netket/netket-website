import netket as nk
import format
import inspect


classes = inspect.getmembers(nk.graph, inspect.isclass)

for cl in classes:

    # format the class header and constructor(s)
    print(format.format_class(cl))

    # methods = inspect.getmembers(cl[1], inspect.isfunction)

    # methods and functions
    # for method in methods:
    #     format.format_function(method)
