**Note: This repo has not been cleaned up and prepared for general consumption
at all. This is just a dump of the project files. If there is any
interest I will be happy to clean it up, put up some instructions on how to
customize, print and build this keyboard. I'm not sure how useful that would be
though. The keyboard has been adjusted to my hand and probably
wouldn't serve well anyone else. So at this point it's basically a proof of
concept.**

![Wearing both sides](img/20220321_0020.png?raw=true "Wearing both sides")

![One side hanging](img/20220321_0021.png?raw=true "One side hanging")

![One side removed](img/20220321_0024.png?raw=true "One side removed")


Demo
====

Video demo of typing: [https://youtu.be/d8-P9P5Dz6U](https://youtu.be/d8-P9P5Dz6U)


What's this?
============

3D-printable parts of a pretty weird but fully functional keyboard. My design goals:
* It has to be fully usable while walking, since I like to pace back-and-forth
  while thinking
* Even though it's strapped to the arms, it should not hinder basic
  manual tasks that a programmer might need to perform during his work, most
  importantly: preparing and drinking coffee.
* It should be impossible or extremely rare to 'get lost' on the keyboard, i.e.,
  to become uncertain where specific keys are located in relation to the user's
  fingers
* It has to offer all the keys, including modifiers, for normal writing,
  programming and using software such as vim, tmux, etc.
* The typing speed should not suffer _too much_. It might be impossible to reach
  the same speed as on a standard QWERTY keyboards though - some sacrifice is
  acceptable
* (Non-critical) It should look nerdy


Name and pronunciation
======================

Viosuo is pronounced like the [Polish word for
oar](https://translate.google.com/?sl=en&tl=pl&text=oar&op=translate). I chose
this name because an early prototype looked a lot like an oar and was as
uncomfortable as it sounds.


What's in this repo
===================

* The `stl/` subdirectory contains STL files of the most recent design. All of
  them can be easily printed on Ender 3.
* The `viosuo.FCStd` is a FreeCAD file with the entire design. It's done really,
  really badly mostly due to my inexperience, but also because I was working
around the [Topological Naming problem](https://wiki.freecadweb.org/Topological_naming_problem).
* `macros/hole_puncher.py` is a simple FreeCAD macro that for a selectedy Body finds all surfaces that look like they might be inteded for a key and cuts out a 14x14mm square through the middle, intended for an MX switch
* `macros/fc_plumbing.py` is my quickly-abandoned attempt at writing a framework
that would make python scripting in FreeCAD much easier. I still think
somethink like this would be an amazing tool and should be reasonably easy to
create but I'm too lazy to do it myself. I'm including this here since
`hole_puncher` depends on it.
* `zmk/` is my fork of the [ZMK framework](https://github.com/zmkfirmware/zmk)
with a keymap and all the necessary boilerplate for Viosuo added.


How to build one
================


Printing suggestions
--------------------

I used Ultimaker Cura for slicer and printed on Ender 3. Support structure was Tree. Every part was
printed with a Brim for adhesion.

* The Sleeve was printed vertically
* The Connector was printed horizontally, with almost all of its body resting on
  the support structure
* The Palm was printed flat, without any additional rotation. You might have to
  fiddle with the support structure's settings and slowly carefully preview the
  generated gcode to make sure that every hole has enough support.
* The Cover is optional. I printed it upside-down
* The Travel\_bottom and Travel\_top should not be needed at all - I designed
  them quickly when I had to travel and throw my keyboard into a suitcase.


Additional materials
--------------------

* M5x40 screws and M5 nuts (4x)
* Some kind of elastic sleeve to strap the keyboard to your forearm - I used
  football calf compression socks for boys: https://www.emag.ro/set-1-1-jampieri-rucanor-pentru-baieti-rosu-796830/pd/DFV01TMBM/
* nice!nano (2x): https://nicekeyboards.com/nice-nano/
* Mill Max Low Profile Sockets (2 pairs) - optional if you want to connect your
  nice!nanos somehow else
* batteries (2x) - See the nice!nano page for requirements; I used some no-name: https://www.emag.ro/acumulator-li-po-3-7v-400mah-2-fire-1337/pd/DW87YGBBM/
* 1N4148 diodes (68x)
* XDA keycaps (68x)
* MX-compatible switches (68x) - I used gateron greens
* wires
* heat-shrink tubes


Wiring
------

Here are some pictures of the left-hand side's wiring. Please note that I have
soldered sockets to the nice!nano upside-down. There is a very simple reason for
that: I made a mistake.

![wiring01](img/wiring01.png?raw=true "wiring01")

![wiring02](img/wiring02.png?raw=true "wiring02")

![wiring03](img/wiring03.png?raw=true "wiring03")

In the pictures above each wire responsible for a column (i.e., set of keys
operated by a single finger) ends with a black heat-shrink tube. Every row-wire
ends with a red heat-shrink tube. The thumb cluster is treated as another row
but this one ends with a yellow heat-shrink tube.

In order to plug the wires into the Mill Max sockets soldered to nice!nanos I
did the following:

1. Put the heat-shrink tube on each of the wires
1. Gather the diode legs cut off while soldering the keyboard
2. Solder one to the chip-facing end of each of the wires
3. Bend the end of each of those legs at a right angle. The length of the bent
   piece should be such that it fits into the socket but doesn't stick out much.
4. Slide the heat-shrink tube all the way towards the bent part and apply heat.
   That way the wires should not short when they are plugged in next to each
   other.


Sleeve
------

I simply put the 3D-printed "Sleeve" part into my textile sleeves, cut out the
holes for the protruding elements and then stabled the surrounding area of the
textile sleeve so that the holes do not rip.


License
=======

Um... I don't know. I will pick one if there is any interest. It will be
something open and permissive.
