from tensorflow.python.autograph.core import converter as converter
from tensorflow.python.autograph.lang import directives as directives
from tensorflow.python.autograph.pyct import templates as templates

class SliceTransformer(converter.Base):
    def visit_Assign(self, node): ...
    def visit_Subscript(self, node): ...

def transform(node, ctx): ...
