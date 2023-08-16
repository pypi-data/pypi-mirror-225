#+
#   ARES/HADES/BORG Package -- ./scripts/notebooks/src/special_regions.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import numpy as np

def dir_vec(ra,dec):
    #angles in degrre	
    x=np.cos(dec/180.*np.pi)*np.cos(ra/180.*np.pi)
    y=np.cos(dec/180.*np.pi)*np.sin(ra/180.*np.pi)
    z=np.sin(dec/180.*np.pi)
    return np.array([x,y,z])



#set special sites
special_coords = {}
special_coords['home']={'ra': 0.95,'dec': 0.98,'z': 0.0, 'rc' : 400., 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['coma']={'ra': 194.95,'dec': 27.98,'z': 0.0232, 'rc' : 40., 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['shapley']={'ra': 202.011,'dec': -31.493,'z': 0.0480, 'rc' :  100. *0.68 , 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['coronaborealis']={'ra': 232.0000,'dec': 28.8833,'z': 0.065, 'rc' : 10, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['bootesvoid']={'ra': 215.0000,'dec': 26.000,'z': 0.05, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['hydra']={'ra': 158.68749975,'dec': -27.23192123,'z': np.nan, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['cetus']={'ra': 217.40988269,'dec': -69.94391168,'z': np.nan, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['vela']={'ra': 141.17998324,'dec': -50.57228815,'z': np.nan, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['norma']={'ra': 243.5936928,'dec': -60.85205904,'z': np.nan, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['A3158']={'ra': 55.87672518,'dec': -53.4820204,'z': np.nan, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['hydra-cen']={'ra': 200.02772883,'dec': -53.81840285,'z': np.nan, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }
special_coords['horologium']={'ra': 6.74460262,'dec': -49.70333177,'z': np.nan, 'rc' : 12, 'mu_mass' : 1, 'var_mass' : 1, 'mu_delta' : 1, 'var_delta' : 1 }


def get_objpos_range(objname,cosmolo={'omega_M_0' : 0.307, 'omega_lambda_0' : 0.693, 'h' : 0.6777}):
    from astropy.cosmology import LambdaCDM
    cosmo = LambdaCDM(H0=100.*cosmolo['h'], Om0=cosmolo['omega_M_0'], Ode0=cosmolo['omega_lambda_0'])
    
    
    ra   = special_coords[objname]['ra']
    dec  = special_coords[objname]['dec']
    z    = special_coords[objname]['z']
    rc   = special_coords[objname]['rc'] # units Mpc/h

    dcom = np.array(cosmo.comoving_distance(z).value)*cosmolo['h']

    d = dir_vec(ra,dec)
    pos_SSC = dcom * d
    return pos_SSC, rc


# I just want a switch....can't live without it
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False



def sky_region(region,ra,dec):

    for case in switch(region):
        if case('R1'):
            #SDSS-NGC Withburn & Shanks 2014
            return np.where( (ra>150.)*(ra<220.)*(dec>0.)*(dec<50.)), 3072.38*(np.pi/180.)**2
            break
        if case('R2'):
            #6dFGS-SGC Withburn & Shanks 2014
            return np.where( ((ra>330.)*(ra<360.)*(dec<0)*(dec>-50.)) + ((ra>0.)*(ra<50.)*(dec<0)*(dec>-50.))), 3511.29*(np.pi/180.)**2
            break
        if case('R3'):
            #6dFGS-NGC Withburn & Shanks 2014
            return np.where( (ra>150.)*(ra<220.)*(dec<0)*(dec>-40.)), 2578.03*(np.pi/180.)**2
            break
        if case(): # default, could also just omit condition or 'if True'
            print ("Case not known!")
            # No need to break here, it'll stop anyway
