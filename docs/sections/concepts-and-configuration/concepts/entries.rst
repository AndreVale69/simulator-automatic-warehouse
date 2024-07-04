
.. _entries:

=======
Entries
=======

In the Simulator Automatic Warehouse library, each item is identified as an Entry.
For example, if a tray is 50 centimetres high and each entry by default 
(default space in the configuration) is 25 centimetres high, 
this means that the tray occupies two entries in the warehouse.

Obviously, an entry cannot always be occupied by a tray. 
For this reason we have created two different types of tray: ``TrayEntry`` and ``EmptyEntry``.

-----------
Empty entry
-----------

An EmptyEntry is a simple entry where there is no tray. It is a very simply class.

----------
Tray entry
----------

A TrayEntry is an entry that is marked as `occupied`. 
Note that a set of TrayEntries can identify the same tray.
For this reason, each TrayEntry can have a pointer to the tray. 
The library also provides some useful methods, 
such as ``add_tray`` to add another tray to this tray entry.
