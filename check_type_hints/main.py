import ast
import subprocess
from typing import List, Union

import typer
from typing_extensions import Annotated

app = typer.Typer()


def get_files_to_commit() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
        capture_output=True,
        text=True,
    )
    changed_files = result.stdout.strip().split("\n")
    return [file for file in changed_files if file.endswith(".py")]


class TypeHintChecker(ast.NodeVisitor):
    def __init__(self, file: str, file_method: set = None):
        self.errors = []
        self.file = file
        self.file_method = file_method if file_method else {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.check_type_hints(node, "Function")

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.check_type_hints(node, "Async Function")

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.check_type_hints(item, "Method")
        self.generic_visit(node)

    def check_type_hints(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef], func_type: str
    ) -> None:
        if self.file_method and node.name in self.file_method:
            return
        if node.name != "__init__" and node.returns is None:
            self.errors.append(
                f"Warning: {self.file} {func_type} '{node.name}' is missing return type hint"
            )
        for arg in node.args.args:
            if arg.arg in ["self", "cls"]:
                continue
            if arg.annotation is None:
                self.errors.append(
                    f"Warning: {self.file}{func_type} '{node.name}' is missing type hint for argument '{arg.arg}'"
                )


def check_file_for_type_hints(file: str, filter_method: set = None) -> List[str]:
    with open(file, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())

    checker = TypeHintChecker(file, filter_method)
    checker.visit(tree)

    return checker.errors


def filter_directory(file: str, filter_set: set) -> bool:
    folds = file.split("/")
    return folds[1] in filter_set if len(folds) > 1 else False


@app.command()
def check(
    ignore: Annotated[
        bool,
        typer.Option(
            help="In the pre-commit, select whether to ignore the error and proceed with the commit."
        ),
    ] = False,
    filter: Annotated[
        List[str],
        typer.Option(
            help="You can enable filter to filter the folders that do not participate in the check. such as tests, pytests"
        ),
    ] = None,
    method: Annotated[
        List[str],
        typer.Option(
            help="You can choose to filter certain special methods, such as get, post, put, delete, patch."
        ),
    ] = None,
) -> None:
    errors = []
    filter = set(filter) if filter else None
    method = set(method) if method else None
    for file in get_files_to_commit():
        if filter and filter_directory(file, set(filter)):
            continue
        if file_errors := check_file_for_type_hints(file, method):
            errors.extend([f"{file}: {error}" for error in file_errors])
    if errors:
        print("Type hint errors found:")
        for error in errors:
            print(error)
    else:
        print("No type hint errors found")
    if not ignore and errors:
        exit(1)
    else:
        exit(0)


@app.command()
def check_file(file: str) -> None:
    errors = []
    if file_errors := check_file_for_type_hints(file):
        errors.extend([f"{file}: {error}" for error in file_errors])

    if errors:
        print("No type hint errors found")
        exit(0)


if __name__ == "__main__":
    app()
