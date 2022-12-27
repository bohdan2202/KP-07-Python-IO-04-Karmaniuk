
# пимилочки


class Bungle:
    def __init__(self, names_error, details):
        self.error_name = names_error
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        return result


class IllegalCharBungle(Bungle):
    def __init__(self, details):
        super().__init__('*помилочка*-Illegal Character', details)


class InvalidSyntaxBungle(Bungle):
    def __init__(self, details=''):
        super().__init__('*помилочка*-Invalid Syntax', details)


class NameBungle(Bungle):
    def __init__(self, details):
        super().__init__('*помилочка*-NameError', details)

class TypeBungle(Bungle):
    def __init__(self, details):
        super().__init__('*помилочка*-TypeError', details)

class MainBungle(Bungle):
    def __init__(self, details):
        super().__init__('*помилочка*-MainError', details)