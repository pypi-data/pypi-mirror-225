import gast
from tensorflow.python.autograph.pyct import errors as errors

class UnsupportedFeaturesChecker(gast.NodeVisitor):
    def visit_Attribute(self, node) -> None: ...
    def visit_For(self, node) -> None: ...
    def visit_While(self, node) -> None: ...
    def visit_Yield(self, node) -> None: ...
    def visit_YieldFrom(self, node) -> None: ...

def verify(node) -> None: ...
