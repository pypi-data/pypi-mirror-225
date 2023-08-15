# PyGRPM

The PyGRPM Medical Physics Library contains many utility features used within 
the Medical Physics Research Group at Université Laval.

This library also contains a multitude of sub-projects, which all contain
practical functionalities, such as creating DICOM SR, manipulating DICOM CT
or even performing calculations with the TG43 formalism.

# Installation
`pip install pygrpm`

# DICOM
## Making SR (Structured Report)
The creation of DICOM SR (Structured Report) has been simplified thanks
to the `pygrpm.make_sr()` and `pygrpm.make_sr_from_text()` functions.
Note that the `SRBuilder` class could allow a more refined/controlled creation.

To create an SR from an arbitrary string, use:
```python
import pygrpm

sr = pygrpm.make_sr_from_text('my text', ['ref_series/ct-1.dcm', 'ref_series/ct-2,dcm'])

sr  # Is a pydicom.FileDataset
sr.ContentSequence[0].TextValue  # Contains the text
sr.ReferencedInstanceSequence  # Contains reference values
```

To use a custom content sequence (i.e: a specific structure):
```python
import pygrpm

# The content sequence can be basically anything if it respects the DICOM standard.
# The user that want a specific structure is invited to read on SR in the DICOM standard.
content_sequence = {
    'ValueType': 'CONTAINER',
    'ConceptNameCodeSequence': {'CodeValue': 'DOC', 'CodeMeaning': 'Document', 'CodingSchemeDesignator': 'DCM'},
    'ContinuityOfContent': 'SEPARATE',
    'Value': [
        {
            'RelationshipType': 'HAS PROPERTIES',
            'ValueType': 'TEXT',
            'ConceptNameCodeSequence': {'CodeValue': '113012',
                                        'CodeMeaning': 'Key Object Description',
                                        'CodingSchemeDesignator': 'DCM'},
            'Value': 'Some text',
        }
    ],
},

sr = pygrpm.make_sr(content_sequence, ['ref_series/ct-1.dcm', 'ref_series/ct-2,dcm'])

sr  # Is a pydicom.FileDataset
sr.ContentSequence  # Correspond to the given content sequence
sr.ReferencedInstanceSequence  # Contains reference values
```

Users who wish to have more information on the creation
of SR are invited to read
https://git.valeria.science/YALEM10/pygrpm/-/blob/master/doc/dicom_sr_builder.md,
https://git.valeria.science/YALEM10/pygrpm/-/blob/master/doc/manufacturer_sr_dose_content_sequence_formats.md
and https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.17.html.


# TG43
Python package to calculate the TG43 formalism based on xarray and the data from
[ESTRO](https://www.estro.org/about/governance-organisation/committees-activities/tg43).


Available seeds
---------------
- SelectSeed
- MicroSelectronV2
- MBDCA
- Flexisource

To add a source, add a directory with the name of the source in data/ with the
following files:
- L.dat containing the active length of the source
- Lambda.dat containing the dose rate constant
- gL.dat containing a list of pairs <r> <gL(r)>
- F.dat containing a matrix of F(r, theta) data with the first line being the r
  values and the first column being the theta values
- (Optional) phi.dat containing a list of pairs <r> <phi(r)> (If the phi.dat
  file is not present, the phi(r) data is created by averaging the F(r, theta)
  data)


Usage
-----
```
import pygrpm
from pygrpm.tg43 import Seed
from matplotlib.pyplot import plt

seed = pygrpm.tg43.Seed("MBDCA")
print(seed.gL)
print(seed.F)

# Display dosimetric grid
grid = seed.grid()
# Plot arbitrary 100th slice
plt.imshow(grid.data[:, :, 100])
plt.show()

# Plot mean dose vs radius with std
mean = seed.get_mean(grid)
std = seed.get_std(grid)
plt.errorbar(mean["r"].data, mean.data, std.data, fmt='o')
plt.show()
```


# Index tracker
Submodule that allows scrolling through slices of 3-D images using the matplotlib backend.

```python
import matplotlib.pyplot as plt
import numpy
import pygrpm

tracker = pygrpm.IndexTracker(
    *plt.subplot(),
    numpy.random.rand(512, 512, 10),
    ...
)
tracker.ax.set_title('My 3-D random image')
tracker.show()
```

See this for more information https://git.valeria.science/YALEM10/pygrpm/-/blob/master/doc/index_tracker.md


# NISTParser
A simple class to extract information from certain NIST webpages.
At the time of writing this covers atomic and electronic cross sections,
material attenuation, as well as material composition.

#### get_cross_sections
This method retrieves the desired cross sections of an element at given energies
on the NIST website in (barns/electron), barn=10^-24cm^2.

Simple use example:

```python
import numpy as np
from pygrpm.nistparser import get_cross_sections

# Define the energies in KeV
# Numpy array is not mandatory, can be any sequence
energies = np.linspace(30, 200, 200)

# Prints the returned list
print(get_cross_sections("H", energies))
```

#### get_electronic_cross_section
See get_cross_section(), method use is identical minus the options argument

#### get_attenuations
Method to retrieve the attenuation of a material in cm^2/g at given energies on the NIST website.
* Note the `option` parameter which can specify the attenuation physics types
* Note the `outopt` parameter which can alter the returned information

Example is similar to get_cross_sections()

#### get_composition
This method is used to get and parse material composition from https://physics.nist.gov/cgi-bin/Star/compos.pl

Simple use example:

```python
from pygrpm.nistparser import get_composition
from pygrpm.nistparser.materials_enum import NISTMaterials

# Prints the returned dictionary
print(get_composition(NISTMaterials.M3_WAX))
```
Note that get_composition expects the material to be of instance NISTMaterials

### Acknowledgements
* This submodule makes use of the `HTMLTablePasrer` built by Josua Schmid, further information can be found in the `pygrpm.nistparser.nistparser.py` file header.
* This submodule is also dependent on the data provided by https://www.nist.gov/pml


# Hounsfield conversion
A helper class meant to offer a quick and simple means to convert an HU array to density values
based on a provided conversion table. Note that the conversion factors for HU to 
density are generally provided by the CT manufacturer.
This class is currently only able to be read under csv format type.

### Usage
Assuming the following sample data as `./curve.csv` file
```text
HU,Mass density [g/cm^3]
-1000,0.00121
-804,0.217
-505,0.508
-72,0.967
-32,0.99
7,1.018
44,1.061
52,1.071
254,1.159
4000,3.21
```

A call through the class can be made to rescale an arbitrary array of Hounsfield unit to density values.
```python
import numpy as np
from pygrpm.ct_utils import ConvertHUToDensity

fithu = ConvertHUToDensity()
my_curve = fithu.load_curve_csv("./curve.csv")

# Note that setting plot to True generates a matplotlib plot of the curve fitting
data, fit_params, labels = fithu.fit_curve(my_curve, plot=True)
# Fit returns unused in this example

my_real_image = np.array([-980, -1000., -823., 1, 20, 700, 2900])
densities = fithu.apply_fit(my_real_image, my_curve)

print(densities)  # [0.02702014 0.00652871 0.18787786 1.0291972 1.03955733 1.41034076, 2.60993423]
```

# TG263
Basic TG263 implementation. Use this module to filter structure names based on the TG263. 


See https://git.valeria.science/YALEM10/pygrpm/-/blob/master/doc/tg263_nomenclature.md