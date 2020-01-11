# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 04:26:20 2019

@author: yoelr
"""
from .units_of_measure import chemical_units_of_measure, definitions, types
from ..utils import var_with_units, get_obj_values
from .documenter import autodoc_functor
from inspect import signature

__all__ = ("Functor", "MixtureFunctor", 
           "TFunctor", "TPFunctor", "TIntegralFunctor",
           "zTFunctor", "zTPFunctor",
           "functor", 'H', 'S', 'V', 'Cn', 'mu', 'kappa', 'sigma', 'delta', 'epsilon',
           'Psat', 'Hvap', 'display_asfunctor', 'functor_lookalike',
           'functor_matching_params', 'functor_base_and_params',)

RegisteredArgs = set()
RegisteredFunctors = []

# %% Utilities

def functor_name(functor):
    return functor.__name__ if hasattr(functor, "__name__") else type(functor).__name__

def display_asfunctor(functor, var=None, name=None, show_var=True):
    name = name or functor_name(functor)
    info = f"{name}{str(signature(functor)).replace('self, ', '')}"
    var = var or (functor.var if hasattr(functor, 'var') else None)
    units = functor.units_of_measure if hasattr(functor, "units_of_measure") else chemical_units_of_measure
    if var:
        if show_var:
            info += f" -> " + var_with_units(var, units)
        else:
            name, *_ = var.split('.')
            u = units.get(name)
            if u: info += f" -> {u}"
    return info

def functor_lookalike(cls):
    cls.__repr__ = Functor.__repr__
    cls.__str__ = Functor.__str__
    return cls

def functor_matching_params(params):
    length = len
    N_total = length(params)
    for base in RegisteredFunctors:
        args = base._args
        N = length(args)
        if N > N_total: continue
        if args == params[:N]: return base
    raise ValueError("could not match function signature to registered functors")

def functor_base_and_params(function):
    params = tuple(signature(function).parameters)
    base = functor_matching_params(params)
    return base, params[len(base._args):]


# %% Decorator
  
def functor(function=None, var=None, wrap=None, **autodoc):
    """Return a Functor subclass from function."""
    if function:
        base, params = functor_base_and_params(function)
        dct = {'__slots__': (),
               'function': staticmethod(function),
               'params': params,
               'var': var}
        cls = type(function.__name__, (base,), dct)
        cls._autodoc_ = autodoc
        if wrap: cls.wrapper(wrap, **autodoc)
        elif autodoc: autodoc_functor(cls, **autodoc)
        cls.__module__ = function.__module__
        return cls
    else:
        return lambda function: functor(function, var, wrap, **autodoc)


# %% Decorators
    
class FunctorFactory:
    __slots__ = ('var',)
   
    def __init__(self, var):
        self.var = var
    
    def __call__(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var, wrap, **autodoc)
    
    def s(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var + '.s', wrap, **autodoc)
    
    def l(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var + '.l',  wrap, **autodoc)
    
    def g(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var + '.g', wrap, **autodoc)
    
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.var)})"
    
H, S, Cn, V, kappa, mu, Psat, Hvap, sigma, delta, epsilon = [FunctorFactory(i) for i in
                                                             ('H', 'S', 'Cn', 'V', 'kappa',
                                                              'mu', 'Psat', 'Hvap',
                                                              'sigma', 'delta', 'epsilon')]


# %% Functors

class Functor: 
    __slots__ = ()
    units_of_measure = chemical_units_of_measure
    definitions = definitions
    types = types
    
    def __init_subclass__(cls, args=None, before=None, after=None):
        if args and not hasattr(cls, 'function'):
            args = tuple(args)
            assert args not in RegisteredArgs, f"abstract functor with args={args} already implemented"
            if before:
                index = RegisteredFunctors.index(before)
            elif after:
                index = RegisteredFunctors.index(after) + 1
            else:
                index = 0
            RegisteredFunctors.insert(index, cls)
            RegisteredArgs.add(args)
            cls._args = args
    
    def __str__(self):
        return display_asfunctor(self)
    
    def __repr__(self):
        return f"<{self}>"


class PureComponentFunctor(Functor):
    __slots__ = ('function_kwargs', '_data')
    
    def __init__(self, *args, **kwargs):
        for i, j in zip(self.params, args): kwargs[i] = j
        self.set_data(kwargs)
    
    def _load_data(self, data):
        self.function_kwargs = self.wrap(**data) if hasattr(self, 'wrap') else data
    
    def get_data(self):
        return self._data.copy()
    
    def set_data(self, data):
        self._data = data
        self._load_data(data)
    
    def update_data(self, **kwargs):
        data = self._data
        data.update(kwargs)
        self._load_data(data)
    
    @classmethod
    def from_other(cls, other):
        self = cls.__new__(cls)
        self._data = other._data
        self.function_kwargs = other.function_kwargs
        return self
    
    @classmethod
    def from_args(cls, data):
        self = cls.__new__(cls)
        self.set_data(dict(zip(self.params, data)))
        return self
    
    @classmethod
    def from_kwargs(cls, data):
        self = cls.__new__(cls)
        self.set_data(data)
        return self
    
    @classmethod
    def from_obj(cls, data):
        self = cls.__new__(cls)
        self.set_data(dict(zip(self.params, get_obj_values(data, self.params))))
        return self
    
    @classmethod
    def wrapper(cls, wrap=None, **autodoc):
        if wrap:
            cls.params = tuple(signature(wrap).parameters)
            cls.wrap = staticmethod(wrap)
            autodoc_options = autodoc or cls._autodoc_
            if autodoc_options: autodoc_functor(cls, **autodoc_options)
            return cls
        else:
            return lambda wrap: cls.wrapper(wrap, **autodoc)
    
    def show(self):
        info = f"Functor: {display_asfunctor(self)}"
        data = self._data
        units = self.units_of_measure
        for key, value in data.items():
            if value is None:
                info += f"\n {key}: {value}"
                continue
            else:
                try:
                    info += f"\n {key}: {value:.5g}"
                except:
                    info += f"\n {key}: {value}"    
                else:
                    key, *_ = key.split('_')
                    u = units.get(key) or chemical_units_of_measure.get(key)
                    if u: info += ' ' + str(u)
        print(info)
        
    _ipython_display_ = show


class TFunctor(PureComponentFunctor, args=('T',)):
    __slots__ = ()
    kind = "functor of temperature (T; in K)"
    def __call__(self, T, P=None):
        return self.function(T, **self.function_kwargs)


class TIntegralFunctor(PureComponentFunctor, args=('Ta', 'Tb')):
    __slots__ = ()
    kind = "temperature integral functor (Ta to Tb; in K)"
    def __call__(self, Ta, Tb, P=None):
        return self.function(Ta, Tb, **self.function_kwargs)

# class PIntegralFunctor(PureComponentFunctor, args=('Pa', 'Pb', 'T')):
#     __slots__ = ()
    
#     def __call__(self, Pa, Pb, T):
#         return self.function(Pa, Pb, T, **self.kwargs)


class TPFunctor(PureComponentFunctor, args=('T', 'P')):
    __slots__ = ()
    kind = "functor of temperature (T; in K) and pressure (P; in Pa)"
    def __call__(self, T, P):
        return self.function(T, P, **self.function_kwargs)


class MixtureFunctor(Functor):
    __slots__ = ('function_kwargs', '_chemicals')
    
    def __init__(self, chemicals, function_kwargs=None):
        chemicals = tuple(chemicals)
        if function_kwargs:
            self._chemicals = chemicals
            self.function_kwargs = function_kwargs
        else:
            self.chemicals = chemicals
    
    @classmethod
    def wrap(cls, kwargs):
        cls.calculate_kwargs = staticmethod(kwargs)
        return cls
    
    @property
    def chemicals(self):
        return self._chemicals
    
    @chemicals.setter
    def chemicals(self, chemicals):
        if chemicals == self._chemicals: return
        self._chemicals = chemicals = tuple(chemicals)
        if chemicals in self.cache:
            self.function_kwargs = self.cache[chemicals]
        else:
            self.cache[chemicals] = self.function_kwargs = self.calculate_kwargs(self.chemicals)
            
    
class zTFunctor(MixtureFunctor, args=('z', 'T')): 
    __slots__ = ()
    kind = "functor of composition (z) and temperature (T; in K)"
    def __init_subclass__(self):
        self.cache = {}
    
    def __call__(self, z, T, P=None):
        return self.function(z, T, **self.function_kwargs)
        

class zTPFunctor(MixtureFunctor, args=('z', 'T', 'P')):
    __slots__ = ()
    kind = "functor of composition (z), temperature (T; in K) and pressure (P; in Pa)"
    def __init_subclass__(self):
        self.cache = {}
    
    def __call__(self, z, T, P):
        return self.function(z, T, P, **self.function_kwargs)
    
    
    
    