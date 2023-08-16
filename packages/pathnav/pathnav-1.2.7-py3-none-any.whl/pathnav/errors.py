class AbsentPathError(Exception):
	def __init__(self, message="The path you provided does not exist or is invalid"):
		self.message = message
		super().__init__(self.message)

class AbsentChildDirectoryError(Exception):
	def __init__(self, message="The directory you provided does not exist"):
		self.message = message
		super().__init__(self.message)

class AbsentFileError(Exception):
	def __init__(self, message="The file you provided does not exist"):
		self.message = message
		super().__init__(self.message)

class NoParentDirectoryError(Exception):
	def __init__(self, message="You cannot go back a directory as there is not a parent directory"):
		self.message = message
		super().__init__(self.message)