class Room ():
	def __init__(self, id, name):
		self.name = name
		self.id = id
		self.occupancy = 0
	
	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def getOccupancy(self):
		return self.occupancy

	def changeOccupancy(self, change):
		self.occupancy += change
	
	def __str__(self):
		return f"{self.name} ({self.occupancy})"