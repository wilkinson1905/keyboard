import skip
schem = skip.Schematic('keyboard_.kicad_sch')
print(schem.symbol.SW1.property.Footprint.value)
sw2 = schem.symbol.SW1.clone()
sw2.setAllReferences(f'SW2')
sw2.move(100,100)
schem.symbol.SW2.property.Footprint.value = "kbd_SW:CherryMX_Solder_1.25u"
schem.write('keyboard.kicad_sch')