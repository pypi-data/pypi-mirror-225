import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.integrate import quad
from scipy.special import erf
import scipy
import mystats
import collections
from pyhipp.astro.quantity.unit_system import UnitSystem
from pyhipp.core import DataDict
from pyhipp.core.abc import HasLog, HasDictRepr
from .functional import BoundFunction
from typing import Tuple, Union, Callable

def create_default_unit_system():
    U = UnitSystem
    u_l = U.mpc_to_m * 1.0e-3           # kpc
    u_v = 1.0e3                         # km/s
    u_t = u_l / u_v
    u_m = U.msun_to_kg * 1.0e10         # 10^10 Msun
    return UnitSystem(u_l, u_t, u_m)

class HaloProfile(HasLog, HasDictRepr):
    '''
    Subclass must implement _Irho() and define _meta.
    
    default_us: an unit system defined by (L=kpc, V=km/s, M=1.0e10Msun). 
    '''
    
    default_us = create_default_unit_system()
    
    repr_attr_keys = ('_meta', '_us')
    
    def __init__(self, us: UnitSystem = None, meta_kw: dict = None, **base_kw):
        
        super().__init__(**base_kw)
        if us is None:
            us = HaloProfile.default_us

        self._us = us
        
        self._meta: DataDict
        if meta_kw is not None:
            self._meta |= meta_kw
        
        self.__prepare_meta()
        
    def _Irho(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError()
        
    def __getitem__(self, key: Union[str, Tuple[str, ...]]):
        return self._meta[key]
    
    def rho(self, r: np.ndarray) -> np.ndarray:
        rho0, rs = self['rho0', 'rs']
        return rho0*self._Irho(r/rs)
    
    def M(self, r: np.ndarray) -> np.ndarray:
        Ms, rs = self['Ms', 'rs']
        return 3.0*Ms*self._IM(r/rs)
    
    def V(self, r: np.ndarray) -> np.ndarray:
        V0, Vs, rs = self['V0', 'Vs', 'rs']
        return V0 + 3.0*Vs*self._IV(r/rs)
    
    def sigma2(self, r: np.ndarray) -> np.ndarray:
        Vs, rs = self['Vs', 'rs']        
        x = r/rs
        ans = 3.0*Vs/self._Irho(x)*self._Isigma(x)
        ans = np.clip(ans, 0., None)
        return ans
    
    def r_at_M(self, M: np.ndarray) -> np.ndarray:
        Ms, rs = self['Ms', 'rs']
        ans = self._inv_IM( M/(3.0*Ms) )*rs
        return ans
    
    def fE(self, E: np.ndarray) -> np.ndarray:
        IE_eps, V0, Vs, fE0 = self['IE_eps', 'V0', 'Vs', 'fE0']
        xE = np.log(IE_eps+(E-V0)/(3.0*Vs))
        ans = fE0 * self._IfxE(xE)
        return ans
    
    def __prepare_meta(self):
        rs = self['rs']
        vols = 4.0/3.0 * np.pi * rs**3, 
        self._meta |= {'vols': vols}
        
        self.log(f'Profile {self.name}: Interpolating ...')
        self.__interp_IM()
        self.__interp_IV()
        self.__interp_Isigma()
        self.__interp_If()
    
    def _make_interp(self, x: np.ndarray, y: np.ndarray) -> Callable:
        return PchipInterpolator(x, y)
    
    def _make_integ(self, fn: Callable, a: float, b: float, **kw) -> float:
        return quad(fn, a, b, **kw)[0]
    
    def __Irhoy(self, y: np.ndarray) -> np.ndarray:
        return self._Irho( np.exp(y) )
    
    def __report_interp(self, target: str, x_vals: np.ndarray, 
                        y_vals: np.ndarray = None):
        min, max = x_vals[0], x_vals[-1]
        msg = f'Done for {target}. x range [{min:.4g}, {max:.4g}].'
        if y_vals is not None:
            msg += f' y range [{y_vals[0]:.4g}, {y_vals[-1]:.4g}].'
        self.log(msg)
    
    def __interp_IM(self):
        f = lambda y: np.exp(3.0*y) * self.__Irhoy(y)
        y_vals, yin = self['y_vals', 'yin']
        IMys = [self._make_integ(f, yin, y) for y in y_vals]
        _IMy = self._make_interp(y_vals, IMys)
        _IM = lambda x: _IMy( np.log(x) )
        _inv_IMy = BoundFunction(self._make_interp(IMys, y_vals), 
                                 IMys[0], IMys[-1]) 
        _inv_IM = lambda IM: np.exp(_inv_IMy(IM) )
        
        mass, yvir, vols, rs = self['mass', 'yvir', 'vols', 'rs']
        Ms = mass / (3.0*_IMy(yvir))
        rho0 = Ms / vols
        Vs = self._us.c_gravity * Ms / rs
        
        self._IMy, self._IM = _IMy, _IM
        self._inv_IMy, self._inv_IM = _inv_IMy, _inv_IM
        self._meta |= {'Ms': Ms, 'rho0': rho0, 'Vs': Vs}
        self.__report_interp('M', IMys)
        
    def __interp_IV(self):
        f = lambda y: self._IMy(y) / np.exp(y)
        y_vals, yin, Vs = self['y_vals', 'yin', 'Vs']
        IVys = [ self._make_integ(f, yin, y) for y in y_vals ]
        _IVy = self._make_interp(y_vals, IVys)
        _IV = lambda x: _IVy( np.log(x) )
        V0 = -3.0*Vs*IVys[-1]
        
        self._IVy, self._IV = _IVy, _IV
        self._meta |= {'V0': V0}
        self.__report_interp('V', IVys)
    
    def __interp_Isigma(self):
        f = lambda y: self._IMy(y) * self.__Irhoy(y) / np.exp(y)
        y_vals, yt = self['y_vals', 'yt']
        Isigmays = [self._make_integ(f, y, yt) for y in y_vals]
        _Isigmay = self._make_interp(y_vals, Isigmays)
        _Isigma = lambda x: _Isigmay( np.log(x) )
        self._Isigmay, self._Isigma = _Isigmay, _Isigma
        self.__report_interp('sigma', Isigmays)
    
    def __interp_If(self):
        Irho_eps = 1.0
        IV_eps = q_eps = IE_eps =  0.01
        Int_eps = 1.0
        a_eps = -np.log(q_eps)+q_eps
        
        # make the integrand
        # It consists of a detivative drho / dV, or dx_rho / dx_V
        y_vals = self['y_vals']
        Irhos, IVs = self.__Irhoy(y_vals), self._IVy(y_vals)
        xrhos, xVs = np.log( Irho_eps + Irhos ), np.log( IV_eps + IVs )
        _xrhoxV = self._make_interp(xVs, xrhos)
        _dxrhoxV = _xrhoxV.derivative()
        expq_eps = np.exp(q_eps)
        def f(q, IE):
            expq = np.exp(q)
            A = expq - expq_eps
            IV = IE + A*A
            xV = np.log( IV_eps + IV )
            xrho = _xrhoxV(xV)
            return expq * _dxrhoxV( xV ) * np.exp(xrho) / np.exp(xV)
        
        IEs = IVs + 0.
        IEt = IVs[-1]
        Ints = []
        for IE in IEs:
            f2int = lambda q: f(q, IE)
            q_lo, q_hi = q_eps, np.log(np.sqrt(IEt-IE)+expq_eps)
            Ints.append( self._make_integ( f2int, q_lo, q_hi, 
                epsrel=1.0e-4, limit=500 ) )
        Ints = np.array(Ints)
        
        # make derivative again
        xEs, xInts = np.log( IE_eps + IEs ), np.log( Int_eps - Ints )
        _xIntxE = self._make_interp( xEs, xInts )
        _dxIntdxE = BoundFunction(_xIntxE.derivative(), xEs[0], xEs[-1])
        _xIntxE = BoundFunction(_xIntxE, xEs[0], xEs[-1])
        def _IfxE(xE):
            xInt = _xIntxE(xE)
            dxIntdxE = _dxIntdxE(xE)
            return - np.exp(xInt) / np.exp(xE) * dxIntdxE
        #self._IfxE = mystats.InterpBound(xEs[0], xEs[-400], _IfxE) 
        self._IfxE = BoundFunction(_IfxE, xEs[0], xEs[-1]) 
        rho0, Vs = self['rho0', 'Vs']
        fE0 = 2.0/( np.sqrt(8.0)*np.pi*np.pi ) * rho0 / ( 3.0*Vs )**1.5
        
        self._meta |= {
            'Irho_eps':Irho_eps, 
            'IV_eps':IV_eps, 'q_eps':q_eps, 'IE_eps':IE_eps, 
            'Int_eps':Int_eps, 'a_eps':a_eps,
            'xEs':xEs,'xInts':xInts,'IEs':IEs,
            'fE0': fE0,
        }
        self.__report_interp('fE', xEs, xInts)


class NFWProfile(HaloProfile):
    def __init__(self, mass: float, rs: float, rvir: float = None, 
                 rt: float = None, rw: float = None, r0: float = None, 
                 rcore: float = None, **base_kw):
        
        _rs = rs
        _rvir = rvir if rvir is not None else 15.0*_rs
        _rt = rt if rt is not None else 2.0*_rvir
        _rw = rw if rw is not None else 0.2*_rvir
        _r0 = r0 if r0 is not None else 1.0e-4*_rs
        _rin = 0.1*_r0
        _rcore = rcore if rcore is not None else 1.0e-10*_rs
        r_vals = np.array([_rin, _r0, _rcore, 
            _rs, _rvir, _rw, _rt], dtype=float)
        r_keys = 'in', '0', 'core', 's', 'vir', 'w', 't'
        
        meta = DataDict({'mass': mass})
        for r_val, r_key in zip(r_vals, r_keys):
            meta |= { 'r'+r_key: r_val, 'x'+r_key: r_val/_rs, 
                'y'+r_key: np.log(r_val/_rs) }
            
        y_ins = np.linspace(meta['y0'], np.log( 0.8*meta['xt'] ), 1500)
        y_outs = np.log( np.linspace(0.801*meta['xt'], meta['xt'], 400) )
        y_vals = np.hstack( (y_ins, y_outs) )
        meta |= {'y_vals': y_vals}
        
        self._meta = meta        
        super().__init__(**base_kw)
    
    def _Irho(self, x: np.ndarray) -> np.ndarray:
        xcore, xt, xw = self['xcore', 'xt', 'xw']
        xp1, xpc = 1.0 + x, xcore + x
        return 1.0 / ( xpc*xp1*xp1 ) * erf( (xt-x)/xw )
    
class HernquistProfile(NFWProfile):
    def __init__(self, mass: float, rs: float, rvir: float = None, 
                 rt: float = None, rw: float = None, 
                 r0: float = None, rcore: float = None, **base_kw):
        super().__init__(mass, rs, rvir, rt, rw, r0, rcore, **base_kw)
    
    def _Irho(self, x):
        xcore, xt, xw = self['xcore', 'xt', 'xw']
        xp1, xpc = 1.0+x, xcore+x

        return 1.0/( xpc*xp1*xp1*xp1 ) * erf( (xt-x)/xw )

class DoublePowerlawProfile(NFWProfile):
    def __init__(self, alpha: float, beta: float, gamma: float,
        mass: float, rs: float, rvir: float = None, rt: float = None, 
        rw: float = None, r0: float = None, rcore: float = None, **base_kw):

        meta_kw = { 'alpha': alpha, 'beta': beta, 'gamma': gamma }
        super().__init__(mass, rs, rvir, rt, rw,r0, rcore, meta_kw=meta_kw, 
                         **base_kw)
    
    def _Irho(self, x):
        alpha, beta, gamma, xcore = self['alpha', 'beta', 'gamma', 'xcore']
        xpc = xcore + x
        xin = np.power(xpc, gamma)
        xout = np.power( 1.0+np.power(x, 1.0/alpha), (beta-gamma)*alpha )
        return 1.0 / (xin * xout)