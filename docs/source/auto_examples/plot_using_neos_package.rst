.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_using_neos_package.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_using_neos_package.py:


Analyzing NEOs
==============

NEO stands for near-Earth object. The Center for NEO Studies
(`CNEOS <http://cneos.jpl.nasa.gov/>`__) defines NEOs as comets and
asteroids that have been nudged by the gravitational attraction of
nearby planets into orbits that allow them to enter the Earth’s
neighborhood.

And what does "near" exactly mean? In terms of orbital elements,
asteroids and comets can be considered NEOs if their perihelion (orbit
point which is nearest to the Sun) is less than 1.3 au = 1.945 \* 108 km
from the Sun.



.. code-block:: default


    from astropy import time
    import matplotlib.pyplot as plt

    from poliastro.twobody.orbit import Orbit
    from poliastro.bodies import Earth
    from poliastro.plotting import StaticOrbitPlotter









Small Body Database (SBDB)
--------------------------



.. code-block:: default


    eros = Orbit.from_sbdb("Eros")
    eros.plot(label="Eros");
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_using_neos_package_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/Git/poliastro/docs/source/examples/plot_using_neos_package.py:36: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





You can also search by IAU number or SPK-ID (there is a faster
``neows.orbit_from_spk_id()`` function in that case, although):



.. code-block:: default


    ganymed = Orbit.from_sbdb("1036")  # Ganymed IAU number
    amor = Orbit.from_sbdb("2001221")  # Amor SPK-ID
    eros = Orbit.from_sbdb("2000433")  # Eros SPK-ID

    # Following comment sets this image as thumbail for gallery examples
    # sphinx_gallery_thumbnail_number = 2
    frame = StaticOrbitPlotter()
    frame.plot(ganymed, label="Ganymed")
    frame.plot(amor, label="Amor")
    frame.plot(eros, label="Eros");
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_using_neos_package_002.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/Git/poliastro/docs/source/examples/plot_using_neos_package.py:54: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





You can use the wildcards from that browser: ``*`` and ``?``.


.. raw:: html

   <div class="alert alert-info">

Keep it in mind that ``from_sbdb()`` can only return one Orbit, so if
several objects are found with that name, it will raise an error with
the different bodies.

.. raw:: html

   </div>



.. code-block:: default


    try:
        Orbit.from_sbdb("*alley")
    except ValueError:
        print("There exist several objects with that name")






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    There exist several objects with that name




.. raw:: html

   <div class="alert alert-info">

Note that epoch is provided by the service itself, so if you need orbit
on another epoch, you have to propagate it:

.. raw:: html

   </div>



.. code-block:: default


    print("Eros epoch: ", eros.epoch.iso)

    epoch = time.Time(2458000.0, scale="tdb", format="jd")
    eros_november = eros.propagate(epoch)
    print("Eros November epoch: ", eros_november.epoch.iso)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Eros epoch:  2019-04-27 00:01:09.186
    Eros November epoch:  2017-09-03 12:00:00.000




DASTCOM5 module
---------------

This module can also be used to get NEOs orbit, in the same way that
``neows``, but it have some advantages (and some disadvantages).

It relies on DASTCOM5 database, a NASA/JPL maintained asteroid and comet
database. This database has to be downloaded at least once in order to
use this module. According to its README, it is updated typically a
couple times per day, but potentially as frequently as once per hour, so
you can download it whenever you want the more recently discovered
bodies. This also means that, after downloading the file, you can use
the database offline.

The file is a ~230 MB zip that you can manually
`download <ftp://ssd.jpl.nasa.gov/pub/ssd/dastcom5.zip>`__ and unzip in
``~/.poliastro`` or, more easily, you can use

.. code:: python

    dastcom5.download_dastcom5()


The main DASTCOM5 advantage over NeoWs is that you can use it to search
not only NEOs, but any asteroid or comet. The easiest function is
``orbit_from_name()``:



.. code-block:: default


    from poliastro.neos import dastcom5

    atira = dastcom5.orbit_from_name("atira")[0]  # NEO
    wikipedia = dastcom5.orbit_from_name("wikipedia")[0]  # Asteroid, but not NEO.

    frame = StaticOrbitPlotter()
    frame.plot(atira, label="Atira (NEO)")
    frame.plot(wikipedia, label="Wikipedia (asteroid)");
    plt.show()





.. image:: /auto_examples/images/sphx_glr_plot_using_neos_package_003.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/lobo/Git/poliastro/docs/source/examples/plot_using_neos_package.py:141: UserWarning:

    Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.





Keep in mind that this function returns a list of orbits matching your
string. This is made on purpose given that there are comets which have
several records in the database (one for each orbit determination in
history) what allow plots like this one:



.. code-block:: default


    halleys = dastcom5.orbit_from_name("1P")
    print("THIS IS HALLEYS LIST:", halleys)

    frame = StaticOrbitPlotter()
    frame.plot(halleys[0], label="Halley")
    frame.plot(halleys[5], label="Halley")
    frame.plot(halleys[10], label="Halley")
    frame.plot(halleys[20], label="Halley")
    frame.plot(halleys[-1], label="Halley");
    plt.show()





.. code-block:: pytb

    Traceback (most recent call last):
      File "/home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/sphinx_gallery/gen_rst.py", line 440, in _memory_usage
        out = func()
      File "/home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/sphinx_gallery/gen_rst.py", line 425, in __call__
        exec(self.code, self.globals)
      File "/home/lobo/Git/poliastro/docs/source/examples/plot_using_neos_package.py", line 151, in <module>
        halleys = dastcom5.orbit_from_name("1P")
      File "/home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/neos/dastcom5.py", line 341, in orbit_from_name
        orbits.append(orbit_from_record(record))
      File "/home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/neos/dastcom5.py", line 361, in orbit_from_record
        body_data = read_record(record)
      File "/home/lobo/anaconda3/envs/poliastro/lib/python3.7/site-packages/poliastro/neos/dastcom5.py", line 510, in read_record
        f.seek(phis_rec, os.SEEK_SET)
    OSError: [Errno 22] Invalid argument




While ``neows`` can only be used to get Orbit objects, ``dastcom5`` can
also provide asteroid and comet complete database. Once you have this,
you can get specific data about one or more bodies. The complete
databases are ``ndarrays``, so if you want to know the entire list of
available parameters, you can look at the ``dtype``, and they are also
explained in `documentation API
Reference <https://docs.poliastro.space/en/latest/api/safe/neos/dastcom5_parameters.html>`__:



.. code-block:: default


    ast_db = dastcom5.asteroid_db()
    comet_db = dastcom5.comet_db()
    ast_db.dtype.names[
        :20
    ]  # They are more than 100, but that would be too much lines in this notebook :P



.. raw:: html

   <div class="alert alert-info">

Asteroid and comet parameters are not exactly the same (although they
are very close)

.. raw:: html

   </div>


With these ``ndarrays`` you can classify asteroids and comets, sort
them, get all their parameters, and whatever comes to your mind.

For example, NEOs can be grouped in several ways. One of the NEOs group
is called ``Atiras``, and is formed by NEOs whose orbits are contained
entirely with the orbit of the Earth. They are a really little group,
and we can try to plot all of these NEOs using ``asteroid_db()``:


Talking in orbital terms, ``Atiras`` have an aphelion distance,
``Q < 0.983 au`` and a semi-major axis, ``a < 1.0 au``. Visiting
`documentation API
Reference <https://docs.poliastro.space/en/latest/api/safe/neos/dastcom5_parameters.html>`__,
you can see that DASTCOM5 provides semi-major axis, but doesn't provide
aphelion distance. You can get aphelion distance easily knowing
perihelion distance (q, QR in DASTCOM5) and semi-major axis
``Q = 2*a - q``, but there are probably many other ways.



.. code-block:: default


    aphelion_condition = 2 * ast_db["A"] - ast_db["QR"] < 0.983
    axis_condition = ast_db["A"] < 1.3
    atiras = ast_db[aphelion_condition & axis_condition]



The number of ``Atira NEOs`` we use using this method is:



.. code-block:: default


    print(len(atiras))



Which is consistent with the `stats published by
CNEOS <https://cneos.jpl.nasa.gov/stats/totals.html>`__


Now we're gonna plot all of their orbits, with corresponding labels,
just because we love plots :)

We only need to get the 16 orbits from these 16 ``ndarrays``.

There are two ways:

-  Gather all their orbital elements manually and use the
   ``Orbit.from_classical()`` function.
-  Use the ``NO`` property (logical record number in DASTCOM5 database)
   and the ``dastcom5.orbit_from_record()`` function.

The second one seems easier and it is related to the current notebook,
so we are going to use that one, using the ``ASTNAM`` property of
DASTCOM5 database:



.. code-block:: default


    from poliastro.bodies import Earth

    earth = Orbit.from_body_ephem(Earth)
    frame = StaticOrbitPlotter()
    frame.plot(earth, label=Earth)

    for record in atiras["NO"]:
        ss = dastcom5.orbit_from_record(record).to_icrs()
        frame.plot(ss, color="#666666")
    plt.show()



If we needed also the names of each asteroid, we could do:



.. code-block:: default


    frame = StaticOrbitPlotter()

    frame.plot(earth, label=Earth)

    for i in range(len(atiras)):
        record = atiras["NO"][i]
        label = atiras["ASTNAM"][i].decode().strip()  # DASTCOM5 strings are binary
        ss = dastcom5.orbit_from_record(record).to_icrs()
        frame.plot(ss, label=label)
    plt.show()



.. raw:: html

   <div class="alert alert-info">

We knew beforehand that there are no ``Atira`` comets, only asteroids
(comet orbits are usually more eccentric), but we could use the same
method with ``com_db`` if we wanted.

.. raw:: html

   </div>


Finally, another interesting function in ``dastcom5`` is
``entire_db()``, which is really similar to ``ast_db`` and ``com_db``,
but it returns a ``Pandas dataframe`` instead of a ``numpy ndarray``.
The dataframe has asteroids and comets in it, but in order to achieve
that (and a more manageable dataframe), a lot of parameters were
removed, and others were renamed:



.. code-block:: default


    db = dastcom5.entire_db()
    print(db.columns)



Also, in this function, DASTCOM5 data (specially strings) is ready to
use (decoded and improved strings, etc):



.. code-block:: default


    db[
        db.NAME == "Halley"
    ]  # As you can see, Halley is the name of an asteroid too, did you know that?



Panda offers many functionalities, and can also be used in the same way
as the ``ast_db`` and ``comet_db`` functions:



.. code-block:: default


    aphelion_condition = (2 * db["A"] - db["QR"]) < 0.983
    axis_condition = db["A"] < 1.3
    atiras = db[aphelion_condition & axis_condition]

    print(len(atiras))



What? I said they can be used in the same way!


Dont worry :) If you want to know what's happening here, the only
difference is that we are now working with comets too, and some comets
have a negative semi-major axis!



.. code-block:: default


    print(len(atiras[atiras.A < 0]))



So, rewriting our condition:



.. code-block:: default


    axis_condition = (db["A"] < 1.3) & (db["A"] > 0)
    atiras = db[aphelion_condition & axis_condition]
    print(len(atiras))



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  22.515 seconds)


.. _sphx_glr_download_auto_examples_plot_using_neos_package.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_using_neos_package.py <plot_using_neos_package.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_using_neos_package.ipynb <plot_using_neos_package.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
