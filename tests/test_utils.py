import pytest
from utils import sanitize_custom_options

def test_sanitize_custom_options_valid():
    valid_options = ["-sS", "-Pn", "-T4", "-p22,80", "--top-ports", "-v"]
    sanitized = sanitize_custom_options(valid_options)
    assert sanitized == valid_options

def test_sanitize_custom_options_with_mixed_valid_and_prefixes():
    options = ["-sS", "-p22,80", "--top-ports", "-T3"]
    sanitized = sanitize_custom_options(options)
    assert sanitized == options

def test_sanitize_custom_options_raises_on_invalid():
    with pytest.raises(ValueError) as excinfo:
        sanitize_custom_options(["-sS", "--evil-flag"])
    assert "❌ Unsafe or unsupported Nmap option" in str(excinfo.value)

def test_sanitize_custom_options_empty_list():
    assert sanitize_custom_options([]) == []

def test_sanitize_custom_options_partial_injection():
    with pytest.raises(ValueError):
        sanitize_custom_options(["-sS", "; rm -rf /"])
