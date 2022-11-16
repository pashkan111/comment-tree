import pprint
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class Comment:
    id: int
    text: str
    parent_id: Optional[int] = 0
    is_child: Optional[bool] = False
    children: List['Comment'] = field(default_factory=list)
    
    def __post_init__(self):
        if self.parent_id != 0:
            self.is_child = True
            

@dataclass
class Tree:
    data: Optional[List[Dict[int, Comment]]] = field(default_factory=list)


comments = [
    Comment(1, 'comment1'),
    Comment(2, 'comment2', 1),
    Comment(3, 'comment3', 1),
    Comment(4, 'comment4', 2),
    Comment(5, 'comment5', 2),
    Comment(6, 'comment6', 2),
]

# comment1
#   comment2
#       comment4
#       comment5
#   comment3    
    

def get_root_by_id(root: List[Comment], id: int) -> Optional[dict]:
    for comment in root:
        if comment.id == id:
            return comment


def find_orphans(comments: List[Comment], comments_tree: Tree = Tree()) -> Tree:
    """Build comment tree"""
    data = comments_tree.data
    childs = []
    for comment in comments:
        if comment.is_child is False:
            tree = {}
            tree[comment.id] = comment
            data.append(tree)
            continue
        parent_id = comment.parent_id
        parent = get_root_by_id(comments, parent_id)
        if parent:
            children: list = parent.children
            children.append(comment)
        else:
            childs.append(comment)
    if len(childs) != 0:
        data = find_orphans(childs, data)
    return comments_tree  
        
           
pprint.pprint(find_orphans(comments), indent=4)