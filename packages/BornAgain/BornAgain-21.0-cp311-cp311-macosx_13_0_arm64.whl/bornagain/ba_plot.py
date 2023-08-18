#  **************************************************************************  #
"""
#   BornAgain: simulate and fit reflection and scattering
#
#   @file      Wrap/Python/ba_plot.py
#   @brief     Python extensions of the SWIG-generated Python module bornagain.
#
#   @homepage  http://apps.jcns.fz-juelich.de/BornAgain
#   @license   GNU General Public License v3 or higher (see COPYING)
#   @copyright Forschungszentrum Juelich GmbH 2016
#   @authors   Scientific Computing Group at MLZ (see CITATION, AUTHORS)
"""
#  **************************************************************************  #

import math, os, pathlib, sys
import bornagain as ba
try:
    import numpy as np
    import matplotlib as mpl
    from matplotlib import rc
    from matplotlib import pyplot as plt
    from matplotlib import gridspec, colors
    from mpl_toolkits.axes_grid1 import make_axes_locatable, axes_size
except Exception as e:
    print(f"Import failure in ba_plot.py: {e}")


def env_to_bool(varname):
    if varname not in os.environ:
        return False
    value = os.environ[varname].lower()
    if value in ('false', 'off', 'n', 'no', '0'):
        return False
    if value in ('true', 'on', 'y', 'yes', '1'):
        return True
    raise Exception(
        f"Environment variable {varname} has ambiguous value {value}.")


#  **************************************************************************  #
#  internal functions
#  **************************************************************************  #

def parse_any(tmp):
    for key in list(tmp.keys()):
        if key[0:4] == 'sim_':
            simargs[key[4:]] = tmp[key]
            print(f"""
Warning from bp.parse_args,
called from {sys.argv[0]}:
Obsolete argument \"{key}\".
All arguments starting with \"sim_\" are obsolete since BornAgain 21.
Support for bp.simargs will be removed in future releases.
Replace \"bp.simargs['{key[4:]}']\" by a hard-coded value
or by variable under your own control.
""")
        else:
            plotargs[key] = tmp[key]

    global datfile, figfile, do_show, tolerance, reference
    a = plotargs.pop('datfile', None)
    if a:
        datfile = a
        if pathlib.Path(datfile).suffix != '':
            raise Exception(
                "Parameter 'datfile' must contain no suffix (we will append .int.gz)")

    a = plotargs.pop('figfile', None)
    if a:
        figfile = a
        saveformat = pathlib.Path(figfile).suffix[1:]
        if saveformat == '':
            raise Exception(
                "Parameter 'figfile' must contain extension (like .pdf)")

    a = plotargs.pop('show', None)
    if a:
        if a == 'y':
            do_show = True
        elif a == 'n':
            do_show = False
        else:
            raise Exception("Parameter 'show' must be 'y' or 'n'")

    a = plotargs.pop('tolerance', None)
    if a:
        tolerance = float(a)

    a = plotargs.pop('reference', None)
    if a:
        reference = a

    if (tolerance is not None and reference is None) or \
       (tolerance is None and reference is not None):
        raise Exception(
            "If one of tolerance and reference is given, then the other must also be given")


def parse_commandline():
    tmp = {}
    for arg in sys.argv[1:]:
        s = arg.split("=")
        if len(s) != 2:
            raise Exception(
                f"command-line argument '{arg}' does not have form key=value"
            )
        try:
            tmp[s[0]] = int(s[1])
        except:
            tmp[s[0]] = s[1]
    parse_any(tmp)


def get_axes_limits(result, units):
    """
    Returns axes range as expected by pyplot.imshow.
    :param result: SimulationResult object from a Simulation
    :param units: units to use
    :return: axes ranges as a flat list
    """
    limits = []
    for i in range(result.rank()):
        ami, ama = result.axisMinMax(i, units)
        assert ami < ama, f'SimulationResult has invalid axis {i}, extending from {ami} to {ama}'
        limits.append(ami)
        limits.append(ama)

    return limits


def translate_axis_label(label):
    """
    Formats an axis label into a LaTeX representation
    :param label: text representation of the axis label
    :return: LaTeX representation
    """
    label_dict = {
        'X [nbins]': r'$X \; $(bins)',
        'X [mm]': r'$X \; $(mm)',
        'Y [nbins]': r'$Y \; $(bins)',
        'Y [mm]': r'$Y \; $(mm)',
        'phi_f [rad]': r'$\varphi_f \; $(rad)',
        'phi_f [deg]': r'$\varphi_f \;(^\circ)$',
        'alpha_i [rad]': r'$\alpha_{\rm i} \; $(rad)',
        'alpha_i [deg]': r'$\alpha_{\rm i} \;(^\circ)$',
        'alpha_f [rad]': r'$\alpha_{\rm f} \; $(rad)',
        'alpha_f [deg]': r'$\alpha_{\rm f} \;(^\circ)$',
        'Qx [1/nm]': r'$Q_x \; $(nm$^{-1}$)',
        'Qy [1/nm]': r'$Q_y \; $(nm$^{-1}$)',
        'Qz [1/nm]': r'$Q_z \; $(nm$^{-1}$)',
        'Q [1/nm]': r'$Q \; $(nm$^{-1}$)',
        'Position [nm]': r'Position (nm)'
    }
    if label in label_dict.keys():
        return label_dict[label]
    return label


def get_axes_labels(result, units):
    """
    Returns axes range as expected by pyplot.imshow.
    :param result: SimulationResult object from a Simulation
    :param units: units to use
    :return: axes ranges as a flat list
    Used internally and in Examples/fit/specular/RealLifeReflectometryFitting.py.
    """
    labels = []
    for i in range(result.rank()):
        labels.append(translate_axis_label(result.name_of_axis(i, units)))

    return labels


def plot_curve(xarray, yarray, **kwargs):
    """
    Used internally.
    """
    title = kwargs.pop('title', None)
    xlabel = kwargs.pop('xlabel', None)
    ylabel = kwargs.pop('ylabel', None)

    if xlabel:
        plt.xlabel(xlabel, fontsize=label_fontsize)
    if ylabel:
        plt.ylabel(ylabel, fontsize=label_fontsize)
    if title:
        plt.title(title)

    inside_ticks()

    plt.plot(xarray, yarray, **kwargs)


def plot_specular_curve(result):
    """
    Plots intensity data for specular simulation result
    :param result: SimulationResult from SpecularSimulation
    Used internally.
    """
    units = plotargs.pop('units', ba.Coords_UNDEFINED)

    intensity = result.array(units)
    x_axis = result.convertedBinCenters(units)

    xlabel = plotargs.pop('xlabel', get_axes_labels(result, units)[0])
    ylabel = plotargs.pop('ylabel', "Intensity")

    plt.yscale('log')

    ymax = plotargs.pop('intensity_max', np.amax(np.amax(intensity)*2))
    ymin = plotargs.pop('intensity_min',
                        max(np.amin(intensity)*0.5, 1e-18*ymax))
    plt.ylim([ymin, ymax])

    plot_curve(x_axis, intensity, xlabel=xlabel, ylabel=ylabel, **plotargs)


def check_or_save(result, fname, subname=""):
    if not tolerance or not reference:
        return
    reffile = reference + subname + ".int.gz"
    ok = ba.dataMatchesFile(result, reffile, tolerance)
    if not ok:
        outfile = fname + subname + ".int.gz"
        ba.writeDatafield(result, outfile)
        print(f"to overwrite reference:\ncp -f {outfile} {reffile}")
        raise Exception(f"=> no agreement between result and reference")

#  **************************************************************************  #
#  multiple frames in one plot
#  **************************************************************************  #

def save_results(results, name):
    """
    Write multiple simulation results to data files.
    Used internally.
    """
    nDigits = int(math.log10(len(results))) + 1
    formatN = "%" + str(nDigits) + "i"
    for i, result in enumerate(results):
        check_or_save(result, name, "." + (formatN % i))


class MultiPlot:
    """
    Used internally.
    """

    def __init__(self, n, ncol, fontsize=None):
        self.n = n
        self.ncol = ncol
        self.nrow = 1 + (self.n - 1) // self.ncol

        # Parameters as fraction of subfig size.
        yskip = 0.2
        bottomskip = yskip
        topskip = yskip/2
        xskip = 0.18
        leftskip = xskip
        rightskip = 0.28 + ncol*0.03
        xtot = self.ncol*1.0 + (self.ncol - 1)*xskip + leftskip + rightskip
        ytot = self.nrow*1.0 + (self.nrow - 1)*yskip + bottomskip + topskip

        # We need parameters as fraction of total fig size.
        self.xskip = xskip/xtot
        self.leftskip = leftskip/xtot
        self.rightskip = rightskip/xtot
        self.yskip = yskip/ytot
        self.bottomskip = bottomskip/ytot
        self.topskip = topskip/ytot

        # Set total figure dimensions.
        ftot = 5
        if fontsize:
            self.fontsize = fontsize
        else:
            self.fontsize = 18 + 36.0/(ncol + 2)
        # Create the figure 'fig' and its subplots axes ('tmp'->'axes').
        self.fig, tmp = plt.subplots(self.nrow,
                                     self.ncol,
                                     figsize=(ftot*xtot, ftot*ytot))
        if n > 1:
            self.axes = tmp.flat
        else:
            self.axes = [tmp]

        # Adjust whitespace around and between subfigures.
        plt.subplots_adjust(wspace=self.xskip,
                            hspace=self.yskip,
                            left=self.leftskip,
                            right=1 - self.rightskip,
                            bottom=self.bottomskip,
                            top=1 - self.topskip)

    def plot_colorlegend(self, im):
        # Plot the color legend.
        cbar_ax = self.fig.add_axes([
            1 - self.rightskip + 0.4*self.xskip, self.bottomskip,
            0.25*self.xskip, 1 - self.bottomskip - self.topskip
        ])
        cb = self.fig.colorbar(im, cax=cbar_ax)
        cb.set_label(r'$\left|F(q)\right|^2/V^{\,2}$',
                     fontsize=self.fontsize)


#  **************************************************************************  #
#  versatile plot calls
#  **************************************************************************  #

def inside_ticks():
    """
    Ticks settings for xy plots: on all axes and pointing inside.
    Used internally and in a few examples.
    """
    plt.gca().yaxis.set_ticks_position('both')
    plt.gca().xaxis.set_ticks_position('both')
    plt.gca().tick_params(which='both', direction='in')


def plot_array(array, axes_limits=None, **kwargs):
    """
    Plots numpy array as a heatmap in log scale.
    Used internally and in Examples/varia/AccessingSimulationResults.py.
    """
    assert len(array.shape) == 2
    assert array.shape[0] > 0
    assert array.shape[1] > 0
    if axes_limits is not None:
        assert len(axes_limits) == 4
        assert axes_limits[0] < axes_limits[
            1], f'Invalid x interval {axes_limits[0]} .. {axes_limits[1]}'
        assert axes_limits[2] < axes_limits[
            3], f'Invalid y interval {axes_limits[2]} .. {axes_limits[3]}'

    zmax = kwargs.pop('intensity_max', np.amax(array))
    zmin = kwargs.pop('intensity_min', 1e-6*zmax)

    if zmin == zmax == 0.0:
        norm = mpl.colors.Normalize(0, 1)
    else:
        norm = mpl.colors.LogNorm(zmin, zmax)

    xlabel = kwargs.pop('xlabel', None)
    ylabel = kwargs.pop('ylabel', None)
    zlabel = kwargs.pop('zlabel', "Intensity")
    title = kwargs.pop('title', None)
    aspect = kwargs.pop('aspect', 'equal')
    cmap = kwargs.pop('cmap', cmap_default)
    withCBar = kwargs.pop('with_cb', True)

    ax = plt.gca()
    im = ax.imshow(array,
                   cmap=cmap,
                   norm=norm,
                   aspect=aspect,
                   extent=axes_limits,
                   **kwargs)

    if xlabel:
        plt.xlabel(xlabel, fontsize=label_fontsize)
    if ylabel:
        plt.ylabel(ylabel, fontsize=label_fontsize)
    if title:
        plt.title(title)

    if withCBar:
        aspect = 20
        pad_fraction = 3

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="7%", pad="5%")
        cb = plt.colorbar(im, cax=cax)
        if zlabel:
            cb.set_label(zlabel, size=label_fontsize)

    return im


def plot_histogram(field, **kwargs):
    """
    Plots intensity data as heat map
    :param field: two-dimensional Datafield
    Used internally and in a few examples.
    """

    if 'xlabel' not in kwargs:
        kwargs['xlabel'] = translate_axis_label(field.xAxis().axisName())
    if 'ylabel' not in kwargs:
        kwargs['ylabel'] = translate_axis_label(field.yAxis().axisName())

    axes_limits = [
        field.xAxis().min(),
        field.xAxis().max(),
        field.yAxis().min(),
        field.yAxis().max()
    ]

    plot_array(field.npArray(), axes_limits=axes_limits, **kwargs)


def plot_simres(result, **kwargs):
    """
    Plots intensity data as heat map
    :param result: SimulationResult from GISAS/OffspecSimulation
    Used internally and in a few examples.
    """

    units = kwargs.pop('units', ba.Coords_UNDEFINED)
    axes_limits = get_axes_limits(result, units)
    axes_labels = get_axes_labels(result, units)

    if 'xlabel' not in kwargs:
        kwargs['xlabel'] = axes_labels[0]
    if 'ylabel' not in kwargs:
        kwargs['ylabel'] = axes_labels[1]

    return plot_array(result.array(), axes_limits=axes_limits, **kwargs)

#  **************************************************************************  #
#  standard user calls
#  **************************************************************************  #

def parse_args(**kwargs):
    """
    Ingests plot options:
    :param intensity_min: Min value on amplitude's axis or color legend
    :param intensity_max: Max value on amplitude's axis or color legend
    :param units: units for plot axes
    :param ymin: minimal y-axis value to show
    :param ymax: maximum y-axis value to show
    :param zmin: Min value on amplitude's color legend
    :param zmax: Max value on amplitude's color legend
    and instrumentation parameters:
    :param datfile: save result to data file
    :param figfile: save figure to image file (with extension .pdf .png or similar)
    :param show: if 'n' than do not show the plot
    :param tolerance: maximum relative error when checking against reference
    :param reference: data file (without extension .int.gz) to check against
    """
    tmp = {}
    for key, val in kwargs.items():
        tmp[key] = val
    parse_any(tmp)

    parse_commandline() # command line overwrites options in script


def show_or_export():
    if figfile:
        plt.savefig(figfile, format=saveformat, bbox_inches='tight')
    if do_show:
        plt.show()


def plot_simulation_result(result):
    """
    Draws simulation result and (optionally) shows the plot.
    """
    if datfile:
        check_or_save(result, datfile)

    if len(result.array().shape) == 1:
        # 1D data => assume specular simulation
        plot_specular_curve(result, **plotargs)
    else:
        plot_simres(result, **plotargs)
    plt.tight_layout()

    show_or_export()


def make_plot_row(results):
    make_plot(results, len(results))


def make_plot(results, ncol):
    """
    Make a plot consisting of one detector image for each Result in results,
    plus one common color legend.

    :param results: List of simulation results
    :param ncol:    Maximum number of plot frames per row
    """
    if datfile:
        save_results(results, datfile)

    multiPlot = MultiPlot(len(results), ncol,
                          plotargs.pop('fontsize', None))
    cmap = plotargs.pop('cmap', cmap_default)

    # Always the same color legend, to facilitate comparisons between figures.
    norm = mpl.colors.LogNorm(1e-8, 1)
    # Plot the subfigures.
    for i, result in enumerate(results):
        ax = multiPlot.axes[i]
        axes_limits = get_axes_limits(result, ba.Coords_UNDEFINED)

        im = ax.imshow(result.array(),
                       cmap=cmap,
                       norm=norm,
                       extent=axes_limits,
                       aspect=1,
                       **plotargs)

        ax.set_xlabel(r'$\varphi_{\rm f} (^{\circ})$',
                      fontsize=multiPlot.fontsize)
        if i % ncol == 0:
            ax.set_ylabel(r'$\alpha_{\rm f} (^{\circ})$',
                          fontsize=multiPlot.fontsize)
        if result.title() != "":
            ax.set_title(result.title(), fontsize=multiPlot.fontsize)
        ax.tick_params(axis='both',
                       which='major',
                       labelsize=multiPlot.fontsize*21/24)

    multiPlot.plot_colorlegend(im)

    show_or_export()


def plot_multicurve(results, xlabel, ylabel):
    """
    Plots any number of xy curves into one frame.
    """
    if datfile:
        save_results(results, datfile)

    legend = []
    for result in results:
        x = result.convertedBinCenters()
        y = result.array()
        legend.append(result.title())
        plt.plot(x, y)

    inside_ticks()

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.legend(legend, loc=plotargs.pop('legendloc', 'upper right'))

    show_or_export()


def plot_multicurve_specular(results):
    plt.yscale('log')
    xlabel = get_axes_labels(results[0], ba.Coords_UNDEFINED)[0]
    plot_multicurve(results, xlabel, r'Intensity')

#  **************************************************************************  #
#  global settings
#  **************************************************************************  #

# default values from environment variables
cmap_default = os.environ['CMAP'] if 'CMAP' in os.environ else 'inferno'
usetex_default = env_to_bool('USETEX')

label_fontsize = 16
# rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
rc('text', usetex=usetex_default)
# mpl.rcParams['image.interpolation'] = 'none'

plotargs = {}
simargs = {}
datfile = None
figfile = None
saveformat = None
do_show = True
tolerance = None
reference = None

parse_commandline()
