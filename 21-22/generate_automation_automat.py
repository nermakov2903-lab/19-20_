"""
generate_automation_automat.py

Устойчивый генератор диаграммы автомата из APP_AUTOMATON.

Usage:
    py generate_automation_automat.py [module_name] [var_name]

Defaults:
    module_name = "main"
    var_name = "APP_AUTOMATON"

Если указанный модуль/переменная не найдены, скрипт просканирует
все .py файлы в текущей директории и попробует выполнить их в
изолированном пространстве имён, чтобы найти переменную.
(Это удобно, если APP_AUTOMATON определён в другом файле или имеет другое имя.)
"""

import importlib
import sys
import os
import pydot
import traceback
from typing import Any, Dict

OUT_DOT = "automaton.dot"
OUT_PNG = "automaton.png"
OUT_SVG = "automaton.svg"

def load_automaton_from_module(module_name: str, var_name: str) -> Dict[str, Any]:
    """Попытаться импортировать переменную из модуля через importlib."""
    try:
        m = importlib.import_module(module_name)
    except Exception as e:
        raise ImportError(f"Can't import module '{module_name}': {e}")
    if not hasattr(m, var_name):
        raise AttributeError(f"module '{module_name}' has no attribute '{var_name}'")
    return getattr(m, var_name)

def scan_py_files_for_var(var_name: str):
    """
    Просканировать все .py файлы в текущей директории (и поддиректориях, кроме venv)
    и попытаться исполнить их в локальном namespace чтобы найти var_name.
    Возвращает tuple(filename, value) при успехе или None.
    """
    cwd = os.getcwd()
    exclude_dirs = {"venv", ".venv", "__pycache__"}
    for root, dirs, files in os.walk(cwd):
        # пропускаем виртуальные окружения
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            full = os.path.join(root, fname)
            try:
                with open(full, "r", encoding="utf-8") as f:
                    src = f.read()
                # Выполняем в изолированном неймспейсе
                namespace = {"__file__": full, "__name__": "__scan__"}
                exec(compile(src, full, "exec"), namespace)
                if var_name in namespace:
                    return full, namespace[var_name]
            except Exception:
                # не критично — файл мог требовать импортов/зависимостей
                # распечатаем трассировку для отладки, но продолжим
                #print(f"Warning: couldn't exec {full}: {traceback.format_exc()}")
                continue
    return None, None

def build_graph(automaton: Dict[str, dict], initial_state=None, title="Automaton"):
    graph = pydot.Dot(graph_type="digraph", rankdir="LR", label=title, fontsize="12", fontname="Arial")

    # states = keys of automaton + EXIT
    states = set(automaton.keys())
    states.add("EXIT")

    # create nodes
    for s in states:
        if s == initial_state or (initial_state is None and s == list(automaton.keys())[0]):
            node = pydot.Node(s, shape="rectangle", style="filled", fillcolor="#a8d5ff", fontname="Arial")
        elif s == "EXIT":
            node = pydot.Node(s, shape="doublecircle", fontname="Arial")
        else:
            node = pydot.Node(s, shape="rectangle", fontname="Arial")
        graph.add_node(node)

    # add edges
    for state, transitions in automaton.items():
        for input_key, cfg in transitions.items():
            label = input_key
            if "action" in cfg:
                label += " / " + cfg["action"]
            if "error" in cfg:
                label += " / error:" + cfg["error"]
            # next may be called next_state or next
            next_state = cfg.get("next_state") or cfg.get("next") or state
            if next_state == "BACK":
                # map BACK to a caller state (if MAIN exists use it, else use first key)
                next_state_label = "MAIN" if "MAIN" in automaton else list(automaton.keys())[0]
            else:
                next_state_label = next_state
            edge = pydot.Edge(state, next_state_label, label=label, fontname="Arial")
            # red color for error edges
            if "error" in cfg:
                edge.set_color("red")
            graph.add_edge(edge)

    return graph

def main():
    module_name = "main"
    var_name = "APP_AUTOMATON"
    if len(sys.argv) >= 2:
        module_name = sys.argv[1]
    if len(sys.argv) >= 3:
        var_name = sys.argv[2]

    print(f"Looking for variable '{var_name}' in module '{module_name}' ...")
    automaton = None
    source = None

    # first try import module
    try:
        automaton = load_automaton_from_module(module_name, var_name)
        source = f"module:{module_name}"
    except Exception as e:
        print(f"Import failed: {e}")

    # if not found, scan files
    if automaton is None:
        print("Scanning .py files in project to find variable...")
        fname, value = scan_py_files_for_var(var_name)
        if value is not None:
            automaton = value
            source = fname
            print(f"Found {var_name} in file: {fname}")
        else:
            print(f"Could not find variable '{var_name}' in module '{module_name}' or in project files.")
            print("Make sure APP_AUTOMATON is defined at module level or pass the correct module/var name:")
            print("Usage: py generate_automation_automat.py <module> <varname>")
            sys.exit(2)

    # validate automaton basic structure
    if not isinstance(automaton, dict):
        print("Found variable but it is not a dict. Aborting.")
        sys.exit(3)

    initial = list(automaton.keys())[0] if len(automaton) > 0 else None
    print(f"Building graph from {source}, initial state: {initial}")
    graph = build_graph(automaton, initial_state=initial, title=var_name)

    # write outputs
    graph.write_raw(OUT_DOT)
    print("Wrote", OUT_DOT)
    try:
        graph.write_png(OUT_PNG)
        print("Wrote", OUT_PNG)
    except Exception as e:
        print("Could not write PNG (graphviz may be missing):", e)
    try:
        graph.write_svg(OUT_SVG)
        print("Wrote", OUT_SVG)
    except Exception as e:
        print("Could not write SVG (graphviz may be missing):", e)

if __name__ == "__main__":
    main()
