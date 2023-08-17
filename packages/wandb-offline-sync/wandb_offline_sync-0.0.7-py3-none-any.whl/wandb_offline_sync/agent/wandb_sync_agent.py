import requests
import os
import wandb
import time
import sys

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

HOSTNAME = os.environ.get('WANDB_SYNC_FARM_HOST', 'localhost')
PORT = os.environ.get('WANDB_SYNC_FARM_PORT', 57891)
WANDB_SYNC_FARM_USERNAME = os.environ.get('WANDB_SYNC_FARM_USERNAME', 'user')
WANDB_SYNC_FARM_PASSWORD = os.environ.get('WANDB_SYNC_FARM_PASSWORD', 'pass')

class SyncAgent:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
            return cls.instance
    
    def init(self, frequency=300, timeout=5, force_wait_time=30, verbose=False):
        self.frequency = frequency
        self.timeout = timeout
        self.verbose = verbose
        self.force_wait_time = force_wait_time

        try:
            self.run_id = wandb.run.id
            self.run_dir = wandb.run.dir.removesuffix('/files')
            self.data = {
                'run_id': self.run_id,
                'run_dir': self.run_dir.removesuffix('/files'),
            }
            self.old_time = time.time()
        except:
            print('SYNC FARM AGENT - ERROR: wandb is not initialized. Call wandb.init() before initializing the agent', file=sys.stderr)
    
    def trigger_sync(self, force=False):
        if not hasattr(self, 'run_id'):
            print('WANDB SYNC FARM AGENT - ERROR: agent is not initialized. Call agent.init() before triggering sync', file=sys.stderr)
            return
    
        if force:
            if self.verbose:
                print('WANDB SYNC FARM AGENT - Forcing sync')
                print(f'WANDB SYNC FARM AGENT - Waiting for {self.force_wait_time} seconds before requesting sync')
            time.sleep(self.force_wait_time)
            self.old_time = time.time()
            self._request_sync()
            return
        
        if not force and (time.time() - self.old_time) < self.frequency:
            if self.verbose:
                print('WANDB SYNC FARM AGENT - The time interval between syncs has not passed. Not triggering sync')
            return
        
        self.old_time = time.time()
        try:
            self._request_sync()
        
        except Exception as e:
            if self.verbose:
                print('WANDB SYNC FARM AGENT - ERROR: sync farm not responding', file=sys.stderr)
                print(e)
        
    def _request_sync(self):
        if self.verbose:
            print('WANDB SYNC FARM AGENT - Sending sync request')
        r = requests.post(f'https://{HOSTNAME}:{PORT}/sync', verify=False,
                auth=(WANDB_SYNC_FARM_USERNAME, WANDB_SYNC_FARM_PASSWORD),
                data=self.data, timeout=self.timeout)
        return r
        