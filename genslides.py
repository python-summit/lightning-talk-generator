import subprocess
from pathlib import Path
from jinja2 import Environment


TALKS: list[tuple[str, str, str | None]] = [
    ("Dominik Gresch", "Better Autocomplete with Type Hints", "better_autocomplete_with_type_hints.pdf"),
    ("Tamara Reuveni Mazig", "Topic Modelling for Customer experience", "Lightning Talk Tamara Reuveni Mazig.pptx.pdf"),
    # ("Jan Werth", r"AI \& our Brain $\rightarrow$ not quite there yet", None),  # FIXME
    ("Simon Niederberger", r"Jupyter \& Git", "presentation.pdf"),
    ("Vita Midori", "ML at Demokratis.ch", "Vita Midori - ML at Demokratis.pdf"),
    ("Tim Head", "Zero Code Change Acceleration", 'Lightning - Zero Code Change.pptx.pdf'),
    # ("Timon Erhart", "Data Dashboard in 5min", None),
    ("Josua Schmid", "Funny Slides for Data Scientist", "2024-10-18 Funny Slides for Data Scientists.pdf"),
    ("Ricardo Pereira", "Python Superset", "PythonSuperset.pdf"),
    ("Stefan Keller", "Pythons and Ducks!", "Lightning_Talk_Stefan_Keller_Pythons_and_Ducks.pdf"),
    # ("Florian Bruhin", "fstring.help", None),  # FIXME
    ("Florian Bruhin", "A .py/.tex/.pdf quine", None),
]


def main() -> None:
    talks: list[tuple[str, str, str | None, str]] = [
        (speaker, title, pdf, next_speaker)
        for (speaker, title, pdf), (next_speaker, _, _)
        in zip(TALKS, TALKS[1:] + [("", "", None)])
    ]

    env = Environment(
        variable_start_string="((",
        variable_end_string="))",
        block_start_string="((*",
        block_end_string="*))",
        comment_start_string="((=",
        comment_end_string="=))",
        autoescape=False,
    )
    j2_src = Path("genslides.tex.j2").read_text()
    template = env.from_string(j2_src)
    tex_src = template.render(entries=talks)

    tex_path = Path("talks.tex")
    tex_path.write_text(tex_src)

    subprocess.run(
        ["latexmk", "-pdf", "-shell-escape", tex_path],
        check=True,
    )


if __name__ == "__main__":
    main()
