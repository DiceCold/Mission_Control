#dialogue
null_pilot = "null_pilot"
blank_frame = "blank_frame"
selected = "selected"

class Speaker():
    def __init__(self,pilot):
        self.pilot = pilot
        self.name = pilot.name
        self.portrait = blank_frame
        self.lines = ["empty"]

class Plot_Manager():
    def __init__(self,plot_thread):
        if plot_thread == "marko's munitions":
            self.plot_threat = plot_thread

speaker = Speaker()
speaker.nighthawk = "nighthawk"
speaker.rose = "rose"
speaker.lightbringer = "lightbringer"
speaker.stalker = "stalker"
speaker.azurekite = "azurekite"


def load_scene_dialogue(topic, scene_index):
    #mission 1: train under attack
    if topic == "mission" and scene_index == 1:
        speaker.nighthawk.lines = ["Hi, you've got great timing! Normally I'd give you the whole 'welcome to Arcturus' bit, but someone is attacking one of our supply trains and I'm en-route to respond. I can probably handle it, but I'd appreciate it if you could call in some backup just in case.",
                                    "Alright, showtime."]
        speaker.rose.lines = ["Nighthawk needs help? No problem, I'm on my way!"]
        speaker.lightbringer.lines = ["Understood, I've been itching for a chance to test out a new weapon."]
        speaker.stalker.lines = ["Just let me know who needs killing."]
        speaker.azurekite.lines = ["Currently assigned on another mission. Try contacting anyway?",
                                    "Currently unavailable."]
        speaker.deadlift.lines = ["Currently assigned on another mission. Try contacting anyway?",
                                    "Currently unavailable."]
    #social event 1: free trial weapons offer
    if topic == "social_event" and scene_index == 1:
        speaker.benny.lines = ["Hi there, the name's Benny. I'm the local representative of Marco's Munitions LLC. I just wanted to thank you and your team for your hard work keeping us all safe.",
                                "The company lets me give out free trials of our latest products to potential buyers, so as a token of appreciation I'd like to set you up with our brand-new weapon 'The Emissary of the Void' for the next month 100% free of charge.",
                                "Fantastic! Just make sure you get that back to us in a month. Otherwise you can let us know if you'd like to make a purchase and I'll see what I can do in the way of discounts."]
    #social event 2: invitation from Falcone
    if topic == "social_event" and scene_index == 2:
        speaker.carmichael.lines = ["Mr. Falcone has expressed an interest in speaking with you.",
                                "He's a respectable local businessman. Pillar a' the community.",
                                "A few words of advice; be polite, don't talk for too long, and don't ask any questions about the eye."]                    
    #social event (getting to know them)
    if topic == "personal" and scene_index == 1:
        if selected.pilot == nighthawk:
            speaker.nighthawk.lines = ["Good evening, Captain. It's good to meet you properly now that things have quieted down.",
                                        "So, what would you like to know?",
                                        "Before this? I actually came to this planet to be a transport operator as part of the first landing.",
                                        "Nobody who wasn't here when it happened can really understand what it was like to live through few the first days and months of the Collapse. It's the experience of being in a tall building when the bottom few stories abruptly cease to exist. That feeling in the pit of your stomach when suddenly the floor starts to drop as gravity takes hold.",
                                        "No doubt in my mind, the biggest threat to people is the organized gangs in the city."]
    #overheard between pilots
    if topic == overheard and scene_index == 1:
        #Stalker berates Rose
        #triggers after a mission where rose kills < half stalker's total
        speaker.stalker.lines.clear()
        speaker.rose.lines.clear()
        speaker = stalker
        
        stalker.lines = [
            "How is it that you're still such a pathetic loser who can't aim?",
            "You think I'm the only one who thinks you don't deserve a place on the team? I'm just the only one willing to say it to your face.",
            "You'll what? You'll hit me? Try it you weak little tourist, I goddamn dare you.",
            "That's what I thought. You should do everyone a favour and just quit. Someone as worthless as you is just taking up space a better pilot could be filling."
            ]
        rose.lines = [
            "Get lost, Stalker.",
            "Get your hands off me, or I'll--"
            "    "
            ]
        
    #prayers
    if topic == "prayer and scene_index == 1:
        #prayer to the blood god
        lines = [
            "Violent and terrifying master.", 
            "You whose son was born of the virgin Mary so that you might torture and slaughter him in a spell to temper your own savage wrath."
            ]
            
        #prayer to the purifier
        lines = [
            "Oh Lord our creator, master of heaven and earth, hear my prayer.",
            "Please bless [name] with your spirit, that their filthy and wretched soul made be made worthy of you."
            ]
    
load_scene_dialogue("personal",1)
print(speaker.nighthawk.lines[2])