from src.compiler import Compiler
import ply.lex as lex
if __name__ == '__main__':
    path = '/root/workspace/Compilers/compilingPrinciple/testCode/simple.pas'
    debug = True
    print('目标文件：{}'.format(path))
    compiler = Compiler(path, debug)
    compiler.analyze()