---
file_format: mystnb
kernelspec:
  name: python3
jupytext:
  text_representation:
    extension: .md
    format_name: myst
---

(dataset-spec)=
# Quantify dataset specification

```{seealso}
The complete source code of this tutorial can be found in

{nb-download}`Quantify dataset - specification.ipynb`
```

```{code-cell} ipython3
:tags: [hide-cell]
from pathlib import Path

import matplotlib.pyplot as plt
import xarray as xr
from rich import pretty

import quantify_core.data.dataset_adapters as dadapters
import quantify_core.data.dataset_attrs as dattrs
from quantify_core.data import handling as dh
from quantify_core.utilities import dataset_examples
from quantify_core.utilities.examples_support import round_trip_dataset
from quantify_core.utilities.inspect_utils import display_source_code

pretty.install()

dh.set_datadir(Path.home() / "quantify-data")  # change me!
```

This document describes the Quantify dataset specification.
Here we focus on the concepts and terminology specific to the Quantify dataset.
It is based on the Xarray dataset, hence, we assume basic familiarity with the {class}`xarray.Dataset`.
If you are not familiar with it, we highly recommend to first have a look at our {ref}`xarray-intro` for a brief overview.

(sec-coordinates-and-variables)=

## Coordinates and Variables

The Quantify dataset is an xarray dataset that follows certain conventions. We define "subtypes" of xarray coordinates and variables:

(sec-main-coordinates)=

### Main coordinate(s)

- Xarray **Coordinates** that have an attribute {attr}`~quantify_core.data.dataset_attrs.QCoordAttrs.is_main_coord` set to `True`.

- Often correspond to physical coordinates, e.g., a signal frequency or amplitude.

- Often correspond to quantities set through {class}`.Settable`s.

- The dataset must have at least one main coordinate.

  > - Example: In some cases, the idea of a coordinate does not apply, however a main coordinate in the dataset is required. A simple "index" coordinate should be used, e.g., an array of integers.

- See also the method {func}`~quantify_core.data.dataset_attrs.get_main_coords`.

(sec-secondary-coordinates)=

### Secondary coordinate(s)

- A ubiquitous example is the coordinates that are used by "calibration" points.
- Similar to {ref}`main coordinates <sec-main-coordinates>`, but intended to serve as the coordinates of {ref}`secondary variables <sec-secondary-variables>`.
- Xarray **Coordinates** that have an attribute {attr}`~quantify_core.data.dataset_attrs.QCoordAttrs.is_main_coord` set to `False`.
- See also {func}`~quantify_core.data.dataset_attrs.get_secondary_coords`.

(sec-main-variables)=

### Main variable(s)

- Xarray **Variables** that have an attribute {attr}`~quantify_core.data.dataset_attrs.QVarAttrs.is_main_var` set to `True`.
- Often correspond to a physical quantity being measured, e.g., the signal magnitude at a specific frequency measured on a metal contact of a quantum chip.
- Often correspond to quantities returned by {class}`.Gettable`s.
- See also {func}`~quantify_core.data.dataset_attrs.get_main_vars`.

(sec-secondary-variables)=

### Secondary variables(s)

- Again, the ubiquitous example is "calibration" datapoints.
- Similar to {ref}`main variables <sec-main-variables>`, but intended to serve as reference data for other main variables (e.g., calibration data).
- Xarray **Variables** that have an attribute {attr}`~quantify_core.data.dataset_attrs.QVarAttrs.is_main_var` set to `False`.
- The "assignment" of secondary variables to main variables should be done using {attr}`~quantify_core.data.dataset_attrs.QDatasetAttrs.relationships`.
- See also {func}`~quantify_core.data.dataset_attrs.get_secondary_vars`.

```{note}
In this document we show exemplary datasets to highlight the details of the Quantify dataset specification.
However, for completeness, we always show a valid Quantify dataset with all the required properties.
```

In order to follow the rest of this specification more easily have a look at the example below.
It should give you a more concrete feeling of the details that are exposed afterward.
See {ref}`sec-dataset-examples` for an exemplary dataset.

We use the
{func}`~quantify_core.utilities.dataset_examples.mk_two_qubit_chevron_dataset` to
generate our dataset.

```{code-cell} ipython3
---
tags: [hide-cell]
mystnb:
  code_prompt_show: Source code for generating the dataset below
---
display_source_code(dataset_examples.mk_two_qubit_chevron_dataset)
```

```{code-cell} ipython3
dataset = dataset_examples.mk_two_qubit_chevron_dataset()
assert dataset == round_trip_dataset(dataset)  # confirm read/write
```

### 2D example

In the dataset below we have two main coordinates `amp` and `time`; and two main
variables `pop_q0` and `pop_q1`.
Both main coordinates "lie" along a single xarray dimension, `main_dim`.
Both main variables lie along two xarray dimensions `main_dim` and `repetitions`.

```{code-cell} ipython3
dataset
```

**Please note** how the underlying arrays for the coordinates are structured!
Even for "gridded" data, the coordinates are arranged in arrays
that match the dimensions of the variables in the xarray. This is
done so that the data can support more complex scenarios, such as
irregularly spaced samples and measurements taken at unknown locations.

```{code-cell} ipython3
n_points = 110  # only plot a few points for clarity
_, axs = plt.subplots(4, 1, sharex=True, figsize=(10, 10))
dataset.amp[:n_points].plot(
    ax=axs[0], marker=".", color="C0", label=dataset.amp.long_name
)
dataset.time[:n_points].plot(
    ax=axs[1], marker=".", color="C1", label=dataset.time.long_name
)
_ = dataset.pop_q0.sel(repetitions=0)[:n_points].plot(
    ax=axs[2], marker=".", color="C2", label=dataset.pop_q0.long_name
)
_ = dataset.pop_q1.sel(repetitions=0)[:n_points].plot(
    ax=axs[3], marker=".", color="C3", label=dataset.pop_q1.long_name
)
for ax in axs:
    ax.legend()
    ax.grid()
```

As seen above, in the Quantify dataset the main coordinates do not explicitly index
the main variables because not all use-cases fit within this paradigm.
However, when possible, the Quantify dataset can be reshaped to take advantage of the
xarray built-in utilities.

<!-- FIXME when a Quantify dataset has a class re-evaluate the need for following sentence or some equivalent: -->
<!-- Note, however, that this reshaping will produce an xarray dataset that does not comply with the Quantify dataset specification. -->

```{code-cell} ipython3

dataset_gridded = dh.to_gridded_dataset(
    dataset,
    dimension="main_dim",
    coords_names=dattrs.get_main_coords(dataset),
)
dataset_gridded.pop_q0.plot.pcolormesh(x="amp", col="repetitions")
_ = dataset_gridded.pop_q1.plot.pcolormesh(x="amp", col="repetitions")
```

## Dimensions

The main variables and coordinates present in a Quantify dataset have the following required and optional xarray dimensions:

### Main dimension(s) \[Required\]

The main dimensions comply with the following:

- The outermost dimension of any main coordinate/variable, OR the second outermost dimension if the outermost one is a {ref}`repetitions dimension <sec-repetitions-dimensions>`.
- Do not require to be explicitly specified in any metadata attributes, instead utilities for extracting them are provided. See {func}`~quantify_core.data.dataset_attrs.get_main_dims` which simply applies the rule above while inspecting all the main coordinates and variables present in the dataset.
- The dataset must have at least one main dimension.

```{admonition} Note on nesting main dimensions
Nesting main dimensions is allowed in principle and such examples are
provided but it should be considered an experimental feature.

- Intuition: intended primarily for time series, also known as "time trace" or simply trace. See {ref}`sec-dataset-t1-traces` for an example.
```

### Secondary dimension(s) \[Optional\]

Equivalent to the main dimensions but used by the secondary coordinates and variables.
The secondary dimensions comply with the following:

- The outermost dimension of any secondary coordinate/variable, OR the second outermost dimension if the outermost one is a {ref}`repetitions dimension <sec-repetitions-dimensions>`.
- Do not require to be explicitly specified in any metadata attributes, instead utilities for extracting them are provided. See {func}`~quantify_core.data.dataset_attrs.get_secondary_dims` which simply applies the rule above while inspecting all the secondary coordinates and variables present in the dataset.

(sec-repetitions-dimensions)=
### Repetitions dimension(s) \[Optional\]

Repetition dimensions comply with the following:

- Any dimension that is the outermost dimension of a main or secondary variable when its attribute {attr}`QVarAttrs.has_repetitions <quantify_core.data.dataset_attrs.QVarAttrs.has_repetitions>` is set to `True`.
- Intuition for this xarray dimension(s): the equivalent would be to have `dataset_reptition_0.hdf5`, `dataset_reptition_1.hdf5`, etc. where each dataset was obtained from repeating exactly the same experiment. Instead we define an outer dimension for this.
- Default behavior of (live) plotting and analysis tools can be to average the main variables along the repetitions dimension(s).
- Can be the outermost dimension of the main (and secondary) variables.
- Variables can lie along one (and only one) repetitions outermost dimension.

#### Example datasets with repetition

As shown in the {ref}`xarray-intro` an xarray dimension can be indexed by a `coordinate` variable. In this example the `repetitions` dimension is indexed by the `repetitions` xarray coordinate. Note that in an xarray dataset, a dimension and a data variable or a coordinate can share the same name. This might be confusing at first. It takes just a bit of dataset manipulation practice to gain an intuition for how it works.

```{code-cell} ipython3
coord_dims = ("repetitions",)
coord_values = ["A", "B", "C", "D", "E"]
dataset_indexed_rep = xr.Dataset(coords=dict(repetitions=(coord_dims, coord_values)))

dataset_indexed_rep
```

```{code-cell} ipython3
# merge with the previous dataset
dataset_rep = dataset.merge(dataset_indexed_rep, combine_attrs="drop_conflicts")

assert dataset_rep == round_trip_dataset(dataset_rep)  # confirm read/write

dataset_rep
```

And as before, we can reshape the dataset to take advantage of the xarray built-in utilities.

```{code-cell} ipython3
dataset_gridded = dh.to_gridded_dataset(
    dataset_rep,
    dimension="main_dim",
    coords_names=dattrs.get_main_coords(dataset),
)
dataset_gridded
```

It is now possible to retrieve (select) a specific entry along the `repetitions` dimension:

```{code-cell} ipython3
_ = dataset_gridded.pop_q0.sel(repetitions="A").plot(x="amp")
plt.show()
_ = dataset_gridded.pop_q0.sel(repetitions="D").plot(x="amp")
```

## Dataset attributes

The required attributes of the Quantify dataset are defined by the following dataclass.
It can be used to generate a default dictionary that is attached to a dataset under the {attr}`xarray.Dataset.attrs` attribute.

```{eval-rst}
.. autoclass:: quantify_core.data.dataset_attrs.QDatasetAttrs
    :members:
    :noindex:
    :show-inheritance:
```

Additionally in order to express relationships between coordinates and/or variables
the following template is provided:

```{eval-rst}
.. autoclass:: quantify_core.data.dataset_attrs.QDatasetIntraRelationship
    :members:
    :noindex:
    :show-inheritance:
```

```{code-cell} ipython3
from quantify_core.data.dataset_attrs import QDatasetAttrs

# tip: to_json and from_dict, from_json  are also available
dataset.attrs = QDatasetAttrs().to_dict()
dataset.attrs
```

Note that xarray automatically provides the entries of the dataset attributes as python attributes. And similarly for the xarray coordinates and data variables.

```{code-cell} ipython3
dataset.quantify_dataset_version, dataset.tuid
```

## Main coordinates and variables attributes

Similar to the dataset attributes ({attr}`xarray.Dataset.attrs`), the main coordinates and variables have each their own required attributes attached to them as a dictionary under the {attr}`xarray.DataArray.attrs` attribute.

```{eval-rst}
.. autoclass:: quantify_core.data.dataset_attrs.QCoordAttrs
    :members:
    :noindex:
    :show-inheritance:
```

```{code-cell} ipython3
dataset.amp.attrs
```

```{eval-rst}
.. autoclass:: quantify_core.data.dataset_attrs.QVarAttrs
    :members:
    :noindex:
    :show-inheritance:
```

```{code-cell} ipython3
dataset.pop_q0.attrs
```

## Storage format

The Quantify dataset is written to disk and loaded back making use of xarray-supported facilities.
Internally we write and load to/from disk using:

```{code-cell} ipython3
display_source_code(dh.write_dataset)
display_source_code(dh.load_dataset)
```

Note that we use the `h5netcdf` engine which is more permissive than the default NetCDF engine to accommodate arrays of complex numbers.

```{note}
Furthermore, in order to support a variety of attribute types (e.g. the `None` type) and shapes (e.g. nested dictionaries) in a seamless dataset round trip, some additional tooling is required. See source codes below that implements the two-way conversion adapter used by the functions shown above.
```

```{code-cell} ipython3
display_source_code(dadapters.AdapterH5NetCDF)
```
