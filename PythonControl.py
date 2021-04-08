"""
Gets movements from a JSON file and execute them.

JSON 
"""


import time
import serial
import json
import winsound

import convert

rule_file = r"C:\Users\Ingvar Pétursson\Documents\Data\År 3\GA\Rörelsemönster\rörelsemönster\ptwo\ptwo_4.json"

with open(rule_file, "r") as file:
    jfile = json.loads(file.read())

print("CURRENT FILE:", rule_file)

"""
repeat = 1
if "repeat" in jfile.keys():
    pattern_repeat = jfile['repeat']
    if pattern_repeat != 0:
        repeat = pattern_repeat
"""

total_steps = 0
multi = 1
rules = list()
"""
for i in range(0, repeat):
    for i in jfile['movement']:
        x = round(multi * i['x'])
        y = round(multi * i['y'])
        rules.append( {"x":x, "y":y} )
"""

cube_sides = float(input("cube side size: "))
stepper_length = 0.01935 #

print(jfile['movement'][0:10])

rules, position = convert.convert(jfile['movement'], jfile['position'], cube_sides, 1, stepper_length)

print(rules)

all_x = list()
all_y = list()

for i in jfile['position']:
    all_x.append(i["x"])
    all_y.append(i["y"])
    
multi = 1
print("x")
print("Max:",max(all_x) * multi)
print("Min:",min(all_x) * multi)
print("\ny")
print("Max:",max(all_y) * multi)
print("Min:",min(all_y) * multi)

await_input = input("Press enter to start...")

for i in rules:
    total_steps += abs(i['x']) + abs(i['y'])

exchangeXandY = False
step_ms = 3 * 0.001 # The amount of time to move one step in milliseconds

print("Print time:", step_ms * total_steps, "s")

port = "COM3" # The port the arduino is connected to
arduino = serial.Serial(port, 9600) # 9600 bits / sec => Arduino char = 10 bits => 960 chars / sec

def move(x, y):
    # Moves the machine x and y steps.
    data = str(x) + ":" + str(y) + "\n"
    arduino.write(data.encode())
    print(data)


def main():

    count = 0
    for i in rules:

        if exchangeXandY == False:
            move(i["x"], i["y"])
        else:
            move(i["y"], i["x"])

        time_cal = (abs(i["x"]) + abs(i["y"])) * step_ms
        count += 1
        print("Sleep:", time_cal, str(round((count / len(rules)) * 100, 2)) + "%")
        time.sleep(time_cal)




for i in range(5, 0, -1):
    print(i)
    time.sleep(1)
print("START:")
print("-" * 20)

main()
print("\a")


# Move back to start location

await_input = input("Press enter to return to start position")

return_back_movement = position[-1]
move(return_back_movement['x'] * -1, return_back_movement['y'] * -1)