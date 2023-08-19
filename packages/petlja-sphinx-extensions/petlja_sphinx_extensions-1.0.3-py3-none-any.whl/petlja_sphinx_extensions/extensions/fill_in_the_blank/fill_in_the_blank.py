__author__ = 'petlja'

from docutils import nodes
from docutils.parsers.rst import Directive, directives


def setup(app):
    app.add_css_file('fill-in-the-blank.css')
    app.add_js_file('fill-in-the-blank.js')
    app.add_directive('fitb', FITBDirective)
    app.add_node(FITBNode, html=(visit_fitb_node, depart_fitb_node))



TEMPLATE_START = '''
    <div class="course-box course-box-question course-content petlja-problem-box fitb-question">
        <div class="image-background"></div>
        <div class="petlja-problem-box-icon-holder"> </div>
        <img src="../_static/qchoice-img.svg" class="petlja-problem-image qchoice-image" />
    <fill-in-the-blank
    regex="%(answer)s">
    '''


TEMPLATE_END = '''
      </fill-in-the-blank>
    </div>
    '''


class FITBNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(FITBNode, self).__init__()
        self.note = content


def visit_fitb_node(self, node):
    node.delimiter = "_start__{}_".format("info")
    self.body.append(node.delimiter)
    res = TEMPLATE_START % node.note
    self.body.append(res)


def depart_fitb_node(self, node):
    res = TEMPLATE_END
    self.body.append(res)
    self.body.remove(node.delimiter)


class FITBDirective(Directive):
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

        innode = FITBNode(self.options)
        self.state.nested_parse(self.content, self.content_offset, innode)

        return [innode]
    

