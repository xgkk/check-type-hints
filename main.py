import ast
import subprocess
from typing import List, Union


def get_files_to_commit() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=AM"],
        capture_output=True,
        text=True,
    )
    changed_files = result.stdout.strip().split("\n")
    return [file for file in changed_files if file.endswith(".py")]


class TypeHintChecker(ast.NodeVisitor):
    def __init__(self, file: str):
        self.errors = []
        self.file = file

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


def check_file_for_type_hints(file: str) -> List[str]:
    with open(file, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())

    checker = TypeHintChecker(file)
    checker.visit(tree)

    return checker.errors


def main():
    errors = []
    for file in get_files_to_commit():
        if file_errors := check_file_for_type_hints(file):
            errors.extend([f"{file}: {error}" for error in file_errors])

    if errors:
        print("Type hint errors found:")
        for error in errors:
            print(error)
        exit(1)
    else:
        print("No type hint errors found")
        exit(0)


if __name__ == "__main__":
    main()
