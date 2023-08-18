import pytest
import jax
import ml_confs as mlc
from pathlib import Path

tests_path = Path(__file__).parent
configs_path = tests_path / 'test_configs/valid_conf.yaml'

@pytest.mark.parametrize('register_jax_pytree', [True, False])
def test_tree_properties(register_jax_pytree):
    configs = mlc.from_file(configs_path, register_jax_pytree=register_jax_pytree)
    if register_jax_pytree:     
        childs, aux = configs.tree_flatten()
        assert len(childs) == len(aux)
        assert dict(zip(aux, childs)) == configs._storage
    else: 
        with pytest.raises(AttributeError):
            configs.tree_flatten()

def test_tree_flatten_unflatten():
    configs = mlc.from_file(configs_path)
    leafs, treedef = jax.tree_util.tree_flatten(configs)
    configs_reconstructed = jax.tree_util.tree_unflatten(treedef, leafs)
    assert configs == configs_reconstructed 

@pytest.mark.parametrize('exp', [0.0, 1.0, 2.0, 3.0, 4.0])    
def test_jit(exp):
    configs = mlc.from_dict({'exp': exp})
    def _f(x, cfg):
        return x**cfg.exp
    f = jax.jit(_f)
    assert f(2.0, configs) == 2.0**exp

@pytest.mark.parametrize('exp', [0.0, 1.0, 2.0, 3.0, 4.0])    
def test_jit_grad(exp):
    configs = mlc.from_dict({'exp': exp})
    def _f(x, cfg):
        return x**cfg.exp
    f = jax.jit(_f)
    grad_f = jax.grad(f)
    assert grad_f(3.0, configs) == 3.0**(exp - 1.0) * exp