import subprocess
from pathlib import Path
from jinja2 import Environment


TALKS: list[tuple[str, str, str]] = [
    ("Speaker 1", "Title 1", "testfile1.pdf"),
    ("Speaker 2", "Title 2", "testfile2.pdf"),
    ("Speaker 3", "Title 3", "testfile3.pdf"),
    # ("Speaker 4", "Title 4", "testfile4.pdf"),
    # ("Speaker 5", "Title 5", "testfile5.pdf"),
    # ("Speaker 6", "Title 6", "testfile6.pdf"),
    ("Florian Bruhin", "A .py/.tex/.pdf quine", None),
]


def main() -> None:
    talks = [
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
