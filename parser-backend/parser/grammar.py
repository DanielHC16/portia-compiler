"""
PORTIA Language Grammar Definition
===================================
Authoritative source: revised-documents/[PARSER REVAMP] *.txt

This module exports every token-class constant, FIRST set, FOLLOW set,
and PREDICT set used by the recursive-descent parser so that
``portia_parser.py`` never hard-codes raw token strings.

243 productions · 118 non-terminals
"""

# =========================================================================
# Token-class constants
# =========================================================================
DTYPE_KEYWORDS = frozenset({"int", "long", "float", "double", "char", "string", "bool"})
LITERAL_TYPES  = frozenset({"INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT", "CHARLIT", "STRINGLIT"})
NUM_LIT_TYPES  = frozenset({"INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT"})
WHOLE_LIT_TYPES = frozenset({"INTLIT", "LONGLIT"})
REL_OPS        = frozenset({"==", "!=", ">", "<", ">=", "<="})
ASSIGN_OPS     = frozenset({"=", "+=", "-=", "*=", "/=", "%="})
UPDATE_OPS     = frozenset({"+=", "-=", "*=", "/=", "%="})
BOOL_LITERALS  = frozenset({"true", "false"})
ADDITIVE_OPS   = frozenset({"+", "-"})
MULT_OPS       = frozenset({"*", "/", "%"})

# =========================================================================
# FIRST sets  (keyed by non-terminal name as in the CFG document)
#
# Only sets that the parser actually inspects for lookahead are included.
# Epsilon-capable sets carry a sentinel "_eps" element so callers can
# distinguish nullable entries if needed.
# =========================================================================
FIRST = {
    # ── top-level ─────────────────────────────────────────────────────
    "program":          {"global", "weave", "func", "int"},
    "global_dec":       {"global", "weave"},            # eps handled by FOLLOW
    "mutability":       {"var", "const"},
    "var_or_weave":     DTYPE_KEYWORDS | {"id"},
    "const_weave":      DTYPE_KEYWORDS | {"id"},
    "dtype":            DTYPE_KEYWORDS,
    "var_or_arr":       {"=", "["},
    "const_or_arr":     {"=", "["},
    "value":            {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "multi_dec":        {","},
    "size":             {"intlit"},
    "literals_num":     {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "-"},
    "num_lit":          {"intlit", "longlit", "floatlit", "doublelit"},
    "var_1D_or_2D":     {"=", "["},
    "1D_elem_list":     {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "id"},
    "elem_value":       {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "id"},
    "1D_elem_list_tail": {","},
    "arr_2D_init_opt":  {"="},
    "arr_2D_init":      {"="},
    "2D_elem_list":     {"{"},
    "2D_elem_list_cont": {","},
    "const_1D_or_2D":   {"=", "["},
    "weave_init_list":  {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "-", "id"},
    "weave_elem":       {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "-", "id"},
    "weave_init_list_tail": {","},
    "weave_def":        {"weave"},
    "field_list":       DTYPE_KEYWORDS,
    "field_dec":        DTYPE_KEYWORDS,

    # ── functions & params ────────────────────────────────────────────
    "function":         {"func"},
    "function_def":     {"func"},
    "ret_type":         DTYPE_KEYWORDS | {"void"},
    "ret_struct":       {"["},
    "ret_2D":           {"["},
    "param":            DTYPE_KEYWORDS,
    "param_tail":       {","},
    "param_struct":     {"["},
    "param_2D":         {"["},
    "param_cont":       {","},

    # ── function body / blocks ────────────────────────────────────────
    "function_body":    {"using", "local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do"},
    "using_block":      {"using"},
    "using_stmt":       {"using"},
    "using_cont":       {","},
    "local_block":      {"local"},
    "statement_list":   {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do"},
    "statement":        {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do"},

    # ── expressions ───────────────────────────────────────────────────
    "expression":       {"id"},
    "assign_expr":      {"id"},
    "mod_or_call":      {".", "[", "("} | ASSIGN_OPS,
    "assign_mod_opt":   {".", "["},
    "lhs_index_2d_opt": {"["},
    "assign_stmt_op":   ASSIGN_OPS,
    "size_mod":         {"intlit", "id"},
    "string_or_logical_expr": {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "string_expr_tail": {".."},
    "logical_expr":     {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "logical_expr_tail": {"||"},
    "logical_term":     {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "logical_term_tail": {"&&"},
    "logical_factor":   {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "rel_expr":         {"id", "-", "("} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "rel_expr_cont":    REL_OPS,
    "arith_expr":       {"id", "-", "("} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "add_min_cont":     ADDITIVE_OPS,
    "term":             {"id", "-", "("} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "mult_div_modulo_cont": MULT_OPS,
    "primary":          {"id", "-", "("} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "cast_or_val":      DTYPE_KEYWORDS | {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "atom":             {"id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "iden_mod":         {"[", "(", "."},
    "arr_or_func":      {"[", "("},
    "2D_array":         {"["},
    "literals":         {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "arg":              {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "multi_arg":        {","},

    # ── I/O ───────────────────────────────────────────────────────────
    "I/O_stmt":         {"trap", "thread", "threadln"},
    "input_stmt":       {"trap"},
    "trap_target":      {"id"},
    "trap_suffix":      {"[", "."},
    "output_stmt":      {"thread", "threadln"},
    "print_args":       {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "print_tail":       {","},
    "string_print":     {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},

    # ── control structures ────────────────────────────────────────────
    "ctrl_struct":      {"if", "switch", "for", "while", "do"},
    "conditional_stmt": {"if", "switch"},
    "if_stmt":          {"if"},
    "condition":        {"!", "true", "false", "id", "("},
    "or_tail":          {"||"},
    "and_expr":         {"!", "true", "false", "id", "("},
    "and_tail":         {"&&"},
    "logical_op":       {"!", "true", "false", "id", "("},
    "bool_ctrl":        {"true", "false", "id", "("},
    "bool_primary":     {"true", "false", "id", "("},
    "bool_ctrl_tail":   REL_OPS,
    "rel_op":           REL_OPS,
    "ctrl_body":        {"local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "break"},
    "ctrl_statement_list": {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "break"},
    "ret_ctrl_body":    {"return"},
    "else_if_ei_stmt":  {"else"},
    "else_stmt":        {"if", "{"},
    "switch_stmt":      {"switch"},
    "case_list":        {"case"},
    "switch_val":       {"!", "(", "-"} | {"id"} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "case_stmt":        {"case"},
    "case_val":         {"charlit", "true", "false", "intlit", "longlit", "-"},
    "unique_val":       {"charlit", "true", "false", "intlit", "longlit", "-"},
    "whole_lit":        {"intlit", "longlit"},
    "default_stmt":     {"default"},

    # ── loops ─────────────────────────────────────────────────────────
    "loop_stmt":        {"for", "while", "do"},
    "for_stmt":         {"for"},
    "initializer":      {"local", "id"},
    "update":           {"id"},
    "update_op":        UPDATE_OPS,
    "while_stmt":       {"while"},
    "do_stmt":          {"do"},

    # ── return / main ─────────────────────────────────────────────────
    "ret_stmt":         {"return"},
    "main_func":        {"int"},
    "main_body":        {"using", "local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return"},
}

# =========================================================================
# FOLLOW sets  (keyed by non-terminal name)
#
# The parser consults FOLLOW when choosing the epsilon-production path.
# =========================================================================
FOLLOW = {
    "program":          set(),                      # $
    "global_dec":       {"func", "int"},
    "mutability":       {";"},
    "var_or_weave":     {";"},
    "const_weave":      {";"},
    "dtype":            {"id", "[", ")"},
    "var_or_arr":       {";"},
    "const_or_arr":     {";"},
    "value":            {",", ";", ")"},
    "multi_dec":        {";"},
    "size":             {"]"},
    "size_mod":         {"]"},
    "literals_num":     {",", ";", "}"},
    "num_lit":          {",", ";", "}"},
    "var_1D_or_2D":     {";"},
    "1D_elem_list":     {"}"},
    "elem_value":       {",", "}"},
    "1D_elem_list_tail": {"}"},
    "arr_2D_init_opt":  {";"},
    "arr_2D_init":      {";"},
    "2D_elem_list":     {"}"},
    "2D_elem_list_cont": {"}"},
    "const_1D_or_2D":   {";"},
    "weave_init_list":  {"}"},
    "weave_elem":       {",", "}"},
    "weave_init_list_tail": {"}"},
    "weave_def":        {"global", "weave", "func", "int"},
    "field_list":       {"}"},
    "field_dec":        {"int", "long", "float", "double", "char", "string", "bool", "}"},
    "function":         {"int"},
    "function_def":     {"func", "int"},
    "ret_type":         {"func", "int"},
    "ret_struct":       {"id"},
    "ret_2D":           {"id"},
    "param":            {")"},
    "param_tail":       {")"},
    "param_struct":     {",", ")"},
    "param_2D":         {",", ")"},
    "param_cont":       {"}"},
    "function_body":    {"return"},
    "using_block":      {"local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return"},
    "using_stmt":       {"using", "local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", ";"},
    "using_cont":       {";"},
    "local_block":      {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "break", "}", "case", "default"},
    "statement_list":   {"return", "}", "case", "default"},
    "statement":        {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "expression":       {";"},
    "assign_expr":      {";"},
    "mod_or_call":      {";"},
    "assign_mod_opt":   ASSIGN_OPS,
    "lhs_index_2d_opt": ASSIGN_OPS,
    "assign_stmt_op":   {";"},
    "string_or_logical_expr": {",", ";", ")"},
    "string_expr_tail": {",", ";", ")"},
    "logical_expr":     {"..", ",", ";", ")"},
    "logical_expr_tail": {"..", ",", ";", ")"},
    "logical_term":     {"||", "..", ",", ";", ")"},
    "logical_term_tail": {"||", "..", ",", ";", ")"},
    "logical_factor":   {"&&", "||", "..", ",", ";", ")"},
    "rel_expr":         {"&&", "||", "..", ",", ";", ")"},
    "rel_expr_cont":    {"&&", "||", "..", ",", ";", ")"},
    "arith_expr":       REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "add_min_cont":     REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "term":             ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "mult_div_modulo_cont": ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "primary":          MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "cast_or_val":      MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "atom":             MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "iden_mod":         MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "arr_or_func":      MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "2D_array":         MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"},
    "literals":         {",", ";", "}"} | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ")"},
    "arg":              {")"},
    "multi_arg":        {")"},
    "I/O_stmt":         {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "input_stmt":       {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "trap_target":      {")"},
    "trap_suffix":      {")"},
    "output_stmt":      {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "print_args":       {")"},
    "print_tail":       {")"},
    "string_print":     {"}"},
    "ctrl_struct":      {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "conditional_stmt": {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "if_stmt":          {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "condition":        {")", ";"},
    "or_tail":          {")", ";"},
    "and_expr":         {"||", ")", ";"},
    "and_tail":         {"||", ")", ";"},
    "logical_op":       {"&&", "||", ")", ";"},
    "bool_ctrl":        {"&&", "||", ")", ";"},
    "bool_primary":     REL_OPS | {"&&", "||", ")", ";"},
    "bool_ctrl_tail":   {"&&", "||", ")", ";"},
    "rel_op":           {"id", "-", "("} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "ctrl_body":        {"return", "}", "case", "default"},
    "ctrl_statement_list": {"return", "}", "case", "default"},
    "ret_ctrl_body":    {"}"},
    "else_if_ei_stmt":  {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "else_stmt":        {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "switch_stmt":      {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "case_list":        {"default", "}"},
    "switch_val":       {")"},
    "case_stmt":        {"case", "default", "}"},
    "case_val":         {":"},
    "unique_val":       {":"},
    "whole_lit":        {":"},
    "default_stmt":     {"}"},
    "loop_stmt":        {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "for_stmt":         {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "initializer":      {";"},
    "update":           {")"},
    "update_op":        {"id", "-", "("} | {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    "while_stmt":       {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "do_stmt":          {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},
    "ret_stmt":         {"}"},
    "main_func":        set(),                      # $
    "main_body":        {"}"},
}

# =========================================================================
# PREDICT sets  (keyed by production number 1–243)
#
# Updated for revised CFG (243 productions, 118 non-terminals).
# Key changes from prior 240-production grammar:
#   - Prod 95: assign_mod_opt → λ  (explicit epsilon)
#   - Prods 104-105: size_mod → intlit | id  (new non-terminal)
#   - Prod 116: (blank/removed – old logical_factor → ( logical_expr ))
#   - Prod 137: primary → ( cast_or_val  (parenthesised expr/cast at primary)
#   - Prod 139: cast_or_val → value )  (parenthesised expression)
#
# Only productions whose ε-alternative or multi-alternative dispatching
# actually matters at parse time are listed.
# =========================================================================
PREDICT = {
    # ── program / global ──────────────────────────────────────────────
    1:   {"global", "weave", "func", "int"},
    2:   {"global"},
    3:   {"weave"},
    4:   {"func", "int"},                           # global_dec → ε
    5:   {"var"},
    6:   {"const"},
    7:   DTYPE_KEYWORDS,
    8:   {"id"},
    9:   DTYPE_KEYWORDS,
    10:  {"id"},
    # 11-17: dtype individual keywords (trivial)
    18:  {"="},
    19:  {"["},
    20:  {"="},
    21:  {"["},
    23:  {","},
    24:  {";"},                                     # multi_dec → ε
    25:  {"intlit"},
    26:  {"intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},
    27:  {"-"},
    32:  {"="},
    33:  {"["},
    34:  {";"},                                     # var_1D_or_2D → ε
    38:  {","},
    39:  {"}"},                                     # 1D_elem_list_tail → ε
    40:  {"="},
    41:  {";"},                                     # arr_2D_init_opt → ε
    44:  {","},
    45:  {"}"},                                     # 2D_elem_list_cont → ε
    46:  {"="},
    47:  {"["},
    51:  {","},
    52:  {"}"},                                     # weave_init_list_tail → ε
    53:  {"weave"},
    54:  DTYPE_KEYWORDS,
    55:  {"}"},                                     # field_list → ε
    57:  {"func"},
    58:  {"int"},                                   # function → ε
    62:  {"["},
    63:  {"id"},                                    # ret_struct → ε
    64:  {"["},
    65:  {"id"},                                    # ret_2D → ε
    66:  DTYPE_KEYWORDS,
    67:  {")"},                                     # param → ε
    68:  {","},
    69:  {")"},                                     # param_tail → ε
    70:  {"["},
    71:  {",", ")"},                                # param_struct → ε
    72:  {"["},
    73:  {",", ")"},                                # param_2D → ε
    74:  {","},
    75:  {"}"},                                     # param_cont → ε
    76:  {"using", "local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return"},
    77:  {"using"},
    78:  {"local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return"},
    80:  {","},
    81:  {";"},                                     # using_cont → ε
    82:  {"local"},
    83:  {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "break", "}", "case", "default"},
    84:  {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do"},
    85:  {"return", "}", "case", "default"},        # statement_list → ε
    # ── expressions (renumbered from prod 91 onward) ──────────────────
    91:  {".", "[", "=", "+=", "-=", "*=", "/=", "%="},  # mod_or_call → assign path
    92:  {"("},                                     # mod_or_call → call
    93:  {"."},                                     # assign_mod_opt → . id
    94:  {"["},                                     # assign_mod_opt → [ size_mod ]
    95:  ASSIGN_OPS,                                # assign_mod_opt → ε
    96:  {"["},                                     # lhs_index_2d_opt → [ size_mod ]
    97:  ASSIGN_OPS,                                # lhs_index_2d_opt → ε
    104: {"intlit"},                                 # size_mod → intlit
    105: {"id"},                                    # size_mod → id
    107: {".."},                                    # string_expr_tail → ..
    108: {",", ";", ")"},                           # string_expr_tail → ε
    110: {"||"},                                    # logical_expr_tail → ||
    111: {"..", ",", ";", ")"},                      # logical_expr_tail → ε
    113: {"&&"},                                    # logical_term_tail → &&
    114: {"||", "..", ",", ";", ")"},                # logical_term_tail → ε
    115: {"!"},                                     # logical_factor → !
    # 116: (blank – removed production)
    117: {"-", "(", "id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},  # logical_factor → rel_expr
    119: {"=="},                                    # rel_expr_cont → ==
    120: {"!="},                                    # rel_expr_cont → !=
    121: {">"},                                     # rel_expr_cont → >
    122: {"<"},                                     # rel_expr_cont → <
    123: {">="},                                    # rel_expr_cont → >=
    124: {"<="},                                    # rel_expr_cont → <=
    125: {"&&", "||", "..", ",", ";", ")"},          # rel_expr_cont → ε
    127: {"+"},                                     # add_min_cont → +
    128: {"-"},                                     # add_min_cont → -
    129: REL_OPS | {"&&", "||", "..", ",", ";", ")"}, # add_min_cont → ε
    131: {"*"},                                     # mult_div_modulo_cont → *
    132: {"/"},                                     # mult_div_modulo_cont → /
    133: {"%"},                                     # mult_div_modulo_cont → %
    134: ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"}, # mult_div_modulo_cont → ε
    135: {"id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},  # primary → atom
    136: {"-"},                                     # primary → - primary
    137: {"("},                                     # primary → ( cast_or_val
    138: DTYPE_KEYWORDS,                            # cast_or_val → dtype ) primary
    139: {"!", "-", "(", "id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"},  # cast_or_val → value )
    144: {"["},                                     # arr_or_func → [
    145: {"("},                                     # arr_or_func → (
    146: MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"}, # arr_or_func → ε
    147: {"["},                                     # 2D_array → [
    148: MULT_OPS | ADDITIVE_OPS | REL_OPS | {"&&", "||", "..", ",", ";", ")"}, # 2D_array → ε
    158: {")"},                                     # arg → ε
    159: {","},                                     # multi_arg → ,
    160: {")"},                                     # multi_arg → ε
    # ── I/O ───────────────────────────────────────────────────────────
    161: {"trap"},                                   # I/O_stmt → input
    162: {"thread", "threadln"},                     # I/O_stmt → output
    171: {","},                                     # print_tail → ,
    172: {")"},                                     # print_tail → ε
    # ── control ───────────────────────────────────────────────────────
    174: {"if", "switch"},                           # ctrl_struct → conditional
    175: {"for", "while", "do"},                     # ctrl_struct → loop
    180: {"||"},                                    # or_tail → ||
    181: {")", ";"},                                 # or_tail → ε
    183: {"&&"},                                    # and_tail → &&
    184: {"||", ")", ";"},                           # and_tail → ε
    188: {"true"},                                   # bool_primary → true
    189: {"false"},                                  # bool_primary → false
    190: {"id"},                                    # bool_primary → id
    191: {"("},                                     # bool_primary → (
    192: REL_OPS,                                   # bool_ctrl_tail → rel_op
    193: {"&&", "||", ")", ";"},                     # bool_ctrl_tail → ε
    201: {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do"},  # ctrl_statement_list → stmt_list
    202: {"break"},                                  # ctrl_statement_list → break
    203: {"return"},                                 # ret_ctrl_body → return
    204: {"}"},                                     # ret_ctrl_body → ε
    205: {"else"},                                   # else_if_ei_stmt → else
    206: {"id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return", "}", "case", "default"},  # else_if_ei_stmt → ε
    210: {"case"},                                   # case_list → case
    211: {"default", "}"},                          # case_list → ε
    223: {"default"},                                # default_stmt → default
    224: {"}"},                                     # default_stmt → ε
    225: {"for"},                                    # loop_stmt → for
    226: {"while"},                                  # loop_stmt → while
    227: {"do"},                                     # loop_stmt → do
    229: {"local"},                                  # initializer → local
    230: {"id"},                                    # initializer → id
    231: {";"},                                     # initializer → ε
    232: {"id"},                                    # update → id
    233: {")"},                                     # update → ε
    243: {"using", "local", "id", "trap", "thread", "threadln", "if", "switch", "for", "while", "do", "return"},  # main_body
}
