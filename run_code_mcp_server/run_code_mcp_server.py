"""
Run Code Snippet MCP Server
A FastMCP server similar to Pylance's pylanceRunCodeSnippet MCP server.
Allows AI assistants (Copilot, Claude, etc.) to execute Python code snippets
and return structured results including stdout, stderr, return value, and errors.
"""

import sys
import io
import traceback
import ast
import contextlib
from typing import Any
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP(
    name="RunCodeSnippet",
    instructions=(
        "This MCP server lets you execute Python code snippets in an isolated environment. "
        "Use `run_code_snippet` to execute code and get structured output including stdout, "
        "stderr, return values, and error details. "
        "Use `check_syntax` to validate Python syntax without executing it. "
        "Use `run_code_with_context` to execute code with pre-defined variables/context."
    ),
)


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _execute_code(code: str, global_vars: dict | None = None) -> dict[str, Any]:
    """Core execution engine – runs code and collects all output."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()

    exec_globals = {"__builtins__": __builtins__}
    if global_vars:
        exec_globals.update(global_vars)

    return_value = None
    error = None
    error_type = None
    traceback_str = None
    success = False

    try:
        # Try to compile & detect if last statement is an expression we can eval
        tree = ast.parse(code, mode="exec")
        last_return = None

        if tree.body and isinstance(tree.body[-1], ast.Expr):
            # Split: run everything except last line, then eval last line
            *body_stmts, last_expr = tree.body
            body_module = ast.Module(body=body_stmts, type_ignores=[])
            ast.fix_missing_locations(body_module)
            expr_module = ast.Expression(body=last_expr.value)
            ast.fix_missing_locations(expr_module)

            body_code = compile(body_module, "<snippet>", "exec")
            expr_code = compile(expr_module, "<snippet>", "eval")

            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(body_code, exec_globals)   # noqa: S102
                last_return = eval(expr_code, exec_globals)  # noqa: S307
        else:
            compiled = compile(tree, "<snippet>", "exec")
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(compiled, exec_globals)   # noqa: S102

        return_value = last_return
        success = True

    except SyntaxError as exc:
        error_type = "SyntaxError"
        error = str(exc)
        traceback_str = traceback.format_exc()
    except Exception as exc:           # noqa: BLE001
        error_type = type(exc).__name__
        error = str(exc)
        traceback_str = traceback.format_exc()

    return {
        "success": success,
        "stdout": stdout_buf.getvalue(),
        "stderr": stderr_buf.getvalue(),
        "return_value": repr(return_value) if return_value is not None else None,
        "error_type": error_type,
        "error": error,
        "traceback": traceback_str,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────────────────────────────────────

@mcp.tool()
def run_code_snippet(code: str) -> dict[str, Any]:
    """
    Execute a Python code snippet and return structured results.

    Similar to VS Code Pylance's pylanceRunCodeSnippet tool.
    Captures stdout, stderr, return value of the last expression,
    and full error/traceback information.

    Args:
        code: The Python code to execute.

    Returns:
        A dict with keys:
          - success (bool)
          - stdout (str)
          - stderr (str)
          - return_value (str | None)  – repr of the last expression
          - error_type (str | None)
          - error (str | None)
          - traceback (str | None)
    """
    return _execute_code(code)


@mcp.tool()
def run_code_with_context(code: str, context: dict[str, Any]) -> dict[str, Any]:
    """
    Execute a Python code snippet with pre-defined variables injected into scope.

    Useful when you want to test a function against specific values or pass
    objects (serialisable as JSON) into the execution environment.

    Args:
        code:    The Python code to execute.
        context: A dict of variable names → JSON-serialisable values that will
                 be available as globals inside the snippet.

    Returns:
        Same structure as `run_code_snippet`, plus:
          - context_vars (list[str]) – names that were injected.
    """
    result = _execute_code(code, global_vars=context)
    result["context_vars"] = list(context.keys())
    return result


@mcp.tool()
def check_syntax(code: str) -> dict[str, Any]:
    """
    Check the syntax of a Python code snippet WITHOUT executing it.

    Args:
        code: The Python code to check.

    Returns:
        A dict with keys:
          - valid (bool)
          - error (str | None)       – human-readable error message
          - line (int | None)        – line number of the error
          - offset (int | None)      – column offset of the error
          - error_type (str | None)
    """
    try:
        ast.parse(code)
        return {"valid": True, "error": None, "line": None, "offset": None, "error_type": None}
    except SyntaxError as exc:
        return {
            "valid": False,
            "error": exc.msg,
            "line": exc.lineno,
            "offset": exc.offset,
            "error_type": "SyntaxError",
        }


@mcp.tool()
def get_python_info() -> dict[str, str]:
    """
    Return information about the Python runtime used by this MCP server.

    Returns:
        A dict with version, platform, and executable path.
    """
    import platform
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("starting server")
    mcp.run(transport="streamable-http")