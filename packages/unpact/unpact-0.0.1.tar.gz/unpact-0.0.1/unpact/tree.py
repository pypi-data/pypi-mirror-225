from functools import reduce
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, TypedDict, Union


__all__ = ['ColumnSpec', 'Tree']

class ColumnSpec(TypedDict, total=False):
    name: str
    formatter: Callable[[dict], dict]
    


class Tree:
    def __init__(self, parent: Optional["Tree"], path: str) -> None:
        self.parent: Union[Tree, None] = parent
        self.depth: int = 0
        if parent and parent.depth is not None:
            self.depth = parent.depth + 1
        
        self.path: str = path
        self.children: List[Tree] = []
        self.tree_spec: ColumnSpec = {}
    
    @property
    def name(self) -> Any:
        if self.tree_spec.get('name'):
            return self.tree_spec.get('name')
        return self.path
    
    def get_value(self, value: Any):
        formatter = self.tree_spec.get('formatter')
        if formatter:
            return formatter(value)
        
        return {self.name: value}
        
        
            
        
    def add_child(self, child_tree: 'Tree') -> None:
        self.children.append(child_tree)
        
    def get_child(self, path: str) -> 'Tree':
        paths = path.split('.')
        def _select_child(tree: 'Tree', path: str):
            return next(filter(lambda p: p.path == path, tree.children))
        
        child = reduce(lambda tree, path: _select_child(tree, path), paths, self)
        return child
        
        
    def __repr__(self) -> str:
        base = f'{self.path}\n'
        
        for child in self.children:
            sep = '\t' * self.depth
            base += f'{sep}{repr(child)}\n'
        
        return base

def load_tree(data, path, parent=None, root_name='root'):
    
    if parent == None:
        tree = Tree(parent, root_name)
    else:
        tree = Tree(parent=parent, path=path)
    
    if isinstance(data, dict):
        for k,v in data.items():
            child = load_tree(v, k, tree)
            tree.add_child(child)
        
    return tree

def paths_to_dict_tree(paths: list[str], accum: dict ={}):
    if (len(paths) == 0):
        return
    if not accum.get(paths[0]):
        accum[paths[0]] = paths_to_dict_tree(paths[1:], {})
    else:
        accum[paths[0]].update(paths_to_dict_tree(paths[1:], {}))
    return accum

def load_tree_rep(paths: Sequence[Union[str,  Tuple[str, ColumnSpec]]]) -> Tree:
    tree_dict: Dict[str, Any] = {}
    for path in paths:
        if isinstance(path, tuple):
            path = path[0]
        paths_to_dict_tree(path.split('.'), tree_dict)
    tree = load_tree(tree_dict, 'None', parent=None)
    
    specs: List[Tuple[str, ColumnSpec]] = [path for path in paths if isinstance(path, tuple)]
    for path, spec in specs:
        child = tree.get_child(path)
        child.tree_spec = spec
    
    
    return tree