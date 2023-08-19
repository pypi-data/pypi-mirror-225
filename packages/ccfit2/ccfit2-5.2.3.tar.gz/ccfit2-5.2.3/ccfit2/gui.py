'''
This module contains gui helper functions
'''

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.cm as cm
from matplotlib.colorbar import Colorbar
import matplotlib.colors as mpl_col
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from matplotlib.ticker import NullFormatter, FormatStrFormatter, LogLocator, \
                              SymmetricalLogLocator, FuncFormatter # noqa

import numpy as np
import numpy.typing as npt
import sys

from qtpy import QtWidgets, QtCore
import pyqtgraph as pg

from . import utils

# Default values for interactive parameter widgets of relaxation.FitWindow
widget_defaults = {
    'Orbach': {
        'u_eff': {
            'min': 0.,
            'max': 3000.,
            'valinit': 1500.,
            'step': 1,
            'decimals': 2
        },
        'A': {
            'min': -30.,
            'max': 30.,
            'valinit': -11.,
            'step': 0.01,
            'decimals': 3
        }
    },
    'Raman': {
        'R': {
            'min': -30.,
            'max': 30.,
            'valinit': -6.,
            'step': 0.01,
            'decimals': 3
        },
        'n': {
            'min': 0,
            'max': 20.,
            'valinit': 3.,
            'step': 0.01,
            'decimals': 3
        }
    },
    'QTM': {
        'Q': {
            'min': -6.,
            'max': 6.,
            'valinit': 1.,
            'step': 0.01,
            'decimals': 4
        }
    },
    'Direct': {
        'D': {
            'min': -6.,
            'max': 6.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        }
    },
    'FD-QTM': {
        'Q': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'Q_H': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'p': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        }
    },
    'Raman-II': {
        'C': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'm': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        }
    },
    'Constant': {
        'Ct': {
            'min': -30.,
            'max': 10.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        }
    },
    'Brons-Van-Vleck * Raman-II': {
        'e': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'f': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'C': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'm': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
    },
    'Brons-Van-Vleck * Constant': {
        'e': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'f': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        },
        'Ct': {
            'min': -30.,
            'max': 30.,
            'valinit': 0.1,
            'step': 0.01,
            'decimals': 4
        }
    }
}


def min_max_ticks_with_zero(values: list[float],
                            nticks: int) -> tuple[list[float], float]:
    '''
    Calculates tick positions including zero given a specified number of
    ticks either size of zero

    Parameters
    ----------
    values: list[float]
        Values plotted on this axis e.g. y-values or x-values
    n_ticks: int
        Number of ticks to produce either side of zero.
        i.e. total number of ticks is 2*n_ticks + 1

    Returns
    -------
    list[float]
        Tick positions
    float
        Maximum tick value
    '''

    # Extra tick for zero
    nticks += 1

    lowticks = np.linspace(-np.max(np.abs(values)), 0, nticks)
    highticks = np.linspace(np.max(np.abs(values)), 0, nticks)
    ticks = np.append(np.append(lowticks[:-1], [0.0]), np.flip(highticks[:-1]))

    return ticks, np.max(np.abs(values))


def calc_y_rate_lims(rates: list[float],
                     rate_err: list[float] = []) -> tuple[float, float]:
    '''
    Defines rate plot y limits as 10^integer

    Parameters
    ----------
    rates: list[float]
        Relaxation rates in s^-1
    rate_err: list[float], default []
        Error on rate, upper then lower\n
        Shape (n_rates, 2)

    Returns
    -------
    float
        Upper tick position
    float
        Lower tick position
    '''
    # Define limits of y axis
    # Upper limit from rounding up to nearest power of 10
    # Lower from rounding down to nearest power of 10

    if isinstance(rate_err, list):
        rate_err = np.asarray(rate_err)

    if not len(rate_err):
        rate_err = np.zeros([2, len(rates)])
    y_lower = 10**np.floor(
        np.log10(
            np.nanmin(
                [rates, rates + rate_err[1, :], rates - rate_err[0, :]]
            )
        )
    )
    y_upper = 10**np.ceil(
        np.log10(
            np.nanmax(
                [rates, rates + rate_err[1, :], rates - rate_err[0, :]]
            )
        )
    )

    if np.isnan(y_lower):
        y_lower = y_upper / 10
    if np.isnan(y_upper):
        y_upper = y_lower / 10

    return y_lower, y_upper


def calc_linthresh(x_vals: npt.ArrayLike) -> float:
    '''
    Calculates linthresh for symlog scale using field values.
    Valid only for rate/time versus field plots

    Parameters
    ----------
    x_vals: array_like
        Field values in Oe

    Returns
    -------
    float
        linthresh for symlog scale
    '''

    x_vals = np.asarray(x_vals)

    # Using first value greater than machine eps calculate new threshold
    it = np.argmin(x_vals[np.where(x_vals > np.finfo(float).eps)])
    linthresh = 10**np.floor(
        np.log10(x_vals[np.where(x_vals > np.finfo(float).eps)][it])
    )

    return linthresh


def calc_linscale(x_vals: npt.ArrayLike) -> float:
    '''
    Calculates how much space the linear region takes up on the symlog axis
    Defined here as reciprocal of number of decades spanned by data + 1
    where the +1 accounts for the zero point itself, considered as its own
    decade

    Parameters
    ----------
    x_vals: array_like[float]
        X values

    Returns
    -------
    float
        Width of linear region
    '''

    nz_x_vals = np.log10(x_vals[np.nonzero(x_vals)])
    decs = [np.floor(val) for val in nz_x_vals]

    n_dec = np.max(decs) - np.min(decs) + 1

    return 1 / n_dec


def format_rate_x_y_axes(ax: plt.Axes, rates: list[float],
                         x_vals: list[float],
                         rate_err: list[float] = [],
                         x_type: str = 'temperature') -> None:
    '''
    Wrapper for calc_y_rate_lims and set_rate_xtick_formatting
    Formats both axes of a rate vs T or H plot

    Parameters
    ----------
    ax: plt.Axes
        Axis to modify
    rates: list[float]
        Relaxation rates in s^-1
    x_vals: list[float]
        x values of plot (T or H)
    rate_err: list[float], default []
        Error on rates, upper then lower one per rate.\n
        Shape (n_rates, 2)
    x_type: str, {'field', 'temperature'}
        Type of data, temperature (T) or field (H)

    Returns
    -------
    None
    '''

    y_lower, y_upper = calc_y_rate_lims(rates, rate_err)

    ax.set_ylim([y_lower, y_upper])

    set_rate_xtick_formatting(ax, x_vals, x_type=x_type)

    ax.yaxis.set_minor_locator(LogLocator(base=10, subs='auto'))

    return


def set_rate_xtick_formatting(ax: plt.Axes, x_vals: list[float],
                              x_type: str = 'temperature') -> None:
    '''
    Sets x-tick formatting for rate plot. Enables minor tick labels if <1.1
    order of magnitude spanned by ticks

    Parameters
    ----------
    ax: plt.Axes
        Axis to modify
    x_vals: list[float]
        x values of plot (T or H)
    x_type: str, {'field', 'temperature'}
        Type of data, temperature (T) or field (H)

    Returns
    -------
    None
    '''

    if x_type == 'field':

        # Major ticks
        # Let matplotlib decide decimal values, but stop it
        # converting them to 10^val notation
        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda y, _: '{:g}'.format(y))
        )
        # Disable minor tick labels
        ax.xaxis.set_minor_formatter(NullFormatter())
        # and set minor tick locations
        ax.xaxis.set_minor_locator(
            SymmetricalLogLocator(
                base=10,
                subs=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                linthresh=calc_linthresh(x_vals)
            )
        )
    elif x_type == 'temperature':
        x_vals = np.log10(x_vals)
        # Major ticks
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
        # Minor ticks
        if np.max(x_vals) - np.min(x_vals) > 1.05:
            # No minor ticks if > 1 and a bit decades spanned by temperature
            ax.xaxis.set_minor_formatter(NullFormatter())
        else:
            # Add minor tick labels when range is small
            # i.e. only just crosses a decade
            # and make tick lengths equal to major ticks
            ax.xaxis.set_minor_formatter(FormatStrFormatter('%.0f'))
            ax.tick_params('x', length=3.5, width=1, which='major')
            ax.tick_params('x', length=3.5, width=1, which='minor')

    return


def convert_log_ticks_to_lin(ax: pg.graphicsItems.AxisItem.AxisItem,
                             logx_vals: list[float],
                             shift: float = 0.) -> None:
    '''
    Converts logarithmic tick values to linear and adds to pyqtgraph axis

    Shift applies a shift to the ticks, and is neccessary when the data
    has been shifted to accommodate a x_value of 0 (e.g. Field = 0)
    '''

    # Determine size of this item in pixels
    bounds = ax.mapRectFromParent(ax.geometry())
    span = (bounds.topLeft(), bounds.topRight())
    points = list(map(ax.mapToDevice, span))

    lengthInPixels = pg.Point(points[1] - points[0]).length()
    if lengthInPixels == 0:
        return

    # Determine major / minor / subminor axis ticks
    tick_tuple = ax.tickValues(ax.range[0], ax.range[1], lengthInPixels)

    minor_ticks = []
    intermediate_ticks = []

    if len(tick_tuple) >= 1:
        major_tick_vals = tick_tuple[0][1]
        major_ticks = [
            (level + shift, '{:.0f}'.format(10**level))
            for level in major_tick_vals
        ]

    if len(tick_tuple) >= 2:
        minor_tick_vals = tick_tuple[-1][1]

        if np.max(logx_vals) - np.min(logx_vals) < 1.1:
            minor_ticks = [
                (level + shift, '{:.0f}'.format(10**level))
                for level in minor_tick_vals
            ]
        else:
            minor_ticks = [
                (level + shift, '')
                for level in minor_tick_vals
            ]

    if len(tick_tuple) >= 3:
        inter_tick_vals = tick_tuple[1][1]
        intermediate_ticks = [
            (level + shift, '{:.0f}'.format(10**level))
            for level in inter_tick_vals
        ]

    if any(val == 0 for val in logx_vals):
        major_ticks.append((0., '0'))

    ax.setTicks([major_ticks, intermediate_ticks, minor_ticks])

    return


def error_box(message: str, title: str = 'Error') -> None:
    '''
    Creates simple qt error box with specified text and title

    Parameters
    ----------
    message: str
        Text shown in body of window
    title: str, default 'error'
        Text shown in title of window

    Returns
    -------
    None
    '''
    _ = QtWidgets.QApplication(sys.argv)
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.exec_()
    sys.exit()


class SampleInfoEntry(QtWidgets.QMainWindow):
    '''
    QT Widget for sample information input (mass and molecular weight)
    '''

    def __init__(self, user_cfg: utils.UserConfig, *args, **kwargs):

        # If user closes, then do not continue as values
        # haven't been entered
        self.close_continue = False

        super(SampleInfoEntry, self).__init__(*args, **kwargs)

        self.setWindowTitle('Sample information')

        self.setAttribute(QtCore.Qt.WA_QuitOnClose)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setStyleSheet(
            '''
            QMainWindow {
                background-color: white
            }
            '''
        )

        # Minimum Window Size
        self.setMinimumSize(QtCore.QSize(310, 150))

        # Center the window on the screen
        qtRectangle = self.frameGeometry()
        centre_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centre_point)
        self.move(qtRectangle.topLeft())
        qtRectangle = self.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Widget to wrap everything
        self.widget = QtWidgets.QWidget(parent=self)
        self.setCentralWidget(self.widget)

        layout = QtWidgets.QVBoxLayout(self.widget)

        # First column, text entry and label for MW
        col_1_widget = QtWidgets.QWidget(parent=self.widget)
        col_1_layout = QtWidgets.QHBoxLayout(col_1_widget)

        self.mw_entry = QtWidgets.QDoubleSpinBox(parent=col_1_widget)
        self.mw_entry.setMaximum(200000)
        self.mw_entry.setDecimals(5)
        self.mw_entry.setButtonSymbols(QtWidgets.QDoubleSpinBox.NoButtons)
        self.mw_entry.setKeyboardTracking(False)

        mw_label = QtWidgets.QLabel(r'Molecular Weight (g mol<sup>-1<\sup>)')
        col_1_layout.addWidget(mw_label)
        col_1_layout.addWidget(self.mw_entry)

        # 2nd column, text entry and label for MW
        col_2_widget = QtWidgets.QWidget(parent=self.widget)
        col_2_layout = QtWidgets.QHBoxLayout(col_2_widget)

        self.mass_entry = QtWidgets.QDoubleSpinBox(parent=col_2_widget)
        self.mass_entry.setMaximum(200000)
        self.mass_entry.setDecimals(5)
        self.mass_entry.setButtonSymbols(QtWidgets.QDoubleSpinBox.NoButtons)
        self.mass_entry.setKeyboardTracking(False)

        mass_label = QtWidgets.QLabel('Sample mass (mg)')
        col_2_layout.addWidget(mass_label)
        col_2_layout.addWidget(self.mass_entry)

        # 3rd column - submit button
        col_3_widget = QtWidgets.QWidget(parent=self.widget)
        col_3_layout = QtWidgets.QHBoxLayout(col_3_widget)

        submit_button = QtWidgets.QPushButton(
            parent=col_3_widget,
            text='Submit'
        )
        submit_button.clicked.connect(
            lambda x: self.parse_info(user_cfg)
        )
        col_3_layout.addWidget(submit_button)

        layout.addWidget(col_1_widget)
        layout.addWidget(col_2_widget)
        layout.addWidget(col_3_widget)

        return

    def parse_info(self, user_cfg: utils.UserConfig):
        '''
        Callback function for qt window for mass and molecular weight

        Parameters
        ----------
        user_cfg: utils.UserConfig
            UserConfig object which will contain mass and mw

        Returns
        -------
        None
        '''

        mass = float(self.mass_entry.text())
        mw = float(self.mw_entry.text())

        if mass <= 0.:
            error_box('Mass cannot be <= zero')
        if mw <= 0.:
            error_box('MW cannot be <= zero')

        setattr(user_cfg, 'mass', mass)
        setattr(user_cfg, 'mw', mw)

        self.close_continue = True
        self.close()

        return

    def closeEvent(self, event):
        '''
        Catch if user closes prompt
        '''
        if self.close_continue:
            self.close()
        else:
            sys.exit()


def mass_mw_entry(user_cfg: utils.UserConfig) -> None:
    '''
    Creates qt window for user to input mass and molecular weight of
    sample

    Parameters
    ----------
    user_cfg: utils.UserConfig
        Configuration object

    Returns
    -------
    None
    '''

    app = QtWidgets.QApplication([])

    window = SampleInfoEntry(user_cfg)
    window.show()

    app.exec()

    del app

    return


def filename_entry(user_cfg: utils.UserConfig) -> None:
    '''
    Creates qt window for user to input mass and molecular weight of
    sample

    Parameters
    ----------
    user_cfg: utils.UserConfig
        Configuration object

    Returns
    -------
    None
    '''

    _ = QtWidgets.QApplication(sys.argv)

    window = QtWidgets.QMainWindow()

    file = QtWidgets.QFileDialog.getOpenFileName(
        window,
        caption="File to Import",
        directory=".",
        filter="Text files (*.dat *.txt *.csv)"
    )

    # Check for empty filename - user has closed window
    if file[0] is None:
        sys.exit()
    elif not len(file[0]):
        sys.exit()
    else:
        user_cfg.file_name = file[0]

    return


def make_mpl_radiobuttons(pos: list[float], labels: list[str],
                          figure: plt.Figure, circle_area: float = 100.,
                          ax: str | plt.Axes = 'create',
                          facecolor: str = 'blue') -> RadioButtons:
    '''
    Creates matplotlib radiobuttons on given figure

    Parameters
    ----------
    pos: list[float]
        Four values specifying left, bottom, width, height of
        rectangle in which buttons will reside
    labels: list[str]
        Label for each radiobutton
    figure: plt.Figure
        Figure to which radiobuttons are added
    circle_area: float, default 100.
        Area of radiobutton circle
    ax: str | plt.Axes, default 'create'
        If string 'create', a new axis is made, else the provided axis is used
    facecolor: str
        Name of colour used for button when activated

    Returns
    -------
    matplotlib.widgets.RadioButtons
        Set of radiobuttons for matplotlib figure window
    '''

    if ax == 'create':
        ax = plt.axes(
            pos,
            facecolor='w',
            frameon=False,
            aspect='equal',
            figure=figure
        )
    buttons = RadioButtons(
        ax,
        labels,
        radio_props={
            's': circle_area,
            'facecolor': facecolor
        }
    )

    if len(labels) == 1:
        fc = [0, 0, 0, 0]
    else:
        fc = [
            [0, 0, 0, 0] for _ in range(len(labels))
        ]

    buttons._buttons.set_facecolor(
        fc
    )

    return buttons


def create_ac_temp_colorbar(ax: plt.Axes, fig: plt.Figure,
                            temps: list[float],
                            colors: mpl_col.Colormap) -> Colorbar:
    '''
    Creates colorbar for temperatures in AC plotting

    Parameters
    ----------

    ax: plt.Axes
        Axis to which colorbar is added
    fig: plt.Figure
        Figure to which colorbar is added
    temps: list[float]
        Temperatures in Kelvin
    colors: matplotlib.colors.Colormap
        Colormap used in plot

    Returns
    -------
    matplotlib.colorbar.Colorbar
        Matplotlib colorbar object

    Raises
    ------
    ValueError
        If no temperatures specified
    '''

    n_temps = len(temps)

    if n_temps == 0:
        raise ValueError('Cannot create colorbar for zero temperatures')

    # Make colourbar
    # Indexing starts at zero and ends at num_temps
    norm = mpl_col.BoundaryNorm(
        np.arange(0, n_temps + 1),
        ncolors=colors.N
    )

    # Scalar mappable converts colourmap numbers into an image of colours
    sm = cm.ScalarMappable(cmap=colors, norm=norm)

    colorbar_ticks = np.arange(1, n_temps + 1) - 0.5
    colorbar_labels = get_temp_colourbar_ticks(temps)

    cbar = fig.colorbar(
        sm,
        ticks=colorbar_ticks,
        orientation='horizontal',
        format='%.1f',
        cax=ax
    )

    ax.set_xticklabels(
        colorbar_labels,
        rotation=0,
        fontsize='smaller'
    )

    ax.minorticks_off()

    # Set colourbar label - technically title - above bar
    cbar.ax.set_title('T (K)', fontsize='smaller')

    return cbar


def get_temp_colourbar_ticks(temperatures: list[float]) -> list[float]:
    '''
    Creates ticks for a temperature colourbar.

    If there are fewer than 9 data points, give tick to all temperatures

    If there are between 9 and 17, slice every 3 or 4 points depending on
    even-odd.

    If there are more than 17, slice every 5 or 6 points depending on
    even-odd.

    Parameters
    ----------
    temperatures: list[float]
        Temperatures in Kelvin

    Returns
    -------
    list[float]
        Colourbar tick positions
    '''

    n_temps = len(temperatures)

    ticks = ['{:.1f}'.format(tp) for tp in temperatures]

    if n_temps <= 8:
        step = 1
    elif 9 <= n_temps <= 17:
        if n_temps % 2 == 0:
            step = 3
        else:
            step = 4
    else:
        if n_temps % 2 == 0:
            step = n_temps // 5
        else:
            step = n_temps // 4

    # Swap numbers for blanks, and ensure start and end are present
    ticks = [ti if not it % step else '' for (it, ti) in enumerate(ticks)]
    ticks[0] = '{:.1f}'.format(temperatures[0])
    ticks[-1] = '{:.1f}'.format(temperatures[-1])

    # Remove adjacent labels at end
    if n_temps > 8 and ticks[-2] != '':
        ticks[-2] = ''

    return ticks


class SusceptibilityCanvas(FigureCanvasQTAgg):
    '''
    Figure and axes for AC Susceptibility plots
    '''

    def __init__(self, width, height, dpi=100, parent=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.gs = gridspec.GridSpec(3, 1, height_ratios=[0.05, 1, 1])
        self.ax = [
            self.fig.add_subplot(self.gs[0]),
            self.fig.add_subplot(self.gs[1]),
            self.fig.add_subplot(self.gs[2])
        ]
        super(SusceptibilityCanvas, self).__init__(self.fig)


class ColeColeCanvas(FigureCanvasQTAgg):
    '''
    Figure and axes for AC Cole-Cole plots
    '''

    def __init__(self, width, height, dpi=100, parent=None):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.gs = gridspec.GridSpec(2, 1, height_ratios=[0.03, 0.9])
        self.ax = [
            self.fig.add_subplot(self.gs[0]),
            self.fig.add_subplot(self.gs[1])
        ]
        super(ColeColeCanvas, self).__init__(self.fig)
