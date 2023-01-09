# Finite Volume Method - 2D
That is the result of the project for the computational fluid dynamics discipline in a master's program. The project aimed to model the lid-driven cavity, and the heat conduction on plate problems, using the finite volume method. Due to the limited time, one used Python to implement the numerical solutions. However, they have a relatively good performance. Furthermore, one tried to build the codes to be comprehensible, but for any problem, feel free to contact me (almeriopamplona@gmail.com).

I did some validations that I compiled in these papers: <a href="Reports/LidCavity_AlmerioPamplona.pdf"></a> and <a href="Reports/2DHeatTransfer_AlmerioPamplona.pdf"></a>

## Some results: Lid-driven Cavity

One run simulations for six Reynolds numbers: 100, 400, 1000, 3200, 7500, and 10000. These are the same cases that Ghia (1982) investigated in his paper and were used to validate the code. Additionally, one used mainly a 128 x 128 staggered grid. For Re = 100, 400, and 1000, one used a time step equal to 1E-5 s and a final time equal to 30 s. For the other three Reynolds numbers,  one used a time step equal to 2E-4 and final time equal to 660 s.

<p align="center">
<img src="Reports/video10s.gif" alt="Home Screen" style="float:center;margin-right=10px;" width="400"/>
</p>
