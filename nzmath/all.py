import os, os.path, imp

import nzmath
_NZMATH_root = os.path.split(nzmath.__path__[0])[0]
del nzmath

def import_all(directory):
    """
    Execute 'from (directory) import (all files except "all.py")'.
    """
    exec('import ' + directory)
    try:
        import_files = eval(directory + ".__all__")
        for import_file in import_files:
            if import_file != "all":
                exec('import ' + directory + '.' + import_file)
    except AttributeError: # __all__ does not exist
        pass
    except ImportError: # import_file is not file name
        pass

def search_subdir(directory):
    """
    Return all (1-level) subdirectory-names in directory.
    directory should be a path string.
    """
    return [subdir for subdir in os.listdir(directory) 
            if os.path.isdir(os.path.join(directory, subdir))]

def path_to_import_str(path, import_root_path='/'):
    """
    Return '.' separated form (for Python import statements)
    from an (absolute) path.
    """
    for (suffix,mode,imp_type) in imp.get_suffixes():
        dot_idx = path.find(suffix)
        if path.find(suffix) >= 0:
            path = path[:len(suffix)]

    if path.find(import_root_path) >= 0:
        path = path[len(import_root_path):]
    if os.path.isabs(path):
        path = path[1:]

    head, tail = os.path.split(path)
    if not(head):
        return tail
    head = path_to_import_str(head, import_root_path)
    return head + '.' + tail

def recursive_import_all(rootdir, import_root_path):
    """
    Execute 'from (dir) import *' at all directories in rootdir recursively.
    All directories are searched by using Breadth-First Search 
    from rootdir (rootdir is included in). 

    rootdir should be an absolute path under import_root_path. 
    import_root_path should be a directory 
    whose Python can be searchable on importing process.
    """
    queue = [rootdir]
    while queue:
        target_dir = queue.pop(0)
        import_all(path_to_import_str(target_dir, import_root_path))
        queue.extend([os.path.join(target_dir, subdir) 
            for subdir in search_subdir(target_dir)])

script_dir = os.path.split(__file__)[0]
recursive_import_all(script_dir, _NZMATH_root)

del imp, os.path, os
