import random

c_chord = ["C4", "E4", "G4"]
seven_nation_army = [("E4", 0.7), ("E4", 0.3), ("G4", 0.3), ("E4", 0.3), ("D4", 0.3), ("C4", 0.7),
                     ("B3", 0.7), ("E4", 0.7), ("E4", 0.3), ("G4", 0.3), ("E4", 0.3), ("D4", 0.3),
                     ("C4", 0.3), ("D4", 0.3), ("C4", 0.3), ("B3", 0.7)]
seven_nation_army_tones = ["B3", "C4", "D4", "E4", "G4"]

amours_toujours = [("E4", 0.4), ("E4", 0.4), ("C5", 0.4), ("B4", 0.7), ("B4", 0.4), ("B4", 0.4), ("C5", 0.4),
                   ("A4", 0.7), ("A4", 0.4), ("A4", 0.4), ("G4", 0.4), ("A4", 0.4), ("A4", 0.4), ("A4", 0.4),
                   ("G4", 0.4), ("A4", 0.4), ("G4", 0.4), ("A4", 0.4), ("G4", 0.4), ("E4", 0.7), ]
amours_toujours_tones = ["E4", "G4", "A4", "B4", "C5"]

i_cant_get_no_satisfaction = [("D4", 0.7), ("D4", 0.7), ("D4", 0.4), ("E4", 0.4), ("F4", 0.7), ("F4", 0.4), ("F4", 0.4),
                              ("E4", 0.4), ("E4", 0.4), ("D4", 0.7), ("D4", 0.7), ("D4", 0.4), ("D4", 0.4), ("E4", 0.4),
                              ("F4", 0.7), ("F4", 0.4), ("F4", 0.4), ("E4", 0.4), ("E4", 0.4), ("D4", 0.7), ("D4", 0.7),
                              ("D4", 0.7)]
i_cant_get_no_satisfaction_tones = ["D4", "E4", "F4"]

smoke_on_the_water = [("E4", 0.4), ("G4", 0.4), ("A4", 0.4), ("E4", 0.4), ("G4", 0.4), ("A#4", 0.4), ("A4", 0.4),
                      ("E4", 0.4), ("G4", 0.4), ("A4", 0.4), ("E4", 0.4), ("G4", 0.4)]
smoke_on_the_water_tones = ["E4", "G4", "A4", "A#4"]

come_as_you_are = [("B3", 0.4), ("B3", 0.4), ("C4", 0.4), ("C#4", 0.4), ("E4", 0.4), ("C#4", 0.4), ("E4", 0.4),
                   ("C#4", 0.4),
                   ("C#4", 0.4), ("C4", 0.4), ("B3", 0.4), ("F#4", 0.4), ("B3", 0.4), ("B3", 0.4), ("B3", 0.4),
                   ("B3", 0.4),
                   ("C4", 0.4), ("C#4", 0.4), ("E4", 0.4), ("C#4", 0.4), ("E4", 0.4), ("C#4", 0.4), ("C#4", 0.4),
                   ("C4", 0.4),
                   ("B3", 0.4), ("F#4", 0.4), ("B3", 0.4), ("B3", 0.4), ]
come_as_you_are_tones = ["B3", "C4", "C#4", "E4", "F#4"]

another_one_bites_the_dust = [("D3", 0.4), ("D3", 0.4), ("D3", 0.4), ("D3", 0.4), ("D3", 0.4), ("F3", 0.4), ("D3", 0.4),
                              ("G3", 0.4),
                              ("D3", 0.4), ("D3", 0.4), ("D3", 0.4), ("D3", 0.4), ("B3", 0.4), ("F3", 0.4), ("D3", 0.4),
                              ("G3", 0.4)]
another_one_bites_the_dust_tones = ["D3", "F3", "G3"]

practice_tones= ["C4", "D4", "E4", "F4", "G4"]

songs_name_list = ["seven_nation_army", "amours_toujours", "i_cant_get_no_satisfaction", "smoke_on_the_water", "come_as_you_are", "another_one_bites_the_dust"]
song_sounds_list = [seven_nation_army_tones, amours_toujours_tones, i_cant_get_no_satisfaction_tones, smoke_on_the_water_tones, come_as_you_are_tones, another_one_bites_the_dust_tones]

d = {}
d["seven_nation_army"] = seven_nation_army, seven_nation_army_tones
d["amours_toujours"] = amours_toujours, amours_toujours_tones
d["i_cant_get_no_satisfaction"] = i_cant_get_no_satisfaction, i_cant_get_no_satisfaction_tones
d["smoke_on_the_water"] = smoke_on_the_water, smoke_on_the_water_tones
d["come_as_you_are"] = come_as_you_are, come_as_you_are_tones
d["another_one_bites_the_dust"] = another_one_bites_the_dust, another_one_bites_the_dust_tones

def select_new_song():
    random_song = random.choice(list(d.keys()))
    random_values = d.get(random_song)
    return random_song, random_values

def select_practice_tones():
    return practice_tones