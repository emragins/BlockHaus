import ika

class Timer:
	"""
		Sets a current time and duration to be used 
		to tell whether that time has passed yet. 
	"""
	
	def __init__(self, duration):
		"""
			Starts the timer. Duration is the length it lasts in 1/100s of seconds.
		"""
				
		self.startTime = ika.GetTime()
		self.duration = duration
		self.endTime = self.startTime+duration
		
		self.Reset()
		
	def Reset(self):
		"""
			Resets the start and end times based on
			the original duration of the timer.
		"""
				
		self.startTime = ika.GetTime()
		self.endTime = self.startTime+self.duration
		
	def IsDone(self):
		"""
			Returns true or false depending on whether the 
			timer's designated end time has passed.
		"""
		
		if self.endTime <= ika.GetTime():
			return True
		else:
			return False