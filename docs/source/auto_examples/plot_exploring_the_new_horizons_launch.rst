.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_exploring_the_new_horizons_launch.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_exploring_the_new_horizons_launch.py:


New Horizons launch and trajectory
==================================

Main data source: Guo & Farquhar "New Horizons Mission Design"
http://www.boulder.swri.edu/pkb/ssr/ssr-mission-design.pdf


.. code-block:: default


    from astropy import time
    from astropy import units as u
    import matplotlib.pyplot as plt

    from poliastro.bodies import Sun, Earth, Jupiter
    from poliastro.twobody import Orbit
    from poliastro.plotting import StaticOrbitPlotter
    from poliastro import iod
    from poliastro.util import norm









Parking orbit
-------------

Quoting from "New Horizons Mission Design":

    It was first inserted into an elliptical Earth parking orbit of
    **perigee altitude 165 km** and **apogee altitude 215 km**.
    [Emphasis mine]



.. code-block:: default


    r_p = Earth.R + 165 * u.km
    r_a = Earth.R + 215 * u.km

    a_parking = (r_p + r_a) / 2
    ecc_parking = 1 - r_p / a_parking

    parking = Orbit.from_classical(
        Earth,
        a_parking,
        ecc_parking,
        0 * u.deg,
        0 * u.deg,
        0 * u.deg,
        0 * u.deg,  # We don't mind
        time.Time("2006-01-19", scale="utc"),
    )

    print(parking.v)
    parking.plot();
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_exploring_the_new_horizons_launch_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [0.         7.81989358 0.        ] km / s
    /home/lobo/Git/poliastro/docs/source/examples/plot_exploring_the_new_horizons_launch.py:51: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





Hyperbolic exit
---------------

Hyperbolic excess velocity:

.. math::  v_{\infty}^2 = \frac{\mu}{-a} = 2 \varepsilon = C_3 

Relation between orbital velocity :math:`v`, local escape velocity
:math:`v_e` and hyperbolic excess velocity :math:`v_{\infty}`:

.. math::  v^2 = v_e^2 + v_{\infty}^2 

Option a): Insert :math:`C_3` from report, check :math:`v_e` at parking perigee
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: default


    C_3_A = 157.6561 * u.km ** 2 / u.s ** 2  # Designed

    a_exit = -(Earth.k / C_3_A).to(u.km)
    ecc_exit = 1 - r_p / a_exit

    exit = Orbit.from_classical(
        Earth,
        a_exit,
        ecc_exit,
        0 * u.deg,
        0 * u.deg,
        0 * u.deg,
        0 * u.deg,  # We don't mind
        time.Time("2006-01-19", scale="utc"),
    )

    print(norm(exit.v).to(u.km / u.s))






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    16.71806884482923 km / s




Quoting "New Horizons Mission Design":

    After a short coast in the parking orbit, the spacecraft was then
    injected into the desired heliocentric orbit by the Centaur second
    stage and Star 48B third stage. At the Star 48B burnout, the New
    Horizons spacecraft reached the highest Earth departure speed,
    **estimated at 16.2 km/s**, becoming the fastest spacecraft ever
    launched from Earth. [Emphasis mine]



.. code-block:: default


    v_estimated = 16.2 * u.km / u.s

    print(
        "Relative error of {:.2f} %".format(
            (norm(exit.v) - v_estimated) / v_estimated * 100
        )
    )






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Relative error of 3.20 %




So it stays within the same order of magnitude. Which is reasonable,
because real life burns are not instantaneous.



.. code-block:: default



    fig, ax = plt.subplots(figsize=(8, 8))
    op = StaticOrbitPlotter(ax=ax)

    op.plot(parking)
    op.plot(exit)

    ax.set_xlim(-8000, 8000)
    ax.set_ylim(-20000, 20000);
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_exploring_the_new_horizons_launch_002.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/Git/poliastro/docs/source/examples/plot_exploring_the_new_horizons_launch.py:124: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





Option b): Compute :math:`v_{\infty}` using the Jupyter flyby
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

According to Wikipedia, the closest approach occurred at 05:43:40 UTC.
We can use this data to compute the solution of the Lambert problem
between the Earth and Jupiter.



.. code-block:: default


    nh_date = time.Time("2006-01-19 19:00", scale="utc")
    nh_flyby_date = time.Time("2007-02-28 05:43:40", scale="utc")
    nh_tof = nh_flyby_date - nh_date

    nh_earth = Orbit.from_body_ephem(Earth, nh_date)
    nh_r_0, v_earth = nh_earth.rv()

    nh_jup = Orbit.from_body_ephem(Jupiter, nh_flyby_date)
    nh_r_f, v_jup = nh_jup.rv()

    (nh_v_0, nh_v_f), = iod.lambert(Sun.k, nh_r_0, nh_r_f, nh_tof)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/twobody/orbit.py:418: TimeScaleWarning:

    Input time was converted to scale='tdb' with value 2006-01-19 19:01:05.184. Use Time(..., scale='tdb') instead.

    /home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/twobody/orbit.py:418: TimeScaleWarning:

    Input time was converted to scale='tdb' with value 2007-02-28 05:44:45.185. Use Time(..., scale='tdb') instead.





The hyperbolic excess velocity is measured with respect to the Earth:



.. code-block:: default


    C_3_lambert = (norm(nh_v_0 - v_earth)).to(u.km / u.s) ** 2
    print(C_3_lambert)

    print("Relative error of {:.2f} %".format((C_3_lambert - C_3_A) / C_3_A * 100))






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    158.4752711083674 km2 / s2
    Relative error of 0.52 %




Which again, stays within the same order of magnitude of the figure
given to the Guo & Farquhar report.


From Earth to Jupiter
---------------------



.. code-block:: default


    nh = Orbit.from_vectors(Sun, nh_r_0.to(u.km), nh_v_0.to(u.km / u.s), nh_date)

    op = StaticOrbitPlotter()

    op.plot(nh_jup, label=Jupiter)
    op.plot(nh_earth, label=Earth)
    op.plot(nh, label="New Horizons");
    plt.show()




.. image:: /auto_examples/images/sphx_glr_plot_exploring_the_new_horizons_launch_003.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/Git/poliastro/docs/source/examples/plot_exploring_the_new_horizons_launch.py:177: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.






.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.562 seconds)


.. _sphx_glr_download_auto_examples_plot_exploring_the_new_horizons_launch.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_exploring_the_new_horizons_launch.py <plot_exploring_the_new_horizons_launch.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_exploring_the_new_horizons_launch.ipynb <plot_exploring_the_new_horizons_launch.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
