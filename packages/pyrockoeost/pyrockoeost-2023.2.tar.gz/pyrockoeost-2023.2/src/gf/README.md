
## pyrockoeost-GF: storage and calculation of synthetic seismograms

The `pyrockoeost.gf` subpackage splits functionality into several submodules:

* The `pyrockoeost.gf.store` module deals with the storage, retrieval and summation of Green's functions.
* The `pyrockoeost.gf.meta` module provides data structures for the meta information associated with the Green's function stores and implements various the Green's function lookup indexing schemes.
* The `pyrockoeost.gf.builder` module defines a common base for Green's function store builders.
* The `pyrockoeost.gf.seismosizer` module provides high level synthetic seismogram synthesis.

All classes defined in the `pyrockoeost.gf.*` submodules are imported into the
`pyrockoeost.gf` namespace, so user scripts may simply use ``from pyrockoeost
import gf`` or ``from pyrockoeost.gf import *`` for convenience.
