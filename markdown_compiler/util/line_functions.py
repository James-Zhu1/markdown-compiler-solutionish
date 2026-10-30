'''
Each function takes a single line and transforms it in some way.

Four functions are stubs -- they return their input unchanged and must
be implemented.  Five are already implemented and must not be touched.
'''


def _pair(line, delim, open_tag, close_tag):
    '''
    Replace each alternating pair of delim with open_tag/close_tag.

    >>> _pair('a*b*c', '*', '<i>', '</i>')
    'a<i>b</i>c'
    >>> _pair('a*b', '*', '<i>', '</i>')
    'a<i>b'
    '''
    out, i, opened = '', 0, False
    while i < len(line):
        if line[i:i + len(delim)] == delim:
            out += close_tag if opened else open_tag
            opened = not opened
            i += len(delim)
        else:
            out += line[i]
            i += 1
    return out


def compile_headers(line):
    '''
    Convert markdown headers into <h1>,<h2>,etc tags.

    >>> compile_headers('# This is the main header')
    '<h1> This is the main header</h1>'
    >>> compile_headers('## This is a sub-header')
    '<h2> This is a sub-header</h2>'
    >>> compile_headers('### This is a sub-header')
    '<h3> This is a sub-header</h3>'
    >>> compile_headers('#### This is a sub-header')
    '<h4> This is a sub-header</h4>'
    >>> compile_headers('##### This is a sub-header')
    '<h5> This is a sub-header</h5>'
    >>> compile_headers('###### This is a sub-header')
    '<h6> This is a sub-header</h6>'
    >>> compile_headers('      # this is not a header')
    '      # this is not a header'
    '''
    return line


def compile_italic_star(line):
    '''
    Convert "*italic*" into "<i>italic</i>".

    >>> compile_italic_star('*This is italic!* This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_star('*This is italic!*')
    '<i>This is italic!</i>'
    >>> compile_italic_star('This is *italic*!')
    'This is <i>italic</i>!'
    >>> compile_italic_star('This is not *italic!')
    'This is not *italic!'
    >>> compile_italic_star('*')
    '*'
    '''
    return line


def compile_italic_underscore(line):
    '''
    Convert "_italic_" into "<i>italic</i>".

    >>> compile_italic_underscore('_This is italic!_ This is not italic.')
    '<i>This is italic!</i> This is not italic.'
    >>> compile_italic_underscore('_This is italic!_')
    '<i>This is italic!</i>'
    >>> compile_italic_underscore('This is _italic_!')
    'This is <i>italic</i>!'
    >>> compile_italic_underscore('This is not _italic!')
    'This is not _italic!'
    >>> compile_italic_underscore('_')
    '_'
    '''
    return _pair(line, '_', '<i>', '</i>')


def compile_strikethrough(line):
    '''
    Convert "~~strikethrough~~" to "<ins>strikethrough</ins>".

    >>> compile_strikethrough('~~This is strikethrough!~~ This is not strikethrough.')
    '<ins>This is strikethrough!</ins> This is not strikethrough.'
    >>> compile_strikethrough('~~This is strikethrough!~~')
    '<ins>This is strikethrough!</ins>'
    >>> compile_strikethrough('This is ~~strikethrough~~!')
    'This is <ins>strikethrough</ins>!'
    >>> compile_strikethrough('This is not ~~strikethrough!')
    'This is not ~~strikethrough!'
    >>> compile_strikethrough('~~')
    '~~'
    '''
    return _pair(line, '~~', '<ins>', '</ins>')


def compile_bold_stars(line):
    '''
    Convert "**bold**" to "<b>bold</b>".

    >>> compile_bold_stars('**This is bold!** This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_stars('**This is bold!**')
    '<b>This is bold!</b>'
    >>> compile_bold_stars('This is **bold**!')
    'This is <b>bold</b>!'
    >>> compile_bold_stars('This is not **bold!')
    'This is not **bold!'
    >>> compile_bold_stars('**')
    '**'
    '''
    return line


def compile_bold_underscore(line):
    '''
    Convert "__bold__" to "<b>bold</b>".

    >>> compile_bold_underscore('__This is bold!__ This is not bold.')
    '<b>This is bold!</b> This is not bold.'
    >>> compile_bold_underscore('__This is bold!__')
    '<b>This is bold!</b>'
    >>> compile_bold_underscore('This is __bold__!')
    'This is <b>bold</b>!'
    >>> compile_bold_underscore('This is not __bold!')
    'This is not __bold!'
    >>> compile_bold_underscore('__')
    '__'
    '''
    return _pair(line, '__', '<b>', '</b>')


def compile_code_inline(line):
    '''
    Add <code> tags and escape HTML inside them.

    >>> compile_code_inline('This is inline code: `1+2`')
    'This is inline code: <code>1+2</code>'
    >>> compile_code_inline('`1+2`')
    '<code>1+2</code>'
    >>> compile_code_inline('This example has html within the code: `<b>bold!</b>`')
    'This example has html within the code: <code>&lt;b&gt;bold!&lt;/b&gt;</code>'
    >>> compile_code_inline('this example has a math formula in the  code: `1 + 2 < 4`')
    'this example has a math formula in the  code: <code>1 + 2 &lt; 4</code>'
    >>> compile_code_inline('```')
    '```'
    '''
    out, inside, i = '', False, 0
    while i < len(line):
        if line[i:i + 3] == '```':
            out += '```'
            i += 3
            continue
        c = line[i]
        if c == '`':
            out += '</code>' if inside else '<code>'
            inside = not inside
        elif inside and c == '<':
            out += '&lt;'
        elif inside and c == '>':
            out += '&gt;'
        else:
            out += c
        i += 1
    return out


def compile_links(line):
    '''
    Add <a> tags.

    >>> compile_links('Click on the [course webpage](https://x)!')
    'Click on the <a href="https://x">course webpage</a>!'
    >>> compile_links('[course webpage](https://x)')
    '<a href="https://x">course webpage</a>'
    >>> compile_links('this is wrong: [course webpage]    (https://x)')
    'this is wrong: [course webpage]    (https://x)'
    '''
    out = line
    while '[' in out and '](' in out:
        i = out.find('[')
        j = out.find('](', i)
        k = out.find(')', j)
        if j < 0 or k < 0:
            break
        out = out[:i] + f'<a href="{out[j+2:k]}">{out[i+1:j]}</a>' + out[k+1:]
    return out


def compile_images(line):
    '''
    Add <img> tags.

    >>> compile_images('[Mike Izbicki](https://x/y.png)')
    '[Mike Izbicki](https://x/y.png)'
    >>> compile_images('![Mike Izbicki](https://x/y.png)')
    '<img src="https://x/y.png" alt="Mike Izbicki" />'
    >>> compile_images('This is an image: ![Mike](https://x/y.png)')
    'This is an image: <img src="https://x/y.png" alt="Mike" />'
    '''
    return line
