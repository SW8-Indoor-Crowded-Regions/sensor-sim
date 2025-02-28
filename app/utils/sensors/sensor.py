# Make a class for sensor which has an id and two rooms (linked to room class)
class Sensor:
		def __init__(self, id, room1, room2):
				self.id = id
				self.room1 = room1
				self.room2 = room2

		def getId(self):
				return self.id

		def getRoom1(self):
				return self.room1

		def getRoom2(self):
				return self.room2

		def setRoom1(self, room):
				self.room1 = room

		def setRoom2(self, room):
				self.room2 = room
		
		def __str__(self):
				return f"Sensor {self.id}: {self.room1.getName()} ({self.room1.getOccupancy()}) -> {self.room2.getName()} ({self.room2.getOccupancy()})" + self.getRoom1()