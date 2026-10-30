"""
The grader's tests, one function per stub so that pytest -x
stops at one failure at a time.
"""
from markdown_compiler.util.line_functions import (
    compile_headers, compile_italic_star, compile_bold_stars, compile_images,
    compile_links,
)
from markdown_compiler import compile_lines


def test_headers():
    assert compile_headers('# This is the main header') == \
           '<h1> This is the main header</h1>'
    assert compile_headers('## This is a sub-header') == \
           '<h2> This is a sub-header</h2>'
    assert compile_headers('###### This is a sub-header') == \
           '<h6> This is a sub-header</h6>'
    assert compile_headers('      # this is not a header') == \
           '      # this is not a header'


def test_italic_star():
    assert compile_italic_star('*This is italic!* This is not italic.') == \
           '<i>This is italic!</i> This is not italic.'
    assert compile_italic_star('This is *italic*!') == \
           'This is <i>italic</i>!'
    assert compile_italic_star('This is not *italic!') == \
           'This is not *italic!'
    assert compile_italic_star('*') == '*'


def test_bold_stars():
    assert compile_bold_stars('**This is bold!** This is not bold.') == \
           '<b>This is bold!</b> This is not bold.'
    assert compile_bold_stars('This is **bold**!') == \
           'This is <b>bold</b>!'
    assert compile_bold_stars('This is not **bold!') == \
           'This is not **bold!'
    assert compile_bold_stars('**') == '**'


def test_images():
    assert compile_images('[Mike](https://x/y.png)') == \
           '[Mike](https://x/y.png)'
    assert compile_images('![Mike](https://x/y.png)') == \
           '<img src="https://x/y.png" alt="Mike" />'
    assert compile_images('an image: ![Mike](https://x/y.png)') == \
           'an image: <img src="https://x/y.png" alt="Mike" />'


def test_links_still_work():
    # compile_links was already implemented; the test exists so that a
    # patch to compile_images that breaks links is caught.
    assert compile_links('Click on the [page](https://x)!') == \
           'Click on the <a href="https://x">page</a>!'


def test_integration():
    # runs only after the four stubs above are all green
    assert compile_lines('This is **bold** _italic_ `code`.\n') == \
           '<p>\nThis is <b>bold</b> <i>italic</i> <code>code</code>.\n</p>'
