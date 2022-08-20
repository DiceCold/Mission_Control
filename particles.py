
import pygame, sys, random	

class ParticlePrinciple:
	def __init__(self):
		self.particles = []

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]
				particle[1] -= 0.2
				pygame.draw.circle(screen,pygame.Color('Red'),particle[0], int(particle[1]))
	def add_particles(self):
		pos_x = 200
		pos_y = 200
		radius = 10
		direction_x = random.randint(-3,3)
		direction_y = random.randint(-3,3)
		particle_circle = [[pos_x,pos_y],radius,[direction_x,direction_y]]
		self.particles.append(particle_circle)
	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particles = particle_copy


pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

particle1 = ParticlePrinciple()
particle2 = ParticlePrinciple()

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,40)

# while True:
	# for event in pygame.event.get():
		# if event.type == pygame.QUIT:
			# pygame.quit()
			# sys.exit()
		# if event.type == PARTICLE_EVENT:
			# particle1.add_particles()

	# screen.fill((30,30,30))
	# particle1.emit()
	# pygame.display.update()
	# clock.tick(120)