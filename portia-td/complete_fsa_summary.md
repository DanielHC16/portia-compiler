# PORTIA Transition Diagram Extraction Summary

## Extraction Date
All FSAs extracted from PORTIA Transition Diagram images.

## Files Extracted

### Source Images
- `PORTIA TD- keywords1.jpg` - Keywords Part 1
- `PORTIA TD- keywords2.jpg` - Keywords Part 2
- `PORTIA TD- keywords3.jpg` - Keywords Part 3
- `PORTIA TD- symbols1.jpg` - Symbols Part 1 (Operators)
- `PORTIA TD- symbols2.jpg` - Symbols Part 2 (Delimiters)
- `PORTIA TD- Final - comments and strings.jpg` - Comments and String Literals
- `PORTIA TD- Final - numlitint.jpg` - Integer Literals
- `PORTIA TD- Final - numlitlong.jpg` - Long Literals (Part 1)
- `PORTIA TD- Final - numlitlong2.jpg` - Long Literals (Part 2)
- `PORTIA TD- Final - numlitfloat.jpg` - Float Literals
- `PORTIA TD- Final - numlitdouble.jpg` - Double Literals (Part 1)
- `PORTIA TD- Final - numlitdouble2.jpg` - Double Literals (Part 2)
- `PORTIA TD- Final - idenlit.jpg` - Numerical Continuation

## Extracted FSAs

### Keywords FSAs (3 parts)
1. **Keywords Part 1**: States 0-62 (13 keywords)
2. **Keywords Part 2**: States 0, 127-151 (5 keywords)
3. **Keywords Part 3**: States 0-126 (13 keywords)

**Total**: 31 keywords

### Symbols FSAs (2 parts)
1. **Symbols Part 1**: States 0-189 (18 operator symbols)
2. **Symbols Part 2**: States 0, 190-219 (15 delimiter symbols)

**Total**: 33 symbols

### Literals and Comments FSAs
1. **Comments**: States 168, 271-276 (2 comment types)
2. **String Literals**: States 0, 277-278
3. **Integer Literals**: States 0, 279-298
4. **Long Literals**: States 297-336
5. **Float Literals**: States 337-351
6. **Double Literals**: States 350-367
7. **Numerical Continuation**: States 366-383

## State Statistics

| FSA | Initial State | State Range | Final States Count |
|-----|---------------|-------------|-------------------|
| Keywords Part 1 | 0 | 0-62 | 13 |
| Keywords Part 2 | 0 | 0, 127-151 | 5 |
| Keywords Part 3 | 0 | 0-126 | 13 |
| Symbols Part 1 | 0 | 0-189 | 18 |
| Symbols Part 2 | 0 | 0, 190-219 | 15 |
| Comments | 168 | 168, 271-276 | 2 |
| String Literals | 0 | 0, 277-278 | 1 |
| Integer Literals | 0 | 0, 279-298 | 10 |
| Long Literals | 297 | 297-336 | 19 |
| Float Literals | 337 | 337-351 | 7 |
| Double Literals | 350 | 350-367 | 8 |
| Numerical Continuation | 366 | 366-383 | 8 |

**Total Final States**: 119

## Connection Points

- State 297: Integer FSA → Long FSA
- State 350: Float FSA → Double FSA
- State 366: Double FSA → Continuation FSA

## Output Files

- `portia_fsa.md` - Complete consolidated FSA documentation with state transition tables
- `complete_fsa_summary.md` - This summary document
