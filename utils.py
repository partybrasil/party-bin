import random
import string
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

def generate_url(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def highlight_code(code, language=None):
    try:
        if language:
            lexer = get_lexer_by_name(language, stripall=True)
        else:
            lexer = guess_lexer(code)
        formatter = HtmlFormatter(linenos=True, cssclass="codehilite")
        return highlight(code, lexer, formatter)
    except Exception:
        return f'<pre class="codehilite">{code}</pre>'
