import numpy as np
import scipy.optimize as opt
from .profile import HaloProfile
from pyhipp.core.abc import HasLog, HasDictRepr
from pyhipp.core import DataDict, dataproc as dp
from pyhipp.stats.random import Rng
from typing import Tuple, Union, Any, Optional
from dataclasses import dataclass

@dataclass
class ParticleSample:
    '''
    @vel: None if passing requires_vel = False to the sampler.
    '''
    pos:    np.ndarray
    vel:    Optional[np.ndarray]
    mass:   Union[float, np.ndarray] 

class InitialCondition(HasDictRepr, HasLog):
    '''
    Subclasses must implement get() and add mass, m_lo, m_hi to _meta.
    '''
    repr_attr_keys = ('_profile', '_rng', '_meta')
    
    def __init__(self, profile: HaloProfile, seed: Union[int, None, Rng] = 0, 
                 **base_kw) -> None:
        
        super().__init__(**base_kw)
        
        self._profile = profile
        self._rng = Rng(seed)
        self._meta = DataDict()
        
    def __getitem__(self, key: Union[str, Tuple[str, ...]]) -> Any:
        return self._meta[key]
    
    def get(self, n: int, requires_vel: bool = True) -> ParticleSample:
        raise NotImplementedError()
    
    def _report_sampling(self, x, v, m_particle, n_trys):
        if not self.verbose:
            return
        n = len(x)
        sampling_rate = n / n_trys
        x_max = np.max(np.abs(x))
        v_max = np.max(np.abs(v)) if v is not None else 'None'
        self.log(f'Sampled: {n} particles, '
                 f'{m_particle=}, {x_max=}, {v_max=}, {sampling_rate=}')

    def _sample_r(self, n: int) -> np.ndarray:
        pf, rng = self._profile, self._rng
        mass, m_lo, m_hi = self['mass', 'm_lo', 'm_hi']
        M = rng.uniform(m_lo, m_hi, size=n) * mass
        r = pf.r_at_M(M)
        return r


class Jeans(InitialCondition):
    def __init__(self, *args, **base_kw):
        super().__init__(*args, **base_kw)
        
        pf = self._profile
        
        rvir, r0, rt, rw = pf['rvir', 'r0', 'rt', 'rw']
        mass = pf.M(rvir)
        
        self._meta |= {'mass': mass, 'm_hi': 1., 'm_lo': 0., 
            'r0': r0, 'rt': rt, 'rw': rw}
            
    def get(self, n: int, requires_vel: bool = True) -> ParticleSample:
        pf, rng = self._profile, self._rng
        
        r = self._sample_r(n)
        pos = rng.uniform_sphere(size=n) * r[:, None]
        m_partcile = self['mass'] / n
        
        if requires_vel:
            sigma = np.sqrt(pf.sigma2(r))
            vel = rng.standard_normal(size=(n,3)) * sigma[:, None]
            vel = vel - vel.mean(axis=0)
        else:
            vel = None
            
        self._report_sampling(pos, vel, m_partcile, n)
        return ParticleSample(pos, vel, m_partcile)

class EddInv(InitialCondition):
    def __init__(self, *args, **base_kw):
        super().__init__(*args, **base_kw)
        
        pf = self._profile
        r0, rw, rt, rvir = pf['r0', 'rw', 'rt', 'rvir']
        Et, mass = pf.V(rt), pf.M(rvir)
        
        f_opt = lambda x,y: 0.25*(3.0*x - x*x*x) + 0.5 - y
        rands = np.linspace(0., 1., 10000)
        xs = [ opt.root_scalar( 
            f_opt, args=(rand,), bracket=[-1,1], method='brentq' ).root \
              for rand in rands ]
        r2vr = pf._make_interp(rands, xs)
        
        self._r2vr = r2vr
        self._meta |= {'mass': mass, 'Et': Et, 'm_hi': 1., 'm_lo': 0., 
            'r0': r0, 'rt': rt, 'rw': rw}
        
    def __vmax(self, V: np.ndarray) -> np.ndarray:
        Et = self['Et']
        dV = Et - V
        if np.any(dV < -1.0e-10):
            V_except = V[dV < -1.0e-10]
            raise ValueError(f'Error V {V_except:.6g} > {Et:.6g}')
        dV[dV < 0.] = 0.
        return np.sqrt(2.0*dV)
    
    def __samples(self, n: int, requires_vel: bool = True):
        r = self._sample_r(n)
        if not requires_vel:
            return r, None, None, n
        
        pf = self._profile
        V = pf.V(r)
        vmax = self.__vmax(V)
        vmax2 = vmax*vmax
        fV, vr, vt = pf.fE(V), np.zeros(n), np.zeros(n)
        # If fV == 0, then vr, rt are both 0. In the following we deal with
        # cases of fV != 0.
        ids_todo = np.arange(n,dtype=int)[fV != 0.]
        n_trys, n_ids = 0, len(ids_todo)
        while n_ids > 0:
            n_trys += n_ids
            acc, _vr, _vt = self.__samples_at_r(r[ids_todo], 
                V[ids_todo], vmax[ids_todo], vmax2[ids_todo], fV[ids_todo])
            ids_acc = ids_todo[acc]
            vr[ids_acc] = _vr
            vt[ids_acc] = _vt
            ids_todo = ids_todo[~acc]
            n_ids = len(ids_todo)
            if n_ids < n/5000+5: break
            
        self.log(f'Start chunk acceleration for {n_ids} samples')
        for id_todo in ids_todo:
            base_n, fac_n, max_fac_n = 1000, 1, 10000
            while True:
                ones = np.ones(base_n*fac_n, dtype=float)
                n_trys += len(ones)
                acc, _vr, _vt = self.__samples_at_r( r[id_todo]*ones, 
                    V[id_todo]*ones, vmax[id_todo]*ones, 
                    vmax2[id_todo]*ones, fV[id_todo]*ones )
                if len(_vr) > 0:
                    vr[id_todo] = _vr[0]
                    vt[id_todo] = _vt[0]
                    break
                if fac_n < max_fac_n: fac_n *= 2
                else: 
                    print('\n\tFor sample %d find difficulty, r=%g, fV=%g... '%(\
                        id_todo, r[id_todo], fV[id_todo]), end='')
                    vr[id_todo] = 0.
                    vt[id_todo] = 0.
                    break
        return r, vr, vt, n_trys
    
    def __samples_at_r(self, r: np.ndarray, V: np.ndarray, vmax: np.ndarray, 
                       vmax2: np.ndarray, fV: np.ndarray):
        pf, rng, n = self._profile, self._rng, len(r)
        R1, R2, R3 = rng.uniform(1.0e-6, 1-1.0e-6, size=(3, n))
        z = np.sqrt(R1)
        vr = self._r2vr(R2)*vmax
        vr2 = vr*vr
        vt2 = z*z*(vmax2-vr2)
        fE = pf.fE( 0.5*(vr2+vt2)+V )
        accept = fE / fV > R3
        return accept, vr[accept], np.sqrt(vt2[accept])
    
    def get(self, n: int, requires_vel: bool = True) -> ParticleSample:
        
        r, vr, vt, n_trys = self.__samples(n, requires_vel)
        rng = self._rng
        pos = rng.uniform_sphere(size=n) * r[:, None]
        m_partcile = self['mass'] / n
        
        if requires_vel:
            circ=rng.uniform_circle(size=n)*vt[:, None]
            v = np.stack((circ[:, 0], circ[:, 1], vr), axis=-1)
            v = dp.frame.Polar.rt_to_cart(pos, v)
            vel = v - v.mean( axis=0 )
        else:
            vel = None
            
        self._report_sampling(pos, vel, m_partcile, n_trys)
        return ParticleSample(pos, vel, m_partcile)