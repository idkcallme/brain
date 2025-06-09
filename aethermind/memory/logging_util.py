import logging

logging.basicConfig(
    filename='memory.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('AetherMindMemory')
