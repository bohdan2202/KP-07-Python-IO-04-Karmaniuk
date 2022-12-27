from Unchanging import *
from Bungle import *
import sys



class Interpreter:
    def __init__(self):
        self.itr = 0
        self.advance()
        self.main = ''
        self.code = ''
        self.data = ''
        self.data_var = ''
        self.current_func = ''
        self.func_call = ''
        self.var_list = []
        self.func_list = []
        self.decl_list = []
        self.func_in_func = False

    def advance(self):
        self.itr += 1

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')



    def op_div(self, left, right):
        result = 'O' + str(self.itr)
        code = r"""    ;дiлемo двa числа
    mov eax, {}
    mov ecx, {}
    cdq
    idiv ecx
    mov {}, eax
""".format(left, right, result)
        if self.current_func == 'main': self.main += code
        else: self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result

    def op_proc(self, left, right):
        result = 'O' + str(self.itr)
        code = r"""    ;залишок дiлення двох чисел
    mov eax, {}
    mov ecx, {}
    cdq
    idiv ecx
    mov {}, edx
""".format(left, right, result)
        if self.current_func == 'main':
            self.main += code
        else:
            self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result

    def op_mul(self, left, right):
        result = 'O' + str(self.itr)
        code = r"""    ;примноження двох цифр
    mov eax, {}
    mov ebx, {}
    mul ebx
    mov {}, eax
""".format(left, right, result)
        if self.current_func == 'main': self.main += code
        else: self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result

    def op_minus(self, left, right):
        result = 'O' + str(self.itr)
        code = r"""    ;відiймання двох чисел
    mov eax, {}
    mov ebx, {}
    sub eax, ebx
    mov {}, eax
""".format(left, right, result)
        if self.current_func == 'main':
            self.main += code
        else:
            self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result

    def op_gt(self, left, right):
        result = 'O' + str(self.itr)
        greater = '@GREATER' + str(self.itr)
        exit = '@EXIT_GT' + str(self.itr)
        code = r"""    ;робимо порiвняння двох чисел >    
    mov eax, {0}
    mov ebx, {1}
    cmp eax, ebx
    jg {3}
    mov eax, 0
    mov {2}, eax
    jmp {4}
    {3}: 
    mov eax, 1
    mov {2}, eax
    {4}:
""".format(left, right, result, greater, exit)
        if self.current_func == 'main': self.main += code
        else: self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result

    def op_lt(self, left, right):
        result = 'O' + str(self.itr)
        lower = '@LOWER' + str(self.itr)
        exit = '@EXIT_LT' + str(self.itr)
        code = r"""    ;зіставлення двох чисел     
    mov eax, {0}
    mov ebx, {1}
    cmp eax, ebx
    jl {3}
    mov eax, 0
    mov {2}, eax
    jmp {4}
    {3}: 
    mov eax, 1
    mov {2}, eax
    {4}:
""".format(left, right, result, lower, exit)
        if self.current_func == 'main':
            self.main += code
        else:
            self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result

    def op_bit_or(self, left, right):
        result = 'O' + str(self.itr)
        code = r"""    ;побiтове АБО двох цифр
    mov eax, {}
    mov ebx, {}
    or eax, ebx
    mov {}, eax
""".format(left, right, result)
        if self.current_func == 'main':
            self.main += code
        else:
            self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result

    def un_op_minus(self, number):
        result = 'O' + str(self.itr)
        code = r"""    ;унaрний мінус:   
    mov eax, {}
    neg eax
    mov {}, eax
""".format(number, result)
        if self.current_func == 'main': self.main += code
        else: self.code += code
        self.data += r"""{} dd 0
""".format(result)
        self.advance()
        return result


    def visit_ProgramNode(self, node):
        for function in node.functions:
            self.visit(function)

        if 'main' not in self.func_list:
            print('Error: ' + MainBungle(f"undefined reference to main()").as_string())
            input()
            sys.exit(0)

        if self.func_in_func:
            self.data_var = r""";перелік перемінних факторіал
n_factorial dd 0
fact_factorial dd 1
ret_factorial dd 1
;список змінних main
n_main dd 0
ret_main dd 0
"""
            self.data += 'O1 dd 0\n'
            self.code = r"""factorial proc
    ;зітавлення двох цифр <
    mov eax, n_factorial
    mov ebx, 1
    cmp eax, ebx
    jl @LOWER1
    mov eax, 0
    mov O1, eax
    jmp @EXIT_LT1
    @LOWER1:
    mov eax, 1
    mov O1, eax
    @EXIT_LT1:
    ;if
    mov eax, O1
    mov ebx, 0
    cmp eax, ebx
    jne @TRUE1
    ;false
    ;помножування двох чисел
    mov eax, fact_factorial
    mov ebx, n_factorial
    mul ebx
    mov fact_factorial, eax
    ;віднімання двох чисел
    mov eax, n_factorial
    mov ebx, 1
    sub eax, ebx
    mov n_factorial, eax
    ;повернення наслідку функції
    mov eax, fact_factorial
    mov ret_factorial, eax
    call factorial
    @TRUE1:
    ;true
    ret
factorial endp
"""

        code = self.code
        main = self.main
        data = self.data
        data_var = self.data_var
        asmtext = r""".386
.model flat, stdcall
option casemap:none

include \masm32\include\masm32rt.inc

.data
{}
{}  
.code
start:
{}
{}
invoke main
invoke ExitProcess, 0
END start""".format(data_var, data, main, code)
        return asmtext

    def visit_FuncNode(self, node):
        name = node.name.value
        self.func_list.append(name)
        self.current_func = name

        self.data_var += f';перелік несталих {name}\n'

        code = f'\n{name} proc\n'
        if self.current_func == 'main': self.main += code
        else: self.code +=code

        self.visit(node.decl_list)

        self.visit(node.node)

        if name == 'main': self.main +=f'    fn MessageBox,0,str$(ret_main), "Return", MB_OK\n'

        code = f'    ret\n{name} endp\n'
        if self.current_func == 'main': self.main += code
        else: self.code +=code

    def visit_DeclListNode(self, node):
        list = []
        for declaration in node.declarations:
            node = self.visit(declaration)
            list.append(node)
        if self.current_func == 'main' and len(list) !=0:
            print('Error: ' + TypeBungle(f"main() takes only zero arguments").as_string())
            input()
            sys.exit(0)
        self.decl_list.append(list)

    def visit_DeclarationNode(self, node):
        var = node.name.value
        var_func = f'{var}_{self.current_func}'
        if var_func in self.var_list:
            print('Error: ' + NameBungle(f"'{var}' was identefined in {self.current_func}() function").as_string())
            input()
            sys.exit(0)
        else:
            self.var_list.append(var_func)
            self.data_var += f'{var_func} dd 0\n'
        return var_func

    def visit_StmtListNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_DoWhileNode(self, node):
        do = '@DO_WHILE' + str(self.itr)
        self.advance()
        code = r"""    ;do
    {}:
""".format(do)
        if self.current_func == 'main': self.main += code
        else: self.code += code
        self.visit(node.node_stmt)

        code = '    ;while\n'
        if self.current_func == 'main': self.main += code
        else: self.code += code
        expr = self.visit(node.node_expr)

        code = r"""    mov eax, {0}
    mov ebx, 0
    cmp eax, ebx
    jne {1}
    @BREAK:
""".format(expr, do)
        if self.current_func == 'main': self.main += code
        else: self.code += code

    def visit_WhileNode(self, node):
        while_do = '@WHILEDO' + str(self.itr)
        exit = '@EXIT_WHILE' + str(self.itr)
        self.advance()
        code = f'    ;while\n    {while_do}:\n'
        if self.current_func == 'main': self.main += code
        else: self.code += code

        expr = self.visit(node.node_expr)
        code = r"""    mov eax, {0}
    mov ebx, 0
    cmp eax, ebx
    je {1}
""".format(expr, exit)
        if self.current_func == 'main': self.main += code
        else: self.code += code

        self.visit(node.node_stmt)
        code = r"""    jmp {}
    {}:
""".format(while_do, exit)
        if self.current_func == 'main': self.main += code
        else: self.code += code

    def visit_IfElseNode(self, node):
        true_ = '@TRUE' + str(self.itr)
        exit = '@EXIT_IF' + str(self.itr)
        self.advance()

        condition = self.visit(node.node_expr)
        code = r"""    ;if
    mov eax, {0}
    mov ebx, 0
    cmp eax, ebx
    jne {1}
    ;false
""".format(condition, true_)
        if self.current_func == 'main':
            self.main += code
        else:
            self.code += code

        false_result = self.visit(node.node_stmt_else)
        code = r"""    jmp {}
    {}: 
    ;true
""".format(exit, true_)
        if self.current_func == 'main':
            self.main += code
        else:
            self.code += code

        true_result = self.visit(node.node_stmt_if)
        code = r"""    {}:
""".format(exit)
        if self.current_func == 'main':
            self.main += code
        else:
            self.code += code

    def visit_VarAssignNode(self, node):
        var = node.name.value
        var_func = f'{var}_{self.current_func}'
        node = self.visit(node.node)

        if var_func in self.var_list:
            print('Error: ' + NameBungle(f"'{var}' was identefined in {self.current_func}() function").as_string())
            input()
            sys.exit(0)

        else:
            self.var_list.append(var_func)
            self.data_var += f'{var_func} dd 0\n'

            code = r"""    ;внесення значення в перемінну
    mov eax, {}
    mov {}, eax
""".format(node, var_func)
            if self.current_func == 'main': self.main += code
            else: self.code += code

    def visit_VarAssignNullNode(self, node):
        var = node.name.value
        var_func = f'{var}_{self.current_func}'

        if var_func in self.var_list:
            print('Error: ' + NameBungle(f"'{var}' was identefined in {self.current_func}() function").as_string())
            input()
            sys.exit(0)

        else:
            self.var_list.append(var_func)
            self.data_var += f'{var_func} dd 0\n'

    def visit_ReturnNode(self, node):
        return_ = self.visit(node.node)
        ret_func = f'ret_{self.current_func}'

        if (ret_func not in self.var_list):
            self.var_list.append(ret_func)
            self.data_var += f'{ret_func} dd 0\n'

        code = r"""    ;повернення наслідок функції
    mov eax, {}
    mov {}, eax
""".format(return_, ret_func)
        if self.current_func == 'main': self.main += code
        else: self.code += code

    def visit_BreakNode(self, node):
        code = r"""    ;припинення циклу
    jmp @BREAK
"""
        if self.current_func == 'main': self.main += code
        else: self.code += code

    def visit_AssignNode(self, node):
        code = ''
        var = node.name.value
        var_func = f'{var}_{self.current_func}'
        op = node.op.type
        node = self.visit(node.node)
        if var_func in self.var_list:
            if op == TT_DIV_EQ:
                code = r"""    ;ділення і занести значення в змінну
    mov eax, {0}
    mov ecx, {1}
    cdq
    idiv ecx
    mov {0}, eax
""".format(var_func, node)

            if op == TT_EQ:
                code = r"""    ;занести значення в змінну
    mov eax, {}
    mov {}, eax
""".format(node, var_func)

            if self.current_func == 'main': self.main += code
            else: self.code += code

            return var_func

        else:
            print('Error: ' + NameBungle(f"'{var}' is not defined in {self.current_func}() function").as_string())
            input()
            sys.exit(0)

    def visit_TerneryNode(self, node):
        true_ = '@TRUE' + str(self.itr)
        exit = '@EXIT_IF' + str(self.itr)
        result = 'Ans' + str(self.itr)
        self.data += r"""{} dd 0
""".format(result)
        condition = self.visit(node.condition)
        code = r"""    ;if
    mov eax, {0}
    mov ebx, 0
    cmp eax, ebx
    jne {1}
    ;false
""".format(condition, true_)
        if self.current_func == 'main': self.main += code
        else: self.code += code

        false_result = self.visit(node.value_if_false)
        code = r"""    ;виведення неправда(false)   
    mov eax, {}
    mov {}, eax
    jmp {}
    {}: 
    ;true
""".format(false_result, result, exit, true_)
        if self.current_func == 'main': self.main += code
        else: self.code += code

        true_result = self.visit(node.value_if_true)
        code = r"""    ;виведення правди(true)
    mov eax, {}
    mov {}, eax
    {}:
""".format(true_result, result, exit)
        if self.current_func == 'main': self.main += code
        else: self.code += code

        self.advance()
        return result

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_tok.type == TT_DIV:
            result = self.op_div(left, right)
            return result
        elif node.op_tok.type == TT_PROC:
            result = self.op_proc(left, right)
            return result
        elif node.op_tok.type == TT_MUL:
            result = self.op_mul(left, right)
            return result
        elif node.op_tok.type == TT_GT:
            result = self.op_gt(left, right)
            return result
        elif node.op_tok.type == TT_LT:
            result = self.op_lt(left, right)
            return result
        elif node.op_tok.type == TT_BIT_OR:
            result = self.op_bit_or(left, right)
            return result
        elif node.op_tok.type == TT_MINUS:
            result = self.op_minus(left, right)
            return result
        else:
            pass

    def visit_UnaryOpNode(self, node):
        number = self.visit(node.node)

        if node.op_tok.type == TT_MINUS:
            result = self.un_op_minus(number)
            return result
        else:
            pass

    def visit_NumberNode(self, node):
        numb = f'{int(node.tok.value)}'
        return numb

    def visit_VarAccessNode(self, node):
        var = node.var_name_tok.value
        var_func = f'{var}_{self.current_func}'
        if var_func in self.var_list:
            return var_func
        else:
            print('Error: ' + NameBungle(f"'{var}' is not defined").as_string())
            input()
            sys.exit(0)

    def visit_FuncCallNode(self, node):
        func = node.name.value
        self.func_call = func
        ret_func = f'ret_{func}'
        if func == self.current_func:
            self.func_in_func = True

        if func in self.func_list:
            self.visit(node.arguments)

            code = f'    call {func}\n'
            if self.current_func == 'main': self.main += code
            else: self.code += code

            return ret_func

        else:
            print('Error: ' + NameBungle(f"{func}() is not defined").as_string())
            input()
            sys.exit(0)

    def visit_ExprListNode(self, node):
        list = self.decl_list[self.func_list.index(f'{self.func_call}')]
        index = 0

        k = 0
        for i in node.expressions:
            k+=1

        if k != len(list):
            print('Error: ' + NameBungle(
                f"{self.func_call}() takes {len(list)} positional arguments but {k} were given").as_string())
            input()
            sys.exit(0)

        for expression in node.expressions:
            node = self.visit(expression)
            code = r"""    ;записувати значення в перемінну
    mov eax, {}
    mov {}, eax
""".format(node, list[index])
            if self.current_func == 'main': self.main += code
            else: self.code += code
            index += 1