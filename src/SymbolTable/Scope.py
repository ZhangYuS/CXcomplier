class Scope:
    father_scope = None
    child_scopes = []

    def __init__(self, father_scope):
        self.father_scope = father_scope

    def open_scope(self):
        child_scope = Scope(self)
        self.child_scopes.append(child_scope)
        return child_scope

    def get_father_scope(self):
        return self.father_scope