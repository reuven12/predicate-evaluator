# BioCatch Predicate Evaluation System

A modular Python-based engine for evaluating JSON-defined predicates against dynamic Python objects. Designed with clean architecture, type safety, and full Docker-based workflow.

---

## 📁 Project Structure

```
predicate_project/
├── app/                       # Core application logic
│   ├── predicate/             # Operations, parsers, exceptions
│   ├── tests/                 # Unit tests
│   ├── Dockerfile             # App runtime container
│   ├── requirements*.txt      # Runtime and test dependencies
│   └── main.py                # Manual entry point (optional)
├── flask_server/              # Mock Flask server for remote predicates
├── docker-compose.yml         # Multi-service orchestration
├── Makefile                   # Dev shortcuts for Linux/macOS
├── make.bat                   # Dev shortcuts for Windows
```

---

## 🚀 Common Commands

### Build and Run All Services

```bash
make run              # Linux/macOS
.\make.bat run        # Windows
```

### Run Unit Tests

```bash
make test
.\make.bat test
```

### Lint with flake8

```bash
make lint
.\make.bat lint
```

### Format with black

```bash
make format
.\make.bat format
```

### Clean Containers and Volumes

```bash
make clean
.\make.bat clean
```

---

## 🧰 Prerequisites

- Docker
- Docker Compose

---

This project emphasizes modularity, testability, and developer experience. All services are containerized and can be launched with a single command. Fully ready for evaluation and extension.
