# HaloFactory - Semi-analytical dark matter halo generators

[![Last commit](https://img.shields.io/github/last-commit/ChenYangyao/halofactory/master)](https://github.com/ChenYangyao/halofactory/commits/master)
[![Workflow Status](https://img.shields.io/github/actions/workflow/status/ChenYangyao/halofactory/python-package.yml)](https://github.com/ChenYangyao/halofactory/actions/workflows/python-package.yml)
[![MIT License](https://img.shields.io/badge/License-MIT-blue)](https://github.com/ChenYangyao/halofactory/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/halofactory)](https://pypi.org/project/halofactory/)

In astrophysics, it is known that dark matter halos building blocks of the Universe's large-scale structures. 
Given their significance in theoretical and numerical studies of galaxy formation, 
it is imperative to generate halo catalogs not only following closely to 
structure formation theory but also being efficient in computation. 

This repository presents a comprehensive collection of semi-analytical methods 
that facilitate the generation of halo catalogs and their corresponding merger trees. 
These methods are either purely theoretical or calibrate by numerical simulations.
Building upon this repository, we intend to publish another repository dedicated 
to "semi-analytical galaxy formation models", which will utilize the 
halo-to-galaxy connection to populate halos with galaxies.

It is important to note that this package is currently in the process of being 
developed and is subject to structural modifications and functional expansions. 
The documentation is currently empty, and the testing does not encompass the 
entire source tree. We will continue to work towards completing these aspects.

Dependencies:
- Python>=3.9.
- [pyhipp](https://github.com/ChenYangyao/pyhipp)>=0.0.2, scipy, numpy.

To install `halofactory` and automatically handle the dependencies, use `PyPI`:
```bash
pip install halofactory
```

## Interesting Features

**Halo Density Profile**. HaloFactory predefines a set of density profiles for 
halos. For example, the following codes defines an NFW profile instance:
```py
>>> from halofactory.profile import NFWProfile
>>> profile = NFWProfile(mass = 1.0e2, rs = 10.0)
>>> profile

{'type': 'NFWProfile',
 '_meta': {'mass': 100.0, 'rin': 0.0001, 'xin': 1e-05, 'rvir': 150.0, ... },
 '_us': {'u_l': '3.085677581491367e+19 m', 'u_t': '3.085677581491367e+16 s',
         'u_m': '1.988409870698051e+40 kg', ...}}
```
The printed message includes the metainfo (mass, virial radius, etc.) of the halo, 
as well as the unit system in use.

To find information of the profile at given radii, for example, the density, write:
```py
>>> profile.rho([1., 2., 3.])

array([0.03583832, 0.01505707, 0.00855313])
```

To sample from the profile and thus create a set of particles used as input for 
N-body simulation, define a sampler such as the Eddington Inversion sampler:
```py
>>> from halofactory.initial_condition import EddInv
>>> sampler = EddInv(profile)
>>> sampler

{'type': 'EddInv',
 '_profile': {'type': 'NFWProfile', ...},
 '_rng': <pyhipp.stats.random.Rng object at 0x15092bc90>,
 '_meta': {'mass': 100.00000000000001, 'Et': 0.0, 'm_hi': 1.0, ...}}
```
The message indicates the method of the sampler, the input profile, the random 
number generator, and various of metadata.

To generate a sample, e.g., 1000 particles, write:
```py
>>> sample = sampler.get(1000)
>>> sample.pos, sample.vel, sample.mass

(array([[-27.04020173,  60.70242802,  -6.84922322], ...]),
 array([[  12.7955374 , -114.31584255,   30.89851955],...]),
 0.10000000000000002)
```
The returned `sample` instance contains positions, velocities and mass of the sampled 
particles.

**More is coming ...**