'''
This module contains functions and objects for working with waveform data
'''

from . import utils as ut
from . import dc
from . import ac

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from math import isnan
import operator
import scipy.signal as signal
from itertools import groupby


#: Supported Waveform Headers - One of each MUST be found in the input file.
#:
#:  Note - These differ between magnetometers\
#:
#:  These keys are the arguments to the Measurement constructor, but their
#:  order does not matter
HEADERS_SUPPORTED: dict[str, list[str]] = {
    'dc_field': [
        'Magnetic Field (Oe)',
        'Field (Oe)'
    ],
    'temperature': [
        'Temperature (K)'
    ],
    'time': [
        'Time Stamp (sec)'
    ],
    'moment': [
        'Moment (emu)',
    ],
    'moment_err': [
        'M. Std. Err. (emu)',
    ]
}

# Generic dc magnetometer file header names
HEADERS_GENERIC = HEADERS_SUPPORTED.keys()


class Measurement(dc.Measurement):
    '''
    Stores data for a single Waveform measurement at a
    given temperature and applied field

    Parameters
    ----------
    dc_field : float
        Applied dc field (Oe)
    temperature : float
        Temperature of datapoint (K)
    moment : float
        Magnetisation of datapoint (emu)
    time : float
        Time of datapoint (s)

    Attributes
    ----------
    dc_field : float
        Applied dc field (Oe)
    temperature : float
        Temperature of datapoint (K)
    moment : float
        Magnetic moment of datapoint (emu)
    time : float
        Time of datapoint (s)
    rep_temperature : float
        Representative temperature assigned to this datapoint (K)
    rep_dc_field : float
        Representative dc field assigned to this datapoint (Oe)
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_file(cls, file: str, header_indices: dict | str = 'find',
                  data_header: str = '[Data]',
                  verbose: bool = True) -> list['Measurement']:
        '''
        Extracts waveform data from magnetometer output file and
        returns list of datapoints, one for each valid measurement
        Incomplete lines are ignored

        Parameters
        ----------
        file : str
            Name of magnetometer output file
        header_indices : str | dict, default 'find'
            Default 'find' will automatically locate headers, else provide dict
            with:
            Keys as generic header names given in `HEADERS_GENERIC`
            Values as column index (number) of header in file
        data_header : str default '[Data]'
            Contents of line which specifies the beginning of the data block
            in input file default is to find line containing '[Data]'
        verbose: bool, default True
            If True, issues parsing measurements are written to terminal

        Returns
        -------
        list
            Measurement objects, each specifying a single datapoint
            List has the same order as the magnetometer file
        '''

        # Find encoding of input file
        encoding = ut.detect_encoding(file)

        # Check data_header is in file
        data_index = ut.locate_data_header(file, data_header=data_header)

        if header_indices == 'find':
            # Get file headers
            header_indices, _ = ut.parse_headers(
                file, data_index, HEADERS_SUPPORTED
            )

        # Columns to extract from file
        cols = {
            gen: header_indices[gen] for gen in HEADERS_GENERIC
        }

        # Convert strings to floats, if not possible then mark as NaN
        converters = {
            it: lambda s: (float(s.strip() or np.NaN)) for it in cols.values()
        }

        # Read required columns of file
        data = np.loadtxt(
            file,
            skiprows=data_index + 1,
            delimiter=',',
            converters=converters,
            usecols=cols.values(),
            encoding=encoding
        )

        # Remove missing entries that have been marked as nan
        data = [
            row for row in data
            if not any(isnan(val) for val in row)
        ]

        # Keep moments smaller than their error (remove noisy data)
        # and keep only the field values which fall outside window
        mom_col = list(cols.keys()).index('moment')
        err_col = list(cols.keys()).index('moment_err')

        data = np.array([
            np.delete(row, err_col) for row in data
            if row[err_col] / row[mom_col] <= 0.3
        ])

        # Convert array of floats into list of Measurement objects, one per
        # line
        # Remove positional nature of Measurement constructor args by using
        # kwargs through dict
        measurements = [
            cls(**{
                col: val
                for col, val in zip(cols, row)
            })
            for row in data
            if not any(isnan(val) for val in row)
        ]

        if not len(measurements) and verbose:
            _msg = '\n Error: Cannot parse measurements from file {}'.format(
                file
            )
            ut.cprint(_msg, 'red')

        return measurements


class Experiment(dc.Experiment):
    '''
    Stores data for multiple waveform measurements at a
    given temperature and oscillating dc field frequency

    Parameters
    ----------
    rep_temperature: float
        Representative temperature of experiment (K) e.g. mean
    rep_dc_field : float
        Representative dc field assigned to this experiment (Oe)
    raw_temperatures: array_like
        Raw temperatures of experiment, one per measurement (K)
    times : array_like
        Time value, one per measurement (s)
    moments : array_like
        Measured moment, one value per measurement (emu)
    dc_fields : array_like
        Applied dc field in Oe, one value per measurement (Oe)

    Attributes
    ----------
    rep_temperature: float
        Representative temperature of experiment e.g. mean (K)
    raw_temperatures: ndarray of floats
        Raw temperatures of experiment, one per measurement (K)
    times : ndarray of floats
        Time value, one per measurement (s)
    moments : ndarray of floats
        Measured moment, one value per measurement (emu)
    dc_fields : ndarray of floats
        Applied dc field in Oe, one value per measurement (Oe)
    rep_dc_field : float
        Representative dc field assigned to this experiment (Oe)
    '''

    @classmethod
    def from_measurements(cls,
                          measurements: list[Measurement],
                          field_window: list[float],
                          temp_thresh: float = .1) -> list[list['Experiment']]:
        '''
        Creates list of Experiment objects from a list of individual
        Measurement objects. An experiment is defined as a set of measurements
        which have the same temperature and DC Field period.

        Parameters
        ----------
        measurement: list[Measurement]
            Measurements at various times but same temperatures and
            dc field period.
        field_window: list[float], default [-0.5, 0.5]
            Range of values at which DC Field is sampled to determine
            different DC field periods
        temp_thresh: float, default 0.1 K
            Threshold used to discriminate between temperatures (K)

        Returns
        -------
        list[list[Experiment]]
            Experiments
        '''

        # Sort measurements by temperature then time
        measurements = sorted(
            measurements,
            key=operator.attrgetter('temperature', 'time', )
        )

        # Find mean temperature values
        mean_temperatures, split_ind = ut.find_mean_values(
            [
                measurement.temperature
                for measurement in measurements
            ],
            thresh=temp_thresh
        )

        # Set each measurement's representative temperature, here the mean
        for mm, mt in zip(measurements, np.concatenate(mean_temperatures)):
            mm.rep_temperature = mt

        # Re-sort using mean temperatures
        measurements = sorted(
            measurements,
            key=operator.attrgetter('rep_temperature', 'time', )
        )

        # Split by temperature
        measurements: list[list[Measurement]] = np.split(
            measurements,
            split_ind + 1
        )

        field_window = np.sort(field_window)

        exp = []

        # Split measurements into experiments based on dc field
        # oscillation frequency
        for mm in measurements:
            fields = np.array([
                m.dc_field
                for m in mm
            ])

            # Find indices of points where field is changing, rather than
            # those where it is saturated.
            indxs = np.where(
                (fields > field_window[0]) & (fields < field_window[1])
            )[0]

            if len(indxs) <= 1:
                raise ValueError('No waveform data detected in file')

            # Ignore single data points that accidentally fall within the
            # field_window
            delete = []
            for i in range(1, len(indxs) - 1):
                if abs(indxs[i - 1] - indxs[i]) > 1 and abs(indxs[i] - indxs[i + 1]) > 1: # noqa
                    delete += indxs[i]
            indxs = [i for i in indxs if i not in delete]

            # Find breaks in indices, these correspond to a change in field
            # frequency
            # Store all breaks identified by groupby (where field is flat).
            lims = []
            for k, g in groupby(enumerate(indxs), lambda ix: ix[0] - ix[1]):
                lims.append(list(g))

            # Collect first and last element of list; these are tuples with
            # index and value of indxs array, respectively.
            limits = []
            for i in lims:
                limits.append((i[0][1], i[-1][1]))

            # Find bounds of each experiment's datapoints
            bounds = []
            for i in range(len(limits) - 1):
                bounds.append((limits[i][1] + 1, limits[i + 1][0] - 1))

            times = np.array([
                m.time
                for m in mm
            ])

            moments = np.array([
                m.moment
                for m in mm
            ])

            temperatures = np.array([
                m.temperature
                for m in mm
            ])

            time = [
                times[i:j] for i, j in bounds
            ]

            field = [
                fields[i:j] for i, j in bounds
            ]

            temperature = [
                temperatures[i:j] for i, j in bounds
            ]

            moment = [
                moments[i:j] for i, j in bounds
            ]

            _exp = []
            for ti, fi, te, mo in zip(time, field, temperature, moment):
                # Set zero time for each experiment
                ti -= ti[0]
                _exp.append(
                    cls(
                        mm[0].rep_temperature,
                        0.,
                        te,
                        ti,
                        mo,
                        fi
                    )
                )

            exp.append(_exp)

        return exp


class FTResult():

    '''
    Contains result of Fourier Transforming an Experiment.

    Parameters
    ----------
    ft_fields: array_like
        Fourier Transform of DC Fields
    ft_moments: array_like
        Fourier Transform of Magnetic Moments
    ft_freqs: array_like
        Frequencies associated with above fourier transformation
    temperature: float
        Temperature associated with this Experiment
    period: float
        Period associated with the oscillating DC field

    Attributes
    ----------
    ft_fields: ndarray of floats
        Fourier Transform of DC Fields, ordered by low to high frequency
    ft_moments: ndarray of floats
        Fourier Transform of Magnetic Moments, ordered by low to high
        frequency
    ft_freqs: ndarray of floats
        Frequencies associated with above fourier transformation, ordered
        low to high
    temperature: float
        Temperature associated with this Experiment
    period: float
        Period associated with the oscillating DC field

    '''

    def __init__(self, ft_fields: npt.NDArray, ft_moments: npt.NDArray,
                 ft_freqs: npt.NDArray, temperature: float,
                 period: float) -> None:

        order = np.argsort(ft_freqs)

        self.ft_fields = np.asarray(ft_fields)[order]
        self.ft_moments = np.asarray(ft_moments)[order]
        self.ft_freqs = np.asarray(ft_freqs)[order]
        self.temperature = temperature
        self.period = period

        pass

    @classmethod
    def from_experiment(cls, experiment: Experiment) -> 'FTResult':
        '''
        Fourier Transforms waveform Experiment to give FTResult object
        containing fourier transform data

        Parameters
        ----------
        experiment: Experiment
            Waveform Experiment object which will be fourier transformed

        Returns
        -------
        FTResult
            FTResult object containing fft data
        '''

        # Calculate the sample spacing (inverse of sampling rate).
        # Sampling rate is defined as npoints/measurement_time.
        spacing = experiment.times[-1] / len(experiment.times)

        # Retreive the associated frequencies.
        ft_freqs = np.fft.fftfreq(len(experiment.times), d=spacing)

        # Calculate the Fourier transform of field and moment
        ft_fields = np.fft.fft(experiment.dc_fields)
        ft_moments = np.fft.fft(experiment.moments)

        # Calculate period of experimental DC field
        period = calculate_period(experiment)

        result = cls(
            ft_fields, ft_moments, ft_freqs, experiment.rep_temperature, period
        )

        return result

    @staticmethod
    def create_ac_experiment(ft_results: list['FTResult'],
                             experiments: list[Experiment],
                             mass: float, mw: float) -> ac.Experiment:
        '''
        Creates ac.Experiment using a list of Fourier Transform results

        Parameters
        ----------
        ft_results: list[FTResult]
            Fourier transform results, each constituting a single
            datapoint in an AC susceptiblity experiment
        exepriments: list[Experiments]
            Waveform experiments which accompany ft_results, order must match
        mass: float
            Mass of sample, used to convert real and imaginary susceptibility
            from emu/Oe to cm3 mol^{-1}\n
            Set to None for no conversion
        mw: float
            Molecular weight of sample, used to convert real and imaginary
            susceptibility from emu/Oe to cm3 mol^{-1}\n
            Set to None for no conversion

        Returns
        -------
        ac.Experiment
            ccfit2.ac.Experiment object for this set of AC Susceptibility data
        '''

        ac_freqs = []
        real_sus = []
        imag_sus = []

        for ftr in ft_results:

            # Find largest FT field index
            idx_field = np.argmax(np.abs(ftr.ft_fields))
            ac_freqs.append(np.abs(ftr.ft_freqs[idx_field]))

            # Calculate susceptibility as M/H at maximum (emu/Oe)
            chi = np.abs(ftr.ft_moments[idx_field])
            chi /= np.abs(ftr.ft_fields[idx_field])

            # Calculate the phase angle (rad) of the ratio between field and
            # moment spectra at their fundamental frequency.
            # It is the ratio because any function of the type:
            # Acos(X) + Bsin(X) = Ccos(X + phasefactor)
            # This phasefactor angle is determined by the ratio of A/B
            phi = calculate_phase(
                ftr.ft_fields[idx_field], ftr.ft_moments[idx_field]
            )

            # Calculate real and imaginary susceptibility components
            real_sus.append(abs(chi * np.cos(phi)))
            imag_sus.append(abs(chi * np.sin(phi)))

        real_sus = np.array(real_sus)
        imag_sus = np.array(imag_sus)
        ac_freqs = np.array(ac_freqs)

        # Convert real and imaginary susceptibility from (emu/Oe)
        # to cm^3mol^(-1)
        if None not in (mw, mass):
            real_sus *= mw / (mass / 1000.)
            imag_sus *= mw / (mass / 1000.)

        # Collect temperature data
        temperatures = np.array([ftr.temperature for ftr in ft_results])
        mean_temp = np.mean(temperatures)

        ac_fields = np.array([
            calculate_ac_field(exp)
            for exp in experiments
        ])

        # Sort all data by ac frequency, low to high
        order = np.argsort(ac_freqs)

        # Create AC experiment using waveform susceptibility data
        ac_experiment = ac.Experiment(
            mean_temp,
            temperatures[order],
            real_sus[order],
            imag_sus[order],
            ac_freqs[order],
            0.,
            np.zeros(len(temperatures)),
            ac_fields[order]
        )

        return ac_experiment


def calculate_period(experiment: Experiment) -> float:
    '''
    Calculates the period of a waveform experiment's square wave

    Parameters
    ----------
    experiment: Experiment
        Waveform experiment object

    Returns
    -------
    float
        period of square wave
    '''

    dfields = np.diff(experiment.dc_fields)

    dpeaks = signal.find_peaks(
        np.abs(dfields),
        threshold=0.7 / 2
    )[0]

    # Forward difference of time values at turning points will give period
    periods = np.diff(experiment.times[dpeaks])

    # Take mean
    period = np.mean(periods)

    return period


def calculate_ac_field(experiment: Experiment):
    '''
    Calculates the ac field of single waveform experiment

    Parameters
    ----------
    experiment: Experiment
        Waveform experiment object

    Returns
    -------
    float
        ac field
    '''

    # low to high field values
    sorted_fields = np.sort(experiment.dc_fields)

    n_fields = len(sorted_fields)

    # Take upper and lower 50%
    low = np.mean(sorted_fields[:n_fields // 2])
    high = np.mean(sorted_fields[n_fields // 2:])

    # and average them to get the ac field
    acf = abs((high - low) / 2.)

    return acf


def calculate_phase(ft_field: float, ft_moment: float):
    '''
    Calculates phase between fourier tranformed dc field and moment values

    Parameters
    ----------
    ft_field: float
        Fourier Transformed dc field value
    ft_moment: float
        Fourier Transformed moment value

    Returns
    -------
    float
        Phase in radians
    '''

    phase = abs(
        np.angle(
            ft_field / ft_moment,
            deg=False
        )
    )

    return phase


def plot_waveform_data(ft_result: FTResult, save: bool = True,
                       show: bool = True,
                       save_name: str = 'FT_waveform.png',
                       window_title: str = 'Fourier Transformed Data',
                       verbose: bool = True) -> tuple[plt.Figure, list[plt.Axes]]: # noqa
    '''
    Plot fourier transform data for a given waveform experiment

    Parameters
    ----------
    ft_result: FTResult
        Fts
    save: bool, default True
        If True, saves plot to file
    show: bool, default True
        If True, shows plot on screen
    save_name: str, default 'FT_waveform.png'
        If save is True, will save plot to this file name
    window_title: str, default 'Fourier Transformed Data'
        Title of figure window, not of plot
    verbose: bool, default True
        If True, plot file location is written to terminal

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    list[plt.Axes]
        Matplotlib axis objects, first contains FT of field, second
        contains FT of moment
    '''

    # Define canvas object.
    fig, ax1 = plt.subplots(1, 1, num=window_title)

    ax2 = ax1.twinx()

    # Plot the data.
    ax1.plot(ft_result.ft_freqs, np.abs(ft_result.ft_fields), color='k')
    ax2.plot(
        ft_result.ft_freqs, np.abs(ft_result.ft_moments), color='tab:blue'
    )

    ax1.set_ylabel(r'|FT$^\mathregular{D}$ (H)|')
    ax2.set_ylabel(r'|FT$^\mathregular{D}$ (M)|')

    ax1.yaxis.label.set_color('k')
    ax2.yaxis.label.set_color('tab:blue')

    ax1.set_xscale('log')

    ax1.set_xlabel('Frequency (Hz)')

    fig.tight_layout()

    if save:
        fig.savefig(save_name, dpi=400)
        if verbose:
            ut.cprint(
                f'\n Fourier Transform plot saved to \n {save_name}\n',
                'cyan'
            )
    if show:
        plt.show()

    return fig, [ax1, ax2]
