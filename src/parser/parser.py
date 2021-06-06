import re
from src.lexer.tokrules import tokens
from src.parser.Abstract_Syntax_Tree import *

from src.parser.bool import *
from src.parser.expression import *
from src.parser.function import *
from src.parser.statement import *
from src.parser.var_def import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    (
        'right', 'UMINUS'
    ),  # Unary minus operator(%prec UMINUS覆盖了默认的优先级（MINUS的优先级），将UMINUS指代的优先级应用在该语法规则上)
)


# ProgDef:     program Iden ';' SubProg '.'
# SubProg:     VarDef compound_statement
# 将SubProg改为如下,以支持函数定义:
# SubProg:     VarDef label_declaration_part function_definition compound_statement
def p_ProgDef(p):
    'ProgDef : PROGRAM ID SEMICOLON SubProg ENDPOINT'
    p[0] = ProgramNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)


def p_SubProg(p):
    'SubProg : VarDef function_definition compound_statement'
    #    'SubProg : VarDef label_declaration_part function_definition compound_statement'
    p[0] = SubProgNode(p[1], p[2], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_error(p):
    print('[语法分析] 不能接受的Token "{}" 位于 {}. 总位置: {})'.format(
        p.value, p.lineno, p.lexpos))
    # p.lexer.mparser.statestack.pop()
    # p.lexer.mparser.symstack.pop()
    # p.lexer.mparser.state = p.lexer.mparser.statestack[-1]
    # p.lexer.mparser.errorok = True
    # return p.lexer.token()
    pass


def p_empty(p):
    'empty : '
    pass


# 增加对goto的文法支持
# label_declaration_part : LABEL label_list ';'
#                        | empty
# label_list : label_list ',' label
#            | label
# label : DIGSEQ      ——>已经在goto那部分有了


def p_label_declaration_part_1(p):
    'label_declaration_part : DIGSEQ label_list SEMICOLON'
    p[0] = p[1]


def p_label_declaration_part_2(p):
    'label_declaration_part : empty'
    pass


def p_label_list_1(p):
    'label_list : label_list COMMA label'
    P[0] = LabelListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)


def p_label_list_2(p):
    'label_list : label'
    p[0] = p[1]
