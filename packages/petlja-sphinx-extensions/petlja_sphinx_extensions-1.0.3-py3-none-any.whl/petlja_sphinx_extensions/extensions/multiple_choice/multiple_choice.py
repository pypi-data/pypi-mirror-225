__author__ = 'petlja'

from docutils import nodes
from docutils.parsers.rst import Directive, directives


def setup(app):
    app.add_css_file('multiple-choice.css')
    app.add_js_file('multiple-choice.js')
    app.add_directive('mchoice', MchoiceDirective)
    app.add_node(MchoiceNode, html=(visit_node, depart_node))
    app.add_node(AnswerNode, html=(visit_answer_node, depart_answer_node))
    app.add_node(QuestionNode, html=(visit_question_node, depart_question_node))



TEMPLATE_START = '''
    <div class="course-box course-box-question course-content petlja-problem-box choice-question">
        <div class="image-background"></div>
        <div class="petlja-problem-box-icon-holder"> </div>
        <img src="../_static/qchoice-img.svg" class="petlja-problem-image qchoice-image" />
    <multiple-choice correct-answers="%(correct)s">
    '''


TEMPLATE_END = '''
      </multiple-choice>
    </div>
    '''

TEMPLATE_START_ANSWER = '''<answer>'''
TEMPLATE_END_ANSWER =   '''</answer>  '''

TEMPLATE_START_QUESTION = '''<question>''' 
TEMPLATE_END_QUESTION =   '''</question>  '''

class AnswerNode(nodes.General, nodes.Element):
    def __init__(self):
        super(AnswerNode, self).__init__()

class QuestionNode(nodes.General, nodes.Element):
    def __init__(self):
        super(QuestionNode, self).__init__()
    
class MchoiceNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(MchoiceNode, self).__init__()
        self.content = content

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
        answer_nodes = []
        for i in range(1, 7):
            answer_label = f'answer{i}'
            if answer_label in self.options:
                answer_node = AnswerNode()
                self.state.nested_parse([self.options[answer_label]], self.content_offset, answer_node)
                answer_nodes.append(answer_node)

        qchoice = QuestionNode()
        self.state.nested_parse(self.content, self.content_offset, qchoice)

        mchoice_node = MchoiceNode(self.options)
        mchoice_node.children.append(qchoice)
        mchoice_node.children += answer_nodes

        return [mchoice_node]
    

    

def visit_question_node(self, node):
    node.delimiter = "_start__{}_".format("question")
    self.body.append(node.delimiter)
    res = TEMPLATE_START_QUESTION
    self.body.append(res)

def depart_question_node(self, node):
    self.body.remove(node.delimiter)
    res = TEMPLATE_END_QUESTION
    self.body.append(res)


def visit_answer_node(self, node):
    node.delimiter = "_start__{}_".format("answer")
    self.body.append(node.delimiter)
    res = TEMPLATE_START_ANSWER
    self.body.append(res)

def depart_answer_node(self, node):
    res = TEMPLATE_END_ANSWER
    self.body.append(res)
    self.body.remove(node.delimiter)
    
def visit_node(self, node):
    node.delimiter = "_start__{}_".format("node")
    self.body.append(node.delimiter)
    self.body.append(TEMPLATE_START % node.content)


def depart_node(self, node):
    self.body.append(TEMPLATE_END)
    self.body.remove(node.delimiter)
