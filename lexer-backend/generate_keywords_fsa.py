#!/usr/bin/env python3
"""Generate complete keyword FSA code from TD specifications"""

# Based strictly on TD images, define ALL keywords with their exact state paths
keywords = {
    # Format: keyword: (start_state, path_list, final_state)
    'bool': (1, [(1,'o',2), (2,'o',3), (3,'l',4)], 4),
    'break': (1, [(1,'r',6), (6,'e',7), (7,'a',8), (8,'k',9)], 9),
    'case': (11, [(11,'a',12), (12,'s',13), (13,'e',14)], 14),
    'char': (11, [(11,'h',16), (16,'a',17), (17,'r',18)], 18),
    'const': (11, [(11,'o',20), (20,'n',21), (21,'s',22), (22,'t',23)], 23),
    'default': (25, [(25,'e',26), (26,'f',27), (27,'a',28), (28,'u',29), (29,'l',30), (30,'t',31)], 31),
    'do': (25, [(25,'o',33)], 33),
    'double': (25, [(25,'o',33), (33,'u',35), (35,'b',36), (36,'l',37), (37,'e',38)], 38),
    'else': (40, [(40,'l',41), (41,'s',42), (42,'e',43)], 43),
    'false': (45, [(45,'a',46), (46,'l',47), (47,'s',48), (48,'e',49)], 49),
    'float': (45, [(45,'l',51), (51,'o',52), (52,'a',53), (53,'t',54)], 54),
    'for': (45, [(45,'o',56), (56,'r',57)], 57),
    'func': (45, [(45,'u',59), (59,'n',60), (60,'c',61)], 61),
    'global': (63, [(63,'l',64), (64,'o',65), (65,'b',66), (66,'a',67), (67,'l',68)], 68),
    'if': (70, [(70,'f',71)], 71),
    'int': (70, [(70,'n',73), (73,'t',74)], 74),
    'local': (76, [(76,'o',77), (77,'c',78), (78,'a',79), (79,'l',80)], 80),
    'long': (76, [(76,'o',77), (77,'n',82), (82,'g',83)], 83),
    'main': (85, [(85,'a',86), (86,'i',87), (87,'n',88)], 88),
    'return': (90, [(90,'e',91), (91,'t',92), (92,'u',93), (93,'r',94), (94,'n',95)], 95),
    'string': (97, [(97,'t',98), (98,'r',99), (99,'i',100), (100,'n',101), (101,'g',102)], 102),
    'switch': (97, [(97,'w',104), (104,'i',105), (105,'t',106), (106,'c',107), (107,'h',108)], 108),
    'thread': (110, [(110,'h',111), (111,'r',112), (112,'e',113), (113,'a',114), (114,'d',115)], 115),
    'threadln': (110, [(110,'h',111), (111,'r',112), (112,'e',113), (113,'a',114), (114,'d',115), (115,'l',117), (117,'n',118)], 118),
    'trap': (110, [(110,'r',120), (120,'a',121), (121,'p',122)], 122),
    'true': (110, [(110,'r',120), (120,'u',124), (124,'e',125)], 125),
    'using': (127, [(127,'s',128), (128,'i',129), (129,'n',130), (130,'g',131)], 131),
    'var': (133, [(133,'a',134), (134,'r',135)], 135),
    'void': (133, [(133,'o',137), (137,'i',138), (138,'d',139)], 139),
    'weave': (141, [(141,'e',142), (142,'a',143), (143,'v',144), (144,'e',145)], 145),
    'while': (141, [(141,'h',147), (147,'i',148), (148,'l',149), (149,'e',150)], 150),
}

# Build state graph
states = {}
for kw, (start, path, final) in keywords.items():
    for (from_s, char, to_s) in path:
        if from_s not in states:
            states[from_s] = {}
        states[from_s][char] = to_s

# Generate Python match/case code
print("            # BOOL, BREAK")
print("            case 's1':")
print("                match currChar:") 
if 'o' in states.get(1, {}):
    print(f"                    case 'o': return 's{states[1]['o']}'")
if 'r' in states.get(1, {}):
    print(f"                    case 'r': return 's{states[1]['r']}'")
print("                    case _: return 'UNDEFINED'")

# Collect all used state numbers
all_states = set(states.keys())
for kw, (start, path, final) in keywords.items():
    all_states.add(final)
    for (f, c, t) in path:
        all_states.add(t)

for state_num in sorted(all_states):
    if state_num == 1:
        continue  # Already handled
    
    print(f"            case 's{state_num}':")
    
    # Check if final state
    is_final = state_num in [final for kw,(start,path,final) in keywords.items()]
    
    # Check if this state has outgoing transitions
    has_transitions = state_num in states
    
    if is_final and has_transitions:
        # State is both final AND has transitions (e.g., do→double, thread→threadln)
        print("                match currChar:")
        for char, next_state in sorted(states[state_num].items()):
            print(f"                    case '{char}': return 's{next_state}'")
        print("                    case 'ANY': return 'DEFINED'")
        print("                    case _: return 'UNDEFINED'")
    elif is_final:
        # State is only final
        print(f"                # Final state")
        print("                match currChar:")
        print("                    case 'ANY': return 'DEFINED'")
        print("                    case _: return 'UNDEFINED'")
    elif state_num in states:
        print("                match currChar:")
        for char, next_state in sorted(states[state_num].items()):
            print(f"                    case '{char}': return 's{next_state}'")
        print("                    case _: return 'UNDEFINED'")

