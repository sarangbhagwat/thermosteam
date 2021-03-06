# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
import pytest
from numpy.testing import assert_allclose

def test_stream():
    import thermosteam as tmo
    tmo.settings.set_thermo(['Water'], cache=True)
    stream = tmo.Stream(None, Water=1, T=300)
    assert [stream.chemicals.Water] == stream.available_chemicals
    assert_allclose(stream.epsilon, 77.72395675564552)
    assert_allclose(stream.alpha * 1e6, 0.1462889847474686)
    assert_allclose(stream.nu, 8.596760626756933e-07)
    assert_allclose(stream.Pr, 5.876560454361681)
    assert_allclose(stream.Cn, 75.29555729396768)
    assert_allclose(stream.C, 75.29555729396768)
    assert_allclose(stream.Cp, 4.179538552493643)
    assert_allclose(stream.P_vapor, 3533.918074415897)
    assert_allclose(stream.mu, 0.0008564676992124578)
    assert_allclose(stream.kappa, 0.609138593165859)
    assert_allclose(stream.rho, 996.2679390499142)
    assert_allclose(stream.V, 1.808276598480142e-05)
    assert_allclose(stream.H, 139.3139852692184)
    assert_allclose(stream.S, 0.4658177637668395)
    assert_allclose(stream.sigma, 0.07168596252716256)
    assert_allclose(stream.z_mol, [1.0])
    assert_allclose(stream.z_mass, [1.0])
    assert_allclose(stream.z_vol, [1.0])
    assert not stream.source
    assert not stream.sink
    assert stream.main_chemical == 'Water'
    assert not stream.isfeed()
    assert not stream.isproduct()
    assert stream.vapor_fraction == 0.
    with pytest.raises(ValueError):
        stream.get_property('isfeed', 'kg/hr')
    with pytest.raises(ValueError):
        stream.set_property('invalid property', 10, 'kg/hr')
    with pytest.raises(ValueError):
        tmo.Stream(None, Water=1, units='kg')
    
    stream.mol = 0.
    stream.mass = 0.
    stream.vol = 0.
    
    with pytest.raises(AttributeError):
        stream.F_mol = 1.
    with pytest.raises(AttributeError):
        stream.F_mass = 1.
    with pytest.raises(AttributeError):
        stream.F_vol = 1.
        
def test_multistream():
    import thermosteam as tmo
    tmo.settings.set_thermo(['Water'], cache=True)
    stream = tmo.MultiStream(None, l=[('Water', 1)], T=300)
    assert [stream.chemicals.Water] == stream.available_chemicals
    assert_allclose(stream.epsilon, 77.72395675564552)
    assert_allclose(stream.alpha * 1e6, 0.1462889847474686)
    assert_allclose(stream.nu, 8.596760626756933e-07)
    assert_allclose(stream.Pr, 5.876560454361681)
    assert_allclose(stream.Cn, 75.29555729396768)
    assert_allclose(stream.C, 75.29555729396768)
    assert_allclose(stream.Cp, 4.179538552493643)
    assert_allclose(stream.P_vapor, 3533.918074415897)
    assert_allclose(stream.mu, 0.0008564676992124578)
    assert_allclose(stream.kappa, 0.609138593165859)
    assert_allclose(stream.rho, 996.2679390499142)
    assert_allclose(stream.V, 1.808276598480142e-05)
    assert_allclose(stream.H, 139.3139852692184)
    assert_allclose(stream.S, 0.4658177637668395)
    assert_allclose(stream.sigma, 0.07168596252716256)
    assert_allclose(stream.z_mol, [1.0])
    assert_allclose(stream.z_mass, [1.0])
    assert_allclose(stream.z_vol, [1.0])
    assert not stream.source
    assert not stream.sink
    assert stream.main_chemical == 'Water'
    assert not stream.isfeed()
    assert not stream.isproduct()
    assert stream.vapor_fraction == 0.
    with pytest.raises(ValueError):
        stream.get_property('isfeed', 'kg/hr')
    with pytest.raises(ValueError):
        stream.set_property('invalid property', 10, 'kg/hr')
    with pytest.raises(ValueError):
        tmo.MultiStream(None, l=[('Water', 1)], units='kg')
    
    stream.empty()
    
    with pytest.raises(AttributeError):
        stream.mol = 1.
    with pytest.raises(AttributeError):
        stream.mass = 1.
    with pytest.raises(AttributeError):
        stream.vol = 1.
    with pytest.raises(AttributeError):
        stream.F_mol = 1.
    with pytest.raises(AttributeError):
        stream.F_mass = 1.
    with pytest.raises(AttributeError):
        stream.F_vol = 1.
    
