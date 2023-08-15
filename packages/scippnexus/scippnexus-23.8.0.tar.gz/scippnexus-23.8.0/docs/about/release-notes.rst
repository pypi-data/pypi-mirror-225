.. _release-notes:

Release Notes
=============


.. Template, copy this to create a new section after a release:

   vrelease
   --------

   Features
   ~~~~~~~~

   Breaking changes
   ~~~~~~~~~~~~~~~~

   Bugfixes
   ~~~~~~~~

   Deprecations
   ~~~~~~~~~~~~

v23.08.0
--------

Breaking changes
~~~~~~~~~~~~~~~~

* ``scippnexus.v2`` is now the default when running ``import scippnexus``.
  Legacy interface has moved to ``scippnexus.v1``, but this will be removed in a future release `#158 <https://github.com/scipp/scippnexus/pull/158>`_.

v23.07.0
--------

Breaking changes
~~~~~~~~~~~~~~~~

* When loading slices, coordinates are no longer converted to attributes but are flagged as unaligned.
  This is equivalent to slicing in Scipp since v23.07.0 `#154 <https://github.com/scipp/scippnexus/pull/154>`_.

v23.05.1
--------

Bugfixes
~~~~~~~~

* Fix loading of data with legacy ``axes`` attribute on signal fields `#145 <https://github.com/scipp/scippnexus/pull/145>`_.
* Fix loading of groups with single-valued and unit-less signal field `#145 <https://github.com/scipp/scippnexus/pull/145>`_.

v23.05.0
--------

Features
~~~~~~~~

* ``scippnexus.v2``: Support NXlog with "sublogs" such as connection_status and alarm `#138 <https://github.com/scipp/scippnexus/pull/138>`_.
* ``scippnexus.v2``: Fall back to dim labels from HDF5 if NeXus does not define labels in NXdata and related classes `#139 <https://github.com/scipp/scippnexus/pull/139>`_.

v23.04.1
--------

* ``scippnexus.v2``: Fix event selection of length 0 `#137 <https://github.com/scipp/scippnexus/pull/137>`_.

v23.04.0
--------

Features
~~~~~~~~

* Added the future API of ``scippnexus`` as ``scippnexus.v2``.
  For many users the API changes will be minor.
  The old API will be deprecated soon and users should try to migrate to the new API.
  Note that ``v2`` is not fully stable yet and in particular the behavior in edge cases is subject to change.

v23.03.0
--------

Features
~~~~~~~~

* Improve handling of files with legacy ``signal`` and ``axis`` attributes, yielding better dim labels `#108 <https://github.com/scipp/scippnexus/pull/108>`_.
* Improve loading and parsing of ``NXoff_geometry`` and ``NXcylindrical_geometry`` `#109 <https://github.com/scipp/scippnexus/pull/109>`_.

Breaking changes
~~~~~~~~~~~~~~~~

Bugfixes
~~~~~~~~

* Fix issue where subgroups in NXdata-like groups where silently skipped.
  This now falls back to loading as ``scipp.DataGroup`` `#108 <https://github.com/scipp/scippnexus/pull/108>`_.

v23.01.0
--------

Features
~~~~~~~~

* Any NXobject can now be loaded as ``scipp.DataGroup`` `#95 <https://github.com/scipp/scippnexus/pull/95>`_.

Breaking changes
~~~~~~~~~~~~~~~~

* :class:`scippnexus.NXevent_data` is now loaded without automatically assigning a variance of 1 to the event weights `#94 <https://github.com/scipp/scippnexus/pull/94>`_.
* If an implementation of :class:`scippnexus.NXobject` fails to load (e.g., as a :class:`scipp.DataArray`), the implementation will fall back to a generic load of all datasets in subgroups as a :class:`scipp.DataGroup`.
  Previously, this was handled in a variety of cases by simply skipping the offending dataset or group `#95 <https://github.com/scipp/scippnexus/pull/95>`_.

v0.4.2 (November 2022)
----------------------

Bugfixes
~~~~~~~~

* Fix SASdata to raise an exception when given Q-edges, which is not valid for SASdata `#77 <https://github.com/scipp/scippnexus/pull/77>`_.

Contributors
~~~~~~~~~~~~

Simon Heybrock :sup:`a`

v0.4.1 (November 2022)
----------------------

Bugfixes
~~~~~~~~

* Fix NXdetetector mechanism for finding dimension labels, which was broken in 0.4.0 in certain cases `#76 <https://github.com/scipp/scippnexus/pull/76>`_.

Contributors
~~~~~~~~~~~~

Simon Heybrock :sup:`a`

v0.4.0 (November 2022)
----------------------

Features
~~~~~~~~

* Add experimental support for application definitions and customization of loader strategies `#63 <https://github.com/scipp/scippnexus/pull/63>`_.

Contributors
~~~~~~~~~~~~

Simon Heybrock :sup:`a` and Jan-Lukas Wynen :sup:`a`

v0.3.3 (October 2022)
---------------------

Bugfixes
~~~~~~~~

* Fix :meth:`scippnexus.Field.dims` and :meth:`scippnexus.Field.shape` to consistently return tuples instead of lists `#62 <https://github.com/scipp/scippnexus/pull/62>`_.
* Fix :meth:`scippnexus.NXobject.__getitem__` to return children with correctly set up field dimensions when indexed with a class name `#62 <https://github.com/scipp/scippnexus/pull/62>`_.

v0.3.0 (September 2022)
-----------------------

Features
~~~~~~~~

* :class:`scippnexus.NXsource`, :class:`scippnexus.NXsample`, and :class:`scippnexus.NXdisk_chopper` now load all entries `#54 <https://github.com/scipp/scippnexus/pull/54>`_.
* :meth:`scippnexus.NXobject.__getitem__` now also accepts :class:`scippnexus.Field` as key and returns all direct children that are NeXus fields, i.e., HDF5 datasets (not groups) `#55 <https://github.com/scipp/scippnexus/pull/55>`_.
* :meth:`scippnexus.NXobject.__getitem__` now also accepts a list of classes for selecting multiple child classes `#55 <https://github.com/scipp/scippnexus/pull/55>`_.

Breaking changes
~~~~~~~~~~~~~~~~

* :class:`scippnexus.NXsource`, :class:`scippnexus.NXsample`, and :class:`scippnexus.NXdisk_chopper` return a ``dict`` instead of ``scipp.Dataset`` `#54 <https://github.com/scipp/scippnexus/pull/54>`_.
* :meth:`scippnexus.Field.__getitem__` now returns a Python object instead of a ``scipp.Variable`` if the field's shape is empty and no unit is given `#57 <https://github.com/scipp/scippnexus/pull/57>`_.

Bugfixes
~~~~~~~~

Deprecations
~~~~~~~~~~~~

v0.2.1 (August 2022)
--------------------

Features
~~~~~~~~

Breaking changes
~~~~~~~~~~~~~~~~

Bugfixes
~~~~~~~~

* Improved mechanism to determine dimension labels in ``NXdetector`` which previous resulted in inconsistent behavior `#53 <https://github.com/scipp/scippnexus/pull/53>`_.

Deprecations
~~~~~~~~~~~~

Contributors
~~~~~~~~~~~~

Simon Heybrock :sup:`a`\ ,
Neil Vaytet :sup:`a`\ ,
and Jan-Lukas Wynen :sup:`a`

v0.2.0 (August 2022)
--------------------

Features
~~~~~~~~

* :meth:`scippnexus.NXobject.__getitem__` now accepts classes such as :class:`scippnexus.NXlog` or :class:`scippnexus.NXdata` as key and returns all direct children with an ``NX_class`` attribute matching the provided class `#48 <https://github.com/scipp/scippnexus/pull/48>`_.
* Added "dynamic" properties to :class:`scippnexus.NXobject`, to access unique children such as entry or instrument `#49 <https://github.com/scipp/scippnexus/pull/49>`_.

Breaking changes
~~~~~~~~~~~~~~~~

* The ``NX_class`` enum has been removed. Use classes such as ``NXlog`` as keys from now on `#48 <https://github.com/scipp/scippnexus/pull/48>`_.
* The ``by_nx_class`` method has been removed `#48 <https://github.com/scipp/scippnexus/pull/48>`_.

Bugfixes
~~~~~~~~

Contributors
~~~~~~~~~~~~

Simon Heybrock :sup:`a`
Neil Vaytet :sup:`a`\ ,
and Jan-Lukas Wynen :sup:`a`

v0.1.3 (June 2022)
------------------

Bugfixes
~~~~~~~~

* Fixed exception when slicing with single integer (instead of a range) `#36 <https://github.com/scipp/scippnexus/pull/36>`_.
* Fixed slicing with bin-edge coords, which previously dropped the upper bound `#36 <https://github.com/scipp/scippnexus/pull/36>`_.

Contributors
~~~~~~~~~~~~

Simon Heybrock :sup:`a`

v0.1.0 (May 2022)
-----------------

Features
~~~~~~~~

This is the initial non-experimental release of scippnexus.

Contributors
~~~~~~~~~~~~

Simon Heybrock :sup:`a`\ ,
Neil Vaytet :sup:`a`\ ,
and Jan-Lukas Wynen :sup:`a`

Contributing Organizations
--------------------------
* :sup:`a`\  `European Spallation Source ERIC <https://europeanspallationsource.se/>`_, Sweden
