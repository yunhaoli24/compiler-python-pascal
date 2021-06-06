# 词法单元的类型定义为tokens元组，元组的元素就是所有的词法单元类型。tokens元组定义了词法分析器可以产生的所有词法单元的类型，并且在语法分析时这个元组同样会用到，来识别终结符。
part_tokens = [
    'INT_NUMBER',  # 整数
    'REAL_NUMBER',  # 浮点数
    'ID',  # 标识符 Identifier
    'PLUS',  # +
    'MINUS',  # -
    'TIMES',  # *
    'DIVIDE',  # /
    'ASSIGNMENT',  # :=
    'SEMICOLON',  # ;
    'COLON',  # :
    'COMMA',  # ,
    'EQ',  # =
    'LT',  # <
    'LE',  # <=
    'GT',  # >
    'GE',  # >=
    'NE',  # !=
    'LPAREN',  # (
    'RPAREN',  # )
    'LBRAC',  # [
    'RBRAC',  # ]
    'LLAVEI',  # {
    'LLAVED',  # }
    'ENDPOINT',  # .(结束符)
    'DIGSEQ',  # 十进制整数(可以用来做label,即只允许label是'DIGSEQ')
    'GOTO',
    'DOTDOT',  # ..(为了支持数组)
]

# 保留字
reserved = {
    'program': 'PROGRAM',
    'begin': 'BEGIN',
    'end': 'END',
    'var': 'VAR',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'case': 'CASE',
    'of': 'OF',
    'while': 'WHILE',
    'do': 'DO',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'mod': 'MOD',
    'array': 'ARRAY',
    'boolean': 'BOOLEAN',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'integer': 'INTEGER',
    'real': 'REAL',
    'char': 'CHAR',
    'string': 'STRING',
    'uses': 'USES',
    'const': 'CONST',
    # 'true' : 'TRUE',
    # 'false' : 'FALSE',
    'type': 'TYPE',
    'for': 'FOR',
    'to': 'TO',
    'downto': 'DOWNTO',
    'continue': 'CONTINUE',  # 增加对continue的支持
    'break': 'BREAK',  # 增加对break的支持
}

tokens = part_tokens + list(reserved.values())

# 简单的正则表达式，当输入的字符序列符合这个正则表达式时，该序列就会被识别为该类型的词法单元：

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGNMENT = r':='
t_SEMICOLON = r'\;'
t_COLON = r':'
t_COMMA = r','
t_EQ = r'\='
t_LT = r'\<'
t_LE = r'<='
t_GT = r'\>'
t_GE = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRAC = r'\['
t_RBRAC = r'\]'
t_LLAVEI = r'{'
t_LLAVED = r'}'
t_NE = r'!='  # 和Pascal中的<>不同
t_ENDPOINT = r'.'

t_ignore = ' \t\r\x0c'

# value：默认就是识别出的字符串序列。
# type：词法单元的类型，就是在tokens元组中的定义的。
# line：词法单元在源代码中的行号。
# lexpos：词法单元在该行的列号。


# 浮点数(实数) b
def t_REAL_NUMBER(t):
    # r'\d+\.\d+'
    r"[\+-](\d+\.\d+([eE][\+-]\d+)?)|(\d+[eE][\+-]\d+)"
    t.value = float(t.value)
    t.endlexpos = t.lexpos + len(str(t.value))
    return t


# 整数
def t_INT_NUMBER(t):
    r'\d+'  # 如果需要执行动作的话，规则可以写成一个方法。如果使用方法的话，正则表达式写成方法的文档字符串。
    # t.lexer.integer_count += 1  # 统计整数出现的次数
    if (int(t.value) > 65535):
        print("[词法分析] 第{} 行 整数越界'{}'".format(t.lexer.lineno, t.value.lower()))
    t.value = int(t.value)
    t.endlexpos = t.lexpos + len(str(t.value))
    return t


#布尔
def t_BOOLEAN(t):
    r'true|false'
    t.endlexpos = t.lexpos + len(t.value)
    return t


#标记被lex返回后，它们的值被保存在value属性中。正常情况下，value是匹配的实际文本。事实上，value可以被赋为任何Python支持的类型。
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value.lower() in reserved:  # 识别保留字
        t.type = reserved[t.value.lower()]  # 前面如果有下划线，则表示是保留字，而不是普通的ID
    else:
        if len(t.value.lower()) > 8:
            print("[词法分析] 第{} 行标识符长度大于8 '{}' ".format(t.lexer.lineno,
                                                      t.value.lower()))
        t.type = 'ID'  # Check for reserved words
    t.endlexpos = t.lexpos + len(t.value)
    return t


# 丢弃注释,可以用 t_ignore_COMMENT = r'...' 来代替
def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*\n)'
    # r"(?s)(\(\*.*?\*\))|({[^}]*})"
    t.lexer.lineno += (t.value.count("\n"))
    t.endlexpos = t.lexpos + len(t.value)
    pass


def t_CHINESE(t):
    r'[\u4e00-\u9fa5]'
    t.lexer.lineno += (t.value.count("\n"))
    t.endlexpos = t.lexpos + len(t.value)
    print("[词法分析] 第{} 行 忽略中文 '{}' ".format(t.lexer.lineno, t.value.lower()))
    pass


# 识别字符(取决于特定的实现)
# 只支持转义字符：'\t' '\n' and '\\'
def t_CHAR(t):
    r"(\'(([^\\\'])|(\\[\\tn]))\')"
    t.value = t.value[1:-1]
    t.endlexpos = t.lexpos + len(t.value)
    return t


# 识别字符串。允许在字符串中出现 paired \'
def t_STRING(t):
    r"(\'((\'(([^\\\'])|(\\[\\tn]))*\')|((([^\\\'])|(\\[\\tn]))*))*\')"
    escaped = False
    s = t.value[1:-1]  # 提取单引号中间的字符
    new_str = ''
    for i in range(0, len(s)):
        c = s[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = False
        else:
            if c == "\\":
                escaped = True
            else:
                new_str += c
    t.endlexpos = t.lexpos + len(t.value)
    t.value = new_str
    return t


# 十进制整数
# leading zeros are allowed.
def t_DIGSEQ(t):
    r'[0-9]+'
    t.endlexpos = t.lexpos + len(t.value)
    return t


# -------------------- todo ----------------------
def t_STARs(t):
    r"\*\*"
    t.endlexpos = t.lexpos + len(t.value)
    return t


def t_UPARROW(t):
    r"\^"
    t.endlexpos = t.lexpos + len(t.value)
    return t


# ------------------------------------------------

# =========================== array ==============================


#支持数组
def t_DOTDOT(t):
    r"\.\."
    t.endlexpos = t.lexpos + len(t.value)
    return t


# Define a rule so we can track line numbers
#lex.py是不提供行号信息，因为它不知如何识别一行。可以通过t_newline()规则来更新行号信息：
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    print("非法字符: '%s'" % t.value[0])
    t.lexer.skip(1)


# 计算列号，为了指示上下文的错误位置，只在必要时有用。
# input is the input text string, token is a token instance
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column