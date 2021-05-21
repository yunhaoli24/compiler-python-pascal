# -------------------- 表达式Expression的文法--------------

# Expr:       Expr'+'Expr | Expr'-'Expr | Expr'*'Expr
#             | Expr'/'Expr | '('Expr')' | '-' Expr %prec UMINUS
#             | Variable | Const
# Const:      IntNo | RealNo

from src.parser.Abstract_Syntax_Tree import *

def p_expression_plus(p):
    'Expr : Expr PLUS Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_expression_minus(p):
    'Expr : Expr MINUS Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_expression_times(p):
    'Expr : Expr TIMES Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_expression_div(p):
    'Expr : Expr DIVIDE Expr'
    p[0] = BinaryOpNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_expr_Parentheses(p):
    'Expr : LPAREN Expr RPAREN'
    p[0] = p[2]


def p_expression_uminus(p):
    'Expr : MINUS Expr %prec UMINUS'
    p[0] = UnaryOpNode(p[1], p[2])
    p[0].pos_info = getPosition(p, 0)


def p_expression_variable(p):
    'Expr : Variable'
    p[0] = p[1]


def p_expression_const(p):
    'Expr : const'
    p[0] = p[1]


# 常量(整数和浮点数)
def p_const_INT_NUMBER(p):
    'const : INT_NUMBER'
    p[0] = p[1]


def p_const_REAL_NUMBER(p):
    'const : REAL_NUMBER'
    p[0] = p[1]