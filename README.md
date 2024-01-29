In order to properly load into the DockingPie plugin in PyMOL, a ligand .mol2 file must have each atom numbered;
however, this is not the default for structures saved through Avogadro. Hence, this simple program with sort and number
each atom in a .mol2 file such that it is compatible with DockingPie.

Usage in the command prompt:
```
python mol2clean.py input_filename.py output_filename.py
```

Examples of .mol2 files containing the structure of pencillin G before and after processing with this script are uploaded for your reference.
