import ast
import subprocess
from pathlib import Path
from ast import NodeTransformer, fix_missing_locations, dump
from _fastrpc.server.utils.log import logger


# class RemoteFunctionTransformer(NodeTransformer):
#     """
#     AST transformer to replace the body of functions decorated with `@myapi`
#     to a simple print statement.
#     """

#     def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
#         # Check if the function has a decorator @remote
#         if any(
#             isinstance(decorator, ast.Name) and decorator.id == "myapi"
#             for decorator in node.decorator_list
#         ):
#             # Replace the body of the function with a print statement
#             new_body = ast.Expr(
#                 value=ast.Call(
#                     func=ast.Name(id="print", ctx=ast.Load()),
#                     args=[ast.Str(s=f"Function '{node.name}' called!")],
#                     keywords=[],
#                 )
#             )
#             node.body = [new_body]  # Replace the body with the print statement
#         return node


# def copy_files_with_remote_functions(source_dir: Path, target_dir: Path) -> None:
#     """
#     Copies Python files that contain remote functions to the target directory
#     and modifies their function implementations.
#     """

#     def process_python_file(source_file: Path) -> None:
#         """
#         Processes a single Python file:
#         1. Checks if it has remote functions.
#         2. Replaces the body of those functions with a print statement.
#         3. Cleans up unused imports.
#         4. Copies the file to the target directory.
#         """
#         with source_file.open("r") as file:
#             source_code = file.read()

#         # Parse the Python file's AST
#         tree = ast.parse(source_code)

#         # Transform the AST
#         transformer = RemoteFunctionTransformer()
#         transformed_tree = transformer.visit(tree)

#         # Check if any function was transformed
#         if dump(tree) != dump(transformed_tree):
#             # If transformations were made, write the modified code to the new directory
#             new_code = ast.unparse(fix_missing_locations(transformed_tree))
#             target_file = target_dir / source_file.name
#             with target_file.open("w") as file:
#                 file.write(new_code)

#                 subprocess.run(
#                     ["autoflake",
#                      "--remove-all-unused-imports",
#                      "--in-place",
#                      str(target_file)],
#                     check=True,
#                 )
#     target_dir.mkdir(parents=True, exist_ok=True)
#     for source_file in source_dir.rglob("*.py"):
#         process_python_file(source_file)


def source_to_client(source_root: Path, client_out: Path) -> None:
    logger.info(f"Generating client code...")
    logger.info(f"Client code generated [see {str(client_out)}]")
