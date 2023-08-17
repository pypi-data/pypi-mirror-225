__author__ = 'petlja'

from docutils import nodes
from docutils.parsers.rst import Directive, directives


def setup(app):
    app.add_css_file('fill-in-the-blank.css')
    app.add_js_file('fill-in-the-blank.js')
    app.add_directive('fitb', FIDBDirective)
    app.add_node(FIDBNode, html=(visit_note_node, depart_note_node))



TEMPLATE_START = '''
    <div class="course-box course-box-question course-content petlja-problem-box fitb-question">
        <div class="image-background"></div>
        <div class="petlja-problem-box-icon-holder"> </div>
        <img src="../_static/qchoice-img.svg" class="petlja-problem-image qchoice-image" />
    <fill-in-the-blank
    question="%(question)s"
    regex="%(answer)s">
    '''


TEMPLATE_END = '''
      </fill-in-the-blank>
    </div>
    '''


class FIDBNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(FIDBNode, self).__init__()
        self.note = content


def visit_note_node(self, node):
    node.delimiter = "_start__{}_".format("info")
    self.body.append(node.delimiter)
    res = TEMPLATE_START % node.note
    self.body.append(res)


def depart_note_node(self, node):
    res = TEMPLATE_END
    self.body.append(res)
    self.body.remove(node.delimiter)


class FIDBDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    has_content = True
    option_spec = {}
    option_spec.update({
    'answer': directives.unchanged,
    })

    def run(self):
        """
        generate html to include note box.
        :param self:
        :return:
        """

        self.options['question'] = "\n".join(self.content)
        print(self.options['answer'])
        self.content=[]
        innode = FIDBNode(self.options)
        self.state.nested_parse(self.content, self.content_offset, innode)

        return [innode]
    

