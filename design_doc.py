startup = True

Original colonization: year -17
Bankruptcy (aka Day01): year 0
Present day: year 2.5

mood_list = ["angry", "happy", "scared",]

if startup: #list traits
    traits = {
        "Marhold Pilot's License":"+1 evasion",
        "Arcturus Pilot's License":"+1 to hit targets at close range"
        "Sulani Pilot's License":"+1 to hit with cold weapons"
        "Upset":"-1 to all rolls",
        "Panicked":"-1 to all rolls",
        "Excited":"+1 to all rolls",
        "Defiant":"+10% chance to ignore orders"
        "Abusive":"Will initiate negative social interactions",
        "Bloodthirsty":"Orders will always switch from objective to aggressive after making an attack",
        "Reckless":"+1 to hit, -1 to evasion. Incompatible with Cautious",
        "Cautious":"-1 to hit, +1 to evasion. Incompatible with Reckless",
        "Trusting":"+10% chance to follow orders. Will initiate positive social interactions"
        "Curious":"+10 chance of success when scouting or exploring. Will initiate positive and negative social interactions unintentionally."
        "Quick Reflexes":"+1 to hit, +1 to evasion"
        "Religion (Tyrant)":"Religious follower of The Blood God"
        "Religious (Purity)":"Religious follower of The Church of Purification"
        "Feel no Pain":"+10 chance to ignore injuries",
        "Disciplined":"+10% chance to follow orders, +1 to hit",
        "Alluring":"Causes others to initiate social interactions with them"
        "Shield-breaker":"+1 to hit if target is shielded"
        "The Black Rage":"Infected with a disease that alters cognition, making them prone to fly into violent fits of anger and hallucinations"
        }
        
class Pilot_Characterization:
    def __init__(self, pilot):
        try: self.name = pilot.name
        except: print("Error: Pilot has no name")
        
        self.pilot_bio = " "
        
        if pilot == "Rose":
            self.pilot_bio = {
                                "Name":"Roselina",
                                "Origin":"A student from a prosperous and aristocratic tradeworld.",
                                "Begins as":"An outsider from off-world.",
                                "During the collapse":"Completed her education and then joined the humanitarian aid mission aproximately 2 years after Day01.",
                                "Dependant on":"Long-distance asynchronous messaging, serialized media and care packages from her home-world friends and family.",
                                "Heading towards":"Social isolation, depression, guilt.",
                                "Willing to":"Sacrifice her own wellbeing."
                                }
        
        elif pilot == "Nighthawk":
            self.pilot_bio = {
                                "Name":"Olivere",
                                "Origin":"A local who was part of the original colonizaiton effort as a transportation operator.",
                                "Begins as": "Team leader",
                                "During the collapse":"Organized and let an armed neighbourhood watch in her community.",
                                "Dependant on": "Having a position of authority and control over others.",
                                "Heading towards": "A poor decision or stress induced breakdown rendering her unfit to lead the team.",
                                "Willing to":"Act extra-judicially"
                                }
        
        elif pilot == "Lightbringer":
            self.pilot_bio = {
                                "Name":"Mickael",
                                "Origin":"A semi-local who took a contract for corporate security on the frontier world a decade ago and was promoted to pilot.",
                                "Begins as":"Team's most experienced pilot.",
                                "During the collapse":"Took his battlesuit and went mercenary, making a small fortune defending supply ships from bandits.",
                                "Dependant on":"A steady flow of drinks and victories, being seen as a hero.",
                                "Willing to":"Walk away if the job's not worth it."
                                }
                                
        elif pilot == "Shadowstalker":
            self.pilot_bio = {
                                "Name":"Sophia",
                                "Origin":"A local youth/student/petty criminal born to colonist parents.",
                                "Begins as":"Cruel bully.",
                                "During the collapse":"Distinguished herself as a quick learner in a battlesuit, was able to evade juvenile prosecution.",
                                "Dependant on":"Dominating and humiliating others to fuel her own ego.",
                                "Willing to":"Completely ruin the life of someone she believes is unworthy."
                                }
        
        elif pilot == "Kite":
            self.pilot_bio = {
                                "Name":"Kaito",
                                "Origin":"Professional racing pilot from off-world.",
                                "Begins as":"Polite but private about his personal life and prefers to keep others at a professional distance.",
                                "During the collapse":"Came seeking information following the dissapearance of a friend, who was found hospitalized and comatose.",
                                "Dependant on":"The hope that their friend will recover.",
                                "Willing to":"Wield unconventional but powerful weapons."
                                }
                                
        elif pilot == "Valorant Phoenix":
            self.pilot_bio = {
                                "Name":"Helena",
                                "Origin":"Daughter of the assistant regional manager for MaxEdDal, born local.",
                                "Begins as":"Private, suspicious, and vengeful towards organized crime.",
                                "During the collapse":"Witnessed the death of her parents at the hands of home-invaders while she hid. Used his ID to break into a hanger and steal suit with weapons, pretended to be an offworlder who had arrived with the relief effort.",
                                "Dependant on":"Her burning desire to see justice done.",
                                "Willing to":"Take down and interrogate criminals while not wearing an obvious and identifiable battlesuit."
                                }
                                
        elif pilot == "Questing Ricochet":
            self.pilot_bio = {
                                "Name":"Adam",
                                "Origin":"Local construction suit operator",
                                "Begins as":"Boastful stalwart",
                                "During the collapse":"Encountered a dead pilot and assumed their identity as an off-world security contractor. Things were so disorganized at the time that nobody questioned it, and his experience piloting construction suits was enough for him to handle at least basic movement.",
                                "Dependant on":"Maintaining his fake identity.",
                                "Willing to":"Be blackmailed by shadowstalker so she doesn't reveal his secret."
                                }
                                
Events = {
            "1":"You discover a relationship between a superior and their subordinate. Not necesarilly problematic, but there is a power imbalance.",
            "2":"A pilot is making heavy use of stimmulants to elevate their performance in the field.",
            "3":"A pilot holds a personal grudge against a faction and wants you to devote more resources to taking them down.",
            "4":"A pilot is personal friends with a pilot in an enemy faction and is reluctant to engage in combat with them.",
            "5":"While on patrol a pilot encounters a situation where someone is in danger. They want to intervene immediately instead of waiting for reinforcements, but doing so is dangerous for them."
            "6":"You discover an immense trove of wealth that is difficult to transport quietly. Others are going to notice and try to take it for themselves if you move it.",
            "7":"A young prince from the Cascadian Royal Families has run away from home to the planet. They wish for him to be returned whether he likes it or not, and quietly to avoid tarnishing the Family's reputation.",
            "8":"One of the pilots has a history they're ashamed of and wish to keep secret. There's nothing morally wrong with it, but their upbringing makes them ashamed and the Church would start shit if they knew.",
            "9":"You realize your mind has been manipulated by another party against your will, changing what consitutes 'you'.",
            "10":"You gain compromising information about someone and must choose whether to release it or keep it hidden and use it as blackmail."
            }

Themes = [
            "Safeguards",
            "Moral compromise",
            "Transparency vs security",
            "Moral hazard and outsourcing costs",
            "Integrity and continuity of self",
            "Nature of personhood",
            "Reciprocal duty between individual and society",
            "The stifiling oppression of copyright, DRM, and licensing",
            ]

Loose_Notes = [
                "Reactive armor",  
                "Taking prisoners is a luxury",
                "Add 'origin' and 'target' variables to he weapon effects so that they don't switch targets",
                "Making the choice of whether you want to use tools that will give you greater power at the risk of terrible consequences",
                "Choosing to aid or oppose the faction that is doing good work and helping people, but is also a delusional cult",
                "Traitors, spies, and trust"
                "Fallout of acting based on bad intel",
                "The flight computer for a battlesuit requires an always-on satnet connection to validate the software license and will not launch otherwise"
                "Being forced to rebuy the exact program you already own becuase you're not permitted to reinstall it on other battlesuit models"
                "Opperating your surgery suite requires proprietary code. Pirating it may save lives"
                ]

Unused_Pilot_Names = [
                    "Torchstar",
                    "Myriad",
                    "Crimson Wing",
                    "Invincible Reason"
                    ]

Policy = {
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

Resources = {
        "spare parts": 10,
        "credits": 0,
        "cybernetics": 2,
        "medications": 10
        }
        
Regions = [
        "Wind turbine field",
        "Hydroelectric dam",
        "Greenhouse",
        "Factory",
        "Mine",
        "Water treatment plant",
        "Starport",
        "Data center/server farm",
        "Wilderness",
        "Wasteland"
        ]