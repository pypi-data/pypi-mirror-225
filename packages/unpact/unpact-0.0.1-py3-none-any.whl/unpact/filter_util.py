from typing import Any,  MutableMapping
from .tree import Tree, load_tree_rep



def _filter_tree(data: dict[str, Any], tree: Tree, accum: dict[str, Any]={}) -> dict[str, Any]:
    if len(tree.children) == 0 or not data:
        if isinstance(data, list):
            return [_filter_tree(d, tree, accum) for d in data]
        return {tree.path: data.get(tree.path)}
    
    for child in tree.children:
        if isinstance(data, list):
            ls = []
            for item in data:
                if isinstance(item, MutableMapping):
                    value = _filter_tree(item.get(tree.path, {}), child, {})
                    if value:
                        ls.append(value)
            accum[tree.path] = ls
        elif isinstance(data, MutableMapping):
            value = _filter_tree(data.get(tree.path, {}), child, {})
            if value is not None:
                if isinstance(value, MutableMapping):
                    if tree.path not in accum:
                        accum[tree.path] = {}
                    accum[tree.path].update(value) 
                else:
                    accum[tree.path] = value
    return accum





def filter_dict(data: dict[str, Any], paths: list[str]):
    tree = load_tree_rep(paths)
    filtered = _filter_tree({'root': data}, tree)
    return filtered['root']


    
    

    





