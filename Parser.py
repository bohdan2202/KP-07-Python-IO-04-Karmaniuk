from Unchanging import *
from Bungle import *
#вузл
class ProgramNode:
    def __init__(self, functions):
        self.functions = functions

    def __repr__(self):
        return f'{self.functions}'


class FuncNode:
    def __init__(self, type_, decl_list, title, tie):
        self.type = type_
        self.decl_list = decl_list
        self.name = title
        self.node = tie

    def __repr__(self):
        return f'function {self.name}({self.decl_list}) {self.node}'


class StmtListNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'{self.statements}'


class DeclListNode:
    def __init__(self, declarations):
        self.declarations = declarations

    def __repr__(self):
        return f'{self.declarations}'


class DeclarationNode:
    def __init__(self, type_, name):
        self.type_ = type
        self.name = name

    def __repr__(self):
        return f'{self.name}'


class DoWhileNode:
    def __init__(self, node_stmt, node_expr):
        self.node_stmt = node_stmt
        self.node_expr = node_expr

    def __repr__(self):
        return f'\n\tdo {{{self.node_stmt}}} while ({self.node_expr})'


class WhileNode:
    def __init__(self, node_expr, node_stmt):
        self.node_stmt = node_stmt
        self.node_expr = node_expr

    def __repr__(self):
        return f'\n\twhile ({self.node_expr}){{{self.node_stmt}}}'


class IfElseNode:
    def __init__(self, node_expr, node_stmt_if, node_stmt_else):
        self.node_stmt_if = node_stmt_if
        self.node_stmt_else = node_stmt_else
        self.node_expr = node_expr

    def __repr__(self):
        return f'\n\tif ({self.node_expr}){{{self.node_stmt_if}}} else{{{self.node_stmt_else}}}'


class VarAssignNode:
    def __init__(self, type_, name, node):
        self.name = name
        self.node = node
        self.type = type_

    def __repr__(self):
        return f'\n\t{self.name}  = {self.node}'


class VarAssignNullNode:
    def __init__(self, type_, name):
        self.type = type_
        self.name = name

    def __repr__(self):
        return f'\n\t({self.name} = 0)'


class ReturnNode:
    def __init__(self, node):
        self.node = node

    def __repr__(self):
        return f'\n\tRETURN: {self.node}'


class BreakNode:
    def __init__(self):
        pass

    def __repr__(self):
        return f'\n\tBREAK'


class AssignNode:
    def __init__(self, name, op, node):
        self.name = name
        self.op = op
        self.node = node

    def __repr__(self):
        return f'({self.name}  {self.op} {self.node})'


class TerneryNode:
    def __init__(self, condition, value_if_true, value_if_false):
        self.condition = condition
        self.value_if_true = value_if_true
        self.value_if_false = value_if_false

    def __repr__(self):
        return f'if({self.condition}) then ({self.value_if_true}) else ({self.value_if_false})'


class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

    def __repr__(self):
        return f'{self.var_name_tok}'


class FuncCallNode:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f'call {self.name}({self.arguments})'


class ExprListNode:
    def __init__(self,expressions):
        self.expressions = expressions

    def __repr__(self):
        return f'{self.expressions}'

#результат парсеру
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
#парсер
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def retreat(self):
        self.tok_idx -= 1
        if self.tok_idx > 0:
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.program()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxBungle("Error"))
        return res



    def program(self):
        res = ParseResult()
        func_list=[]

        while self.current_tok.type != TT_EOF:
            func = res.register(self.func())
            if res.error: return res
            func_list.append(func)

        return res.success(ProgramNode(func_list))

    def func(self):
        res = ParseResult()
        if self.current_tok.type in (TT_TYPE_FLOAT,TT_TYPE_INT):
            type_ = self.current_tok
            res.register(self.advance())
        else:
            return res.failure(InvalidSyntaxBungle('Expected type'))

        if self.current_tok.type == TT_IDENTIFIER:
            name_of_func = self.current_tok
            res.register(self.advance())
        else:
            return res.failure(InvalidSyntaxBungle('Expected identefier'))

        if self.current_tok.type == TT_LPAREN:
            res.register(self.advance())
        else:
            return res.failure(InvalidSyntaxBungle("Expected '('"))

        decl_list = res.register(self.decl_list())
        if res.error: return res

        if self.current_tok.type == TT_RPAREN:
            res.register(self.advance())
        else:
            return res.failure(InvalidSyntaxBungle("Expected ')' or type"))

        if self.current_tok.type == TT_LBLOCK:
            res.register(self.advance())
        else:
            return res.failure(InvalidSyntaxBungle("Expected '{'"))

        stmt_list = res.register(self.stmt_list())
        if res.error: return res

        if self.current_tok.type == TT_RBLOCK:
            res.register(self.advance())
            return res.success(FuncNode(type_, decl_list, name_of_func, stmt_list))
        else:
            return res.failure(InvalidSyntaxBungle("Expected '}'"))

    def decl_list(self):
        res = ParseResult()
        decl_list = []

        if self.current_tok.type in (TT_TYPE_FLOAT, TT_TYPE_INT):
            decl = res.register(self.decl())
            if res.error: return res
            decl_list.append(decl)
            while self.current_tok.type == TT_COMMA:
                res.register(self.advance())
                decl = res.register(self.decl())
                if res.error: return res
                decl_list.append(decl)

        return res.success(DeclListNode(decl_list))

    def decl(self):
        res = ParseResult()
        if self.current_tok.type in (TT_TYPE_INT, TT_TYPE_FLOAT):
            type_ = self.current_tok
            res.register(self.advance())
            if self.current_tok.type == TT_IDENTIFIER:
                ID = self.current_tok
                res.register(self.advance())
                return res.success(DeclarationNode(type_ , ID))
            else:
                return res.failure(InvalidSyntaxBungle("Expected identifier"))
        else:
            return res.failure(InvalidSyntaxBungle("Expected type"))

    def stmt_list(self):
        res = ParseResult()
        stmt_list = []

        while self.current_tok.type != TT_RBLOCK:
            stmt = res.register(self.stmt())
            if res.error: return res
            stmt_list.append(stmt)

        return res.success(StmtListNode(stmt_list))

    def stmt(self):
        res = ParseResult()
        if self.current_tok.matches(TT_KEYWORD, 'return'):
            res.register(self.advance())
            expr = res.register(self.cond_expr())
            if res.error: return res
            if self.current_tok.type == TT_SEMICOLON:
                res.register(self.advance())
                return res.success(ReturnNode(expr))
            else:
                return res.failure(InvalidSyntaxBungle("Expected ';' or invalid action"))

        if self.current_tok.matches(TT_KEYWORD, 'do'):
            res.register(self.advance())
            if self.current_tok.type == TT_LBLOCK:
                res.register(self.advance())
                stmt_list = res.register(self.stmt_list())
                if res.error: return res
                if self.current_tok.type == TT_RBLOCK:
                    res.register(self.advance())
                    if self.current_tok.matches(TT_KEYWORD, 'while'):
                        res.register(self.advance())
                        expr = res.register(self.cond_expr())
                        if res.error: return res
                        if self.current_tok.type == TT_SEMICOLON:
                            res.register(self.advance())
                            return res.success(DoWhileNode(stmt_list, expr))
                        else:
                            return res.failure(InvalidSyntaxBungle("Expected ';'"))
                    else:
                        return res.failure(InvalidSyntaxBungle("Expected keyword 'while'"))
                else:
                    return res.failure(InvalidSyntaxBungle("Expected '}'"))
            else:
                return res.failure(InvalidSyntaxBungle("Expected '{'"))

        if self.current_tok.matches(TT_KEYWORD, 'if'):
            res.register(self.advance())
            expr = res.register(self.cond_expr())
            if res.error: return res
            if self.current_tok.type == TT_LBLOCK:
                res.register(self.advance())
                stmt_list_if = res.register(self.stmt_list())
                if res.error: return res
                if self.current_tok.type == TT_RBLOCK:
                    res.register(self.advance())
                    if self.current_tok.matches(TT_KEYWORD, 'else'):
                        res.register(self.advance())
                        if self.current_tok.type == TT_LBLOCK:
                            res.register(self.advance())
                            stmt_list_else = res.register(self.stmt_list())
                            if res.error: return res
                            if self.current_tok.type == TT_RBLOCK:
                                res.register(self.advance())
                                if self.current_tok.type == TT_SEMICOLON:
                                    res.register(self.advance())
                                    return res.success(IfElseNode(expr, stmt_list_if, stmt_list_else))
                                else:
                                    return res.failure(InvalidSyntaxBungle("Expected ';'"))
                            else:
                                return res.failure(InvalidSyntaxBungle("Expected '}'"))
                        else:
                            return res.failure(InvalidSyntaxBungle("Expected '{'"))
                    else:
                        return res.failure(InvalidSyntaxBungle("Expected 'else'"))
                else:
                    return res.failure(InvalidSyntaxBungle("Expected '}'"))
            else:
                return res.failure(InvalidSyntaxBungle("Expected '{'"))

        if self.current_tok.matches(TT_KEYWORD, 'while'):
            res.register(self.advance())
            expr = res.register(self.cond_expr())
            if res.error: return res
            if self.current_tok.type == TT_LBLOCK:
                res.register(self.advance())
                stmt_list = res.register(self.stmt_list())
                if res.error: return res
                if self.current_tok.type == TT_RBLOCK:
                    res.register(self.advance())
                    if self.current_tok.type == TT_SEMICOLON:
                        res.register(self.advance())
                        return res.success(WhileNode(expr, stmt_list))
                    else:
                        return res.failure(InvalidSyntaxBungle("Expected ';'"))
                else:
                    return res.failure(InvalidSyntaxBungle("Expected '}'"))
            return res.failure(InvalidSyntaxBungle("Expected '{'"))

        if self.current_tok.matches(TT_KEYWORD, 'break'):
            res.register(self.advance())
            if self.current_tok.type == TT_SEMICOLON:
                res.register(self.advance())
                return res.success(BreakNode())
            else:
                return res.failure(InvalidSyntaxBungle("Expected ';'"))

        if self.current_tok.type in (TT_TYPE_INT, TT_TYPE_FLOAT):
            type = self.current_tok.type
            res.register(self.advance())
            if self.current_tok.type == TT_IDENTIFIER:
                ID = self.current_tok
                res.register(self.advance())
                if self.current_tok.type == TT_EQ:
                    res.register(self.advance())
                    expr = res.register(self.cond_expr())
                    if res.error: return res
                    if self.current_tok.type == TT_SEMICOLON:
                        res.register(self.advance())
                        return res.success(VarAssignNode(type, ID, expr))
                    else:
                        return res.failure(InvalidSyntaxBungle("Expected ';' or invalid action"))
                elif self.current_tok.type == TT_SEMICOLON:
                    res.register(self.advance())
                    return res.success(VarAssignNullNode(type, ID))
                else:
                    return res.failure(InvalidSyntaxBungle("Expected '=' or ';'"))

            else:
                return res.failure(InvalidSyntaxBungle("Expected identifier"))

        else:
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_SEMICOLON:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxBungle("Expected ';'"))

    def expr_list(self):
        res = ParseResult()
        expr_list = []

        if self.current_tok.type != TT_RPAREN:
            expr = res.register(self.expr())
            if res.error: return res
            expr_list.append(expr)
            while self.current_tok.type == TT_COMMA:
                res.register(self.advance())
                expr = res.register(self.expr())
                if res.error: return res
                expr_list.append(expr)

        return res.success(ExprListNode(expr_list))

    def expr(self):
        res = ParseResult()
        if self.current_tok.type == TT_IDENTIFIER:
            ID = self.current_tok
            res.register(self.advance())
            if self.current_tok.type in (TT_EQ, TT_DIV_EQ):
                op = self.current_tok
                res.register(self.advance())
                expr = res.register(self.expr())
                if res.error: return res
                return res.success(AssignNode(ID, op, expr))
            else:
                res.register(self.retreat())
                cond_expr = res.register(self.cond_expr())
                if res.error: return res
                return res.success(cond_expr)
        else:
            cond_expr = res.register(self.cond_expr())
            if res.error: return res
            return res.success(cond_expr)

    def cond_expr(self):
        res = ParseResult()
        bit_or = res.register(self.bit_or())
        if res.error: return res
        if self.current_tok.type == TT_QM:
            res.register(self.advance())
            expr1 = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_COLON:
                res.register(self.advance())
                expr2 = res.register(self.expr())
                if res.error: return res
                return res.success(TerneryNode(bit_or, expr1, expr2))
            else:
                return res.failure(InvalidSyntaxBungle("Expected ':'"))
        else:
            return res.success(bit_or)

    def bit_or(self):
        return self.bin_op(self.not_equas, TT_BIT_OR)

    def not_equas(self):
        return self.bin_op(self.add, (TT_GT, TT_LT))

    def add(self):
        return self.bin_op(self.term, TT_MINUS)

    def term(self):
        return self.bin_op(self.factor, (TT_DIV, TT_MUL, TT_PROC))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in TT_MINUS:
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT_DEC_NUM, TT_FLOAT_NUMBER, TT_INT_OCT_NUMBER):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register(self.advance())
            if self.current_tok.type == TT_LPAREN:
                res.register(self.advance())

                expr_list = res.register(self.expr_list())
                if res.error: return res

                if self.current_tok.type == TT_RPAREN:
                    res.register(self.advance())
                    return res.success(FuncCallNode(tok, expr_list))
                else:
                    return res.failure(InvalidSyntaxBungle("Expected ')'"))
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxBungle("Expected ')'"))

        elif tok.type == TT_INVALID_NUMBER:
            return res.failure(InvalidSyntaxBungle("Invalid number"))
        return res.failure(InvalidSyntaxBungle("Expected number or invalid expressions"))


    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left)
