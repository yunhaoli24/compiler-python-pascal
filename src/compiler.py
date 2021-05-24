import sys
import os
import ply.lex as lex
import ply.yacc as yacc
from src.lexer import tokrules
from src.parser import parser
from src.parser import AST_Dumper
from src.symbol_table.symbol_table import SymbolTable
from src.semantics_analyze.semantics_Analyze import SemanticsAnalyze
from src.intermediate_code.Gen_IntermediateCode import IC_Generator


class Compiler(object):
    def __init__(self, file_path, debug):
        self.data = self.read_file(file_path)
        self.debug = debug

        self.lexer = lex.lex(module=tokrules, debug=False)
        self.parser = yacc.yacc(module=parser, debug=False, start="ProgDef")

    def analyze(self):
        if (self.debug):
            self.lexer.input(self.data)
            for token in self.lexer:
                print(token)

        print("正在进行语法分析....")
        Abstract_Syntax_Tree = self.parser.parse(input=self.data,
                                                 lexer=self.lexer,
                                                 tracking=True)
        # 打印抽象语法树
        print('+' * 43 + ' 抽象语法树 ' + '+' * 43)
        AST_Dumper.showNode(Abstract_Syntax_Tree, 0)
        print('+' * 48 + '+' * 48)

        # 生成符号表
        symbol_table = SymbolTable(Abstract_Syntax_Tree)
        symbol_table.generate_symbolTable()
        symbol_table.print_SymbolTable()

        # 语义分析
        semantics_analyze = SemanticsAnalyze(Abstract_Syntax_Tree,
                                             symbol_table)
        semantics_analyze.analyze()
        semantics_analyze.print_newSymbolTable()

        # 生成四元式
        ic_generator_obj = IC_Generator(Abstract_Syntax_Tree)
        print('+' * 44 + ' 四元式 ' + '+' * 44)
        ic_generator_obj.print_IC()
        print('+' * 48 + '+' * 48)

    def read_file(self, file_path):
        try:
            print('正在读入目标代码....')
            with open(file_path, 'r', encoding='utf-8') as sourceF:
                data = sourceF.read()
            return data
        except Exception:
            print("输入正确的文件路径！")
            sys.exit(-1)
