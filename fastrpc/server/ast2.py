import ast
import astor
from pathlib import Path

# Specify your source and destination directories
source_dir = Path("path/to/source_directory")
destination_dir = Path("path/to/destination_directory")

# Create destination directory if it doesn't exist
destination_dir.mkdir(parents=True, exist_ok=True)


# Function to modify the AST
class FastrpcFunctionModifier(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Check for the 'fastrpc' decorator
        if any(decorator.id == "fastrpc" for decorator in node.decorator_list):
            # Change the function body to just print something
            node.body = [
                ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="print", ctx=ast.Load()),
                        args=[ast.Str(s="This function is modified.")],
                        keywords=[],
                    )
                )
            ]
        return node


def modify_and_copy_file(src_file):
    with src_file.open("r") as f:
        tree = ast.parse(f.read(), filename=str(src_file))

    # Modify the function implementations
    modifier = FastrpcFunctionModifier()
    modified_tree = modifier.visit(tree)

    # Clean up unused imports
    new_tree = ast.Module(body=[], type_ignores=[])

    # Collect all used names
    used_names = set()

    for node in ast.walk(modified_tree):
        if isinstance(node, ast.Name):
            used_names.add(node.id)

    for node in ast.walk(modified_tree):
        if isinstance(node, ast.Import):
            if node.names[0].name in used_names:
                new_tree.body.append(node)
        elif isinstance(node, ast.ImportFrom):
            if node.module in used_names:
                new_tree.body.append(node)

    # Add modified functions to the new tree
    new_tree.body.extend(modified_tree.body)

    # Write the modified content to the new directory
    dest_file = destination_dir / src_file.name
    with dest_file.open("w") as f:
        f.write(astor.to_source(new_tree))


def main():
    for src_file in source_dir.rglob("*.py"):
        with src_file.open("r") as f:
            content = f.read()
            if "fastrpc" in content:
                modify_and_copy_file(src_file)


if __name__ == "__main__":
    main()
