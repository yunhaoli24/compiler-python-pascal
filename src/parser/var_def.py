# ========================= [变量声明的文法]=============================

# VarDef:         Var VarDefList ';'
# VarDefList:     VarDefList ';' VarDefState | VarDefState
# VarDefState:    VarList ':' Type
#                 | ArrayDefState
# VarList:        VarList ',' Variable | Variable
# Type:           Integer | Real | BOOLEAN | arrayName
# Variable:       Iden

# ArrayDefState:  TYPE arrayName '=' ARRAY '[' index_list ']' OF Type
# arrayName:      Iden
# index_list:     index_list ',' index | index
# index:          startIndex '.''.' endIndex
# startIndex:     Const
# endIndex:       Const

from src.parser.Abstract_Syntax_Tree import *


def p_VarDef(p):
    'VarDef : VAR VarDefList SEMICOLON'
    p[0] = VarDefNode(p[2])
    p[0].pos_info = getPosition(p, 0)


def p_VarDefList_1(p):
    'VarDefList : VarDefList SEMICOLON VarDefState'
    p[0] = VarDefListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)


def p_VarDefList_2(p):
    'VarDefList : VarDefState'
    p[0] = VarDefListNode(p[1])
    p[0].pos_info = getPosition(p, 0)


def p_VarDefState_1(p):
    'VarDefState : VarList COLON Type'
    p[0] = VarDefStateNode(Varlist=p[1], Type=p[3])
    p[0].pos_info = getPosition(p, 0)


def p_VarDefState_2(p):
    'VarDefState : ArrayDefState'
    p[0] = VarDefStateNode(ArrayDefState=p[1])
    p[0].pos_info = getPosition(p, 0)


def p_VarList_1(p):
    'VarList : VarList COMMA Variable'
    p[0] = VarListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)


def p_VarList_2(p):
    'VarList : Variable'
    p[0] = VarListNode(p[1])
    p[0].pos_info = getPosition(p, 0)


def p_ArrayDefState(p):
    'ArrayDefState : TYPE arrayName EQ ARRAY LBRAC index_list RBRAC OF Type'
    p[0] = ArrayNode(p[2], p[6], p[9])
    p[0].pos_info = getPosition(p, 0)


def p_arrayName(p):
    'arrayName : ID'
    p[0] = IdNode(p[1])
    p[0].pos_info = getPosition(p, 0)


def p_index_list_1(p):
    'index_list : index_list COMMA index'
    p[0] = IndexListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)


def p_index_list_2(p):
    'index_list : index'
    p[0] = IndexListNode(p[1])
    p[0].pos_info = getPosition(p, 0)


def p_index(p):
    'index : startIndex DOTDOT endIndex'
    p[0] = IndexNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_type_1(p):
    'Type : INTEGER'  # INTEGER关键字
    p[0] = p[1]


def p_type_2(p):
    'Type : REAL'  # REAL关键字
    p[0] = p[1]


def p_type_3(p):
    'Type : BOOLEAN'
    p[0] = p[1]


def p_type_4(p):
    'Type : arrayName'
    p[0] = p[1]


def p_variable_id(p):
    'Variable : ID'
    # p[0] = p[1]   # 这样写貌似不对
    p[0] = IdNode(p[1])
    p[0].pos_info = getPosition(p, 0)


def p_startIndex(p):
    'startIndex : const'
    p[0] = p[1]


def p_endIndex(p):
    'endIndex : const'
    p[0] = p[1]