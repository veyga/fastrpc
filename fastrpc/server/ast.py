import os

import shutil

import ast

from ast import NodeTransformer, fix_missing_locations, dump


class RemoteFunctionTransformer(NodeTransformer):
    """

    AST transformer to replace the body of functions decorated with `@remote`

    to a simple print statement.

    """

    def visit_FunctionDef(self, node):

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


def clean_unused_imports(file_path):
    """

    Removes unused imports by parsing and rebuilding the AST.

    This requires the 'autoflake' library, which can be installed via pip.

    """

    try:

        import autoflake

    except ImportError:

        raise ImportError("Please install 'autoflake' via pip: pip install autoflake")

    os.system(f"autoflake --remove-all-unused-imports --in-place {file_path}")


def process_python_file(source_file, target_dir):
    """

    Processes a single Python file:

    1. Checks if it has remote functions.

    2. Replaces the body of those functions with a print statement.

    3. Cleans up unused imports.

    4. Copies the file to the target directory.

    """

    with open(source_file, "r") as file:

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

        target_file = os.path.join(target_dir, os.path.basename(source_file))

        with open(target_file, "w") as file:

            file.write(new_code)

        # Clean unused imports

        clean_unused_imports(target_file)


def copy_files_with_remote_functions(source_dir, target_dir):
    """

    Copies Python files that contain remote functions to the target directory

    and modifies their function implementations.

    """

    if not os.path.exists(target_dir):

        os.makedirs(target_dir)

    for root, _, files in os.walk(source_dir):

        for file in files:

            if file.endswith(".py"):

                source_file = os.path.join(root, file)

                process_python_file(source_file, target_dir)


# Usage Example:

source_directory = "/path/to/source/python/files"

target_directory = "/path/to/target/directory"

copy_files_with_remote_functions(source_directory, target_directory)
