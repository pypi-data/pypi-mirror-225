
#############################
# TIDAL STUFF, PRAPS SHOULD #
# BE IN A TIDAL MODULE NOT ##
# THE HA MODULE #############
#############################
# List of tidal frequencies #
#############################

import numpy as np
twopi= 2*np.pi
#    tidedict = {'M2':twopi/(12.42*3600.0), 
#                'S2':twopi/(12.00*3600.0), 
#                'N2':twopi/(12.66*3600.0),  
#                'K2':twopi/(11.97*3600.0), 
#                'K1':twopi/(23.93*3600.0), 
#                'O1':twopi/(25.85*3600.0), 
#                'P1':twopi/(24.07*3600.0), 
#                'Q1':twopi/(26.87*3600.0), 
#                'MF':twopi/(327.90*3600.0), 
#                'MM':twopi/(661.30*3600.0),
#                'M4':twopi/(6.21*3600.0)
#                }
                
class TideDict(object):
    """
    A class for handling tidal constituents.
    """

    deg_per_hour_all = {
        'J1':                           15.5854433,
        'K1':                           15.0410686,
        'K2':                           30.0821373,
        'L2':                           29.5284789,
        'M1':                           14.4966939,
        'M2':                           28.9841042,
        'M3':                           43.4761563,
        'M4':                           57.9682084,
        'M6':                           86.9523126,
        'M8':                          115.9364169,
        'N2':                           28.4397295,
        '2N2':                          27.8953548,
        'O1':                           13.9430356,
        'OO1':                          16.1391017,
        'P1':                           14.9589314,
        'Q1':                           13.3986609,
        '2Q1':                          12.8542862,
        'R2':                           30.0410667,
        'S1':                           15.0000000,
        'S2':                           30.0000000,
        'S4':                           60.0000000,
        'S6':                           90.0000000,
        'T2':                           29.9589333,
        'LAM2':                         29.4556253,
        'MU2':                          27.9682084,
        'NU2':                          28.5125831,
        'RHO':                         13.4715145,
        'MK3':                          44.0251729,
        '2MK3':                         42.9271398,
        'MN4':                          57.4238337,
        'MS4':                          58.9841042,
        '2SM2':                         31.0158958,
        'MF':                            1.0980331,
        'MSF':                           1.0158958,
        'MM':                            0.5443747,
        'SA':                            0.0410686,
        'SSA':                           0.0821373,
        'SA-IOS':                        0.0410667,
        'MF-IOS':                        1.0980331,
        'S1-IOS':                       15.0000020,
        'OO1-IOS':                      16.1391017,
        'R2-IOS':                       30.0410667,
        'A7':                            1.6424078,
        '2MK5':                         73.0092771,
        '2MK6':                         88.0503457,
        '2MN2':                         29.5284789,
        '2MN6':                         86.4079379,
        '2MS6':                         87.9682084,
        '2NM6':                         85.8635632,
        '2SK5':                         75.0410686,
        '2SM6':                         88.9841042,
        '3MK7':                        101.9933813,
        '3MN8':                        115.3920422,
        '3MS2':                         26.9523126,
        '3MS4':                         56.9523126,
        '3MS8':                        116.9523126,
        'ALP1':                         12.3827651,
        'BET1':                         14.4145567,
        'CHI1':                         14.5695476,
        'H1':                           28.9430375,
        'H2':                           29.0251709,
        'KJ2':                          30.6265120,
        'ETA2':                         30.6265120,
        'KQ1':                          16.6834764,
        'UPS1':                         16.6834764,
        'M10':                         144.9205211,
        'M12':                         173.9046253,
        'MK4':                          59.0662415,
        'MKS2':                         29.0662415,
        'MNS2':                         27.4238337,
        'EPS2':                         27.4238337,
        'MO3':                          42.9271398,
        'MP1':                          14.0251729,
        'TAU1':                         14.0251729,
        'MPS2':                         28.9430356,
        'MSK6':                         89.0662415,
        'MSM':                           0.4715211,
        'MSN2':                         30.5443747,
        'MSN6':                         87.4238337,
        'NLK2':                         27.8860711,
        'NO1':                          14.4966939,
        'OP2':                          28.9019669,
        'OQ2':                          27.3509801,
        'PHI1':                         15.1232059,
        'KP1':                          15.1232059,
        'PI1':                          14.9178647,
        'TK1':                          14.9178647,
        'PSI1':                         15.0821353,
        'RP1':                          15.0821353,
        'S3':                           45.0000000,
        'SIG1':                         12.9271398,
        'SK3':                          45.0410686,
        'SK4':                          60.0821373,
        'SN4':                          58.4397295,
        'SNK6':                         88.5218668,
        'SO1':                          16.0569644,
        'SO3':                          43.9430356,
        'THE1':                         15.5125897,
        '2PO1':                         15.9748271,
        '2NS2':                         26.8794590,
        'MLN2S2':                       26.9523126,
        '2ML2S2':                       27.4966873,
        'SKM2':                         31.0980331,
        '2MS2K2':                       27.8039339,
        'MKL2S2':                       28.5947204,
        'M2(KS)2':                      29.1483788,
        '2SN(MK)2':                     29.3734880,
        '2KM(SN)2':                     30.7086493,
        'NO3':                          42.3827651,
        '2MLS4':                        57.4966873,
        'ML4':                          58.5125831,
        'N4':                           56.8794590,
        'SL4':                          59.5284789,
        'MNO5':                         71.3668693,
        '2MO5':                         71.9112440,
        'MSK5':                         74.0251729,
        '3KM5':                         74.1073101,
        '2MP5':                         72.9271398,
        '3MP5':                         71.9933813,
        'MNK5':                         72.4649024,
        '2NMLS6':                       85.3920422,
        'MSL6':                         88.5125831,
        '2ML6':                         87.4966873,
        '2MNLS6':                       85.9364169,
        '3MLS6':                        86.4807916,
        '2MNO7':                       100.3509735,
        '2NMK7':                       100.9046319,
        '2MSO7':                       101.9112440,
        'MSKO7':                       103.0092771,
        '2MSN8':                       116.4079379,
        '2(MS)8':                      117.9682084,
        '2(MN)8':                      114.8476675,
        '2MSL8':                       117.4966873,
        '4MLS8':                       115.4648958,
        '3ML8':                        116.4807916,
        '3MK8':                        117.0344499,
        '2MSK8':                       118.0503457,
        '2M2NK9':                      129.8887361,
        '3MNK9':                       130.4331108,
        '4MK9':                        130.9774855,
        '3MSK9':                       131.9933813,
        '4MN10':                       144.3761464,
        '3MNS10':                      145.3920422,
        '4MS10':                       145.9364169,
        '3MSL10':                      146.4807916,
        '3M2S10':                      146.9523126,
        '4MSK11':                      160.9774855,
        '4MNS12':                      174.3761464,
        '5MS12':                       174.9205211,
        '4MSL12':                      175.4648958,
        '4M2S12':                      175.9364169,
        'M1C':                          14.4920521,
        '3MKS2':                        26.8701754,
        'OQ2-HORN':                     27.3416965,
        'MSK2':                         28.9019669,
        'MSP2':                         29.0251729,
        '2MP3':                         43.0092771,
        '4MS4':                         55.9364169,
        '2MNS4':                        56.4079379,
        '2MSK4':                        57.8860711,
        '3MN4':                         58.5125831,
        '2MSN4':                        59.5284789,
        '3MK5':                         71.9112440,
        '3MO5':                         73.0092771,
        '3MNS6':                       85.3920422,
        '4MS6':                        85.9364169,
        '2MNU6':                       86.4807916,
        '3MSK6':                       86.8701754,
        'MKNU6':                       87.5788246,
        '3MSN6':                       88.5125831,
        'M7':                          101.4490066,
        '2MNK8':                       116.4900752,
        '2(MS)N10':                    146.4079379,
        'MNUS2':                       27.4966873,
        '2MK2':                        27.8860711,
        '60d':                         360/(60.*24.), # 6th annual harmonic
        '72d':                         360/(72.*24.), # 5th annual harmonic
        '90d':                         360/(90.*24.), # 4th annual harmonic
        '120d':                        360/(120.*24.), # 3rd annual harmonic
        '18y':                         360/(18.61*365.25*24), # 18.6 year tide
        '4y':                          360/(4.4*365.25*24), # 4.4 year tide
        'MA2':                         28.9841042 + 360/(365.25*24), 
        'MB2':                         28.9841042 - 360/(365.25*24), 
        'MSA2':                        28.9841042 + 360/(182.*24), 
        'MSB2':                        28.9841042 - 360/(182.*24), 
        }

    # @property
    def deg_per_hour(self, Fin=None):

        print(Fin)
        if Fin is None:
            #Fin=tidedict.keys()
            Fin = ['M2','S2','N2','K2','K1','O1','P1','Q1','M4']
        elif Fin=='all':
            Fin=list(self.deg_per_hour_all.keys())
        elif type(Fin) == list:
            pass
        else:
            raise(Exception('Fin must be list or "all"'))

        deg_per_hour = { your_key: self.deg_per_hour_all[your_key] for your_key in Fin }

        return deg_per_hour

    # @property
    def deg_per_sec(self, Fin=None):
        
        out = {}
        deg_per_hour = self.deg_per_hour(Fin=Fin)
        for key in deg_per_hour.keys():
            out[key] = deg_per_hour[key]/3600
        
        return out
    
    # @property
    def rad_per_sec(self, Fin=None):
        
        out = {}
        deg_per_hour = self.deg_per_hour(Fin=Fin)
        for key in deg_per_hour.keys():
            out[key] = (twopi/360)*deg_per_hour[key]/3600
        
        return out
    
    # @property
    def hours(self, Fin=None):
        
        out = {}
        deg_per_hour = self.deg_per_hour(Fin=Fin)
        for key in deg_per_hour.keys():
            out[key] = 360/deg_per_hour[key]
        
        return out
    

def getTideFreq(Fin=None):
    """
    Return a vector of frequency [rad s-1] of common tidal constituents
    
    """
    
    tidedict = TideDict()
    deg_per_hour = tidedict.deg_per_hour(Fin=Fin)

    Fin=list(deg_per_hour.keys())
        
    frq = []
    Fout = Fin[:]
    for f in Fin:
        if f in deg_per_hour:
            frq.append(twopi/(360.0/deg_per_hour[f]*3600.0))
        else:
            'Warning: could not find constituent name: %s'%f
            Fout.remove(f)
        
    return frq, Fout

 