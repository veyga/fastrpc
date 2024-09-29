import ast
from logging import Logger
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from ast import NodeTransformer, fix_missing_locations, dump
from _fastrpc.server.utils.log import logger


class RemoteFunctionTransformer(NodeTransformer):
    """
    AST transformer to replace the body of functions decorated with `@remote`
    to a simple print statement.
    """

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        # Check if the function has a decorator @remote
        if any(
            isinstance(decorator, ast.Name) and decorator.id == "remote"
            for decorator in node.decorator_list
        ):
            # Replace the body of the function with a print statement
            new_body = ast.Expr(
                value=ast.Call(
                    func=ast.Name(id="print", ctx=ast.Load()),
                    args=[ast.Str(s=f"Function '{node.name}' called!")],
                    keywords=[],
                )
            )
            node.body = [new_body]  # Replace the body with the print statement
        return node


def clean_unused_imports(file_path: Path) -> None:
    """
    Removes unused imports by parsing and rebuilding the AST.
    This requires the 'autoflake' library, which can be installed via pip.
    """

    subprocess.run(
        ["autoflake", "--remove-all-unused-imports", "--in-place", str(file_path)],
        check=True,
    )


def process_python_file(source_file: Path, target_dir: Path) -> None:
    """
    Processes a single Python file:
    1. Checks if it has remote functions.
    2. Replaces the body of those functions with a print statement.
    3. Cleans up unused imports.
    4. Copies the file to the target directory.
    """
    with source_file.open("r") as file:
        source_code = file.read()

    # Parse the Python file's AST
    tree = ast.parse(source_code)

    # Transform the AST
    transformer = RemoteFunctionTransformer()
    transformed_tree = transformer.visit(tree)

    # Check if any function was transformed
    if dump(tree) != dump(transformed_tree):
        # If transformations were made, write the modified code to the new directory
        new_code = ast.unparse(fix_missing_locations(transformed_tree))
        target_file = target_dir / source_file.name
        with target_file.open("w") as file:
            file.write(new_code)

        # Clean unused imports
        clean_unused_imports(target_file)


def copy_files_with_remote_functions(source_dir: Path, target_dir: Path) -> None:
    """
    Copies Python files that contain remote functions to the target directory
    and modifies their function implementations.
    """
    target_dir.mkdir(parents=True, exist_ok=True)

    for source_file in source_dir.rglob("*.py"):
        process_python_file(source_file, target_dir)


def transform_source(
    source_root: Path,
    client_out: Path,
) -> None:
    """
    Resolves + transforms all @fastrpc decorated definitions from a source root.
    """
    logger.info(
        "\nTransforming sources...\n"
        f"source_root = {source_root}\n"
        f"client_out = {client_out}\n"
    )
    try:
        if client_out.exists():
            logger.debug("eleting existing client sources..")
            shutil.rmtree(client_out)
        # copy_files_with_remote_functions(source_root, Path(client_out))
        print(f"Done, check directory for new source files: '{client_out}''")
    except Exception as e:
        print(f"Error: {e}")


__all__ = [
    "transform_source",
]
