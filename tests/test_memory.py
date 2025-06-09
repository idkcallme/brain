from aethermind import Brain


def test_store_and_recall(monkeypatch):
    brain = Brain()
    monkeypatch.setattr(brain.controller, "_choose_action", lambda state: "short_term")
    brain.remember("hello")
    result = brain.controller.short_term.get_all()
    assert any(item.data == "hello" for item in result)
