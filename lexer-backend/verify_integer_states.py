"""Verify all integer states s278-s297 are implemented with no gaps"""
from app.lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

print("="*80)
print(" "*20 + "INTEGER STATES s278-s297 VERIFICATION")
print("="*80)

print("\nChecking if all states s278-s297 are implemented...")
print("-"*80)

missing_states = []
implemented_states = []

for state_num in range(278, 298):  # 278 to 297 inclusive
    state = f's{state_num}'
    
    # Test if state exists by trying to transition from it
    try:
        # Try with 'numbers' for building states (even numbers)
        # Try with 'ANY' for final states (odd numbers)
        if state_num % 2 == 0:  # Building state
            result = lexer.lex_transition(state, '5')
        else:  # Final state
            result = lexer.lex_transition(state, 'ANY')
        
        if result == 'UNDEFINED':
            # State might not be implemented
            # Double-check by trying the other transition type
            if state_num % 2 == 0:
                result2 = lexer.lex_transition(state, 'ANY')
            else:
                result2 = lexer.lex_transition(state, '5')
            
            if result2 == 'UNDEFINED':
                missing_states.append(state)
                print(f"❌ {state}: NOT IMPLEMENTED (both transitions return UNDEFINED)")
            else:
                implemented_states.append(state)
                print(f"✅ {state}: Implemented")
        else:
            implemented_states.append(state)
            print(f"✅ {state}: Implemented")
    except Exception as e:
        missing_states.append(state)
        print(f"❌ {state}: ERROR - {str(e)}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print(f"\nTotal states to implement: 20 (s278-s297)")
print(f"Implemented: {len(implemented_states)}")
print(f"Missing: {len(missing_states)}")

if missing_states:
    print(f"\n⚠️  Missing states: {', '.join(missing_states)}")
else:
    print(f"\n✅ ALL STATES s278-s297 IMPLEMENTED - NO GAPS!")

print("\n" + "="*80)
print("STATE PATTERN VERIFICATION")
print("="*80)

print("\nExpected pattern from FSA diagram:")
print("  Building states (even): s278, s280, s282, s284, s286, s288, s290, s292, s294, s296")
print("  Final states (odd):     s279, s281, s283, s285, s287, s289, s291, s293, s295, s297")

building_states = [f's{n}' for n in range(278, 298, 2)]
final_states = [f's{n}' for n in range(279, 298, 2)]

print(f"\nBuilding states count: {len(building_states)} (expected: 10)")
print(f"Final states count: {len(final_states)} (expected: 10)")

# Check state transitions
print("\n" + "="*80)
print("TRANSITION VERIFICATION")
print("="*80)

print("\nChecking building → next building transitions (numbers):")
for i in range(len(building_states) - 1):
    curr = building_states[i]
    expected_next = building_states[i + 1]
    actual_next = lexer.lex_transition(curr, '5')
    status = "✅" if actual_next == expected_next else "❌"
    print(f"{status} {curr} --[numbers]--> {actual_next} (expected: {expected_next})")

print("\nChecking building → final transitions (ANY/nbl_delim):")
for i in range(len(building_states)):
    building = building_states[i]
    expected_final = final_states[i]
    actual_final = lexer.lex_transition(building, 'ANY')
    status = "✅" if actual_final == expected_final else "❌"
    print(f"{status} {building} --[ANY]--> {actual_final} (expected: {expected_final})")

print("\nChecking decimal point transitions (building → s314):")
# All building states except s296 should transition to s314 on '.'
for building in building_states[:-1]:  # Exclude s296
    result = lexer.lex_transition(building, '.')
    status = "✅" if result == 's314' else "❌"
    print(f"{status} {building} --[.]--> {result} (expected: s314)")

# s296 should also go to s314
result = lexer.lex_transition('s296', '.')
status = "✅" if result == 's314' else "❌"
print(f"{status} s296 --[.]--> {result} (expected: s314)")

print("\nChecking final states return DEFINED (nbl_delim):")
for final in final_states:
    result = lexer.lex_transition(final, 'ANY')
    status = "✅" if result == 'DEFINED' else "❌"
    print(f"{status} {final} --[ANY]--> {result} (expected: DEFINED)")

print("\n" + "="*80)
print("VERIFICATION COMPLETE")
print("="*80)
