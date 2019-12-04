from .Scope import Scope


class SymbolTable:

    root_scope = None
    current_scope = None

    def __init__(self):
        self.root_scope = Scope(None)
        self.current_scope = self.root_scope

    def open_scope(self):
        self.current_scope = self.current_scope.open_scope()

    def close_scope(self):
        self.current_scope = self.current_scope.get_father_scope()
