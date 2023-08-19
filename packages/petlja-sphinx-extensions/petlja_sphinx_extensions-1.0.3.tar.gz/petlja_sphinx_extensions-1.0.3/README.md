# Petlja Sphinx Extension

The Petlja Sphinx Extension is a project designed to enhance the capabilities of Sphinx, a widely used documentation generation tool. This extension provides custom directives that are particularly useful for creating e-learning content within your Sphinx documentation.

## Directives

### `mchoice` Directive

The `mchoice` directive enables you to embed multiple-choice questions within your documentation. This is particularly handy for creating interactive educational content. Here's an example of how to use this directive:

```rst
.. mchoice::
   :answer1: Belgrade
   :answer2: Paris
   :answer3: Madrid
   :correct: 2

   What is the capital of France?
```

In this example, a multiple-choice question is created with three answer options, and the correct answer is set to "Paris".

### `fitb` Directive

The `fitb` directive allows you to insert fill-in-the-blank questions in your documentation. This is a great way to create interactive exercises. Here's an example of how to use this directive:

```rst
.. fitb::
   :answer: OpenAI

   The GPT-3 model is developed by |blank|. 
```

In this example, a fill-in-the-blank question is created where the answer is "OpenAI".

## Installation and Usage

To use the Petlja Sphinx Extension in your Sphinx project, follow these steps:

1. Install the extension using pip:

   ```
   pip install petlja-sphinx-extension
   ```

2. Add the extension to your Sphinx project's `conf.py` file:

   ```python
   extensions = [
       # ... other extensions ...
       'petlja_sphinx_extensions.extensions.multiple_choice',
       'petlja_sphinx_extensions.extensions.fill_in_the_blank',
   ]
   ```

3. Once the extension is enabled, you can start using the `mchoice` and `fitb` directives in your documentation files as demonstrated in the examples above.


This will render a fill-in-the-blank question where the answer is "Python".

Feel free to explore the capabilities of the Petlja Sphinx Extension to create engaging and interactive e-learning content within your Sphinx documentation.

## About

This project is maintained by Petlja and is aimed at enhancing the educational content creation experience using Sphinx. For more information about Petlja and its initiatives, please visit [Petlja's website](https://www.petlja.org).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

*Note: This readme is intended for PyPI distribution and provides a concise overview of the Petlja Sphinx Extension and its features.*