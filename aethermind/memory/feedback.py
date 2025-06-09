from typing import Any
from .logging_util import logger

class FeedbackProcessor:
    """Processes feedback to update the RL policy and memory."""

    def __init__(self, controller: 'MemoryController'):
        self.controller = controller

    def process(self, feedback: dict):
        success = feedback.get('success', True)
        reward = 1.0 if success else -1.0
        state = feedback.get('state', 'store')
        action = feedback.get('action')
        if action:
            self.controller._update_q(state, action, reward)
        logger.info(f"Processed feedback: {feedback}")
