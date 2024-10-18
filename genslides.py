import shutil
import subprocess
import tempfile
from pathlib import Path
from jinja2 import Environment


TALKS: list[tuple[str, str, str | None]] = [
    ("Speaker 1", "Title 1", "testfile1.pdf"),
    ("Speaker 2", "Title 2", "testfile2.pdf"),
    ("Speaker 3", "Title 3", "testfile3.pdf"),
    # ("Speaker 4", "Title 4", "testfile4.pdf"),
    # ("Speaker 5", "Title 5", "testfile5.pdf"),
    # ("Speaker 6", "Title 6", "testfile6.pdf"),
    # ("Florian Bruhin", "A .py/.tex/.pdf quine", "testfile7.pdf"),
]


def main() -> None:
    talks = [
        (speaker, title, Path(pdf).resolve() if pdf else None, next_speaker)
        for (speaker, title, pdf), (next_speaker, _, _) in zip(
            TALKS, TALKS[1:] + [("", "", None)]
        )
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
    template = env.from_string(Path("genslides.tex.j2").read_text())
    tex_src = template.render(entries=talks)

    with tempfile.TemporaryDirectory() as tempdir:
        tempdir_path = Path(tempdir)
        tex_file_path = tempdir_path / "talks.tex"

        tex_file_path.write_text(tex_src)

        subprocess.run(["latexmk", "-pdf", tex_file_path], check=True, cwd=tempdir_path)
        final_pdf_path = tex_file_path.with_suffix(".pdf")
        output_pdf_path = Path.cwd() / final_pdf_path.name
        shutil.copy(final_pdf_path, output_pdf_path)


if __name__ == "__main__":
    main()
