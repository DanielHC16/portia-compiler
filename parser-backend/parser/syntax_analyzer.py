from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

# ==================== PREDICT SETS ====================

PREDICT_SETS = {
    # Production 1: <program>
    "program": ["global", "int", "long", "float", "double", "char", "string", "bool", "weave", "id", "func"],
    
    # Productions 2-18: <global_dec> variations
    "global_dec": ["global", "int", "long", "float", "double", "char", "string", "bool", "id", "weave"],
    "global_dec_empty": ["func", "int"],  # Production 18: λ (Follow set)
    "int_global_dec": ["global"],  # Production 2
    "long_global_dec": ["global"],  # Production 3
    "float_global_dec": ["global"],  # Production 4
    "double_global_dec": ["global"],  # Production 5
    "char_global_dec": ["global"],  # Production 6
    "string_global_dec": ["global"],  # Production 7
    "true_global_dec": ["global"],  # Production 8
    "false_global_dec": ["global"],  # Production 9
    "arr_1D": ["int", "long", "float", "double", "char", "string", "bool", "id"],  # Production 10
    "weave_def": ["weave"],  # Production 11
    "int_weave_global_dec": ["global"],  # Production 12
    "long_weave_global_dec": ["global"],  # Production 13
    "float_weave_global_dec": ["global"],  # Production 14
    "double_weave_global_dec": ["global"],  # Production 15
    "char_weave_global_dec": ["global"],  # Production 16
    "string_weave_global_dec": ["global"],  # Production 17
    
    # Productions 33-34: <mutability>
    "mutability": ["var", "const"],
    
    # Productions 35-50: Multiple declarations
    "int_multi_dec": [","],  # Production 35
    "int_multi_dec_empty": [";"],  # Production 36: λ
    "long_multi_dec": [","],  # Production 37
    "long_multi_dec_empty": [";"],  # Production 38: λ
    "float_multi_dec": [","],  # Production 39
    "float_multi_dec_empty": [";"],  # Production 40: λ
    "double_multi_dec": [","],  # Production 41
    "double_multi_dec_empty": [";"],  # Production 42: λ
    "char_multi_dec": [","],  # Production 43
    "char_multi_dec_empty": [";"],  # Production 44: λ
    "string_multi_dec": [","],  # Production 45
    "string_multi_dec_empty": [";"],  # Production 46: λ
    "true_multi_dec": [","],  # Production 47
    "true_multi_dec_empty": [";"],  # Production 48: λ
    "false_multi_dec": [","],  # Production 49
    "false_multi_dec_empty": [";"],  # Production 50: λ
    
    # Productions 51-57: <dtype>
    "dtype": ["int", "long", "float", "double", "char", "string", "bool"],
    
    # Productions 58-65: <value>
    "value": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"],
    
    # Productions 66-81: <arr_1D> variations
    # Productions 66-73: arr_1D_UD types
    "int_arr_1D_UD": ["id", ";"],  # Production 66
    "long_arr_1D_UD": ["id", ";"],  # Production 67
    "float_arr_1D_UD": ["id", ";"],  # Production 68
    "double_arr_1D_UD": ["id", ";"],  # Production 69
    "char_arr_1D_UD": ["id", ";"],  # Production 70
    "string_arr_1D_UD": ["id", ";"],  # Production 71
    "true_arr_1D_UD": ["id", ";"],  # Production 72
    "false_arr_1D_UD": ["id", ";"],  # Production 73
    # Productions 74-81: Explicit type arr_1D
    "arr_1D_int": ["int"],  # Production 74
    "arr_1D_long": ["long"],  # Production 75
    "arr_1D_float": ["float"],  # Production 76
    "arr_1D_double": ["double"],  # Production 77
    "arr_1D_char": ["char"],  # Production 78
    "arr_1D_string": ["string"],  # Production 79
    "arr_1D_true": ["bool"],  # Production 80
    "arr_1D_false": ["bool"],  # Production 81
    
    # Productions 82-97: arr_1D_tail variations
    "int_arr_1D_tail": ["["],  # Production 82
    "int_arr_1D_tail_empty": [";"],  # Production 83: λ
    "long_arr_1D_tail": ["["],  # Production 84
    "long_arr_1D_tail_empty": [";"],  # Production 85: λ
    "float_arr_1D_tail": ["["],  # Production 86
    "float_arr_1D_tail_empty": [";"],  # Production 87: λ
    "double_arr_1D_tail": ["["],  # Production 88
    "double_arr_1D_tail_empty": [";"],  # Production 89: λ
    "char_arr_1D_tail": ["["],  # Production 90
    "char_arr_1D_tail_empty": [";"],  # Production 91: λ
    "string_arr_1D_tail": ["["],  # Production 92
    "string_arr_1D_tail_empty": [";"],  # Production 93: λ
    "true_arr_1D_tail": ["["],  # Production 94
    "true_arr_1D_tail_empty": [";"],  # Production 95: λ
    "false_arr_1D_tail": ["["],  # Production 96
    "false_arr_1D_tail_empty": [";"],  # Production 97: λ
    
    # Production 98: arr_1D_init
    "arr_1D_init": ["="],  # Production 98
    
    # Productions 99-107: elem_1D_list variations
    "elem_1D_list_int": ["(", "intlit"],  # Production 99
    "elem_1D_list_long": ["(", "longlit"],  # Production 100
    "elem_1D_list_float": ["(", "floatlit"],  # Production 101
    "elem_1D_list_double": ["(", "doublelit"],  # Production 102
    "elem_1D_list_char": ["(", "charlit"],  # Production 103
    "elem_1D_list_string": ["(", "stringlit"],  # Production 104
    "elem_1D_list_true": ["(", "true"],  # Production 105
    "elem_1D_list_false": ["(", "false"],  # Production 106
    "elem_1D_list_empty": ["}"],  # Production 107: λ
    
    # Productions 108-109: arr_tpc_type (typecast)
    "arr_tpc_type": ["("],  # Production 108
    "arr_tpc_type_empty": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"],  # Production 109: λ
    
    # Productions 111-126: elem_1D_list_tail variations
    "int_elem_1D_list_tail": [","],  # Production 111
    "int_elem_1D_list_tail_empty": ["}"],  # Production 112: λ
    "long_elem_1D_list_tail": [","],  # Production 113
    "long_elem_1D_list_tail_empty": ["}"],  # Production 114: λ
    "float_elem_1D_list_tail": [","],  # Production 115
    "float_elem_1D_list_tail_empty": ["}"],  # Production 116: λ
    "dbl_elem_1D_list_tail": [","],  # Production 117
    "dbl_elem_1D_list_tail_empty": ["}"],  # Production 118: λ
    "char_elem_1D_list_tail": [","],  # Production 119
    "char_elem_1D_list_tail_empty": ["}"],  # Production 120: λ
    "string_elem_1D_list_tail": [","],  # Production 121
    "string_elem_1D_list_tail_empty": ["}"],  # Production 122: λ
    "true_elem_1D_list_tail": [","],  # Production 123
    "true_elem_1D_list_tail_empty": ["}"],  # Production 124: λ
    "false_elem_1D_list_tail": [","],  # Production 125
    "false_elem_1D_list_tail_empty": ["}"],  # Production 126: λ
    
    # Productions 127-128: Generic elem_1D_list_tail
    "elem_1D_list_tail": [","],  # Production 127
    "elem_1D_list_tail_empty": ["}"],  # Production 128: λ
    
    # Productions 129-144: arr_2D variations
    "int_arr_2D": ["["],  # Production 129
    "int_arr_2D_empty": [";"],  # Production 130: λ
    "long_arr_2D": ["["],  # Production 131
    "long_arr_2D_empty": [";"],  # Production 132: λ
    "float_arr_2D": ["["],  # Production 133
    "float_arr_2D_empty": [";"],  # Production 134: λ
    "double_arr_2D": ["["],  # Production 135
    "double_arr_2D_empty": [";"],  # Production 136: λ
    "char_arr_2D": ["["],  # Production 137
    "char_arr_2D_empty": [";"],  # Production 138: λ
    "string_arr_2D": ["["],  # Production 139
    "string_arr_2D_empty": [";"],  # Production 140: λ
    "true_arr_2D": ["["],  # Production 141
    "true_arr_2D_empty": [";"],  # Production 142: λ
    "false_arr_2D": ["["],  # Production 143
    "false_arr_2D_empty": [";"],  # Production 144: λ
    
    # Productions 145-146: arr_2D_init
    "arr_2D_init": ["="],  # Production 145
    "arr_2D_init_empty": [";"],  # Production 146: λ
    
    # Productions 147-180: arr_2D_UD and arrup_2D variations (abbreviated for space)
    "int_arr_2D_UD": ["="],  # Production 147
    "int_arr_2D_UD_empty": [";"],  # Production 148: λ
    "int_arr_1D_UD_rec": ["id"],  # Production 149
    "int_arr_1D_UD_empty": [";"],  # Production 150: λ
    "long_arr_2D_UD": ["="],  # Production 151 (implied)
    "long_arr_2D_UD_empty": [";"],
    "float_arr_2D_UD": ["="],
    "float_arr_2D_UD_empty": [";"],
    "double_arr_2D_UD": ["="],
    "double_arr_2D_UD_empty": [";"],
    "char_arr_2D_UD": ["="],
    "char_arr_2D_UD_empty": [";"],
    "string_arr_2D_UD": ["="],
    "string_arr_2D_UD_empty": [";"],
    "true_arr_2D_UD": ["="],
    "true_arr_2D_UD_empty": [";"],
    "false_arr_2D_UD": ["="],
    "false_arr_2D_UD_empty": [";"],
    
    # arrup_2D variations
    "int_arrup_2D": ["["],
    "int_arrup_2D_empty": [";"],
    "long_arrup_2D": ["["],
    "long_arrup_2D_empty": [";"],
    "float_arrup_2D": ["["],
    "float_arrup_2D_empty": [";"],
    "double_arrup_2D": ["["],
    "double_arrup_2D_empty": [";"],
    "char_arrup_2D": ["["],
    "char_arrup_2D_empty": [";"],
    "string_arrup_2D": ["["],
    "string_arrup_2D_empty": [";"],
    "true_arrup_2D": ["["],
    "true_arrup_2D_empty": [";"],
    "false_arrup_2D": ["["],
    "false_arrup_2D_empty": [";"],
    
    # elem_2D_list (for nested array initialization)
    "elem_2D_list": ["{"],
    "elem_2D_list_empty": ["}"],
    "elem_2D_list_tail": [","],
    "elem_2D_list_tail_empty": ["}"],
    
    # General array predict sets (used in parser logic)
    "arr_1D": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    "arr_dtype": ["int", "long", "float", "double", "char", "string", "bool"],
    "elem_1D_list": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "("],
    
    # Productions 199-210: Weaves (Structures)
    "weave_def": ["weave"],  # Production 199
    "field_list": ["int", "long", "float", "double", "char", "string", "bool", "id"],  # Production 200
    "field_list_empty": ["}"],  # Production 201: λ
    "field_dec": ["int", "long", "float", "double", "char", "string", "bool", "id"],  # Production 202
    "field_dec_cont": [","],  # Production 203
    "field_dec_cont_empty": [";"],  # Production 204: λ
    "field_array_spec_opt": ["["],  # Production 205
    "field_array_spec_opt_empty": [",", ";"],  # Production 206: λ
    "field_type_dtype": ["int", "long", "float", "double", "char", "string", "bool"],  # Production 207
    "field_type_weave": ["id"],  # Production 208
    "field_type": ["int", "long", "float", "double", "char", "string", "bool", "id"],  # Combined 207-208
    "weave_id": ["id"],  # Production 209
    
    # Productions 211-212: Functions
    "function": ["func"],  # Production 211
    "function_empty": ["int"],  # Production 212: λ (main_func starts with int)
    
    # Production 213: Function Definition
    "function_def": ["func"],  # Production 213
    
    # Productions 214-216: Return Type
    "ret_type_dtype": ["int", "long", "float", "double", "char", "string", "bool"],  # Production 214
    "ret_type_weave": ["id"],  # Production 215
    "ret_type_void": ["void"],  # Production 216
    "ret_type": ["int", "long", "float", "double", "char", "string", "bool", "id", "void"],  # Combined 214-216
    
    # Productions 217-219: Return Structure (array specs)
    "ret_struct": ["[", "."],  # Productions 217-218
    "ret_struct_empty": ["id"],  # Production 219: λ
    
    # Productions 220-221: ret_2D
    "ret_2D": ["["],  # Production 220
    "ret_2D_empty": ["id"],  # Production 221: λ
    
    # Productions 222-231: Parameters
    "param": ["int", "long", "float", "double", "char", "string", "bool", "id"],  # Production 222
    "param_empty": [")"],  # Production 223: λ
    "param_type_dtype": ["int", "long", "float", "double", "char", "string", "bool"],  # Production 224
    "param_type_weave": ["id"],  # Production 225
    "param_type": ["int", "long", "float", "double", "char", "string", "bool", "id"],  # Combined 224-225
    "param_struct": ["["],  # Production 226
    "param_struct_empty": [",", ")", "id"],  # Production 227: λ
    "param_2D": ["["],  # Production 228
    "param_2D_empty": [",", ")", "id"],  # Production 229: λ
    "param_cont": [","],  # Production 230
    "param_cont_empty": [")"],  # Production 231: λ
    
    # Production 232: Function Body
    "function_body": ["using", "local", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", 
                      "--", "++", "stringlit", "charlit", "true", "false", "thread", "threadln", 
                      "trap", "if", "switch", "for", "while", "do", "int", "long", "float", 
                      "double", "char", "string", "bool", "return"],
    
    # Productions 233-234: Import Block
    "import_block": ["using"],  # Production 233
    "import_block_empty": ["local", "!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", 
                          "--", "++", "stringlit", "charlit", "true", "false", "thread", "threadln", 
                          "trap", "if", "switch", "for", "while", "do", "int", "long", "float", 
                          "double", "char", "string", "bool", "return"],  # Production 234: λ
    
    # Production 235: Import Statement
    "import_stmt": ["using"],  # Production 235
    
    # Productions 236-237: Import Continuation
    "import_cont": [","],  # Production 236
    "import_cont_empty": [";"],  # Production 237: λ
    
    # Productions 238-241: Local Block
    "local_block": ["local", "int", "long", "float", "double", "char", "string", "bool", "id"],  # Productions 238-240
    "local_block_empty": ["!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", "--", "++", 
                         "stringlit", "charlit", "true", "false", "thread", "threadln", "trap", 
                         "if", "switch", "for", "while", "do", "int", "long", "float", "double", 
                         "char", "string", "bool", "return", "}", "break"],  # Production 241: λ
    
    # Productions 242-249: Local Declaration Types
    "local_dec": ["local"],  # Productions 242-249 (all start with local)
    "int_local_dec": ["local"],  # Production 242
    "long_local_dec": ["local"],  # Production 243
    "float_local_dec": ["local"],  # Production 244
    "double_local_dec": ["local"],  # Production 245
    "char_local_dec": ["local"],  # Production 246
    "string_local_dec": ["local"],  # Production 247
    "true_local_dec": ["local"],  # Production 248
    "false_local_dec": ["local"],  # Production 249
    
    # Productions 250-257: Specific Local Declarations
    # Production 250: int_local_dec → local <mutability> int id = intlit <int_multi_dec>;
    # Production 251: long_local_dec → local <mutability> long id = longlit <multi_dec>;
    # Production 252: float_local_dec → local <mutability> float id = floatlit <multi_dec>;
    # Production 253: double_local_dec → local <mutability> double id = doublelit <multi_dec>;
    # Production 254: char_local_dec → local <mutability> char id = charlit <multi_dec>;
    # Production 255: string_local_dec → local <mutability> string id = stringlit <multi_dec>;
    # Production 256: true_local_dec → local <mutability> bool id = true <multi_dec>;
    # Production 257: false_local_dec → local <mutability> bool id = false <multi_dec>;
    
    # Productions 258-265: Empty Local Declarations (λ - Follow sets)
    "int_local_dec_empty": ["local", "!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", 
                           "--", "++", "stringlit", "charlit", "true", "false", "thread", "threadln", 
                           "trap", "if", "switch", "for", "while", "do", "int", "long", "float", 
                           "double", "char", "string", "bool", "return"],  # Production 258: λ
    "long_local_dec_empty": ["local", "!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", 
                            "--", "++", "stringlit", "charlit", "true", "false", "thread", "threadln", 
                            "trap", "if", "switch", "for", "while", "do", "int", "long", "float", 
                            "double", "char", "string", "bool", "return"],  # Production 259: λ
    "float_local_dec_empty": ["local", "!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", 
                             "--", "++", "stringlit", "charlit", "true", "false", "thread", "threadln", 
                             "trap", "if", "switch", "for", "while", "do", "int", "long", "float", 
                             "double", "char", "string", "bool", "return"],  # Production 260: λ
    "double_local_dec_empty": ["local", "-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                              "charlit", "true", "false", "thread", "threadln", "trap", "if", "switch", 
                              "for", "while", "do", "int", "long", "float", "double", "char", "string", 
                              "bool", "return"],  # Production 261: λ
    "char_local_dec_empty": ["local", "-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                            "charlit", "true", "false", "thread", "threadln", "trap", "if", "switch", 
                            "for", "while", "do", "int", "long", "float", "double", "char", "string", 
                            "bool", "return"],  # Production 262: λ
    "string_local_dec_empty": ["local", "-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                              "charlit", "true", "false", "thread", "threadln", "trap", "if", "switch", 
                              "for", "while", "do", "int", "long", "float", "double", "char", "string", 
                              "bool", "return"],  # Production 263: λ
    "true_local_dec_empty": ["local", "-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                            "charlit", "true", "false", "thread", "threadln", "trap", "if", "switch", 
                            "for", "while", "do", "int", "long", "float", "double", "char", "string", 
                            "bool", "return"],  # Production 264: λ
    "false_local_dec_empty": ["local", "-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                             "charlit", "true", "false", "thread", "threadln", "trap", "if", "switch", 
                             "for", "while", "do", "int", "long", "float", "double", "char", "string", 
                             "bool", "return"],  # Production 265: λ
    
    # Productions 266-267: Multi Declaration
    "multi_dec": [","],  # Production 266
    "multi_dec_empty": [";"],  # Production 267: λ
    
    # Production 268: Weave Local Declaration
    "weave_local_dec": ["local"],  # Production 268
    
    # Productions 269-270: Statement List
    "statement_list": ["local", "!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", "--", "++", 
                      "stringlit", "charlit", "true", "false", "thread", "threadln", "trap", "if", 
                      "switch", "for", "while", "do", "int", "long", "float", "double", "char", 
                      "string", "bool", "return", "break", "}"],  # Production 269
    "statement_list_empty": ["return", "}"],  # Production 270: λ
    
    # Productions 271-276: Statement Types
    "statement": ["!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", "--", "++", 
                 "stringlit", "charlit", "true", "false", "thread", "threadln", "trap", "if", 
                 "switch", "for", "while", "do", "int", "long", "float", "double", "char", 
                 "string", "bool"],  # Combined productions 271-275
    "statement_expression": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
                           "stringlit", "charlit", "true", "false"],  # Production 271
    "statement_io": ["thread", "threadln", "trap"],  # Production 272
    "statement_assign": ["id"],  # Production 273
    "statement_ctrl": ["if", "switch", "for", "while", "do"],  # Production 274
    "statement_arr": ["int", "long", "float", "double", "char", "string", "bool"],  # Production 275
    "statement_empty": ["!", "-", "(", "intlit", "longlit", "floatlit", "doublelit", "id", "--", "++", 
                       "stringlit", "charlit", "true", "false", "thread", "threadln", "trap", "if", 
                       "switch", "for", "while", "do", "int", "long", "float", "double", "char", 
                       "string", "bool", "return", "}"],  # Production 276: λ
    
    # Production 277: Expression
    "expression": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
                  "stringlit", "charlit", "true", "false"],  # Production 277
    
    # Production 278: Logical Expression
    "logical_expr": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
                    "stringlit", "charlit", "true", "false"],  # Production 278
    
    # Productions 279-281: Logical Expression Continuation
    "logical_expr_cont": ["&&", "||"],  # Productions 279-280
    "logical_expr_cont_empty": [";"],  # Production 281: λ
    
    # Production 282: Relational Expression
    "rel_expr": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
                "stringlit", "charlit", "true", "false"],  # Production 282
    
    # Productions 283-289: Relational Expression Continuation
    "rel_expr_cont": ["==", "!=", ">", "<", ">=", "<="],  # Productions 283-288
    "rel_expr_cont_empty": [";"],  # Production 289: λ
    
    # Production 290: Arithmetic Expression
    "arith_expr": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
                  "stringlit", "charlit", "true", "false"],  # Production 290
    
    # Productions 291-293: Add/Minus Continuation
    "add_min_cont": ["+", "-"],  # Productions 291-292
    "add_min_cont_empty": ["==", "!=", ">", "<", ">=", "<=", "&&", "||", ";", ")"],  # Production 293: λ
    
    # Production 294: Term
    "term": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
            "stringlit", "charlit", "true", "false"],  # Production 294
    
    # Productions 295-298: Mult/Div/Modulo Continuation
    "mult_div_modulo_cont": ["*", "/", "%"],  # Productions 295-297
    "mult_div_modulo_cont_empty": ["+", "-", "==", "!=", ">", "<", ">=", "<=", "&&", "||", ";", ")"],  # Production 298: λ
    
    # Production 299: Factor
    "factor": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
              "stringlit", "charlit", "true", "false"],  # Production 299
    
    # Productions 300-304: Primary
    "primary": ["!", "-", "(", "id", "++", "--", "intlit", "floatlit", "longlit", "doublelit", 
               "stringlit", "charlit", "true", "false"],  # Productions 300-304
    "primary_not": ["!"],  # Production 300
    "primary_neg": ["-"],  # Production 301
    "primary_cast": ["("],  # Production 302
    "primary_atom": ["intlit", "floatlit", "--", "++", "id", "stringlit", "charlit", "true", "false"],  # Production 303
    "primary_paren": ["intlit", "longlit", "floatlit", "doublelit", "--", "++", "id", "stringlit", 
                     "charlit", "true", "false"],  # Production 304
    
    # Production 305: Cast Value
    "cast_val": ["("],  # Production 305: cast_val → ( <dtype> ) <factor>
    
    # Productions 306-313: Atoms
    "atom": ["id", "--", "++", "intlit", "longlit", "floatlit", "doublelit", "stringlit", "charlit", "true", "false"],  # Production 306-313
    "id_atom": ["id"],  # Production 314: id_atom → <iden>
    "incdec_atom": ["--", "++"],  # Production 315: incdec_atom → <pre_incdec> | <post_incdec>
    "pre_incdec": ["--", "++"],  # Production 316-317: pre_incdec → ++ id | -- id
    "post_incdec": ["id"],  # Production 318-319: post_incdec → id ++ | id --
    "num_lit_type": ["intlit", "longlit", "floatlit", "doublelit"],  # Production 320-324
    
    # Productions 325-327: I/O Statements
    "I/O_stmt": ["trap", "thread", "threadln"],  # Production 325-327: I/O_stmt → <input_stmt> | <output_stmt>
    "input_stmt": ["trap"],  # Production 328: input_stmt → trap ( <iden> )
    "output_stmt": ["thread", "threadln"],  # Production 334-335: output_stmt → thread(...) | threadln(...)
    
    # Productions 329-333: Identifier
    "iden": ["id"],  # Production 329: iden → id<iden_val>
    "iden_val": ["[", ")"],  # Production 330-333: iden_val → <isize> | λ
    "iden_val_empty": [")"],  # Production 333: iden_val → λ
    "isize": ["["],  # Production 331-332: isize → [ <size> ]
    "isize_empty": [")"],  # Production 333: iden_val → λ (when no isize)
    
    # Productions 336-343: Expression1
    "expression1": ["intlit", "longlit", "floatlit", "doublelit", "id", "--", "++", "stringlit", "charlit", "true", "false", "("],  # Production 336-342: expression1 → <expression><expr1_cont>
    "expr1_cont": [","],  # Production 343: expr1_cont → , <expression1>
    "expr1_cont_empty": [")"],  # Production 343: expr1_cont → λ
    
    # Productions 344-350: String Expressions and Values
    "string_expr": ["stringlit", "(", "id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "true", "false"],  # Production 344: string_expr → <string_value>..<string_value>
    "string_value": ["stringlit", "(", "id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "true", "false"],  # Production 345-350
    "typecast_expr": ["("],  # Production 347: typecast_expr → ( <dtype> ) <value>
    
    # Productions 351-356: Function Calls
    "function_call": ["id"],  # Production 351: function_call → id ( <arg> ) <multi_arg>
    "arg": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "id"],  # Production 352-353: arg → <value> | id
    "arg_empty": [",", ")"],  # Production 354: arg → λ
    "multi_arg": [","],  # Production 355: multi_arg → , <arg> <multi_arg>
    "multi_arg_empty": [")"],  # Production 356: multi_arg → λ
    
    # Productions 357-364: Identifier (iden1)
    "iden1": ["id"],  # Production 357: iden1 → id<iden1_weave>
    "iden1_weave": ["[", "."],  # Production 358-359: iden1_weave → [<size>]<iden1_tail> | .id<iden1_cont>
    "iden1_tail": ["["],  # Production 360: iden1_tail → [<size>]
    "iden1_tail_empty": [")"],  # Production 361: iden1_tail → λ
    "iden1_cont": [","],  # Production 362: iden1_cont → , id . id <iden1_cont>
    "iden1_cont_empty": [")"],  # Production 363: iden1_cont → λ
    
    # Productions 364-375: Assignment Statements
    "assign_stmt": ["id"],  # Production 364-365: assign_stmt → <iden1><assign_stmt_op> | id<array_spec_opt><assign_stmt_op>
    "array_spec_opt": ["["],  # Production 366: array_spec_opt → [<size>]<array_spec_2D>
    "array_spec_opt_empty": ["=", "+=", "-=", "*=", "/=", "%="],  # Production 367: array_spec_opt → λ
    "array_spec_2D": ["["],  # Production 368: array_spec_2D → [<size>]
    "array_spec_2D_empty": ["=", "+=", "-=", "*=", "/=", "%="],  # Production 369: array_spec_2D → λ
    "assign_stmt_op": ["=", "+=", "-=", "*=", "/=", "%="],  # Production 370-375
    
    # Productions 376-379: Control Structures
    "ctrl_struct": ["if", "switch", "for", "while", "do"],  # Production 376-377: ctrl_struct → <conditional_stmt> | <loop_stmt>
    "conditional_stmt": ["if", "switch"],  # Production 378-379: conditional_stmt → <if_stmt> | <switch_stmt>
    "loop_stmt": ["for", "while", "do"],  # Production 377: loop_stmt
    
    # Productions 380-388: If Statements
    "if_stmt": ["if"],  # Production 380: if_stmt → if(<condition>){<ctrl_body><ret_ctrl_body>}<else_if_ei_stmt>
    "condition": ["-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", "charlit", "true", "false"],  # Production 381: condition → <logical_expr>
    "ctrl_body": ["local", "-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                 "charlit", "true", "false", "trap", "thread", "threadln", "if", "switch", 
                 "for", "while", "do", "int", "long", "float", "double", "char", "string", "bool", "return", "}", "break"],  # Production 382: ctrl_body
    "ret_ctrl_body": ["return"],  # Production 383: ret_ctrl_body → <ret_stmt>
    "ret_ctrl_body_empty": ["}", "break"],  # Production 384: ret_ctrl_body → λ
    "else_if_ei_stmt": ["else"],  # Production 385: else_if_ei_stmt → else <else_stmt>
    "else_if_ei_stmt_empty": ["-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                              "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                              "switch", "for", "while", "do", "int", "long", "float", "double", 
                              "char", "string", "bool", "return"],  # Production 386: else_if_ei_stmt → λ
    "else_stmt": ["if", "return", "local", "{", "-", "(", "intlit", "floatlit", "id", "--", "++", "stringlit", 
                 "charlit", "true", "false", "trap", "thread", "threadln", "switch", 
                 "for", "while", "do", "int", "long", "float", "double", "char", "string", "bool"],  # Production 387-388
    
    # Productions 389-394: Switch Statements
    "switch_stmt": ["switch"],  # Production 389: switch_stmt → switch(<switch_val>) { <case_stmt> <default_stmt>}
    "switch_val": ["id", "intlit", "stringlit", "!", "-", "(", "++", "--", "longlit", "floatlit", "doublelit", "charlit", "true", "false"],  # Production 390-393
    "case_stmt": ["case"],  # Production 394: case_stmt → case<case_val>: <ctrl_body> break; <case_stmt_cont>
    "case_stmt_cont": ["case"],  # Production 395: case_stmt_cont → <case_stmt><case_stmt_cont>
    "case_stmt_cont_empty": ["default", "}"],  # Production 396: case_stmt_cont → λ
    "case_val": ["intlit", "longlit", "charlit", "true", "false"],  # Production 397: case_val → <unique_val>
    "unique_val": ["intlit", "longlit", "charlit", "true", "false"],  # Production 398-402
    "default_stmt": ["default"],  # Production 403: default_stmt → default : <ctrl_body>
    "default_stmt_empty": ["}"],  # Production 404: default_stmt → λ
    
    # Productions 405-419: Loop Statements
    "loop_stmt": ["for", "while", "do"],  # Production 405-407: loop_stmt → <for_stmt> | <while_stmt> | <do_stmt>
    "for_stmt": ["for"],  # Production 408: for_stmt → for(<initializer>;<condition>;<update>){<ctrl_body>}
    "initializer": ["local", "id"],  # Production 409-410: initializer → local var <dtype> id = <value> <multi_dec> | <assign_stmt>
    "initializer_empty": [";"],  # Production 411: initializer → λ
    "update": ["++", "--", "id"],  # Production 412-414: update → ++id | --id | id<up_post>
    "update_empty": [")"],  # Production 415: update → λ
    "up_post": ["++", "--"],  # Production 416-417: up_post → ++ | --
    "while_stmt": ["while"],  # Production 418: while_stmt → while (<condition>){<ctrl_body>}
    "do_stmt": ["do"],  # Production 419: do_stmt → do{<ctrl_body>} while(<condition>);
    
    # Productions 420-424: Return Statements
    "ret_stmt": ["return"],  # Production 420: ret_stmt → return<ret_value>;
    "ret_value": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", 
                 "true", "false", "id", "-", "(", "--", "++"],  # Production 421-423: ret_value → <value> | id | <logical_expr>
    "ret_value_empty": [";"],  # Production 424: ret_value → λ
    
    # Productions 425-426: Main Function
    "main_func": ["int"],  # Production 425: main_func → int main(){<main_body>}
    "main_body": ["using", "local", "-", "(", "intlit", "floatlit", "id", "--", "++", 
                 "stringlit", "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                 "switch", "for", "while", "do", "int", "long", "float", "double", "char", 
                 "string", "bool", "return"],  # Production 426: main_body
}


# ==================== AST NODE CLASSES ====================
# Abstract Syntax Tree node definitions for PORTIA language constructs

@dataclass
class ASTNode:
    # Base class for all AST nodes
    pass

# -------------------- Value Nodes --------------------

@dataclass
class NumberNode(ASTNode):
    # Represents numeric literals (int, long, float, double)
    value: str
    token_type: str  # "intlit", "longlit", "floatlit", "doublelit"
    line: int
    column: int
    
    def __repr__(self):
        return f"Number({self.value}, type={self.token_type})"

@dataclass
class StringNode(ASTNode):
    # Represents string literals
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"String({repr(self.value)})"

@dataclass
class CharNode(ASTNode):
    # Represents character literals
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Char({repr(self.value)})"

@dataclass
class BoolNode(ASTNode):
    # Represents boolean literals (true/false)
    value: bool
    line: int
    column: int
    
    def __repr__(self):
        return f"Bool({self.value})"

@dataclass
class IdentifierNode(ASTNode):
    # Represents identifiers (variable names, function names, etc.)
    name: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Id({self.name})"

# -------------------- Expression Nodes --------------------

@dataclass
class BinaryOpNode(ASTNode):
    # Represents binary operations (arithmetic, relational, logical)
    left: ASTNode
    operator: str
    right: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"BinOp({self.left} {self.operator} {self.right})"

@dataclass
class UnaryOpNode(ASTNode):
    # Represents unary operations (-, !, ++, --)
    operator: str
    operand: ASTNode
    is_prefix: bool  # True for prefix (++i), False for postfix (i++)
    line: int
    column: int
    
    def __repr__(self):
        if self.is_prefix:
            return f"UnaryOp({self.operator}{self.operand})"
        else:
            return f"UnaryOp({self.operand}{self.operator})"

@dataclass
class CastNode(ASTNode):
    # Represents type casting: (type)expression
    target_type: str
    expression: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"Cast({self.target_type})({self.expression})"

@dataclass
class ArrayAccessNode(ASTNode):
    # Represents array element access: arr[index] or arr[i][j]
    array: ASTNode  # Can be IdentifierNode or another expression
    index1: ASTNode
    index2: Optional[ASTNode] = None  # For 2D arrays
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        if self.index2:
            return f"ArrayAccess({self.array}[{self.index1}][{self.index2}])"
        return f"ArrayAccess({self.array}[{self.index1}])"

@dataclass
class WeaveAccessNode(ASTNode):
    # Represents weave member access: weaveVar.field
    weave: ASTNode
    field: str
    line: int
    column: int
    
    def __repr__(self):
        return f"WeaveAccess({self.weave}.{self.field})"

@dataclass
class FunctionCallNode(ASTNode):
    # Represents function calls: func(arg1, arg2, ...)
    function_name: str
    arguments: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"Call({self.function_name}({args_str}))"

@dataclass
class StringConcatNode(ASTNode):
    # Represents string concatenation: str1..str2
    left: ASTNode
    right: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"StringConcat({self.left}..{self.right})"

# -------------------- Declaration Nodes --------------------

@dataclass
class VariableDeclarationNode(ASTNode):
    # Represents variable declarations: global/local var/const type id = value
    scope: str  # "global" or "local"
    mutability: str  # "var" or "const"
    data_type: str
    identifier: str
    initial_value: Optional[ASTNode] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        init = f" = {self.initial_value}" if self.initial_value else ""
        return f"VarDecl({self.scope} {self.mutability} {self.data_type} {self.identifier}{init})"

@dataclass
class MultipleDeclarationNode(ASTNode):
    # Represents multiple variable declarations in one statement
    declarations: List[VariableDeclarationNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"MultiDecl({len(self.declarations)} vars)"

@dataclass
class ArrayDeclarationNode(ASTNode):
    # Represents array declarations: type id[size] or type id[size1][size2]
    scope: str  # "global" or "local"
    data_type: str
    identifier: str
    size1: Optional[ASTNode]  # Can be intlit or None
    size2: Optional[ASTNode] = None  # For 2D arrays
    initial_values: Optional[List[ASTNode]] = None  # Initialization list
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        dim = f"[{self.size1}]"
        if self.size2:
            dim += f"[{self.size2}]"
        init = f" = {self.initial_values}" if self.initial_values else ""
        return f"ArrayDecl({self.scope} {self.data_type} {self.identifier}{dim}{init})"

@dataclass
class WeaveDefinitionNode(ASTNode):
    # Represents weave (struct) definitions
    name: str
    fields: List['WeaveFieldNode']
    line: int
    column: int
    
    def __repr__(self):
        return f"WeaveDef({self.name}, {len(self.fields)} fields)"

@dataclass
class WeaveFieldNode(ASTNode):
    # Represents a field in a weave definition
    field_type: str
    field_name: str
    is_array: bool = False
    array_size: Optional[int] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        arr = f"[{self.array_size}]" if self.is_array else ""
        return f"Field({self.field_type} {self.field_name}{arr})"

@dataclass
class FunctionDefinitionNode(ASTNode):
    # Represents function definitions
    return_type: str
    name: str
    parameters: List['ParameterNode']
    body: 'FunctionBodyNode'
    line: int
    column: int
    
    def __repr__(self):
        params = ", ".join(str(p) for p in self.parameters)
        return f"FuncDef({self.return_type} {self.name}({params}))"

@dataclass
class ParameterNode(ASTNode):
    # Represents function parameters
    param_type: str
    name: str
    is_array: bool = False
    is_2d_array: bool = False
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        arr = "[][]" if self.is_2d_array else "[]" if self.is_array else ""
        return f"Param({self.param_type} {self.name}{arr})"

@dataclass
class FunctionBodyNode(ASTNode):
    # Represents function body: imports, local declarations, statements, return
    imports: List['UsingStatementNode']
    local_declarations: List[ASTNode]
    statements: List[ASTNode]
    return_statement: Optional['ReturnStatementNode'] = None
    
    def __repr__(self):
        return f"FuncBody({len(self.statements)} stmts)"

# -------------------- Statement Nodes --------------------

@dataclass
class AssignmentStatementNode(ASTNode):
    # Represents assignment statements: id = expr, id += expr, etc.
    target: ASTNode  # Can be Id, ArrayAccess, or WeaveAccess
    operator: str  # "=", "+=", "-=", "*=", "/=", "%="
    value: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"Assign({self.target} {self.operator} {self.value})"

@dataclass
class InputStatementNode(ASTNode):
    # Represents input statements: trap(variable)
    target: ASTNode  # Variable to store input
    line: int
    column: int
    
    def __repr__(self):
        return f"Input(trap({self.target}))"

@dataclass
class OutputStatementNode(ASTNode):
    # Represents output statements: thread(...) or threadln(...)
    is_newline: bool  # True for threadln, False for thread
    expressions: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        stmt = "threadln" if self.is_newline else "thread"
        return f"Output({stmt}({len(self.expressions)} expr))"

@dataclass
class ReturnStatementNode(ASTNode):
    # Represents return statements
    value: Optional[ASTNode] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        val = f"({self.value})" if self.value else "(void)"
        return f"Return{val}"

@dataclass
class BreakStatementNode(ASTNode):
    # Represents break statements
    line: int
    column: int
    
    def __repr__(self):
        return "Break"

@dataclass
class ContinueStatementNode(ASTNode):
    # Represents continue statements
    line: int
    column: int
    
    def __repr__(self):
        return "Continue"

@dataclass
class UsingStatementNode(ASTNode):
    # Represents using/import statements
    modules: List[str]  # List of module names
    line: int
    column: int
    
    def __repr__(self):
        return f"Using({', '.join(self.modules)})"

# -------------------- Control Structure Nodes --------------------

@dataclass
class IfStatementNode(ASTNode):
    # Represents if statements with optional else/else-if chains
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        else_part = f", else({len(self.else_body)} stmts)" if self.else_body else ""
        return f"If({self.condition}, then({len(self.then_body)} stmts){else_part})"

@dataclass
class SwitchStatementNode(ASTNode):
    # Represents switch statements
    switch_value: ASTNode
    cases: List['CaseNode']
    default_case: Optional['DefaultCaseNode'] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"Switch({self.switch_value}, {len(self.cases)} cases)"

@dataclass
class CaseNode(ASTNode):
    # Represents a case in a switch statement
    case_value: ASTNode
    statements: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"Case({self.case_value}: {len(self.statements)} stmts)"

@dataclass
class DefaultCaseNode(ASTNode):
    # Represents default case in a switch statement
    statements: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"Default({len(self.statements)} stmts)"

@dataclass
class ForLoopNode(ASTNode):
    # Represents for loops
    initializer: Optional[ASTNode]  # Can be VarDecl or Assignment
    condition: Optional[ASTNode]
    update: Optional[ASTNode]
    body: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"For(init={self.initializer}, cond={self.condition}, update={self.update})"

@dataclass
class WhileLoopNode(ASTNode):
    # Represents while loops
    condition: ASTNode
    body: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"While({self.condition})"

@dataclass
class DoWhileLoopNode(ASTNode):
    # Represents do-while loops
    body: List[ASTNode]
    condition: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"DoWhile({self.condition})"

# -------------------- Program Structure Nodes --------------------

@dataclass
class ProgramNode(ASTNode):
    # Root node representing the entire PORTIA program
    global_declarations: List[ASTNode]
    functions: List[FunctionDefinitionNode]
    main_function: 'MainFunctionNode'
    
    def __repr__(self):
        return f"Program({len(self.global_declarations)} globals, {len(self.functions)} funcs)"

@dataclass
class MainFunctionNode(ASTNode):
    # Represents the main function
    body: FunctionBodyNode
    line: int
    column: int
    
    def __repr__(self):
        return f"Main()"

@dataclass
class ArrayLiteralNode(ASTNode):
    # Represents an array or struct literal initialization like {1, 2, 3} or {0, 0}
    elements: List[Any]  # Can be expressions or nested lists for 2D arrays
    line: int
    column: int
    
    def __repr__(self):
        return f"ArrayLiteral({len(self.elements)} elements)"

# ==================== PARSER CLASS ====================

class Parser:
    # PORTIA Recursive Descent Parser

    # Implements LL(1) parsing based on CFG and predict sets
    
    def __init__(self):
        self.tokens: List[Dict[str, Any]] = []
        self.current = 0
        self.errors: List[Dict[str, Any]] = []
        self.source_lines: List[str] = []
    
    # -------------------- Token Management --------------------
    
    def current_token(self) -> Optional[Dict[str, Any]]:
        # Get the current token without consuming it
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def peek(self, offset: int = 1) -> Optional[Dict[str, Any]]:
        # Look ahead at token at current + offset position
        pos = self.current + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Dict[str, Any]:
        # Consume and return the current token
        token = self.current_token()
        if token:
            self.current += 1
        return token
    
    def match(self, expected_type: str) -> bool:
        # Check if current token matches expected type
        token = self.current_token()
        if not token:
            return False
        return token.get("type") == expected_type or token.get("lexeme") == expected_type
    
    def expect(self, expected: str, consume: bool = True) -> Optional[Dict[str, Any]]:
        # Expect a specific token type or lexeme.

        # If consume=True, advance past it. Otherwise just check.

        # Returns the token if match, None otherwise (and adds error).

        # Args:

        # expected: Token type or lexeme to expect

        # consume: Whether to consume the token if it matches
        token = self.current_token()
        if not token:
            message = f"Expected '{expected}'"
            self.add_error(message, None, expected)
            return None
        
        if token.get("type") == expected or token.get("lexeme") == expected:
            return self.advance() if consume else token
        else:
            message = f"Expected '{expected}'"
            self.add_error(message, token, expected)
            return None
    
    def match_predict_set(self, non_terminal: str) -> bool:
        # Check if current token is in the predict set for a non-terminal
        if non_terminal not in PREDICT_SETS:
            return False
        
        token = self.current_token()
        if not token:
            return False
        
        predict_set = PREDICT_SETS[non_terminal]
        return token.get("type") in predict_set or token.get("lexeme") in predict_set
    
    def expect_predict_set(self, non_terminal: str) -> bool:
        # Check if current token matches PREDICT set for non-terminal.

        # If not, generates error showing all expected tokens from PREDICT set.

        # Args:

        # non_terminal: Non-terminal name to check PREDICT set for

        # Returns:

        # True if match, False otherwise (error added)
        if self.match_predict_set(non_terminal):
            return True
        
        # Get PREDICT set for error message
        predict_set = PREDICT_SETS.get(non_terminal, [])
        token = self.current_token()
        
        if token:
            token_str = token.get('lexeme', token.get('type', 'unknown'))
            message = f"Expected {non_terminal} but got '{token_str}'"
        else:
            message = f"Expected {non_terminal} but reached end of input"
        
        self.add_error(message, token, predict_set)
        return False
    
    # -------------------- Error Handling --------------------
    
    def add_error(self, message: str, token: Optional[Dict[str, Any]] = None, expected: Optional[Union[str, List[str]]] = None):
        # Add a syntax error to the error list
        # Args:
        #   message: Primary error message
        #   token: Token where error occurred
        #   expected: Expected token(s) - single string or list for PREDICT sets
        # Build error message in format: Unexpected: '<token>' Expected: '<expected>'
        if token and expected:
            token_str = token.get('lexeme', token.get('type', 'unknown'))
            
            if isinstance(expected, list):
                # PREDICT set - show all possible tokens
                if len(expected) == 1:
                    expected_str = f"'{expected[0]}'"
                elif len(expected) == 2:
                    expected_str = f"'{expected[0]}' or '{expected[1]}'"
                else:
                    # Multiple options: quote each, join with commas, use 'or' before last
                    quoted = [f"'{tok}'" for tok in expected]
                    expected_str = f"{', '.join(quoted[:-1])}, or {quoted[-1]}"
            else:
                # Single terminal
                expected_str = f"'{expected}'"
            
            full_message = f"Unexpected: '{token_str}' Expected: {expected_str}"
        elif token:
            # Token but no expected - use original message
            token_str = token.get('lexeme', token.get('type', 'unknown'))
            full_message = f"Unexpected: '{token_str}'"
        elif expected:
            # Expected but no token (end of input)
            if isinstance(expected, list):
                if len(expected) == 1:
                    expected_str = f"'{expected[0]}'"
                elif len(expected) == 2:
                    expected_str = f"'{expected[0]}' or '{expected[1]}'"
                else:
                    quoted = [f"'{tok}'" for tok in expected]
                    expected_str = f"{', '.join(quoted[:-1])}, or {quoted[-1]}"
            else:
                expected_str = f"'{expected}'"
            full_message = f"{message}, Expected: {expected_str}"
        else:
            # No token or expected - just use message
            full_message = message
        
        if token:
            error = {
                "message": full_message,
                "line": token.get("line", 0),
                "column": token.get("column", 0),
                "token": token.get("lexeme", ""),
                "type": "syntax_error"
            }
        else:
            error = {
                "message": full_message,
                "line": 0,
                "column": 0,
                "token": "",
                "type": "syntax_error"
            }
        
        self.errors.append(error)
        raise SyntaxError(full_message)
    
    def synchronize(self, sync_tokens: List[str]):
        # Error recovery: skip tokens until we find one in sync_tokens

        # Used to recover from syntax errors and continue parsing
        while self.current_token():
            token = self.current_token()
            if token.get("type") in sync_tokens or token.get("lexeme") in sync_tokens:
                # Don't clear panic mode - let successful parsing clear it
                return
            self.advance()
    
    # -------------------- Main Parsing Entry Points --------------------
    
    def normalize_tokens(self, tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Normalize tokens from lexer format to parser format.

        # - Converts token types to match parser expectations

        # - Filters out whitespace tokens

        # - Adds EOF token if not present
        normalized = []
        
        # Token type mapping from lexer to parser
        # Lexer now outputs symbols directly (e.g., ';', '{', '+', etc.)
        # No mapping needed - lexer tokens are used as-is
        type_map = {
            # Lexer-specific types to parser types
            "identifier": "id",
            "main": "keyword",
            "spell": "keyword",
            # All other tokens use their actual symbols/names from lexer
        }
        
        for token in tokens:
            token_type = token.get("tokenType") or token.get("type", "")
            lexeme = token.get("tokenName") or token.get("lexeme", "")
            
            # Skip whitespace and newline tokens
            if token_type in ["space", "newline", "tab"]:
                continue
            
            # Map token type if in mapping, otherwise keep as-is
            mapped_type = type_map.get(token_type, token_type)
            
            # Create normalized token
            normalized_token = {
                "lexeme": lexeme,
                "type": mapped_type,
                "line": token.get("line", 0),
                "column": token.get("column", 0)
            }
            normalized.append(normalized_token)
        
        # Add EOF token if not present
        if not normalized or normalized[-1].get("lexeme") != "EOF":
            last_token = normalized[-1] if normalized else {"line": 1, "column": 1}
            normalized.append({
                "lexeme": "EOF",
                "type": "EOF",
                "line": last_token.get("line", 1),
                "column": last_token.get("column", 1) + len(str(last_token.get("lexeme", "")))
            })
        
        return normalized
    
    def parse_from_tokens(self, tokens: List[Dict[str, Any]], source: Optional[str] = None) -> Dict[str, Any]:
        # Main entry point for parsing from token list.

        # Returns a dictionary with AST and any errors.
        # Normalize tokens from lexer format
        normalized_tokens = self.normalize_tokens(tokens)
        
        self.tokens = normalized_tokens
        self.current = 0
        self.errors = []
        self.source_lines = source.split('\n') if source else []
        
        try:
            # Parse the program (start symbol)
            ast = self.parse_program()
            
            # Check for unconsumed tokens
            current = self.current_token()
            if current and current.get('type') != 'EOF':
                self.add_error(
                    f"Unexpected token after program end: '{current.get('lexeme')}'",
                    current
                )
            
            return {
                "success": True,
                "status": "success",
                "ast": self.ast_to_dict(ast) if ast else None,
                "errors": [],
                "token_count": len(tokens)
            }
        except SyntaxError:
            # Syntax error already recorded in self.errors
            return {
                "success": False,
                "status": "error",
                "ast": None,
                "errors": self.errors,
                "token_count": len(tokens)
            }
        except Exception as e:
            # Unexpected error
            error = {
                "message": f"Internal parser error: {str(e)}",
                "line": 0,
                "column": 0,
                "token": "",
                "type": "internal_error"
            }
            return {
                "success": False,
                "status": "error",
                "ast": None,
                "errors": [error],
                "token_count": len(tokens)
            }
    
    def parse_from_source(self, source: str) -> Dict[str, Any]:
        # Parse from source code by first calling the lexer, then parsing tokens.
        import requests
        try:
            # Call lexer API
            response = requests.post("http://localhost:8000/lex", json={"code": source})
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Failed to connect to lexer",
                    "ast": None,
                    "errors": ["Lexer service unavailable"]
                }
            
            lex_result = response.json()
            
            # Check for lexer errors
            if lex_result.get("errors"):
                return {
                    "success": False,
                    "message": "Lexical analysis failed",
                    "ast": None,
                    "errors": lex_result["errors"]
                }
            
            # Parse tokens
            tokens = lex_result.get("tokens", [])
            return self.parse_from_tokens(tokens, source)
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "ast": None,
                "errors": [str(e)]
            }
    
    def ast_to_dict(self, node: Optional[ASTNode]) -> Optional[Dict[str, Any]]:
        # Convert AST node to dictionary for JSON serialization
        if node is None:
            return None
        
        if isinstance(node, list):
            return [self.ast_to_dict(item) for item in node]
        
        result = {
            "node_type": node.__class__.__name__,
        }
        
        # Add all fields from the dataclass
        for field_name, field_value in node.__dict__.items():
            if field_name.startswith('_'):
                continue
            
            if isinstance(field_value, ASTNode):
                result[field_name] = self.ast_to_dict(field_value)
            elif isinstance(field_value, list):
                result[field_name] = [
                    self.ast_to_dict(item) if isinstance(item, ASTNode) else item
                    for item in field_value
                ]
            else:
                result[field_name] = field_value
        
        return result
    
    # ==================== RECURSIVE DESCENT PARSING METHODS ====================
    
    # -------------------- Program Structure --------------------
    
    def parse_program(self) -> Optional[ProgramNode]:
        # <program> → <global_dec> <function> <main_func>
        # Production 1
        global_declarations = []
        functions = []
        
        # Special case: if program starts with "int ..." check if it's main function
        # Valid starts for main: "int main(", "int identifier..." 
        # If we see "int (" it's a malformed main function (missing 'main' keyword)
        first_token = self.current_token()
        second_token = self.peek(1)
        if (first_token and second_token and
            (first_token.get("type") == "int" or first_token.get("lexeme") == "int")):
            # Check second token
            if second_token.get("lexeme") == "main":
                # This is "int main(...)" - skip global_dec parsing
                pass
            elif second_token.get("lexeme") == "(":
                # This is "int (...)" - malformed main function, missing 'main' keyword
                # Don't try to parse as array, go straight to main_func which will error correctly
                pass  
            else:
                # This is "int <something_else>" - could be global decl or array
                # Continue to global_dec parsing below
                # Parse global declarations
                iterations = 0
                max_iterations = 100
                while self.match_predict_set("global_dec") and iterations < max_iterations:
                    iterations += 1
                    
                    # Check if this is "int main(" - if so, break and parse as main_func
                    current = self.current_token()
                    next_tok = self.peek(1)
                    if current and next_tok:
                        current_is_int = current.get("type") == "int" or current.get("lexeme") == "int"
                        next_is_main = next_tok.get("lexeme") == "main"
                        if current_is_int and next_is_main:
                            break  # This is main function, not global declaration
                    
                    # Track position to detect infinite loops
                    pos_before = self.current
                    global_decl = self.parse_global_dec()
                    
                    if global_decl:
                        if isinstance(global_decl, list):
                            global_declarations.extend(global_decl)
                        else:
                            global_declarations.append(global_decl)
                    
                    # If no progress was made, skip this token and try next
                    if self.current == pos_before:
                        self.add_error(f"Unexpected token", self.current_token(), PREDICT_SETS.get("global_dec", []))
                        # Synchronize to recover from error
                        self.synchronize([";", "global", "weave", "func", "int"])
                        if self.match(";"):
                            self.advance()  # Consume semicolon and continue
                        break  # Stop parsing global declarations after error
        else:
            # Doesn't start with "int", parse global declarations normally
            # Parse global declarations
            iterations = 0
            max_iterations = 100
            while self.match_predict_set("global_dec") and iterations < max_iterations:
                iterations += 1
                
                # Check if this is "int main(" - if so, break and parse as main_func
                current = self.current_token()
                next_tok = self.peek(1)
                if current and next_tok:
                    current_is_int = current.get("type") == "int" or current.get("lexeme") == "int"
                    next_is_main = next_tok.get("lexeme") == "main"
                    if current_is_int and next_is_main:
                        break  # This is main function, not global declaration
                
                # Track position to detect infinite loops
                pos_before = self.current
                global_decl = self.parse_global_dec()
                
                if global_decl:
                    if isinstance(global_decl, list):
                        global_declarations.extend(global_decl)
                    else:
                        global_declarations.append(global_decl)
                
                # If no progress was made, skip this token and try next
                if self.current == pos_before:
                    self.add_error(f"Unexpected token", self.current_token(), PREDICT_SETS.get("global_dec", []))
                    # Synchronize to recover from error
                    self.synchronize([";", "global", "weave", "func", "int"])
                    if self.match(";"):
                        self.advance()  # Consume semicolon and continue
                    break  # Stop parsing global declarations after error
        
        # Parse function definitions
        iterations = 0
        max_iterations = 100
        while self.match_predict_set("function") and iterations < max_iterations:
            iterations += 1
            pos_before = self.current
            func = self.parse_function_def()
            if func:
                functions.append(func)
            # Break if no progress (with error recovery)
            if self.current == pos_before:
                self.add_error(f"Unexpected token", self.current_token(), PREDICT_SETS.get("function", []))
                # Synchronize to recover
                self.synchronize(["func", "int"])
                break  # Stop trying to parse more functions after error
        
        # Parse main function (required)
        main_func = self.parse_main_func()
        if not main_func:
            # Only report missing main if no other errors occurred
            self.add_error("Expected main function", self.current_token(), PREDICT_SETS.get("main_func", []))
            return None
        
        return ProgramNode(
            global_declarations=global_declarations,
            functions=functions,
            main_function=main_func
        )
    
    def parse_main_func(self) -> Optional[MainFunctionNode]:
        # <main_func> → int main(){<main_body>}
        # Production 425
        token = self.expect("int")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("main"):
            return None
        if not self.expect("("):
            return None
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse main body
        body = self.parse_main_body()
        
        if not self.expect("}"):
            return None
        
        return MainFunctionNode(body=body, line=line, column=col)
    
    def parse_main_body(self) -> FunctionBodyNode:
        # <main_body> → <import_block> <local_block> <statement_list> return intlit;
        # Production 426
        # Parse imports
        imports = []
        while self.match_predict_set("import_block"):
            pos_before = self.current
            import_stmt = self.parse_import_stmt()
            if import_stmt:
                imports.append(import_stmt)
            if self.current == pos_before:
                break
        
        # Parse local declarations
        local_declarations = []
        while self.match_predict_set("local_block"):
            pos_before = self.current
            local_decl = self.parse_local_dec()
            if local_decl:
                if isinstance(local_decl, list):
                    local_declarations.extend(local_decl)
                else:
                    local_declarations.append(local_decl)
            if self.current == pos_before:
                break
        
        # Parse statements
        statements = []
        while self.match_predict_set("statement_list"):
            # Stop if we see 'return' - it's handled separately
            if self.match("return"):
                break
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            if self.current == pos_before:
                # No progress made - unexpected token in statement context
                self.add_error("Unexpected token", self.current_token(), 
                             PREDICT_SETS.get("statement_list", []))
                break
        
        # Parse return statement (required in main)
        # Main must return intlit (Production 426)
        if not self.expect("return"):
            self.add_error("Expected return statement", self.current_token(), ["return"])
        
        return_value = None
        if self.match("intlit"):
            token = self.advance()
            return_value = NumberNode(
                value=token.get("lexeme"),
                token_type="intlit",
                line=token.get("line", 0),
                column=token.get("column", 0)
            )
        
        if not self.expect(";"):
            self.add_error("Expected ';'", self.current_token(), ";")
        
        return_stmt = ReturnStatementNode(value=return_value, line=0, column=0)
        
        return FunctionBodyNode(
            imports=imports,
            local_declarations=local_declarations,
            statements=statements,
            return_statement=return_stmt
        )
    
    # -------------------- Global Declarations --------------------
    
    def parse_global_dec(self) -> Optional[Union[ASTNode, List[ASTNode]]]:
        # <global_dec> → <int_global_dec> | <long_global_dec> | ... | <arr_1D> | <weave_def>
        # Productions 2-11: Global declarations (variables, arrays, weaves)
        # Production 18: global_dec → λ (handled in parse_program loop)
        token = self.current_token()
        
        if self.match("global"):
            self.advance()  # consume 'global'
            
            # After 'global' keyword, we MUST have var/const for variable declarations
            # Arrays do NOT use the 'global' keyword (they start directly with type)
            # CFG: global <mutability> <dtype> id = <value>;
            if self.match_predict_set("mutability"):
                # Global variable declaration: global var/const <type> id = value;
                return self.parse_variable_declaration("global")
            else:
                # Error: expected var/const after 'global'
                # Arrays don't use 'global' keyword - they start with type directly
                self.add_error("Expected 'var' or 'const' after 'global'", self.current_token(), 
                             ["var", "const"])
                return None
        
        elif self.match("weave"):
            # Weave definition
            return self.parse_weave_def()
        
        elif self.match_predict_set("arr_dtype"):
            # Array declaration at global scope (without 'global' keyword)
            # But NOT if it's "int main(" which is the main function
            next_tok = self.peek(1)
            if next_tok and next_tok.get("lexeme") == "main":
                # This is "int main()", not an array declaration
                return None
            
            # Arrays must start with type keywords, not identifiers
            arr = self.parse_arr_1D("global")
            if arr and self.expect(";"):
                return arr
        
        return None
    
    def parse_variable_declaration(self, scope: str) -> Optional[Union[VariableDeclarationNode, List[VariableDeclarationNode]]]:
        # Parse variable declaration with possible multiple declarations
        # global/local ⟨mutability⟩ ⟨dtype⟩ id = ⟨value⟩ ⟨multi_dec⟩;
        # Productions 2-17 (global), 242-249 (local), 33-34 (mutability), 51-57 (dtype), 35-50 (multi_dec)
        
        # Parse mutability
        mutability_token = self.current_token()
        if not self.match_predict_set("mutability"):
            self.add_error("Expected 'var' or 'const'", mutability_token)
            return None
        mutability = self.advance().get("lexeme")
        
        # Parse data type (built-in or weave type)
        dtype_token = self.current_token()
        if self.match_predict_set("dtype"):
            data_type = self.advance().get("lexeme")
        elif self.match("id"):
            # Check if this identifier is followed by '=' 
            # If so, it's the variable name, not a type - missing type error
            next_tok = self.peek(1)
            if next_tok and next_tok.get("lexeme") == "=":
                # This is "global var x =" - missing data type before variable name
                # Include 'id' in expected because weave types (identifiers) are valid
                self.add_error("Expected data type", dtype_token, 
                             ["int", "long", "float", "double", "char", "string", "bool", "id"])
                return None
            # Otherwise, allow identifiers for weave types
            data_type = self.advance().get("lexeme")
        else:
            # Report error with expected data types from PREDICT set
            # Include 'id' for weave types in addition to built-in types
            self.add_error("Expected data type", dtype_token, 
                         ["int", "long", "float", "double", "char", "string", "bool", "id"])
            return None
        
        # Parse identifier
        id_token = self.expect("id")
        if not id_token:
            return None
        identifier = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # After identifier, the ONLY valid token is '=' (initialization is REQUIRED per CFG)
        # Production: global/local <mutability> <dtype> id = <value> <multi_dec> ;
        if not self.expect("="):
            return None
        
        # Parse value (REQUIRED)
        initial_value = None
        # Check if this is a brace-enclosed initialization (for arrays/weaves)
        if self.match("{"):
            self.advance()
            elements = []
            if self.match_predict_set("elem_1D_list") or self.match("{"):
                # Parse first element (could be nested for 2D arrays)
                if self.match("{"):
                    # 2D array or nested structure
                    elements = []
                    while self.match("{"):
                        self.advance()
                        row = []
                        if self.match_predict_set("elem_1D_list"):
                            row.append(self.parse_expression())
                            while self.match(","):
                                self.advance()
                                row.append(self.parse_expression())
                        self.expect("}")
                        elements.append(row)
                        if not self.match(","):
                            break
                        self.advance()
                else:
                    # 1D array or struct
                    elements.append(self.parse_expression())
                    while self.match(","):
                        self.advance()
                        if self.match_predict_set("elem_1D_list"):
                            elements.append(self.parse_expression())
            self.expect("}")
            initial_value = ArrayLiteralNode(elements=elements, line=line, column=col)
        else:
            # Regular expression
            initial_value = self.parse_expression()
            if not initial_value:
                # Missing value after '=' - report error at current token
                self.add_error("Expected expression after '='", self.current_token(),
                             PREDICT_SETS.get("expression", []))
                return None
        
        # Create first declaration
        declarations = [VariableDeclarationNode(
            scope=scope,
            mutability=mutability,
            data_type=data_type,
            identifier=identifier,
            initial_value=initial_value,
            line=line,
            column=col
        )]
        
        # Parse multiple declarations
        while self.match(","):
            self.advance()
            id_token = self.expect("id")
            if not id_token:
                break
            
            identifier = id_token.get("lexeme")
            initial_value = None
            if self.match("="):
                self.advance()
                # Check if this is a brace-enclosed initialization
                if self.match("{"):
                    self.advance()
                    elements = []
                    if self.match_predict_set("elem_1D_list") or self.match("{"):
                        if self.match("{"):
                            # 2D array
                            while self.match("{"):
                                self.advance()
                                row = []
                                if self.match_predict_set("elem_1D_list"):
                                    row.append(self.parse_expression())
                                    while self.match(","):
                                        self.advance()
                                        row.append(self.parse_expression())
                                self.expect("}")
                                elements.append(row)
                                if not self.match(","):
                                    break
                                self.advance()
                        else:
                            # 1D array or struct
                            elements.append(self.parse_expression())
                            while self.match(","):
                                self.advance()
                                if self.match_predict_set("elem_1D_list"):
                                    elements.append(self.parse_expression())
                    self.expect("}")
                    initial_value = ArrayLiteralNode(elements=elements, line=id_token.get("line", 0), column=id_token.get("column", 0))
                else:
                    # Regular expression
                    initial_value = self.parse_expression()
            
            declarations.append(VariableDeclarationNode(
                scope=scope,
                mutability=mutability,
                data_type=data_type,
                identifier=identifier,
                initial_value=initial_value,
                line=id_token.get("line", 0),
                column=id_token.get("column", 0)
            ))
        
        # Expect semicolon
        self.expect(";")
        
        return declarations if len(declarations) > 1 else declarations[0]
    
    def parse_local_dec(self) -> Optional[Union[ASTNode, List[ASTNode]]]:
        # <local_dec> → <int_local_dec> | <long_local_dec> | ... | <weave_local_dec>
        # Productions 242-249: Local declarations (int, long, float, double, char, string, bool)
        # Production 268: weave_local_dec → local <weave_id> id={<value>}<elem_1D_list_tail>;
        # Also handles local array declarations
        if not self.match("local"):
            return None
        
        self.advance()  # consume 'local'
        
        # Check if this is a weave declaration without mutability (Production 268)
        # Format: local WeaveType varName = {...};
        if self.match("id"):
            # Could be: local WeaveType id = {...} OR local var/const type id = value
            # Look ahead to determine which
            checkpoint = self.current
            type_or_mut = self.advance()  # consume id (could be weave type or next token after var/const)
            
            # Check if next token is 'id' (variable name)
            if self.match("id"):
                # Pattern: local <identifier> <identifier>
                # This is weave declaration: local WeaveType varName
                weave_type = type_or_mut.get("lexeme")
                id_token = self.advance()
                identifier = id_token.get("lexeme")
                line = id_token.get("line", 0)
                col = id_token.get("column", 0)
                
                # Expect '=' for initialization
                if not self.expect("="):
                    return None
                
                # Parse brace-enclosed initialization
                if not self.expect("{"):
                    return None
                
                elements = []
                # Parse elements (could be values or nested arrays)
                if self.match_predict_set("elem_1D_list") or self.match("{"):
                    # Check if first element is a nested array
                    if self.match("{"):
                        # Nested array - parse it as an array literal
                        self.advance()  # consume '{'
                        nested = []
                        if self.match_predict_set("elem_1D_list"):
                            nested.append(self.parse_expression())
                            while self.match(","):
                                self.advance()
                                if self.match_predict_set("elem_1D_list"):
                                    nested.append(self.parse_expression())
                        self.expect("}")
                        elements.append(ArrayLiteralNode(elements=nested, line=line, column=col))
                    else:
                        # Regular value
                        elements.append(self.parse_expression())
                    
                    # Parse remaining elements
                    while self.match(","):
                        self.advance()
                        if self.match("{"):
                            # Another nested array
                            self.advance()  # consume '{'
                            nested = []
                            if self.match_predict_set("elem_1D_list"):
                                nested.append(self.parse_expression())
                                while self.match(","):
                                    self.advance()
                                    if self.match_predict_set("elem_1D_list"):
                                        nested.append(self.parse_expression())
                            self.expect("}")
                            elements.append(ArrayLiteralNode(elements=nested, line=line, column=col))
                        elif self.match_predict_set("elem_1D_list"):
                            # Regular value
                            elements.append(self.parse_expression())
                
                if not self.expect("}"):
                    return None
                if not self.expect(";"):
                    return None
                
                # Create weave instance node
                return VariableDeclarationNode(
                    scope="local",
                    mutability="var",  # Default for weave instances
                    data_type=weave_type,
                    identifier=identifier,
                    initial_value=ArrayLiteralNode(elements=elements, line=line, column=col),
                    line=line,
                    column=col
                )
            else:
                # Not weave declaration, reset and parse normally
                self.current = checkpoint
        
        # Check if this is an array declaration with mutability
        # Arrays: local var/const type id[size]
        # Variables: local var/const type id = value
        if self.match_predict_set("mutability"):
            # Save position to look ahead
            checkpoint = self.current
            mutability = self.advance()  # consume var/const
            
            # Check if it's a type followed by id followed by '['
            if self.match_predict_set("arr_dtype"):
                type_checkpoint = self.current
                self.advance()  # consume type
                
                if self.match("id"):
                    id_checkpoint = self.current
                    self.advance()  # consume id
                    
                    if self.match("["):
                        # It's an array! Reset to after 'local' and parse as array
                        self.current = checkpoint
                        arr = self.parse_arr_1D("local")
                        if arr:
                            self.expect(";")  # Arrays need semicolon
                        return arr
                    else:
                        # It's a variable, reset to after 'local'
                        self.current = checkpoint
                else:
                    # Reset
                    self.current = checkpoint
            else:
                # Reset
                self.current = checkpoint
        
        return self.parse_variable_declaration("local")
    
    def parse_weave_def(self) -> Optional[WeaveDefinitionNode]:
        # <weave_def> → weave id{<field_list>};
        # Production 199
        token = self.expect("weave")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        id_token = self.expect("id")
        if not id_token:
            return None
        
        weave_name = id_token.get("lexeme")
        
        if not self.expect("{"):
            return None
        
        # Parse field list
        fields = []
        while self.match_predict_set("field_list") and not self.match("}"):
            pos_before = self.current
            field = self.parse_field_dec()
            if field:
                if isinstance(field, list):
                    fields.extend(field)
                else:
                    fields.append(field)
            
            # Check for infinite loop - if no progress was made
            if self.current == pos_before:
                self.add_error("Unexpected token in weave definition", 
                             self.current_token(), 
                             PREDICT_SETS.get("field_list", []))
                break
        
        if not self.expect("}"):
            return None
        if not self.expect(";"):
            return None
        
        return WeaveDefinitionNode(
            name=weave_name,
            fields=fields,
            line=line,
            column=col
        )
    
    def parse_field_dec(self) -> Optional[Union[WeaveFieldNode, List[WeaveFieldNode]]]:
        # <field_dec> → <field_type>id <field_array_spec_opt><field_dec_cont>;
        # Productions 200-206: field_list, field_dec, field_dec_cont, field_array_spec_opt, field_type
        # Parse field type
        type_token = self.current_token()
        if self.match_predict_set("dtype"):
            field_type = self.advance().get("lexeme")
        elif self.match("id"):
            field_type = self.advance().get("lexeme")  # Weave type
        else:
            self.add_error("Expected field type", type_token, 
                         PREDICT_SETS.get("field_type", []))
            return None
        
        # Parse field name
        id_token = self.expect("id")
        if not id_token:
            return None
        
        field_name = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # Parse optional array specification
        is_array = False
        array_size = None
        if self.match("["):
            is_array = True
            self.advance()
            size_token = self.expect("intlit")
            if size_token:
                array_size = int(size_token.get("lexeme"))
            self.expect("]")
        
        fields = [WeaveFieldNode(
            field_type=field_type,
            field_name=field_name,
            is_array=is_array,
            array_size=array_size,
            line=line,
            column=col
        )]
        
        # Parse additional fields (comma-separated)
        while self.match(","):
            self.advance()
            id_token = self.expect("id")
            if not id_token:
                break
            
            field_name = id_token.get("lexeme")
            is_array = False
            array_size = None
            if self.match("["):
                is_array = True
                self.advance()
                size_token = self.expect("intlit")
                if size_token:
                    array_size = int(size_token.get("lexeme"))
                self.expect("]")
            
            fields.append(WeaveFieldNode(
                field_type=field_type,
                field_name=field_name,
                is_array=is_array,
                array_size=array_size,
                line=id_token.get("line", 0),
                column=id_token.get("column", 0)
            ))
        
        # Production 201 requires semicolon at end
        if not self.expect(";"):
            return None
        
        return fields if len(fields) > 1 else fields[0]
    
    def parse_arr_1D(self, scope: str) -> Optional[ArrayDeclarationNode]:
        # Array declarations (1D and 2D)
        # Productions 66-180: arr_1D variations, initialization, element lists, 2D arrays
        # For global: type id[size] (no mutability keyword per refactored CFG)
        # For local: var/const type id[size] (mutability required)
        token = self.current_token()
        if not token:
            return None
        
        # For local scope, we need to parse mutability (var/const)
        mutability = None
        if scope == "local":
            if self.match_predict_set("mutability"):
                mutability = self.advance().get("lexeme")
            else:
                self.add_error("Expected 'var' or 'const' for local array", self.current_token(), ["var", "const"])
                return None
        
        # Parse array data type
        token = self.current_token()
        if not token:
            return None
            
        token_lexeme = token.get("lexeme", "")
        valid_array_types = ["int", "long", "float", "double", "char", "string", "bool"]
        
        if token_lexeme not in valid_array_types:
            # This token cannot start an array declaration - return silently
            return None
            
        # Parse array data type - we already validated it's a valid type
        data_type = self.advance().get("lexeme")
        
        # Parse identifier
        id_token = self.expect("id")
        if not id_token:
            return None
        
        identifier = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # Parse size
        if not self.expect("["):
            return None
        
        size1 = None
        if self.match("intlit"):
            size_token = self.advance()
            size1 = NumberNode(
                value=size_token.get("lexeme"),
                token_type="intlit",
                line=size_token.get("line", 0),
                column=size_token.get("column", 0)
            )
        
        if not self.expect("]"):
            return None
        
        # Check for 2D array
        size2 = None
        if self.match("["):
            self.advance()
            if self.match("intlit"):
                size_token = self.advance()
                size2 = NumberNode(
                    value=size_token.get("lexeme"),
                    token_type="intlit",
                    line=size_token.get("line", 0),
                    column=size_token.get("column", 0)
                )
            self.expect("]")
        
        # Parse optional initialization
        initial_values = None
        if self.match("="):
            self.advance()
            if self.expect("{"):
                initial_values = self.parse_elem_list(size2 is not None)
                self.expect("}")
        
        return ArrayDeclarationNode(
            scope=scope,
            data_type=data_type,
            identifier=identifier,
            size1=size1,
            size2=size2,
            initial_values=initial_values,
            line=line,
            column=col
        )
    
    def parse_elem_list(self, is_2d: bool) -> List[ASTNode]:
        # Parse array initialization list
        # Productions 99-180: elem_1D_list variations for different types, 2D arrays
        elements = []
        
        if is_2d:
            # 2D array: {{val1, val2}, {val3, val4}}
            # Check if first element is a nested brace
            if self.match("{"):
                # Proper 2D initialization with nested braces
                while self.match("{"):
                    self.advance()
                    row = []
                    if self.match_predict_set("elem_1D_list"):
                        row.append(self.parse_expression())
                        while self.match(","):
                            self.advance()
                            row.append(self.parse_expression())
                    self.expect("}")
                    elements.append(row)
                    if not self.match(","):
                        break
                    self.advance()
            elif self.match_predict_set("elem_1D_list"):
                # Flat initialization for 2D array - parse as flat list
                # This is more lenient than strict grammar but easier for users
                row = []
                row.append(self.parse_expression())
                while self.match(","):
                    self.advance()
                    if self.match_predict_set("elem_1D_list"):
                        row.append(self.parse_expression())
                elements.append(row)
        else:
            # 1D array: {val1, val2, val3}
            if self.match_predict_set("elem_1D_list"):
                elements.append(self.parse_expression())
                while self.match(","):
                    self.advance()
                    if self.match_predict_set("elem_1D_list"):
                        elements.append(self.parse_expression())
        
        return elements
    
    # -------------------- Function Definitions --------------------
    
    def parse_function_def(self) -> Optional[FunctionDefinitionNode]:
        # <function_def> → func<ret_type>id(<param>){<function_body>}
        # Productions 211 (function), 213 (function_def)
        token = self.expect("func")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        # Parse return type
        ret_type = self.parse_ret_type()
        if not ret_type:
            return None
        
        # Parse function name
        id_token = self.expect("id")
        if not id_token:
            return None
        
        func_name = id_token.get("lexeme")
        
        # Parse parameters
        if not self.expect("("):
            return None
        
        parameters = []
        if self.match_predict_set("param"):
            param = self.parse_param()
            if param:
                parameters.append(param)
            
            # After first parameter, expect comma (for more params) or closing paren
            # Production 229: <param_cont> → ,<param>
            # Production 230: <param_cont> → λ
            while self.match(","):
                self.advance()
                param = self.parse_param()
                if param:
                    parameters.append(param)
        
        # After parameters, expect closing paren only
        if not self.match(")"):
            # If we don't see ), provide error with valid continuations
            # At this point, only ) is valid (if there was a comma, we'd still be in the loop)
            curr_token = self.current_token()
            if curr_token:
                self.add_error("Unexpected token in parameter list", curr_token, [",", ")"])
            return None
        self.advance()  # consume )
        
        # Parse function body
        if not self.expect("{"):
            return None
        
        body = self.parse_function_body()
        
        if not self.expect("}"):
            return None
        
        return FunctionDefinitionNode(
            return_type=ret_type,
            name=func_name,
            parameters=parameters,
            body=body,
            line=line,
            column=col
        )
    
    def parse_ret_type(self) -> Optional[str]:
        # <ret_type> → <dtype> | id<ret_struct> | void
        # Productions 214-216: ret_type_dtype, ret_type_weave, ret_type_void
        token = self.current_token()
        
        if self.match("void"):  # Production 215
            self.advance()
            return "void"
        
        if self.match_predict_set("dtype"):  # Production 213
            return self.advance().get("lexeme")
        
        if self.match("id"):  # Production 214
            # Could be weave type with array/member notation
            type_name = self.advance().get("lexeme")
            # TODO: Handle <ret_struct> for arrays/members if needed
            return type_name
        
        self.add_error("Expected return type", token, PREDICT_SETS.get("ret_type", []))
        return None
    
    def parse_param(self) -> Optional[ParameterNode]:
        # <param> → <param_type>id<param_struct><param_cont>
        # Productions 222-229: param, param_type, param_struct, param_2D, param_cont
        # Parse parameter type
        param_type_token = self.current_token()
        if self.match_predict_set("dtype"):
            param_type = self.advance().get("lexeme")
        elif self.match("id"):
            param_type = self.advance().get("lexeme")  # Weave type
        else:
            self.add_error("Expected parameter type", param_type_token, 
                         PREDICT_SETS.get("param_type", []))
            return None
        
        # Parse parameter name
        id_token = self.expect("id")
        if not id_token:
            return None
        
        param_name = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # Check for array parameter - Production 225
        is_array = False
        is_2d_array = False
        if self.match("["):
            is_array = True
            self.advance()
            self.expect("intlit")  # Size for array parameter
            self.expect("]")
            
            if self.match("["):  # Production 227 - 2D array
                is_2d_array = True
                self.advance()
                self.expect("intlit")
                self.expect("]")
        
        return ParameterNode(
            param_type=param_type,
            name=param_name,
            is_array=is_array,
            is_2d_array=is_2d_array,
            line=line,
            column=col
        )
    
    def parse_function_body(self) -> FunctionBodyNode:
        # <function_body> → <import_block> <local_block> <statement_list> <ret_stmt>
        # Production 232
        # Parse imports
        imports = []
        while self.match_predict_set("import_block"):
            import_stmt = self.parse_import_stmt()
            if import_stmt:
                imports.append(import_stmt)
        
        # Parse local declarations
        local_declarations = []
        while self.match_predict_set("local_block"):
            local_decl = self.parse_local_dec()
            if local_decl:
                if isinstance(local_decl, list):
                    local_declarations.extend(local_decl)
                else:
                    local_declarations.append(local_decl)
        
        # Parse statements
        statements = []
        while self.match_predict_set("statement_list") and not self.match("return"):
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token())
                break
        
        # Parse optional return statement
        return_stmt = None
        if self.match("return"):
            return_stmt = self.parse_return_stmt()
        
        return FunctionBodyNode(
            imports=imports,
            local_declarations=local_declarations,
            statements=statements,
            return_statement=return_stmt
        )
    
    def parse_import_stmt(self) -> Optional[UsingStatementNode]:
        # <import_stmt> → using id<import_cont>;
        # Productions 233 (import_block), 235 (import_stmt), 236-237 (import_cont)
        token = self.expect("using")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        modules = []
        id_token = self.expect("id")
        if id_token:
            modules.append(id_token.get("lexeme"))
        
        # Parse additional modules (comma-separated)
        while self.match(","):
            self.advance()
            id_token = self.expect("id")
            if id_token:
                modules.append(id_token.get("lexeme"))
        
        self.expect(";")
        
        return UsingStatementNode(modules=modules, line=line, column=col)
    
    # -------------------- Expressions --------------------
    
    def parse_value(self) -> Optional[ASTNode]:
        # <value> → intlit | longlit | floatlit | doublelit | charlit | stringlit | true | false

        # Productions 58-65
        token = self.current_token()
        if not token:
            return None
        
        token_type = token.get("type")
        lexeme = token.get("lexeme")
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if token_type in ["intlit", "longlit", "floatlit", "doublelit"]:
            self.advance()
            return NumberNode(value=lexeme, token_type=token_type, line=line, column=col)
        
        if token_type == "charlit":
            self.advance()
            return CharNode(value=lexeme, line=line, column=col)
        
        if token_type == "stringlit":
            self.advance()
            return StringNode(value=lexeme, line=line, column=col)
        
        if lexeme in ["true", "false"]:
            self.advance()
            return BoolNode(value=(lexeme == "true"), line=line, column=col)
        
        return None
    
    def parse_expression(self) -> Optional[ASTNode]:
        # <expression> → <logical_expr>
        # Production 277
        return self.parse_logical_expr()
    
    def parse_logical_expr(self) -> Optional[ASTNode]:
        # <logical_expr> → <rel_expr> <logical_expr_cont>
        # Productions 278-281: logical_expr, logical_expr_cont (&&, ||)
        left = self.parse_rel_expr()
        if not left:
            return None
        
        while self.match("&&") or self.match("||"):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            right = self.parse_rel_expr()
            if not right:
                # After logical operator, expect a relational expression
                self.add_error("Expected expression", 
                             self.current_token(), PREDICT_SETS.get("rel_expr", []))
                break
            
            left = BinaryOpNode(
                left=left,
                operator=operator,
                right=right,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        return left
    
    def parse_rel_expr(self) -> Optional[ASTNode]:
        # <rel_expr> → <arith_expr><rel_expr_cont>
        # Productions 282-289: rel_expr, rel_expr_cont (==, !=, >, <, >=, <=)
        left = self.parse_arith_expr()
        if not left:
            return None
        
        while self.match_predict_set("rel_expr_cont"):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            
            right = self.parse_arith_expr()
            if not right:
                # After relational operator, expect an arithmetic expression
                self.add_error("Expected expression", 
                             self.current_token(), PREDICT_SETS.get("arith_expr", []))
                break
            
            left = BinaryOpNode(
                left=left,
                operator=operator,
                right=right,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        return left
    
    def parse_arith_expr(self) -> Optional[ASTNode]:
        # <arith_expr> → <term> <add_min_cont>
        # Productions 290-293: arith_expr, add_min_cont (+, -)
        left = self.parse_term()
        if not left:
            return None
        
        while self.match("+") or self.match("-") or self.match(".."):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            # Production 301 for +, 302 for -
            prod_num = 301 if operator == "+" else 302 if operator == "-" else 300
            
            right = self.parse_term()
            if not right:
                self.add_error("Expected term", self.current_token(), PREDICT_SETS.get("term", []))
                break
            
            # Use StringConcatNode for .. operator, BinaryOpNode for + and -
            if operator == "..":
                left = StringConcatNode(
                    left=left,
                    right=right,
                    line=op_token.get("line", 0),
                    column=op_token.get("column", 0)
                )
            else:
                # Validate that + and - are not used with string literals
                # Grammar only allows .. for string concatenation
                if isinstance(left, StringNode) or isinstance(right, StringNode):
                    self.add_error("Cannot use arithmetic operator with string", 
                                 op_token, [".."])
                    return None
                
                left = BinaryOpNode(
                    left=left,
                    operator=operator,
                    right=right,
                    line=op_token.get("line", 0),
                    column=op_token.get("column", 0)
                )
        
        return left
    
    def parse_term(self) -> Optional[ASTNode]:
        # <term> → <factor> <mult_div_modulo_cont>
        # Productions 294-298: term, mult_div_modulo_cont (*, /, %)
        left = self.parse_factor()
        if not left:
            return None
        
        while self.match("*") or self.match("/") or self.match("%"):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            # Production 305 for *, 306 for /, 307 for %
            prod_map = {"*": 305, "/": 306, "%": 307}
            prod_num = prod_map.get(operator, 304)
            
            right = self.parse_factor()
            if not right:
                self.add_error("Expected factor", self.current_token(), PREDICT_SETS.get("factor", []))
                break
            
            left = BinaryOpNode(
                left=left,
                operator=operator,
                right=right,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        return left
    
    def parse_factor(self) -> Optional[ASTNode]:
        # <factor> → <primary>
        # Production 299
        return self.parse_primary()
    
    def parse_primary(self) -> Optional[ASTNode]:
        # <primary> → !<primary> | -<primary> | <cast_val> | <atom> | ( <expression> )
        # Productions 300-305: primary_not, primary_neg, primary_cast, primary_atom, primary_paren
        token = self.current_token()
        
        # Unary minus - Production 311
        if self.match("-"):
            op_token = self.advance()
            operand = self.parse_primary()
            if not operand:
                self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("primary", []))
                return None
            return UnaryOpNode(
                operator="-",
                operand=operand,
                is_prefix=True,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        # Logical NOT - Production 310
        if self.match("!"):
            op_token = self.advance()
            operand = self.parse_primary()
            if not operand:
                self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("primary", []))
                return None
            return UnaryOpNode(
                operator="!",
                operand=operand,
                is_prefix=True,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        # Parenthesized expression or cast - Production 314 or 315
        if self.match("("):
            self.advance()
            # Check if this is a cast: (type) - Production 315
            if self.match_predict_set("dtype"):
                type_token = self.advance()
                if self.expect(")"):
                    # This is a cast - MUST have a factor after it
                    # Production 315: <cast_val> → (<dtype>) <factor>
                    expr = self.parse_factor()
                    if not expr:
                        # No factor found after cast - invalid
                        self.add_error("Expected expression after cast", 
                                     self.current_token(), PREDICT_SETS.get("factor", []))
                        return None
                    return CastNode(
                        target_type=type_token.get("lexeme"),
                        expression=expr,
                        line=type_token.get("line", 0),
                        column=type_token.get("column", 0)
                    )
            else:
                # Regular parenthesized expression - Production 314
                expr = self.parse_expression()
                self.expect(")")
                return expr
        
        # Atom - Production 313
        return self.parse_atom()
    
    def parse_atom(self) -> Optional[ASTNode]:
        # <atom> → <id_atom> | <incdec_atom> | <num_lit_type> | <function_call> | stringlit | charlit | true | false
        # Productions 306-324: atom variations, id_atom, incdec_atom, pre_incdec, post_incdec, num_lit_type
        token = self.current_token()
        if not token:
            return None
        
        token_type = token.get("type")
        lexeme = token.get("lexeme")
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        # Literals - Productions 331-334 (numeric), 320-323 (other)
        if token_type in ["intlit", "longlit", "floatlit", "doublelit"]:
            self.advance()
            return NumberNode(value=lexeme, token_type=token_type, line=line, column=col)
        
        if token_type == "charlit":  # Production 321
            self.advance()
            return CharNode(value=lexeme, line=line, column=col)
        
        if token_type == "stringlit":  # Production 320
            self.advance()
            return StringNode(value=lexeme, line=line, column=col)
        
        if lexeme in ["true", "false"]:  # Productions 322, 323
            self.advance()
            return BoolNode(value=(lexeme == "true"), line=line, column=col)
        
        # Prefix increment/decrement - Productions 327, 328
        if lexeme in ["++", "--"]:
            op = self.advance().get("lexeme")
            prod_num = 327 if op == "++" else 328
            id_token = self.expect("id")
            if not id_token:
                return None
            return UnaryOpNode(
                operator=op,
                operand=IdentifierNode(
                    name=id_token.get("lexeme"),
                    line=id_token.get("line", 0),
                    column=id_token.get("column", 0)
                ),
                is_prefix=True,
                line=line,
                column=col
            )
        
        # Identifier (variable, function call, array access, weave access, postfix ops)
        # Productions 316 (id_atom), 319 (function_call), 329-330 (postfix)
        if token_type == "id":
            return self.parse_identifier_expression()
        
        return None
    
    def parse_identifier_expression(self) -> Optional[ASTNode]:
        # Parse identifier with possible function call, array access, weave member access, or postfix operators
        # Supports chaining: id[0].field, id.field[0], id[0][1], id.field1.field2, etc.

        # Productions 319 (function call), 329-330 (postfix increment/decrement)
        id_token = self.advance()
        identifier = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        base = IdentifierNode(name=identifier, line=line, column=col)
        
        # Function call - Production 319, 360
        if self.match("("):
            self.advance()
            arguments = []
            
            if self.match_predict_set("arg"):
                arg = self.parse_expression()
                if arg:
                    arguments.append(arg)
                
                while self.match(","):
                    self.advance()
                    arg = self.parse_expression()
                    if arg:
                        arguments.append(arg)
            
            self.expect(")")
            return FunctionCallNode(
                function_name=identifier,
                arguments=arguments,
                line=line,
                column=col
            )
        
        # Array access and weave member access - can be chained
        # Loop to handle multiple accesses: arr[0].field, obj.field[0], obj.a.b[0][1], etc.
        while self.match("[") or self.match("."):
            if self.match("["):
                # Array access
                self.advance()
                index1 = self.parse_expression()
                self.expect("]")
                
                base = ArrayAccessNode(
                    array=base,
                    index1=index1,
                    index2=None,
                    line=line,
                    column=col
                )
            elif self.match("."):
                # Weave member access
                self.advance()
                field_token = self.expect("id")
                if field_token:
                    base = WeaveAccessNode(
                        weave=base,
                        field=field_token.get("lexeme"),
                        line=line,
                        column=col
                    )
        
        # Postfix increment/decrement - Productions 329, 330
        if self.match("++") or self.match("--"):
            op_token = self.advance()
            return UnaryOpNode(
                operator=op_token.get("lexeme"),
                operand=base,
                is_prefix=False,
                line=line,
                column=col
            )
        
        return base
    
    # -------------------- Statements --------------------
    
    def parse_statement(self) -> Optional[ASTNode]:
        # <statement> → <expression>; | <I/O_stmt> | <assign_stmt>; | <ctrl_struct> | <arr_1D>;
        # Productions 271-276: statement types (expression, I/O, assignment, control, array)
        token = self.current_token()
        
        # Return statement
        if self.match("return"):
            return self.parse_return_stmt()
        
        # Break statement
        if self.match("break"):
            token = self.advance()
            self.expect(";")
            return BreakStatementNode(line=token.get("line", 0), column=token.get("column", 0))
        
        # Continue statement
        if self.match("continue"):
            token = self.advance()
            self.expect(";")
            return ContinueStatementNode(line=token.get("line", 0), column=token.get("column", 0))
        
        # Local variable declaration
        if self.match("local"):
            return self.parse_local_dec()
        
        # I/O statements
        if self.match("trap"):
            return self.parse_input_stmt()
        
        if self.match("thread") or self.match("threadln"):
            return self.parse_output_stmt()
        
        # Control structures
        if self.match("if"):
            return self.parse_if_stmt()
        
        if self.match("switch"):
            return self.parse_switch_stmt()
        
        if self.match("for"):
            return self.parse_for_stmt()
        
        if self.match("while"):
            return self.parse_while_stmt()
        
        if self.match("do"):
            return self.parse_do_while_stmt()
        
        # Assignment or expression statement
        # Need to distinguish between assignment and expression
        if self.match("id"):
            # Production 374: <assign_stmt> → id<array_spec_opt><assign_stmt_op>
            # After 'id', valid tokens are: '[' (array), '.', or assignment operators
            # If we see '(' it means this is a function call, not an assignment
            
            checkpoint = self.current
            id_token = self.current_token()
            
            # Peek ahead after the identifier
            self.advance()  # consume id
            
            # Check what comes after the id
            if self.match("("):
                # This is a function call - rewind and parse as expression statement
                self.current = checkpoint
                expr = self.parse_expression()
                if expr:
                    self.expect(";")
                    return expr
                return None
            
            # Not a function call, rewind and parse identifier expression
            self.current = checkpoint
            id_node = self.parse_identifier_expression()
            
            # Check if followed by assignment operator
            if self.match_predict_set("assign_stmt_op"):
                # This is a valid assignment
                op_token = self.advance()
                value = self.parse_expression()
                if not value:
                    self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression", []))
                    return None
                self.expect(";")
                return AssignmentStatementNode(
                    target=id_node,
                    operator=op_token.get("lexeme"),
                    value=value,
                    line=op_token.get("line", 0),
                    column=op_token.get("column", 0)
                )
            else:
                # This is an expression statement
                self.expect(";")
                return id_node
        
        # General expression statement
        expr = self.parse_expression()
        if expr:
            self.expect(";")
            return expr
        
        return None
    
    def parse_input_stmt(self) -> Optional[InputStatementNode]:
        # <input_stmt> → trap(<iden>);
        # Production 328 (input_stmt)
        token = self.expect("trap")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        # Parse identifier (can be variable, array element, or weave member)
        target = self.parse_identifier_expression()
        
        if not self.expect(")"):
            return None
        if not self.expect(";"):
            return None
        
        return InputStatementNode(target=target, line=line, column=col)
    
    def parse_output_stmt(self) -> Optional[OutputStatementNode]:
        # <output_stmt> → thread(<expression1>); | threadln(<expression1>);
        # Productions 334-343: output_stmt (thread, threadln), expression1, expr1_cont
        token = self.current_token()
        is_newline = self.match("threadln")
        self.advance()
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        expressions = []
        # Parse first expression
        if self.match_predict_set("expression1"):
            expr = self.parse_expression()
            if expr:
                expressions.append(expr)
            elif not self.match(")"):
                # If we're in the expression1 predict set but got no expression,
                # and we're not at the closing paren, that's an error
                self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression1", []))
            
            # Parse continuation (,id , ,id , ...)
            # Production 351: <expr1_cont> → , <expression1>
            # Production 352: <expr1_cont> → 𝝺
            while self.match(","):
                self.advance()
                # After a comma, we MUST have an expression (non-nullable)
                expr = self.parse_expression()
                if expr:
                    expressions.append(expr)
                else:
                    # Error: comma without following expression
                    self.add_error("Expected expression after comma", self.current_token(), PREDICT_SETS.get("expression1", []))
                    return None
        
        if not self.expect(")"):
            return None
        if not self.expect(";"):
            return None
        
        return OutputStatementNode(
            is_newline=is_newline,
            expressions=expressions,
            line=line,
            column=col
        )
    
    def parse_return_stmt(self) -> Optional[ReturnStatementNode]:
        # <ret_stmt> → return<ret_value>;
        # Productions 420-424: ret_stmt, ret_value variations
        token = self.expect("return")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        # Parse optional return value
        return_value = None
        if self.match_predict_set("ret_value"):
            return_value = self.parse_expression()
        
        self.expect(";")
        
        return ReturnStatementNode(value=return_value, line=line, column=col)
    
    # -------------------- Control Structures --------------------
    
    def parse_if_stmt(self) -> Optional[IfStatementNode]:
        # <if_stmt> → if(<condition>){<ctrl_body><ret_ctrl_body>}<else_if_ei_stmt>
        # Productions 380-388: if_stmt, condition, ctrl_body, ret_ctrl_body, else_if_ei_stmt, else_stmt
        token = self.expect("if")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        # Parse condition - REQUIRED (non-nullable)
        condition = self.parse_expression()
        if not condition:
            # Empty condition or invalid expression
            self.add_error("Expected condition expression", self.current_token(), 
                         PREDICT_SETS.get("condition", []))
            return None
        
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse statement list
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        # Parse else-if chain - Production 393, 395
        elif_parts = []
        while self.match("else") and self.peek() and self.peek().get("lexeme") == "if":
            self.advance()  # consume 'else'
            self.advance()  # consume 'if'
            
            if not self.expect("("):
                break
            
            elif_cond = self.parse_expression()
            
            if not self.expect(")"):
                break
            if not self.expect("{"):
                break
            
            elif_body = []
            while not self.match("}") and self.current_token():
                pos_before = self.current
                stmt = self.parse_statement()
                if stmt:
                    elif_body.append(stmt)
                # Prevent infinite loop if no progress
                if self.current == pos_before:
                    self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                    break
            
            if not self.expect("}"):
                break
            
            elif_parts.append({"condition": elif_cond, "body": elif_body})
        
        # Parse else part - Production 393, 396
        else_body = None
        if self.match("else"):
            self.advance()
            
            if not self.expect("{"):
                return None
            
            else_body = []
            while not self.match("}") and self.current_token():
                pos_before = self.current
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
                # Prevent infinite loop if no progress
                if self.current == pos_before:
                    self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                    break
            
            if not self.expect("}"):
                return None
        
        return IfStatementNode(
            condition=condition,
            then_body=body,
            else_body=else_body,
            line=line,
            column=col
        )
    
    def parse_switch_stmt(self) -> Optional[SwitchStatementNode]:
        # <switch_stmt> → switch(<switch_val>) { <case_stmt><default_stmt>}
        # Productions 389-393: switch_stmt, switch_val, case_stmt, case_val, unique_val
        token = self.expect("switch")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        expression = self.parse_expression()
        
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse cases
        cases = []
        while self.match("case"):
            case_node = self.parse_case()
            if case_node:
                cases.append(case_node)
        
        # Parse default case
        default_case = None
        if self.match("default"):
            default_case = self.parse_default_case()
        
        if not self.expect("}"):
            return None
        
        return SwitchStatementNode(
            switch_value=expression,
            cases=cases,
            default_case=default_case,
            line=line,
            column=col
        )
    
    def parse_case(self) -> Optional[CaseNode]:
        # <case_stmt> → case<case_val>: <ctrl_body> break;
        # Productions 394-397: case_stmt, case_stmt_cont, case_val, unique_val
        token = self.expect("case")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        case_value = self.parse_expression()
        
        if not self.expect(":"):
            return None
        
        # Check if case body is wrapped in a block { }
        has_block = self.match("{")
        if has_block:
            self.advance()  # consume '{'
        
        # Parse statement list
        statements = []
        while not self.match("break") and not self.match("case") and not self.match("default") and not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        # If block syntax was used, expect closing brace
        if has_block:
            if not self.expect("}"):
                return None
        
        # Parse break statement
        if self.match("break"):
            self.advance()
            self.expect(";")
        
        return CaseNode(
            case_value=case_value,
            statements=statements,
            line=line,
            column=col
        )
    
    def parse_default_case(self) -> Optional[DefaultCaseNode]:
        # <default_stmt> → default : <ctrl_body>
        # Productions 403-404: default_stmt (and empty variation)
        token = self.expect("default")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect(":"):
            return None
        
        # Check if default body is wrapped in a block { }
        has_block = self.match("{")
        if has_block:
            self.advance()  # consume '{'
        
        # Parse statement list
        statements = []
        while not self.match("break") and not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        # If block syntax was used, expect closing brace
        if has_block:
            if not self.expect("}"):
                return None
        
        # Parse break statement
        if self.match("break"):
            self.advance()
            self.expect(";")
        
        return DefaultCaseNode(
            statements=statements,
            line=line,
            column=col
        )
    
    def parse_for_stmt(self) -> Optional[ForLoopNode]:
        # <for_stmt> → for(<initializer>;<condition>;<update>){<ctrl_body>}
        # Productions 408-417: for_stmt, initializer, update, up_post
        token = self.expect("for")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        # Parse initialization - Production 417
        init = None
        # Check for 'local' keyword (variable declaration in for loop)
        if self.match("local"):
            self.advance()  # consume 'local'
            
            # Parse mutability
            if not self.match_predict_set("mutability"):
                self.add_error("Expected 'var' or 'const'", self.current_token(), ["var", "const"])
                return None
            mutability = self.advance().get("lexeme")
            
            # Parse data type
            if self.match_predict_set("dtype"):
                data_type = self.advance().get("lexeme")
            elif self.match("id"):
                data_type = self.advance().get("lexeme")
            else:
                self.add_error(f"Expected data type", self.current_token(), PREDICT_SETS.get("dtype", []))
                return None
            
            # Parse first variable
            id_token = self.expect("id")
            if not id_token:
                return None
            identifier = id_token.get("lexeme")
            
            # Parse assignment for first variable
            initial_value = None
            if self.match("="):
                self.advance()
                # Parse ONLY the primary value, not full expression to avoid consuming commas
                initial_value = self.parse_primary()
            
            # Create first declaration
            declarations = [VariableDeclarationNode(
                scope="local",
                mutability=mutability,
                data_type=data_type,
                identifier=identifier,
                initial_value=initial_value,
                line=id_token.get("line", 0),
                column=id_token.get("column", 0)
            )]
            
            # Parse additional comma-separated declarations
            while self.current_token() and self.current_token().get("lexeme") == ",":
                self.advance()  # consume comma
                
                id_token = self.expect("id")
                if not id_token:
                    break
                
                identifier = id_token.get("lexeme")
                initial_value = None
                
                if self.current_token() and self.current_token().get("lexeme") == "=":
                    self.advance()  # consume =
                    # Parse ONLY the primary value
                    initial_value = self.parse_primary()
                
                declarations.append(VariableDeclarationNode(
                    scope="local",
                    mutability=mutability,
                    data_type=data_type,
                    identifier=identifier,
                    initial_value=initial_value,
                    line=id_token.get("line", 0),
                    column=id_token.get("column", 0)
                ))
            
            init = declarations if len(declarations) > 1 else declarations[0]
            
            # Expect semicolon
            if not self.expect(";"):
                return None
                
        elif self.current_token() and self.current_token().get("lexeme") != ";":
            # Production 419: <initializer> → <assign_stmt>
            # Assignment statement (e.g., i = 0)
            if self.match("id"):
                checkpoint = self.current
                id_node = self.parse_identifier_expression()
                
                # Check if followed by assignment operator
                if self.match_predict_set("assign_stmt_op"):
                    # This is an assignment statement
                    op_token = self.advance()
                    value = self.parse_expression()
                    if not value:
                        self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression", []))
                        return None
                    
                    init = AssignmentStatementNode(
                        target=id_node,
                        operator=op_token.get("lexeme"),
                        value=value,
                        line=id_node.line if hasattr(id_node, 'line') else 0,
                        column=id_node.column if hasattr(id_node, 'column') else 0
                    )
                else:
                    # Not an assignment, treat as expression
                    self.current = checkpoint
                    init = self.parse_expression()
            else:
                # Not starting with id, parse as expression
                init = self.parse_expression()
            
            if not self.expect(";"):
                return None
        else:
            # Empty initializer, just consume the semicolon
            if not self.expect(";"):
                return None
        
        # Parse condition - Production 389 (REQUIRED, non-nullable)
        condition = self.parse_expression()
        if not condition:
            # Empty condition or invalid expression
            self.add_error("Expected condition expression", self.current_token(), 
                         PREDICT_SETS.get("condition", []))
            return None
        
        if not self.expect(";"):
            return None
        
        # Parse update - Productions 420-422
        update = None
        if self.current_token() and self.current_token().get("lexeme") != ")":
            # Update can be an assignment or expression
            # Try to parse as assignment first (id = expr)
            if self.match("id"):
                checkpoint = self.current
                id_node = self.parse_identifier_expression()
                
                # Check if followed by assignment operator
                if self.match_predict_set("assign_stmt_op"):
                    # This is an assignment - but don't consume semicolon
                    op_token = self.advance()
                    value = self.parse_expression()
                    if not value:
                        self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression", []))
                        return None
                    # Create assignment node (but no semicolon in for update)
                    update = AssignmentStatementNode(
                        target=id_node,
                        operator=op_token.get("lexeme"),
                        value=value,
                        line=id_node.line if hasattr(id_node, 'line') else 0,
                        column=id_node.column if hasattr(id_node, 'column') else 0
                    )
                else:
                    # Not an assignment, rewind and parse as expression
                    self.current = checkpoint
                    update = self.parse_expression()
            else:
                # Not starting with id, just parse as expression (e.g., i++, ++i)
                update = self.parse_expression()

        
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse body
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        return ForLoopNode(
            initializer=init,
            condition=condition,
            update=update,
            body=body,
            line=line,
            column=col
        )
    
    def parse_while_stmt(self) -> Optional[WhileLoopNode]:
        # <while_stmt> → while(<condition>){<ctrl_body>}
        # Production 418
        token = self.expect("while")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        condition = self.parse_expression()
        
        # After expression, expect ) or report better error
        if not self.match(")"):
            # Expression might be incomplete - could need operators or )
            # Show both closing paren and possible expression continuations
            expected_tokens = [")", "==", "!=", ">", "<", ">=", "<=", "&&", "||", "+", "-", "*", "/", "%"]
            self.add_error("Expected closing parenthesis or operator", self.current_token(), expected_tokens)
            return None
        self.advance()  # consume )
        
        if not self.expect("{"):
            return None
        
        # Parse body
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        return WhileLoopNode(
            condition=condition,
            body=body,
            line=line,
            column=col
        )
    
    def parse_do_while_stmt(self) -> Optional[DoWhileLoopNode]:
        # <do_stmt> → do{<ctrl_body>} while(<condition>);
        # Production 419
        token = self.expect("do")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("{"):
            return None
        
        # Parse body
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        if not self.expect("while"):
            return None
        if not self.expect("("):
            return None
        
        condition = self.parse_expression()
        
        if not self.expect(")"):
            return None
        if not self.expect(";"):
            return None
        
        return DoWhileLoopNode(
            body=body,
            condition=condition,
            line=line,
            column=col
        )
