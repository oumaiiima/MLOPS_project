import subprocess
import pytest

def test_flake8():
    """Test la qualité du code avec flake8."""
    result = subprocess.run(
        ["flake8", "src", "--max-line-length=100", "--exclude=venv"],
        capture_output=True,
        text=True
    )
    # Vérifier qu'il n'y a pas d'erreurs
    assert result.returncode == 0, f"Flake8 errors:\n{result.stdout}"

def test_pylint():
    """Test la qualité du code avec pylint."""
    result = subprocess.run(
        ["pylint", "src", "--ignore=venv"],
        capture_output=True,
        text=True
    )
    # Vérifier qu'il n'y a pas d'erreurs
    assert result.returncode == 0, f"Pylint issues:\n{result.stdout}"
