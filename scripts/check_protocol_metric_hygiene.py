#!/usr/bin/env python3
"""Fail CI if protocol metrics drift toward Python runtime serialization.

Scientific wire-size evidence must come from CAMH-CUFE canonical encoders. This
static guard rejects imports/calls that commonly caused legacy object-size
measurements to be confused with protocol bytes.
"""
from __future__ import annotations

import ast
from pathlib import Path
import sys

ROOTS = (Path("src/camh_cufe"), Path("experiments"))
FORBIDDEN_MODULES = {"pickle", "cloudpickle", "dill"}
FORBIDDEN_CALLS = {
    ("sys", "getsizeof"),
    ("pickle", "dumps"),
    ("pickle", "dump"),
    ("cloudpickle", "dumps"),
    ("dill", "dumps"),
}


def dotted_name(node: ast.AST) -> tuple[str, ...] | None:
    if isinstance(node, ast.Name):
        return (node.id,)
    if isinstance(node, ast.Attribute):
        prefix = dotted_name(node.value)
        if prefix is not None:
            return (*prefix, node.attr)
    return None


def inspect_file(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    problems: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] in FORBIDDEN_MODULES:
                    problems.append(f"{path}:{node.lineno}: forbidden import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            if module in FORBIDDEN_MODULES:
                problems.append(f"{path}:{node.lineno}: forbidden import from {node.module}")
        elif isinstance(node, ast.Call):
            name = dotted_name(node.func)
            if name is not None and tuple(name[-2:]) in FORBIDDEN_CALLS:
                problems.append(
                    f"{path}:{node.lineno}: forbidden runtime-size/serialization call {'.'.join(name)}"
                )
    return problems


def main() -> int:
    files: list[Path] = []
    for root in ROOTS:
        if root.exists():
            files.extend(sorted(root.rglob("*.py")))

    problems: list[str] = []
    for path in files:
        problems.extend(inspect_file(path))

    if problems:
        print("Protocol metric hygiene check FAILED:", file=sys.stderr)
        for problem in problems:
            print(f" - {problem}", file=sys.stderr)
        print(
            "Use typed canonical encoders and src/camh_cufe/wire_metrics.py for protocol bytes.",
            file=sys.stderr,
        )
        return 1

    print(f"Protocol metric hygiene check passed for {len(files)} Python files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
