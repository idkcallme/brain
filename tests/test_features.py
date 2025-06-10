import numpy as np
import pytest

from aethermind import (
    Brain,
    GoalManager,
    ReasoningLoop,
    SelfModificationGuard,
    EmergencyShutdown,
    process_user_input,
)
from aethermind.memory import (
    ShortTermCache, ShortTermItem, EpisodicMemory, SemanticVectorStore,
    ProceduralMemory, ArchivalMemory, FeedbackProcessor, MemoryController
)

def test_short_term_cache_operations():
    cache = ShortTermCache(capacity=2)
    cache.add(ShortTermItem('a'))
    cache.add(ShortTermItem('b'))
    assert len(cache) == 2
    popped = cache.pop_oldest()
    assert popped.data == 'a'
    cache.clear()
    assert len(cache) == 0

def test_episodic_memory_search_and_recent():
    epi = EpisodicMemory()
    epi.add('first event')
    epi.add('second keyword event')
    epi.add('third keyword event')
    results = epi.search('keyword')
    assert len(results) == 2
    assert results[0].data == 'third keyword event'
    recent = epi.get_recent(2)
    assert len(recent) == 2
    assert recent[-1].data == 'third keyword event'

def test_semantic_vector_store_add_and_search():
    store = SemanticVectorStore(dim=3)
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    store.add(v1, 'a')
    store.add(v2, 'b')
    query = np.array([1.0, 0.0, 0.0])
    results = store.search(query, top_k=1)
    assert results[0][1].data == 'a'
    with pytest.raises(ValueError):
        store.add(np.array([1.0]), 'bad')

def test_procedural_memory_routine():
    pm = ProceduralMemory()
    pm.add_routine('foo', lambda: 'bar')
    routine = pm.get_routine('foo')
    assert routine() == 'bar'
    assert 'foo' in pm.list_routines()

def test_archival_memory_append(tmp_path):
    path = tmp_path / 'arch.pkl.gz'
    arch = ArchivalMemory(path)
    arch.append({'x': 1})
    data = arch.load()
    assert data == [{'x': 1}]

def test_feedback_processor_updates_weight(monkeypatch):
    controller = MemoryController()
    controller.episodic.add('event', weight=1.0)
    processor = FeedbackProcessor(controller)
    feedback = {'success': True, 'state': 'store', 'action': 'episodic', 'weight_delta': 0.5}
    processor.process(feedback)
    assert controller.episodic._events[-1].weight == pytest.approx(1.5)

def test_memory_controller_consolidate(monkeypatch):
    controller = MemoryController()
    controller.short_term = ShortTermCache(capacity=1)
    controller.short_term_threshold = 1
    monkeypatch.setattr(controller, '_choose_action', lambda state: 'short_term')
    controller.store('first')
    controller.store('second')
    assert len(controller.episodic) == 2
    assert controller.episodic._events[0].data == 'first'

def test_brain_export_memory(monkeypatch):
    brain = Brain()
    monkeypatch.setattr(brain.controller, '_choose_action', lambda state: 'short_term')
    brain.remember('hello')
    data = brain.export_memory()
    assert 'short_term' in data and data['short_term']

def test_goal_manager_flow():
    gm = GoalManager()
    gm.add_goal('high', priority=1)
    gm.add_goal('low', priority=0)
    assert gm.next_goal().description == 'high'
    gm.complete_goal('high')
    assert gm.next_goal().description == 'low'

def test_self_modification_guard():
    guard = SelfModificationGuard()
    with pytest.raises(PermissionError):
        guard.ensure_safe()
    guard.allowed = True
    guard.ensure_safe()

def test_emergency_shutdown(tmp_path):
    shutdown = EmergencyShutdown()
    phrase = EmergencyShutdown.PHRASE
    with pytest.raises(SystemExit):
        shutdown.check_phrase(f"{phrase}")
    shutdown.disarm()
    shutdown.check_phrase(phrase)  # no exception

def test_reasoning_loop_cycle(monkeypatch):
    brain = Brain()
    goals = GoalManager()
    goals.add_goal('ask for help')
    guard = SelfModificationGuard(); guard.allowed = True
    shutdown = EmergencyShutdown(); shutdown.disarm()
    loop = ReasoningLoop(brain, goals, guard=guard, shutdown=shutdown)
    result = loop.cycle('hello')
    assert result == 'ask'


def test_process_user_input_blocks_modification():
    guard = SelfModificationGuard()
    with pytest.raises(PermissionError):
        process_user_input("please change your code", guard)
    assert process_user_input("hello", guard) == "hello"
