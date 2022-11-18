from dataclasses import dataclass, field
from typing import Optional, List


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
    data: Optional[List[Comment]] = field(default_factory=list)


comments = [
    Comment(1, 'comment1'),
    Comment(2, 'comment2', 1),
    Comment(3, 'comment3', 1),
    Comment(9, 'comment9', 1),
    Comment(10, 'comment10', 1),
    Comment(8, 'comment8'),
    Comment(6, 'comment6', 2),
]


def get_root_by_id(root: List[Comment], id: int) -> Optional[dict]:
    for comment in root:
        if comment.id == id:
            return comment


def build_tree(
    comments: List[Comment], 
    comments_tree: Tree = Tree()
    ) -> Tree:
    """Build comment tree"""
    data = comments_tree.data
    childs = []
    for comment in comments:
        if comment.is_child is False:
            data.append(comment)
            continue
        parent_id = comment.parent_id
        parent = get_root_by_id(comments, parent_id)
        if parent:
            children: list = parent.children
            children.append(comment)
        else:
            childs.append(comment)
    if len(childs) != 0:
        data = build_tree(childs, data)
    return comments_tree


def get_comments_with_level(
    comments: List[Comment], 
    level: int = 0, 
    res: List[dict] = []
    ) -> List[set]:
    """Creates a list of tuples. The tuple contains text comment and 
        level.
    """
    for comment in comments:
        res.append((comment.text, level))
        children = comment.children
        if len(children) == 0:
            continue
        get_comments_with_level(children, level+3, res)
    return res


def show_comments(comments: List[set]):
    """Show the tree of comments"""
    for comment in comments:
        text, level = comment
        print(f'{" "*level}{text}')


comment_tree = build_tree(comments=comments, comments_tree=Tree())
comments_with_level = get_comments_with_level(comment_tree.data)
show_comments(comments_with_level)
