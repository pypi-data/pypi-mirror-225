from fastapi import WebSocket
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import MarkdownLexer, get_lexer_by_name


class MarkdownRenderer(object):
    def __init__(self, text, language=None):
        self.text = text
        self.language = language

    def format(self) -> str:
        if self.language:
            lexer = get_lexer_by_name(self.language)
        else:
            lexer = MarkdownLexer()
        formatter = HtmlFormatter()
        return highlight(self.text, lexer, formatter)

    async def stream(self, websocket: WebSocket):
        await websocket.send_text(self.format())

def markdown(text: str):
    return MarkdownRenderer(text).format()
