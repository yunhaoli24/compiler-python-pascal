# -------------------- 布尔表达式BoolExpr的文法 --------------

# BoolExpr:    Expr RelationOp Expr | BoolExpr And BoolExpr | BoolExpr Or BoolExpr
#             | Not BoolExpr | '(' BoolExpr ')'
#             | Expr                                                                ——>[zcr补充]
# RelationOp:  '<' | '>' | '=' | GE | NE | LE
from src.parser.Abstract_Syntax_Tree import *

def p_BoolExpr_LT(p):
    'BoolExpr : Expr LT Expr'
    # p[0] = (p[1] < p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_LE(p):
    'BoolExpr : Expr LE Expr'
    # p[0] = (p[1] <= p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_GT(p):
    'BoolExpr : Expr GT Expr'
    # p[0] = (p[1] > p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_GE(p):
    'BoolExpr : Expr GE Expr'
    # p[0] = (p[1] >= p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_EQ(p):
    'BoolExpr : Expr EQ Expr'
    # p[0] = (p[1] == p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_NE(p):
    'BoolExpr : Expr NE Expr'
    p[0] = (p[1] != p[3])
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_AND(p):
    'BoolExpr : BoolExpr AND BoolExpr'
    # p[0] = p[1] and p[3]
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_OR(p):
    'BoolExpr : BoolExpr OR BoolExpr'
    # p[0] = p[1] or p[3]
    p[0] = BinaryBoolNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_NOT(p):
    'BoolExpr : NOT BoolExpr'
    # p[0] = not p[2]
    p[0] = UnaryBoolNode(p[1], p[2])  # 这里一元bool运算其实只有非运算(not)
    p[0].pos_info = getPosition(p, 0)


def p_BoolExpr_Parentheses(p):
    'BoolExpr : LPAREN BoolExpr RPAREN'
    p[0] = p[2]


def p_BoolExpr(p):
    'BoolExpr : Expr'
    p[0] = p[1]