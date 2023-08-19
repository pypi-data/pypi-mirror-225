# Concept of h5complete

Tab completion for h5complete

Example:
HDF5 file at folder/file.h5
dataset at folder/file.h5/group/dset

How the completion handler should react:
''                        : glob '*', always append '/' to results
'f'                       : glob 'f*', always append '/' to results
'folder/'                 : before '/' is directory, so glob 'folder/*'
'folder/fi'               : before '/' is directory, so glob 'folder/fi*'
'folder/file.h5/'         : before '/' is file, so open file (if HDF5)
                            filter '*'
                            append '/' to groups, but not to datasets
'folder/file.h5/gr'       : before '/' is file, so open file (if HDF5)
                            filter 'gr*'
                            append '/' to groups, but not to datasets
'folder/file.h5/group/ds' : before '/' is neither file nor directory
                            go back a '/' until before '/' is a file
                            after '/' until last '/' must be valid group
                            filter 'ds*'
                            append '/' to groups, but not to datasets

Option: Filter non-HDF5 files. Issue: Need to attempt to open all files...

If more than one possible result is returned, return only the next possible
elements of the path. If only one possible result remains, return the complete
new path.


   folder / file.h5 / group / dset
  0       1         2       3      4
