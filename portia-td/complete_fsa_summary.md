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
- `PORTIA TD- Final - idenlit.jpg` - Identifier Literals

## Extracted FSAs

### Keywords FSAs (3 parts)
1. **Keywords Part 1**: States 0-62 (13 keywords)
2. **Keywords Part 2**: States 0-126 (13 keywords)
3. **Keywords Part 3**: States 0, 127-151 (5 keywords)

**Total**: 31 keywords

### Symbols FSAs (2 parts)
1. **Symbols Part 1**: States 0-189 (18 operator symbols)
2. **Symbols Part 2**: States 0, 190-219 (15 delimiter symbols)

**Total**: 33 symbols

### Literals and Comments FSAs
1. **Comments**: States 168, 271-276 (2 comment types)
2. **String Literals**: States 0, 277-278
3. **Integer Literals**: States 0, 279-298, 337
4. **Long Literals**: States 297-336, 337
5. **Float Literals**: States 337-351
6. **Double Literals**: States 350-367, 368-383 (Part 1 and Part 2)
7. **Identifier Literals**: States 0, 220-270

## State Statistics

| FSA | Initial State | State Range | Final States Count |
|-----|---------------|-------------|-------------------|
| Keywords Part 1 | 0 | 0-62 | 13 |
| Keywords Part 2 | 0 | 0-126 | 13 |
| Keywords Part 3 | 0 | 0, 127-151 | 5 |
| Symbols Part 1 | 0 | 0-189 | 18 |
| Symbols Part 2 | 0 | 0, 190-219 | 15 |
| Comments | 168 | 168, 271-276 | 2 |
| String Literals | 0 | 0, 277-278 | 1 |
| Integer Literals | 0 | 0, 279-298, 337 | 10 |
| Long Literals | 297 | 297-336, 337 | 19 |
| Float Literals | 337 | 337-351 | 7 |
| Double Literals | 350 | 350-367, 368-383 | 16 |
| Identifier Literals | 0 | 0, 220-270 | 21 |

**Total Final States**: 140

**Note**: Identifier Literals has 21 unique final states that accept identifiers of 1-25 characters (some states accept multiple lengths).

## Connection Points

- **State 297**: Integer FSA → Long FSA (after 10 digits)
- **State 337**: Shared intermediate state in Integer/Long FSAs; entry point for Float/Double FSAs (reached via decimal point transitions from Long states 313, 315, 317, 319, 321, 323, 325, 327, 329, 331, 333, 335)
- **State 350**: Float FSA → Double FSA Part 1 (after 7 fractional digits)
- **State 366**: Double FSA Part 1 → Part 2 (after 8 fractional digits in Part 1)
- **Identifier FSA**: Starts independently at state 0 (does not connect to numerical literal FSAs)

## Output Files

- `portia_fsa.md` - Complete consolidated FSA documentation with state transition tables
- `complete_fsa_summary.md` - This summary document
