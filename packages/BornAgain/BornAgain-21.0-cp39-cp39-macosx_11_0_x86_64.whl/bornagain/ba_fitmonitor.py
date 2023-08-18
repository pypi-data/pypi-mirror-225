#  **************************************************************************  #
"""
#   BornAgain: simulate and fit reflection and scattering
#
#   @file      Wrap/Python/ba_fitmonitor.py
#   @brief     Plotter classes for monitoring fit progress.
#
#   @homepage  http://apps.jcns.fz-juelich.de/BornAgain
#   @license   GNU General Public License v3 or higher (see COPYING)
#   @copyright Forschungszentrum Juelich GmbH 2019
#   @authors   Scientific Computing Group at MLZ (see CITATION, AUTHORS)
"""
#  **************************************************************************  #

import bornagain as ba
from bornagain import ba_plot as bp
try:  # workaround for build servers
    import numpy as np
    from matplotlib import pyplot as plt
    from matplotlib import gridspec
except Exception as e:
    print("In ba_fitmonitor.py: {:s}".format(str(e)))

class Plotter:
    """
    Draws fit progress. Base class for simulation-specific classes (PlotterGISAS etc).
    """

    def __init__(self,
                 zmin=None,
                 zmax=None,
                 xlabel=None,
                 ylabel=None,
                 units=ba.Coords_UNDEFINED,
                 aspect=None):

        self._fig = plt.figure(figsize=(10.25, 7.69))
        self._fig.canvas.draw()
        self._zmin = zmin
        self._zmax = zmax
        self._xlabel = xlabel
        self._ylabel = ylabel
        self._units = units
        self._aspect = aspect

    def __call__(self, fit_objective):
        self.plot(fit_objective)

    def reset(self):
        self._fig.clf()

    def plot(self):
        self._fig.tight_layout()
        plt.pause(0.3)


class PlotterGISAS(Plotter):
    """
    Draws fit progress, for GISAS simulation.
    """

    def __init__(self,
                 zmin=None,
                 zmax=None,
                 xlabel=None,
                 ylabel=None,
                 units=ba.Coords_UNDEFINED,
                 aspect=None):
        Plotter.__init__(self, zmin, zmax, xlabel, ylabel, units, aspect)

    @staticmethod
    def make_subplot(nplot):
        plt.subplot(2, 2, nplot)
        plt.subplots_adjust(wspace=0.2, hspace=0.2)

    def plot(self, fit_objective):
        Plotter.reset(self)

        real_data = fit_objective.experimentalData()
        sim_data = fit_objective.simulationResult()
        diff = fit_objective.absoluteDifference()

        self.make_subplot(1)

        # same limits for both plots
        arr = real_data.array()
        zmax = np.amax(arr) if self._zmax is None else self._zmax
        zmin = zmax*1e-6 if self._zmin is None else self._zmin

        bp.plot_simres(real_data,
                       title="Experimental data",
                       intensity_min=zmin,
                       intensity_max=zmax,
                       units=self._units,
                       xlabel=self._xlabel,
                       ylabel=self._ylabel,
                       zlabel='',
                       aspect=self._aspect)

        self.make_subplot(2)
        bp.plot_simres(sim_data,
                       title="Simulated data",
                       intensity_min=zmin,
                       intensity_max=zmax,
                       units=self._units,
                       xlabel=self._xlabel,
                       ylabel=self._ylabel,
                       zlabel='',
                       aspect=self._aspect)

        self.make_subplot(3)
        bp.plot_simres(diff,
                       title="Difference",
                       intensity_min=zmin,
                       intensity_max=zmax,
                       units=self._units,
                       xlabel=self._xlabel,
                       ylabel=self._ylabel,
                       zlabel='',
                       aspect=self._aspect)

        self.make_subplot(4)
        plt.title('Parameters')
        plt.axis('off')

        iteration_info = fit_objective.iterationInfo()

        plt.text(
            0.01, 0.85, "Iterations  " +
            '{:d}'.format(iteration_info.iterationCount()))
        plt.text(0.01, 0.75,
                 "Chi2       " + '{:8.4f}'.format(iteration_info.chi2()))
        index = 0
        params = iteration_info.parameterMap()
        for key in params:
            plt.text(0.01, 0.55 - index*0.1,
                     '{:30.30s}: {:6.3f}'.format(key, params[key]))
            index = index + 1

        Plotter.plot(self)


class PlotterSpecular:
    """
    Draws fit progress, for specular simulation.
    """

    def __init__(self, units=ba.Coords_UNDEFINED, pause=0.0):
        self.units = units
        self.pause = pause
        self._fig = plt.figure(figsize=(10, 7))
        self._fig.canvas.draw()

    def __call__(self, fit_objective):
        self.plot(fit_objective)

    def plot(self, fit_objective):
        self._fig.clf()
        # retrieving data from fit suite
        exp_data = fit_objective.experimentalData()
        sim_data = fit_objective.simulationResult()
        unc_data = fit_objective.uncertaintyData()

        # data values
        sim_values = sim_data.array(self.units)
        exp_values = exp_data.array(self.units)
        unc_values = None if unc_data is None else unc_data.array(
            self.units)

        # default font properties dictionary to use
        font = { 'size': 16 }

        plt.yscale('log')
        plt.ylim((0.5*np.min(exp_values), 5*np.max(exp_values)))
        plt.plot(exp_data.convertedBinCenters(), exp_values, 'k--')
        if unc_values is not None:
            plt.plot(exp_data.convertedBinCenters(),
                     exp_values - unc_values,
                     'xkcd:grey',
                     alpha=0.6)
            plt.plot(exp_data.convertedBinCenters(),
                     exp_values + unc_values,
                     'xkcd:grey',
                     alpha=0.6)
        plt.plot(sim_data.convertedBinCenters(), sim_values, 'b')

        xlabel = bp.get_axes_labels(exp_data, self.units)[0]
        legend = ['Experiment', 'BornAgain']
        if unc_values is not None:
            legend = ['Experiment', r'Exp $\pm \sigma$', 'BornAgain']
        plt.legend(legend, loc='upper right', prop=font)
        plt.xlabel(xlabel, fontdict=font)
        plt.ylabel("Intensity", fontdict=font)
        if bp.do_show:
            plt.pause(self.pause)

    def show(self):
        if bp.do_show:
            plt.show()
