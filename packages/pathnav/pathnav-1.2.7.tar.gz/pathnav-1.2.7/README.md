# pathnav
Navigate paths with ease for python

# Docs
## Install pathnav
`pip install pathnav`
## Create new path object
```py
import pathnav

path = pathnav.path("C:\\Users\\titushm\\Repos\\Github") # create a directory path object

# Properties
print(path.path) # get the path as a string
print(path.dir_name) # get the name of the directory
print(path.child_dirs) # get a list of directorys in the directory
print(path.child_files) # get a list of files in the directory
print(path.dir_size) # get the size in bytes of the directory
print(path.resolved_path) # get the full path without relative parts such as .. and %enviroment_varible%

# Methods
print(path.up()) # go up one directory
print(path.into("example-repo")) # go down one specified directory
print(path.get_file("text-file.txt")) # get a file by name in the directory, returns None if no file is present
parent_path = pathnav.path("C:\\Users\\titushm\\Repos")
print(path.is_subdir(parent_path)) # check if a path is a subdirectory of another path

path = pathnav.path("C:\\Users\\titushm\\Repos\\Github\\test-file.txt") # create a file path object

# Properties
print(path.path) # get the path as a string
print(path.file_name) # get the file name as string
print(path.file_type) # get the file type as a string
print(path.parent_dir) # returns a directory path object for the directory that the file is in
# Methods
print(path.is_subdir(parent_path))
```
