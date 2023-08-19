__author__ = 'petlja'

from docutils import nodes
from docutils.parsers.rst import Directive


def setup(app):
    app.add_css_file('notes.css')
    app.add_js_file('notes.js')

    app.add_directive('infonote', NoteDirective)
    app.add_directive('suggestionnote', NoteDirective)
    app.add_directive('learnmorenote', NoteDirective)
    app.add_directive('technicalnote', NoteDirective)
    app.add_directive('questionnote', QuestionNoteDirective)

    app.add_node(NoteNode, html=(visit_note_node, depart_note_node))
    app.add_node(QuestionNoteNode, html=(
        visit_question_note_node, depart_question_note_node))


TEMPLATE_START = """
    <div class="note-wrapper %(notetype)s-type">
        <div class="note-icon-holder"> </div>
        <img src="../_static/%(notetype)s-img.svg" class="note-image %(notetype)s-image" /> 
        <div class="course-content">
            
"""

TEMPLATE_END = """
    </div></div>
"""


class NoteNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(NoteNode, self).__init__()
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


class NoteDirective(Directive):

    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self):
        """
        generate html to include note box.
        :param self:
        :return:
        """

        self.options['source'] = "\n".join(self.content)
        self.options['notetype'] = self.name
        innode = NoteNode(self.options)
        self.state.nested_parse(self.content, self.content_offset, innode)

        return [innode]


TEMPLATE_START_Q = """
    <div class="note-wrapper questionnote-type">
        <div class="note-icon-holder"> </div>
        <img src="../_static/question-mark.png" class="note-image questionnote-image" /> 
        <div class="course-content">
"""

TEMPLATE_END_Q = """
    </div></div>
"""


class QuestionNoteNode(nodes.General, nodes.Element):
    def __init__(self, content):
        super(QuestionNoteNode, self).__init__()
        self.note = content


def visit_question_note_node(self, node):
    node.delimiter = "_start__{}_".format("info")
    self.body.append(node.delimiter)
    res = TEMPLATE_START_Q
    self.body.append(res)


def depart_question_note_node(self, node):
    res = TEMPLATE_END_Q
    self.body.append(res)
    self.body.remove(node.delimiter)


class QuestionNoteDirective(Directive):
    """
.. questionnote::
    """
    required_arguments = 0
    optional_arguments = 0
    has_content = True

    def run(self):
        """
        generate html to include note box.
        :param self:
        :return:
        """

        self.options['source'] = "\n".join(self.content)
        qnnode = QuestionNoteNode(self.options)
        self.state.nested_parse(self.content, self.content_offset, qnnode)

        return [qnnode]
