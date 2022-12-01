startup = True


class CompletionTracker:
    def __init__(self):
        self.missions_completed = 0
        self.missions_total = 10
        self.random_events_completed = 0
        self.random_events_total = 20

        self.enemy_types_completed = 0
        self.enemy_types_total = 3

        self.weapons_completed = 1
        self.weapons_total = 5
        self.shields_completed = 1
        self.shields_total = 3
        self.jets_completed = 1
        self.jets_total = 3
        self.active_abilities_completed = 0
        self.active_abilities_total = 5

        self.pilot_list = ["Kite", "Nighthawk", "Deadlift", "Stalker", "Saint"]
        self.mood_list = ["Default", "Happy", "Excited", "Serious", "Angry", "Worried", "Impressed", "Sad", "Scared"]
        self.pilot_art_completed = {
            "Kite": 7,
            "Nighthawk": 1,
            "Deadlift": 3,
            "Stalker": 5,
            "Saint": 0
        }

        self.npc_list = {
            "Roger": "Baal Corporation",
            "Martino": "Cabarelli Family",
            "Miranda": "Pinnacle Research Ltd",
            "Nasha": "Sallowar Enterprises",
            "Desmond": "Baal Corporation",
            "Kail - Undefined": "The Bravos Gang"
        }


colonization_year: -17
zero_year: 0
current_year: 2.5

Events = {
    "1": "Relationship between superior and subordinate. Not necessarily problematic, but there is a power imbalance.",
    "2": "Pilot is making heavy use of stimulants to elevate their performance in the field.",
    "3": "Pilot holds a personal grudge against a faction and wants you to devote more resources to taking them down.",
    "4": "Pilot is personal friends with a Pilot in an enemy faction and is reluctant to engage in combat with them.",
    "5": "Pilot encounters someone in danger. Wants to intervene immediately instead of waiting for reinforcements.",
    "6": "You discover immense wealth that is difficult to transport. Others are going to notice and try to take it.",
    "7": "Prince from Cascadian Royals ran away from home. They want him returned quietly, whether he likes it or not.",
    "8": "Pilot is ashamed of their past due to religious upbringing. Church will pressure you if they find out.",
    "9": "You realize your mind has been compromised.",
    "10": "Discover compromising information on a political figure: release it or use it as blackmail."
}

Themes = [
    "Safeguards",
    "Moral compromise",
    "Transparency vs security",
    "Moral hazard and outsourcing costs",
    "Integrity and continuity of self",
    "Nature of personhood",
    "Reciprocal duty between individual and society",
    "The stifling oppression of copyright, DRM, and licensing",
]

Loose_Notes = [
    "Reactive armor",
    "Taking prisoners is a luxury",
    "Add 'origin' and 'target' variables to he weapon effects so that they don't switch targets",
    "Greater power at the risk of terrible consequences",
    "Choosing to aid or oppose the faction that is doing good work and helping people, but is also a delusional cult",
    "Traitors, spies, and trust"
    "Fallout of acting based on bad intel",
    "The flight computer for a battlesuit requires an always-on satnet connection to validate the software license"
    "Forced to rebuy software because it's licensed per-suit"
    "Operating your surgery suite requires proprietary code. Pirating it may save lives"
]

Unused_Pilot_Names = [
    "Torchstar",
    "Myriad",
    "Crimson Wing",
    "Invincible Reason",
    "Yellow King"
]

policy = {
    "hostage negotiation": "permitted",
    "recreational substance use": "permitted",
    "excess use of force": "prohibited",
    "privacy violation": "permitted",
    "withdraw from combat": "when injured",
    "copyright violation": "permitted",
    "hate speech": "prohibited",
    "religious beliefs": "permitted when private",
    "disclosing classified security information": "prohibited",
    "cooperating with journalists": "permitted",
    "speaking negatively about the organization": "permitted, statements of opinion only"
}

resources = {
    "spare parts": 10,
    "credits": 0,
    "cybernetics": 2,
    "medications": 10
}

regions = [
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
