#!/usr/bin/python3
import core.project
import core.file

rows = [
    (None, 0, "hello, world!"),
        (0, 1, "benis"),
            (1, 10, "asd"),
                (10, 100, "123"),
                (10, 101, "10101"),
                (10, 102, "portals"),
                    (102, 1020, "cube"),
                    (102, 1021, "gahnoo"),
                        (1021, 10210, "lonix"),
            (1, 11, "m$"),
                (11, 110, "winders"),
            (1, 13, "bsd"),
            (1, 14, "p9"),
        (0, 2, "c++"),
            (2, 20, "java"),
]

proj = core.project.Project("test.db")
proj.add_file("ld-2.24.so")
so = proj.open_file(1)

class Tree:

    def __init__(self, nodes, base=None, parent=None):
        # Lol @ python's recursive stuff.  Default stack depth is 999 after
        # which it will just error.  Therefore, we should make non-recursive
        # tree.
        self.subs = {id: Tree(nodes, id, self)
                     for (parent, id, _) in nodes if parent == base}
        values = [value for (_, id, value) in nodes if id == base]
        self.root = len(values) == 0
        if not self.root:
            self.parent = parent
            self.value = values[0]

def find_path(start, end):
    (up_start, up_end) = ([], [])

# def depth_search(start, target):
#     # TODO: We can't have recursive anything!!
#     if not start.root and start.value == target:
#         return [start]
#     for (id, sub) in start.subs.items():
#         r = depth_search(sub, target)
#         if r is not None:
#             return [start] + r
#     return None

# def find_path(start, end):
#     # TODO: Same fucking thing
#     # Cancer!
#     r = depth_search(start, end)
#     if r is None:
#         return [start] + find_path(start.parent, end)
#     return r


# root = Tree(rows)

# for x in depth_search(root, "lonix"):
#     print("root" if x.root else x.value)

# for x in find_path(root.subs[0].subs[2].subs[20], "p9"):
#     print("root" if x.root else x.value)
