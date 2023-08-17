__author__ = 'petlja'

from docutils import nodes
from docutils.parsers.rst import Directive, directives


def setup(app):
    app.add_css_file('multiple-choice.css')
    app.add_js_file('multiple-choice.js')
    app.add_directive('mchoice', MchoiceDirective)
    app.add_node(MchoiceNode, html=(visit_note_node, depart_note_node))



TEMPLATE_START = '''
    <div class="course-box course-box-question course-content petlja-problem-box choice-question">
        <div class="image-background"></div>
        <div class="petlja-problem-box-icon-holder"> </div>
        <img src="../_static/qchoice-img.svg" class="petlja-problem-image qchoice-image" />
    <multiple-choice question="%(question)s" %(answers)s correct-answers="%(correct)s">
    '''


TEMPLATE_END = '''
      </multiple-choice>
    </div>
    '''


class MchoiceNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(MchoiceNode, self).__init__()
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


class MchoiceDirective(Directive):

    required_arguments = 0
    optional_arguments = 0
    has_content = True
    option_spec = {}
    option_spec.update({
        'answer1':directives.unchanged,
        'answer2':directives.unchanged,
        'answer3':directives.unchanged,
        'answer4':directives.unchanged,
        'answer5':directives.unchanged,
        'answer6':directives.unchanged,
        'correct': directives.unchanged,
    })

    def run(self):
        """
        generate html to include note box.
        :param self:
        :return:
        """

        self.options['question'] = "\n".join(self.content)
        self.content = []
        self.options['answers'] = ""
        for i in range(1, 7):
            answer_label = f'answer{i}'
            if answer_label in self.options:
                self.options['answers'] += f' {answer_label}="{self.options[answer_label]}" '
        
        innode = MchoiceNode(self.options)
        self.state.nested_parse(self.content, self.content_offset, innode)

        return [innode]
