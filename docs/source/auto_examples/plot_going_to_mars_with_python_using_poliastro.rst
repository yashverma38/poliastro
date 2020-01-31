.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_going_to_mars_with_python_using_poliastro.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_going_to_mars_with_python_using_poliastro.py:


Going to Mars with Python using poliastro
=========================================

This is an example on how to use
`poliastro <https://github.com/poliastro/poliastro>`__, a little library
I've been working on to use in my Astrodynamics lessons. It features
conversion between **classical orbital elements** and position vectors,
propagation of **Keplerian orbits**, initial orbit determination using
the solution of the **Lambert's problem** and **orbit plotting**.

In this example we're going to draw the trajectory of the mission `Mars
Science Laboratory (MSL) <http://mars.jpl.nasa.gov/msl/>`__, which
carried the rover Curiosity to the surface of Mars in a period of
something less than 9 months.

**Note**: This is a very simplistic analysis which doesn't take into
account many important factors of the mission, but can serve as an
starting point for more serious computations (and as a side effect
produces a beautiful plot at the end).

First of all, we import the necessary modules. Apart from poliastro we
will make use of astropy to deal with physical units and time
definitions and jplephem to compute the positions and velocities of the
planets.



.. code-block:: default


    import numpy as np

    import astropy.units as u
    import matplotlib.pyplot as plt
    from astropy import time

    from poliastro import iod
    from poliastro.bodies import Earth, Mars, Sun
    from poliastro.twobody import Orbit
    from poliastro.maneuver import Maneuver

    import plotly









We need a binary file from NASA called *SPICE kernel* to compute the
position and velocities of the planets. Astropy downloads it for us:



.. code-block:: default


    from astropy.coordinates import solar_system_ephemeris
    solar_system_ephemeris.set("jpl")






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    <ScienceState solar_system_ephemeris: 'jpl'>



The initial data was gathered from Wikipedia: the date of the launch was
on **November 26, 2011 at 15:02 UTC** and landing was on **August 6,
2012 at 05:17 UTC**. We compute then the time of flight, which is
exactly what it sounds.



.. code-block:: default


    # Initial data
    date_launch = time.Time("2011-11-26 15:02", scale="utc")
    date_arrival = time.Time("2012-08-06 05:17", scale="utc")









To compute the transfer orbit, we have the useful function ``lambert`` :
according to a theorem with the same name, *the transfer orbit between
two points in space only depends on those two points and the time it
takes to go from one to the other*. We could make use of the raw
algorithms available in ``poliastro.iod`` for solving this but working
with the ``poliastro.maneuvers`` is even easier!

We just need to create the orbits for each one of the planets at the
specific departure and arrival dates.



.. code-block:: default


    # Solve for departure and target orbits
    ss_earth = Orbit.from_body_ephem(Earth, date_launch)
    ss_mars = Orbit.from_body_ephem(Mars, date_arrival)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/twobody/orbit.py:418: TimeScaleWarning:

    Input time was converted to scale='tdb' with value 2011-11-26 15:03:06.183. Use Time(..., scale='tdb') instead.

    /home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/twobody/orbit.py:418: TimeScaleWarning:

    Input time was converted to scale='tdb' with value 2012-08-06 05:18:07.183. Use Time(..., scale='tdb') instead.





We can now solve for the maneuver that will take us from Earth to Mars.
After solving it, we just need to apply it to the departure orbit to
solve for the transfer one.



.. code-block:: default


    # Solve for the transfer maneuver
    man_lambert = Maneuver.lambert(ss_earth, ss_mars)

    # Get the transfer and final orbits
    ss_trans, ss_target = ss_earth.apply_maneuver(man_lambert, intermediate=True)









Let's plot this transfer orbit in 3D!



.. code-block:: default


    from poliastro.plotting import OrbitPlotter3D

    plotter = OrbitPlotter3D()
    plotter.plot(ss_earth, label="Earth at launch position", color="navy")
    plotter.plot(ss_mars, label="Mars at arrival position", color="red")
    plotter.plot_trajectory(ss_trans.sample(max_anomaly=180*u.deg), color="black", label="Transfer orbit")
    fig = plotter.set_view(30 * u.deg, 260 * u.deg, distance=3 * u.km)
    plotly.io.show(fig)





.. raw:: html
    :file: images/sphx_glr_plot_going_to_mars_with_python_using_poliastro_001.html





Not bad! Let's celebrate with some music!



.. code-block:: default


    from IPython.display import YouTubeVideo
    YouTubeVideo('zSgiXGELjbc')





.. only:: builder_html

    .. raw:: html


                <iframe
                    width="400"
                    height="300"
                    src="https://www.youtube.com/embed/zSgiXGELjbc"
                    frameborder="0"
                    allowfullscreen
                ></iframe>
        
        <br />
        <br />


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  2.326 seconds)


.. _sphx_glr_download_auto_examples_plot_going_to_mars_with_python_using_poliastro.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_going_to_mars_with_python_using_poliastro.py <plot_going_to_mars_with_python_using_poliastro.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_going_to_mars_with_python_using_poliastro.ipynb <plot_going_to_mars_with_python_using_poliastro.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
