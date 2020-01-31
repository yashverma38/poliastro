.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_plot_propagation_using_Cowells_formulation.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_plot_propagation_using_Cowells_formulation.py:


Cowell's formulation
====================

For cases where we only study the gravitational forces, solving the
Kepler's equation is enough to propagate the orbit forward in time.
However, when we want to take perturbations that deviate from Keplerian
forces into account, we need a more complex method to solve our initial
value problem: one of them is **Cowell's formulation**.

In this formulation we write the two body differential equation
separating the Keplerian and the perturbation accelerations:

.. math:: \ddot{\mathbb{r}} = -rac{\mu}{|\mathbb{r}|^3} \mathbb{r} + \mathbb{a}_d

.. raw:: html

   <div class="alert alert-info">

For an in-depth exploration of this topic, still to be integrated in
poliastro, check out this Master thesis

.. raw:: html

   </div>


.. raw:: html

   <div class="alert alert-info">

An earlier version of this notebook allowed for more flexibility and
interactivity, but was considerably more complex. Future versions of
poliastro and plotly might bring back part of that functionality,
depending on user feedback. You can still download the older version
here.

.. raw:: html

   </div>


First example
-------------

Let's setup a very simple example with constant acceleration to
visualize the effects on the orbit.



.. code-block:: default


    import numpy as np
    from astropy import units as u
    from astropy import time
    import matplotlib.pyplot as plt
    import plotly

    from poliastro.bodies import Earth
    from poliastro.twobody import Orbit
    from poliastro.twobody.propagation import propagate
    from poliastro.examples import iss

    from poliastro.twobody.propagation import cowell
    from poliastro.plotting import OrbitPlotter3D
    from poliastro.util import norm










To provide an acceleration depending on an extra parameter, we can use
**closures** like this one:



.. code-block:: default


    accel = 2e-5

    def constant_accel_factory(accel):
        def constant_accel(t0, u, k):
            v = u[3:]
            norm_v = (v[0]**2 + v[1]**2 + v[2]**2)**.5
            return accel * v / norm_v

        return constant_accel

    times = np.linspace(0, 10 * iss.period, 500)
    print(times)

    positions = propagate(
        iss,
        time.TimeDelta(times),
        method=cowell,
        rtol=1e-11,
        ad=constant_accel_factory(accel),
    )






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [    0.           111.36211826   222.72423652   334.08635478
       445.44847304   556.8105913    668.17270956   779.53482782
       890.89694608  1002.25906434  1113.6211826   1224.98330086
      1336.34541912  1447.70753738  1559.06965564  1670.4317739
      1781.79389216  1893.15601042  2004.51812868  2115.88024694
      2227.2423652   2338.60448346  2449.96660172  2561.32871997
      2672.69083823  2784.05295649  2895.41507475  3006.77719301
      3118.13931127  3229.50142953  3340.86354779  3452.22566605
      3563.58778431  3674.94990257  3786.31202083  3897.67413909
      4009.03625735  4120.39837561  4231.76049387  4343.12261213
      4454.48473039  4565.84684865  4677.20896691  4788.57108517
      4899.93320343  5011.29532169  5122.65743995  5234.01955821
      5345.38167647  5456.74379473  5568.10591299  5679.46803125
      5790.83014951  5902.19226777  6013.55438603  6124.91650429
      6236.27862255  6347.64074081  6459.00285907  6570.36497733
      6681.72709559  6793.08921385  6904.45133211  7015.81345037
      7127.17556863  7238.53768689  7349.89980515  7461.26192341
      7572.62404167  7683.98615992  7795.34827818  7906.71039644
      8018.0725147   8129.43463296  8240.79675122  8352.15886948
      8463.52098774  8574.883106    8686.24522426  8797.60734252
      8908.96946078  9020.33157904  9131.6936973   9243.05581556
      9354.41793382  9465.78005208  9577.14217034  9688.5042886
      9799.86640686  9911.22852512 10022.59064338 10133.95276164
     10245.3148799  10356.67699816 10468.03911642 10579.40123468
     10690.76335294 10802.1254712  10913.48758946 11024.84970772
     11136.21182598 11247.57394424 11358.9360625  11470.29818076
     11581.66029902 11693.02241728 11804.38453554 11915.7466538
     12027.10877206 12138.47089032 12249.83300858 12361.19512684
     12472.5572451  12583.91936336 12695.28148161 12806.64359987
     12918.00571813 13029.36783639 13140.72995465 13252.09207291
     13363.45419117 13474.81630943 13586.17842769 13697.54054595
     13808.90266421 13920.26478247 14031.62690073 14142.98901899
     14254.35113725 14365.71325551 14477.07537377 14588.43749203
     14699.79961029 14811.16172855 14922.52384681 15033.88596507
     15145.24808333 15256.61020159 15367.97231985 15479.33443811
     15590.69655637 15702.05867463 15813.42079289 15924.78291115
     16036.14502941 16147.50714767 16258.86926593 16370.23138419
     16481.59350245 16592.95562071 16704.31773897 16815.67985723
     16927.04197549 17038.40409375 17149.76621201 17261.12833027
     17372.49044853 17483.85256679 17595.21468505 17706.57680331
     17817.93892156 17929.30103982 18040.66315808 18152.02527634
     18263.3873946  18374.74951286 18486.11163112 18597.47374938
     18708.83586764 18820.1979859  18931.56010416 19042.92222242
     19154.28434068 19265.64645894 19377.0085772  19488.37069546
     19599.73281372 19711.09493198 19822.45705024 19933.8191685
     20045.18128676 20156.54340502 20267.90552328 20379.26764154
     20490.6297598  20601.99187806 20713.35399632 20824.71611458
     20936.07823284 21047.4403511  21158.80246936 21270.16458762
     21381.52670588 21492.88882414 21604.2509424  21715.61306066
     21826.97517892 21938.33729718 22049.69941544 22161.0615337
     22272.42365196 22383.78577022 22495.14788848 22606.51000674
     22717.872125   22829.23424325 22940.59636151 23051.95847977
     23163.32059803 23274.68271629 23386.04483455 23497.40695281
     23608.76907107 23720.13118933 23831.49330759 23942.85542585
     24054.21754411 24165.57966237 24276.94178063 24388.30389889
     24499.66601715 24611.02813541 24722.39025367 24833.75237193
     24945.11449019 25056.47660845 25167.83872671 25279.20084497
     25390.56296323 25501.92508149 25613.28719975 25724.64931801
     25836.01143627 25947.37355453 26058.73567279 26170.09779105
     26281.45990931 26392.82202757 26504.18414583 26615.54626409
     26726.90838235 26838.27050061 26949.63261887 27060.99473713
     27172.35685539 27283.71897365 27395.08109191 27506.44321017
     27617.80532843 27729.16744669 27840.52956494 27951.8916832
     28063.25380146 28174.61591972 28285.97803798 28397.34015624
     28508.7022745  28620.06439276 28731.42651102 28842.78862928
     28954.15074754 29065.5128658  29176.87498406 29288.23710232
     29399.59922058 29510.96133884 29622.3234571  29733.68557536
     29845.04769362 29956.40981188 30067.77193014 30179.1340484
     30290.49616666 30401.85828492 30513.22040318 30624.58252144
     30735.9446397  30847.30675796 30958.66887622 31070.03099448
     31181.39311274 31292.755231   31404.11734926 31515.47946752
     31626.84158578 31738.20370404 31849.5658223  31960.92794056
     32072.29005882 32183.65217708 32295.01429534 32406.3764136
     32517.73853186 32629.10065012 32740.46276838 32851.82488664
     32963.18700489 33074.54912315 33185.91124141 33297.27335967
     33408.63547793 33519.99759619 33631.35971445 33742.72183271
     33854.08395097 33965.44606923 34076.80818749 34188.17030575
     34299.53242401 34410.89454227 34522.25666053 34633.61877879
     34744.98089705 34856.34301531 34967.70513357 35079.06725183
     35190.42937009 35301.79148835 35413.15360661 35524.51572487
     35635.87784313 35747.23996139 35858.60207965 35969.96419791
     36081.32631617 36192.68843443 36304.05055269 36415.41267095
     36526.77478921 36638.13690747 36749.49902573 36860.86114399
     36972.22326225 37083.58538051 37194.94749877 37306.30961703
     37417.67173529 37529.03385355 37640.39597181 37751.75809007
     37863.12020833 37974.48232658 38085.84444484 38197.2065631
     38308.56868136 38419.93079962 38531.29291788 38642.65503614
     38754.0171544  38865.37927266 38976.74139092 39088.10350918
     39199.46562744 39310.8277457  39422.18986396 39533.55198222
     39644.91410048 39756.27621874 39867.638337   39979.00045526
     40090.36257352 40201.72469178 40313.08681004 40424.4489283
     40535.81104656 40647.17316482 40758.53528308 40869.89740134
     40981.2595196  41092.62163786 41203.98375612 41315.34587438
     41426.70799264 41538.0701109  41649.43222916 41760.79434742
     41872.15646568 41983.51858394 42094.8807022  42206.24282046
     42317.60493872 42428.96705698 42540.32917524 42651.6912935
     42763.05341176 42874.41553002 42985.77764828 43097.13976653
     43208.50188479 43319.86400305 43431.22612131 43542.58823957
     43653.95035783 43765.31247609 43876.67459435 43988.03671261
     44099.39883087 44210.76094913 44322.12306739 44433.48518565
     44544.84730391 44656.20942217 44767.57154043 44878.93365869
     44990.29577695 45101.65789521 45213.02001347 45324.38213173
     45435.74424999 45547.10636825 45658.46848651 45769.83060477
     45881.19272303 45992.55484129 46103.91695955 46215.27907781
     46326.64119607 46438.00331433 46549.36543259 46660.72755085
     46772.08966911 46883.45178737 46994.81390563 47106.17602389
     47217.53814215 47328.90026041 47440.26237867 47551.62449693
     47662.98661519 47774.34873345 47885.71085171 47997.07296997
     48108.43508822 48219.79720648 48331.15932474 48442.521443
     48553.88356126 48665.24567952 48776.60779778 48887.96991604
     48999.3320343  49110.69415256 49222.05627082 49333.41838908
     49444.78050734 49556.1426256  49667.50474386 49778.86686212
     49890.22898038 50001.59109864 50112.9532169  50224.31533516
     50335.67745342 50447.03957168 50558.40168994 50669.7638082
     50781.12592646 50892.48804472 51003.85016298 51115.21228124
     51226.5743995  51337.93651776 51449.29863602 51560.66075428
     51672.02287254 51783.3849908  51894.74710906 52006.10922732
     52117.47134558 52228.83346384 52340.1955821  52451.55770036
     52562.91981862 52674.28193688 52785.64405514 52897.0061734
     53008.36829166 53119.73040991 53231.09252817 53342.45464643
     53453.81676469 53565.17888295 53676.54100121 53787.90311947
     53899.26523773 54010.62735599 54121.98947425 54233.35159251
     54344.71371077 54456.07582903 54567.43794729 54678.80006555
     54790.16218381 54901.52430207 55012.88642033 55124.24853859
     55235.61065685 55346.97277511 55458.33489337 55569.69701163] s




And we plot the results:



.. code-block:: default


    frame = OrbitPlotter3D()
    frame.set_attractor(Earth)
    fig = frame.plot_trajectory(positions, label="ISS")
    plotly.io.show(fig)





.. raw:: html
    :file: images/sphx_glr_plot_propagation_using_Cowells_formulation_001.html





Error checking
--------------



.. code-block:: default


    def state_to_vector(ss):
        r, v = ss.rv()
        x, y, z = r.to(u.km).value
        vx, vy, vz = v.to(u.km / u.s).value
        return np.array([x, y, z, vx, vy, vz])

    k = Earth.k.to(u.km ** 3 / u.s ** 2).value

    rtol = 1e-13
    full_periods = 2

    u0 = state_to_vector(iss)
    tf = ((2 * full_periods + 1) * iss.period / 2)

    u0, tf

    iss_f_kep = iss.propagate(tf, rtol=1e-18)

    r, v = cowell(iss.attractor.k, iss.r, iss.v, [tf] * u.s, rtol=rtol)

    iss_f_num = Orbit.from_vectors(Earth, r[0], v[0], iss.epoch + tf)

    iss_f_num.r, iss_f_kep.r

    assert np.allclose(iss_f_num.r, iss_f_kep.r, rtol=rtol, atol=1e-08 * u.km)
    assert np.allclose(iss_f_num.v, iss_f_kep.v, rtol=rtol, atol=1e-08 * u.km / u.s)

    assert np.allclose(iss_f_num.a, iss_f_kep.a, rtol=rtol, atol=1e-08 * u.km)
    assert np.allclose(iss_f_num.ecc, iss_f_kep.ecc, rtol=rtol)
    assert np.allclose(iss_f_num.inc, iss_f_kep.inc, rtol=rtol, atol=1e-08 * u.rad)
    assert np.allclose(iss_f_num.raan, iss_f_kep.raan, rtol=rtol, atol=1e-08 * u.rad)
    assert np.allclose(iss_f_num.argp, iss_f_kep.argp, rtol=rtol, atol=1e-08 * u.rad)
    assert np.allclose(iss_f_num.nu, iss_f_kep.nu, rtol=rtol, atol=1e-08 * u.rad)









Numerical validation
--------------------

According to [Edelbaum, 1961], a coplanar, semimajor axis change with
tangent thrust is defined by:

.. math:: \frac{\operatorname{d}\!a}{a_0} = 2 \frac{F}{m V_0}\operatorname{d}\!t, \qquad \frac{\Delta{V}}{V_0} = \frac{1}{2} \frac{\Delta{a}}{a_0}

So let's create a new circular orbit and perform the necessary checks,
assuming constant mass and thrust (i.e. constant acceleration):



.. code-block:: default


    ss = Orbit.circular(Earth, 500 * u.km)
    tof = 20 * ss.period

    ad = constant_accel_factory(1e-7)

    r, v = cowell(ss.attractor.k, ss.r, ss.v, [tof] * u.s, ad=ad)

    ss_final = Orbit.from_vectors(Earth, r[0], v[0], ss.epoch + tof)

    da_a0 = (ss_final.a - ss.a) / ss.a
    da_a0

    dv_v0 = abs(norm(ss_final.v) - norm(ss.v)) / norm(ss.v)
    2 * dv_v0

    np.allclose(da_a0, 2 * dv_v0, rtol=1e-2)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    True



This means **we successfully validated the model against an extremely
simple orbit transfer with approximate analytical solution**. Notice
that the final eccentricity, as originally noticed by Edelbaum, is
nonzero:



.. code-block:: default


    print(ss_final.ecc)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    6.662142719219677e-06




References
----------

-  [Edelbaum, 1961] "Propulsion requirements for controllable
   satellites"



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  3.088 seconds)


.. _sphx_glr_download_auto_examples_plot_propagation_using_Cowells_formulation.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: plot_propagation_using_Cowells_formulation.py <plot_propagation_using_Cowells_formulation.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: plot_propagation_using_Cowells_formulation.ipynb <plot_propagation_using_Cowells_formulation.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
