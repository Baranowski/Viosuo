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


License
=======

Um... I don't know. I will pick one if there is any interest. It will be
something open and permissive.
