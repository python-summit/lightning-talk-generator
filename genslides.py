import subprocess
from pathlib import Path
from jinja2 import Environment


TALKS: list[tuple[str, str, str | None]] = [
    ("Stefan Keller", "Pythons and Ducks!", "Lightning_Talk_Stefan_Keller_Pythons_and_Ducks.pdf"),
    ("Dominik Gresch", "Better Autocomplete with Type Hints", "better_autocomplete_with_type_hints.pdf"),
    ("Tamara Reuveni Mazig", "Topic Modelling for Customer experience", None),  # FIXME
    ("Jan Werth", r"AI \& our Brain $\rightarrow$ not quite there yet", None),  # FIXME
    ("Simon Niederberger", r"Jupyter \& Git", None),  # FIXME
    ("Vita Midori", "ML at Demokratis.ch", None),  # FIXME
    ("Tim Head", "Zero Code Change Acceleration", None),  # FIXME
    # ("Florian Bruhin", "fstring.help", None),  # FIXME
    # ("Timon Erhart", "Data Dashboard in 5min", None),  # FIXME
    # ("Josua Schmid", "Funny Slides for Data Scientist", "2024-10-18 Funny Slides for Data Scientists.pdf"),
    # (..., ..., ...)
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
