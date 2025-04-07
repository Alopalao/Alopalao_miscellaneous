from dash import Dash, html
import dash_cytoscape as cyto

class Node:
    def __init__(self, val:str = "", nei=None):
        self.val = val
        self.nei = nei or []

    def __lt__(self, other):
        return self.val < other.val
    
    def __eq__(self, other):
        if isinstance(other, str):
            return self.val == other
        return self.val == other.val
    
    def __str__(self):
        return self.val
    
    def __repr__(self):
        return self.val
    
class Tree:
    def __init__(self, val:str = "", order=0, parent=None, child=None):
        self.val = val
        self.order = order
        self.child = child or []
        # For the graph drawer
        self.parent = parent or ""

    def __eq__(self, other):
        if isinstance(other, str):
            return self.val == other
        return self.val == other.val
    
    def __repr__(self, level=0):
        parent_val = ""
        if self.parent:
            parent_val = self.parent.val
        ret = "\t"*level+self.val+":"+str(self.order)+":"+parent_val+"\n"
        for child in self.child:
            ret += child.__repr__(level+1)
        return ret
    

def populate_tree(root:Tree, visited:list, global_counter:int):
    visited = visited[1:]
    prev = root
    for letter in visited:
        try:
            index = root.child.index(letter)

            root = root.child[index]
        except ValueError:
            global_counter += 1
            node = Tree(letter, global_counter, prev)
            root.child.append(node)
            root = node
        prev = root

    return global_counter


def dfs_backtrack(root: Node, total: int):
    # Also serves as a backtrack mechanism
    visited = []
    # Starting tree
    tree_root = Tree("a", 0)
    global_counter = 0
    # An encountered path
    my_stack:list[tuple[Node, int]] = [(root, 0)]

    back_flag = 0

    complete_paths = []

    while my_stack:
        curr = my_stack.pop()
        #if curr[1] > 20:
        #    break
        if back_flag != 0:
            retrieve = back_flag-curr[1]
            if visited[-1] == 'a':
                retrieve += 1
            visited = visited[:-retrieve]
            back_flag = 0
        print(curr[0].val + " - " + str(curr[1]))
        print("VISITED -> ", visited)
        visited.append(curr[0].val)
        neighbors:list[Node] = curr[0].nei
        print("NEI -> ", neighbors)

        # Check if there are neighbors not in visited
        aux = []
        count = 1
        for node in neighbors:
            if node not in visited:
                aux.append((node, curr[1]+count))
                count += 1
        print("AUX -> ", aux)
        if not aux:
            # Backtrack I think
            x = 0
            print("BACKTRACK")
            back_flag = curr[1]
            if len(visited) == total:
                if root in curr[0].nei:
                    visited.append('a')
                    complete_paths.append(visited)
                    print("FOUND 1")
                    print("THE VISITED")
            global_counter = populate_tree(tree_root, visited, global_counter)
        else:
            my_stack.extend(aux)

    print("ALL PATHS")
    for path in complete_paths:
        print(path)
    return tree_root
        
#a = Node("a")
#b = Node("b")
#c = Node("c")
#d = Node("d")
#e = Node("e")
#f = Node("f")
#
##a.nei = [b, c, d]
#a.nei = [b, d, c]
#b.nei = [a, c, f]
#c.nei = [a, b, d, e]
#d.nei = [a, c, e]
#e.nei = [c, d, f]
#f.nei = [b, e]
#
#a.nei.sort(reverse=True)
#b.nei.sort(reverse=True)
#c.nei.sort(reverse=True)
#d.nei.sort(reverse=True)
#e.nei.sort(reverse=True)
#f.nei.sort(reverse=True)

a = Node("a")
b = Node("b")
c = Node("c")
d = Node("d")
e = Node("e")
f = Node("f")
g = Node("g")
h = Node("h")
i = Node("i")
j = Node("j")
k = Node("k")
l = Node("l")

a.nei = [b, c, d]
b.nei = [a, e, f]
c.nei = [a, d, g]
d.nei = [a, c, h, e]
e.nei = [b, d, f, i]
f.nei = [e, b, j]
g.nei = [h, c, k]
h.nei = [d, g, k, i]
i.nei = [e, h, l, j]
j.nei = [i, f, l]
k.nei = [g, h, l]
l.nei = [k, i, j]


tree = dfs_backtrack(a, 12)

# DRAW TREEE

def draw_tree(tree):
    elemets = []
    
    # Through tree
    stack = [tree]
    while stack:
        curr:Tree = stack.pop()
        label = f"{curr.val}:{curr.order}"
        curr_data = {'id': label, 'label': label}
        elemets.append({'data': curr_data})
        if curr.parent:
            parent_data = {
                "source": f"{curr.parent.val}:{curr.parent.order}",
                "target": curr_data['id']
            }
            elemets.append({'data': parent_data})
        stack.extend(curr.child)

    app = Dash("tree?")
    app.layout = html.Div([
        html.P("Some about dash"),
        cyto.Cytoscape(
            id='cytoscape',
            elements=elemets,
            layout={
                'name': 'breadthfirst',
                'roots': '[id="a:0"]',
                'spacingFactor': 1,
            },
            style={'width': '5000px', 'height': '2000px'},
            stylesheet=[
                {
                    'selector': 'node',
                    'style': {
                        'label': 'data(label)',
                        'font-size': '50px',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'width': 'label',
                        'height': 'label',
                        'padding': '10px',
                    }
                },
            ]
        )
    ])
    app.run(debug=True)

draw_tree(tree)

