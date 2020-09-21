import pytest
import yaml
from pathlib import Path
v0_files = """
README.md
LICENSE
.yamllint
.github/workflows/lint.yml
.github/workflows/yamllint.yml
.github/ISSUE_TEMPLATE/custom.md
.github/pull_request_template.md""".split()


@pytest.mark.parametrize("fpath", v0_files)
def test_v0(fpath):
    assert Path(fpath).exists()


def test_v1():
    assert Path("docker-compose.yml").exists()
    compose = yaml.safe_load(Path("docker-compose.yml").read_text())
    assert "test-oas" in compose['services']
    assert "stoplight/spectral" in compose['services']['test-oas']['image']


def test_v2():
    assert Path("tox.ini").exists()

