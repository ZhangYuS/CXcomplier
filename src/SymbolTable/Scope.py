from .Symbol import Symbol

class Scope:

    def __init__(self, father_scope):
        self.father_scope = father_scope
        self.child_scopes = []
        self.variables = dict()
        self.address = 0

    def open_scope(self):
        child_scope = Scope(self)
        self.child_scopes.append(child_scope)
        child_scope.address = self.address
        return child_scope

    def close_scope(self):
        self.father_scope.address = self.address
        return self.father_scope

    def open_function_scope(self):
        child_scope = Scope(self)
        self.child_scopes.append(child_scope)
        child_scope.address = 5
        return child_scope

    def close_function_scope(self):
        return self.father_scope, self.address

    def get_father_scope(self):
        return self.father_scope
