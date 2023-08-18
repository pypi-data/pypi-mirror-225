import os
import json
import yaml
from rich.console import Console
from rich.table import Table
from pathlib import Path
from copy import deepcopy
import re
import dataclasses
import types
from collections.abc import Mapping
from warnings import warn

allowed_types = (int, float, str, bool, type(None))
allowed_iterables = (list, )

class InvalidStructureError(Exception):
    pass

class Configs(Mapping):
    def __getitem__(self, key):
        return self._storage[key]
    def __iter__(self):
        return iter(self._storage)
    def __len__(self):
        return len(self._storage)
    def __contains__(self, key):
        return key in self._storage
    def __eq__(self, other):
        if not isinstance(other, Configs):            
            return False
        return (self._storage == other._storage) and (self._is_jax_pytree == other._is_jax_pytree)
    
    def to_dict(self) -> dict:
        """Export configurations to a python dictionary.
        
        Returns:
            dict: A standard python dictionary containing the configurations.
        """
        return self._storage
    
    def to_json(self, path: os.PathLike):
        """Save configurations to a JSON file.
        
        Args:
            path (os.PathLike): File path to save the configurations.
        """        
        to_json(path, self)
    
    def to_yaml(self, path: os.PathLike):
        """Save configurations to a YAML file.
        
        Args:
            path (os.PathLike): File path to save the configurations.
        """        
        to_yaml(path, self)
    
    def to_file(self, path: os.PathLike):
        """Save configurations to a YAML/JSON file.
        
        Args:
            path (os.PathLike): File path to save the configurations.
        """        
        to_file(path, self)
    
    def tabulate(self):
        """
        Print the configurations in a tabular format.
        """        
        pprint(self)

class PytreeConfigs(Configs):    
    #JAX pytree compatibility
    def tree_flatten(self):
        return tuple(self._storage.values()), tuple(self._storage.keys())
    
    @classmethod
    def tree_unflatten(cls, aux_data, children):
        #Pop last element from aux_data
        storage = dict(zip(aux_data, children))
        return make_base_config_class(storage, register_jax_pytree=True)


def check_structure(mapping: Mapping, _ignore_jax_tracers: bool = False):
    seen = set()
    for key, value in mapping.items():
        if not isinstance(key, str):
            raise InvalidStructureError('Keys must be strings')
        if key in seen:
            raise InvalidStructureError('Duplicate keys are not allowed')
        seen.add(key)
        if isinstance(value, allowed_types):
            continue
        if isinstance(value, allowed_iterables):
            seen_types = set()
            for item in value:
                if not isinstance(item, allowed_types):
                    raise InvalidStructureError('Element types must be one of: {}'.format(allowed_types))
                seen_types.add(type(item))
            if len(seen_types) > 1:
                raise InvalidStructureError('Lists must be homogenous')
            continue

        if _ignore_jax_tracers:
            try:
                from jax.core import Tracer
                if isinstance(value, Tracer):
                    continue
            except ImportError:
                warn('The argument `_ignore_jax_tracers` will be ingored, as jax is not installed.')
                continue
        
        error_str = f"The element {key} is of type {type(value)} while it must be one of:\n"
        for t in allowed_types:
            error_str += f"\t{t.__name__}\n"
        raise InvalidStructureError(error_str)  

def make_base_config_class(storage: dict, register_jax_pytree: bool = True):

    #JAX pytree compatibility
    if register_jax_pytree:
        _ignore_jax_tracers = True
    else:
        _ignore_jax_tracers = False
    
    check_structure(storage, _ignore_jax_tracers=_ignore_jax_tracers)
    defaults = {}
    annotations = {}
    for key, value in storage.items():
        annotations[key] = type(value)
    annotations['_storage'] = dict
    annotations['_is_jax_pytree'] = bool
    def exec_body_callback(ns):
        ns.update(defaults)
        ns['__annotations__'] = annotations

    storage['_storage'] = deepcopy(storage)
    if register_jax_pytree:    
        cls = types.new_class('LoadedConfigs', (PytreeConfigs,), {}, exec_body_callback)
        cls = dataclasses.dataclass(cls, frozen=True, eq=False)
        try:
            from jax.tree_util import register_pytree_node_class
            cls = register_pytree_node_class(cls)
            storage['_is_jax_pytree'] = True
        except ImportError:
            warn('Unable to import JAX. The argument `register_jax_pytree` will be ignored. To suppress this warning, load the configurations with `register_jax_pytree=False`.')
            cls = types.new_class('LoadedConfigs', (Configs,), {}, exec_body_callback)
            cls = dataclasses.dataclass(cls, frozen=True, eq=False)
            storage['_is_jax_pytree'] = False
    else:
        cls = types.new_class('LoadedConfigs', (Configs,), {}, exec_body_callback)
        cls = dataclasses.dataclass(cls, frozen=True, eq=False)
        storage['_is_jax_pytree'] = False
    
    return cls(**storage)


#Fix for yaml scientific notation https://stackoverflow.com/questions/30458977/yaml-loads-5e-6-as-string-and-not-a-number
loader = yaml.SafeLoader
loader.add_implicit_resolver(
    u'tag:yaml.org,2002:float',
    re.compile(u'''^(?:
     [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
    |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
    |\\.[0-9_]+(?:[eE][-+][0-9]+)?
    |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
    |[-+]?\\.(?:inf|Inf|INF)
    |\\.(?:nan|NaN|NAN))$''', re.X),
    list(u'-+0123456789.'))

def create_base_dir(path: os.PathLike):
    path = Path(path)
    base_path = path.parent
    if not base_path.exists():
        base_path.mkdir(parents=True)

def from_json(path: os.PathLike, register_jax_pytree: bool = True):
    """Load configurations from a JSON file.

    Args:
        path (os.PathLike): Configuration file path.
        register_jax_pytree (bool, optional): Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False.

    Returns:
        Configs: Instance of the loaded configurations.
    """
    with open(path, 'r') as f:
        storage = json.load(f)
    return make_base_config_class(storage, register_jax_pytree)

def from_yaml(path: os.PathLike, register_jax_pytree: bool = True):
    """Load configurations from a YAML file.

    Args:
        path (os.PathLike): Configuration file path.
        register_jax_pytree (bool, optional): Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False.

    Returns:
        Configs: Instance of the loaded configurations.
    """    
    with open(path, 'r') as f:
        storage = yaml.load(f, Loader=loader)
    return make_base_config_class(storage, register_jax_pytree)

def from_dict(storage: dict, register_jax_pytree: bool = True):
    """Load configurations from a python dictionary.

    Args:
        storage (dict): Configuration dictionary.
        register_jax_pytree (bool, optional): Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False.

    Returns:
        Configs: Instance of the loaded configurations.
    """
    storage = deepcopy(storage)
    return make_base_config_class(storage, register_jax_pytree)

def from_file(path: os.PathLike, register_jax_pytree: bool = True):
    """Load configurations from a YAML/JSON file.

    Args:
        path (os.PathLike): Configuration file path.
        register_jax_pytree (bool, optional): Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False.

    Returns:
        Configs: Instance of the loaded configurations.
    """
    path = str(path)
    if path.endswith('.json'):
        return from_json(path, register_jax_pytree)
    elif path.endswith('.yaml') or path.endswith('.yml'):
        return from_yaml(path, register_jax_pytree)
    else:
        raise ValueError('File extension must be one of: .json, .yaml, .yml')

def to_json(path: os.PathLike, configs: Configs):
    """Save configurations to a JSON file.

    Args:
        path (os.PathLike): File path to save the configurations.
        configs (Configs): Instance of the configurations.
    """    
    path = str(path)
    assert path.endswith('.json'), 'File extension must be .json'
    create_base_dir(path)
    with open(path, 'w') as f:
        json.dump(configs._storage, f, indent=4)

def to_yaml(path: os.PathLike, configs: Configs):
    """Save configurations to a YAML file.

    Args:
        path (os.PathLike): File path to save the configurations.
        configs (Configs): Instance of the configurations.
    """
    path = str(path)
    assert path.endswith('.yaml') or path.endswith('.yml'), 'File extension must be .yaml or .yml'
    create_base_dir(path)
    with open(path, 'w') as f:
        yaml.safe_dump(configs._storage, f)

def to_file(path: os.PathLike, configs: Configs):
    """Save configurations to a YAML/JSON file.

    Args:
        path (os.PathLike): File path to save the configurations.
        configs (Configs): Instance of the configurations.
    """
    path = str(path)
    if path.endswith('.json'):
        to_json(path, configs)
    elif path.endswith('.yaml') or path.endswith('.yml'):
        to_yaml(path, configs)
    else:
        raise ValueError('File extension must be one of: .json, .yaml, .yml')

def to_dict(configs: Configs) -> dict:
    """Export configurations to a python dictionary.

    Args:
        configs (Configs): Instance of the configurations.

    Returns:
        dict: A standard python dictionary containing the configurations.
    """    
    return configs._storage

def pprint(configs: Configs):
    """Pretty print configurations.

    Args:
        configs (Configs): An instance of the configurations.
    """    
    console = Console()
    table = Table(show_header=True, header_style="bold")
    table.add_column("Key")
    table.add_column("Value")
    table.add_column("Type")

    for key, value in configs._storage.items():
        if isinstance(value, list):
            value_str = '['
            value_str += ', '.join(str(item) for item in value)
            value_str += ']'
            value_type = r"list\[" + f"{type(value[0]).__name__}]"            
        else:
            value_str = str(value)
            value_type = type(value).__name__
        
        table.add_row(str(key), value_str, value_type)
    console.print(table)