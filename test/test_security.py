import subprocess

def test_bandit():
    """Test de sécurité du code avec Bandit."""
    result = subprocess.run(["bandit", "-r", "src"], capture_output=True, text=True)
    assert result.returncode == 0, f"Bandit security issues:\n{result.stdout}"

def test_safety():
    """Test de sécurité des dépendances avec Safety."""
    result = subprocess.run(["safety", "scan", "--full-report"], capture_output=True, text=True)
    assert result.returncode == 0, f"Safety vulnerabilities:\n{result.stdout}"
