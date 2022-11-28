#policy selections

policy = {
	"hostage negotiation":"permitted",
	"recreational substance use":"permitted",
	"excess use of force":"prohibited",
	"privacy violation":"permitted",
	"withdraw from combat":"when injured",
	"copyright violation":"permitted",
	"hate speech":"prohibited",
	"religious beliefs":"permitted when private",
	"disclosing classified security information":"prohibited",
	"cooperating with journalists":"permitted",
	"speaking negatively about the organization":"permitted, statements of opinion only"
}

resources = {
	"spare parts": 10,
	"credits": 0,
	"cybernetics": 2,
	"medications": 10
}


class facilities():
	def __init__(self, type, location):
		
		self.type = type
		self.location = location
		self.rank = 1
		self.failure_rate = 0.60 - (0.1 * self.rank)

		if self.type == "battlesuit_hangar":
			self.capacity = self.rank
			self.repair_bays = {
				"repair_bay 1":"empty",
				"repair_bay 2":"empty",
				"repair_bay 3":"empty",
				"repair_bay 4":"empty",
				"repair_bay 5":"empty",
				"repair_bay 6":"empty"
			}

			def perform_repairs(self):
				for suit in self.repair_bays:
					if resources["spare parts"] > 0 and suit != "empty":
					 if suit.damaged == True:
						resources["spare parts"] -= 1
						percentile_roll = random.ranint(0,100)/100
						if percentile_roll > self.failure_rate:
							if suit.severely_damaged == True: suit.severely_damaged = False
							elif suit.damaged == True: suit.damaged = False
					if suit.damaged == False: suit = "empty"

		if self.type == "infirmary":
			self.capacity = self.rank
			self.med_beds = {
				"bed 1":"empty",
				"bed 2":"empty",
				"bed 3":"empty",
				"bed 4":"empty",
				"bed 5":"empty",
				"bed 6":"empty",
			}

			# #placeholder writing out Pilot health conditions
			# Pilot.health = {
			# 	"bleeding":"blood loss",
			# 	"disease":"illness",
			# 	"pain":7/10,
			# 	"skull":"fractured",
			#	"pelvis":"broken"
			#	"ribs":"fractured"
			# 	"left arm":"prosthetic (damaged)"
			# 	"left leg":"shattered",
			# 	"right arm":"lacerated"
			# 	"right leg":"maimed"
			# }
			# for condition in Pilot.health: condition = "empty"
			# #placeholder writing out Pilot health conditions



			def perform_healing(self):
				for pilot in self.med_beds:
					if pilot != "empty":
						for condition in pilot.health:
							
							#treat illnesses
							if condition == "illness" and resources["medications"] > 0:
								resources["medications"] -= 1
								condition = "illness (recovering)"
							elif condition == "illness (recovering)" and resources["medications"] > 0:
								resources["medications"] -= 1
								percentile_roll = random.ranint(0,100)/100
								if percentile_roll > self.failure_rate: condition = "empty"
							
							#treat blood loss
							elif condition == "severe blood loss": condition = "blood loss"
							elif condition == "blood loss": condition = "blood loss (recovering)"
							elif condition == "blood loss (recovering)": 
								percentile_roll = random.ranint(0,100)/100
								if percentile_roll > self.failure_rate: condition = "empty"

							#treat broken bones
							elif condition == "fractured": condition = "fractured (recovering)"
							elif condition == "broken": condition = "broken (recovering)"
							elif condition == "fractured (recovering)" or condition == "broken (recovering)":
								percentile_roll = random.ranint(0,100)/100
								if percentile_roll > self.failure_rate: condition = "empty"

							#prosthetics
							elif condition == "maimed": condition = "amputated"
							elif condition == "amputated" and resources["cybernetics"] >= 2:
								resources["cybernetics"] -= 2
								condition = "prosthetic"
							elif condition = "prosthetic (damaged)" and resources["cybernetics"] >= 1:
								resources["cybernetics"] -= 1
								condition = "prosthetic"

		if self.type == "prison":
			self.capacity = self.rank*2
			self.cells = {
				"cell 1":"empty",
				"cell 2":"empty",
				"cell 3":"empty",
				"cell 4":"empty",
				"cell 5":"empty",
				"cell 6":"empty",
				"cell 7":"empty",
				"cell 8":"empty",
				"cell 9":"empty",
				"cell 10":"empty",
				"solitary confinement 1":"empty",
				"solitary confinement 2":"empty",
			}

		if self.type == "research lab":
			self.current_project = "none"
			self.research_progress = 0.00
			self.completed_projects = []
			
			def complete_research(self, project):
				if self.research_progress == 1:
					self.completed_projects.append(self.current_project)
					self.current_project = "none"
					self.research_progress = 0
