<div align="center">
<!---
![PyPI - Version](https://img.shields.io/pypi/v/annotation-tool)
![PyPI - Downloads](https://img.shields.io/pypi/dm/annotation-tool)
![PyPI - License](https://img.shields.io/pypi/l/annotation-tool?color=brightgreen)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/annotation-tool)
-->

</div>

# Installation

All stable versions can be installed from [PyPI] by using [pip] or your favorite package manager

    pip install xai-explainer

You can get pre-published versions from [TestPyPI] or this repository

**From Source:**

    pip install git+https://gitlab.fachschaften.org/xai/explainer/xai-first-project.git@main


# Development

**Requirements:**
- Python 3.8 or higher
- [poetry] 1.2 or higher
- [make]

For installing the development environment run

```bash
make setup
```

Run scripts using poetry

    poetry run python script_name.py

[make]: https://www.gnu.org/software/make/
[pip]: https://pypi.org/project/pip/
[poetry]: https://python-poetry.org/
[pypi]: https://pypi.org/
[testpypi]: https://test.pypi.org/project/annotation-tool/
