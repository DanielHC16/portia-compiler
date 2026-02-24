"""
PORTIA Language Grammar Definition
===================================

This module exports every token-class constant, FIRST set, FOLLOW set,
and PREDICT set used by the recursive-descent parser so that
portia_parser.py never hard-codes raw token strings.

247 productions · 116 non-terminals
"""

# =========================================================================
# Token-class constants
# =========================================================================
DTYPE_KEYWORDS  = frozenset({"int", "long", "float", "double", "char", "string", "bool"})
LITERAL_TYPES   = frozenset({"INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT", "CHARLIT", "STRINGLIT"})
NUM_LIT_TYPES   = frozenset({"INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT"})
WHOLE_LIT_TYPES = frozenset({"INTLIT", "LONGLIT"})
REL_OPS         = frozenset({"==", "!=", ">", "<", ">=", "<="})
ASSIGN_OPS      = frozenset({"=", "+=", "-=", "*=", "/=", "%="})
UPDATE_OPS      = frozenset({"+=", "-=", "*=", "/=", "%="})
BOOL_LITERALS   = frozenset({"true", "false"})
ADDITIVE_OPS    = frozenset({"+", "-"})
MULT_OPS        = frozenset({"*", "/", "%"})

# =========================================================================
# FIRST sets  (keyed by non-terminal name as in the CFG document)
#
# Only non-epsilon elements; nullable NTs have their epsilon handled
# by checking FOLLOW in the parser.
# =========================================================================
FIRST = {
    # -- top-level -----------------------------------------------------
    "program":              {"global", "weave", "func", "int"},
    "global_dec":           {"global", "weave"},
    "mutability":           {"var", "const"},
    "var_or_weave":         DTYPE_KEYWORDS | {"id"},
    "const_weave":          DTYPE_KEYWORDS | {"id"},
    "dtype":                DTYPE_KEYWORDS,
    "var_or_arr":           {"=", "["},
    "const_or_arr":         {"=", "["},
    "value":                {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "multi_dec":            {","},
    "size":                 {"intlit"},
    "literals_num":         {"intlit", "longlit", "floatlit", "doublelit", "charlit",
                             "stringlit", "true", "false", "-"},
    "num_lit":              {"intlit", "longlit", "floatlit", "doublelit"},
    "var_1D_or_2D":         {"=", "["},
    "1D_elem_list":         {"intlit", "longlit", "floatlit", "doublelit", "charlit",
                             "stringlit", "true", "false", "id"},
    "elem_value":           {"intlit", "longlit", "floatlit", "doublelit", "charlit",
                             "stringlit", "true", "false", "id"},
    "1D_elem_list_tail":    {","},
    "arr_2D_init_opt":      {"="},
    "arr_2D_init":          {"="},
    "2D_elem_list":         {"{"},
    "2D_elem_list_cont":    {","},
    "const_1D_or_2D":       {"=", "["},
    "weave_init_list":      {"intlit", "longlit", "floatlit", "doublelit", "charlit",
                             "stringlit", "true", "false", "-", "id"},
    "weave_elem":           {"intlit", "longlit", "floatlit", "doublelit", "charlit",
                             "stringlit", "true", "false", "-", "id"},
    "weave_init_list_tail": {","},
    "weave_def":            {"weave"},
    "field_list":           DTYPE_KEYWORDS,
    "field_dec":            DTYPE_KEYWORDS,

    # -- functions & params --------------------------------------------
    "function":             {"func"},
    "function_def":         {"func"},
    "ret_type":             DTYPE_KEYWORDS | {"void"},
    "ret_struct":           {"["},
    "ret_2D":               {"["},
    "param":                DTYPE_KEYWORDS,
    "param_tail":           {","},
    "param_struct":         {"["},
    "param_2D":             {"["},

    # -- function body / blocks ----------------------------------------
    "function_body":        {"using", "local", "id", "trap", "thread", "threadln",
                             "if", "switch", "for", "while", "do"},
    "using_block":          {"using"},
    "using_stmt":           {"using"},
    "using_cont":           {","},
    "local_block":          {"local"},
    "statement_list":       {"id", "trap", "thread", "threadln", "if", "switch",
                             "for", "while", "do"},
    "statement":            {"id", "trap", "thread", "threadln", "if", "switch",
                             "for", "while", "do"},

    # -- expressions ---------------------------------------------------
    "expression":           {"id"},
    "assign_expr":          {"id"},
    "mod_or_call":          {".", "[", "(", "=", "+=", "-=", "*=", "/=", "%="},
    "assign_mod_opt":       {".", "["},
    "lhs_index_2d_opt":     {"["},
    "assign_stmt_op":       {"=", "+=", "-=", "*=", "/=", "%="},
    "size_mod":             {"intlit", "id"},
    "string_or_logical_expr": {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                               "charlit", "stringlit", "true", "false", "-", "("},
    "string_expr_tail":     {".."},
    "logical_expr":         {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "logical_expr_tail":    {"||"},
    "logical_term":         {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "logical_term_tail":    {"&&"},
    "logical_factor":       {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "rel_expr":             {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "rel_expr_cont":        REL_OPS,
    "arith_expr":           {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "add_min_cont":         ADDITIVE_OPS,
    "term":                 {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "mult_div_modulo_cont": MULT_OPS,
    "primary":              {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "cast_or_val":          DTYPE_KEYWORDS | {"!", "id", "intlit", "longlit", "floatlit",
                             "doublelit", "charlit", "stringlit", "true", "false", "-", "("},
    "atom":                 {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false"},
    "iden_mod":             {"[", "(", "."},
    "arr_or_func":          {"[", "("},
    "2D_array":             {"["},
    "literals":             {"intlit", "longlit", "floatlit", "doublelit", "charlit",
                             "stringlit", "true", "false"},
    "arg":                  {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "multi_arg":            {","},

    # -- I/O -----------------------------------------------------------
    "I/O_stmt":             {"trap", "thread", "threadln"},
    "input_stmt":           {"trap"},
    "trap_target":          {"id"},
    "trap_suffix":          {"[", "."},
    "output_stmt":          {"thread", "threadln"},
    "print_args":           {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "print_tail":           {","},

    # -- control structures --------------------------------------------
    "ctrl_struct":          {"if", "switch", "for", "while", "do"},
    "conditional_stmt":     {"if", "switch"},
    "if_stmt":              {"if"},
    "condition":            {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "or_tail":              {"||"},
    "and_expr":             {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "and_tail":             {"&&"},
    "logical_op":           {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "bool_ctrl":            {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "bool_ctrl_tail":       REL_OPS,
    "cmp_start":            {"-", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit"},
    "rel_op":               REL_OPS,
    "ctrl_body":            {"local", "id", "trap", "thread", "threadln", "if",
                             "switch", "for", "while", "do", "break"},
    "ctrl_statement_list":  {"id", "trap", "thread", "threadln", "if", "switch",
                             "for", "while", "do", "break"},
    "break_opt":            {"break"},
    "ret_ctrl_body":        {"return"},
    "else_if_ei_stmt":      {"else"},
    "else_stmt":            {"if", "{"},
    "switch_stmt":          {"switch"},
    "case_list":            {"case"},
    "switch_val":           {"!", "id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "case_stmt":            {"case"},
    "case_val":             {"charlit", "true", "false", "intlit", "longlit", "-"},
    "unique_val":           {"charlit", "true", "false", "intlit", "longlit", "-"},
    "whole_lit":            {"intlit", "longlit"},
    "default_stmt":         {"default"},

    # -- loops ---------------------------------------------------------
    "loop_stmt":            {"for", "while", "do"},
    "for_stmt":             {"for"},
    "initializer":          {"local", "id"},
    "update":               {"id"},
    "update_op":            UPDATE_OPS,
    "while_stmt":           {"while"},
    "do_stmt":              {"do"},

    # -- return / main -------------------------------------------------
    "ret_stmt":             {"return"},
    "main_func":            {"int"},
    "main_body":            {"using", "local", "id", "trap", "thread", "threadln",
                             "if", "switch", "for", "while", "do", "return"},
}

# =========================================================================
# FOLLOW sets  (keyed by non-terminal name)
#
# The parser consults FOLLOW when choosing the epsilon-production path.
# =========================================================================
FOLLOW = {
    "program":              set(),                        # $
    "global_dec":           {"func", "int"},
    "mutability":           {";"},
    "var_or_weave":         {";"},
    "const_weave":          {";"},
    "dtype":                {"id", "[", ")"},
    "var_or_arr":           {";"},
    "const_or_arr":         {";"},
    "value":                {",", ";", ")"},
    "multi_dec":            {";"},
    "size":                 {"]"},
    "literals_num":         {",", ";", "}"},
    "num_lit":              {",", ";", "}"},
    "var_1D_or_2D":         {";"},
    "1D_elem_list":         {"}"},
    "elem_value":           {",", "}"},
    "1D_elem_list_tail":    {"}"},
    "arr_2D_init_opt":      {";"},
    "arr_2D_init":          {";"},
    "2D_elem_list":         {"}"},
    "2D_elem_list_cont":    {"}"},
    "const_1D_or_2D":       {";"},
    "weave_init_list":      {"}"},
    "weave_elem":           {",", "}"},
    "weave_init_list_tail": {"}"},
    "weave_def":            {"global", "weave", "func", "int"},
    "field_list":           {"}"},
    "field_dec":            {"int", "long", "float", "double", "char", "string", "bool", "}"},
    "function":             {"int"},
    "function_def":         {"func", "int"},
    "ret_type":             {"func", "int"},
    "ret_struct":           {"id"},
    "ret_2D":               {"id"},
    "param":                {")"},
    "param_tail":           {")"},
    "param_struct":         {",", ")"},
    "param_2D":             {",", ")"},
    "function_body":        {"return"},
    "using_block":          {"local", "id", "trap", "thread", "threadln", "if", "switch",
                             "for", "while", "do", "return"},
    "using_stmt":           {";"},
    "using_cont":           {";"},
    "local_block":          {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "statement_list":       {"return", "break", "}", "case", "default"},
    "statement":            {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "expression":           {";"},
    "assign_expr":          {";"},
    "mod_or_call":          {";"},
    "assign_mod_opt":       {"=", "+=", "-=", "*=", "/=", "%="},
    "lhs_index_2d_opt":     {"=", "+=", "-=", "*=", "/=", "%="},
    "assign_stmt_op":       {";"},
    "size_mod":             {"]"},
    "string_or_logical_expr": {",", ";", ")"},
    "string_expr_tail":     {",", ";", ")"},
    "logical_expr":         {"..", ",", ";", ")"},
    "logical_expr_tail":    {"..", ",", ";", ")"},
    "logical_term":         {"||", "..", ",", ";", ")"},
    "logical_term_tail":    {"||", "..", ",", ";", ")"},
    "logical_factor":       {"&&", "||", "..", ",", ";", ")"},
    "rel_expr":             {"&&", "||", "..", ",", ";", ")"},
    "rel_expr_cont":        {"&&", "||", "..", ",", ";", ")"},
    "arith_expr":           REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "add_min_cont":         REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "term":                 ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "mult_div_modulo_cont": ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "primary":              MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "cast_or_val":          MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "atom":                 MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "iden_mod":             MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "arr_or_func":          MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "2D_array":             MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "literals":             {",", ";", "}"} | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ")"},
    "arg":                  {")"},
    "multi_arg":            {")"},
    "I/O_stmt":             {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "input_stmt":           {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "trap_target":          {")"},
    "trap_suffix":          {")"},
    "output_stmt":          {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "print_args":           {")"},
    "print_tail":           {")"},
    "ctrl_struct":          {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "conditional_stmt":     {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "if_stmt":              {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "condition":            {")", ";"},
    "or_tail":              {")", ";"},
    "and_expr":             {"||", ")", ";"},
    "and_tail":             {"||", ")", ";"},
    "logical_op":           {"&&", "||", ")", ";"},
    "bool_ctrl":            {"&&", "||", ")", ";"},
    "bool_ctrl_tail":       {"&&", "||", ")", ";"},
    "cmp_start":            MULT_OPS | ADDITIVE_OPS | REL_OPS,
    "rel_op":               {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "ctrl_body":            {"return", "}", "case", "default"},
    "ctrl_statement_list":  {"return", "}", "case", "default"},
    "break_opt":            {"return", "}", "case", "default"},
    "ret_ctrl_body":        {"}", "case", "default"},
    "else_if_ei_stmt":      {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "else_stmt":            {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "switch_stmt":          {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "case_list":            {"default", "}"},
    "switch_val":           {")"},
    "case_stmt":            {"case", "default", "}"},
    "case_val":             {":"},
    "unique_val":           {":"},
    "whole_lit":            {":"},
    "default_stmt":         {"}"},
    "loop_stmt":            {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "for_stmt":             {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "initializer":          {";"},
    "update":               {")"},
    "update_op":            {"id", "intlit", "longlit", "floatlit", "doublelit",
                             "charlit", "stringlit", "true", "false", "-", "("},
    "while_stmt":           {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "do_stmt":              {"id", "trap", "thread", "threadln", "if", "switch", "for",
                             "while", "do", "return", "break", "}", "case", "default"},
    "ret_stmt":             {"}", "case", "default"},
    "main_func":            set(),                        # $
    "main_body":            {"}"},
}

# =========================================================================
# PREDICT sets  (keyed by production number 1-247)
# =========================================================================
PREDICT = {
    # -- program / global_dec  (1-4) ----------------------------------
    1:   {"global", "weave", "func", "int"},
    2:   {"global"},
    3:   {"weave"},
    4:   {"func", "int"},                           # global_dec -> eps
    # -- mutability (5-6) ---------------------------------------------
    5:   {"var"},
    6:   {"const"},
    # -- var_or_weave / const_weave (7-10) ----------------------------
    7:   DTYPE_KEYWORDS,
    8:   {"id"},
    9:   DTYPE_KEYWORDS,
    10:  {"id"},
    # -- dtype (11-17) ------------------------------------------------
    11:  {"int"},
    12:  {"long"},
    13:  {"float"},
    14:  {"double"},
    15:  {"char"},
    16:  {"string"},
    17:  {"bool"},
    # -- var_or_arr / const_or_arr (18-21) ----------------------------
    18:  {"="},
    19:  {"["},
    20:  {"="},
    21:  {"["},
    # -- value (22) ---------------------------------------------------
    22:  {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    # -- multi_dec (23-24) --------------------------------------------
    23:  {","},
    24:  {";"},                                     # multi_dec -> eps
    # -- size (25) ----------------------------------------------------
    25:  {"intlit"},
    # -- literals_num (26-27) -----------------------------------------
    26:  {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit",
          "true", "false"},
    27:  {"-"},
    # -- num_lit (28-31) ----------------------------------------------
    28:  {"intlit"},
    29:  {"longlit"},
    30:  {"floatlit"},
    31:  {"doublelit"},
    # -- var_1D_or_2D (32-34) -----------------------------------------
    32:  {"="},
    33:  {"["},
    34:  {";"},                                     # var_1D_or_2D -> eps
    # -- 1D_elem_list (35) --------------------------------------------
    35:  {"id", "intlit", "longlit", "floatlit", "doublelit", "charlit",
          "stringlit", "true", "false"},
    # -- elem_value (36-37) -------------------------------------------
    36:  {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit",
          "true", "false"},
    37:  {"id"},
    # -- 1D_elem_list_tail (38-39) ------------------------------------
    38:  {","},
    39:  {"}"},                                     # 1D_elem_list_tail -> eps
    # -- arr_2D_init_opt (40-41) --------------------------------------
    40:  {"="},
    41:  {";"},                                     # arr_2D_init_opt -> eps
    # -- arr_2D_init (42) ---------------------------------------------
    42:  {"="},
    # -- 2D_elem_list / 2D_elem_list_cont (43-45) --------------------
    43:  {"{"},
    44:  {","},
    45:  {"}"},                                     # 2D_elem_list_cont -> eps
    # -- const_1D_or_2D (46-47) ---------------------------------------
    46:  {"="},
    47:  {"["},
    # -- weave_init_list / weave_elem / weave_init_list_tail (48-52) --
    48:  {"-", "id", "intlit", "longlit", "floatlit", "doublelit", "charlit",
          "stringlit", "true", "false"},
    49:  {"-", "intlit", "longlit", "floatlit", "doublelit", "charlit",
          "stringlit", "true", "false"},
    50:  {"id"},
    51:  {","},
    52:  {"}"},                                     # weave_init_list_tail -> eps
    # -- weave_def (53) -----------------------------------------------
    53:  {"weave"},
    # -- field_list / field_dec (54-56) --------------------------------
    54:  DTYPE_KEYWORDS,
    55:  {"}"},                                     # field_list -> eps
    56:  DTYPE_KEYWORDS,
    # -- function (57-58) ---------------------------------------------
    57:  {"func"},
    58:  {"int"},                                   # function -> eps
    # -- function_def (59) --------------------------------------------
    59:  {"func"},
    # -- ret_type (60-61) ---------------------------------------------
    60:  DTYPE_KEYWORDS,
    61:  {"void"},
    # -- ret_struct (62-63) -------------------------------------------
    62:  {"["},
    63:  {"id"},                                    # ret_struct -> eps
    # -- ret_2D (64-65) -----------------------------------------------
    64:  {"["},
    65:  {"id"},                                    # ret_2D -> eps
    # -- param / param_tail (66-69) -----------------------------------
    66:  DTYPE_KEYWORDS,
    67:  {")"},                                     # param -> eps
    68:  {","},
    69:  {")"},                                     # param_tail -> eps
    # -- param_struct (70-71) -----------------------------------------
    70:  {"["},
    71:  {",", ")"},                                # param_struct -> eps
    # -- param_2D (72-73) ---------------------------------------------
    72:  {"["},
    73:  {",", ")"},                                # param_2D -> eps
    # -- function_body (74) -------------------------------------------
    74:  {"using", "local", "id", "trap", "thread", "threadln",
          "if", "switch", "for", "while", "do", "return"},
    # -- using_block (75-76) ------------------------------------------
    75:  {"using"},
    76:  {"local", "id", "trap", "thread", "threadln", "if", "switch",
          "for", "while", "do", "return"},
    # -- using_stmt (77) ----------------------------------------------
    77:  {"using"},
    # -- using_cont (78-79) -------------------------------------------
    78:  {","},
    79:  {";"},                                     # using_cont -> eps
    # -- local_block (80-81) ------------------------------------------
    80:  {"local"},
    81:  {"id", "trap", "thread", "threadln", "if", "switch", "for", "while",
          "do", "return", "break", "}", "case", "default"},
    # -- statement_list (82-83) ---------------------------------------
    82:  {"id", "trap", "thread", "threadln", "if", "switch", "for",
          "while", "do"},
    83:  {"return", "break", "}", "case", "default"},
    # -- statement (84-86) --------------------------------------------
    84:  {"id"},
    85:  {"trap", "thread", "threadln"},
    86:  {"if", "switch", "for", "while", "do"},
    # -- expression / assign_expr (87-88) -----------------------------
    87:  {"id"},
    88:  {"id"},
    # -- mod_or_call (89-90) ------------------------------------------
    89:  {".", "[", "=", "+=", "-=", "*=", "/=", "%="},
    90:  {"("},
    # -- assign_mod_opt (91-93) ---------------------------------------
    91:  {"."},
    92:  {"["},
    93:  {"=", "+=", "-=", "*=", "/=", "%="},       # assign_mod_opt -> eps
    # -- lhs_index_2d_opt (94-95) -------------------------------------
    94:  {"["},
    95:  {"=", "+=", "-=", "*=", "/=", "%="},       # lhs_index_2d_opt -> eps
    # -- assign_stmt_op (96-101) --------------------------------------
    96:  {"="},
    97:  {"+="},
    98:  {"-="},
    99:  {"*="},
    100: {"/="},
    101: {"%="},
    # -- size_mod (102-103) -------------------------------------------
    102: {"intlit"},
    103: {"id"},
    # -- string_or_logical_expr / string_expr_tail (104-106) ----------
    104: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    105: {".."},
    106: {",", ";", ")"},                           # string_expr_tail -> eps
    # -- logical_expr / logical_expr_tail (107-109) -------------------
    107: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    108: {"||"},
    109: {"..", ",", ";", ")"},                     # logical_expr_tail -> eps
    # -- logical_term / logical_term_tail (110-112) -------------------
    110: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    111: {"&&"},
    112: {"||", "..", ",", ";", ")"},               # logical_term_tail -> eps
    # -- logical_factor (113-114) -------------------------------------
    113: {"!"},
    114: {"-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    # -- rel_expr / rel_expr_cont (115-122) ---------------------------
    115: {"-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    116: {"=="},
    117: {"!="},
    118: {">"},
    119: {"<"},
    120: {">="},
    121: {"<="},
    122: {"&&", "||", "..", ",", ";", ")"},         # rel_expr_cont -> eps
    # -- arith_expr / add_min_cont (123-126) --------------------------
    123: {"-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    124: {"+"},
    125: {"-"},
    126: REL_OPS | {"&&", "||", "..", ",", ";", ")"},  # add_min_cont -> eps
    # -- term / mult_div_modulo_cont (127-131) ------------------------
    127: {"-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    128: {"*"},
    129: {"/"},
    130: {"%"},
    131: ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    # -- primary (132-134) --------------------------------------------
    132: {"id", "intlit", "longlit", "floatlit", "doublelit", "charlit",
          "stringlit", "true", "false"},
    133: {"-"},
    134: {"("},
    # -- cast_or_val (135-136) ----------------------------------------
    135: DTYPE_KEYWORDS,
    136: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    # -- atom (137-138) -----------------------------------------------
    137: {"id"},
    138: {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit",
          "true", "false"},
    # -- iden_mod (139-140) -------------------------------------------
    139: {"[", "(", "*", "/", "%", "+", "-", "==", "!=", ">", "<", ">=", "<=",
          "&&", "||", "..", ",", ";", ")"},
    140: {"."},
    # -- arr_or_func (141-143) ----------------------------------------
    141: {"["},
    142: {"("},
    143: {"*", "/", "%", "+", "-", "==", "!=", ">", "<", ">=", "<=",
          "&&", "||", "..", ",", ";", ")"},
    # -- 2D_array (144-145) -------------------------------------------
    144: {"["},
    145: {"*", "/", "%", "+", "-", "==", "!=", ">", "<", ">=", "<=",
          "&&", "||", "..", ",", ";", ")"},
    # -- literals (146-153) -------------------------------------------
    146: {"intlit"},
    147: {"longlit"},
    148: {"floatlit"},
    149: {"doublelit"},
    150: {"charlit"},
    151: {"stringlit"},
    152: {"true"},
    153: {"false"},
    # -- arg / multi_arg (154-157) ------------------------------------
    154: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    155: {")"},                                     # arg -> eps
    156: {","},
    157: {")"},                                     # multi_arg -> eps
    # -- I/O_stmt (158-159) -------------------------------------------
    158: {"trap"},
    159: {"thread", "threadln"},
    # -- input_stmt (160) ---------------------------------------------
    160: {"trap"},
    # -- trap_target (161) --------------------------------------------
    161: {"id"},
    # -- trap_suffix (162-164) ----------------------------------------
    162: {"["},
    163: {"."},
    164: {")"},                                     # trap_suffix -> eps
    # -- output_stmt (165-166) ----------------------------------------
    165: {"thread"},
    166: {"threadln"},
    # -- print_args / print_tail (167-169) ----------------------------
    167: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    168: {","},
    169: {")"},                                     # print_tail -> eps
    # -- ctrl_struct (170-171) ----------------------------------------
    170: {"if", "switch"},
    171: {"for", "while", "do"},
    # -- conditional_stmt (172-173) -----------------------------------
    172: {"if"},
    173: {"switch"},
    # -- if_stmt (174) ------------------------------------------------
    174: {"if"},
    # -- condition / or_tail (175-177) --------------------------------
    175: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    176: {"||"},
    177: {")", ";"},                                # or_tail -> eps
    # -- and_expr / and_tail (178-180) --------------------------------
    178: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    179: {"&&"},
    180: {"||", ")", ";"},                          # and_tail -> eps
    # -- logical_op (181-182) -----------------------------------------
    181: {"!"},
    182: {"-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    # -- bool_ctrl (183-187) ------------------------------------------
    183: {"id"},
    184: {"true"},
    185: {"false"},
    186: {"("},
    187: {"-", "intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit"},
    # -- bool_ctrl_tail (188-189) -------------------------------------
    188: REL_OPS,
    189: {"&&", "||", ")", ";"},                    # bool_ctrl_tail -> eps
    # -- cmp_start (190-196) ------------------------------------------
    190: {"-"},
    191: {"intlit"},
    192: {"longlit"},
    193: {"floatlit"},
    194: {"doublelit"},
    195: {"charlit"},
    196: {"stringlit"},
    # -- rel_op (197-202) ---------------------------------------------
    197: {"=="},
    198: {"!="},
    199: {">"},
    200: {"<"},
    201: {">="},
    202: {"<="},
    # -- ctrl_body (203) ----------------------------------------------
    203: {"local", "break", "id", "trap", "thread", "threadln", "if", "switch",
          "for", "while", "do", "return", "}", "case", "default"},
    # -- ctrl_statement_list (204) ------------------------------------
    204: {"id", "trap", "thread", "threadln", "if", "switch", "for", "while",
          "do", "break", "return", "}", "case", "default"},
    # -- break_opt (205-206) ------------------------------------------
    205: {"break"},
    206: {"return", "}", "case", "default"},        # break_opt -> eps
    # -- ret_ctrl_body (207-208) --------------------------------------
    207: {"return"},
    208: {"}", "case", "default"},                  # ret_ctrl_body -> eps
    # -- else_if_ei_stmt (209-210) ------------------------------------
    209: {"else"},
    210: {"id", "trap", "thread", "threadln", "if", "switch", "for", "while",
          "do", "return", "break", "}", "case", "default"},
    # -- else_stmt (211-212) ------------------------------------------
    211: {"if"},
    212: {"{"},
    # -- switch_stmt (213) --------------------------------------------
    213: {"switch"},
    # -- case_list (214-215) ------------------------------------------
    214: {"case"},
    215: {"default", "}"},                          # case_list -> eps
    # -- switch_val (216) ---------------------------------------------
    216: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit",
          "charlit", "stringlit", "true", "false"},
    # -- case_stmt (217) ----------------------------------------------
    217: {"case"},
    # -- case_val / unique_val (218-224) ------------------------------
    218: {"charlit", "true", "false", "intlit", "longlit", "-"},
    219: {"charlit"},
    220: {"true"},
    221: {"false"},
    222: {"intlit"},
    223: {"longlit"},
    224: {"-"},
    # -- whole_lit (225-226) ------------------------------------------
    225: {"intlit"},
    226: {"longlit"},
    # -- default_stmt (227-228) ---------------------------------------
    227: {"default"},
    228: {"}"},                                     # default_stmt -> eps
    # -- loop_stmt (229-231) ------------------------------------------
    229: {"for"},
    230: {"while"},
    231: {"do"},
    # -- for_stmt (232) -----------------------------------------------
    232: {"for"},
    # -- initializer (233-235) ----------------------------------------
    233: {"local"},
    234: {"id"},
    235: {";"},                                     # initializer -> eps
    # -- update (236-237) ---------------------------------------------
    236: {"id"},
    237: {")"},                                     # update -> eps
    # -- update_op (238-242) ------------------------------------------
    238: {"+="},
    239: {"-="},
    240: {"*="},
    241: {"/="},
    242: {"%="},
    # -- while_stmt (243) ---------------------------------------------
    243: {"while"},
    # -- do_stmt (244) ------------------------------------------------
    244: {"do"},
    # -- ret_stmt (245) -----------------------------------------------
    245: {"return"},
    # -- main_func (246) ----------------------------------------------
    246: {"int"},
    # -- main_body (247) ----------------------------------------------
    247: {"using", "local", "id", "trap", "thread", "threadln", "if", "switch",
          "for", "while", "do", "return"},
}
