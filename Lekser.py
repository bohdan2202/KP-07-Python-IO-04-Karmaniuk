# токін
from Unchanging import *
from Bungle import *
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer:
    def __init__(self, tekst):
        self.tekst = tekst
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.tekst[self.pos] if self.pos < len(self.tekst) else None

    @property
    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \r\n':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '-':
                token, error = self.make_minus()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '/':
                token, error = self.make_div()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '*':
                token, error = self.make_mul()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                token, error = self.make_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '>':
                token, error = self.make_greater()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '<':
                token, error = self.make_lower()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '|':
                token, error = self.make_or()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '%':
                tokens.append(Token(TT_PROC))
                self.advance()
            elif self.current_char == '?':
                tokens.append(Token(TT_QM))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBLOCK))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBLOCK))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_SEMICOLON))
                self.advance()
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharBungle("'" + char + "'")

        tokens.append(Token(TT_EOF))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        oct_count = 0

        while self.current_char is not None and self.current_char in DIGITS + 'o.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            elif self.current_char == 'o' and num_str == '0':
                if oct_count == 1: break
                oct_count += 1
                num_str += 'o'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count != 0:
            return Token(TT_FLOAT_NUMBER, float(num_str))
        elif oct_count != 0 and '8' not in num_str and '9' not in num_str:
            return Token(TT_INT_OCT_NUMBER, int(num_str, 8))
        elif dot_count == 0 and oct_count == 0 and ('o' not in num_str):
            return Token(TT_INT_DEC_NUM, int(num_str))
        else:
            return Token(TT_INVALID_NUMBER)

    def make_identifier(self):
        id_str = ''

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        if id_str == 'float':
            tok_type = TT_TYPE_FLOAT
            return Token(tok_type)
        elif id_str == 'int':
            tok_type = TT_TYPE_INT
            return Token(tok_type)
        elif id_str in KEYWORDS:
            tok_type = TT_KEYWORD
            return Token(tok_type, id_str)
        else:
            tok_type = TT_IDENTIFIER
            return Token(tok_type, id_str)

    def make_equals(self):
        tok_type = TT_EQ
        self.advance()

        if self.current_char == '=':
            self.advance()
            return None, IllegalCharBungle("'=='")

        return Token(tok_type), None

    def make_minus(self):
        tok_type = TT_MINUS
        self.advance()

        if self.current_char == '=':
            self.advance()
            return None, IllegalCharBungle("'-='")

        return Token(tok_type), None

    def make_div(self):
        tok_type = TT_DIV
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_DIV_EQ), None

        return Token(tok_type), None

    def make_mul(self):
        tok_type = TT_MUL
        self.advance()

        if self.current_char == '=':
            self.advance()
            return None, IllegalCharBungle("'*='")

        return Token(tok_type), None

    def make_greater(self):
        tok_type = TT_GT
        self.advance()

        if self.current_char == '=':
            self.advance()
            return None, IllegalCharBungle("'>='")

        return Token(tok_type), None

    def make_or(self):
        tok_type = TT_BIT_OR
        self.advance()

        if self.current_char == '|':
            self.advance()
            return None, IllegalCharBungle("'||'")

        return Token(tok_type), None

    def make_lower(self):
        tok_type = TT_LT
        self.advance()

        if self.current_char == '=':
            self.advance()
            return None, IllegalCharBungle("'<='")

        return Token(tok_type), None