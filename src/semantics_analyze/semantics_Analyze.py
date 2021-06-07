'''
语义分析
'''

from src.parser import Abstract_Syntax_Tree as AST
import sys

class SemanticsAnalyze(object):
    def __init__(self, rootNode, SymTab):
        self.rootNode = rootNode
        self.symbol_table_obj = SymTab

    def walkTree(self, node):
        if node is not None and isinstance(node, AST.Node):
            if node.__class__.__name__ == 'AssignmentNode':     # 只有赋值语句可能会使得符号的值改变
                # print(len(node.children))   # 2 [赋值语句的子结点一定是2]
                # print(node.children[0])     # 例如：Identifier: i
                # print(node.children[-1])    # 例如：Unary_Operation、Binary_Operation
                # print(node.children[0].name)  # 例如：i
                if self.symbol_table_obj.symbolTable.get(node.children[0].name) is None:    # 没有查到该符号
                    print("[语义分析]: 变量 %s 未经定义便使用!" % node.children[0].name)
                    sys.exit(1)
                else:   # 该符号在符号表里有定义
                    # print(node.children[-1])
                    value = self.getArithmeticValue(node.children[-1])
                    if value is not None:
                        self.symbol_table_obj.symbolTable[node.children[0].name].value = value 
                        node.expr = value
                    # self.symbol_table_obj.symbolTable[node.children[0].name].value = self.getArithmeticValue(node.children[-1])

        if isinstance(node, AST.Node):
            for child in node.children:
                self.walkTree(child)

    def getArithmeticValue(self, node):
        # if node is None or not isinstance(node, AST.Node):
        if node is None:
            return None
        else:
            # print(node)
            if node.__class__.__name__ == 'UnaryOpNode':
                if node.children[0] == '-':
                    if self.getArithmeticValue(node.children[-1]) is not None:
                        return -self.getArithmeticValue(node.children[-1])
            elif node.__class__.__name__ == 'BinaryOpNode':
                if len(node.children) != 3:    # BinaryOpNode有三个子节点
                    print("错误: BinaryOpNode 应该有 3 个孩子")
                    sys.exit(1)
                else:
                    leftValue = self.getArithmeticValue(node.children[0])
                    rigthValue = self.getArithmeticValue(node.children[-1])
                    operation = node.children[1]
                    if leftValue is None or rigthValue is None:
                        return None
                    if operation == '+':
                        newValue = leftValue + rigthValue
                    elif operation == '-':
                        newValue = leftValue - rigthValue
                    elif operation == '*':
                        newValue = leftValue * rigthValue
                    elif operation == '/':
                        newValue = leftValue / rigthValue

                    return newValue

            elif node.__class__.__name__ == 'IdNode':
                idNodeValue = self.symbol_table_obj.symbolTable.get(node.name).value
                if idNodeValue is None:
                    print("[语义分析]: 变量 %s 未初始化的使用" % node.name)
                    sys.exit(1)
                else:
                    return None
                    # return idNodeValue
            elif isinstance(node, int) or isinstance(node, float):
                # print("is int or float: %d" % node)
                return node

    def analyze(self):
        self.walkTree(self.rootNode)


    def checkVar(self):
        pass

    def print_newSymbolTable(self):
        print('+' * 39 + ' 语义分析新符号表 ' + '+' * 39)
        for k in self.symbol_table_obj.symbolTable.keys():
            print(k + ': ', end = '')
            print(self.symbol_table_obj.symbolTable[k].__dict__.items())
        print('+' * 48 + '+' * 48)
