"""Build the documentation for a package."""
import argparse
import email.utils
import itertools
import os
import pathlib
import shutil
import subprocess
import time
import warnings

from ..utils import CONFIGS, execute_command_list, get_pyproject_config
from .sample_conf import CONF_PY, MARKDOWN, TYPE_HINTS


__commands_to_run = CONFIGS["build_docs_commands"]
BASE_DIR = CONFIGS["base_dir"]
PACKAGE_NAME = CONFIGS["package_name"].replace("-", "_").replace(".", "_")

DOCS_OUTPUT_DIRECTORY = "docs"
DOCS_WORKING_DIRECTORY = "_docs"


def _build_docs():
    pyproject = get_pyproject_config()
    tools = pyproject["tool"].get("jgt_tools") or {}
    if "doc_build_types" in tools:
        message = (
            "The use of doc_build_types is deprecated and may be removed in a "
            "future version of the library. Use build_docs_commands instead."
        )
        warnings.warn(message, FutureWarning)
        if tools["doc_build_types"] == [] and "build_docs_commands" not in tools:
            return
    execute_command_list([x.format(**globals()) for x in __commands_to_run])


def _build_conf():
    docs_dir = BASE_DIR / DOCS_WORKING_DIRECTORY
    docs_dir.mkdir(exist_ok=True)

    pyproject = get_pyproject_config()
    poetry = pyproject["tool"]["poetry"]

    dependencies = list(
        itertools.chain(
            poetry["dependencies"],
            poetry.get("dev-dependencies", {}),
            poetry.get("group", {}).get("dev", {}).get("dependencies", {}),
        )
    )

    conf = CONF_PY.format(
        name=f"{poetry['name']} - {poetry['description']}",
        authors=", ".join(email.utils.parseaddr(x)[0] for x in poetry["authors"]),
        year=time.strftime("%Y"),
        type_hints=TYPE_HINTS if "sphinx-autodoc-typehints" in dependencies else "",
        version=poetry["version"],
        markdown=MARKDOWN if "recommonmark" in dependencies else "",
    )

    (docs_dir / "conf.py").write_text(conf)


def build():
    """Build the docs."""
    # Setup environment variables
    try:
        commit_id = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=BASE_DIR,
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        commit_id = ""
    os.environ["GIT_COMMIT_ID"] = commit_id.rstrip("\n")

    try:
        origin_url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=BASE_DIR,
            universal_newlines=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError:
        origin_url = ""
    os.environ["GIT_ORIGIN_URL"] = origin_url.rstrip("\n")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dirty",
        action="store_true",
        help="Leave the output directory untouched before starting to build documents",
    )
    args = parser.parse_args()

    if not args.dirty:
        shutil.rmtree(str(BASE_DIR / DOCS_OUTPUT_DIRECTORY), ignore_errors=True)
        shutil.rmtree(str(BASE_DIR / DOCS_WORKING_DIRECTORY), ignore_errors=True)

    _build_conf()

    _build_docs()


def push():
    """Push docs to github-pages."""
    if (pathlib.Path(BASE_DIR) / DOCS_OUTPUT_DIRECTORY).exists():
        subprocess.check_call(["poetry", "run", "ghp-import", "-p", "docs/"])


def build_and_push():
    """Build docs then publish."""
    build()
    push()
