# Contributing

We're just getting started! This project is currently pre-0.0.1 and is not
accepting contributions yet.

## Coding Standards and Best Practices

Here are the coding standards and best practices for the project. These
guidelines aim to make the project more maintainable, readable and consistent.

### Automating Standards

When possible, these standards should be automated.

Tools:

- [Bandit](https://bandit.readthedocs.io/) for detecting security issues
- [Black](https://black.readthedocs.io/) for code formatting
- [Coverage](https://coverage.readthedocs.io/) for assessing test coverage
- [Gitleaks](https://gitleaks.io/) for secrets detection
- [Pre-commit](https://pre-commit.com/) to automate checking the code
- [Pylint](https://black.readthedocs.io/) for enforcing standards and
  encouraging best practices
- [Unittest](https://docs.python.org/3/library/unittest.html) for unit tests

### Code Formatting

- Use **four spaces** for indentation; avoid tabs.
- Limit line length to **79 characters** for readability (but may be up to what black allows).
- Place two blank lines between top-level functions and classes.
- Use blank lines sparingly within functions to group related lines of code.
- Write **clear and concise** code, avoiding unnecessary complexity.
- Follow [PEP 8](https://peps.python.org/pep-0008/) for general code
  formatting.

### Naming Conventions

- Use **snake_case** for variable names (e.g., `user_name`, `age_limit`).
- Use **CamelCase** for class names (e.g., `UserService`, `DataLoader`).
- Use **UPPER_CASE** for constants (e.g., `MAX_RETRY_COUNT`).
- Avoid using single characters as variable names except for simple loop
  counters.
- Use descriptive names that reflect the purpose of the variable, function, or
  class.

### Comments and Documentation

- Provide clear and concise comments to explain complex logic, especially when
  it's not immediately obvious.
- Use descriptive comments, avoiding generic labels like "TODO" or "FIXME"
  without a following description.
- Write docstrings for public classes, functions, and modules, following
  [PEP 257](https://peps.python.org/pep-0257/).
- Optimize docstrings for reading from
  [pydoc](https://docs.python.org/3/library/pydoc.html).
- Long form docs should be added as markdown files in the
  [docs folder](./docs).
- Avoid docstrings that effectively restate the name of the function. If that's
  all that makes sense in the docstring, it can be omitted.

### Functions and Methods

- Keep functions and methods short and focused on a single task.
- Avoid deeply nested code and excessive indentation in functions.
- Functions should have verb-noun names that describe their actions (e.g.,
  `calculate_total`, `validate_email`).
- Aim to make functions and methods **pure**, minimizing side effects.
- Consider using type annotations to indicate function parameter and return
  types.

### Error Handling

- Handle exceptions gracefully and avoid using bare `except:` statements.
- Catch specific exceptions whenever possible to avoid catching unexpected
  errors.
- Log exceptions and errors appropriately for debugging and monitoring
  purposes.
- Provide informative error messages that aid in debugging.

### Logging

- At a minimum include enough logging statements to be able to:
  - Debug an issue
  - Detect malicious activity
  - Observe the general operation of the code
- Use the proper log levels (DEBUG, WARNING, INFO, etc).

### Imports

- Import modules and packages explicitly. Avoid using wildcard imports
  (`from module import *`).
- Group imports in the following order:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- Sort imports alphabetically within each group.

### Testing

- Write unit tests for all functions and methods to ensure code correctness and
  to facilitate refactoring.
- Use the **unittest** library to organize and run tests.
- Use **coverage** to assess test coverage.
- Aim for high test coverage, but more importantly make sure the tests provide value:
  - If you broke a function, the unit tests should catch it.
  - Help catch unexpected changes to logic.

### Security

- Sanitize user inputs to prevent injection attacks and other security
  vulnerabilities.
- Use **parameterized queries** when dealing with databases.
- Avoid storing sensitive information, such as passwords, in plain text. Use
  secure storage mechanisms.
- Run SAST tools like **bandit** on the code to detect common security issues.
- Scan your code for accidently included secrets.

### Performance

- Write efficient algorithms and data structures for critical sections of code.
- Use built-in Python functions and libraries for performance-critical
  operations.
- Profile code using tools like **cProfile** to identify bottlenecks.

### Version Control

- Use [short lived branches](https://trunkbaseddevelopment.com/)
- Follow these Git commit best practices:
  - Aim to make separate commits for each logical change.
  - The first line should be 50 characters or less.
  - The rest of the message should be separated by an empty line and wrapped at 72 characters.
  - Title should be imperative from (e.g. "Add new feature" instead of "Added a new feature").

### Miscellaneous

- Remove unused imports, variables, and functions regularly.
- Avoid global variables whenever possible; prefer passing arguments
  explicitly.
- Follow the [Zen of Python](https://www.python.org/dev/peps/pep-0020/)
  principles.
