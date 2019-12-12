# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 04:12:27 2019

@author: yoelr
"""
import thermosteam as tmo

__all__ = ('settings',)

class Settings:
    __slots__ = ('_thermo',
                 '_phase_equivalents',
                 '_phase_name',
                 '_debug')
    
    def __init__(self):
        self._thermo = None
        self._debug = __debug__
        self._phase_name = {'s': 'Solid',
                            'l': 'Liquid',
                            'g': 'Gas'}
        self._phase_equivalents = {'S': 's',
                                   'L': 'l',
                                   'G': 'g',
                                   'V': 'g',
                                   'v': 'g'}
    
    @property
    def debug(self):
        return self._debug
    @debug.setter
    def debug(self, debug):
        self._debug = bool(debug)
    
    @property
    def phase_name(self):
        return self._phase_name
    @property
    def phase_equivalents(self):
        return self._phase_equivalents
    
    def get_thermo(self, thermo):
        if not thermo:
            thermo = settings.thermo
            assert thermo, ("no available 'Thermo' object; "
                            "set ether.settings.thermo first")
        return thermo
    
    def get_chemicals(self, chemicals):
        if isinstance(chemicals, tmo.Chemicals):
            chemicals.compile()
        if not chemicals:
            thermo = settings._thermo
            assert thermo, "no available 'Thermo' object"
            chemicals = thermo.chemicals
        else:
            chemicals = tmo.Chemicals(chemicals)
            chemicals.compile()
        return chemicals
    
    def get_mixture(self, mixture):
        if not mixture:
            thermo = settings.thermo
            assert thermo, ("no available 'Thermo' object; "
                            "set ether.settings.thermo first")
            mixture = thermo.mixture
        return mixture
    
    @property
    def thermo(self):
        return self._thermo
    @thermo.setter
    def thermo(self, thermo):
        if isinstance(thermo, tmo.Thermo):
            self._thermo = thermo
        else:
            raise ValueError("thermo must be a 'Thermo' object, "
                            f"not a '{type(thermo).__name__}'")
    
    def __repr__(self):
        return "ether.settings"
    
settings = Settings()