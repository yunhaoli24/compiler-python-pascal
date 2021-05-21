'''
打印抽象语法树[为了验证建得对不对]
'''

import src.parser.Abstract_Syntax_Tree as AST

def print_space(level):
    print(str(level) + ' ' * level * 2, end = '')

def showNode(node, level):
    
    if node is not None:
        print_space(level)
        print(node)

    if isinstance(node, AST.Node):
        try:
            for child in node.children:
                showNode(child, level + 1)
        except TypeError as e:
            print(node)
            print('gg')
        