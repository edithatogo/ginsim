import nox
from nox.sessions import Session

# Use uv for faster environment creation
nox.options.sessions = ["lint", "type_check", "tests"]
nox.options.default_venv_backend = "uv"


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session: Session) -> None:
    session.install(".[dev]")
    session.run(
        "pytest",
        "-n",
        "auto",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-report=xml",
        *session.posargs,
    )


@nox.session(python="3.11")
def lint(session: Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python="3.11")
def type_check(session: Session) -> None:
    session.install(".[dev]")
    session.install("pyright")
    session.run("pyright", "src")


@nox.session(python="3.11")
def format_code(session: Session) -> None:
    session.install("ruff")
    session.run("ruff", "format", ".")
    session.run("ruff", "check", "--fix", ".")
