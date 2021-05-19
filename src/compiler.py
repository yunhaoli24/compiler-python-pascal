import sys
import os
import ply.lex as lex
import src.tokrules


class Compiler(object):
    def __init__(self, file_path, debug):
        self.data = self.read_file(file_path)
        self.debug = debug

        self.lexer = lex.lex(module=src.tokrules, debug=False)
        self.lexer.input(self.data)

    def analyze(self):
        if self.debug:
            for token in self.lexer:
                print(token)

    def read_file(self, file_path):
        try:
            print('正在读入目标代码....')
            with open(file_path, 'r', encoding='utf-8') as sourceF:
                data = sourceF.read()
            print('读入代码成功！')
            return data
        except Exception:
            print("输入正确的文件路径！")
            sys.exit(-1)
