from aethermind.identity import Identity


def test_identity_load_and_reflect(tmp_path):
    path = tmp_path / "id.yaml"
    path.write_text("name: Test\nboundaries: []\n")
    ident = Identity.load(path)
    assert ident.name == "Test"
    ident.reflect("hello")
    data = path.read_text()
    assert "hello" in data
