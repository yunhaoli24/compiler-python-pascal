from src.compiler import Compiler

if __name__ == '__main__':
    path = '/root/workspace/Compilers/compilingPrinciple/testCode/simple.pas'
    debug = False
    print('目标文件：{}'.format(path))
    compiler = Compiler(path, debug)
    compiler.analyze()