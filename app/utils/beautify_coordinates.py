import json

margin = 0.000005

room_data = json.load(open('data/rooms_copy.json'))
border = [0, 0]
border_count = 0

for item in room_data:
    for coords in item['borders']:
        if abs(border[0] - coords[0]) < margin and abs(border[0] - coords[0]) != 0:
            coords[0] = border[0]
            border_count += 1
        if abs(border[1] - coords[1]) < margin and abs(border[1] - coords[1]) != 0:
            coords[1] = border[1]
            border_count += 1
        border = list(coords)
print(f"Border count: {border_count}")

with open('data/rooms_copy.json', 'w') as f:
    json.dump(room_data, f, indent=2)