# astroscope telescopes
Package contains several different classes representing telescopes and their functionality. 
A full telescope maybe constructed by creating a chile telescope class which inherits from all the appropriate parent classes. 
The AstropyNexStarLTS130 class under local_telescopes is a good example: 

<b>
<p>from nextstar_telescopes import NexStarSLT130
<p>from astropy_telescope import AstropyTelescope
<p>from astroscope.computers.local import LocalComputer
<p>
<p>
<p>class AstropyNexStarSLT130(LocalComputer, AstropyTelescope, NexStarSLT130):

</b>

It inherits the functionality of a plain NexStarSLT130 and is augmented by functionality from the AstropyTelescope and LocalComputer

This method allows for easy creation of telescopes with varying degree of functionality.
