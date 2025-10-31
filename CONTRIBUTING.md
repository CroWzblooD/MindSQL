# Contributing Guidelines

Thank you for your interest in contributing to the MariaDB Vector Store integration for MindSQL!

## Quick Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/MindSQL.git
cd MindSQL

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_demo.txt
pip install mariadb pytest black flake8

# Setup test database
mysql -u root -p
CREATE DATABASE mindsql_test;
CREATE USER 'mindsql_test'@'localhost' IDENTIFIED BY 'test_password';
GRANT ALL PRIVILEGES ON mindsql_test.* TO 'mindsql_test'@'localhost';

# Verify
pytest tests/ -v
```

---

## Coding Standards

### PEP 8 Compliance

```python
# 4 spaces, max 100 chars, type hints required

def process_query(question: str, n_results: int = 5) -> List[str]:
    """
    Brief description.
    
    Args:
        question: Description
        n_results: Description
        
    Returns:
        Description
    """
    return results
```

### Naming Conventions

- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_CASE`
- Private methods: `_leading_underscore`

### Code Quality

```bash
# Format and lint
black mindsql/ tests/
flake8 mindsql/ tests/ --max-line-length=100

# Before commit
pytest tests/ -v && black --check mindsql/ tests/ && flake8 mindsql/ tests/
```

---

## Testing

### Writing Tests

```python
import pytest
from mindsql.vectorstores import MariaDBVectorStore

class TestMariaDBVectorStore:
    @pytest.fixture
    def vectorstore(self):
        config = {'host': 'localhost', 'user': 'mindsql_test', 'password': 'test_password'}
        return MariaDBVectorStore(config=config)
    
    def test_add_ddl(self, vectorstore):
        result = vectorstore.add_ddl("CREATE TABLE users (id INT);")
        assert "Successfully" in result
```

### Running Tests

```bash
pytest tests/ -v                    # All tests
pytest tests/ --cov=mindsql -v      # With coverage
pytest tests/test_file.py::test_name -v  # Specific test
```

**Requirements:**
- New features: 80% coverage minimum
- Bug fixes: Include test reproducing bug
- All public methods tested

---

## Pull Request Process

### Workflow

```bash
# 1. Create branch
git checkout -b feature/your-feature

# 2. Make changes
# Edit code, add tests, update docs

# 3. Test and format
pytest tests/ -v
black mindsql/ tests/
flake8 mindsql/ tests/

# 4. Commit with proper message
git add .
git commit -m "feat: add batch processing support"

# 5. Push and create PR
git push origin feature/your-feature
```

### Commit Message Format

```
<type>: <short description>

[Optional longer description]

[Optional footer: Closes #123]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring

**Examples:**
```
feat: add batch embedding support

fix: resolve connection timeout issue

docs: update API reference for retrieve_ddl
```

### PR Checklist

- [ ] Code follows PEP 8
- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Code formatted (`black mindsql/ tests/`)
- [ ] Documentation updated
- [ ] No breaking changes (or documented)

---

## Issue Reporting

### Bug Report Template

```markdown
**Description:** Brief bug description

**Steps to Reproduce:**
1. Step one
2. Step two

**Expected:** What should happen
**Actual:** What actually happens

**Environment:**
- Python: 3.11.6
- MariaDB: 10.11.5
- OS: Ubuntu 22.04

**Error:**
```
[Paste error message]
```
```

### Feature Request Template

```markdown
**Description:** What feature you want

**Use Case:** Why it's needed

**Proposed Solution:** How it could work
```

---

## Development Best Practices

### Code Quality

- Keep functions small and focused
- Use meaningful names
- Add docstrings to public methods
- Handle errors gracefully
- Follow DRY principle

### Testing

- Test edge cases and errors
- Use descriptive test names
- Keep tests independent
- Mock external dependencies

### Security

- Never commit credentials (use environment variables)
- Validate all inputs
- Use parameterized queries
- Keep dependencies updated

### Documentation

When adding features:
- Update README.md
- Add usage examples
- Update API reference
- Add docstrings

---

## Code Review Guidelines

### For Contributors

- Keep PRs small and focused
- Write clear descriptions
- Respond to feedback promptly
- Be open to suggestions

### For Reviewers

- Be constructive and specific
- Explain the "why"
- Focus on code, not person
- Acknowledge good work

---

## Getting Help

- Check documentation first
- Search existing issues
- Open new issue with details
- Ask in GitHub Discussions

---

## Resources

**Documentation:**
- [MariaDB VECTOR](https://mariadb.com/kb/en/vector-data-type/)
- [MindSQL Project](https://github.com/Mindinventory/MindSQL)
- [Python PEP 8](https://pep8.org/)

**Tools:**
- [pytest](https://docs.pytest.org/)
- [black](https://black.readthedocs.io/)
- [MariaDB Connector](https://mariadb.com/docs/appdev/connector-python/)

---

Thank you for contributing!

**Version:** 1.0.0
