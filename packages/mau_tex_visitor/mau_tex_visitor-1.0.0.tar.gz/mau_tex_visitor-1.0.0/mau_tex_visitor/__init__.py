import re

from mau.visitors.jinja_visitor import JinjaVisitor


DEFAULT_TEMPLATES = {
    "caret.tex": r"\textsuperscript{ {{-content-}} }",
    "class.tex": "{{content}}",
    "inline_image.tex": r"\includegraphics{ {{-uri-}} } ",
    "link.tex": r"\href{ {{-target-}} }{ {{-text-}} }",
    "macro.tex": "",
    "sentence.tex": "{{ content }}",
    "star.tex": r"\textbf{ {{-content-}} }",
    "text.tex": "{{ value }}",
    "tilde.tex": r"\textsubscript{ {{-content-}} }",
    "underscore.tex": r"\textit{ {{-content-}} }",
    "verbatim.tex": r"\texttt{ {{-value-}} }",
    ########################################
    "block-admonition.tex": (
        "{{ kwargs.class }} - {{ kwargs.label }}\n\n" "{{ content }}\n"
    ),
    "block.tex": "{{ content }}\n",
    "block-quote.tex": "{{ content }}\n{{ secondary_content }}\n",
    ########################################
    "source.tex": "{% for line, _ in code %}{{ line }}\n{% endfor %}",
    "callouts_entry.tex": "",
    "callout.tex": "",
    ########################################
    "command.tex": "",
    "container.tex": "{{ content }}",
    "document.tex": "{{ content }}",
    "header.tex": (r"\{{command}}{ {{-value-}} }" "\n\n"),
    "horizontal_rule.tex": (r"\rule{\textwidth}{0.5pt}" "\n\n"),
    "content.html": "",
    "content_image.tex": (
        r"\begin{figure}[h]"
        "\n"
        r"{% if title %}\caption{ {{-title-}} }{% endif %}"
        "\n"
        r"\centering"
        "\n"
        r"\includegraphics[width=\textwidth]{ {{-uri-}} }"
        "\n"
        r"\end{figure}"
        "\n\n"
    ),
    "paragraph.tex": "{{ content }}\n\n\n",
    "raw.tex": "{{ content }}",
    ########################################
    "list_item.tex": (r"\item {{ content }}" "\n\n"),
    "list.tex": (
        "{% if not main_node %}\n{% endif %}"
        r"{% if ordered %}\begin{enumerate}{% else %}\begin{itemize}{% endif %}"
        "\n"
        "{{ items }}"
        r"{% if ordered %}\end{enumerate}{% else %}\end{itemize}{% endif %}"
        "{% if main_node %}\n\n{% endif %}"
    ),
    ########################################
    "toc_entry.tex": "",
    "toc.tex": "",
    ########################################
    "footnote.tex": r"\footnote{ {{-content-}} }",
    "footnotes_entry.tex": "",
    "footnotes.tex": "",
}


class TexVisitor(JinjaVisitor):
    format_code = "tex"
    extension = "tex"

    default_templates = DEFAULT_TEMPLATES

    def _escape_text(self, text):
        conv = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\^{}",
            "\\": r"\textbackslash{}",
            "<": r"\textless{}",
            ">": r"\textgreater{}",
        }
        regex = re.compile(
            "|".join(
                re.escape(str(key))
                for key in sorted(conv.keys(), key=lambda item: -len(item))
            )
        )
        return regex.sub(lambda match: conv[match.group()], text)

    def _visit_header(self, node, *args, **kwargs):
        command_map = {
            "1": r"chapter",
            "2": r"section",
            "3": r"subsection",
            "4": r"subsubsection",
            "5": r"paragraph",
            "6": r"subparagraph",
        }

        base = super()._visit_header(node, *args, **kwargs)
        level = str(base["data"].get("level", 6))
        base["data"]["command"] = command_map.get(level)

        return base

    def _visit_source__default(self, node, *args, **kwargs):
        base = super()._visit_source__default(node, *args, escape=False, **kwargs)
        return base

    def _visit_text(self, node, *args, escape=True, **kwargs):
        base = super()._visit_text(node, *args, **kwargs)

        if escape:
            base["data"]["value"] = self._escape_text(base["data"]["value"])

        return base

    def _visit_verbatim(self, node, *args, **kwargs):
        base = super()._visit_verbatim(node, *args, **kwargs)

        base["data"]["value"] = self._escape_text(base["data"]["value"])

        return base
