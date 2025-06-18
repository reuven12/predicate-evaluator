@echo off
set CMD=%1

if "%CMD%"=="test" (
    echo Running unit tests with coverage report...
    docker compose run --rm predicate-tests
) else if "%CMD%"=="lint" (
    echo Running flake8 linter...
    docker compose run --rm predicate-tests flake8 predicate
) else if "%CMD%"=="format" (
    echo Formatting code with black...
    docker compose run --rm predicate-tests black predicate
) else if "%CMD%"=="run" (
    echo Building and running all containers...
    docker compose up --build
) else if "%CMD%"=="clean" (
    echo Cleaning up containers and volumes...
    docker compose down --volumes --remove-orphans
) else (
    echo Unknown command: %CMD%
    echo Usage: make.bat [test^|lint^|format^|run^|clean]
)
