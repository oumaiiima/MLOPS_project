import subprocess

def test_flake8():
    """Test la qualité du code avec flake8."""
    result = subprocess.run(
        ["flake8", "src", "--max-line-length=100"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Flake8 errors:\n{result.stdout}"

def test_pylint():
    """Test la qualité du code avec pylint."""
    result = subprocess.run(
        ["pylint", "src"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Pylint issues:\n{result.stdout}"
