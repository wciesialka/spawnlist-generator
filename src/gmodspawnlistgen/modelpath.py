from functools import reduce
import re

SPLIT_PATTERN = re.compile(r"[\/\\]")

class ModelPath:

    MODEL_EXTENSION = ".mdl"

    def __init__(self, key: str): 
        self.key = key
        self.models = []
        self.subpaths = {}

    def add_subpath(self, subpath: ModelPath):
        self.subpaths[subpath.key] = subpath
    
    def add_model(self, path: str, split_path = None):
        if split_path is None:
            split_path = SPLIT_PATTERN.split(path)
        # Check if the path is split into multiple parts. If it is, we have to deal
        # with subpaths. If it isn't, we have a model and can add it normally.
        if len(split) == 1:
            if not (path in self.models):
                self.models.append(path)
        else:
            # We have to deal with subpaths recursively.
            # Start from the top-most path and work our way down.
            # Add sub-paths as needed.
            if not (split[0] in self):
                child_path = ModelPath(split[0])
                self.add_subpath(child_path)
            else:
                child_path = self.get_subpath(split[0])
            child_path.add_model(path, split_path=split[1:])
    
    def get_subpath(self, key: str) -> ModelPath:
        if key in self.subpaths:
            return self.subpaths[key]
        raise KeyError(f"Subpath {key} not found in subpaths.")
    
    def remove_model(self, key: str):
        if key in self.models:
            self.models.remove(key)
        raise KeyError(f"Model {key} not found in models.")
    
    def pop_model(self, index: int):
        self.models.pop(index)
    
    def __len__(self):
        length = len(self.models)
        for subpath in self.subpaths.values():
            length += len(subpath)
        return length

    def __contains__(self, key: str) -> bool:
        # If the key ends with our model extension, check models.
        # Otherwise, check subpaths,
        if key.endswith(ModelPath.MODEL_EXTENSION):
            return key in self.models 
        else:
            return key in self.subpaths