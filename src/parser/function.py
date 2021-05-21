# ----------------------------- 增加对函数的文法支持 -------------------------------
# SubProg:     VarDef function_definition compound_statement  [在最上面进行修改]

# function_definition : function_heading ';' function_block
#                     : empty
# function_heading    : FUNCTION funcName ':' return_type
#                     | FUNCTION funcName parameter_list ':' return_type
# parameter_list      : '(' VarDefList ')'
# funcName            : Iden
# return_type         : Type
# function_block      : compound_statement


def p_function_definition_1(p):
    'function_definition : function_heading SEMICOLON function_block'
    p[0] = FuncDefinitionNode(p[1], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_function_definition_2(p):
    'function_definition : empty'  # 可以没有函数定义
    pass


def p_function_heading_1(p):
    'function_heading : FUNCTION funcName COLON return_type'
    p[0] = FuncHeadingNode(p[2], p[4])
    p[0].pos_info = getPosition(p, 0)


def p_function_heading_2(p):
    'function_heading : FUNCTION funcName parameter_list COLON return_type'
    p[0] = FuncHeadingNode(p[2], p[5], p[3])
    p[0].pos_info = getPosition(p, 0)


def p_parameter_list(p):
    'parameter_list : LPAREN VarDefList RPAREN'
    p[0] = p[2]


def p_funcName(p):
    'funcName : ID'
    p[0] = p[1]


def p_return_type(p):
    'return_type : Type'
    p[0] = p[1]


def p_function_block(p):
    'function_block : compound_statement'
    p[0] = p[1]