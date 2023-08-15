from typing import Any, Dict, List, Sequence, Tuple, Union

from .tree import Tree, ColumnSpec, load_tree_rep

__all__ = ['unwind'] 

def _unwind(data: dict, tree: Tree) -> Union[List, List[Dict[str, Any]], Dict[str, Any], dict,  List[dict]]:
    if not tree.children:
        tree_data = data.get(tree.path)
        if isinstance(data, list):
            return [_unwind(d, tree) for d in data]
        if isinstance(tree_data, list):
            return [tree.get_value(x) for x in tree_data]
        return tree.get_value(data.get(tree.path))
    
    level_list: List[dict] = []
    level_dict: dict = {}
    
    tree_data = data.get(tree.path)
    
    if isinstance(tree_data, list):
        for item in tree_data:
            item_output_dict = {}
            item_accum: List[dict] = []
            for child in tree.children:
                value: Union[dict, list] = _unwind(item, child)
                if isinstance(value, list):
                    if item_accum and len(item_accum) == len(value): # Handle adjacents
                        item_accum = [{**a, **b} for a,b in zip(item_accum, value)]
                    else:
                        item_accum.extend(value)
                else:
                    item_output_dict.update(value)
            level_list.extend([{**item_output_dict, **item} for item in item_accum])
            
    else:
        for child in tree.children:
            value = _unwind(tree_data, child) # type: ignore
            if isinstance(value, list):
                level_list.extend(value)
            else:
                level_dict.update(value)
                
    if len(level_list) == 0:
        return level_dict
    
    appended = [{**level_dict, **list_value} for list_value in level_list]
    return appended


def unwind(data: Dict[Any, Any], columns: Sequence[Union[str, Tuple[str, ColumnSpec]]]):
    paths_list = list(columns)
    tree = load_tree_rep(paths_list)
    unwound = _unwind({'root': data}, tree)
    if not isinstance(unwound, list):
        raise Exception('Unwind operation returned a dictionary')
    
    return unwound
                