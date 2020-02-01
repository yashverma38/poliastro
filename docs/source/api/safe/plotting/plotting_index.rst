Plotting module
===============

The :py:mod:`poliastro.plotting` contains a set of submodules in which the
basic classes and functions afor plotting orbit objects are described. This
module contains the following submodules:

.. graphviz::

   digraph {
      "poliastro.plotting" -> "core", "misc", "porkchop", "static", "util";
   }

How to use the plotting module
------------------------------

The package has two kind of plotters: static and interactive ones. While the
first ones are based on `matplotlib` the others rely on `plotly`. Although
poliastro is expected to be used on Jupiter Notebook it is possible to use some
IDE such us Spyder, PyCharm...

* If you are using a Pyhton script, make sure you are always showing your
  figures by setting `plt.show()` or `plotly.io.show(fig)`

* For the case of using Spyder make sure you have installed the `orca` package
  and select manually the render as explained in `here`_.
  
  .. _`here`: https://github.com/poliastro/poliastro/issues/710#issuecomment-511219029

.. toctree::
    :hidden:
    :maxdepth: 1

    core
    misc
    porkchop
    static
    util
