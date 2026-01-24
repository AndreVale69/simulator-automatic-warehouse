# Contributing to Simulator Automatic Warehouse 🚀

Thank you for your interest in contributing to **Simulator - Automatic Warehouse**.
Contributions of any kind are welcome: bug reports, feature proposals, documentation improvements, and code.

This document outlines the guidelines to help maintain a clean, consistent, and collaborative workflow.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs 🐛](#reporting-bugs-)
  - [Suggesting Enhancements ✨](#suggesting-enhancements-)
  - [Contributing Code 💻](#contributing-code-)
- [Development Workflow](#development-workflow)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Questions \& Support](#questions--support)
- [Final Notes](#final-notes)

---

## Code of Conduct

This project follows a **simple rule**:
**Be respectful, constructive, and professional.**

Harassment, discrimination, or aggressive behavior will not be tolerated.

---

## How Can I Contribute?

### Reporting Bugs 🐛

If you find a bug, please open an **Issue** and include:

* A clear and descriptive title
* Steps to reproduce the issue
* Expected behavior vs. actual behavior
* Screenshots or logs (if applicable)
* Environment details (OS, compiler, versions)

If you are unsure whether something is a bug, open an issue anyway; discussion is welcome.

---

### Suggesting Enhancements ✨

Feature requests and design improvements are welcome.

When opening an enhancement issue, please describe:

* The problem you are trying to solve
* Your proposed solution
* Possible alternatives (if any)
* Impact on existing behavior (if known)

---

### Contributing Code 💻

You can contribute code by fixing bugs, implementing features, improving performance, or enhancing documentation.

Before starting large changes:

* Check existing issues and pull requests
* Open a discussion issue if unsure about the design

---

## Development Workflow

1. **Fork** the repository
2. Create a **new branch** from `main`:

   ```bash
   git checkout -b feature/my-feature-1
   ```
   Or for bug fixes:
   ```bash
   git checkout -b fix/bug-description-2
   ```
   Or for documentation:
   ```bash
   git checkout -b docs/improve-topic-3
   ```
   Or for refactoring:
   ```bash
   git checkout -b refactor/component-name-4
   ```
   Usually, use `feature/`, `fix/`, `docs/`, or `refactor/` prefixes to indicate the type of change,
   a short description, and the number of the related issue if applicable (e.g., `feature/add-pathfinding-42`).
3. Make your changes.
4. Ensure the project builds and runs correctly (run tests if applicable)
5. Commit your changes. See [Commit Messages](#commit-messages) for guidelines.
6. Push to your fork and open a **Pull Request**

---

## Coding Guidelines

* Follow the existing project structure and style
* Prefer **clear, readable code** over clever tricks
* Use meaningful variable and function names
* Avoid unnecessary dependencies
* Keep functions focused and modular
* Document non-trivial logic where useful

Consistency matters more than personal preference.

---

## Commit Messages

Use **clear and descriptive commit messages**.

Recommended format:

```
<type>: short description

(optional) longer explanation
```

Examples:

```
fix: prevent collision detection overflow
feat: add priority-based routing strategy
docs: clarify configuration parameters
```

Try to keep commits focused and atomic, possibly following the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style.

---

## Pull Requests

When opening a Pull Request:

* Clearly describe **what** the PR does and **why**
* Reference related issues (e.g. `Fixes #12`)
* Keep PRs focused on a single change when possible
* Ensure the code builds without errors
* Be open to feedback and revisions

Pull requests may be refined before being merged — this is normal and encouraged.

---

## Questions & Support

If you have questions about the project, architecture, or contribution process:

* Open a **discussion issue**
* Ask directly in your Pull Request

Curiosity and learning are always welcome.

---

## Final Notes

This is both a learning and research-oriented project.
Clean contributions, thoughtful discussions, and incremental improvements are valued more than speed.

Thanks again for contributing!
