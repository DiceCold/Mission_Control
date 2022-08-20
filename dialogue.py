#dialogue
null_pilot = "null_pilot"
blank_frame = "blank_frame"
selected = "selected"

class Speaker():
    def __init__(self):
        self.pilot = null_pilot
        self.portrait = blank_frame
        self.lines = ["null"]

class Plot_Manager():
    def __init__(self,plot_thread):
        if plot_thread == "marko's munitions":
            self.plot_threat = plot_thread

speaker = Speaker()
speaker.nighthawk = "nighthawk"
speaker.intreppidrose = "intreppidrose"
speaker.lightbringer = "lightbringer"
speaker.shadowstalker = "shadowstalker"
speaker.azurekite = "azurekite"


def load_scene_dialogue(type, scene_index):
    #mission 1: train under attack
    if type == "mission" and scene_index == 1:
        speaker.nighthawk.lines = ["Hi, you've got great timing! Normally I'd give you the whole 'welcome to Arcturus' bit, but someone is attacking one of our supply trains and I'm en-route to respond. I can probably handle it, but I'd appreciate it if you could call in some backup just in case.",
                                    "Alright, showtime."]
        speaker.intreppidrose.lines = ["Nighthawk needs help? No problem, I'm on my way!"]
        speaker.lightbringer.lines = ["Understood, I've been itching for a chance to test out a new weapon."]
        speaker.shadowstalker.lines = ["Just let me know who needs killing."]
        speaker.azurekite.lines = ["Currently assigned on another mission. Try contacting anyway?",
                                    "Currently unavailable."]
        speaker.deadlift.lines = ["Currently assigned on another mission. Try contacting anyway?",
                                    "Currently unavailable."]
    #social event 1: free trial weapons offer
    if type == "social_event" and scene_index == 1:
        speaker.benny.lines = ["Hi there, the name's Benny. I'm the local representative of Marco's Munitions LLC. I just wanted to thank you and your team for your hard work keeping us all safe.",
                                "The company lets me give out free trials of our latest products to potential buyers, so as a token of appreciation I'd like to set you up with our brand-new weapon 'The Emissary of the Void' for the next month 100% free of charge.",
                                "Fantastic! Just make sure you get that back to us in a month. Otherwise you can let us know if you'd like to make a purchase and I'll see what I can do in the way of discounts."]
    #social event 2: invitation from Falcone
    if type == "social_event" and scene_index == 2:
        speaker.carmichael.lines = ["Mr. Falcone has expressed an interest in speaking with you.",
                                "He's a respectable local businessman. Pillar a' the community.",
                                "A few words of advice; be polite, don't talk for too long, and don't ask any questions about the eye."]                    
    #social event (getting to know them)
    if type == "personal" and scene_index == 1:
        if selected.pilot == nighthawk:
            speaker.nighthawk.lines = ["Good evening, Captain. It's good to meet you properly now that things have quieted down.",
                                        "Do you drink? I brought a bottle of wine as a house-warming gift, so to speak.",
                                        "So, what would you like to know?",
                                        "Before this? I actually came to this planet to be a transport operator as part of the first landing.",
                                        "Nobody who wasn't here when it happened can really understand what it was like to live through few the first days and months of the Collapse. It's the experience of being in a tall building when the bottom few stories abruptly cease to exist. That feeling in the pit of your stomach when suddenly the floor starts to drop as gravity takes hold.",
                                        "No doubt in my mind, the biggest threat to people is the organized gangs in the city."]

load_scene_dialogue("personal",1)
print(speaker.nighthawk.lines[2])