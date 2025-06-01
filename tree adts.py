
from project_demo_final import*

def insert(bst, key):
    if bst =={}:
        bst["value"]=key
        bst["left"]={}
        bst["right"]={}
        # bst=create(e)
    elif key < bst["value"]:
        insert(bst["left"],key)
    elif key> bst["value"]:
        insert(bst["right"],key)

def exist(bst, key):
    
    if bst=={}:
        return True
    elif key < bst["value"]:
        return exist(bst["left"],key)
    elif key>bst["value"]:
        return exist(bst["right"],key)
    elif key==bst["value"]:
        return True


def minimum(bst, starting_node):
    temp=bst
    while temp !={} and temp["value"]!=starting_node:
        if starting_node < temp["value"]:
            temp=temp["left"]
        else:
            temp=temp["right"]
    while temp["left"] !={}:
        temp=temp["left"]
    return temp

def maximum(bst,starting_node):
    
    temp=bst
    while temp !={} and temp["value"]!=starting_node:
        if starting_node < temp["value"]:
            temp=temp["left"]
        else:
            temp=temp["right"]
    while temp["right"] !={}:
        temp=temp["right"]
    return temp

def preorder_traversal(bst, res):
    if bst=={}:
        return 
    res.append(bst["value"])
    preorder_traversal(bst["left"],res)
    preorder_traversal(bst["right"],res)

def inorder_traversal(tree, result):
    """Get numbers in sorted order (left -> middle -> right)"""
    if tree=={}:
        return 
    inorder_traversal(tree["left"], result) #left side
    result.append(center(tree["value"])) #current
    inorder_traversal(tree["right"], result) #right side 

def postorder_traversal(bst, res):
    if bst=={}:
        return 
    postorder_traversal(bst["left"],res)
    postorder_traversal(bst["right"],res)
    res.append(bst["value"])

def successor(BST, key, successor_node=None):    
    if BST =={}:
        return successor_node

    if BST["value"] == key:
        if BST["right"] !={}:
            successor_node=BST["right"]["value"]
            left_most_node=minimum(BST,successor_node)
            return left_most_node["value"]
        if successor_node ==None:
            return None
        return successor_node["value"]
    elif BST["value"] < key:
        return successor(BST["right"],key,successor_node)
    else:
        successor_node=BST
        return successor(BST["left"],key,successor_node)

sphere1 = create_sphere((0, 0, 1), 0.5)
sphere2 = create_sphere((0, 0, 0), 0.5)
sphere3 = create_sphere((0, 0, 2), 0.5)
sphere4 = create_sphere((0, 0, 3), 0.5)
spheres = [sphere1, sphere2, sphere3, sphere4]
ray = Ray((0, 0, -1), (0, 0, 1))
kd_tree = build_kd_tree(spheres)
print(kd_tree)

# """get root"""
# Root = get_root(kd_tree)[0]
# print(Root, "hello")

'''insert node'''
node = ((0,3,0),0.5)
insert(kd_tree, node)
print(kd_tree, "hai")

"""If key in the kd_tree"""
key = ((0, 0, 1),0.5)
print(exist(kd_tree, key),'p')
    
   

"""minimum node"""
print(minimum(kd_tree, ((0,0,2),0.5)),'ok')

"""max node"""
print(maximum(kd_tree,((0,0,2),0.5)))

"""Preorder traversal way of tree"""
result =[]
# print(result)
print(preorder_traversal(kd_tree, result), "idek")
print(result)

"""Inorder traversal way of tree"""
result =[]
# print(result)
print(inorder_traversal(kd_tree, result), "idek")
print(result)

"""Postorder traversal way of tree"""
result =[]
# print(result)
print(postorder_traversal(kd_tree, result), "idek")
print(result)

"""Next successor of (0,0,1)"""
key=((0,3,0),0.5)
result=successor(kd_tree, key)
print(result,'done')

