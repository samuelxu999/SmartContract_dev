import json
import requests
import argparse
import sys
import hashlib
from datetime import date, timedelta

## This class implement merkle tree operation
class MerkleTree:
    def __init__(self, data_blocks):
        self.data_blocks = data_blocks
        self.tree = self.build_tree(data_blocks)

    def build_tree(self, data_blocks):
         # Hash the data blocks
        hashed_data_blocks = [hashlib.sha256(block.encode('utf-8')).hexdigest() for block in data_blocks]
        if len(hashed_data_blocks) == 0:
            return None
        
        # Build the tree
        while len(hashed_data_blocks) > 1:
            if len(hashed_data_blocks) % 2 != 0:
                hashed_data_blocks.append(hashed_data_blocks[-1])
            new_level = []
            for i in range(0, len(hashed_data_blocks), 2):
                combined_hash = hashlib.sha256((hashed_data_blocks[i] + hashed_data_blocks[i+1]).encode('utf-8')).hexdigest()
                new_level.append(combined_hash)
            hashed_data_blocks = new_level
        return hashed_data_blocks[0]

    def get_root(self):
        return self.tree
