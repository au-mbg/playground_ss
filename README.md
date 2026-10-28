# COURSE_TITLE

Starter repository for an HTML course website built with Quarto and Pixi. It
keeps student exercises and instructor solutions in the same source files and
renders two versions of the site.

> [!IMPORTANT]
> The instructor site is published at `/instructor/` by the included GitHub
> Pages workflow. That URL is public and is **not access controlled**. Do not
> use it for confidential assessments, exam answers, or restricted material.

## Start a course repository

1. Create a repository from this template and clone it.
2. [Install Pixi](https://pixi.sh/latest/installation/) if needed.
3. From the repository root, run `pixi run preview`.
4. Replace the starter lesson and the placeholders listed below.

Pixi installs Quarto, Python, and the declared dependencies on first use. No
separate Python environment is required.

## Commands

| Command | Result |
| --- | --- |
| `pixi run preview` | Preview the student site |
| `pixi run preview instructor` | Preview the instructor site |
| `pixi run render` | Render the student site to `course-notes/_site` |
| `pixi run render instructor` | Render to `course-notes/_site/instructor` |
| `pixi run render-all` | Clean and render both profiles |
| `pixi run publish` | Build deployable output in `course-notes/_site` |
| `pixi run clean` | Remove generated output, Quarto state, notebooks, and Python caches |

The published student site is placed at the site root. The instructor version
is placed below `/instructor/`.

## Repository layout

```text
.
├── course-notes/          # Quarto configuration and authored material
│   ├── lessons/           # Example course pages
│   ├── assets/            # Images and other static resources
│   ├── _extensions/       # Versioned teaching filters
│   └── _site/             # Generated website output (ignored)
├── course-utils/          # Optional installable Python helpers
├── pixi.toml              # Dependencies and contributor commands
└── .github/workflows/     # GitHub Pages publication
```

Edit `.qmd` source files, configuration, assets, and utilities. Do not edit
`_output`, `_site`, `.quarto`, or `*.quarto_ipynb`; they are generated.

## Customize the template

Search the repository for these deliberately distinctive values:

| Placeholder | Replace with |
| --- | --- |
| `COURSE_TITLE` | Reader-facing course title |
| `COURSE_REPOSITORY` | Repository name |
| `COURSE_AUTHOR` | Maintainer name and email |
| `GITHUB_ORGANIZATION` | GitHub user or organization |

Also replace the example lesson and asset, then adjust the sidebar in
`course-notes/_quarto.yml`. The neutral design lives in `_brand.yml` and
`styles.css` in that directory.

## Student and instructor content

The two profiles set `teaching.show-solutions` explicitly. Use a solution
callout for an instructor-only worked answer:

```markdown
::: {.callout-solution}
Worked answer.
:::
```

For paired blocks or executable cells, use `teaching="exercise"` and
`teaching="solution"`. Student scaffold cells that must not execute should
also set `#| eval: false`.

The extensions in `course-notes/_extensions` are committed intentionally so
local and CI renders use the same filters.

## Optional Python utilities

`course-utils` demonstrates how reusable implementation details can be kept
out of teaching pages while remaining importable during rendering. Pixi
installs it in editable mode.

To rename it, update the dependency in `pixi.toml`, the project metadata in
`course-utils/pyproject.toml`, the package directory below `course-utils/src`,
and imports in the `.qmd` files.

To remove it, delete `course-utils`, remove its entry from
`[pypi-dependencies]` in `pixi.toml`, remove its imports from the lesson, and
refresh the lockfile with `pixi lock`.

For use outside Pixi, such as a hosted notebook, install the renamed package
from the course repository:

```python
try:
    import course_utils
except ModuleNotFoundError:
    %pip install "course-utils @ git+https://github.com/GITHUB_ORGANIZATION/COURSE_REPOSITORY.git#subdirectory=course-utils"
```

## Publish with GitHub Pages

The workflow in `.github/workflows/publish.yml` runs on pushes to `main` and
can also be started manually. In the GitHub repository, open **Settings →
Pages** and select **GitHub Actions** as the source. A successful workflow
publishes the contents assembled by `pixi run publish`.
