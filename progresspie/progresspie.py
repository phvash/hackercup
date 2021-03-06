import math

class ProgressPie():
	def __init__(self):
		self.radius = 50
		self.cord_centre = (50, 50)
		self.data2write = []
		self.readFile()

	def readFile(self):
		f_obj = open('input.txt', 'r')
		file_lines = f_obj.readlines()
		f_obj.close()
		file_lines = [line.strip('\n') for line in file_lines if line.strip('\n') !=""]
		self.lines_of_input = int(file_lines[0].strip(' '))
		self.data = file_lines[1:]

	def writeData(self):
		f_obj = open('output.txt', 'w')
		self.data2write[-1] = self.data2write[-1].strip('\n')
		file_lines = f_obj.writelines(self.data2write)
		f_obj.close()

	def getDist(self, cord_1, cord_2):
		x1, y1 = cord_1
		x2, y2 = cord_2
		# d = _/(x2-x1)^2 + (y2 - y1)^2
		return math.sqrt(pow(math.fabs((x2-x1)), 2) + pow(math.fabs((y2-y1)), 2))

	def percentage2angle(self, percentage):
		return (percentage/(100*1.0)) * 360


	def isOnCircle(self, coordinates):
		# (x-a)^2 + (x - b)^2 = r^2
		x, y = coordinates
		if self.getDist(self.cord_centre, coordinates) <= self.radius:
			return True
		else:
			return False

	def findTan(self, coordinates):
		gx, gy = coordinates
		if self.getQuadrants(coordinates=coordinates) == 1:
			x = gx - 50
			y = gy - 50
		elif self.getQuadrants(coordinates=coordinates) == 2:
			x = gx - 50
			y = 50 - gy
		elif self.getQuadrants(coordinates=coordinates) == 3:
			x = 50 - gx
			y = 50 - gy
		elif self.getQuadrants(coordinates=coordinates) == 4:
			x = 50 - x
			y = gy - 50
		else:
			raise ValueError('Invalid coordinates')
		return math.degrees(math.atan(y/x))

	def getQuadrants(self, angle=None, coordinates=None):
		if angle is None and coordinates is None:
			raise TypeError("Value must be an angle or a pair of coordinates")
		
		quadrants = []
		if angle:
			if angle >= 0:
				quadrants.append(1)
			if angle >= 90:
				quadrants.append(2)
			if angle >= 180:
				quadrants.append(3)
			if angle >= 270:
				quadrants.append(4)
			if angle > 360:
				raise ValueError("Angle can not be greater than 360 deg")
			print('quadrants: ', quadrants)
			return quadrants
		elif coordinates:
			x, y = coordinates
			if x >=50 and y >=50:
				return 1
			elif x >=50 and y <=50:
				return 2
			elif x <=50 and y <=50:
				return 2
			elif x <=50 and y >=50:
				return 2
			else:
				raise ValueError("Invalid point")

	def valid(self, coordinates, angle):
		if angle == 0:
			print("At '0%' all points are white")
			return False
		if not self.isOnCircle(coordinates):
			print("coordinates outside of circle")
			return False
		if self.getQuadrants(coordinates=coordinates) not in self.getQuadrants(angle=angle):
			print("coordinates'quadrant not covered by anggle sector")
			return False
		return True

	def overlap(self, coordinates, angle):
		angle_given = angle
		tan_angle = self.findTan(coordinates)

		if self.getQuadrants(coordinates=coordinates) == 1:
			if tan_angle >= 90 - angle_given:
				return True
		elif self.getQuadrants(coordinates=coordinates) == 2:
			if tan_angle <= angle_given - 90:
				return True 
		elif self.getQuadrants(coordinates=coordinates) == 3:
			if tan_angle >= 270 - angle_given:
				return True
		elif self.getQuadrants(coordinates=coordinates) == 4:
			if tan_angle <= angle_given - 270:
				return True
		else:
			return False

	def main(self):
		count = 1
		for line in self.data:
			percentage, x, y = line.split(' ')
			angle = self.percentage2angle(int(percentage))
			coordinates = (int(x), int(y))
			print(angle, coordinates)
			result = "Case #{}: White\n".format(count)
			if not self.valid(coordinates, angle):
				count += 1
				print(result)
				self.data2write.append(result)
				continue
			if self.overlap(coordinates, angle):
				result = 'Case #{}: Black\n'.format(count)
				print("valid and overlap")
				print(result)
			else:
				result = 'Case #{}: White\n'.format(count)
				print("Valid but no overlap")
				print(result)
			count += 1
			self.data2write.append(result)
		self.writeData()


if __name__ == '__main__':
	test_cir = ProgressPie()
	test_cir.main()