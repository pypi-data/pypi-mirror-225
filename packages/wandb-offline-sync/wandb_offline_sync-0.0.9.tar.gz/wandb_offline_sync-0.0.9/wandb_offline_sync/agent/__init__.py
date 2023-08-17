from wandb_offline_sync.agent.wandb_sync_agent import SyncAgent

agent = SyncAgent()
init = agent.init
trigger_sync = agent.trigger_sync
finish_sync = agent.finish_sync

__all__ = [
    'agent',
    'init',
    'trigger_sync',
    'finish_sync'
    ]