import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from surfinpy import utils as ut

class ChemicalPotentialPlot:
    """Class that plots a phase diagram as a function of chemical potential.

    Parameters
    ----------
    x : array like
        x axis, chemical potential of species x
    y : array like
        y axis, chemical potential of species y
    z : array like
        two dimensional grid, phase info
    labels : list
        list of phase labels
    ticks : list
        list of phases
    xlabel : str
        species name for x axis label
    ylabel : str
        species name for y axis label
    """
    def __init__(self, x, y, z, labels, ticks, xlabel, ylabel):
        self.x = x
        self.y = y
        self.z = z
        self.labels = labels
        self.ticks = ticks
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot_phase(self, temperature=None, xlabel=None, ylabel=None, output="phase.png", 
                   colourmap="viridis", set_style="default", figsize=None, show_fig=True):
        """Plots a simple phase diagram as a function of chemical potential.

        Parameters
        ----------
        temperature: int (optional)
            Temperature. Default=None
        xlabel: str (optional)
            Set a custom x-axis label. Default=None
        ylabel: str (optional)
            Set a custom y-axis label. Default=None
        output: str (optional)
            Output filename. Default='phase.png'
            If output is set to `None`, no output is generated.
        colourmap: str (optional)
            Colourmap for the plot. Default='viridis'
        figsize: tuple (optional)
            Set a custom figure size. Default=None
        show_fig: bool (optional)
            Automatically display a figure. Default=True
            If set to False the plot is returned as an object.
        """
        if set_style:
            plt.style.use(set_style)
        levels = ut.get_levels(self.z)
        ticky = ut.get_ticks(self.ticks)
        temperature_label = str(temperature) + " K"
        if xlabel:
            XLab = xlabel
        else:
            XLab = "$\Delta \mu_{\mathrm{" + self.xlabel + "}}$" + " (eV)"
        if ylabel:
            YLab = ylabel
        else:
            YLab = "$\Delta \mu_{\mathrm{" + self.ylabel + "}}$" + " (eV)"
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
        CM = ax.contourf(self.x, self.y, self.z, levels=levels, cmap=colourmap)
        ax.set_ylabel(YLab, fontsize=14)
        ax.set_xlabel(XLab, fontsize=14)
        if temperature:
            ax.text(0.1, 0.95, temperature_label,  fontsize=15, color="white",
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes)
        ax.tick_params(labelsize=12)
        cbar = fig.colorbar(CM, ticks=ticky, pad=0.1)
        cbar.ax.set_yticklabels(self.labels)
        plt.tight_layout()
        if output:
            plt.savefig(output, dpi=600)
        if show_fig:
            plt.show()
        else:
            return ax

    def plot_mu_p(self, temperature, output="phase.png", colourmap="viridis",
                  set_style="default"):
        """ Plots a phase diagram  with two sets of axis, one as a function of
        chemical potential and the second is as a function of pressure.

        Parameters
        ----------
        temperature : int (optional)
            temperature
        output : str (optional)
            output filename
        colourmap : str
            colourmap for the plot
        """
        if set_style:
            plt.style.use(set_style)
        p1 = ut.pressure(self.x, temperature)
        p2 = ut.pressure(self.y, temperature)
        temperature_label = str(temperature) + " K"
        levels = ut.get_levels(self.z)
        ticky = ut.get_ticks(self.ticks)
        X1Lab = "$\Delta \mu_{\mathrm{" + self.xlabel + "}}$" + " (eV)"
        Y1Lab = "$\Delta \mu_{\mathrm{" + self.ylabel + "}}$" + " (eV)"
        X2Lab = "$P_" + "{\mathrm{" + self.xlabel + "}}$" + " 298 K (bar)"
        Y2Lab = "$P_" + "{\mathrm{" + self.ylabel + "}}$" + " 298 K (bar)"
        fig = plt.figure(dpi=96, facecolor='#eeeeee', tight_layout=1)
        ax = fig.add_subplot(121)
        gs = gridspec.GridSpec(1, 2, width_ratios=[.95, .05])
        ax, axR = plt.subplot(gs[0]), plt.subplot(gs[1])
        CM = ax.contourf(self.x, self.y, self.z, levels=levels, cmap=colourmap)
        ax.set_xlabel(X1Lab, fontsize=14)
        ax.set_ylabel(Y1Lab, fontsize=14)
        ax2 = ax.twinx()
        ax2.set_ylim(p2[0], p2[-1])
        ax2.set_ylabel(Y2Lab, fontsize=13)
        ax3 = ax.twiny()
        ax3.set_xlim(p1[0], p1[-1])
        ax3.set_xlabel(X2Lab, fontsize=12)
        ax.tick_params(labelsize=10)
        ax2.tick_params(labelsize=10)
        ax3.tick_params(labelsize=10)
        ax.text(0.13, 0.95, temperature_label,  fontsize=15, color="white",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes)
        cbar = fig.colorbar(CM, extend='both', cax=axR, ticks=ticky)
        cbar.ax.set_yticklabels(self.labels)
        axR.set_xlabel('$H_2O$ $nm^{-2}$', fontsize=12)
        plt.savefig(output, dpi=600)
        plt.show()

    def plot_pressure(self, temperature, output="phase.png", colourmap="viridis",
                      set_style="default"):
        """ Plots a phase diagram as a function of pressure.

        Parameters
        ----------
        temperature : int (optional)
            temperature
        output : str (optional)
            output filename
        colourmap : str
            colourmap for the plot
        """
        if set_style:
            plt.style.use(set_style)
        p1 = ut.pressure(self.x, temperature)
        p2 = ut.pressure(self.y, temperature)
        temperature_label = str(temperature) + " K"
        levels = ut.get_levels(self.z)
        ticky = ut.get_ticks(self.ticks)
        XLab = "$P_" + "{\mathrm{" + self.xlabel + "}}$" + " 298 K (bar)"
        YLab = "$P_" + "{\mathrm{" + self.ylabel + "}}$" + " 298 K (bar)"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        CM = ax.contourf(p1, p2, self.z, levels=levels, cmap=colourmap)
        ax.set_ylabel(YLab, fontsize=14)
        ax.set_xlabel(XLab, fontsize=14)
        ax.text(0.1, 0.95, temperature_label,  fontsize=15, color="white",
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes)
        ax.tick_params(labelsize=12)
        cbar = fig.colorbar(CM, ticks=ticky, pad=0.1)
        cbar.ax.set_yticklabels(self.labels)
        plt.tight_layout()
        plt.savefig(output, dpi=600)
        plt.show()
