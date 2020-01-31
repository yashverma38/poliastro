.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_catch_that_asteroid.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_catch_that_asteroid.py:


Catch that asteroid!
====================

First, we need to increase the timeout time to allow the download of
data occur properly



.. code-block:: default


    from astropy.utils.data import conf
    conf.dataurl
    print(conf.dataurl)

    conf.remote_timeout 
    print(conf.remote_timeout)

    conf.remote_timeout = 10000






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    http://data.astropy.org/
    10.0




Then, we do the rest of the imports and create our initial orbits.



.. code-block:: default


    from astropy import units as u
    import matplotlib.pyplot as plt
    from astropy.time import Time
    from astropy.coordinates import solar_system_ephemeris
    import astropy.coordinates as coord
    from astropy.coordinates import (
        GCRS,
        ICRS,
        CartesianDifferential,
        CartesianRepresentation,
        get_body_barycentric,
        get_body_barycentric_posvel,
    )
    solar_system_ephemeris.set("jpl")

    from poliastro.bodies import *
    from poliastro.twobody import Orbit
    from poliastro.plotting import StaticOrbitPlotter
    from poliastro.plotting.misc import plot_solar_system

    EPOCH = Time("2017-09-01 12:05:50", scale="tdb")

    earth = Orbit.from_body_ephem(Earth, EPOCH)
    print(earth)

    earth.plot(label=Earth);
    plt.show()

    florence = Orbit.from_sbdb("Florence")
    print(florence)





.. image:: /auto_examples/images/sphx_glr_plot_catch_that_asteroid_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    1 x 1 AU x 23.4 deg (ICRS) orbit around Sun (☉) at epoch 2017-09-01 12:05:50.000 (TDB)
    /home/lobo/Git/poliastro/docs/source/examples/plot_catch_that_asteroid.py:53: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.

    1 x 3 AU x 22.1 deg (HeliocentricEclipticIAU76) orbit around Sun (☉) at epoch 2458600.5008007586 (TDB)




Two problems: the epoch is not the one we desire, and the inclination is
with respect to the ecliptic!



.. code-block:: default


    print(florence.rv())

    print(florence.epoch)

    print(florence.epoch.iso)

    print(florence.inc)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    (<Quantity [-2.76132872e+08, -1.71570015e+08, -1.09377634e+08] km>, <Quantity [13.17478677, -9.82584123, -1.48126637] km / s>)
    2458600.5008007586
    2019-04-27 00:01:09.186
    22.14239422414861 deg




We first propagate:



.. code-block:: default


    florence = florence.propagate(EPOCH)
    print(florence.epoch.tdb.iso)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    2017-09-01 12:05:50.000




And now we have to convert to the same frame that the planetary
ephemerides are using to make consistent comparisons, which is ICRS:



.. code-block:: default


    def to_icrs(orbit):
        """Creates a new Orbit object with its coordinates transformed to ICRS.
        Notice that, strictly speaking, the center of ICRS is the Solar System Barycenter
        and not the Sun, and therefore these orbits cannot be propagated in the context
        of the two body problem. Therefore, this function exists merely for practical
        purposes.
        """

        coords = orbit.get_frame().realize_frame(orbit.represent_as(CartesianRepresentation, CartesianDifferential))
        coords.representation_type = CartesianRepresentation
        icrs_cart = coords.transform_to(ICRS).represent_as(CartesianRepresentation, CartesianDifferential)

        # Caution: the attractor is in fact the Solar System Barycenter
        ss = Orbit.from_vectors(
            Sun, r=icrs_cart.xyz, v=icrs_cart.differentials["s"].d_xyz, epoch=orbit.epoch
        )
        ss._frame = ICRS()
        return ss

    florence_icrs = to_icrs(florence)
    print(florence_icrs.rv())






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    (<Quantity [ 1.46404253e+08, -5.35752830e+07, -2.05656912e+07] km>, <Quantity [ 7.34329035, 23.47561546, 24.12063696] km / s>)




Let us compute the distance between Florence and the Earth:



.. code-block:: default


    from poliastro.util import norm

    print(norm(florence_icrs.r - earth.r) - Earth.R)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    6967159.889540502 km




.. raw:: html

   <div class="alert alert-success">

This value is consistent with what ESA says! :math:`7\,060\,160` km

.. raw:: html

   </div>



.. code-block:: default


    abs(((norm(florence_icrs.r - earth.r) - Earth.R) - 7060160 * u.km) / (7060160 * u.km))

    from IPython.display import HTML

    HTML(
    """<blockquote class="twitter-tweet" data-lang="en"><p lang="es" dir="ltr">La <a href="https://twitter.com/esa_es">@esa_es</a> ha preparado un resumen del asteroide <a href="https://twitter.com/hashtag/Florence?src=hash">#Florence</a> 😍 <a href="https://t.co/Sk1lb7Kz0j">pic.twitter.com/Sk1lb7Kz0j</a></p>&mdash; AeroPython (@AeroPython) <a href="https://twitter.com/AeroPython/status/903197147914543105">August 31, 2017</a></blockquote>
    <script src="//platform.twitter.com/widgets.js" charset="utf-8"></script>"""
    )







.. only:: builder_html

    .. raw:: html

        <blockquote class="twitter-tweet" data-lang="en"><p lang="es" dir="ltr">La <a href="https://twitter.com/esa_es">@esa_es</a> ha preparado un resumen del asteroide <a href="https://twitter.com/hashtag/Florence?src=hash">#Florence</a> 😍 <a href="https://t.co/Sk1lb7Kz0j">pic.twitter.com/Sk1lb7Kz0j</a></p>&mdash; AeroPython (@AeroPython) <a href="https://twitter.com/AeroPython/status/903197147914543105">August 31, 2017</a></blockquote>
        <script src="//platform.twitter.com/widgets.js" charset="utf-8"></script>
        <br />
        <br />

And now we can plot!



.. code-block:: default


    frame = plot_solar_system(outer=False, epoch=EPOCH)
    frame.plot(florence_icrs, label="Florence");
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_catch_that_asteroid_002.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/Git/poliastro/docs/source/examples/plot_catch_that_asteroid.py:146: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





The difference between doing it well and doing it wrong is clearly
visible:



.. code-block:: default


    frame = StaticOrbitPlotter()

    frame.plot(earth, label="Earth")

    frame.plot(florence, label="Florence (Ecliptic)")
    frame.plot(florence_icrs, label="Florence (ICRS)");
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_catch_that_asteroid_003.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/Git/poliastro/docs/source/examples/plot_catch_that_asteroid.py:160: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





We can express Florence's orbit as viewed from Earth. In order to do
that, we must set the Earth as the new attractor by making use of the
``change_attractor()`` method. However Florence is out of Earth's SOI,
meaning that changing the attractor from Sun to Earth has no physical
sense. We will make use of ``force=True`` argument so this method runs
even if we know that we are out of new attractor's SOI.



.. code-block:: default


    florence_hyper = florence.change_attractor(Earth, force=True)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/twobody/orbit.py:503: PatchedConicsWarning:

    Leaving the SOI of the current attractor





Previous warning was raised since Florence's orbit as seen from Earth is
hyperbolic. Therefore if user wants to propagate this orbit along time,
there will be some point at which the asteroid is out of Earth's
influence (if not already).


We now retrieve the ephemerides of the Moon, which are given directly in
GCRS:



.. code-block:: default


    moon = Orbit.from_body_ephem(Moon, EPOCH)
    print(moon)

    moon.plot(label=Moon);
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_catch_that_asteroid_004.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    367937 x 405209 km x 19.4 deg (GCRS) orbit around Earth (♁) at epoch 2017-09-01 12:05:50.000 (TDB)
    /home/lobo/Git/poliastro/docs/source/examples/plot_catch_that_asteroid.py:192: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





And now for the final plot:



.. code-block:: default


    import matplotlib.pyplot as plt

    frame = StaticOrbitPlotter()

    # This first plot sets the frame
    frame.plot(florence_hyper, label="Florence")

    # And then we add the Moon
    frame.plot(moon, label=Moon)

    plt.xlim(-1000000, 8000000)
    plt.ylim(-5000000, 5000000)

    plt.gcf().autofmt_xdate()
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_catch_that_asteroid_005.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/twobody/orbit.py:1212: OrbitSamplingWarning:

    anomaly outside range, clipping

    /home/lobo/Git/poliastro/docs/source/examples/plot_catch_that_asteroid.py:213: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





.. raw:: html

   <div style="text-align: center; font-size: 3em;">

Per Python ad astra!

.. raw:: html

   </div>



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  1.276 seconds)


.. _sphx_glr_download_auto_examples_plot_catch_that_asteroid.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_catch_that_asteroid.py <plot_catch_that_asteroid.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_catch_that_asteroid.ipynb <plot_catch_that_asteroid.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
