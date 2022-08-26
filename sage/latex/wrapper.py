import requests

from sage.logger import logger


class LatexWrapper:
    def __init__(self, url: str):
        # docker run --rm -p 5030:5030 planqk/latex-renderer:latest
        logger.info("Init latex wrapper at: %s" % (url))
        self.__url = url

    def prepare(self, txt: str) -> bytes:
        # curl -X POST localhost:5030/renderLatex -H "content-type:application/json" \
        # -d '{"content":"\\begin{math} \\frac{2 + 2}{6} \\end{math}","latexPackages":[],"output":"svg"}'  -o out.svg
        eq = "\\pagecolor{gray}\n\\color{white}\n\\begin{math} %s \\end{math}" % txt
        in_data = {'content': eq, 'latexPackages': ['\\usepackage{xcolor}'], 'output': 'svg'}
        x = requests.post(self.__url, json=in_data)
        if x.status_code != 200:
            raise Exception("Can't prepare equation image")
        return x.text
        # data = "\n".join(data.split("\n")[1:])
        # return bytes(data, 'utf-8')
