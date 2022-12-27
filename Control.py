from Lekser import *
from Parser import *
from Exegete import *

def run(text):
    # генерація tokens
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens
    if error: return None, error

    # генерація AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # генерація ASM
    interpreter = Interpreter()
    result = interpreter.visit(ast.node)

    return result, None
