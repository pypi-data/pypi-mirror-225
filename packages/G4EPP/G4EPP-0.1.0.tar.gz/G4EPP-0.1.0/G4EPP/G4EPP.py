import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import numpy as np
import pandas as pd
import scipy as sci
import os

import seaborn as sns
sns.set_theme(font_scale=1.5);

from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.signal import savgol_filter

import pickle

from G4EPP.utils import FileReader

# Globals
Earray  = np.round(np.logspace(np.log10(0.250), np.log10(10000), 100), 2)

h       = np.arange(0, 500);

runList = np.array([10, 14, 20, 32, 50, 71, 100, 141, 200, 316, 500, 
                    707, 1000, 1414, 2000, 3162, 5000, 7071, 10000])

PAlist  = np.arange(0, 70+5, 5);



class api(FileReader):
    def __init__(self):

        # Altitude array abscissa
        self.h = h 
        
        # Energy array abscissa
        self.Earray = Earray 
        
        # Delta E
        self.dE = np.hstack([np.diff(self.Earray), np.diff(self.Earray)[-1]])

        self.EbinCenters = self.Earray + self.dE

        self.runList        = runList
        self.PAlist         = PAlist

        self.dirname = os.path.dirname(__file__)
        
        # Check if look up table downloaded
        if self._check_if_data_present() is False:

            print("Lookup table data missing, downloading now...")
            
            # If not, download from Zenodo
            self._download_data()

        super().__init__(self.Earray, self.runList, self.PAlist)



        self.X_energy, self.Y_altitude = np.meshgrid(self.Earray, self.h)

        

    def _check_if_data_present(self):
        """
        Internal function to check if look up table is present
        """

        total_path = self.dirname + '/data/G4data_mono_discretePAD_0degLat.pkl'

        return os.path.isfile(total_path)

    def _download_data(self):
        """
        Internal function to download 
        """
        import wget, sys

        os.mkdir(self.dirname + '/data')

        url = "https://zenodo.org/record/8034275/files/G4data_mono_discretePAD_0degLat.pkl?download=1"
        def bar_progress(current, total, width=80):
            progress_message = "Downloading: %d%% [%d / %d] kB" % (current / total * 100, int(1e-3 * current), int(1e-3 * total))
            sys.stdout.write("\r" + progress_message)
            sys.stdout.flush()


        #try:
        wget.download(url, out=self.dirname + '/data', bar=bar_progress)
        print("Data downloaded!")
        #except:
            #print("Couldn't download data :( contact Grant.Berland@colorado.edu and I'll email it to you")

    def plot_spectral_profile(self, energyDistribution, 
                                    pitchAngleDistribution, 
                                    flux, 
                                    particle=None):

        result, norm = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'spectra',
                                                        particle)

        result /= self.EbinCenters[np.newaxis,:]

        result[result < 1e-10] = 0
    
        plt.pcolormesh(self.X_energy, self.Y_altitude, norm * result, norm=LogNorm())
        plt.xscale('log')
        plt.ylim(0, 300)
        plt.xlim(1e0, 1e4)
        plt.ylabel('Altitude [km]')
        plt.xlabel('Energy [keV]')
        plt.colorbar(label='Flux [cm$^{-2}$ s$^{-1}$ sr$^{-1}$ keV$^{-1}$]')


        # Return spectrum with units cm^-2 s^-1 sr^-1 keV^-1
        return result 


    def get_spectral_profile(self, energyDistribution, 
                                    pitchAngleDistribution, 
                                    flux, 
                                    particle=None):

        result_el, norm_el = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'spectra',
                                                        'electron')

        result_el /= self.EbinCenters[np.newaxis,:]

    
        result_ph, norm_ph = self._formGreensFunctionSpectrum(energyDistribution, 
                                                pitchAngleDistribution, 
                                                flux,
                                                'spectra',
                                                'photon')

        result_ph /= self.EbinCenters[np.newaxis,:]

        # Return spectrum with units cm^-2 s^-1 sr^-1 keV^-1
        return norm_el * result_el, norm_ph * result_ph 
    
    def plot_ionization_profile(self, energyDistribution, 
                                      pitchAngleDistribution,
                                      flux,
                                      **plotParams):


        result, norm = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'ioni')

        # Normalize to unity
        result /= np.trapz(result, x=1e5 * self.h)
        
        # Make it integrate to what it should be
        result *= (norm/35)
       
        # Plot on current figure
        plt.semilogx(result, self.h, **plotParams)
    
        plt.xlabel("Ionization Rate [cm$^{-3}$ s$^{-1}$]");
        plt.ylabel("Altitude [km]");

        plt.ylim(0, 300);
        plt.grid(True, which='both')
       
        return result

    # Getter methods
    def get_all_ionization_profiles(self):
        return self._get_ionization_table()

    def get_all_data(self):
        return self._get_all_data()

    def get_altitude_array(self):
        return self.h

    def get_spectral_abscissa(self):
        return self.X_energy, self.Y_altitude

    def get_energy_array(self):
        return self.Earray

    def get_bin_width(self):
        return self.binWidth

    def get_run_list(self):
        return 1e3 * self.runList

    def get_PA_list(self):
        return self.PAlist


class XrayAnalysis(FileReader):
    def __init__(self):
        
        # Import globals
        self.Earray         = Earray
        self.runList        = runList
        self.PAlist         = PAlist 

        self.dE = np.hstack([np.diff(Earray), np.diff(Earray)[-1]])
        self.EbinCenters = self.Earray + self.dE

        # Send them up
        super().__init__(self.Earray, self.runList, self.PAlist)


    def getSpectrumAtAltitude(self, energyDistribution, pitchAngleDistribution, flux, altitudeRange):

        result, norm = self._formGreensFunctionSpectrum(energyDistribution, 
                                                        pitchAngleDistribution, 
                                                        flux,
                                                        'spectra',
                                                        'photon')

        spectrum = norm * np.mean(result[altitudeRange[0]:altitudeRange[1],:], axis=0)

        # Return spectrum with units cm^-2 s^-1 sr^-1 keV^-1
        return spectrum / self.EbinCenters

    



class RadiationAnalysis:
    def __init__(self, material):
        
        self.dirname = os.path.dirname(__file__)
        
        
        if material is "human":
            
            filepath_pre  = self.dirname + "/data/radiationData/"
            filepath_post = "_human_dose_conversion.csv"

            # Read in data
            # [energy in keV, conversion factor in Sv-cm^2]
            self.el_conv = pd.read_csv(filepath_pre + "electron" + filepath_post, names=['E', 'C']) 
            self.ph_conv = pd.read_csv(filepath_pre + "photon"   + filepath_post, names=['E', 'C'])

    def calculate_radiation_dose(self, el_spectra, ph_spectra):
    
        dosage_alt_array = np.zeros([len(h)]);
   
        for i in range(0, len(h)):
            dosage_alt_array[i] = 2 * np.pi * np.sum(el_spectra[i,:] * self.el_conv.C + \
                                         ph_spectra[i,:] * self.ph_conv.C)

        return dosage_alt_array;

    def _calculate_differential_radiation_dose(self, el_spectra, ph_spectra):
    
        dosage_alt_array = np.zeros([len(h), 100]);
    
        for i in range(0, len(h)):
            dosage_alt_array[i,:] = el_spectra[i,:] * self.el_conv.C + \
                                    ph_spectra[i,:] * self.ph_conv.C

        return dosage_alt_array;

class EnergyDistributions:
    def __init__(self, Nsamples=0):

        # Modified Bessel function for relativistic Maxwellian
        from scipy.special import kn

        # Distribution PDFs
        self.f_powerLaw       = lambda E, alpha, Emin: (alpha-1) / Emin *  (E / Emin)**-alpha

        self.f_exponential    = lambda E, E0: 1/E0 * np.exp(-E / E0)

        self.f_doubMaxwellian = lambda E, T1, T2: np.sqrt(E/np.pi) * (1/T1)**(3/2) * np.exp(-E/T1) + np.sqrt(E/np.pi) * (1/T2)**(3/2) * np.exp(-E/T2)

        m_el = 511 # Electron mass , [keV/c^2]
        self.f_relMaxwell     = lambda E, T: (1 + E/m_el)**2 * np.sqrt(1 - 1/(1 + E/m_el)**2) / ( m_el * (T/m_el) *
 kn(2, m_el/T) ) * np.exp(-(1 + E/m_el) / (T/m_el))

        # Inverse CDF sampling formulas
        self.powerLawSampler    = lambda U, alpha, Emin: np.power(U, 1/(1-alpha)) * Emin
        self.exponentialSampler = lambda U, E0: -E0 * np.log(U)

        # Save input data
        self.Nsamples = Nsamples
        self.samples  = np.zeros([Nsamples])

    # Getter methods
    def powerLaw(self):
        return self.f_powerLaw

    def exponential(self):
        return self.f_exponential

    def doubleMaxwellian(self):
        return self.f_doubMaxwellian

    def relativisticMaxwellian(self):
        return self.f_relMaxwell

    def _doubleMaxwellianSampler(self, T1, T2):

        i = 0
        c = 1
        while i < self.Nsamples:

            # Helper distribution (exponential with E0 = (T1 + T2)/2
            Y = -(T1+T2)/2 * np.log(np.random.rand());

            # Accept/reject algorithm
            if np.random.rand() < self.f_doubleMaxwell(Y, T1, T2)/(c * self.f_exponential(Y, (T1 + T1)/2)):

                # If loop entered, accept sample point 
                self.samples[i] = Y;

                i += 1;

        return self.samples

    def _relativisticMaxwellianSampler(self, T):

        i = 0
        c = 2
        while i < self.Nsamples:

            # Helper distribution (exponential with E0 = T on [1, inf)
            Y = -T * np.log(np.random.rand());

            # Accept/reject algorithm
            if np.random.rand() < self.f_relMaxwell(Y, T)/(c * self.f_exponential(Y, T)):

                # If loop entered, accept sample point 
                self.samples[i] = Y;

                i += 1;

        return self.samples
    
    def generate_mixture_spectrum(self, Earray, weights, coefficients):

        # Power law 
        alpha = coefficients[0]
        Emin  = coefficients[1]

        # Exponential
        E0    = coefficients[2]

        # Double Maxwellian
        T1    = coefficients[3]
        T2    = coefficients[4]

        # Relativistic Maxwellian
        T     = coefficients[5]

        return weights[0] * f_powerlaw(Earray, alpha, Emin) +  \
               weights[1] * f_exponential(Earray, E0) +        \
               weights[2] * f_doubMaxwellian(Earray, T1, T2) + \
               weights[3] * f_relMaxwellian(Earray, T)

    def sample_from_mixture_spectrum(self, weights, coefficients):

        U = np.random.rand(Nsamples, 4)

        return weights[0] * self.powerlawSampler(U[:,0], alpha, Emin) +    \
               weights[1] * self.exponentialSampler(U[:,1], E0) +          \
               weights[2] * self._doubMaxwellianSampler(U[:,2], T1, T2) +  \
               weights[3] * self._relativisticMaxwellianSampler(U[:,3], T)




'''
TODO: loop in Jovian EPP model
class JUNO(DataHandler):
    def __init__(self):
        pass
'''
