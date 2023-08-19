'''
This module contains functions and objects for working with relaxation data
'''

from . import utils as ut
from . import gui
from . import ac
from . import dc
from . import stats

import numpy as np
import numpy.typing as npt
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, AutoMinorLocator
import matplotlib.colors as mcolors
from abc import ABC, abstractmethod
import copy
from functools import partial
from qtpy import QtWidgets, QtCore, QtGui
import pyqtgraph as pg

import warnings
warnings.filterwarnings('ignore', '.*GUI is implemented.*')
warnings.filterwarnings('ignore', 'invalid value encountered in power')
warnings.filterwarnings('ignore', 'invalid value encountered in log10')
warnings.filterwarnings('ignore', 'divide by zero encountered in log10')
warnings.filterwarnings('ignore', 'divide by zero encountered in power')
warnings.filterwarnings('ignore', 'divide by zero encountered in reciprocal')
warnings.filterwarnings('ignore', 'invalid value encountered in divide')
warnings.filterwarnings('ignore', 'overflow encountered in power')
warnings.filterwarnings('ignore', 'overflow encountered in multiply')

pg.setConfigOption('foreground', 'k')


class TauHDataset():
    '''
    Contains experimental rates, rate bounds (+-) and fields


    Parameters
    ----------
    rates: array_like
        Relaxation rates in seconds^-1
    fields: array_like
        Field Values (Oe)
    lograte_pm: array_like
        Plus-Minus of log10(rates) in logspace, assumed to be symmetric\n
        Not! log(rate_pm)

    Attributes
    ----------
    rates: ndarray of floats
        Relaxation rates in seconds^-1
    fields: ndarray of floats
        Field Values (Oe)
    lograte_pm: ndarray of floats
        Plus-minus of log10(rates) in logspace,
        assumed to be symmetric, size is (n_rates,1)\n
        Not! log(rate_pm)
    rate_pm: ndarray of floats
        Plus-minus of rates in linspace,
        will be asymmetric, size is (n_rates,2)\n
        not! 10**(lograte_pm)
    '''
    def __init__(self, rates: npt.ArrayLike, fields: npt.ArrayLike,
                 lograte_pm: npt.ArrayLike = []):

        self.rates = np.asarray(rates)
        self.fields = np.asarray(fields)
        self.lograte_pm = np.asarray(lograte_pm)

        return

    @property
    def lograte_pm(self) -> npt.NDArray:
        return self._lograte_pm

    @lograte_pm.setter
    def lograte_pm(self, value: npt.ArrayLike):

        if isinstance(value, float):
            raise ValueError('lograte_pm must be list')
        elif len(np.shape(value)) != 1:
            raise ValueError('lograte_pm must be symmetric, i.e. (1, n_rates)')
        if not len(value):
            self._lograte_pm = []
            self.rate_pm = []
        else:
            # Use symmetric lograte_pm to obtain difference in rates in linear
            # space - n.b. these will be asymmetric
            self._lograte_pm = np.asarray(value)
            self.rate_pm = self.lograte_pm_to_pm(self.rates, self.lograte_pm)
        return

    @classmethod
    def from_raw(cls, fields: npt.ArrayLike, lntaus: npt.ArrayLike,
                 lntau_stdevs: npt.ArrayLike, lntau_fus: npt.ArrayLike,
                 lntau_fls: npt.ArrayLike) -> 'TauHDataset':
        '''
        Creates dataset from raw values of rates, fields, ln standard
        deviation, and upper and lower lntau values

        Parameters
        ----------
        fields: array_like
            Applied Fields (Oe)
        lntaus: array_like
            ln(tau) values  (ln(seconds))
        lntau_stdev: array_like
            Standard deviation of ln(tau) (ln(seconds)).\n
            These are intrinsic to AC or DC model
        lntau_fus: array_like
            Upper bound of fitted ln(tau) computed using uncertainties from
            fitted parameters
        lntau_fls: array_like
            Lower bound of fitted ln(tau) computed using uncertainties from
            fitted parameters

        Returns
        -------
        TauHDataset
           Single Dataset, rate vs H
        '''

        lntaus = np.array(lntaus)

        taus = np.array([
            np.exp(lntime)
            for lntime in lntaus
        ])

        rates = [tau**-1 for tau in taus]

        # Upper and lower lntau using standard deviation
        # from distribution
        model_upper_tau = np.exp(lntaus + lntau_stdevs)
        model_lower_tau = np.exp(lntaus - lntau_stdevs)

        # Take element wise maximum of these to find max standard deviation
        # considering both stdev inherent to AC/DC model distribution, and from
        # fitting of AC/DC model parameters

        upper_tau = np.maximum(np.exp(lntau_fus), model_upper_tau)
        lower_tau = np.minimum(np.exp(lntau_fls), model_lower_tau)

        # Difference in rates in log space, used as standard deviation in
        # log(tau), required by fitting routine
        # THIS IS NOT!!!! log10(rate_ul_diff)
        # log(sigma(tau)) != sigma(log(tau))
        lograte_ul_diff = [
            np.log10(rates) - np.log10(upper_tau**-1),
            np.log10(lower_tau**-1) - np.log10(rates)
        ]

        # Take maximum of difference in rates in log space
        # If differences arise from model stdev then will be symmetric
        # in log space
        # but if from previous least squares will be asymmetric
        # so take largest and treat as symmetric
        lograte_pm = np.maximum(
            lograte_ul_diff[0],
            lograte_ul_diff[1]
        )

        return cls(rates, fields, lograte_pm)

    @classmethod
    def from_ac_dc(cls, models: list[ac.Model | dc.Model]) -> 'TauHDataset':
        '''
        Creates Dataset from list of fitted AC or DC models

        Parameters
        ----------
        models: list[ac.Model]
            Models of AC or DC data, at least one in list must be
            successfully fitted (i.e. fit_status=True)

        Returns
        -------
        list[TauHDataset]
            Datasets, each rate vs H
            List has 1 dataset if only single-tau models are given\n
            or 2 datasets if >1 double-tau models present in ``models``

        '''
        double_tau_models = [
            ac.DoubleGDebyeEqualChiModel,
            ac.DoubleGDebyeModel,
            dc.DoubleExponentialModel
        ]

        ml1 = []
        ml2 = []

        for model in models:
            # Split double tau models into two single tau models
            if type(model) in double_tau_models:
                m1, m2 = cls.split_model(model)
                ml1.append(m1)
                ml2.append(m2)
            else:
                ml1.append(model)
                ml2.append(model)

        # Process first set of models
        datasets = [cls.from_raw(*cls.extract_ac_dc_model(ml1))]

        # and add on second set if desired
        if any([type(model) in double_tau_models for model in models]):
            datasets.append(cls.from_raw(*cls.extract_ac_dc_model(ml2)))

        return datasets

    @staticmethod
    def split_model(model: ac.DoubleGDebyeModel | ac.DoubleGDebyeEqualChiModel | dc.DoubleExponentialModel) -> list[object]: # noqa
        '''
        Splits double tau models into placeholder single tau models
        returned objects are not actual ac.Model or dc.Model instances,
        they simply possess the attributes required by this class'
        extract_ac_dc_model method.
        '''

        m1 = type(
            'fake_model_1',
            (object,),
            {
                'fit_status': model.fit_status,
                'lntau_expect': model.lntau_expect[0],
                'lntau_stdev': model.lntau_stdev[0],
                'lntau_fit_ul': model.lntau_fit_ul[0],
                'dc_field': model.dc_field
            }
        )

        m2 = type(
            'fake_model_2',
            (object,),
            {
                'fit_status': model.fit_status,
                'lntau_expect': model.lntau_expect[1],
                'lntau_stdev': model.lntau_stdev[1],
                'lntau_fit_ul': model.lntau_fit_ul[1],
                'dc_field': model.dc_field
            }
        )

        return m1, m2

    @classmethod
    def from_ccfit2_files(cls, file_names: str | list[str]) -> 'TauHDataset':
        '''
        Creates Dataset from ccfit2 AC/DC parameter file(s)

        Parameters
        ----------
        file_names: str | list[str]
            Filenames of ccfit2 AC/DC parameter file(s)

        Returns
        -------
        TauHDataset
            Single Dataset, rate vs H
        '''

        if isinstance(file_names, str):
            file_names = [file_names]

        # Find encoding of input files
        encodings = [
            ut.detect_encoding(file)
            for file in file_names
        ]

        headers = {
            'fields': ['H'],
            'lntau': ['<ln(tau)>'],
            'lntau_stdevs': ['sigma_ln(tau)'],
            'lntau_fu': ['fit_upper_ln(tau)'],
            'lntau_fl': ['fit_lower_ln(tau)']
        }

        fields, lntaus, lntau_stdevs, lntau_fls, lntau_fus = [], [], [], [], []

        bounds = True

        for file, encoding in zip(file_names, encodings):

            # Get file headers
            header_indices, _ = ut.parse_headers(
                file, 0, headers, delim=None
            )

            if header_indices['fields'] == -1:
                raise ValueError(f'Cannot find fields in {file}')
            elif header_indices['lntau'] == -1:
                raise ValueError(f'Cannot find <ln(tau)> in {file}')

            # Columns to extract from file
            cols = [header_indices[he] for he in headers.keys()]

            converters = {
                it: lambda s: (float(s.strip() or np.NaN)) for it in cols
            }

            # Read required columns of file
            data = np.loadtxt(
                file,
                skiprows=1,
                converters=converters,
                usecols=cols,
                encoding=encoding
            )

            # If bound headers not found then turn off bounds for all files
            optional_indices = [
                header_indices['lntau_stdevs'],
                header_indices['lntau_fu'],
                header_indices['lntau_fl']
            ]
            if -1 not in optional_indices:
                lntau_stdevs.append(data[:, 2].tolist())
                lntau_fus.append(data[:, 3].tolist())
                lntau_fls.append(data[:, 4].tolist())
            else:
                bounds = False

            # Add to big lists
            fields.append(data[:, 0].tolist())
            lntaus.append(data[:, 1].tolist())

        # Sort all data by field
        order = np.argsort(np.array(ut.flatten_recursive(fields)))

        if bounds:
            # Create dataset from all data
            dataset = cls.from_raw(
                np.array(ut.flatten_recursive(fields))[order],
                np.array(ut.flatten_recursive(lntaus))[order],
                np.array(ut.flatten_recursive(lntau_stdevs))[order],
                np.array(ut.flatten_recursive(lntau_fus))[order],
                np.array(ut.flatten_recursive(lntau_fls))[order]
            )

        else:
            dataset = cls(
                np.exp(-np.array(ut.flatten_recursive(lntaus))[order]),
                np.array(ut.flatten_recursive(fields))[order]
            )

        return dataset

    @classmethod
    def from_rate_files(cls, file_names: str | list[str]) -> 'TauHDataset':
        '''
        Creates Dataset from file(s) containingthe headers\n
        H, rate, <upper>, <lower>\n
        The last two are optional

        Parameters
        ----------
        file_names: str | list[str]
            Filenames of ccfit2 AC/DC parameter file(s)

        Returns
        -------
        TauTDataset
            Single Dataset, rate vs T
        '''

        if isinstance(file_names, str):
            file_names = [file_names]

        # Find encoding of input files
        encodings = [
            ut.detect_encoding(file)
            for file in file_names
        ]

        headers = {
            'fields': ['H'],
            'rate': ['rate'],
            'upper': ['upper'],
            'lower': ['lower']
        }

        fields, rates, upper, lower = [], [], [], []

        indices = []

        bounds = True

        for file, encoding in zip(file_names, encodings):

            # Get file headers
            header_indices, _ = ut.parse_headers(
                file, 0, headers, delim=None
            )

            indices.append(header_indices)

            if header_indices['fields'] == -1:
                raise ValueError(f'Cannot find fields in {file}')
            elif header_indices['rate'] == -1:
                raise ValueError(f'Cannot find rates in {file}')

            # Columns to extract from file
            cols = [header_indices[he] for he in headers.keys()]

            converters = {
                it: lambda s: (float(s.strip() or np.NaN)) for it in cols
            }

            # Read required columns of file
            data = np.loadtxt(
                file,
                skiprows=1,
                converters=converters,
                usecols=cols,
                encoding=encoding
            )

            # Add to big lists
            fields.append(data[:, 0].tolist())
            rates.append(data[:, 1].tolist())

            # If either header not found, then skip
            if -1 not in [header_indices['upper'], header_indices['lower']]:
                upper.append(data[:, 2].tolist())
                lower.append(data[:, 3].tolist())
            else:
                bounds = False

        fields = np.array(ut.flatten_recursive(fields))
        rates = np.array(ut.flatten_recursive(rates))

        # Find low to high field order
        order = np.argsort(np.array(fields))

        # Calculate lograte_pm as difference in logarithmic domain
        if bounds:
            lower = np.array(ut.flatten_recursive(lower))
            lower_logdiff = np.log10(rates) - np.log10(lower)
            upper = np.array(ut.flatten_recursive(upper))
            upper_logdiff = np.log10(upper) - np.log10(rates)
            lograte_pm = np.maximum(lower_logdiff, upper_logdiff)[order]
        else:
            lograte_pm = []

        # Create dataset from all data
        dataset = cls(rates[order], fields[order], lograte_pm)

        return dataset

    @staticmethod
    def extract_ac_dc_model(models: list[ac.Model | dc.Model]) -> tuple[list[float], list[float], list[float], list[float]]: # noqa
        '''
        Extracts, from AC.Model and DC.Model, the parameters required to
        generate a TauHDataset

        Parameters
        ----------
        models: list[ac.Model | dc.Model]
            AC or DC models, one per temperature and static field

        Returns
        -------
        list[float]
            Applied Field values in units of Oersted
        list[float]
            ln(tau) values  in units of ln(seconds)
        list[float]
            Standard deviation of ln(tau) in units of ln(seconds)
            These are intrinsic to AC or DC model
        list[float]
            Upper bound of fitted ln(tau) computed using uncertainties from
            fitted parameters
        list[float]
            Lower bound of fitted ln(tau) computed using uncertainties from
            fitted parameters
        '''

        # <ln(tau)>
        lntaus = np.array([
            model.lntau_expect
            for model in models
            if model.fit_status
        ])

        # Standard deviation inherent to model distribution
        # This is sigma of lntau, so MUST be applied to lntau, not tau
        lntau_stdevs = [
            model.lntau_stdev
            for model in models
            if model.fit_status
        ]

        # Upper and lower bounds of ln(tau) from fit uncertainty
        # in fitted parameters
        lntau_fus = [
            model.lntau_fit_ul[0]
            for model in models
            if model.fit_status
        ]

        lntau_fls = [
            model.lntau_fit_ul[1]
            for model in models
            if model.fit_status
        ]

        fields = [
            model.field
            for model in models
            if model.fit_status
        ]

        # Sort by temperature, low to high
        order = np.argsort(fields)
        fields = [fields[it] for it in order]
        lntaus = [lntaus[it] for it in order]
        lntau_stdevs = [lntau_stdevs[it] for it in order]
        lntau_fus = [lntau_fus[it] for it in order]
        lntau_fls = [lntau_fls[it] for it in order]

        return fields, lntaus, lntau_stdevs, lntau_fus, lntau_fls

    @staticmethod
    def lograte_pm_to_pm(rates: npt.ArrayLike,
                         lograte_pm: npt.ArrayLike) -> npt.NDArray:
        '''
        Converts symmetric log10 error of log10rates to asymmetric linear
        errors.

        Parameters
        ----------
        rates: array_like
            Rates in linear space in s^-1
        lograte_pm: array_like
            +-log10(rate), symmetric, same number of elements as rates

        Returns
        -------
        ndarray of floats
            (2, n_rates) list of upper and lower bounds in linear space
        '''

        rate_pm = np.array([
            rates - 10**(np.log10(rates) - lograte_pm),
            10**(np.log10(rates) + lograte_pm) - rates
        ])

        return rate_pm


class LogTauHModel(ABC):
    '''
    Abstract class on which all phenomenological models of
    field-dependent magnetic relaxation Log10(rate) are based
    '''

    @property
    @abstractmethod
    def NAME() -> str:
        'string name of model'
        raise NotImplementedError

    @property
    @abstractmethod
    def LNAME() -> str:
        'string name of model with Log() around it, e.g. Log(Orbach)'
        raise NotImplementedError

    @property
    @abstractmethod
    def PARNAMES() -> list[str]:
        'string names of parameters which can be fitted or fixed'
        raise NotImplementedError

    @property
    @abstractmethod
    def VARNAMES_MM() -> dict[str, str]:
        '''
        Mathmode (i.e. $$, latex ) versions of PARNAMES\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are mathmode strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def VARNAMES_HTML() -> dict[str, str]:
        '''
        HTML versions of PARNAMES\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are mathmode strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def UNITS() -> dict[str, str]:
        '''
        string names of units of PARNAMES\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are unit name strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def UNITS_MM() -> dict[str, str]:
        '''
        Mathmode (i.e. $$, latex ) versions of UNITS\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are unit name strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def UNITS_HTML() -> dict[str, str]:
        '''
        HTML versions of UNITS\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are unit name strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def BOUNDS() -> dict[str, list[float, float]]:
        '''
        Bounds for each parameter of model\n
        Keys: parameter name\n
        Values: [upper, lower]\n
        used by scipy least_squares
        '''
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def model(parameters: dict[str, float],
              fields: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates model function of log(relaxation rate)
        using provided parameter and field values.

        Parameters
        ----------
        parameters: dict[str, float],
            Parameters to use in model function
        fields: array_like
            DC field values (Oe) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of field

        '''
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def set_initial_vals(parameters: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''
        raise NotImplementedError

    def __init__(self, fit_vars: dict[str, float | str],
                 fix_vars: dict[str, float | str]):
        '''
        Set default values for mandatory attributes
        '''

        # Replace any 'guess' strings with proper guesses
        self.fit_vars = self.set_initial_vals(fit_vars)
        self.fix_vars = self.set_initial_vals(fix_vars)

        # Check all PARNAMES are provided in fit+fix
        input_names = [
            name for name in {**self.fit_vars, **self.fix_vars}.keys()
        ]

        if any([req_name not in input_names for req_name in self.PARNAMES]):
            raise ValueError(
                'Missing fit/fix parameters in {} Model'.format(
                    self.NAME
                )
            )

        # Check for duplicates in fit and fix
        dupe = self.fit_vars.keys() & self.fix_vars.keys()
        if dupe:
            raise ValueError(
                f'Duplicate keys {dupe} provided to both fit and fix'
            )

        # Final model parameter values
        # fitted and fixed
        self._final_var_values = {
            var: None
            for var in self.PARNAMES
        }

        # Fit status and temperature
        self._fit_status = False

        # Fit standard deviation
        self._fit_stdev = {
            var: None
            for var in self.fit_vars.keys()
        }

        return

    @property
    def fit_status(self) -> bool:
        'True if fit successful, else False'
        return self._fit_status

    @fit_status.setter
    def fit_status(self, value: bool):
        if isinstance(value, bool):
            self._fit_status = value
        else:
            raise TypeError
        return

    @property
    def final_var_values(self) -> float:
        'Final values of parameters, both fitted and fixed'
        return self._final_var_values

    @final_var_values.setter
    def final_var_values(self, value: dict):
        if isinstance(value, dict):
            self._final_var_values = value
        else:
            raise TypeError
        return

    @property
    def fit_stdev(self) -> float:
        'Standard deviation on fitted parameters, from fitting routine'
        return self._fit_stdev

    @fit_stdev.setter
    def fit_stdev(self, value: dict):
        if isinstance(value, dict):
            self._fit_stdev = value
        else:
            raise TypeError
        return

    @property
    def fix_vars(self) -> float:
        '''
        Parameters to fix (i.e. not fit)
        keys are names in PARNAMES, values are values
        '''
        # Check for implementation in Model class init
        return self._fix_vars

    @fix_vars.setter
    def fix_vars(self, value: dict):
        if isinstance(value, dict):
            if any([key not in self.PARNAMES for key in value.keys()]):
                raise KeyError('Unknown variable names provided to fix')
            self._fix_vars = value
        else:
            raise TypeError('fix must be dictionary')
        return

    @property
    def fit_vars(self) -> float:
        '''
        Parameters to fit
        keys are names in PARNAMES, values are values
        '''
        # Check for implementation in Model class init
        return self._fit_vars

    @fit_vars.setter
    def fit_vars(self, value: dict):
        if isinstance(value, dict):
            if any([key not in self.PARNAMES for key in value.keys()]):
                raise KeyError('Unknown variable names provided to fit')
            self._fit_vars = value
        else:
            raise TypeError('Fit must be dictionary')
        return

    @classmethod
    def residuals(cls, params: dict[str, float], fields: npt.ArrayLike,
                  true_lograte: npt.ArrayLike) -> npt.NDArray:
        '''
        Calculates difference between measured log10(relaxation rate) and trial
        from model

        Parameters
        ----------
        params: array_like
            model parameter values
        fields: array_like
            Field values (Oe) at which model function is evaluated
        true_lograte: array_like
            true (experimental) values of log10(relaxation rate)

        Returns
        -------
        ndarray of floats
            Residuals
        '''

        # Calculate model log10(relaxation rate) using parameters
        trial_lograte = cls.model(params, fields)

        residuals = trial_lograte - true_lograte

        return residuals

    @classmethod
    def residual_from_float_list(cls, new_vals: npt.ArrayLike,
                                 fit_vars: dict[str, float],
                                 fix_vars: dict[str, float],
                                 fields: npt.ArrayLike,
                                 lograte: npt.ArrayLike,
                                 sigma: npt.ArrayLike = []) -> npt.NDArray:
        '''
        Wrapper for `residuals` method, takes new values from scipy
        least_squares which provides list[float], to construct new
        fit_vars dict, then runs `residuals` method.

        Parameters
        ----------
        new_vals: array_like
            This iteration's fit parameter values provided by least_squares
            this has the same order at fit_vars.keys
        fit_vars: dict[str, float]
            Parameter to fit in model function\n
            keys are PARNAMES, values are float values
        fix_vars: dict[str, float]
            Parameter which remain fixed in model function\n
            keys are PARNAMES, values are float values
        fields: array_like
            Field (Oe) at which model function is evaluated
        lograte: array_like
            True (experimental) values of log10(relaxation rate)
        sigma: array_like
            Standard deviation of tau in logspace

        Returns
        -------
        ndarray of floats
            Residuals
        '''

        # Swap fit values for new values from fit routine
        new_fit_vars = {
            name: guess
            for guess, name in zip(new_vals, fit_vars.keys())
        }

        # And make combined dict of fit and fixed
        # variable names (keys) and values
        all_vars = {**fix_vars, **new_fit_vars}

        residuals = cls.residuals(all_vars, fields, lograte)

        if len(sigma):
            residuals /= sigma

        return residuals

    def fit_to(self, dataset: 'TauHDataset',
               guess: str | dict[str, float] = 'predefined',
               verbose: bool = True) -> None:
        '''
        Fits model to Dataset

        Parameters
        ----------
        dataset: TauHDataset
            Dataset to which a model of rate vs temperature will be fitted
        guess: str | dict[str, float], default 'predefined'
            Either string 'predefined', or dict of initial parameters
            used as starting guess with keys as parameter names and values as
            numerical values
        verbose: bool, default True
            If True, prints information to terminal

        Returns
        -------
        None
        '''

        # Get starting guesses, either predefined in self or given
        # by user
        if guess != 'predefined':
            guess = [
                guess[key] for key in self.fit_vars.keys()
            ]
        else:
            guess = [val for val in self.fit_vars.values()]

        # Get bounds for variables to be fitted
        bounds = np.array([
            self.BOUNDS[name]
            for name in self.fit_vars.keys()
        ]).T

        curr_fit = least_squares(
            self.residual_from_float_list,
            args=[
                self.fit_vars,
                self.fix_vars,
                dataset.fields,
                np.log10(dataset.rates),
                dataset.lograte_pm
            ],
            x0=guess,
            bounds=bounds
        )

        if curr_fit.status == 0:
            if verbose:
                ut.cprint(
                    '\n Fit failed - Too many iterations', 'black_yellowbg'
                )

            self.final_var_values = {
                name: value
                for name, value in zip(self.fit_vars, curr_fit.x)
            }
            self.fit_stdev = {
                label: np.nan
                for label in self.fit_vars.keys()
            }
            self.fit_status = False
        else:
            stdev, no_stdev = stats.svd_stdev(curr_fit)

            # Standard deviation error on the parameters
            self.fit_stdev = {
                label: val
                for label, val in zip(self.fit_vars.keys(), stdev)
            }

            self.fit_status = True

            # Report singular values=0 of Jacobian
            # and indicate that std_dev cannot be calculated
            for par, si in zip(self.fit_vars.keys(), no_stdev):
                if verbose and not si:
                    ut.cprint(
                        f'Warning: Jacobian is degenerate for {par}, standard deviation cannot be found, and is set to zero\n', # noqa
                        'black_yellowbg'
                    )

            # Set fitted values
            self.final_var_values = {
                name: value
                for name, value in zip(self.fit_vars.keys(), curr_fit.x)
            }
            # and fixed values
            for key, val in self.fix_vars.items():
                self.final_var_values[key] = val

        return


class MultiLogTauHModel():
    '''
    Takes multiple LogTauHModel objects and combines into a single object

    Parameters
    ----------
    fit_vars: list[dict[str, float | str]]
        List of fit dicts, with keys as PARNAMES of each LogTauHModel
        and values as either the string 'guess' or a float value
    fix_vars: list[dict[str, float | str]]
        List of fix dicts, with keys as PARNAMES of each LogTauHModel
        and values as either the string 'guess' or a float value
    logmodels: list[LogTauHModel]
        List of uninstantiated LogTauHModel objects

    Attributes
    ----------
    logmodels: list[LogTauHModel]
        List of LogTauHModel objects
    NAME: str
        Names of each LogTauHModel concatenated
    '''

    def __init__(self, logmodels: list[LogTauHModel],
                 fit_vars: list[dict[str, float | str]],
                 fix_vars: list[dict[str, float | str]]) -> None:

        # Instantiate each logmodel and create list of instantiated logmodels
        self.logmodels = self.process_fitfix(fit_vars, fix_vars, logmodels)

        self.NAME = [logmodel.NAME for logmodel in logmodels]
        self.NAME = ''.join(['{}+'.format(name) for name in self.NAME])[:-1]

        self._fit_status = False

        return

    @property
    def fit_status(self) -> bool:
        'True if fit successful, else False'
        return self._fit_status

    @fit_status.setter
    def fit_status(self, value: bool):
        if isinstance(value, bool):
            self._fit_status = value
        else:
            raise TypeError
        return

    @staticmethod
    def process_fitfix(fit_vars: list[dict[str, float | str]],
                       fix_vars: list[dict[str, float | str]],
                       logmodels: list[LogTauHModel]) -> list[LogTauHModel]:
        '''
        Associates fit and fix dicts with a list of logmodels by instantiating
        each logmodel with the specified parameters

        Parameters
        ----------

        fit_vars: list[dict[str, float | str]]
            List of fit dicts, with keys as PARNAMES of each LogTauHModel
            and values as either the string 'guess' or a float value
        fix_vars: list[dict[str, float | str]]
            List of fix dicts, with keys as PARNAMES of each LogTauHModel
            and values as either the string 'guess' or a float value
        logmodels: list[LogTauHModel]
            List of uninstantiated LogTauHModel objects

        Returns
        -------
        list[LogTauHModel]
            Instantiated LogTauHModels with fit and fix dicts applied
        '''

        marked = [False] * len(fit_vars)

        instantiated_models = []

        for logmodel in logmodels:
            for it, (fitvar_set, fix_var_set) in enumerate(zip(fit_vars, fix_vars)): # noqa
                if marked[it]:
                    continue
                elif all([k in logmodel.PARNAMES for k in fitvar_set.keys()]): # noqa
                    if all([k in logmodel.PARNAMES for k in fix_var_set.keys()]) or not len(fix_var_set): # noqa
                        instantiated_models.append(
                            logmodel(fitvar_set, fix_var_set)
                        )
                        marked[it] = True

        return instantiated_models

    @classmethod
    def residual_from_float_list(cls, new_vals: npt.ArrayLike,
                                 logmodels: list[LogTauHModel],
                                 fields: npt.ArrayLike,
                                 lograte: npt.ArrayLike,
                                 sigma: npt.ArrayLike = []) -> npt.NDArray:
        '''
        Wrapper for `residuals` method, takes new values from fitting routine
        which provides list[float], to construct new fit_vars dict, then
        runs `residuals` method.

        Parameters
        ----------
        new_vals: array_like
            This iteration's fit parameter values provided by least_squares
            this has the same order as fit_vars.keys
        logmodels: list[LogTauHModel]
            Models to use
        fields: array_like
            Field values (Oe) at which model function is evaluated
        lograte: array_like
            True (experimental) values of log10(relaxation rate)
        sigma: array_like
            Standard deviation of tau in logspace

        Returns
        -------
        ndarray of floats
            Residuals
        '''

        # Swap fit values for new values from fit routine
        new_fit_vars = []

        it = 0
        for logmodel in logmodels:
            new_dict = {}
            for name in logmodel.fit_vars.keys():
                new_dict[name] = new_vals[it]
                it += 1
            new_fit_vars.append(new_dict)

        residuals = cls.residuals(
            logmodels, new_fit_vars, fields, lograte
        )

        if len(sigma):
            residuals /= sigma

        return residuals

    @staticmethod
    def residuals(logmodels: list[LogTauHModel],
                  new_fit_vars: list[dict[str, float]], fields: npt.ArrayLike,
                  true_lograte: npt.ArrayLike) -> npt.NDArray:
        '''
        Calculates difference between experimental log10(tau^-1)
        and log10(tau^-1) obtained from the sum of the provided logmodels
        using the provided fit variable values at provided fields

        Parameters
        ----------
        logmodels: list[LogTauHModel]
            LogTauHModels which will be evaluated
        new_fit_vars: list[dict[str, float]]
            fit dicts for each LogTauHModel, must have same order as logmodel
            if no vars to fit for that model, then empty dict is given
        fields: array_like
            Experimental fields (Oe)
        true_lograte: array_like
            Experimental Log10(rate)s

        Returns
        -------
        ndarray of floats
            Log10(rate)_trial - Log10(rate)_exp for each temperature
        '''

        # Calculate model log10(relaxation rate) using parameters
        # as sum of contributions from each process
        trial_lograte = np.zeros(len(fields))

        for logmodel, fit_vars in zip(logmodels, new_fit_vars):
            all_vars = {**logmodel.fix_vars, **fit_vars}
            trial_lograte += 10**logmodel.model(all_vars, fields)

        # sum in linear space, then take log
        trial_lograte = np.log10(trial_lograte)

        residuals = trial_lograte - true_lograte

        return residuals

    def fit_to(self, dataset: TauHDataset, verbose: bool = True) -> None:
        '''
        Fits model to Dataset

        Parameters
        ----------
        dataset: TauTDataset
            Dataset to which a model of rate vs fields will be fitted
        verbose: bool, default True
            If True, prints information to terminal

        Returns
        -------
        None
        '''

        # Initial guess is a list of fitvars values
        guess = [
            value for logmodel in self.logmodels
            for value in logmodel.fit_vars.values()
        ]

        bounds = np.array([
            logmodel.BOUNDS[name] for logmodel in self.logmodels
            for name in logmodel.fit_vars.keys()
        ]).T

        curr_fit = least_squares(
            self.residual_from_float_list,
            args=[
                self.logmodels,
                dataset.fields,
                np.log10(dataset.rates),
                dataset.lograte_pm
            ],
            x0=guess,
            bounds=bounds,
            jac='3-point'
        )

        if curr_fit.status == 0:
            if verbose:
                ut.cprint(
                    '\n Fit failed - Too many iterations',
                    'black_yellowbg'
                )

            n_fitted_pars = np.sum(
                [len(logmodel.fit_vars.keys()) for logmodel in self.logmodels]
            )

            stdev = [np.nan] * n_fitted_pars
            self.fit_status = False
        else:

            stdev, no_stdev = stats.svd_stdev(curr_fit)

            self.fit_status = True

        # Add parameters, status and stdev to each LogTauTModel
        it = 0
        for logmodel in self.logmodels:

            # Name of fitted variables in this logmodel
            fit_var_names = logmodel.fit_vars.keys()
            # Number of parameters for this logmodel
            n_pars = len(fit_var_names)

            # Set each standard deviation
            _stdev = stdev[it: it + n_pars]
            logmodel.fit_stdev = {
                label: val
                for label, val in zip(
                    fit_var_names, _stdev
                )
            }

            # Report singular values=0 of Jacobian
            # and indicate that std_dev cannot be calculated
            sings = no_stdev[it: it + n_pars]
            for par, si in zip(fit_var_names, sings):
                if verbose and not si:
                    ut.cprint(
                        f'Warning: Jacobian is degenerate for {par}, standard deviation cannot be found, and is set to zero\n', # noqa
                        'black_yellowbg'
                    )

            # Set final fitted values
            _vals = curr_fit.x[it: it + n_pars]
            logmodel.final_var_values = {
                name: value
                for name, value in zip(fit_var_names, _vals)
            }
            # and fixed values
            for key, val in logmodel.fix_vars.items():
                logmodel.final_var_values[key] = val

            it += n_pars

        return


class TauTDataset():
    '''
    Contains experimental rates, rate bounds (+-) and temperatures

    Parameters
    ----------
    rates: array_like
        Relaxation rates in seconds^-1
    temperatures: array_like
        Temperature values (K)
    lograte_pm: array_like, optional
        Plus-Minus of log10(rates) in logspace, assumed to be symmetric\n
        Not! log(rate_pm)

    Attributes
    ----------
    rates: ndarray of floats
        Relaxation rates in seconds^-1
    temperatures: ndarray of floats
        Temperature values (K)
    lograte_pm: ndarray of floats
        Plus-minus of log10(rates) in logspace,
        assumed to be symmetric, size is (n_rates,1)\n
        Not! log(rate_pm)
    rate_pm: ndarray of floats
        Plus-minus of rates in linspace,
        will be asymmetric, size is (n_rates,2)\n
        not! 10**(lograte_pm)
    '''
    def __init__(self, rates: npt.ArrayLike, temperatures: npt.ArrayLike,
                 lograte_pm: npt.ArrayLike = []):

        self.rates = np.asarray(rates)
        self.temperatures = np.asarray(temperatures)
        self.lograte_pm = np.asarray(lograte_pm)

        return

    @property
    def lograte_pm(self) -> npt.NDArray:
        return self._lograte_pm

    @lograte_pm.setter
    def lograte_pm(self, value: npt.ArrayLike):

        if isinstance(value, float):
            raise ValueError('lograte_pm must be list')
        elif len(np.shape(value)) != 1:
            raise ValueError('lograte_pm must be symmetric, i.e. (1, n_rates)')
        if not len(value):
            self._lograte_pm = []
            self.rate_pm = []
        else:
            # Use symmetric lograte_pm to obtain difference in rates in linear
            # space - n.b. these will be asymmetric
            self._lograte_pm = np.asarray(value)
            self.rate_pm = self.lograte_pm_to_pm(self.rates, self.lograte_pm)
        return

    @classmethod
    def from_raw(cls, temperatures: npt.ArrayLike, lntaus: npt.ArrayLike,
                 lntau_stdevs: npt.ArrayLike, lntau_fus: npt.ArrayLike,
                 lntau_fls: npt.ArrayLike) -> 'TauTDataset':
        '''
        Creates dataset from raw values of rates, temperatures, ln standard
        deviation, and upper and lower lntau values

        Parameters
        ----------
        temperatures: array_like
            Temperatures in units of Kelvin
        lntaus: array_like
            ln(tau) values  in units of ln(seconds)
        lntau_stdev: array_like
            Standard deviation of ln(tau) in units of ln(seconds)
            These are intrinsic to AC or DC model
        lntau_fus: array_like
            Upper bound of fitted ln(tau) computed using uncertainties from
            fitted parameters
        lntau_fls: array_like
            Lower bound of fitted ln(tau) computed using uncertainties from
            fitted parameters

        Returns
        -------
        TauTDataset
           Single Dataset, rate vs T
        '''

        lntaus = np.array(lntaus)

        taus = np.array([
            np.exp(lntime)
            for lntime in lntaus
        ])

        rates = [tau**-1 for tau in taus]

        # Upper and lower lntau using standard deviation
        # from distribution
        model_upper_tau = np.exp(lntaus + lntau_stdevs)
        model_lower_tau = np.exp(lntaus - lntau_stdevs)

        # Take element wise maximum of these to find max standard deviation
        # considering both stdev inherent to AC/DC model distribution, and from
        # fitting of AC/DC model parameters

        upper_tau = np.maximum(np.exp(lntau_fus), model_upper_tau)
        lower_tau = np.minimum(np.exp(lntau_fls), model_lower_tau)

        # Difference in rates in log space, used as standard deviation in
        # log(tau), required by fitting routine
        # THIS IS NOT!!!! log10(rate_ul_diff)
        # log(sigma(tau)) != sigma(log(tau))
        lograte_ul_diff = [
            np.log10(rates) - np.log10(upper_tau**-1),
            np.log10(lower_tau**-1) - np.log10(rates)
        ]

        # Take maximum of difference in rates in log space
        # If differences arise from model stdev then will be symmetric
        # in log space
        # but if from previous least squares will be asymmetric
        # so take largest and treat as symmetric
        # Get rid of nans from log of negative relaxation time
        lograte_ul_diff = np.nan_to_num(lograte_ul_diff, 0.)
        lograte_pm = np.maximum(
            lograte_ul_diff[0],
            lograte_ul_diff[1]
        )

        return cls(rates, temperatures, lograte_pm)

    @classmethod
    def from_ac_dc(cls, models: list[ac.Model | dc.Model]) -> 'TauTDataset':
        '''
        Creates Dataset from list of fitted AC or DC models

        Parameters
        ----------
        models: list[ac.Model]
            Models of AC or DC data, at least one in list must be
            successfully fitted (i.e. fit_status=True)

        Returns
        -------
        list[TauTDataset]
            Datasets, each rate vs T
            List has 1 dataset if only single-tau models are given\n
            or 2 datasets if >1 double-tau models present in ``models``

        '''
        double_tau_models = [
            ac.DoubleGDebyeEqualChiModel,
            ac.DoubleGDebyeModel,
            dc.DoubleExponentialModel
        ]

        ml1 = []
        ml2 = []

        for model in models:
            # Split double tau models into two single tau models
            if type(model) in double_tau_models:
                m1, m2 = cls.split_model(model)
                ml1.append(m1)
                ml2.append(m2)
            else:
                ml1.append(model)
                ml2.append(model)

        # Process first set of models
        datasets = [cls.from_raw(*cls.extract_ac_dc_model(ml1))]

        # and add on second set if desired
        if any([type(model) in double_tau_models for model in models]):
            datasets.append(cls.from_raw(*cls.extract_ac_dc_model(ml2)))

        return datasets

    @staticmethod
    def split_model(model: ac.DoubleGDebyeModel | ac.DoubleGDebyeEqualChiModel | dc.DoubleExponentialModel) -> list[object]: # noqa
        '''
        Splits double tau models into placeholder single tau models
        returned objects are not actual ac.Model or dc.Model instances,
        they simply possess the attributes required by this class'
        extract_ac_dc_model method.
        '''

        m1 = type(
            'fake_model_1',
            (object,),
            {
                'fit_status': model.fit_status,
                'lntau_expect': model.lntau_expect[0],
                'lntau_stdev': model.lntau_stdev[0],
                'lntau_fit_ul': model.lntau_fit_ul[0],
                'temperature': model.temperature
            }
        )

        m2 = type(
            'fake_model_2',
            (object,),
            {
                'fit_status': model.fit_status,
                'lntau_expect': model.lntau_expect[1],
                'lntau_stdev': model.lntau_stdev[1],
                'lntau_fit_ul': model.lntau_fit_ul[1],
                'temperature': model.temperature
            }
        )

        return m1, m2

    @classmethod
    def from_ccfit2_files(cls, file_names: str | list[str]) -> 'TauTDataset':
        '''
        Creates Dataset from ccfit2 AC/DC parameter file(s)

        Parameters
        ----------
        file_names: str | list[str]
            Filenames of ccfit2 AC/DC parameter file(s)

        Returns
        -------
        TauTDataset
            Single Dataset, rate vs T
        '''

        if isinstance(file_names, str):
            file_names = [file_names]

        # Find encoding of input files
        encodings = [
            ut.detect_encoding(file)
            for file in file_names
        ]

        headers = {
            'temps': ['T'],
            'lntau': ['<ln(tau)>'],
            'lntau_stdevs': ['sigma_ln(tau)'],
            'lntau_fu': ['fit_upper_ln(tau)'],
            'lntau_fl': ['fit_lower_ln(tau)']
        }

        temps, lntaus, lntau_stdevs, lntau_fls, lntau_fus = [], [], [], [], []

        bounds = True

        for file, encoding in zip(file_names, encodings):

            # Get file headers
            header_indices, _ = ut.parse_headers(
                file, 0, headers, delim=None
            )

            if header_indices['temps'] == -1:
                raise ValueError(f'Cannot find temperatures in {file}')
            elif header_indices['lntau'] == -1:
                raise ValueError(f'Cannot find <ln(tau)> in {file}')

            # Columns to extract from file
            cols = [header_indices[he] for he in headers.keys()]

            converters = {
                it: lambda s: (float(s.strip() or np.NaN)) for it in cols
            }

            # Read required columns of file
            data = np.loadtxt(
                file,
                skiprows=1,
                converters=converters,
                usecols=cols,
                encoding=encoding
            )

            # If bound headers not found then turn off bounds for all files
            optional_indices = [
                header_indices['lntau_stdevs'],
                header_indices['lntau_fu'],
                header_indices['lntau_fl']
            ]
            if -1 not in optional_indices:
                lntau_stdevs.append(data[:, 2].tolist())
                lntau_fus.append(data[:, 3].tolist())
                lntau_fls.append(data[:, 4].tolist())
            else:
                bounds = False

            # Add to big lists
            temps.append(data[:, 0].tolist())
            lntaus.append(data[:, 1].tolist())

        # Sort all data by temperature
        order = np.argsort(np.array(ut.flatten_recursive(temps)))

        if bounds:
            # Create dataset from all data
            dataset = cls.from_raw(
                np.array(ut.flatten_recursive(temps))[order],
                np.array(ut.flatten_recursive(lntaus))[order],
                np.array(ut.flatten_recursive(lntau_stdevs))[order],
                np.array(ut.flatten_recursive(lntau_fus))[order],
                np.array(ut.flatten_recursive(lntau_fls))[order]
            )

        else:
            dataset = cls(
                np.exp(-np.array(ut.flatten_recursive(lntaus))[order]),
                np.array(ut.flatten_recursive(temps))[order],
            )

        return dataset

    @classmethod
    def from_rate_files(cls, file_names: str | list[str]) -> 'TauTDataset':
        '''
        Creates Dataset from file(s) containingthe headers\n
        T, rate, <upper>, <lower>\n
        The last two are optional

        Parameters
        ----------
        file_names: str | list[str]
            Filenames of ccfit2 AC/DC parameter file(s)

        Returns
        -------
        TauTDataset
            Single Dataset, rate vs T
        '''

        if isinstance(file_names, str):
            file_names = [file_names]

        # Find encoding of input files
        encodings = [
            ut.detect_encoding(file)
            for file in file_names
        ]

        headers = {
            'temps': ['T'],
            'rate': ['rate'],
            'upper': ['upper'],
            'lower': ['lower']
        }

        temps, rates, upper, lower = [], [], [], []

        indices = []

        bounds = True

        for file, encoding in zip(file_names, encodings):

            # Get file headers
            header_indices, _ = ut.parse_headers(
                file, 0, headers, delim=None
            )

            indices.append(header_indices)

            if header_indices['temps'] == -1:
                raise ValueError(f'Cannot find temperatures in {file}')
            elif header_indices['rate'] == -1:
                raise ValueError(f'Cannot find rates in {file}')

            # Columns to extract from file
            cols = [header_indices[he] for he in headers.keys()]

            converters = {
                it: lambda s: (float(s.strip() or np.NaN)) for it in cols
            }

            # Read required columns of file
            data = np.loadtxt(
                file,
                skiprows=1,
                converters=converters,
                usecols=cols,
                encoding=encoding
            )

            # Add to big lists
            temps.append(data[:, 0].tolist())
            rates.append(data[:, 1].tolist())

            # If either header not found, then skip
            if -1 not in [header_indices['upper'], header_indices['lower']]:
                upper.append(data[:, 2].tolist())
                lower.append(data[:, 3].tolist())
            else:
                bounds = False

        temps = np.array(ut.flatten_recursive(temps))
        rates = np.array(ut.flatten_recursive(rates))

        # Find low to high temperature order
        order = np.argsort(np.array(temps))

        # Calculate lograte_pm as difference in logarithmic domain
        if bounds:
            lower = np.array(ut.flatten_recursive(lower))
            lower_logdiff = np.log10(rates) - np.log10(lower)
            upper = np.array(ut.flatten_recursive(upper))
            upper_logdiff = np.log10(upper) - np.log10(rates)
            lograte_pm = np.maximum(lower_logdiff, upper_logdiff)[order]
        else:
            lograte_pm = []

        # Create dataset from all data
        dataset = cls(rates[order], temps[order], lograte_pm)

        return dataset

    @staticmethod
    def extract_ac_dc_model(models: list[ac.Model | dc.Model]) -> tuple[list[float], list[float], list[float], list[float]]: # noqa
        '''
        Extracts, from AC.Model and DC.Model, the parameters required to
        generate a TauTDataset

        Parameters
        ----------
        models: list[ac.Model | dc.Model]
            AC or DC models, one per temperature and static field

        Returns
        -------
        list[float]
            Temperatures in units of Kelvin
        list[float]
            ln(tau) values  in units of ln(seconds)
        list[float]
            Standard deviation of ln(tau) in units of ln(seconds)
            These are intrinsic to AC or DC model
        list[float]
            Upper bound of fitted ln(tau) computed using uncertainties from
            fitted parameters
        list[float]
            Lower bound of fitted ln(tau) computed using uncertainties from
            fitted parameters
        '''

        # <ln(tau)>
        lntaus = np.array([
            model.lntau_expect
            for model in models
            if model.fit_status
        ])

        # Standard deviation inherent to model distribution
        # This is sigma of lntau, so MUST be applied to lntau, not tau
        lntau_stdevs = [
            model.lntau_stdev
            for model in models
            if model.fit_status
        ]

        # Upper and lower bounds of ln(tau) from fit uncertainty
        # in fitted parameters
        lntau_fus = [
            model.lntau_fit_ul[0]
            for model in models
            if model.fit_status
        ]

        lntau_fls = [
            model.lntau_fit_ul[1]
            for model in models
            if model.fit_status
        ]

        temperatures = [
            model.temperature
            for model in models
            if model.fit_status
        ]

        # Sort by temperature, low to high
        order = np.argsort(temperatures)
        temperatures = [temperatures[it] for it in order]
        lntaus = [lntaus[it] for it in order]
        lntau_stdevs = [lntau_stdevs[it] for it in order]
        lntau_fus = [lntau_fus[it] for it in order]
        lntau_fls = [lntau_fls[it] for it in order]

        return temperatures, lntaus, lntau_stdevs, lntau_fus, lntau_fls

    @staticmethod
    def lograte_pm_to_pm(rates: npt.ArrayLike,
                         lograte_pm: npt.ArrayLike) -> npt.NDArray:
        '''
        Converts symmetric log10 error of log10rates to asymmetric linear
        errors.

        Parameters
        ----------
        rates: array_like
            Rates in linear space in s^-1
        lograte_pm: array_like
            +-log10(rate), symmetric, same number of elements as rates

        Returns
        -------
        ndarray of floats
            (2, n_rates) list of upper and lower bounds in linear space
        '''

        rate_pm = np.array([
            rates - 10**(np.log10(rates) - lograte_pm),
            10**(np.log10(rates) + lograte_pm) - rates
        ])

        return rate_pm


class LogFDQTMModel(LogTauHModel):
    '''
    Log(FDQTM) Model of log10(Relaxation rate) vs field
    '''

    #: Model name
    NAME = 'FD-QTM'
    #: Model name with log brackets
    LNAME = 'Log(FD-QTM)'

    #: Model Parameter name strings
    PARNAMES = [
        'Q',
        'Q_H',
        'p'
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'Q': r'$Q$',
        'Q_H': r'$Q_\mathregular{H}$',
        'p': r'$p$'
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'Q_H': 'Q<sub>H</sub>',
        'Q': 'Q',
        'p': 'p'
    }

    #: Model Parameter unit strings
    UNITS = {
        'Q': 'log10[s]',
        'Q_H': 'log10[Oe^p]',
        'p': ''
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'Q': r'$\log_\mathregular{10}\left[\mathregular{s}\right]$',
        'Q_H': r'$\log_\mathregular{10}\left[\mathregular{Oe}^{p}\right]$', # noqa
        'p': ''
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'Q': r'log<sub>10</sub>[s]',
        'Q_H': r'log<sub>10</sub>[Oe<sup>p</sup>]',
        'p': ''
    }

    #: Model Parameter bounds
    BOUNDS = {
        'Q': [-np.inf, np.inf],
        'Q_H': [-np.inf, np.inf],
        'p': [0, np.inf]
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'Q': -2,
            'Q_H': -2,
            'p': 2
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              fields: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(FD-QTM) model of log10(relaxation rate)
        using provided parameter and field values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        fields: array_like
            field values (Oe) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of field

        '''

        q = parameters['Q']
        qh = parameters['Q_H']
        p = parameters['p']

        lograte = np.log10(10**-q / (1 + 10**-qh * np.asarray(fields)**p))

        return lograte


class LogRamanIIModel(LogTauHModel):
    '''
    Log(Raman-II) Model of log10(Relaxation rate) vs field
    '''

    #: Model name
    NAME = 'Raman-II'

    #: Model name with log brackets
    LNAME = 'Log(Raman-II)'

    #: Model Parameter name strings
    PARNAMES = [
        'C',
        'm',
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'C': '$C$',
        'm': '$m$'
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'C': 'C',
        'm': 'm'
    }

    #: Model Parameter unit strings
    UNITS = {
        'C': 'log10[Oe^-m s^-1]',
        'm': ''
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'C': r'$\log_\mathregular{10}\left[\mathregular{Oe}^{-m} \ \mathregular{s}^\mathregular{-1}\right]$', # noqa
        'm': ''
    }

    #: Model Parameter name HTML strings
    UNITS_HTML = {
        'C': r'log<sub>10</sub>[Oe<sup>-m</sup> s<sup>-1</sup>]',
        'm': ''
    }

    #: Model Parameter bounds
    BOUNDS = {
        'C': [-np.inf, np.inf],
        'm': [0, np.inf],
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'C': -4,
            'm': 4
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              fields: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(Raman-II) model of log10(relaxation rate)
        using provided parameter and field values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        fields: array_like
            field values (Oe) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of field

        '''

        c = parameters['C']
        m = parameters['m']

        lograte = np.log10(10**c * np.asarray(fields)**m)

        return lograte


class LogConstantModel(LogTauHModel):
    '''
    Log(Constant) Model of log10(Relaxation rate) vs field
    '''

    #: Model name
    NAME = 'Constant'

    #: Model name with log brackets
    LNAME = 'Log(Constant)'

    #: Model Parameter name strings
    PARNAMES = [
        'Ct',
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'Ct': r'$Ct$',
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'Ct': 'Ct'
    }

    #: Model Parameter unit strings
    UNITS = {
        'Ct': 'log10[s^-1]'
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'Ct': r'$\log_\mathregular{10}\left[\mathregular{s}^\mathregular{-1}\right]$', # noqa
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'Ct': r'log<sub>10</sub>[s<sup>-1</sup>]'
    }

    #: Model parameter bounds
    BOUNDS = {
        'Ct': [-np.inf, np.inf],
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'Ct': -4
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              fields: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(Constant) model of log10(relaxation rate)
        using provided parameter and field values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        fields: array_like
            field values (Oe) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of field

        '''

        ct = parameters['Ct']

        lograte = np.zeros(len(fields)) + np.log10(10**ct)

        return lograte


class LogBVVRamanIIModel(LogTauHModel):
    '''
    Log(Brons-Van-Vleck * Raman-II) Model of log10(Relaxation rate) vs field
    '''

    #: Model name
    NAME = 'Brons-Van-Vleck * Raman-II'

    #: Model name with log brackets
    LNAME = 'Log(Brons-Van-Vleck * Raman-II)'

    #: Model Parameter name strings
    PARNAMES = [
        'e',
        'f',
        'C',
        'm'
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'e': r'$e$',
        'f': r'$f$',
        'C': r'$C$',
        'm': r'$m$',
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'e': 'e',
        'f': 'f',
        'C': 'C',
        'm': 'm'
    }

    #: Model Parameter unit strings
    UNITS = {
        'e': 'log10[Oe^-2]',
        'f': 'log10[Oe^-2]',
        'C': 'log10[s^-1 Oe^-m]',
        'm': ''
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'e': r'$\log_\mathregular{10}\left[\mathregular{Oe}^\mathregular{-2}\right]$', # noqa
        'f': r'$\log_\mathregular{10}\left[\mathregular{Oe}^\mathregular{-2}\right]$', # noqa
        'C': r'$\log_\mathregular{10}\left[\mathregular{s}^\mathregular{-1} \mathregular{Oe}^\mathregular{-2}\right]$', # noqa
        'm': ''
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'e': r'log<sub>10</sub>[Oe<sup>-2</sup>]',
        'f': r'log<sub>10</sub>[Oe<sup>-2</sup>]',
        'C': r'log<sub>10</sub>[s<sup>-1</sup> Oe<sup>-m</sup>]',
        'm': ''
    }

    #: Model parameter bounds
    BOUNDS = {
        'e': [-np.inf, np.inf],
        'f': [-np.inf, np.inf],
        'C': [-np.inf, np.inf],
        'm': [0, np.inf]
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'e': -5.,
            'f': -5.,
            'C': -4,
            'm': 4.
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              fields: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(Raman-II) model of log10(relaxation rate)
        using provided parameter and field values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        fields: array_like
            field values (Oe) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of field

        '''

        e = parameters['e']
        f = parameters['f']
        C = parameters['C']
        m = parameters['m']

        lograte = np.log10(
            (10**C * np.asarray(fields)**m) * (1 + 10**e * np.asarray(fields)**2)/(1 + 10**f * np.asarray(fields)**2) # noqa
        )

        return lograte


class LogBVVConstantModel(LogTauHModel):
    '''
    Log(Brons-Van-Vleck * Constant) Model of log10(Relaxation rate) vs field
    '''

    #: Model name
    NAME = 'Brons-Van-Vleck * Constant'

    #: Model name with log brackets
    LNAME = 'Log(Brons-Van-Vleck * Constant)'

    #: Model Parameter name strings
    PARNAMES = [
        'e',
        'f',
        'Ct'
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'e': r'$e$',
        'f': r'$f$',
        'Ct': r'$Ct$'
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'e': 'e',
        'f': 'f',
        'Ct': 'Ct'
    }

    #: Model Parameter unit strings
    UNITS = {
        'e': 'log10[Oe^-2]',
        'f': 'log10[Oe^-2]',
        'Ct': 'log10[s^-1]'
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'e': r'$\log_\mathregular{10}\left[\mathregular{Oe}^\mathregular{-2}\right]$', # noqa
        'f': r'$\log_\mathregular{10}\left[\mathregular{Oe}^\mathregular{-2}\right]$', # noqa
        'Ct': r'$\log_\mathregular{10}\left[\mathregular{s}^\mathregular{-1}\right]$', # noqa
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'e': r'log<sub>10</sub>[Oe<sup>-2</sup>]',
        'f': r'log<sub>10</sub>[Oe<sup>-2</sup>]',
        'Ct': r'log<sub>10</sub>[s<sup>-1</sup>]'
    }

    #: Model parameter bounds
    BOUNDS = {
        'e': [-np.inf, np.inf],
        'f': [-np.inf, np.inf],
        'Ct': [-np.inf, np.inf]
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'e': -5.,
            'f': -5.,
            'Ct': -4
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              fields: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(LogBVVConstantModel) model of log10(relaxation rate)
        using provided parameter and field values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        fields: array_like
            field values (Oe) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of field

        '''

        e = parameters['e']
        f = parameters['f']
        Ct = parameters['Ct']

        lograte = np.log10(
            10**Ct * (1 + 10**e * np.asarray(fields)**2) / (1 + 10**f * np.asarray(fields)**2) # noqa
        )

        return lograte


class LogTauTModel(ABC):
    '''
    Abstract class on which all phenomenological models of
    temperature-dependent magnetic relaxation Log10(rate) are based
    '''

    @property
    @abstractmethod
    def NAME() -> str:
        'string name of model'
        raise NotImplementedError

    @property
    @abstractmethod
    def LNAME() -> str:
        'string name of model with Log() around it, e.g. Log(Orbach)'
        raise NotImplementedError

    @property
    @abstractmethod
    def PARNAMES() -> list[str]:
        'string names of parameters which can be fitted or fixed'
        raise NotImplementedError

    @property
    @abstractmethod
    def VARNAMES_MM() -> dict[str, str]:
        '''
        Mathmode (i.e. $$, latex ) versions of PARNAMES\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are mathmode strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def VARNAMES_HTML() -> dict[str, str]:
        '''
        HTML versions of PARNAMES\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are mathmode strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def UNITS() -> dict[str, str]:
        '''
        string names of units of PARNAMES\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are unit name strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def UNITS_MM() -> dict[str, str]:
        '''
        Mathmode (i.e. $$, latex ) versions of UNITS\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are unit name strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def UNITS_HTML() -> dict[str, str]:
        '''
        HTML versions of UNITS\n
        Keys are strings from PARNAMES plus any other variables which
        might be needed\n
        Values are unit name strings
        '''
        raise NotImplementedError

    @property
    @abstractmethod
    def BOUNDS() -> dict[str, list[float, float]]:
        '''
        Bounds for each parameter of model\n
        Keys: parameter name\n
        Values: [upper, lower]\n
        used by scipy least_squares
        '''
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def model(parameters: dict[str, float],
              temperatures: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates model function of log(relaxation rate) using provided
        parameter and temperature values.

        Parameters
        ----------
        parameters: array_like
            Parameters to use in model function
        temperatures: array_like
            Temperature values (K) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of temperature

        '''
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def set_initial_vals(parameters: dict[str, float]) -> dict[str, float]:
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''
        raise NotImplementedError

    def __init__(self, fit_vars: dict[str, float | str],
                 fix_vars: dict[str, float | str]):
        '''
        Set default values for mandatory attributes
        '''

        # Replace any 'guess' strings with proper guesses
        self.fit_vars = self.set_initial_vals(fit_vars)
        self.fix_vars = self.set_initial_vals(fix_vars)

        # Check all PARNAMES are provided in fit+fix
        input_names = [
            name for name in {**self.fit_vars, **self.fix_vars}.keys()
        ]

        if any([req_name not in input_names for req_name in self.PARNAMES]):
            raise ValueError(
                'Missing fit/fix parameters in {} Model'.format(
                    self.NAME
                )
            )

        # Check for duplicates in fit and fix
        dupe = self.fit_vars.keys() & self.fix_vars.keys()
        if dupe:
            raise ValueError(
                f'Duplicate keys {dupe} provided to both fit and fix'
            )

        # Final model parameter values
        # fitted and fixed
        self._final_var_values = {
            var: None
            for var in self.PARNAMES
        }

        # Fit status and temperature
        self._fit_status = False

        # Fit standard deviation
        self._fit_stdev = {
            var: None
            for var in self.fit_vars.keys()
        }

        return

    @property
    def fit_status(self) -> bool:
        'True if fit successful, else False'
        return self._fit_status

    @fit_status.setter
    def fit_status(self, value: bool):
        if isinstance(value, bool):
            self._fit_status = value
        else:
            raise TypeError
        return

    @property
    def final_var_values(self) -> float:
        'Final values of parameters, both fitted and fixed'
        return self._final_var_values

    @final_var_values.setter
    def final_var_values(self, value: dict):
        if isinstance(value, dict):
            self._final_var_values = value
        else:
            raise TypeError
        return

    @property
    def fit_stdev(self) -> float:
        'Standard deviation on fitted parameters, from fitting routine'
        return self._fit_stdev

    @fit_stdev.setter
    def fit_stdev(self, value: dict):
        if isinstance(value, dict):
            self._fit_stdev = value
        else:
            raise TypeError
        return

    @property
    def fix_vars(self) -> float:
        '''
        Parameters to fix (i.e. not fit)
        keys are names in PARNAMES, values are values
        '''
        # Check for implementation in Model class init
        return self._fix_vars

    @fix_vars.setter
    def fix_vars(self, value: dict):
        if isinstance(value, dict):
            if any([key not in self.PARNAMES for key in value.keys()]):
                raise KeyError('Unknown variable names provided to fix')
            self._fix_vars = value
        else:
            raise TypeError('fix must be dictionary')
        return

    @property
    def fit_vars(self) -> float:
        '''
        Parameters to fit
        keys are names in PARNAMES, values are values
        '''
        # Check for implementation in Model class init
        return self._fit_vars

    @fit_vars.setter
    def fit_vars(self, value: dict):
        if isinstance(value, dict):
            if any([key not in self.PARNAMES for key in value.keys()]):
                raise KeyError('Unknown variable names provided to fit')
            self._fit_vars = value
        else:
            raise TypeError('Fit must be dictionary')
        return

    @classmethod
    def residuals(cls, params: dict[str, float], temperatures: npt.ArrayLike,
                  true_lograte: npt.ArrayLike) -> npt.NDArray:
        '''
        Calculates difference between measured log10(relaxation rate) and trial
        from model

        Parameters
        ----------
        params: array_like
            model parameter values
        temperatures: array_like
            Temperature values (K) at which model function is evaluated
        true_lograte: array_like
            true (experimental) values of log10(relaxation rate)

        Returns
        -------
        ndarray of floats
            Residuals
        '''

        # Calculate model log10(relaxation rate) using parameters
        trial_lograte = cls.model(params, temperatures)

        residuals = trial_lograte - true_lograte

        return residuals

    @classmethod
    def residual_from_float_list(cls, new_vals: npt.ArrayLike,
                                 fit_vars: dict[str, float],
                                 fix_vars: dict[str, float],
                                 temperatures: npt.ArrayLike,
                                 lograte: npt.ArrayLike,
                                 sigma: npt.ArrayLike = []) -> npt.NDArray:
        '''
        Wrapper for `residuals` method, takes new values from scipy
        least_squares which provides list[float], to construct new
        fit_vars dict, then runs `residuals` method.

        Parameters
        ----------
        new_vals: array_like
            This iteration's fit parameter values provided by least_squares
            this has the same order at fit_vars.keys
        fit_vars: dict[str, float]
            Parameter to fit in model function\n
            keys are PARNAMES, values are float values
        fix_vars: dict[str, float]
            Parameter which remain fixed in model function\n
            keys are PARNAMES, values are float values
        temperatures: array_like
            Temperature values (K) at which model function is evaluated
        lograte: array_like
            True (experimental) values of log10(relaxation rate)
        sigma: array_like
            Standard deviation of tau in logspace

        Returns
        -------
        ndarray of floats
            Residuals
        '''

        # Swap fit values for new values from fit routine
        new_fit_vars = {
            name: guess
            for guess, name in zip(new_vals, fit_vars.keys())
        }

        # And make combined dict of fit and fixed
        # variable names (keys) and values
        all_vars = {**fix_vars, **new_fit_vars}

        residuals = cls.residuals(all_vars, temperatures, lograte)

        if len(sigma):
            residuals /= sigma

        return residuals

    def fit_to(self, dataset: TauTDataset,
               guess: str | dict[str, float] = 'predefined',
               verbose: bool = True) -> None:
        '''
        Fits model to Dataset

        Parameters
        ----------
        dataset: TauTDataset
            Dataset to which a model of rate vs temperature will be fitted
        guess: str | dict[str, float], default 'predefined'
            Either string 'predefined', or dict of initial parameters
            used as starting guess with keys as parameter names and values as
            numerical values
        verbose: bool, default True
            If True, prints information to terminal

        Returns
        -------
        None
        '''

        # Get starting guesses, either predefined in self or given
        # by user
        if guess != 'predefined':
            guess = [
                guess[key] for key in self.fit_vars.keys()
            ]
        else:
            guess = [val for val in self.fit_vars.values()]

        # Get bounds for variables to be fitted
        bounds = np.array([
            self.BOUNDS[name]
            for name in self.fit_vars.keys()
        ]).T

        curr_fit = least_squares(
            self.residual_from_float_list,
            args=[
                self.fit_vars,
                self.fix_vars,
                dataset.temperatures,
                np.log10(dataset.rates),
                dataset.lograte_pm
            ],
            x0=guess,
            bounds=bounds
        )

        if curr_fit.status == 0:
            if verbose:
                ut.cprint(
                    '\n Fit failed - Too many iterations',
                    'black_yellowbg'
                )

            self.final_var_values = {
                name: value
                for name, value in zip(self.fit_vars, curr_fit.x)
            }
            self.fit_stdev = {
                label: np.nan
                for label in self.fit_vars.keys()
            }
            self.fit_status = False
        else:
            stdev, no_stdev = stats.svd_stdev(curr_fit)

            # Standard deviation error on the parameters
            self.fit_stdev = {
                label: val
                for label, val in zip(self.fit_vars.keys(), stdev)
            }

            self.fit_status = True

            # Report singular values=0 of Jacobian
            # and indicate that std_dev cannot be calculated
            for par, si in zip(self.fit_vars.keys(), no_stdev):
                if verbose and not si:
                    ut.cprint(
                        f'Warning: Jacobian is degenerate for {par}, standard deviation cannot be found, and is set to zero\n', # noqa
                        'black_yellowbg'
                    )

            # Set fitted values
            self.final_var_values = {
                name: value
                for name, value in zip(self.fit_vars.keys(), curr_fit.x)
            }
            # and fixed values
            for key, val in self.fix_vars.items():
                self.final_var_values[key] = val

        return


class LogOrbachModel(LogTauTModel):
    '''
    Log(Orbach) Model of log10(Relaxation rate) vs temperature
    '''

    #: Model name
    NAME = 'Orbach'
    #: Model name with log brackets
    LNAME = 'Log(Orbach)'

    #: Model Parameter name strings
    PARNAMES = [
        'u_eff', 'A',
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'u_eff': r'$U_\mathregular{eff}$',
        'A': r'$A$'
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'u_eff': 'U<sub>eff</sub>',
        'A': 'A'
    }

    #: Model Parameter unit strings
    UNITS = {
        'u_eff': r'K',
        'A': r'log10[s]'
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'u_eff': r'$\mathregular{K}$',
        'A': r'$\log_\mathregular{10}\left[\mathregular{s}\right]$' # noqa
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'u_eff': 'K',
        'A': 'log<sub>10</sub>[s]'
    }

    #: Model parameter bounds
    BOUNDS = {
        'u_eff': [0., np.inf],
        'A': [-np.inf, np.inf]
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'u_eff': 1500.,
            'A': -11
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              temperatures: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(Orbach) model of log10(relaxation rate)
        using provided parameter and temperature values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        temperatures: array_like
            temperature values (K) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of temperature

        '''

        u_eff = parameters['u_eff']
        a = parameters['A']

        lograte = np.log10(10**-a * np.exp(-u_eff / np.asarray(temperatures)))

        return lograte


class LogRamanModel(LogTauTModel):
    '''
    Log(Raman) Model of log10(Relaxation rate) vs temperature
    '''

    #: Model name
    NAME = 'Raman'
    #: Model name with log brackets
    LNAME = 'Log(Raman)'

    #: Model Parameter name strings
    PARNAMES = [
        'R', 'n',
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'R': r'$R$',
        'n': r'$n$'
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'R': 'R',
        'n': 'n'
    }

    #: Model Parameter unit strings
    UNITS = {
        'R': 'log10[s^-1 K^-n]',
        'n': ''
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'R': r'$\log_\mathregular{10}\left[\mathregular{s}^\mathregular{-1} \mathregular{K}^{-n}\right]$', # noqa
        'n': ''
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'R': 'log<sub>10</sub>[s<sup>-1</sup> K<sup>-n</sup>]',
        'n': ''
    }

    #: Model parameter bounds
    BOUNDS = {
        'R': [-np.inf, np.inf],
        'n': [0, np.inf]
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'R': -6,
            'n': 3
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              temperatures: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(Raman) model of log10(relaxation rate)
        using provided parameter and temperature values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        temperatures: array_like
            temperature values (K) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of temperature

        '''

        r = parameters['R']
        n = parameters['n']

        lograte = np.log10(10**r * np.asarray(temperatures)**n)

        return lograte


class LogQTMModel(LogTauTModel):
    '''
    Log(QTM) Model of log10(Relaxation rate) vs temperature
    '''
    #: Model name
    NAME = 'QTM'
    #: Model name with log brackets
    LNAME = 'Log(QTM)'

    #: Model Parameter name strings
    PARNAMES = [
        'Q'
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'Q': r'$Q$',
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'Q': 'Q',
    }

    #: Model Parameter unit strings
    UNITS = {
        'Q': 'log10[s]',
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'Q': r'$\log_\mathregular{10}\left[\mathregular{s}\right]$',
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'Q': r'log<sub>10</sub>[s]'
    }

    #: Model parameter bounds
    BOUNDS = {
        'Q': [-np.inf, np.inf]
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'Q': 1
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              temperatures: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(QTM) model of log10(relaxation rate)
        using provided parameter and temperature values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        temperatures: array_like
            temperature values (K) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of temperature

        '''

        q = parameters['Q']

        lograte = np.zeros(len(temperatures)) + np.log10(10**-q)

        return lograte


class LogDirectModel(LogTauTModel):
    '''
    Log(Direct) Model of log10(Relaxation rate) vs temperature
    '''
    #: Model name
    NAME = 'Direct'

    #: Model name with log brackets
    LNAME = 'Log(Direct)'

    #: Model Parameter name strings
    PARNAMES = [
        'D'
    ]

    #: Model Parameter name mathmode strings
    VARNAMES_MM = {
        'D': r'$D$',
    }

    #: Model Parameter name HTML strings
    VARNAMES_HTML = {
        'D': 'D'
    }

    #: Model Parameter unit strings
    UNITS = {
        'D': 'log10[s-1 K-1]',
    }

    #: Model Parameter unit mathmode strings
    UNITS_MM = {
        'D': r'$\log_\mathregular{10}\left[\mathregular{s}^\mathregular{-1} \mathregular{K}^\mathregular{-1}\right]$', # noqa
    }

    #: Model Parameter unit HTML strings
    UNITS_HTML = {
        'D': r's<sup>-1</sup> K<sup>-1</sup>'
    }

    #: Model parameter bounds
    BOUNDS = {
        'D': [-np.inf, np.inf]
    }

    @staticmethod
    def set_initial_vals(param_dict: dict[str, str | float]) -> dict[str, float]: # noqa
        '''
        Sets guess values for parameters if requested by user

        Parameters
        ----------
        param_dict: dict[str, str | float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are either float (actual value) or the string 'guess'

        Returns
        -------
        dict[str, float]
            Keys are fit/fix parameter names (see class.PARNAMES)\n
            Values are float (actual value) which are initial values of
            parameter
        '''

        # Make copy, any str values will be replaced
        new_param_dict = copy.copy(param_dict)

        # Guesses
        guessdict = {
            'D': -2
        }

        # Replace 'guess' with relevant guess
        for var, val in param_dict.items():
            if val == 'guess':
                new_param_dict[var] = guessdict[var]

        return new_param_dict

    @staticmethod
    def model(parameters: dict[str, float],
              temperatures: npt.ArrayLike) -> npt.NDArray:
        '''
        Evaluates log10(Direct) model of log10(relaxation rate)
        using provided parameter and temperature values.

        Parameters
        ----------
        parameters: dict[str, float]
            Parameters to use in model function, keys are given in
            class.PARNAMES
        temperatures: array_like
            temperature values (K) at which model function is evaluated

        Returns
        -------
        ndarray of floats
            log10(Relaxation rate) as a function of temperature

        '''

        d = parameters['D']

        lograte = np.log10(10**d * np.asarray(temperatures))

        return lograte


class MultiLogTauTModel():
    '''
    Takes multiple LogTauTModel objects and combines into a single object

    Parameters
    ----------
    fit_vars: list[dict[str, float | str]]
        List of fit dicts, with keys as PARNAMES of each LogTauTModel
        and values as either the string 'guess' or a float value
    fix_vars: list[dict[str, float | str]]
        List of fix dicts, with keys as PARNAMES of each LogTauTModel
        and values as either the string 'guess' or a float value
    logmodels: list[LogTauTModel]
        List of uninstantiated LogTauTModel objects

    Attributes
    ----------
    logmodels: list[LogTauTModel]
        List of LogTauTModel objects
    NAME: str
        Names of each LogTauTModel concatenated
    '''

    def __init__(self, logmodels: list[LogTauTModel],
                 fit_vars: list[dict[str, float | str]],
                 fix_vars: list[dict[str, float | str]]) -> None:

        # Instantiate each logmodel and create list of instantiated logmodels
        self.logmodels = self.process_fitfix(fit_vars, fix_vars, logmodels)

        self.NAME = [logmodel.NAME for logmodel in logmodels]
        self.NAME = ''.join(['{}+'.format(name) for name in self.NAME])[:-1]

        self._fit_status = False

        return

    @property
    def fit_status(self) -> bool:
        'True if fit successful, else False'
        return self._fit_status

    @fit_status.setter
    def fit_status(self, value: bool):
        if isinstance(value, bool):
            self._fit_status = value
        else:
            raise TypeError
        return

    @staticmethod
    def process_fitfix(fit_vars: list[dict[str, float | str]],
                       fix_vars: list[dict[str, float | str]],
                       logmodels: list[LogTauTModel]) -> list[LogTauTModel]:
        '''
        Associates fit and fix dicts with a list of logmodels by instantiating
        each logmodel with the specified parameters

        Parameters
        ----------

        fit_vars: list[dict[str, float | str]]
            List of fit dicts, with keys as PARNAMES of each LogTauTModel
            and values as either the string 'guess' or a float value
        fix_vars: list[dict[str, float | str]]
            List of fix dicts, with keys as PARNAMES of each LogTauTModel
            and values as either the string 'guess' or a float value
        logmodels: list[LogTauTModel]
            List of uninstantiated LogTauTModel objects

        Returns
        -------
        list[LogTauTModel]
            Instantiated LogTauTModels with fit and fix dicts applied
        '''

        marked = [False] * len(fit_vars)

        instantiated_models = []

        for logmodel in logmodels:
            for it, (fitvar_set, fix_var_set) in enumerate(zip(fit_vars, fix_vars)): # noqa
                if marked[it]:
                    continue
                elif all([k in logmodel.PARNAMES for k in fitvar_set.keys()]): # noqa
                    if all([k in logmodel.PARNAMES for k in fix_var_set.keys()]) or not len(fix_var_set): # noqa
                        instantiated_models.append(
                            logmodel(fitvar_set, fix_var_set)
                        )
                        marked[it] = True

        return instantiated_models

    @classmethod
    def residual_from_float_list(cls, new_vals: npt.ArrayLike,
                                 logmodels: list[LogTauTModel],
                                 temperatures: npt.ArrayLike,
                                 lograte: npt.ArrayLike,
                                 sigma: npt.ArrayLike = []) -> npt.NDArray:
        '''
        Wrapper for `residuals` method, takes new values from fitting routine
        which provides list[float], to construct new fit_vars dict, then
        runs `residuals` method.

        Parameters
        ----------
        new_vals: array_like
            This iteration's fit parameter values provided by least_squares
            this has the same order at fit_vars.keys
        logmodels: list[LogTauTModel]
            Models to use
        temperatures: array_like
            Temperature values (K) at which model function is evaluated
        lograte: array_like
            True (experimental) values of log10(relaxation rate)
        sigma: array_like
            Standard deviation of tau in logspace

        Returns
        -------
        ndarray of floats
            Residuals
        '''

        # Swap fit values for new values from fit routine
        new_fit_vars = []

        it = 0
        for logmodel in logmodels:
            new_dict = {}
            for name in logmodel.fit_vars.keys():
                new_dict[name] = new_vals[it]
                it += 1
            new_fit_vars.append(new_dict)

        residuals = cls.residuals(
            logmodels, new_fit_vars, temperatures, lograte
        )

        if len(sigma):
            residuals /= sigma

        return residuals

    @staticmethod
    def residuals(logmodels: list[LogTauTModel],
                  new_fit_vars: list[dict[str, float]],
                  temperatures: npt.ArrayLike,
                  true_lograte: npt.ArrayLike) -> npt.NDArray:
        '''
        Calculates difference between experimental log10(tau^-1)
        and log10(tau^-1) obtained from the sum of the provided logmodels
        using the provided fit variable values at provided temperatures

        Parameters
        ----------
        logmodels: list[LogTauTModel]
            LogTauTModels which will be evaluated
        new_fit_vars: list[dict[str, float]]
            fit dicts for each LogTauTModel, must have same order as logmodel
            if no vars to fit for that model, then empty dict is given
        temperatures: array_like
            Experimental temperatures (K)
        true_lograte: array_like
            Experimental Log10(rate)s

        Returns
        -------
        ndarray of floats
            Log10(rate)_trial - Log10(rate)_exp for each temperature
        '''

        # Calculate model log10(relaxation rate) using parameters
        # as sum of contributions from each process
        trial_lograte = np.zeros(len(temperatures))

        for logmodel, fit_vars in zip(logmodels, new_fit_vars):
            all_vars = {**logmodel.fix_vars, **fit_vars}
            trial_lograte += 10**logmodel.model(all_vars, temperatures)

        # sum in linear space, then take log
        trial_lograte = np.log10(trial_lograte)

        residuals = trial_lograte - true_lograte

        return residuals

    def fit_to(self, dataset: TauTDataset, verbose: bool = True) -> None:
        '''
        Fits model to Dataset

        Parameters
        ----------
        dataset: TauTDataset
            Dataset to which a model of rate vs temperature will be fitted
        verbose: bool, default True
            If True, prints information to terminal

        Returns
        -------
        None
        '''

        # Initial guess is a list of fitvars values
        guess = [
            value for logmodel in self.logmodels
            for value in logmodel.fit_vars.values()
        ]

        bounds = np.array([
            logmodel.BOUNDS[name] for logmodel in self.logmodels
            for name in logmodel.fit_vars.keys()
        ]).T

        curr_fit = least_squares(
            self.residual_from_float_list,
            args=[
                self.logmodels,
                dataset.temperatures,
                np.log10(dataset.rates),
                dataset.lograte_pm
            ],
            x0=guess,
            bounds=bounds,
            jac='3-point'
        )

        if curr_fit.status == 0:
            if verbose:
                ut.cprint(
                    '\n Fit failed - Too many iterations',
                    'black_yellowbg'
                )

            n_fitted_pars = np.sum(
                [len(logmodel.fit_vars.keys()) for logmodel in self.logmodels]
            )

            stdev = [np.nan] * n_fitted_pars
            self.fit_status = False
        else:

            stdev, no_stdev = stats.svd_stdev(curr_fit)

            self.fit_status = True

        # Add parameters, status and stdev to each LogTauTModel
        it = 0
        for logmodel in self.logmodels:

            # Name of fitted variables in this logmodel
            fit_var_names = logmodel.fit_vars.keys()
            # Number of parameters for this logmodel
            n_pars = len(fit_var_names)

            # Set each standard deviation
            _stdev = stdev[it: it + n_pars]
            logmodel.fit_stdev = {
                label: val
                for label, val in zip(
                    fit_var_names, _stdev
                )
            }

            # Report singular values=0 of Jacobian
            # and indicate that std_dev cannot be calculated
            sings = no_stdev[it: it + n_pars]
            for par, si in zip(fit_var_names, sings):
                if verbose and not si:
                    ut.cprint(
                        f'Warning: Jacobian is degenerate for {par}, standard deviation cannot be found, and is set to zero\n', # noqa
                        'black_yellowbg'
                    )

            # Set final fitted values
            _vals = curr_fit.x[it: it + n_pars]
            logmodel.final_var_values = {
                name: value
                for name, value in zip(fit_var_names, _vals)
            }
            # and fixed values
            for key, val in logmodel.fix_vars.items():
                logmodel.final_var_values[key] = val

            it += n_pars

        return


class FitWindow(QtWidgets.QMainWindow):
    '''
    Interactive Fit Window for rate vs temperature/field data fitting
    '''

    def __init__(self, dataset: TauTDataset | TauHDataset, usel: object,
                 supported_models: list[LogTauTModel | LogTauHModel],
                 widget_defaults: dict[str, dict[str, float]] = gui.widget_defaults, # noqa
                 *args, **kwargs):

        super(FitWindow, self).__init__(*args, **kwargs)

        # Add shortcut to press q to quit
        self.exit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('q'), self)
        self.exit_shortcut.activated.connect(
            lambda: self.close()
        )

        self.setWindowTitle('Interactive Relaxation Profile')

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setStyleSheet(
            '''
            QMainWindow {
                background-color: white
            }

            QCheckBox {
                spacing: 5px;
                font-size:15px;
            }
            QSlider::groove:horizontal {
            border: 1px solid #bbb;
            background: white;
            height: 10px;
            border-radius: 4px;
            }

            QSlider::sub-page:horizontal {
            background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
                stop: 0 #66e, stop: 1 #bbf);
            background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
                stop: 0 #bbf, stop: 1 #55f);
            border: 1px solid #777;
            height: 10px;
            border-radius: 4px;
            }

            QSlider::add-page:horizontal {
            background: #fff;
            border: 1px solid #777;
            height: 10px;
            border-radius: 4px;
            }

            QSlider::handle:horizontal {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #eee, stop:1 #ccc);
            border: 1px solid #777;
            width: 13px;
            margin-top: -2px;
            margin-bottom: -2px;
            border-radius: 4px;
            }

            QSlider::handle:horizontal:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #fff, stop:1 #ddd);
            border: 1px solid #444;
            border-radius: 4px;
            }

            QSlider::sub-page:horizontal:disabled {
            background: #bbb;
            border-color: #999;
            }

            QSlider::add-page:horizontal:disabled {
            background: #eee;
            border-color: #999;
            }

            QSlider::handle:horizontal:disabled {
            background: #eee;
            border: 1px solid #aaa;
            border-radius: 4px;
            }
            '''
        )

        # Set default min, max, init, and step values of sliders and text boxes
        self.defaults = widget_defaults

        # Dictionary for tickbox widgets
        self.tickdict = {
            model.NAME.lower(): None
            for model in supported_models
        }

        # Dictionary for parameter slider, entry, and fitfix widgets
        self.widgetdict = {
            model.NAME.lower(): {
                parname: {
                    'slider': None,
                    'ff_toggle': None,
                    'entry': None
                }
                for parname in model.PARNAMES
            }
            for model in supported_models
        }

        # Minimum Window size
        self.setMinimumSize(QtCore.QSize(1250, 700))

        # Make widgets for entire window
        self.widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.widget)
        bot_row_widget = QtWidgets.QWidget(self.widget)
        top_row_widget = QtWidgets.QWidget(self.widget)
        rhs_col_widget = QtWidgets.QWidget(top_row_widget)

        rhs_col_scroll = QtWidgets.QScrollArea(rhs_col_widget)
        rhs_col_scroll.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOn
        )
        rhs_col_scroll.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff
        )
        rhs_col_scroll.setWidgetResizable(True)

        scroll_container = QtWidgets.QWidget(rhs_col_scroll)
        rhs_col_scroll.setWidget(scroll_container)

        lhs_col_widget = QtWidgets.QWidget(top_row_widget)

        # LHS column - plot only
        lhs_col_layout = QtWidgets.QVBoxLayout(lhs_col_widget)

        # make pgfplots plot widget
        self.plot_widget = pg.PlotWidget(
            parent=lhs_col_widget
        )
        # Add plot to left column
        lhs_col_layout.addWidget(self.plot_widget)

        # Set loglog axes
        self.plot_widget.setLogMode(True, True)

        # Set white plot background
        self.plot_widget.setBackground('w')

        # Select either field or temperature as x data based on dataset type
        # and set x label of plot
        if isinstance(dataset, TauHDataset):
            self.exp_xvals = copy.copy(np.asarray(dataset.fields))
            # Shift all data to become defined in log10 space
            # This shift must only be applied when plotting, not
            # when calculating the values of the function
            if any(val < np.finfo(float).eps for val in self.exp_xvals):
                self.logshift = 1.
            else:
                self.logshift = 0.
            self.exp_xvals += self.logshift
            self.plot_widget.setLabel('bottom', 'Field (Oe)')

        elif isinstance(dataset, TauTDataset):
            self.logshift = 0.
            self.exp_xvals = copy.copy(np.asarray(dataset.temperatures))
            self.plot_widget.setLabel('bottom', 'Temperature (K)')
        # Experimental rates
        self.exp_rates = np.asarray(dataset.rates)

        # Experimental data
        self.exp = self.plot_widget.plot(
            np.array(self.exp_xvals),
            np.array(self.exp_rates),
            pen=None,
            symbol='x',
            symbolBrush=(0, 0, 0)
        )

        # Find nice y-axis limits
        y_lower, y_upper = gui.calc_y_rate_lims(
            self.exp_rates,
            np.array(dataset.rate_pm)
        )

        # Clip them at sensible values
        [y_lower, y_upper] = np.clip([y_lower, y_upper], 1E-10, 1E10)

        # and set values
        self.plot_widget.setYRange(
            np.log10(y_lower),
            np.log10(y_upper),
            padding=0
        )

        # Add experimental errorbars
        if len(dataset.lograte_pm):
            err = pg.ErrorBarItem(
                x=np.log10(self.exp_xvals),
                y=np.log10(self.exp_rates),
                top=dataset.lograte_pm,
                bottom=dataset.lograte_pm,
                beam=0.005
            )
            self.plot_widget.addItem(err)

        # Axis labels
        self.plot_widget.setLabel('left', 'Rate (s<sup>-1</sup>)')

        # Set dictionary of True (fit) and False (fix) for each
        # parameter of all available models
        usel.fit = {
            parname: True
            for model in supported_models
            for parname in model.PARNAMES
        }

        # Set user selection object and supported models
        self.usel = usel
        self.supported_models = supported_models

        # Calculate each model function and plot
        # Note if shift is applied then these values
        # must be the true x variables as they will be used to compute
        # the model values
        self.x_grid = np.linspace(
            np.min(self.exp_xvals - self.logshift),
            np.max(self.exp_xvals - self.logshift),
            1000
        )

        # Sum of all models, set to zero initially
        total_rates = np.zeros(np.shape(self.x_grid))

        # Dictionary of plots
        # keys are model.NAME.lower(), values are plot_widget.plot
        self.model_plots = {}

        # List of nice colors
        colors = mcolors.TABLEAU_COLORS.values()

        # Loop over all possible models, calculate model values
        # at range of temperatures and plot
        # then add to array of total rates
        for color, model in zip(colors, supported_models):

            # Get initial values
            initials = model.set_initial_vals(
                {
                    par: self.defaults[model.NAME][par]['valinit']
                    for par in model.PARNAMES
                }
            )
            # Calculate rates
            rates = 10**(model.model(initials, self.x_grid))
            # and add to total of all models
            total_rates += rates
            # Plot this model
            _plot = self.plot_widget.plot(
                self.x_grid + self.logshift,
                rates,
                pen={'width': 2.5, 'color': color, 'style': QtCore.Qt.DashLine}
            )
            # and store in dict of all plots
            self.model_plots[model.NAME.lower()] = _plot
            # Remove from actual plot widget
            # since no models are visible initially
            # Plots are re-added with model checkboxes
            self.plot_widget.removeItem(_plot)

        # Calculate initial value of on-screen residual
        self.residual_value = 0.

        # Plot sum of all models
        self.tot = self.plot_widget.plot(
            self.x_grid + self.logshift,
            total_rates,
            pen={'width': 2.5, 'color': 'red'}
        )
        self.plot_widget.removeItem(self.tot)

        # Storage object for final parameter values
        # Set all initial values defaults
        self.parstore = type(
            'obj',
            (object,),
            {
                par: self.defaults[model.NAME][par]['valinit']
                for model in supported_models
                for par in model.PARNAMES
            }
        )

        # Convert log temperature ticks to linear
        ax = self.plot_widget.getAxis('bottom')
        gui.convert_log_ticks_to_lin(
            ax, np.log10(self.exp_xvals), shift=self.logshift
        )

        # RHS column of window
        # This contains each model and its associated parameters
        # Each parameter is controlled by a
        # sliders, Text entry, and a fit/fix toggle
        container_layout = QtWidgets.QVBoxLayout(scroll_container)

        # List of number key shortcuts to toggle models
        self.on_off_shortcut = []

        # For each model, make a box to contain all parameters
        # and populate with parameters

        for mit, model in enumerate(supported_models):
            model_widget = self.make_modelbox(
                model,
                scroll_container,
                mit + 1
            )

            # Add this model to the right hand side of the window
            container_layout.addWidget(model_widget, len(model.PARNAMES))

        # Disable every slider, entry, and fit/fix by default
        # This is toggled by the model checkboxes
        for model in supported_models:
            modelname = model.NAME.lower()
            for parname in model.PARNAMES:
                self.widgetdict[modelname][parname]['slider'].setEnabled(False)
                self.widgetdict[modelname][parname]['entry'].setEnabled(False)
                self.widgetdict[modelname][parname]['ff_toggle'].setEnabled(
                    False
                )

        container_layout.setAlignment(QtCore.Qt.AlignVCenter)
        scroll_container.setSizePolicy(
            QtWidgets.QSizePolicy.Maximum,
            QtWidgets.QSizePolicy.Maximum
        )
        rhs_col_scroll.setMinimumHeight(575)

        # Top row
        # LHS plot, RHS Sliders, text, labels
        top_row_layout = QtWidgets.QHBoxLayout(top_row_widget)
        top_row_layout.addWidget(lhs_col_widget, 3)
        top_row_layout.addWidget(rhs_col_widget, 2)

        # Bottom row

        # Residual read-out widget
        self.residual_widget = QtWidgets.QLabel(
            parent=bot_row_widget,
            text=f'Residual = {self.residual_value:.5f}'
        )

        # Buttons for reset and fit
        self.fit_btn_widget = QtWidgets.QPushButton(
            parent=bot_row_widget,
            text='Fit'
        )
        self.fit_btn_widget.setStyleSheet('font-weight: bold;')

        self.fit_btn_widget.setEnabled(False)
        self.fit_btn_widget.clicked.connect(self.fit)
        self.fit_btn_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        reset_btn_widget = QtWidgets.QPushButton(
            parent=bot_row_widget,
            text='Reset',
        )
        reset_btn_widget.setStyleSheet('font-weight: bold;')
        reset_btn_widget.clicked.connect(self.reset)
        reset_btn_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )

        # Modify fit and reset button text colors to look good even
        # in MacOS darkmode.
        palette = QtGui.QPalette(self.fit_btn_widget.palette())
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('#0db273'))
        self.fit_btn_widget.setPalette(palette)
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor('#4b6aad'))
        reset_btn_widget.setPalette(palette)

        # Keyboard shortcut, press f to fit if fit button not greyed out
        self.fit_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('f'), self)
        self.fit_shortcut.activated.connect(
            lambda: self.keyboard_fit_callback()
        )

        bot_row_layout = QtWidgets.QHBoxLayout(bot_row_widget)
        bot_row_layout.addWidget(self.residual_widget)
        bot_row_layout.addWidget(self.fit_btn_widget)
        bot_row_layout.addWidget(reset_btn_widget)

        # Overall app
        # Top and Bottom rows
        full_layout = QtWidgets.QVBoxLayout(self.widget)
        full_layout.addWidget(top_row_widget)
        full_layout.addWidget(bot_row_widget)

        # Set layout
        self.widget.setLayout(full_layout)
        self.widget.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        return

    def keyboard_fit_callback(self):
        '''
        Callback for pressing 'f' key. Runs fit button if not greyed out
        '''

        # Check fit button is not greyed out
        if self.fit_btn_widget.isEnabled():
            # Run fit code, this closes app
            self.fit()

        return

    def reset(self):
        '''
        Callback for Reset button.
        Returns window back to original layout/selections
        '''

        # For each model, remove plot, and reset parameter values
        for model in self.supported_models:
            modelname = model.NAME.lower()

            # Disable all models
            self.usel.models[modelname] = False
            # and untick checkboxes
            self.tickdict[modelname].setCheckState(QtCore.Qt.CheckState(False))

            # Remove corresponding plot
            _plot = self.model_plots[modelname]
            self.plot_widget.removeItem(_plot)

            # Reset each parameter slider, entry, and fitfix
            # back to original value
            for parname in model.PARNAMES:
                setattr(
                    self.parstore,
                    parname,
                    self.defaults[model.NAME][parname]['valinit']
                )
                self.widgetdict[modelname][parname]['slider'].setValue(
                    int(self.defaults[model.NAME][parname]['valinit'])
                )
                self.widgetdict[modelname][parname]['entry'].setValue(
                    self.defaults[model.NAME][parname]['valinit']
                )
                self.widgetdict[modelname][parname]['ff_toggle'].setText(
                    'Free'
                )

        # Remove total model plot
        self.plot_widget.removeItem(self.tot)

        return

    def fit(self):
        '''
        Callback for Fit button.
        Collects variable values of each model and assembles into fit/fix
        dictionaries, then closes the window.
        '''

        lname_to_model = {
            model.NAME.lower(): model
            for model in self.supported_models
        }

        # Collect variables of each model, if that model is enabled
        # and assign to fit or fix
        for modelname, enabled in self.usel.models.items():
            _fit_vars = dict()
            _fix_vars = dict()
            if enabled:
                model = lname_to_model[modelname]
                for name in model.PARNAMES:
                    if self.usel.fit[name]:
                        _fit_vars[name] = getattr(self.parstore, name)
                    else:
                        _fix_vars[name] = getattr(self.parstore, name)

                self.usel.fit_vars.append(_fit_vars)
                self.usel.fix_vars.append(_fix_vars)

        # Set 'has program been exited' flag to false
        self.usel.exited = False

        # Close the window
        self.close()
        return

    def update_modelplot(self, value: float, parname: str,
                         model: LogTauTModel | LogTauHModel):
        '''
        Updates model plots using new parameter values

        Parameters
        ----------
        value: float
            New value of parameters
        parname: str
            Name of parameter (from model.PARNAMES)
        model: LogTauTModel | LogTauHModel
            Model to which this parameter belongs

        Returns
        -------
        None
        '''

        # Set new parameter value
        setattr(self.parstore, parname, float(value))
        parameters = model.set_initial_vals(
            {
                parname: getattr(self.parstore, parname)
                for parname in model.PARNAMES
            }
        )

        # Recalculate rates for this model
        new_rates = 10**model.model(parameters, self.x_grid)

        # and update model plot data
        _plot = self.model_plots[model.NAME.lower()]
        _plot.setData(self.x_grid + self.logshift, new_rates)

        # Update total plot (sum of all models)
        # Sum ydata of each selected model
        total_rates = np.zeros(self.x_grid.shape)

        # and add to total of all models
        total_rates += np.sum(
            [
                _plot.yData
                for name, _plot in self.model_plots.items()
                if self.usel.models[name]
            ],
            axis=0
        )
        self.tot.setData(self.x_grid + self.logshift, total_rates)

        # Update residual value
        self.residual_value = self.calculate_residual_value()
        self.residual_widget.setText(f'Residual = {self.residual_value:.5f}')

        return

    def calculate_residual_value(self) -> float:
        '''
        Calculates value for on-screen residual using current selected models
        and their parameter values

        Returns
        -------
        float
            Residual sum of squares.
            Defined as sum((log10(exp) - log10(calc))**2)
        '''

        # Calculate rates at experimental value
        _lograte_at_exp = np.zeros(len(self.exp_xvals))

        n_parameters = 0

        # Loop over all available models
        for model in self.supported_models:
            # Include only models which have been selected
            if self.usel.models[model.NAME.lower()]:
                parameters = model.set_initial_vals(
                    {
                        parname: getattr(self.parstore, parname)
                        for parname in model.PARNAMES
                    }
                )
                _lograte_at_exp += 10**model.model(parameters, self.exp_xvals)
                n_parameters += len(parameters)

        if n_parameters == 0:
            rss = 0.
        else:
            rss = np.sum(
                (
                    np.log10(self.exp_rates) - np.log10(_lograte_at_exp)
                )**2
            )

        return rss

    def toggle_plot(self, val: int,
                    model: LogTauTModel | LogTauHModel) -> None:
        '''
        Callback for toggling model checkboxes

        Calculates model data, adds/deletes line from plot, updates total model
        plot, and recalculates residual value

        Parameters
        ----------
        val: int {0, 2}
            Value returned by tickbox widget, specifies off / on
        model: LogTauTModel | LogTauHModel
            Model which is being toggled

        Returns
        -------
        None
        '''

        # Convert val (0 or 2) to bool
        val = bool(val / 2)

        modelname = model.NAME.lower()

        # Update list of models
        self.usel.models[modelname] = val
        # Update model values and plot data for each model, and for total
        for parname in model.PARNAMES:
            self.update_modelplot(
                getattr(self.parstore, parname),
                parname,
                model
            )

        # Select model plot to toggle
        _plot = self.model_plots[modelname]

        # Add back in plot
        if val:
            self.plot_widget.removeItem(_plot)
            self.plot_widget.addItem(_plot)
        else:
            self.plot_widget.removeItem(_plot)

        # Enable total plot if > 1 model
        # and enable fit button if > 0 models
        n_models = np.sum([val for val in self.usel.models.values()])
        if n_models == 0:
            self.fit_btn_widget.setEnabled(False)
        elif n_models == 1:
            self.fit_btn_widget.setEnabled(True)
            self.plot_widget.removeItem(self.tot)
        else:
            self.fit_btn_widget.setEnabled(True)
            self.plot_widget.removeItem(self.tot)
            self.plot_widget.addItem(self.tot)

        # Enable/Disable slider, checkbox, and fitfix
        for parname in model.PARNAMES:
            self.widgetdict[modelname][parname]['slider'].setEnabled(val)
            self.widgetdict[modelname][parname]['entry'].setEnabled(val)
            self.widgetdict[modelname][parname]['ff_toggle'].setEnabled(val)

        # Update residual value
        self.residual_value = self.calculate_residual_value()
        self.residual_widget.setText(f'Residual = {self.residual_value:.5f}')

        return

    def make_modelbox(self, model: LogTauTModel | LogTauHModel,
                      parent: QtWidgets.QWidget,
                      num_key: int) -> QtWidgets.QWidget:
        '''
        Creates widget for a given model, containing a checkbox to toggle
        the model, and a row of interactive widgets for each parameter of the
        model.

        Parameters
        ----------
        model: LogTauTModel | LogTauHModel
            Model for which a widget is made
        parent: QtWidgets.QWidget
            Parent widget for this model widget
        num_key: int
            Integer specifying which num_key will toggle this model on and off

        Returns
        -------
        QtWidgets.QWidget
            Widget for this model
        '''

        # Widget for this model
        model_widget = QtWidgets.QWidget(parent=parent)
        model_layout = QtWidgets.QHBoxLayout(model_widget)

        # Create tickbox to toggle this widget
        tickbox_widget = QtWidgets.QCheckBox(
            parent=model_widget,
            text=model.NAME.replace('Brons-Van-Vleck', 'BVV')
        )

        # Add tickbox to this model
        model_layout.addWidget(tickbox_widget)

        # Add to dictionary of all tickboxes, indexed by model.NAME.lower()
        self.tickdict[model.NAME.lower()] = tickbox_widget

        # When toggled, plot this model
        tickbox_widget.stateChanged.connect(
            lambda val: self.toggle_plot(val, model)
        )

        # Add ability to toggle model using number key
        on_off_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence('{:d}'.format(num_key)),
            self
        )
        on_off_shortcut.activated.connect(
            lambda: tickbox_widget.toggle()
        )
        self.on_off_shortcut.append(on_off_shortcut)

        # Create container widget for all parameter rows
        rhs_widget = QtWidgets.QWidget(parent=model_widget)
        rhs_layout = QtWidgets.QVBoxLayout(rhs_widget)

        # Make slider, textbox, and fit/fix toggle for each
        # parameter of the current model
        for parname in model.PARNAMES:

            # Default parameter values
            _defaults = self.defaults[model.NAME][parname]

            # Name and Units as string
            _nu_string = '{} ({})'.format(
                model.VARNAMES_HTML[parname],
                model.UNITS_HTML[parname]
            ).replace('()', '')

            # Callback for interaction with slider, textbox...
            cb = partial(
                self.update_modelplot,
                model=model,
                parname=parname
            )

            # Make row of widgets for this parameter
            parbox_widget, parbox_layout = self.make_parbox(
                cb, parname, _nu_string, _defaults, model_widget,
                model.NAME.lower()
            )

            # and add to the model's box of parameter
            rhs_layout.addWidget(parbox_widget)

        # Set expansion behaviour and centering of widgets
        rhs_layout.setAlignment(QtCore.Qt.AlignVCenter)
        rhs_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        tickbox_widget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )

        rhs_layout.setSpacing(0)
        rhs_layout.addStretch(4)

        # Add parameter rows to this model
        model_layout.addWidget(rhs_widget)

        # and set alignment of the model
        model_layout.setAlignment(QtCore.Qt.AlignTop)

        return model_widget

    def not_ify(self, parname: str):
        '''
        Switches fit dictionary entry True <--> False
        for the provided parname
        '''
        self.usel.fit[parname] = not self.usel.fit[parname]

    def make_parbox(self, cb: partial, parname: str, _nu_string: str,
                    defaults: dict[str, float], op_par: QtWidgets.QWidget,
                    modelname: str):
        '''
        Creates set of widgets for a single parameter of a model.\n
        Contains 2 rows, upper is label and units as string, and lower
        is slider, textentry (doublespinbox), and fit/fix toggle button.

        Parameters
        ----------
        cb: functools.partial
            Partial-ly instantiated callback which will be fired when
            widgets of this parameter are interacted with.
        parname: str
            String name of parameter used as key in
            self.widgetdict[widgetdict]
        _nu_string: str
            String name of parameter and units used as title of this parameter
        defaults: dict[str, float]
            Default values of this parameter, keys are min, max, valinit, step
        op_par: QtWidgets.QWidget
            Parent widget
        modelname: str
            String name of model used as key in self.widgetdict
        '''

        # Widget for this parameter's row of widgets
        one_param_widget = QtWidgets.QWidget(parent=op_par)
        one_param_layout = QtWidgets.QVBoxLayout(one_param_widget)

        # For label and units
        top_boxwidget = QtWidgets.QWidget(parent=one_param_widget)
        top_boxlayout = QtWidgets.QHBoxLayout(top_boxwidget)

        # For interactive widgets
        bot_boxwidget = QtWidgets.QWidget(parent=one_param_widget)
        bot_boxlayout = QtWidgets.QHBoxLayout(bot_boxwidget)

        # Add label and units
        name_units = QtWidgets.QLabel(_nu_string)
        name_units.setFont(QtGui.QFont('Arial', 11))

        name_units.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )

        top_boxlayout.addWidget(name_units)

        # Create slider
        slider = QtWidgets.QSlider(
            orientation=QtCore.Qt.Horizontal,
            parent=bot_boxwidget
        )

        # Scale all slider numbers by this to make into floats
        slider_scale = 1E5

        slider.setMinimum(int(defaults['min'] * slider_scale))
        slider.setMaximum(int(defaults['max'] * slider_scale))
        slider.setValue(int(defaults['valinit'] * slider_scale))
        slider.setSingleStep(int(defaults['step'] * slider_scale))

        self.widgetdict[modelname.lower()][parname]['slider'] = slider

        # Add slider to layout
        bot_boxlayout.addWidget(slider)

        # Create text entry (DoubleSpinBox)
        entry = QtWidgets.QDoubleSpinBox(parent=bot_boxwidget)
        entry.setDecimals(int(defaults['decimals']))
        entry.setButtonSymbols(QtWidgets.QDoubleSpinBox.NoButtons)
        entry.setKeyboardTracking(False)
        entry.setMinimum(defaults['min'])
        entry.setMaximum(defaults['max'])
        entry.setValue(defaults['valinit'])
        entry.setSingleStep(defaults['step'])

        self.widgetdict[modelname.lower()][parname]['entry'] = entry

        # Add doublespinbox to layout
        bot_boxlayout.addWidget(entry)

        # Create fit/fix toggle button
        ff_toggle = QtWidgets.QPushButton('Free', parent=bot_boxwidget)

        self.widgetdict[modelname.lower()][parname]['ff_toggle'] = ff_toggle

        ffsw = {
            'Free': 'Fixed',
            'Fixed': 'Free',
        }

        # Callback for text
        ff_toggle.clicked.connect(
            lambda _: ff_toggle.setText(ffsw[ff_toggle.text()])
        )

        # Callback for fit/fix of this parameter
        ff_toggle.clicked.connect(
            lambda _: self.not_ify(parname)
        )

        # Connect fit/fix to slider and textentry
        slider.valueChanged.connect(lambda val: cb(val * slider_scale**-1))
        slider.valueChanged.connect(
            lambda val: entry.setValue(val * slider_scale**-1)
        )
        entry.valueChanged.connect(cb)
        entry.valueChanged.connect(
            lambda val: slider.setValue(int(val * slider_scale))
        )

        # Add fit/fix to layout
        bot_boxlayout.addWidget(ff_toggle)

        top_boxwidget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        bot_boxwidget.setSizePolicy(
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed
        )
        top_boxlayout.setAlignment(QtCore.Qt.AlignHCenter)

        one_param_layout.addWidget(top_boxwidget)
        one_param_layout.addWidget(bot_boxwidget)

        one_param_layout.setContentsMargins(0, 0, 0, 0)
        one_param_layout.setSpacing(2)
        one_param_layout.addStretch(1)
        one_param_layout.setAlignment(QtCore.Qt.AlignVCenter)

        return one_param_widget, one_param_layout


def interactive_fitting(dataset: TauTDataset | TauHDataset, app,
                        model_opt: str | list[LogTauTModel | LogTauHModel] = 'from_dataset') -> tuple[list[LogTauTModel | LogTauHModel], list[dict[str, float]], list[dict[str, float]], bool]: # noqa
    '''
    Creates qt window for user to interactively fit models to relaxation
    data

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    app: QtWidgets.QApplication
        Application used by current program
        Create with `app=QtWidgets.QApplication([])`
    model_opt: str | list[LogTauTModel | LogTauHModel] default 'from_dataset' 
        List of models to offer to user, if 'from_dataset' will generate
        a list based on the dataset provided

    Returns
    -------
    list[LogTauTModel | LogTauHModel]
        Models selected by user
    list[dict[str, float]]
        fit_vars dicts, one per model
    list[dict[str, float]]
        fix_vars dicts, one per model
    bool
        True if user has exited window instead of fitting
        else False
    ''' # noqa

    if model_opt == 'from_dataset':
        if isinstance(dataset, TauTDataset):
            model_opt = [
                LogOrbachModel,
                LogRamanModel,
                LogQTMModel,
                LogDirectModel
            ]
        elif isinstance(dataset, TauHDataset):
            model_opt = [
                LogFDQTMModel,
                LogRamanIIModel,
                LogBVVRamanIIModel,
                LogConstantModel,
                LogBVVConstantModel,
            ]

    usel = type('obj', (object,), {
        'models': {
            model.NAME.lower(): False
            for model in model_opt
        },
        'fit_vars': [],
        'fix_vars': [],
        'fix': [],
        'exited': True
    })

    param_window = FitWindow(
        dataset,
        usel,
        model_opt,
        gui.widget_defaults
    )
    param_window.show()

    app.exec()

    name_to_model = {
        model.NAME.lower(): model
        for model in model_opt
    }

    r_models = [
        name_to_model[name]
        for name in usel.models
    ]

    return r_models, usel.fit_vars, usel.fix_vars, usel.exited


def plot_fitted_times(dataset: TauTDataset | TauHDataset,
                      model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                      show: bool = True, save: bool = False,
                      save_name: str = 'fitted_rates.png',
                      verbose: bool = True,
                      show_params: bool = True) -> tuple[plt.Figure, plt.Axes]:
    '''
    Plots experimental and fitted (model) relaxation rate as\n
    ln(tau) vs 1/xvar where xvar is T or H.

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model (fitted) to plot
    show: bool, default True
        If True, show plot on screen
    save: bool, default False
        If True, save plot to file `save_name`
    save_name: str, default = 'fitted_rates.png'
        If save is True, will save plot to this filename
    verbose: bool, default True
        If True, plot file location is written to terminal
    show_params: bool, default True
        If True, shows fitted parameters on plot

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    plt.Axes
        Matplotlib axis object
    '''

    if show_params:
        figsize = (6, 6)
    else:
        figsize = (6, 5.5)

    # Create figure and axes
    fig, ax = plt.subplots(
        1,
        1,
        figsize=figsize,
        num='Fitted relaxation profile'
    )

    _plot_fitted_times(dataset, model, fig, ax, show_params=show_params)

    fig.tight_layout()

    if show:
        plt.show()

    if save:
        fig.savefig(save_name, dpi=500)
        if verbose:
            if isinstance(dataset, (TauTDataset)):
                _xvar = 'T'
            elif isinstance(dataset, (TauHDataset)):
                _xvar = 'H'
            ut.cprint(
                f'\n Fitted ln(τ) vs 1/{_xvar} plot saved to \n {save_name}\n', # noqa
                'cyan'
            )

    return fig, ax


def plot_times(dataset: TauTDataset | TauHDataset, show: bool = True,
               save: bool = False, save_name: str = 'relaxation_times.png',
               verbose: bool = True) -> tuple[plt.Figure, plt.Axes]:
    '''
    Plots experimental relaxation time as\n
    ln(tau) vs 1/xvar where xvar is T or H.

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    show: bool, default True
        If True, show plot on screen
    save: bool, default False
        If True, save plot to file `save_name`
    save_name: str, default 'relaxation_times.png'
        If save is True, will save plot to this filename
    verbose: bool, default True
        If True, plot file location is written to terminal

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    plt.Axes
        Matplotlib axis object
    '''

    # Create figure and axes
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(6, 5.5),
        num='Fitted relaxation profile'
    )

    if isinstance(dataset, TauHDataset):
        x_vals = copy.copy(dataset.fields)
        ax.set_xlabel(r'1/H $\left(\mathregular{Oe}^\mathregular{-1}\right)$')
    elif isinstance(dataset, TauTDataset):
        x_vals = copy.copy(dataset.temperatures)
        ax.set_xlabel(r'1/T $\left(\mathregular{K}^\mathregular{-1}\right)$')

    # Add uncertainties as errorbars
    if len(dataset.rate_pm):

        # Calculate time errorbars
        times = 1. / dataset.rates
        min_time = 1. / (dataset.rates + dataset.rate_pm[1, :])
        max_time = 1. / (dataset.rates - dataset.rate_pm[0, :])

        ln_min_time = np.log(min_time)
        ln_max_time = np.log(max_time)

        ln_time_plus = ln_max_time - np.log(times)
        ln_time_minus = np.log(times) - ln_min_time

        lntime_mp = np.array([ln_time_minus, ln_time_plus])

        ax.errorbar(
            1. / x_vals,
            np.log(times),
            yerr=lntime_mp,
            marker='o',
            lw=0,
            elinewidth=1.5,
            fillstyle='none',
            color='black'
        )
    else:
        ax.plot(
            1. / x_vals,
            np.log(1. / dataset.rates),
            marker='o',
            lw=0,
            fillstyle='none',
            color='black'
        )

    # Enable minor ticks
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.set_minor_locator(AutoMinorLocator())

    ax.set_ylabel(r'$\ln\left[\tau\right]$ $\left(\ln\left[\mathregular{s}^\mathregular{-1}\right]\right)$') # noqa

    fig.tight_layout()

    if show:
        plt.show()

    if save:
        fig.savefig(save_name, dpi=500)
        if verbose:
            if isinstance(dataset, (TauTDataset)):
                _xvar = 'T'
            elif isinstance(dataset, (TauHDataset)):
                _xvar = 'H'
            ut.cprint(
                f'\n Fitted ln(tau) vs 1/{_xvar} plot saved to \n {save_name}\n', # noqa
                'cyan'
            )

    return fig, ax


def _plot_fitted_times(dataset: TauTDataset | TauHDataset,
                       model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                       fig: plt.Figure, ax: plt.Axes,
                       show_params: bool = True):
    '''
    Plots experimental and fitted (model) relaxation rate as\n
    ln(tau) vs 1/xvar where xvar is T or H.

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model (fitted) to plot
    fig: plt.Figure
        Matplotlib Figure object used for plot
    ax: plt.Axes
        Matplotlib Axis object used for plot
    show_params: bool, default True
        If True, shows fitted parameters on plot

    Returns
    -------
    None
    '''

    if isinstance(dataset, TauHDataset):
        x_vals = copy.copy(dataset.fields)
        ax.set_xlabel(r'1/H $\left(\mathregular{Oe}^\mathregular{-1}\right)$')
        x_type = 'field'
    elif isinstance(dataset, TauTDataset):
        x_vals = copy.copy(dataset.temperatures)
        ax.set_xlabel(r'1/T $\left(\mathregular{K}^\mathregular{-1}\right)$')
        x_type = 'temperature'

    # Add uncertainties as errorbars
    if len(dataset.rate_pm):

        # Calculate time errorbars
        times = 1. / dataset.rates
        min_time = 1. / (dataset.rates + dataset.rate_pm[1, :])
        max_time = 1. / (dataset.rates - dataset.rate_pm[0, :])

        ln_min_time = np.log(min_time)
        ln_max_time = np.log(max_time)

        ln_time_plus = ln_max_time - np.log(times)
        ln_time_minus = np.log(times) - ln_min_time

        lntime_mp = np.array([ln_time_minus, ln_time_plus])

        ax.errorbar(
            1. / x_vals,
            np.log(times),
            yerr=lntime_mp,
            marker='o',
            lw=0,
            elinewidth=1.5,
            fillstyle='none',
            label='Experiment',
            color='black'
        )
    else:
        ax.plot(
            1. / x_vals,
            np.log(1. / dataset.rates),
            marker='o',
            lw=0,
            fillstyle='none',
            label='Experiment',
            color='black'
        )

    x_vars_grid = np.linspace(
        np.min(x_vals),
        np.max(x_vals),
        1000
    )

    if type(model) in [MultiLogTauTModel, MultiLogTauHModel]:
        logmodels = model.logmodels
    else:
        logmodels = [model]

    for logmodel in logmodels:

        if type(logmodel) is LogOrbachModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['u_eff'],
                logmodel.final_var_values['u_eff']
            )
            label_fit += '\n' + r'{} {:04.3e}'.format(
                logmodel.VARNAMES_MM['A'], logmodel.final_var_values['A']
            )
        elif type(logmodel) is LogRamanModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['R'], logmodel.final_var_values['R']
            )
            label_fit += '\n' + r'{} {:04.3e}'.format(
                logmodel.VARNAMES_MM['n'], logmodel.final_var_values['n']
            )
        elif type(logmodel) is LogQTMModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['Q'], logmodel.final_var_values['Q']
            )
        elif type(logmodel) is LogDirectModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['D'], logmodel.final_var_values['D']
            )
        model_rates = 10**logmodel.model(
            logmodel.final_var_values,
            x_vars_grid,
        )

        # Discard model rates slower than threshold,
        # else these dominate the plot
        thresh = 1E-10
        plot_x_vars_grid = x_vars_grid[model_rates > thresh]
        model_rates = model_rates[model_rates > thresh]
        model_lntau = np.log(1. / np.array(model_rates))

        ax.plot(
            1. / np.array(plot_x_vars_grid),
            model_lntau,
            lw=1.5,
            label=logmodel.NAME,
            ls='--'
        )

    if type(model) in [MultiLogTauTModel, MultiLogTauHModel] and len(logmodels) > 1: # noqa
        total = np.zeros(len(x_vars_grid))

        for logmodel in logmodels:
            total += 10**logmodel.model(
                logmodel.final_var_values,
                x_vars_grid,
            )

        ax.plot(
            1. / x_vars_grid,
            np.log(1. / total),
            lw=1.5,
            label='Total',
            color='red'
        )

    # Enable minor ticks
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.xaxis.set_minor_locator(AutoMinorLocator())

    expression = ''

    for logmodel in logmodels:
        for it, name in enumerate(logmodel.PARNAMES):
            expression += '{} = {:.3f} '.format(
                logmodel.VARNAMES_MM[name],
                logmodel.final_var_values[name],
            )
            if name in logmodel.fit_vars.keys():
                expression += r'$\pm$ '
                expression += '{:.3f} '.format(logmodel.fit_stdev[name])
            expression += '{}    '.format(logmodel.UNITS_MM[name])
            if it == 1 and len(logmodel.fit_vars.keys()) > 2:
                expression += '\n'
        expression += '\n'

    if show_params:
        ax.text(
            0.0, 1.02, s=expression, fontsize=10, transform=ax.transAxes
        )

    if x_type == 'field':
        ax.legend(
            fontsize='10', numpoints=1, ncol=1, frameon=False
        )
    else:
        ax.legend(
            loc='lower right', fontsize='10', numpoints=1, ncol=1,
            frameon=False
        )

    ax.set_ylabel(r'$\ln\left[\tau\right]$ ($\ln\left[\mathregular{s}^\mathregular{-1}\right]$)') # noqa

    return


def plot_fitted_rates(dataset: TauTDataset | TauHDataset,
                      model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                      show: bool = True, save: bool = False,
                      save_name: str = 'fitted_rates.png',
                      verbose: bool = True,
                      show_params: bool = True) -> tuple[plt.Figure, plt.Axes]:
    '''
    Plots experimental and fitted (model) relaxation rate as\n
    rate vs xvar where xvar is T or H. With log log scale.

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model (fitted) to plot
    show: bool, default True
        If True, show plot on screen
    save: bool, default False
        If True, save plot to file `save_name`
    save_name: str, default = 'fitted_rates.png'
        If save is True, will save plot to this filename
    verbose: bool, default True
        If True, plot file location is written to terminal
    show_params: bool, default True
        If True, shows fitted parameters on plot

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    plt.Axes
        Matplotlib axis object
    '''

    if show_params:
        figsize = (6, 6)
    else:
        figsize = (6, 5.5)

    # Create figure and axes
    fig, ax = plt.subplots(
        1,
        1,
        figsize=figsize,
        num='Fitted relaxation profile'
    )

    _plot_fitted_rates(dataset, model, fig, ax, show_params=show_params)

    fig.tight_layout()

    warnings.simplefilter('ignore', UserWarning)
    if show:
        plt.show()

    if save:
        fig.savefig(save_name, dpi=500)
        if verbose:
            if isinstance(dataset, (TauTDataset)):
                _xvar = 'T'
            elif isinstance(dataset, (TauHDataset)):
                _xvar = 'H'
            ut.cprint(
                f'\n Fitted τ⁻¹ vs {_xvar} plot saved to \n {save_name}\n',
                'cyan'
            )
    warnings.simplefilter('default', UserWarning)

    return fig, ax


def qt_plot_fitted_rates(app: QtWidgets.QApplication,
                         dataset: TauTDataset | TauHDataset,
                         model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                         save: bool = False, show: bool = True,
                         save_name: str = 'fitted_rates.png',
                         verbose: bool = True,
                         show_params: bool = True) -> None:
    '''
    Plots experimental and fitted (model) relaxation rate as\n
    rate vs xvar where xvar is T or H. With log log scale.

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model (fitted) to plot
    show: bool, default True
        If True, show plot on screen
    save: bool, default False
        If True, save plot to file `save_name`
    save_name: str, default 'fitted_rates.png'
        If save is True, will save plot to this filename
    verbose: bool, default True
        If True, plot file location is written to terminal
    show_params: bool, default True
        If True, shows fitted parameters on plot

    Returns
    -------
    None
    '''

    window = gui.MatplotlibWindow()

    window.setWindowTitle('Fitted relaxation profile')

    # Add plot
    _plot_fitted_rates(
        dataset, model, window.sc.fig, window.sc.ax, show_params=show_params
    )

    warnings.simplefilter('ignore', UserWarning)
    # Save plot
    if save:
        window.sc.fig.savefig(save_name, dpi=300)
        if verbose:
            if isinstance(dataset, (TauTDataset)):
                _xvar = 'T'
            elif isinstance(dataset, (TauHDataset)):
                _xvar = 'H'
            ut.cprint(
                f'\n Fitted τ⁻¹ vs {_xvar} plot saved to \n {save_name}\n',
                'cyan'
            )

    if show:
        window.show()
        # Call twice else it wont work!
        window.sc.fig.tight_layout()
        window.sc.fig.tight_layout()
        app.exec_()

    warnings.simplefilter('default', UserWarning)

    return


def _plot_fitted_rates(dataset: TauTDataset | TauHDataset,
                       model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                       fig: plt.Figure, ax: plt.Axes,
                       show_params: bool = True):
    '''
    Plots experimental and fitted (model) relaxation rate as\n
    rate vs xvar where xvar is T or H. With log log scale.

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model (fitted) to plot
    fig: plt.Figure
        Matplotlib Figure object used for plot
    ax: plt.Axes
        Matplotlib Axis object used for plot
    show_params: bool, default True
        If True, shows fitted parameters on plot

    Returns
    -------
    None
    '''

    if isinstance(dataset, TauHDataset):
        x_vals = copy.copy(dataset.fields)
        x_type = 'field'
        ax.set_xlabel(r'Field (Oe)')
    elif isinstance(dataset, TauTDataset):
        x_vals = copy.copy(dataset.temperatures)
        x_type = 'temperature'
        ax.set_xlabel(r'Temperature (K)')

    # Add uncertainties as errorbars
    if len(dataset.rate_pm):
        ax.errorbar(
            x_vals,
            dataset.rates,
            yerr=dataset.rate_pm,
            marker='o',
            lw=0,
            elinewidth=1.5,
            fillstyle='none',
            label='Experiment',
            color='black'
        )
    else:
        ax.plot(
            x_vals,
            dataset.rates,
            marker='o',
            lw=0,
            fillstyle='none',
            label='Experiment',
            color='black'
        )

    x_vars_grid = np.linspace(
        np.min(x_vals),
        np.max(x_vals),
        5000
    )

    if type(model) in [MultiLogTauTModel, MultiLogTauHModel]:
        logmodels = model.logmodels
    else:
        logmodels = [model]

    for logmodel in logmodels:

        if type(logmodel) is LogOrbachModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['u_eff'],
                logmodel.final_var_values['u_eff']
            )
            label_fit += '\n' + r'{} {:04.3e}'.format(
                logmodel.VARNAMES_MM['A'], logmodel.final_var_values['A']
            )
        elif type(logmodel) is LogRamanModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['R'], logmodel.final_var_values['R']
            )
            label_fit += '\n' + r'{} {:04.3e}'.format(
                logmodel.VARNAMES_MM['n'], logmodel.final_var_values['n']
            )
        elif type(logmodel) is LogQTMModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['Q'], logmodel.final_var_values['Q']
            )
        elif type(logmodel) is LogDirectModel:
            label_fit = '\nFit with'
            label_fit += '\n' + r'{} {:6.2f} s'.format(
                logmodel.VARNAMES_MM['D'], logmodel.final_var_values['D']
            )
        model_rates = 10**logmodel.model(
            logmodel.final_var_values,
            x_vars_grid,
        )

        ax.plot(
            np.array(x_vars_grid),
            np.array(model_rates),
            lw=1.5,
            label=logmodel.NAME,
            ls='--'
        )

    if type(model) in [MultiLogTauTModel, MultiLogTauHModel] and len(logmodels) > 1: # noqa
        total = np.zeros(len(x_vars_grid))

        for logmodel in logmodels:
            total += 10**logmodel.model(
                logmodel.final_var_values,
                x_vars_grid,
            )

        ax.plot(
            x_vars_grid,
            total,
            lw=1.5,
            label='Total',
            color='red'
        )

    if x_type == 'field':
        if any(val < np.finfo(float).eps for val in x_vals):
            ax.set_xscale(
                'symlog',
                linthresh=gui.calc_linthresh(x_vals),
                linscale=gui.calc_linscale(x_vals)
            )
        else:
            ax.set_xscale('log')
    else:
        ax.set_xscale('log')
    ax.set_yscale('log')

    gui.format_rate_x_y_axes(
        ax,
        dataset.rates,
        x_vals,
        np.abs(dataset.rate_pm),
        x_type=x_type
    )

    expression = ''

    for logmodel in logmodels:
        for it, name in enumerate(logmodel.PARNAMES):
            expression += '{} = {:.3f} '.format(
                logmodel.VARNAMES_MM[name],
                logmodel.final_var_values[name],
            )
            if name in logmodel.fit_vars.keys():
                expression += r'$\pm$ '
                expression += '{:.3f} '.format(logmodel.fit_stdev[name])
            expression += '{}    '.format(logmodel.UNITS_MM[name])
            if it == 1 and len(logmodel.fit_vars.keys()) > 2:
                expression += '\n'
        expression += '\n'

    if show_params:
        ax.text(
            0.0, 1.02, s=expression, fontsize=10, transform=ax.transAxes
        )

    if x_type == 'field':
        ax.legend(
            fontsize='10', numpoints=1, ncol=1, frameon=False
        )
    else:
        ax.legend(
            loc='upper left', fontsize='10', numpoints=1, ncol=1, frameon=False
        )

    ax.set_ylabel(r'Rate (s$^\mathregular{-1}$)')

    return


def plot_rates(dataset: TauTDataset | TauHDataset, show: bool = True,
               save: bool = False, save_name: str = 'relaxation_rates.png',
               verbose: bool = True) -> tuple[plt.Figure, plt.Axes]:
    '''
    Plots experimental relaxation rate vs field/temperature and
    displays on screen.

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    show: bool, default True
        If True, show plot on screen
    save: bool, default False
        If True, save plot to file `save_name`
    save_name: str, default 'relaxation_rates.png'
        If save is True, will save plot to this filename
    verbose: bool, default True
        If True, plot file location is written to terminal

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    plt.Axes
        Matplotlib axis object
    '''

    # Create figure and axes
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(6, 5.5),
        num='Fitted relaxation profile'
    )

    if isinstance(dataset, TauHDataset):
        x_vals = copy.copy(dataset.fields)
        x_type = 'field'
        ax.set_xlabel(r'Field (Oe)')
    elif isinstance(dataset, TauTDataset):
        x_vals = copy.copy(dataset.temperatures)
        x_type = 'temperature'
        ax.set_xlabel(r'Temperature (K)')

    # Add uncertainties as errorbars
    if len(dataset.rate_pm):
        ax.errorbar(
            x_vals,
            dataset.rates,
            yerr=dataset.rate_pm,
            marker='o',
            lw=0,
            elinewidth=1.5,
            fillstyle='none',
            color='black'
        )
    else:
        ax.plot(
            x_vals,
            dataset.rates,
            marker='o',
            lw=0,
            fillstyle='none',
            color='black'
        )

    if x_type == 'field':
        if any(val < np.finfo(float).eps for val in x_vals):
            ax.set_xscale(
                'symlog',
                linthresh=gui.calc_linthresh(x_vals),
                linscale=gui.calc_linscale(x_vals)
            )
        else:
            ax.set_xscale('log')
    else:
        ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_ylabel(r'Rate (s$^\mathregular{-1}$)')

    if len(dataset.lograte_pm):
        all_data = [
            np.log10(dataset.rates) + dataset.lograte_pm
        ]
        all_data += [
            np.log10(dataset.rates) - dataset.lograte_pm
        ]
    else:
        all_data = [
            np.log10(dataset.rates)
        ]
        all_data += [
            np.log10(dataset.rates)
        ]

    gui.format_rate_x_y_axes(
        ax,
        dataset.rates,
        x_vals,
        np.abs(dataset.rate_pm),
        x_type=x_type
    )

    # Set x tick formatting
    gui.set_rate_xtick_formatting(ax, x_vals, x_type=x_type)

    fig.tight_layout()

    # Suppress symlog warning
    warnings.simplefilter('ignore', UserWarning)

    if save:
        plt.savefig(save_name)
        if verbose:
            ut.cprint(
                f'\n Relaxation plot saved to \n {save_name}\n',
                'cyan'
            )
    if show:
        plt.show()

    # Reenable symlog warning
    warnings.simplefilter('default', UserWarning)

    return fig, ax


def plot_rate_residuals(dataset: TauTDataset,
                        model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                        save: bool = False, show: bool = True,
                        save_name: str = 'model_residual_tau.png',
                        verbose: bool = True) -> tuple[plt.Figure, plt.Axes]:
    '''
    Plots difference of log10(experiment) and log10(model) relaxation rates
    (log10(experiment_rate) - log10(model_rate) vs Temperature or Field)

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model (fitted) to plot
    show: bool, default True
        If True, show plot on screen
    save: bool, default False
        If True, save plot to file `save_name`
    save_name: str, default 'model_residual_tau.png'
        If save is True, will save plot to this filename
    verbose: bool, default True
        If True, plot file location is written to terminal

    Returns
    -------
    plt.Figure
        Matplotlib figure object
    plt.Axes
        Matplotlib axis object
    '''
    # Create figure and axes
    fig, ax = plt.subplots(
        1,
        1,
        figsize=[6, 6],
        num='Residuals'
    )

    _plot_rate_residuals(dataset, model, ax)

    fig.tight_layout()

    warnings.simplefilter('ignore', UserWarning)
    # Save plot
    if save:
        plt.savefig(save_name, dpi=300)
        if verbose:
            ut.cprint(
                f'\n Rate residuals plot saved to \n {save_name}\n',
                'cyan'
            )
    if show:
        plt.show()
    warnings.simplefilter('default', UserWarning)

    return fig, ax


def qt_plot_rate_residuals(app: QtWidgets.QApplication, dataset: TauTDataset,
                           model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                           save: bool = False, show: bool = True,
                           save_name: str = 'model_residual_tau.png',
                           verbose: bool = True) -> None:
    '''
    Plots difference of log10(experiment) and log10(model) relaxation rates
    in a qt window using matplotlib

    Parameters
    ----------
    app: QtWidgets.QApplication
        Application used by current program
        Create with `app=QtWidgets.QApplication([])`
    dataset: TauTDataset | TauHDataset
        Dataset to plot
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model (fitted) to plot
    show: bool, default True
        If True, show plot on screen
    save: bool, default False
        If True, save plot to file `save_name`
    save_name: str, default 'model_residual_tau.png'
        If save is True, will save plot to this filename
    verbose: bool, default True
        If True, plot file location is written to terminal

    Returns
    -------
    None
    '''

    window = gui.MatplotlibWindow()
    window.setWindowTitle('Residuals')

    _plot_rate_residuals(dataset, model, window.sc.ax)

    # Save plot
    if save:
        window.sc.fig.savefig(save_name, dpi=300)
        if verbose:
            ut.cprint(
                f'\n Rate residuals plot saved to \n {save_name}\n',
                'cyan'
            )

    warnings.simplefilter('ignore', UserWarning)
    if show:
        window.show()
        # Call twice else it wont work!
        window.sc.fig.tight_layout()
        window.sc.fig.tight_layout()
        app.exec_()
    warnings.simplefilter('default', UserWarning)

    return


def _plot_rate_residuals(dataset: TauTDataset | TauHDataset,
                         model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                         ax: plt.Axes) -> None:
    '''
    Plots difference of log10(experiment) and log10(model) relaxation rates
    onto a given figure and axis

    Parameters
    ----------
    models: list[LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel]
        Models, one per temperature
    file_name: str
        Name of output file
    ax: plt.Axes
        Matplotlib Axis object used for plot

    Returns
    -------
    None
    ''' # noqa

    if isinstance(dataset, TauHDataset):
        x_type = 'field'
        x_vals = copy.copy(dataset.fields)
        ax.set_xlabel(r'Field (Oe)')
    elif isinstance(dataset, TauTDataset):
        x_type = 'temperature'
        x_vals = copy.copy(dataset.temperatures)
        ax.set_xlabel(r'Temperature (K)')

    # Add additional set of axes to create 'zero' line
    ax2 = ax.twiny()
    ax2.get_yaxis().set_visible(False)
    ax2.set_yticks([])
    ax2.set_xticks([])
    ax2.spines['bottom'].set_position(('zero'))

    if type(model) in [MultiLogTauTModel, MultiLogTauHModel]:
        logmodels = model.logmodels
    else:
        logmodels = [model]

    model_rate = np.zeros(len(x_vals))

    for logmodel in logmodels:
        model_rate += 10**logmodel.model(
            logmodel.final_var_values,
            x_vals,
        )

    model_lograte = np.log10(model_rate)

    # Plot residuals
    if len(dataset.lograte_pm):
        ax.errorbar(
            x_vals,
            np.log10(dataset.rates) - model_lograte,
            yerr=dataset.lograte_pm,
            fmt='b.'
        )
    else:
        ax.plot(
            x_vals,
            np.log10(dataset.rates) - model_lograte,
            color='b',
            marker='o',
            lw=0,
            fillstyle='none',
            label='Experiment'
        )
    # Set log scale on x axis
    if x_type == 'field':
        if any(val < np.finfo(float).eps for val in x_vals):
            ax.set_xscale(
                'symlog',
                linthresh=gui.calc_linthresh(x_vals),
                linscale=gui.calc_linscale(x_vals)
            )
        else:
            ax.set_xscale('log')
    else:
        ax.set_xscale('log')

    # Set formatting for y axis major ticks
    ax.yaxis.set_major_formatter(ScalarFormatter())

    # Add minor ticks to y axis with no labels
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    # Symmetrise y axis limits based on max abs error
    if len(dataset.lograte_pm):
        all_data = [
            np.log10(dataset.rates) - model_lograte + dataset.lograte_pm
        ]
        all_data += [
            np.log10(dataset.rates) - model_lograte - dataset.lograte_pm
        ]
    else:
        all_data = [
            np.log10(dataset.rates) - model_lograte
        ]
        all_data += [
            np.log10(dataset.rates) - model_lograte
        ]

    ticks, maxval = gui.min_max_ticks_with_zero(all_data, 5)
    ax.set_yticks(ticks)

    ax.set_ylim([- maxval * 1.1, + maxval * 1.1])

    # Axis labels
    ax.set_ylabel(
        r'$\log_\mathregular{10}\left[\tau^\mathregular{-1}_{\mathregular{exp}}\right] - \log_\mathregular{10}\left[\tau^\mathregular{-1}_{\mathregular{fit}}\right]$  $\left(\log_\mathregular{10}\left[\mathregular{s}^\mathregular{-1}\right]\right)$' # noqa
    )

    # Set x tick formatting
    gui.set_rate_xtick_formatting(ax, x_vals, x_type=x_type)

    return


def write_model_params(model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                       file_name: str, verbose: bool = True) -> None:
    '''
    Writes fitted and fixed parameters of model(s) to file

    Parameters
    ----------
    models: list[LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel]
        Models, one per temperature
    file_name: str
        Name of output file
    verbose: bool, default True
        If True, output file location is written to terminal

    Returns
    -------
    None
    ''' # noqa

    if type(model) in [MultiLogTauTModel, MultiLogTauHModel]:
        logmodels = model.logmodels
    else:
        logmodels = [model]

    f = open(file_name, 'w', encoding='utf-8')

    # Write each term's name, fit vars, stdev, and fix vars
    for logmodel in logmodels:
        f.write('{}\n'.format(logmodel.NAME))
        if len(logmodel.fit_vars.keys()):
            f.write('Fitted Terms: Value and Standard Deviation:\n')
            for name in logmodel.fit_vars.keys():
                f.write('{:>6} {: 1.8E} {: 1.8E} {}\n'.format(
                    name,
                    logmodel.final_var_values[name],
                    logmodel.fit_stdev[name],
                    logmodel.UNITS[name]
                ))
        if len(logmodel.fix_vars.keys()):
            f.write('Fixed Terms: Values\n')
            for name in logmodel.fix_vars.keys():
                f.write('{:>6} {: 1.8E} {}\n'.format(
                    name,
                    logmodel.final_var_values[name],
                    logmodel.UNITS[name]
                ))
        f.write('\n')

    if verbose:
        ut.cprint(
            '\n Relaxation Model parameters written to \n {}\n'.format(
                file_name
            ),
            'cyan'
        )

    return


def write_model_data(dataset: TauTDataset | TauHDataset,
                     model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel, # noqa
                     file_name: str, verbose: bool = True) -> None:
    '''
    Creates file containing rate vs temperature/field calculated using model
    parameters

    Parameters
    ----------
    dataset: TauTDataset | TauHDataset
        Dataset to which a model was successfully fitted (i.e. fit_status=True)
    model: LogTauTModel | MultiLogTauTModel | LogTauHModel | MultiLogTauHModel
        Model which has been fitted to dataset
    file_name: str
        Name of output file
    verbose: bool, default True
        If True, output file location is written to terminal

    Returns
    -------
    None
    '''

    if not model.fit_status:
        return

    if isinstance(dataset, TauHDataset):
        x_vals = copy.copy(dataset.fields)
        x_var_label = 'H (Oe)'

    elif isinstance(dataset, TauTDataset):
        x_vals = copy.copy(dataset.temperatures)
        x_var_label = 'T (K)'

    if type(model) in [MultiLogTauTModel, MultiLogTauHModel]:
        logmodels = model.logmodels
    else:
        logmodels = [model]

    f = open(file_name, 'w', encoding='utf-8')

    x_vars_grid = np.linspace(
        np.min(x_vals),
        np.max(x_vals),
        1000
    )

    f.write('{:>9} '.format(x_var_label))
    for logmodel in logmodels:
        f.write('{:>7} rate '.format(logmodel.NAME))
    if len(logmodels) > 1:
        f.write('  Total rate (s^-1)')
    f.write('\n')

    for grid_pt in x_vars_grid:
        f.write('{: 9.5f} '.format(grid_pt))
        total = 0.
        for logmodel in logmodels:
            rate = 10**logmodel.model(
                logmodel.final_var_values,
                [grid_pt]
            )[0]
            f.write('{:.6E} '.format(rate))
            total += rate
        if len(logmodels) > 1:
            f.write('{:.6E}'.format(total))
        f.write('\n')

    if verbose:
        ut.cprint(
            '\n Relaxation model τ⁻¹ vs {} written to \n {}\n'.format(
                x_var_label[0],
                file_name
            ),
            'cyan'
        )

    return
