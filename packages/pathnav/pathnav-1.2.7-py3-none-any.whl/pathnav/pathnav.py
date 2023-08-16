import os
from . import errors

class path():
	def __new__(self, path):
		if not os.path.isdir(os.path.expandvars(path)) and not os.path.isfile(os.path.expandvars(path)):
			if not os.path.isdir(os.path.expandvars(path)):
				raise errors.AbsentPathError
		self.isFile = os.path.isfile(os.path.expandvars(path))
		path = path.replace("/", "\\")
		parts = path.split("\\")
		self.parts = [item for item in parts if item != ""]
		if self.isFile:
			self.file_name = self.parts[-1]
			del self.parts[-1]
			return filePath(self.parts, path, self.file_name)
		else:
			return dirPath(self.parts, path)

class dirPath():
	def __init__(self, parts, path):
		self.parts = parts
		self.path = path
		self.resolved_path = os.path.abspath(os.path.expandvars(self.path))
		self.dir_name = self.parts[-1]
		children = next(os.walk(self.resolved_path))
		self.child_dirs = children[1]
		self.child_files = children[2]
		self.dir_size = sum(d.stat().st_size for d in os.scandir(self.resolved_path) if d.is_file())

	def up(self):
		if len(self.parts) < 2:
			raise errors.NoParentDirectoryError
		del self.parts[-1]
		self.path = "\\".join(self.parts)
		return dirPath(self.parts, self.path)

	def into(self, childDirectory):
		if not os.path.isdir(f"{os.path.expandvars(self.path)}\\{childDirectory}"):
			raise errors.AbsentChildDirectoryError
		self.path = f"{self.path}\\{childDirectory}"
		self.resolved_path = f"{self.resolved_path}\\{childDirectory}"
		self.parts.append(childDirectory)
		return dirPath(self.parts, self.path)
	
	def get_file(self, file_name):
		file_path = f"{self.path}\\{file_name}"
		if not os.path.isfile(os.path.expandvars(file_path)):
			return None
		return filePath(self.parts, file_path, file_name)

	def is_subdir(self, path: object):
		return self.resolved_path.startswith(path.resolved_path)


class filePath():
	def __init__(self, parts, path, file_name):
		self.parts = parts
		self.path = path
		self.resolved_path = os.path.abspath(os.path.expandvars(self.path))
		self.file_name = file_name
		file_type = file_name.split(".")
		del file_type[0]
		file_type.insert(0, "")
		self.file_type = file_type[-1]
		self.parent_dir = dirPath(self.parts, "\\".join(self.parts))

	def is_subdir(self, path: object):
		return self.resolved_path.startswith(path.resolved_path)
