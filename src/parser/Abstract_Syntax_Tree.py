'''
抽象语法树AST
'''
class Node(object):
    '''定义抽象语法树的结点基类'''
    def accept(self, visitor, arg=None):
        return visitor.visit(self, arg)

    @property
    def children(self):
        return list()

    def replace(self, child, node):
        keys = self.__dict__.keys()
        for k in keys:
            if self.__dict__[k] != child:
                continue
            self.__dict__[k] = node
            return True

        for c in filter(None, self.children):
            if c.replace(child, node):
                return True

        return False

    @property
    def position(self):
        if hasattr(self, 'pos_info'):
            return self.pos_info

        for c in filter(None, self.children):
            if not isinstance(c, Node):
                continue

            pos_info = c.position
            if pos_info is not None:
                return pos_info

    @property
    def type(self):
        if hasattr(self, '_type'):
            return self._type

    @type.setter
    def type(self, val):
        # assert isinstance(val, Type)
        self._type = val

    def __str__(self):
        return self.name

class ProgramNode(Node):
    def __init__(self, ID, SubProg, identifier_list=None):
        self.identifier = ID
        self.SubProg = SubProg
        self.identifier_list = identifier_list

    @property   # 让children方法变成类的属性
    def children(self):
        return [self.identifier, self.identifier_list, self.SubProg]

    def __str__(self):
        return "ProgDef"

class SubProgNode(Node):
    def __init__(self, VarDef, function_definition, CompState):
        self.varDef = VarDef
        self.function_definition = function_definition
        self.compState = CompState

    @property
    def children(self):
        return [self.varDef, self.function_definition, self.compState]

    def __str__(self):
        return "SubProg"

class VarDefNode(Node):
    # variable其实就是identifier(文法中定义：Variable: Iden)
    def __init__(self, VarDefList = None):
        self.var_def_list = VarDefList

    @property
    def children(self):
        return [self.var_def_list]

    def __str__(self):
        return "VarDef"

class VarDefListNode(Node):
    def __init__(self, VarDefState, VarDefList = None):
        self._children = list()
        if VarDefList:
            self._children.extend(VarDefList._children)
        self._children.append(VarDefState)

    @property
    def children(self):
        return self._children

    def __str__(self):
        return "VarDefList"

#  添加对数组的支持
class VarDefStateNode(Node):
    def __init__(self, Varlist = None, Type = None, ArrayDefState = None):
        if Varlist is not None and Type is not None:
            self.varlist = Varlist
            self.type = Type
        elif ArrayDefState is not None:
            self.arrayDefState = ArrayDefState

    @property
    def children(self):
        # if self.varlist is not None and self.type is not None:
        #     return [self.varlist, self.type]
        # elif self.arrayDefState is not None:
        #     return [self.arrayDefState]
        if hasattr(self, 'varlist'):
            return [self.varlist, self.type]
        elif hasattr(self, 'arrayDefState'):
            return [self.arrayDefState]

    def __str__(self):
        return "VarDefState"


class VarListNode(Node):
    def __init__(self, Variable, VarList = None):
        self._children = list()
        if VarList:
            self._children.extend(VarList._children)
        self._children.append(Variable)

    @property
    def children(self):
        return self._children

    def __str__(self):
        return "VarList"

#  添加对数组的支持
class ArrayNode(Node):
    def __init__(self, arrayName, index_list, arrayElem_type):
        self.arrayName = arrayName
        self.index_list = index_list
        self.arrayElem_type = arrayElem_type

    @property
    def children(self):
        return [self.arrayName, self.index_list, self.arrayElem_type]

    def __str__(self):
        return "ArrayDefState"

class IndexListNode(Node):
    def __init__(self, index, index_list = None):
        self._children = list()
        if index_list:
            self._children.extend(index_list._children)
        self._children.append(index)

    @property
    def children(self):
        return self._children

    def __str__(self):
        return "index_list"

class IndexNode(Node):
    def __init__(self, startIndex, endIndex):
        self.startIndex = startIndex
        self.endIndex = endIndex

    @property
    def children(self):
        return [self.startIndex, self.endIndex]

    def __str__(self):
        return "index"


class IdNode(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Identifier: %s" % self.name

#------------------------- Statement ------------------------

class StateListNode(Node):
    def __init__(self, Statement, StateList = None):
        self._children = list()
        if StateList:
            self._children.extend(StateList._children)
        self._children.append(Statement)

    @property
    def children(self):
        return self._children

    def __str__(self):
        return "Statement_List"

class LabeledStatementNode(Node):
    def __init__(self, label, Statement):
        self.label = label
        self.statement = Statement

    @property
    def children(self):
        return [self.label, self.statement]

    def __str__(self):
        return "Labeled_Statement"

class NoneLabeledClosedStatementNode(Node):
    def __init__(self, statement, stat_type):
        self.statement = statement
        self.type = stat_type

    @property
    def children(self):
        return [self.statement, self.type]

    def __str__(self):
        return "non_labeled_closed_statement"

# 添加对case的文法支持
class CaseStatementNode(Node):
    def __init__(self, case_index, case_element_list):
        self.case_index = case_index
        self.case_element_list = case_element_list

    @property
    def children(self):
        return [self.case_index, self.case_element_list]

    def __str__(self):
        return "case_statement"

class CaseElementListNode(Node):
    def __init__(self, case_element, case_element_list = None):
        self._children = list()
        if case_element_list:
            self._children.extend(case_element_list._children)
        self._children.append(case_element)

    @property
    def children(self):
        return self._children

    def __str__(self):
        return "case_element_list"

class CaseElementNode(Node):
    def __init__(self, case_constant, Statement):
        self.case_constant = case_constant
        self.case_statement = Statement

    @property
    def children(self):
        return [self.case_constant, self.case_statement]

    def __str__(self):
        return "case_element"


class IfNode(Node):
    def __init__(self, BoolExpr, true_statement, false_statement = None):
        self.BoolExpr = BoolExpr
        self.iftrue_stat = true_statement
        self.iffalse_stat = false_statement

    @property
    def children(self):
        return [self.BoolExpr, self.iftrue_stat, self.iffalse_stat]

    def __str__(self):
        return "If_Statement"
        
class WhileNode(Node):
    def __init__(self, BoolExpr, while_body):
        self.BoolExpr = BoolExpr
        self.body = while_body

    @property
    def children(self):
        return [self.BoolExpr, self.body]

    def __str__(self):
        return "While_Statement"

class ForNode(Node):
    def __init__(self, Variable, initial_value, direction, final_value, body):
        self.variable = Variable
        self.start_value = initial_value
        self.direction = direction.lower()
        self.end_value = final_value
        self.body = body

    @property
    def children(self):
        return [self.variable, self.start_value, self.direction, self.end_value, self.body]

    def __str__(self):
        return "For_(%s)" % self.direction

class AssignmentNode(Node):
    def __init__(self, Variable, Expr):
        self.variable = Variable
        self.expr = Expr

    @property
    def children(self):
        return [self.variable, self.expr]

    def __str__(self):
        return "Assignment_Statement"

class CompoundStatementNode(Node):
    '''复合语句结点(只有一个子结点Statement_List)'''
    def __init__(self, Statement_List):
        self.Statement_List = Statement_List

    @property
    def children(self):
        return [self.Statement_List]

    def __str__(self):
        return "Compound_Statement"

class GotoNode(Node):
    def __init__(self, label):
        self.label = label

    @property
    def children(self):
        return [self.label]

    def __str__(self):
        return "Goto_Statement"


class BinaryOpNode(Node):
    '''二元算术运算结点'''
    def __init__(self, leftExpr, op, rightExpr):
        self.leftExpr = leftExpr
        self.op = op
        self.rightExpr = rightExpr

    @property
    def children(self):
        return [self.leftExpr, self.op, self.rightExpr]

    def __str__(self):
        return "Binary_Operation"

class UnaryOpNode(Node):
    '''一元算术运算结点'''
    def __init__(self, unary_operation_name, Expr):
        self.unary_op = unary_operation_name
        self.expr = Expr

    @property
    def children(self):
        return [self.unary_op, self.expr]

    def __str__(self):
        return "Unary_Operation"

class BinaryBoolNode(Node):
    '''二元布尔运算结点'''
    def __init__(self, leftExpr, op, rightExpr):
        self.left_boolExpr = leftExpr
        self.bool_op = op
        self.right_boolExpr = rightExpr

    @property
    def children(self):
        return [self.left_boolExpr, self.bool_op, self.right_boolExpr]

    def __str__(self):
        return "Binary_Bool_Operation"

class UnaryBoolNode(Node):
    '''一元布尔运算结点'''
    def __init__(self, unary_bool_operation_name, Expr):
        self.unary_bool_op = unary_bool_operation_name
        self.bool_expr = Expr

    @property
    def children(self):
        return [self.unary_bool_op, self.bool_expr]

    def __str__(self):
        return "Unary_Bool_Operation"

class FuncDefinitionNode(Node):
    def __init__(self, function_heading, function_block):
        self.func_heading = function_heading
        self.func_body = function_block

    @property
    def children(self):
        return [self.func_heading, self.func_body]

    def __str__(self):
        return "function_definition"

class FuncHeadingNode(Node):
    def __init__(self, funcName, return_type, parameter_list = None):
        self.funcName = funcName
        self.return_type = return_type
        # if parameter_list is not None:
        #     self.parameter_list = parameter_list
        self.parameter_list = parameter_list

    @property
    def children(self):
        return [self.funcName, self.return_type, self.parameter_list]

    def __str__(self):
        return "function_heading"



# class StatementNode(Node):
#     def __init__(self, AsignState = None, CompState = None, ISE = None, IBT = None, WBD = None, Statement = None):
#         if AsignState:
#             self.type = 'assignment_statement'
#             self.assignment_state = AsignState
#         elif CompState:
#             self.type = 'compound_statement'
#             self.compound_state = CompState
#         elif ISE and Statement:
#             self.type = 'if_then_else'
#             self.ISE = ISE
#             self.stat_4_ISE = Statement
#         elif IBT and Statement:
#             self.type = 'if_then'
#             self.IBT = IBT
#             self.stat_4_IBT = Statement
#         else:
#             self.type = 'while_statement'
#             self.WBD = WBD
#             self.stat_4_WBD = Statement

#     @property
#     def children(self):
#         if self.type == 'assignment_statement':
#             return [self.assignment_state]
#         elif self.type == 'compound_statement':
#             return [self.compound_state]
#         elif self.type == 'if_then_else':
#             return [self.ISE, self.stat_4_ISE]
#         elif self.type == 'if_then':
#             return [self.IBT, self.stat_4_IBT]
#         else:
#             return [self.WBD, self.stat_4_WBD]

#     def __str__(self):
#         return 'Statement'

# class AsignStateNode(Node):
#     def __init__(self, Variable, Expr):
#         self.variable = Variable
#         self.expression = Expr

#     @property
#     def children(self):
#         return [self.variable, self.expression]

#     def __str__(self):
#         return "Assignment statement"

# class  ISE_Node(Node):
#     def __init__(self, IBT, Statement, Else):
#         self.IBT = IBT
#         self.statement = Statement

#     @property
#     def children(self):
#         return [self.IBT, self.statement]

#     def __str__(self):
#         return "If Statement Else"

# class IBT_Node(Node):
#     def __init__(self, If, BoolExpr, Then):
#         self.BoolExpr = BoolExpr

#     @property
#     def children(self):
#         return [self.BoolExpr]

#     def __str__(self):
#         return "if BoolExpr then"

# class WBD_Node(Node):
#     def __init__(self, BoolExpr, Statement):
#         self.BoolExpr = BoolExpr
#         self.Statement = Statement

#     @property
#     def children(self):
#         return [self.BoolExpr, self.Statement]

#     def __str__(self):
#         return "while BoolExpr do Statement"

# class CompStateNode(Node):
#     def __init__(self, StateList):
#         self.StateList = StateList

#     @property
#     def children(self):
#         return [self.StateList]

#     def __str__(self):
#         return "Compound Statement"

def getPosition(p, num):
    line = p.lineno(num)
    span = p.lexspan(num)

    class PositionInfo(object):
        def __init__(self, **kwargs):
            self.__dict__ = kwargs

        def __str__(self):
            return str(self.lineno)

    return PositionInfo(lineno=line, lexpos=span[0], lexendpos=span[1])