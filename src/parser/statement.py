#------------------------- 语句Statement的文法 ------------------------

# ******************* 原始的关于Statement的文法 *******************
# StateList:   S_L Statement | Statement
# S_L:         StateList ';'
# 将上面两条合并为一条如下：
# StateList:   StateList ';' Statement | Statement
#
# Statement:   AsignState
#             | ISE Statement
#             | IBT Statement
#             | WBD Statement
#             | CompState
#
# CompState:   Begin StateList End
# AsignState:  Variable':''='Expr
# ISE:         IBT Statement Else
# IBT:         If BoolExpr Then
# WBD:         while BoolExpr Do
# ******************* 原始的关于Statement的文法 *******************

# ————————————————————————————————————————————————————————————————————————————————————————————
# 改造文法：从[http://www.moorecad.com/standardpascal/pascal.y]上找到官方关于statement的文法

# StateList : StateList ';' Statement | Statement

# Statement : open_statement
#           | closed_statement

# open_statement : label COLON non_labeled_open_statement
#                | non_labeled_open_statement

# closed_statement : label COLON non_labeled_closed_statement
#                  | non_labeled_closed_statement

# non_labeled_open_statement : open_if_statement
#                            | open_while_statement
#                            | open_for_statement

# non_labeled_closed_statement : assignment_statement
#                              | compound_statement
#                              | closed_if_statement
#                              | closed_while_statement
#                              | closed_for_statement
#                              | goto_statement
#                              | case_statement   [暂未实现]
#                              | empty
#                              | continue_statement
#                              | break_statement

# open_if_statement   : IF BoolExpr THEN Statement
#                     | IF BoolExpr THEN closed_statement ELSE open_statement
# closed_if_statement : IF BoolExpr THEN closed_statement ELSE closed_statement

# open_while_statement   : WHILE BoolExpr DO open_statement
# closed_while_statement : WHILE BoolExpr DO closed_statement

# open_for_statement   : FOR Variable ASSIGNMENT initial_value direction final_value DO open_statement
# closed_for_statement : FOR Variable ASSIGNMENT initial_value direction final_value DO closed_statement

# initial_value : Expr
# final_value : Expr
# direction : TO
#           | DOWNTO

# assignment_statement : Variable ASSIGNMENT Expr

# compound_statement : BEGIN StateList END

# goto_statement : GOTO label
# label : DIGSEQ

# continue_statement : CONTINUE
# break_statement : BREAK

# ————————————————————————————————————————————————————————————————————————————————————————————

from enum import Enum
from src.parser.Abstract_Syntax_Tree import *

statement_type = Enum(
    'statement_type',
    ('assignStat', 'compoundStat', 'ifStat', 'whileStat', 'forStat',
     'gotoStat', 'caseStat', 'continueStat', 'breakStat'))


def p_statementList_1(p):
    'StateList : StateList SEMICOLON Statement'
    p[0] = StateListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)


def p_statementList_2(p):
    'StateList : Statement'
    p[0] = StateListNode(p[1])
    p[0].pos_info = getPosition(p, 0)


def p_statement_1(p):
    'Statement : open_statement'
    p[0] = p[1]


def p_statement_2(p):
    'Statement : closed_statement'
    p[0] = p[1]


def p_open_statement_1(p):
    'open_statement : label COLON non_labeled_open_statement'
    p[0] = LabeledStatementNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_open_statement_2(p):
    'open_statement : non_labeled_open_statement'
    p[0] = p[1]


def p_closed_statement_1(p):
    'closed_statement : label COLON non_labeled_closed_statement'
    p[0] = LabeledStatementNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_closed_statement_2(p):
    'closed_statement : non_labeled_closed_statement'
    p[0] = p[1]


def p_non_labeled_open_statement_1(p):
    'non_labeled_open_statement : open_if_statement'
    p[0] = p[1]


def p_non_labeled_open_statement_2(p):
    'non_labeled_open_statement : open_while_statement'
    p[0] = p[1]


def p_non_labeled_open_statement_3(p):
    'non_labeled_open_statement : open_for_statement'
    p[0] = p[1]


def p_non_labeled_closed_statement_1(p):
    'non_labeled_closed_statement : assignment_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.assignStat)
    p[0].pos_info = getPosition(p, 0)


def p_non_labeled_closed_statement_2(p):
    'non_labeled_closed_statement : compound_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.compoundStat)
    p[0].pos_info = getPosition(p, 0)


def p_non_labeled_closed_statement_3(p):
    'non_labeled_closed_statement : closed_if_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.ifStat)
    p[0].pos_info = getPosition(p, 0)


def p_non_labeled_closed_statement_4(p):
    'non_labeled_closed_statement : closed_while_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.whileStat)
    p[0].pos_info = getPosition(p, 0)


def p_non_labeled_closed_statement_5(p):
    'non_labeled_closed_statement : closed_for_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.forStat)
    p[0].pos_info = getPosition(p, 0)


def p_non_labeled_closed_statement_6(p):
    'non_labeled_closed_statement : goto_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.gotoStat)
    p[0].pos_info = getPosition(p, 0)


def p_non_labeled_closed_statement_7(p):
    'non_labeled_closed_statement : empty'
    pass


# 增加对case的文法支持
def p_non_labeled_closed_statement_8(p):
    'non_labeled_closed_statement : case_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.caseStat)


# 增加对continue的文法支持
def p_non_labeled_closed_statement_9(p):
    'non_labeled_closed_statement : continue_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.continueStat)


def p_continue_statement(p):
    'continue_statement : CONTINUE'
    p[0] = p[1]


# 增加对break的文法支持
def p_non_labeled_closed_statement_10(p):
    'non_labeled_closed_statement : break_statement'
    p[0] = NoneLabeledClosedStatementNode(p[1], statement_type.breakStat)


def p_break_statement(p):
    'break_statement : BREAK'
    p[0] = p[1]


# case_statement : CASE case_index OF case_element_list END
#                | CASE case_index OF case_element_list ';' END

# case_index     : Expr
# case_element_list: case_element_list ';' case_element | case_element
# case_element   : case_constant ':' Statement
# case_constant  : Const


def p_case_statement_1(p):
    'case_statement : CASE case_index OF case_element_list END'
    p[0] = CaseStatementNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)


def p_case_statement_2(p):
    'case_statement : CASE case_index OF case_element_list SEMICOLON END'
    p[0] = CaseStatementNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)


def p_case_index(p):
    'case_index : Expr'
    p[0] = p[1]


def p_case_element_list_1(p):
    'case_element_list : case_element_list SEMICOLON case_element'
    p[0] = CaseElementListNode(p[3], p[1])
    p[0].pos_info = getPosition(p, 0)


def p_case_element_list_2(p):
    'case_element_list : case_element'
    p[0] = CaseElementListNode(p[1])
    p[0].pos_info = getPosition(p, 0)


def p_case_element(p):
    'case_element : case_constant COLON Statement'
    p[0] = CaseElementNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_case_constant(p):
    'case_constant : const'
    p[0] = p[1]


def p_open_if_statement_1(p):
    'open_if_statement : IF BoolExpr THEN Statement'
    p[0] = IfNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)


def p_open_if_statement_2(p):
    'open_if_statement : IF BoolExpr THEN closed_statement ELSE open_statement'
    p[0] = IfNode(p[2], p[4], p[6])
    p[0].pos_info = getPosition(p, 0)


def p_closed_if_statement(p):
    'closed_if_statement : IF BoolExpr THEN closed_statement ELSE closed_statement'
    p[0] = IfNode(p[2], p[4], p[6])
    p[0].pos_info = getPosition(p, 0)


def p_open_while_statement(p):
    'open_while_statement : WHILE BoolExpr DO open_statement'
    p[0] = WhileNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)


def p_closed_while_statement(p):
    'closed_while_statement : WHILE BoolExpr DO closed_statement'
    p[0] = WhileNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)


def p_open_for_statement(p):
    'open_for_statement : FOR Variable ASSIGNMENT initial_value direction final_value DO open_statement'
    p[0] = ForNode(p[2], p[4], p[5], p[6], p[8])
    p[0].pos_info = getPosition(p, 0)


def p_closed_for_statement(p):
    'closed_for_statement : FOR Variable ASSIGNMENT initial_value direction final_value DO closed_statement'
    p[0] = ForNode(p[2], p[4], p[5], p[6], p[8])
    p[0].pos_info = getPosition(p, 0)


def p_initial_value(p):
    'initial_value : Expr'
    p[0] = p[1]


def p_final_value(p):
    'final_value : Expr'
    p[0] = p[1]


def p_direction_1(p):
    'direction : TO'
    p[0] = p[1]


def p_direction_2(p):
    'direction : DOWNTO'
    p[0] = p[1]


def p_assignment_statement(p):
    'assignment_statement : Variable ASSIGNMENT Expr'
    p[0] = AssignmentNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_compound_statement(p):
    'compound_statement : BEGIN StateList END'
    # p[0] = p[2]   # 建立语法分析树的时候,发现有错误,SubPorg的子结点compound_statement没有生成,后来发现是这里的下标写错了...把p[2]写成p[1]了
    # 上面这样写也是对的,对于后面的分析来说,和下面的把compound_statement单独建一个结点是等价的.但是为了打印出来的语法树更直观,就建立一个compound_statement结点，但是这个结点只有一个子节点(就是Statement_List)
    p[0] = CompoundStatementNode(p[2])
    p[0].pos_info = getPosition(p, 0)


def p_goto_statement(p):
    'goto_statement : GOTO label'
    p[0] = GotoNode(p[2])
    p[0].pos_info = getPosition(p, 0)


def p_label(p):
    'label : DIGSEQ'
    p[0] = p[1]