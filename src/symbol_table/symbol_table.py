'''
遍历语法树,生成符号表并维护符号表
'''

import src.parser.Abstract_Syntax_Tree as AST

class SymbolTable_Item(object):
    '''
    符号表中表项的基类
    '''
    def __init__(self):
        # 这里只定义所有符号
        self.NO = -1
        self.type = None
        self.name = ''
        self.value = None

class SymbolTable(object):
    def __init__(self, rootNode):
        self.symbolTable = dict()   # 将符号表定义为一个字典,方便索引
        self.rootNode = rootNode

    def walkTree(self, node):
        if node is not None and isinstance(node, AST.Node):
            if node.__class__.__name__ == 'VarDefStateNode':

                varList_childNode = node.children[0]
                varType_childNode = node.children[-1] # 变量类型
                if varList_childNode.__class__.__name__ == 'VarListNode':
                    if varType_childNode.__class__.__name__ == 'str':
                        symtb_item_type = varType_childNode
                    else:
                        print('错误: VarDefStateNode 的最后一个孩子的类型不是 str!')
                        return
                    for grandson in varList_childNode.children:
                            symtb_item = SymbolTable_Item()
                            print(grandson)     # 打印标志符
                            symtb_item.NO = len(self.symbolTable)
                            symtb_item.name = grandson.name
                            symtb_item.type = symtb_item_type
                            self.symbolTable[symtb_item.name] = symtb_item   # 将符号的字面值作为字典的索引
                else:
                    print('错误: VarDefStateNode 的第一个孩子不是 VarListNode!')
            
            if isinstance(node, AST.Node):
                for child in node.children:
                    self.walkTree(child)

    def generate_symbolTable(self):
        '''
        生成符号表
        '''
        self.walkTree(self.rootNode)

    def print_SymbolTable(self):
        '''
        打印符号表
        '''
        print('+' * 44 + ' 符号表 ' + '+' * 44)
        for k in self.symbolTable.keys():
            print(k + ': ', end = '')
            print(self.symbolTable[k].__dict__.items())
        print('+' * 48 + '+' * 48)

