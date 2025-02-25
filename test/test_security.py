import subprocess
import pytest

def test_bandit():
    """Test de sécurité du code avec Bandit."""
    result = subprocess.run(
        ["bandit", "-r", "src", "-f", "json", "-o", "bandit_report.json"],  # Générer un rapport JSON
        capture_output=True,
        text=True
    )
    # Vérifier qu'il n'y a pas de problèmes de sécurité
    assert result.returncode == 0, f"Bandit security issues:\n{result.stdout}"

def test_safety():
    """Test de sécurité des dépendances avec Safety."""
    result = subprocess.run(
        ["safety", "check", "--full-report"],  # Vérifier les vulnérabilités des dépendances
        capture_output=True,
        text=True
    )
    # Vérifier qu'il n'y a pas de vulnérabilités critiques
    assert result.returncode == 0, f"Safety vulnerabilities:\n{result.stdout}"