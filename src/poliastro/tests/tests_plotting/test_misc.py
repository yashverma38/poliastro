import pytest

from poliastro.constants import J2000
from poliastro.plotting import OrbitPlotter2D, OrbitPlotter3D
from poliastro.plotting.misc import plot_solar_system

import matplotlib.pyplot as plt

@pytest.mark.parametrize("outer,expected", [(True, 8), (False, 4)])
def test_plot_solar_system_has_expected_number_of_orbits(outer, expected):
    assert len(plot_solar_system(outer).trajectories) == expected


@pytest.mark.parametrize(
    "use_3d, plotter_class", [(True, OrbitPlotter3D), (False, OrbitPlotter2D)]
)
def test_plot_solar_system_uses_expected_orbitplotter(use_3d, plotter_class):
    assert isinstance(plot_solar_system(use_3d=use_3d, interactive=True), plotter_class)

@pytest.mark.mpl_image_compare
def test_plot_solar_system_inner():
    fig, ax = plt.subplots()
    plot_solar_system(outer=False, epoch=J2000, ax=ax)

    return fig

@pytest.mark.mpl_image_compare
def test_plot_solar_system_outer():
    fig, ax = plt.subplots()
    plot_solar_system(outer=True, epoch=J2000, ax=ax)

    return fig

@pytest.mark.mpl_image_compare
def test_plot_solar_system_dark():
    fig, ax = plt.subplots()
    plot_solar_system(outer=False, epoch=J2000, ax=ax, dark=True)

    return fig
