# Contributing to scalflow

Thank you for your interest in contributing to scalflow! This document provides guidelines and instructions for contributing to this Special Core Analysis & petrophysics library.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Branch Strategy](#branch-strategy)
- [Code Quality Standards](#code-quality-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project is intended to be a welcoming space for collaboration. We expect all contributors to:
- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize scientific accuracy and code quality
- Help maintain clear documentation

## Getting Started

### Prerequisites

- **Python**: >=3.12
- **Package Manager**: [UV](https://github.com/astral-sh/uv) (not pip or poetry)
- **Git**: For version control
- **GitHub CLI** (optional but recommended): `gh` for easier PR management

### Setting Up Your Development Environment

1. **Fork and clone the repository:**
   ```bash
   gh repo fork oskrgab/scalflow --clone
   cd scalflow
   ```

2. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Set up the development environment:**
   ```bash
   uv sync  # Installs all dependencies including dev dependencies
   ```

4. **Install pre-commit hooks** (IMPORTANT):
   ```bash
   uv run pre-commit install
   ```

   This installs git hooks that automatically check code quality before each commit and **prevent accidental commits to protected branches** (`main` and `dev`).

5. **Verify your setup:**
   ```bash
   uv run pytest              # Run tests
   uv run ruff check .        # Check code quality
   uv run ty check            # Type check
   uv run pre-commit run --all-files  # Test pre-commit hooks
   ```

### Optional: Git Aliases for Easier Workflow

Add these to `~/.gitconfig`:

```ini
[alias]
    # Create feature branch from updated dev
    feature = "!f() { git checkout dev && git pull && git checkout -b feature/$1; }; f"

    # Sync dev with remote
    sync = "!git checkout dev && git pull origin dev"

    # Clean up merged branches
    cleanup = "!git branch --merged dev | grep -v '^* dev$' | xargs git branch -d"
```

Usage:
```bash
git feature my-new-feature    # Creates feature/my-new-feature from updated dev
git sync                      # Updates local dev
git cleanup                   # Deletes merged feature branches
```

### Pre-commit Hooks: Your First Line of Defense

Pre-commit hooks run **automatically before each commit** to catch issues early.

**What's checked:**

1. **Branch protection** - Blocks commits to `main` and `dev` (forces feature branch workflow)
2. **Code formatting** - Auto-formats with ruff
3. **Linting** - Auto-fixes common issues with ruff
4. **Type checking** - Validates types with ty
5. **File hygiene** - Removes trailing whitespace, fixes line endings
6. **YAML/TOML validation** - Checks workflow files and pyproject.toml
7. **Spell checking** - Catches typos with codespell

**Normal workflow:**

```bash
git checkout -b feature/my-feature
# ... make changes ...
git add .
git commit -m "Add feature"

# Pre-commit runs automatically:
# ✅ All checks pass → commit succeeds
# ❌ Any check fails → commit blocked, files may be auto-fixed
```

**If hooks auto-fix files:**

```bash
git commit -m "Add feature"
# ruff-format............Failed
# - files were modified by this hook

# Ruff reformatted your code, re-add and commit:
git add .
git commit -m "Add feature"
# ✅ Passes this time
```

**Protection from mistakes:**

```bash
# ❌ Trying to commit on protected branch
git checkout main
git commit -m "oops"

# Output:
# no-commit-to-branch........Failed
# You're attempting to commit on branch 'main'
# Committing directly to 'main' is not allowed.

# ✅ Use feature branches instead
git checkout -b feature/my-fix
git commit -m "Add fix"  # Works!
```

**Skip hooks temporarily (use sparingly!):**

```bash
git commit --no-verify  # Bypasses pre-commit hooks
# WARNING: CI will still catch issues, and you can't push to main/dev anyway!
```

**Update hooks to latest versions:**

```bash
uv run pre-commit autoupdate
```

## Development Workflow

### Branch Strategy

This project uses a **three-branch model**:

```
main (production, stable releases only)
  ↑
  └── dev (integration branch, latest development)
       ↑
       ├── feature/*   (new features)
       ├── bugfix/*    (bug fixes)
       ├── refactor/*  (code improvements)
       └── hotfix/*    (emergency production fixes - can also go to main)
```

### Branch Naming Conventions

Use these prefixes for your branches:

- **`feature/*`** - New features or enhancements
  - Example: `feature/add-let-model`, `feature/dataset-loader`

- **`bugfix/*`** - Bug fixes found during development
  - Example: `bugfix/fix-calculation-error`, `bugfix/validation-bug`

- **`refactor/*`** - Code improvements without changing functionality
  - Example: `refactor/improve-validation`, `refactor/simplify-api`

- **`hotfix/*`** - Emergency fixes for production issues
  - Example: `hotfix/security-patch`, `hotfix/critical-bug`
  - **Note**: Hotfix branches can merge directly to `main`, bypassing `dev`

### Standard Development Flow

**⚠️ IMPORTANT**: Branch protection is **remote-only**. Git allows you to commit to local `main` or `dev`, but GitHub will reject the push. Always work on feature branches!

#### For Regular Development (Features, Bugfixes, Refactoring)

1. **Create a branch from `dev`:**
   ```bash
   git checkout dev
   git pull origin dev                    # Sync with remote first
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following our [code quality standards](#code-quality-standards)
   - Add tests (we require >90% coverage)
   - Update documentation
   - Commit frequently (commit message quality doesn't matter - we squash merge)

3. **Run quality checks locally:**

   **Option A: Let pre-commit handle it (recommended)**
   ```bash
   git add .
   git commit -m "Add feature"
   # Pre-commit automatically runs: ruff format, ruff check, ty check
   # You still need to run tests manually:
   uv run pytest --cov=scalflow
   ```

   **Option B: Run checks manually before committing**
   ```bash
   uv run ruff format .                   # Auto-format code
   uv run ruff check --fix .              # Fix linting issues
   uv run ty check                        # Type check
   uv run pytest --cov=scalflow            # Run tests with coverage
   ```

   **Note:** Tests are NOT run by pre-commit hooks (too slow). Always run tests manually before pushing.

4. **Push and create PR to `dev`:**
   ```bash
   git push -u origin feature/your-feature-name
   gh pr create --base dev --title "Add feature: your description"
   ```

5. **Wait for CI checks:**
   - `test` - Runs pytest
   - `lint` - Runs ruff format check, ruff check, ty check
   - `validate-source-branch` - Ensures correct branch workflow

6. **Address review feedback** (if any) and push updates

7. **After merge**, clean up:
   ```bash
   git checkout dev
   git pull origin dev
   git branch -d feature/your-feature-name
   ```

#### For Emergency Production Fixes (Hotfixes)

1. **Create a hotfix branch from `main`:**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-issue
   ```

2. **Make your fix and test thoroughly**

3. **Create PR directly to `main`:**
   ```bash
   git push -u origin hotfix/critical-issue
   gh pr create --base main --title "Hotfix: critical issue description"
   ```

4. **After merge to `main`, sync back to `dev`:**
   ```bash
   git checkout dev
   git pull origin dev
   git merge main
   git push origin dev
   ```

### Recovery: Accidentally Committed to Local Main/Dev

**Note:** Pre-commit hooks should prevent this! If you're seeing this scenario, make sure you installed pre-commit hooks with `uv run pre-commit install`.

If you somehow bypassed pre-commit hooks (or didn't install them) and committed to `main` or `dev`:

```bash
# 1. Check what commits you made
git log --oneline -5

# 2. Create feature branch from current position (saves your commits)
git checkout -b feature/recover-my-work

# 3. Reset local main/dev to match remote (discards local commits)
git checkout dev  # or main
git reset --hard origin/dev  # or origin/main

# 4. Continue working on feature branch
git checkout feature/recover-my-work
git push -u origin feature/recover-my-work
gh pr create --base dev
```

## Branch Strategy

### PR Validation Rules

Our CI automatically validates that PRs follow the correct workflow:

**PRs to `main` - Only these are allowed:**
- ✅ `dev` branch (normal release workflow)
- ✅ `hotfix/*` branches (emergency production fixes)

**PRs to `main` - These are blocked:**
- ❌ `feature/*` branches (must merge to `dev` first)
- ❌ `bugfix/*` branches (must merge to `dev` first)
- ❌ Any other branches

**PRs to `dev` - Recommended:**
- ✅ `feature/*` branches (new features)
- ✅ `bugfix/*` branches (bug fixes)
- ✅ `refactor/*` branches (code improvements)
- ✅ `main` branch (syncing hotfixes)
- ⚠️ Other branches (allowed with warning)

## Code Quality Standards

### Design Principles

- **SOLID principles** - Use appropriate design patterns for Python
- **Not everything needs to be a class** - Use pure functions for mathematical operations
- **Use classes where appropriate** - Data models, correlation families, dataset loaders
- **Readability first** - Code should be self-documenting
- **Separation of concerns** - Keep validation, calculation, and presentation logic separate

### Ruff (Linter & Formatter)

We use Ruff for code formatting and linting:

**Configuration** (in `pyproject.toml`):
- Line length: 88 characters
- Python target: 3.12
- Double quotes for strings
- NumPy-style docstrings (mandatory)

**Run locally before committing:**
```bash
uv run ruff format .        # Auto-format code
uv run ruff check .         # Check for issues
uv run ruff check --fix .   # Auto-fix issues
```

**Enabled rule sets:**
- `E`, `F` - Standard errors and pyflakes
- `I` - Import sorting (isort)
- `B` - flake8-bugbear (catches subtle bugs)
- `UP` - pyupgrade (modern Python syntax)
- `N` - PEP8 naming conventions
- `D` - Docstrings (MANDATORY)
- `NPY` - NumPy-specific rules
- `PT` - pytest best practices
- `SIM` - Simplification suggestions

### Ty (Type Checker)

**Type hints are required for:**
- ✅ All function arguments
- ✅ All function return types
- ✅ All class attributes (in `__init__`)

**Run locally:**
```bash
uv run ty check
```

**Example:**
```python
import numpy as np
import numpy.typing as npt

def krw(
    s_eff: npt.NDArray[np.float64],
    krw0: float,
    nw: float,
) -> npt.NDArray[np.float64]:
    """Calculate relative permeability."""
    return krw0 * s_eff**nw
```

### Performance Philosophy

1. **Start simple** - Direct NumPy array operations
2. **Vectorize early** - Avoid Python loops
3. **Profile before optimizing** - Don't guess bottlenecks
4. **Benchmark against NumPy** - Keep it simple if not significantly faster
5. **Document complexity** - Explain optimizations that hurt readability

### Input Validation

All public functions should validate inputs, but keep validation logic separate:

```python
# _core/validation.py (internal)
def validate_saturation(s: npt.NDArray, name: str = "saturation") -> None:
    """Validate saturation is in [0, 1] range."""
    if np.any((s < 0) | (s > 1)):
        raise ValueError(f"{name} must be in [0, 1]")

# Public API function
def krw(sw: npt.NDArray, swr: float, snwr: float, krw0: float, nw: float) -> npt.NDArray:
    """Calculate relative permeability."""
    validate_saturation(sw, "sw")
    validate_corey_params(swr, snwr, krw0, nw)
    # ... calculation
```

## Testing Requirements

### Coverage Requirement: >90%

All contributions must maintain test coverage above 90%.

**Check coverage:**
```bash
uv run pytest --cov=scalflow --cov-report=term-missing
uv run pytest --cov=scalflow --cov-report=html  # HTML report in htmlcov/
```

### Testing Strategy

1. **Unit tests** - Test individual functions with known inputs/outputs
2. **Property-based testing** - Use `hypothesis` for mathematical properties
3. **Integration tests** - Test correlation models end-to-end
4. **Validation tests** - Ensure input validation catches invalid data
5. **Example tests** - Verify documentation examples work

### Property-Based Testing

For mathematical functions, use `hypothesis` to test properties:

```python
from hypothesis import given, strategies as st
import numpy as np

@given(
    sw=st.lists(st.floats(0.2, 0.8), min_size=1, max_size=100),
    swr=st.floats(0.0, 0.15),
    snwr=st.floats(0.0, 0.15),
)
def test_effective_saturation_bounds(sw, swr, snwr):
    """Property: Effective saturation should be in [0, 1]."""
    sw_array = np.array(sw)
    result = s_eff(sw_array, swr, snwr)

    assert np.all(result >= 0)
    assert np.all(result <= 1)
```

**What is property-based testing?**
Instead of specific test cases, you define properties that should always be true. `hypothesis` generates hundreds of random test cases to validate these properties. Perfect for mathematical functions!

## Documentation Standards

### Docstring Requirements (Mandatory)

**All public functions MUST have NumPy-style docstrings** with examples:

```python
def krw(
    s_eff: npt.NDArray[np.float64],
    krw0: float,
    nw: float,
) -> npt.NDArray[np.float64]:
    r"""Calculate the relative permeability of the wetting phase.

    Parameters
    ----------
    s_eff : npt.NDArray[np.float64]
        Effective wetting phase saturation array.
    krw0 : float
        Endpoint relative permeability for the wetting phase.
    nw : float
        Corey exponent for the wetting phase.

    Returns
    -------
    npt.NDArray[np.float64]
        Relative permeability of the wetting phase array.

    Notes
    -----
    The relative permeability ($k_{rw}$) is calculated using the Corey model:

    $$k_{rw} = k_{rw0} \cdot S_{eff}^{n_w}$$

    where $k_{rw0}$ is the endpoint relative permeability, $S_{eff}$ is the
    effective saturation, and $n_w$ is the Corey exponent.

    Examples
    --------
    Calculate relative permeability for a saturation range:

    >>> import numpy as np
    >>> s_eff = np.linspace(0, 1, 50)
    >>> krw_values = krw(s_eff, krw0=0.8, nw=2.0)
    >>> krw_values.shape
    (50,)
    >>> krw_values[0]  # At s_eff=0
    0.0
    >>> krw_values[-1]  # At s_eff=1
    0.8

    References
    ----------
    .. [1] Corey, A.T., "The Interrelation Between Gas and Oil Relative
           Permeabilities", Producers Monthly, 1954.
    """
    return krw0 * s_eff**nw
```

### Documentation Structure

- **NumPy-style docstrings** for all public functions
- **LaTeX equations** using `$$...$$` syntax (rendered with MathJax)
- **Runnable examples** in docstrings (tested with pytest)
- **References** to scientific papers when applicable

### Building Documentation Locally

```bash
uv run mkdocs serve  # Preview at http://127.0.0.1:8000
```

Documentation is automatically deployed to GitHub Pages on release.

## Pull Request Process

### Before Creating a PR

1. **Ensure pre-commit hooks are installed:**
   ```bash
   uv run pre-commit install  # If you haven't already
   ```

2. **Commit your changes** (pre-commit hooks run automatically):
   ```bash
   git add .
   git commit -m "Clear description of changes"
   # Pre-commit runs: format, lint, type check, branch protection
   ```

3. **Run tests manually** (not covered by pre-commit):
   ```bash
   uv run pytest --cov=scalflow
   ```

4. **Ensure all tests pass** and **coverage is >90%**

5. **Update documentation** if you changed the API

6. **Add examples** to docstrings for new functions

**Alternative:** Run all checks manually before committing:
```bash
uv run ruff format .
uv run ruff check --fix .
uv run ty check
uv run pytest --cov=scalflow
```

### Creating a PR

1. **Push your branch:**
   ```bash
   git push -u origin feature/your-feature-name
   ```

2. **Create PR to `dev` branch:**
   ```bash
   gh pr create --base dev --title "Clear description of changes"
   ```

3. **Fill out the PR description:**
   - What problem does this solve?
   - What changes were made?
   - How was it tested?
   - Any breaking changes?

### PR Review Process

- **Automated checks** will run: `test`, `lint`, `validate-source-branch`
  - If you used pre-commit hooks, `lint` should already pass!
  - `test` checks ensure coverage is >90%
  - `validate-source-branch` confirms you're targeting the correct branch
- **All checks must pass** before merging
- **Maintainers will review** code quality, tests, and documentation
- **Address feedback** by pushing new commits to your branch
- **Squash merge** - All commits will be squashed into one clean commit on `dev`

### After Your PR is Merged

```bash
git checkout dev
git pull origin dev
git branch -d feature/your-feature-name  # Clean up local branch
```

## Release Process

Releases are managed by maintainers. The process is:

1. **Batch features on `dev`** until ready for release
2. **Create release PR**: `dev` → `main`
3. **After merge, tag the release:**
   ```bash
   git checkout main
   git pull origin main
   git tag X.Y.Z
   git push origin X.Y.Z
   ```
4. **Automated release workflow** handles:
   - Building the package
   - Publishing to PyPI
   - Creating GitHub Release
   - Deploying documentation

## Common Commands Reference

```bash
# Development
uv sync                                    # Install/sync dependencies
uv run pytest                              # Run tests
uv run pytest --cov=scalflow --cov-report=html  # Test with coverage report
uv run ruff format .                       # Format code
uv run ruff check --fix .                  # Lint and auto-fix
uv run ty check                            # Type check
uv run mkdocs serve                        # Preview docs locally

# Pre-commit hooks
uv run pre-commit install                  # Install git hooks (one-time setup)
uv run pre-commit run --all-files          # Run all hooks on all files
uv run pre-commit autoupdate               # Update hooks to latest versions
git commit --no-verify                     # Skip pre-commit hooks (emergency only)

# Git workflow
git checkout dev                           # Switch to dev
git pull origin dev                        # Sync with remote
git checkout -b feature/my-feature         # Create feature branch
git push -u origin feature/my-feature      # Push feature branch
gh pr create --base dev                    # Create PR to dev
```

## Getting Help

- **Issues**: Open a [GitHub issue](https://github.com/oskrgab/scalflow/issues) for bugs or feature requests
- **Discussions**: Use [GitHub Discussions](https://github.com/oskrgab/scalflow/discussions) for questions
- **Documentation**: Check the [official docs](https://oskrgab.github.io/scalflow)

## Project Goals

This library aims to:
- Provide **industry-standard** relative permeability and capillary pressure correlations
- Maintain **scientific accuracy** with proper references
- Offer **high performance** using NumPy vectorization
- Include **public datasets** for easy access
- Support the **petroleum engineering community** with quality open-source tools

Thank you for contributing to scalflow! 🛢️
