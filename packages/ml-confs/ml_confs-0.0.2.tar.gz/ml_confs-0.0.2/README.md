# ML configurations
A small, highly opinionated `python` tool to handle configurations for machine learning pipelines.
The library is designed to load configurations from both `json` and `yaml` files, as well as from standard python dictionaries.
## Design rules
The configurations, once loaded are frozen. Each configuration file can contain only `int`, `float`, `str`, `bool` and `None` fields, as well as _homogeneous_ lists of one of the same types. That's all. No nested structures are allowed.
## Installation
ML configurations can be installed directly from `git` by running
```
pip install ml-confs
```

## Basic usage
A valid `ml_confs` configuration file `configs.yml` in YAML is:
```yaml
int_field: 1
float_field: 1.0
str_field: 'string'
bool_field: true
none_field: null
list_field: [1, 2, 3]
```
To load it we just use:
```python
import ml_confs

#Loading configs
configs = ml_confs.from_file('configs.yml')

#Accessing configs with dot notation
print(configs.int_field) # >>> 1

#Additionally, one can use the ** notation to unpack the configurations
def foo(**kwargs):
    # Do stuff...
foo(**configs)


#Saving configs to json format
configs.to_file('json_configs_copy.json') #Will create a .json file 
```

One can also pretty print a loaded configuration with `configs.tabulate()`, which in the previous example would output:
```
┏━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Key         ┃ Value     ┃ Type      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ int_field   │ 1         │ int       │
│ float_field │ 1.0       │ float     │
│ str_field   │ string    │ str       │
│ bool_field  │ True      │ bool      │
│ none_field  │ None      │ NoneType  │
│ list_field  │ [1, 2, 3] │ list[int] │
└─────────────┴───────────┴───────────┘
```
### JAX Pytree registration
By default, `ml_confs` will try to register the configuration object as a JAX pytree, so that `configs` can be safely used with JAX transformations.
```python
import ml_confs
import jax

configs = mlc.from_dict({'exp': 1.5})

@jax.jit 
def power_fn(x, cfg):
    return x**cfg.exp

assert f(2.0, configs) == 2.0**exp # This works!
assert jax.grad(power_fn)(3.0, configs) == 3.0**(exp - 1.0) * exp # This works too!
```
 If JAX is not installed the following warning will be displayed:

 `Unable to import JAX. The argument register_jax_pytree will be ignored. To suppress this warning, load the configurations with register_jax_pytree=False.`
 
 If one is not interested in this feature, the warning can be silenced by explicitly setting  `register_jax_pytree` to `False` upon configuration loading.

# API Reference

<!-- markdownlint-disable -->


<a href="../../ml_confs/lib.py#L177"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `ml_confs.from_json`

```python
from_json(path: os.PathLike, register_jax_pytree: bool = True)
```

Load configurations from a JSON file. 



**Args:**
 
 - <b>`path`</b> (os.PathLike):  Configuration file path. 
 - <b>`register_jax_pytree`</b> (bool, optional):  Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False. 



**Returns:**
 
 - <b>`Configs`</b>:  Instance of the loaded configurations. 


---

<a href="../../ml_confs/lib.py#L191"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `ml_confs.from_yaml`

```python
from_yaml(path: os.PathLike, register_jax_pytree: bool = True)
```

Load configurations from a YAML file. 



**Args:**
 
 - <b>`path`</b> (os.PathLike):  Configuration file path. 
 - <b>`register_jax_pytree`</b> (bool, optional):  Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False. 



**Returns:**
 
 - <b>`Configs`</b>:  Instance of the loaded configurations. 


---

<a href="../../ml_confs/lib.py#L205"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `ml_confs.from_dict`

```python
from_dict(storage: dict, register_jax_pytree: bool = True)
```

Load configurations from a python dictionary. 



**Args:**
 
 - <b>`storage`</b> (dict):  Configuration dictionary. 
 - <b>`register_jax_pytree`</b> (bool, optional):  Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False. 



**Returns:**
 
 - <b>`Configs`</b>:  Instance of the loaded configurations. 


---

<a href="../../ml_confs/lib.py#L218"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `ml_confs.from_file`

```python
from_file(path: os.PathLike, register_jax_pytree: bool = True)
```

Load configurations from a YAML/JSON file. 



**Args:**
 
 - <b>`path`</b> (os.PathLike):  Configuration file path. 
 - <b>`register_jax_pytree`</b> (bool, optional):  Register the configuration as a `JAX` pytree. This allows the configurations to be safely used in `JAX`'s transformations.. Defaults to False. 



**Returns:**
 
 - <b>`Configs`</b>:  Instance of the loaded configurations. 



---

<a href="../../ml_confs/lib.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Configs`


---

<a href="../../ml_confs/lib.py#L66"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Configs.tabulate`

```python
tabulate()
```

Print the configurations in a tabular format. 

---

<a href="../../ml_confs/lib.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Configs.to_dict`

```python
to_dict() → dict
```

Export configurations to a python dictionary. 



**Returns:**
 
 - <b>`dict`</b>:  A standard python dictionary containing the configurations. 

---

<a href="../../ml_confs/lib.py#L58"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Configs.to_file`

```python
to_file(path: os.PathLike)
```

Save configurations to a YAML/JSON file. 



**Args:**
 
 - <b>`path`</b> (os.PathLike):  File path to save the configurations. 

---

<a href="../../ml_confs/lib.py#L42"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Configs.to_json`

```python
to_json(path: os.PathLike)
```

Save configurations to a JSON file. 



**Args:**
 
 - <b>`path`</b> (os.PathLike):  File path to save the configurations. 

---

<a href="../../ml_confs/lib.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `Configs.to_yaml`

```python
to_yaml(path: os.PathLike)
```

Save configurations to a YAML file. 



**Args:**
 
 - <b>`path`</b> (os.PathLike):  File path to save the configurations. 

---

_The API reference was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._

