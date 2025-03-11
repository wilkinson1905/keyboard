import skip
import json 
scale = 0.0254
def set_SW_and_D(schem, row_index, col_index):
    length = (550,550)
    SW_at = (250, 150)
    D_at = (450, 350)
    root_at = (1000, 1000)
    if len(schem.global_label.value_matches(f"^COL{col_index}$")) == 0:
        offset = 300
        label = schem.global_label.new()
        label.move((root_at[0]+length[0]*col_index)*scale, (root_at[1]-offset)*scale)
        label.value = f'COL{col_index}'
        wire = schem.wire.new()
        wire.start_at(label)
        wire.delta_x = 0
        wire.delta_y = (6*length[1] + offset+100)*scale
    if len(schem.global_label.value_matches(f"^ROW{row_index}$")) == 0:
        offset = 300
        label = schem.global_label.new()
        label.move((root_at[0]-offset)*scale, (root_at[1]+length[1]*(row_index+1))*scale)
        label.value = f'ROW{row_index}'
        wire = schem.wire.new()
        wire.start_at(label)
        wire.delta_y = 0
        wire.delta_x = (23*length[1] + offset)*scale

    base_at = (root_at[0] + length[0]*col_index, root_at[1] + length[1]*row_index)
    SW_at = (base_at[0]+SW_at[0],base_at[1]+SW_at[1])
    D_at = (base_at[0]+D_at[0], base_at[1]+D_at[1])
    sw = schem.symbol.reference_matches(f"^SW$")[0].clone()
    d = schem.symbol.reference_matches(f"^D$")[0].clone()
    sw.move(SW_at[0]*scale,SW_at[1]*scale)
    d.move(D_at[0]*scale,D_at[1]*scale)
    sw.setAllReferences(f'SW{row_index}-{col_index}')
    sw.property.Footprint.value = "kbd_SW:CherryMX_Solder_1u"
    d.setAllReferences(f'D{row_index}-{col_index}')
    d.property.Footprint.value = "kbd_Parts:Diode_SMD"

    wire = schem.wire.new()
    wire.start_at(sw.pin.n1)
    wire.end_at([base_at[0]*scale, sw.at.value[1]])
    junc = schem.junction.new()
    junc.move(wire.end.value[0], wire.end.value[1])

    wire = schem.wire.new()
    wire.start_at(d.pin.A)
    wire.end_at([d.at.value[0] ,(base_at[1]+length[1])*scale])
    junc = schem.junction.new()
    junc.move(wire.end.value[0], wire.end.value[1])    

    wire = schem.wire.new()
    wire.start_at(sw.pin.n2)
    wire.end_at(d.pin.K)




with open("keyboard-layout-indexed.json","r") as f:
    key_data = json.load(f)
print(key_data)
schem = skip.Schematic('keyboard_template.kicad_sch')
for row_data in key_data:
    for col_data in row_data:
        if isinstance(col_data, dict):
            continue
        row_index, col_index = [int(x) for x in col_data.split(",")]
        set_SW_and_D(schem, row_index, col_index)
schem.write('keyboard.kicad_sch')

# schem = skip.Schematic('keyboard_template.kicad_sch')
# sw2 = schem.symbol.SW.clone()
# sw2.setAllReferences(f'SW2')
# sw2.move(100,100)
# schem.symbol.SW2.property.Footprint.value = "kbd_SW:CherryMX_Solder_1.25u"
# schem.write('keyboard.kicad_sch')