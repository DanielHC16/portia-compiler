"""
PORTIA Language Grammar Definition
===================================
Auto-generated from portia-cfg.md
DO NOT EDIT DIRECTLY - regenerate from source
"""

# Epsilon symbol for empty productions
EPSILON = "ε"

# Start symbol
START_SYMBOL = "program"

# Grammar definition
# Format: "non_terminal": [[production1], [production2], ...]
GRAMMAR = {
    "program": [
        ["global_section"],
    ],
    "global_section": [
        ["global_decl", "global_section"],
        ["int", "id", "int_array_with_init", ";", "global_section"],
        ["long", "id", "long_array_with_init", ";", "global_section"],
        ["float", "id", "float_array_with_init", ";", "global_section"],
        ["double", "id", "double_array_with_init", ";", "global_section"],
        ["char", "id", "char_array_with_init", ";", "global_section"],
        ["string", "id", "string_array_with_init", ";", "global_section"],
        ["bool", "id", "bool_array_with_init", ";", "global_section"],
        ["weave", "id", "{", "field_list", "}", "global_section"],
        ["id", "weave_inst_decl", "global_section"],
        ["function_decl", "func_and_main"],
        ["int", "main", "(", ")", "{", "main_body", "}"],
    ],
    "func_and_main": [
        ["function_decl", "func_and_main"],
        ["int", "main", "(", ")", "{", "main_body", "}"],
    ],
    "global_decl": [
        ["global", "mutability", "int", "id", "=", "intlit", "int_global_cont", ";"],
        ["global", "mutability", "long", "id", "=", "longlit", "long_global_cont", ";"],
        ["global", "mutability", "float", "id", "=", "floatlit", "float_global_cont", ";"],
        ["global", "mutability", "double", "id", "=", "doublelit", "double_global_cont", ";"],
        ["global", "mutability", "char", "id", "=", "charlit", "char_global_cont", ";"],
        ["global", "mutability", "string", "id", "=", "stringlit", "string_global_cont", ";"],
        ["global", "mutability", "bool", "id", "=", "bool_lit", "bool_global_cont", ";"],
    ],
    "function_decl": [
        ["func", "int", "func_ret_int"],
        ["func", "long", "func_ret_long"],
        ["func", "float", "func_ret_float"],
        ["func", "double", "func_ret_double"],
        ["func", "char", "func_ret_char"],
        ["func", "string", "func_ret_string"],
        ["func", "bool", "func_ret_bool"],
        ["func", "id", "func_ret_weave"],
        ["func", "void", "id", "(", ")", "{", "function_body_void", "}"],
    ],
    "bool_lit": [
        ["true"],
        ["false"],
    ],
    "int_global_cont": [
        [",", "id", "=", "intlit", "int_global_cont"],
        [EPSILON],
    ],
    "long_global_cont": [
        [",", "id", "=", "longlit", "long_global_cont"],
        [EPSILON],
    ],
    "float_global_cont": [
        [",", "id", "=", "floatlit", "float_global_cont"],
        [EPSILON],
    ],
    "double_global_cont": [
        [",", "id", "=", "doublelit", "double_global_cont"],
        [EPSILON],
    ],
    "char_global_cont": [
        [",", "id", "=", "charlit", "char_global_cont"],
        [EPSILON],
    ],
    "string_global_cont": [
        [",", "id", "=", "stringlit", "string_global_cont"],
        [EPSILON],
    ],
    "bool_global_cont": [
        [",", "id", "=", "bool_lit", "bool_global_cont"],
        [EPSILON],
    ],
    "weave_inst_decl": [
        ["id", "weave_inst_tail", "weave_inst_cont", ";"],
        ["weave_array_with_init", "weave_arr_cont", ";"],
    ],
    "weave_inst_tail": [
        ["=", "{", "weave_field_value", "weave_field_list_tail", "}"],
        ["weave_array_with_init"],
    ],
    "weave_field_value": [
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["charlit"],
        ["stringlit"],
        ["true"],
        ["false"],
        ["{", "weave_value_list", "}"],
    ],
    "weave_value_list": [
        ["weave_field_value", "weave_value_tail"],
    ],
    "weave_value_tail": [
        [",", "weave_field_value", "weave_value_tail"],
        [EPSILON],
    ],
    "weave_field_list_tail": [
        [",", "weave_field_value", "weave_field_list_tail"],
        [EPSILON],
    ],
    "weave_inst_cont": [
        [",", "id", "weave_inst_tail", "weave_inst_cont"],
        [EPSILON],
    ],
    "weave_arr_cont": [
        [",", "id", "weave_array_with_init", "weave_arr_cont"],
        [EPSILON],
    ],
    "weave_array_with_init": [
        ["[", "size", "]", "weave_array_init_tail"],
    ],
    "weave_array_init_tail": [
        ["[", "size", "]", "weave_arr_init_opt_2d"],
        ["weave_arr_init_opt_1d"],
    ],
    "weave_arr_init_opt_1d": [
        ["=", "{", "weave_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "weave_arr_init_content_1d": [
        ["{", "weave_field_value", "weave_field_list_tail", "}", "weave_init_1d_tail"],
    ],
    "weave_init_1d_tail": [
        [",", "{", "weave_field_value", "weave_field_list_tail", "}", "weave_init_1d_tail"],
        [EPSILON],
    ],
    "weave_arr_init_opt_2d": [
        ["=", "{", "weave_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "weave_arr_init_content_2d": [
        ["{", "weave_init_row", "}", "weave_init_2d_tail"],
    ],
    "weave_init_row": [
        ["{", "weave_field_value", "weave_field_list_tail", "}", "weave_init_1d_tail"],
    ],
    "weave_init_2d_tail": [
        [",", "{", "weave_init_row", "}", "weave_init_2d_tail"],
        [EPSILON],
    ],
    "mutability": [
        ["var"],
        ["const"],
    ],
    "array_dims": [
        ["[", "size", "]", "array_dim2_opt"],
    ],
    "array_dim2_opt": [
        ["[", "size", "]"],
        [EPSILON],
    ],
    "size": [
        ["intlit"],
        ["id"],
    ],
    "int_array_with_init": [
        ["[", "size", "]", "int_array_init_tail"],
    ],
    "int_array_init_tail": [
        ["[", "size", "]", "int_arr_init_opt_2d"],
        ["int_arr_init_opt_1d"],
    ],
    "int_arr_init_opt_1d": [
        ["=", "{", "int_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "int_arr_init_content_1d": [
        ["intlit", "int_elem_1d_tail"],
    ],
    "int_elem_1d_tail": [
        [",", "intlit", "int_elem_1d_tail"],
        [EPSILON],
    ],
    "int_arr_init_opt_2d": [
        ["=", "{", "int_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "int_arr_init_content_2d": [
        ["{", "int_elem_list", "}", "int_elem_2d_tail"],
    ],
    "int_elem_list": [
        ["intlit", "int_elem_1d_tail"],
    ],
    "int_elem_2d_tail": [
        [",", "{", "int_elem_list", "}", "int_elem_2d_tail"],
        [EPSILON],
    ],
    "long_array_with_init": [
        ["[", "size", "]", "long_array_init_tail"],
    ],
    "long_array_init_tail": [
        ["[", "size", "]", "long_arr_init_opt_2d"],
        ["long_arr_init_opt_1d"],
    ],
    "long_arr_init_opt_1d": [
        ["=", "{", "long_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "long_arr_init_content_1d": [
        ["longlit", "long_elem_1d_tail"],
    ],
    "long_elem_1d_tail": [
        [",", "longlit", "long_elem_1d_tail"],
        [EPSILON],
    ],
    "long_arr_init_opt_2d": [
        ["=", "{", "long_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "long_arr_init_content_2d": [
        ["{", "long_elem_list", "}", "long_elem_2d_tail"],
    ],
    "long_elem_list": [
        ["longlit", "long_elem_1d_tail"],
    ],
    "long_elem_2d_tail": [
        [",", "{", "long_elem_list", "}", "long_elem_2d_tail"],
        [EPSILON],
    ],
    "float_array_with_init": [
        ["[", "size", "]", "float_array_init_tail"],
    ],
    "float_array_init_tail": [
        ["[", "size", "]", "float_arr_init_opt_2d"],
        ["float_arr_init_opt_1d"],
    ],
    "float_arr_init_opt_1d": [
        ["=", "{", "float_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "float_arr_init_content_1d": [
        ["floatlit", "float_elem_1d_tail"],
    ],
    "float_elem_1d_tail": [
        [",", "floatlit", "float_elem_1d_tail"],
        [EPSILON],
    ],
    "float_arr_init_opt_2d": [
        ["=", "{", "float_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "float_arr_init_content_2d": [
        ["{", "float_elem_list", "}", "float_elem_2d_tail"],
    ],
    "float_elem_list": [
        ["floatlit", "float_elem_1d_tail"],
    ],
    "float_elem_2d_tail": [
        [",", "{", "float_elem_list", "}", "float_elem_2d_tail"],
        [EPSILON],
    ],
    "double_array_with_init": [
        ["[", "size", "]", "double_array_init_tail"],
    ],
    "double_array_init_tail": [
        ["[", "size", "]", "double_arr_init_opt_2d"],
        ["double_arr_init_opt_1d"],
    ],
    "double_arr_init_opt_1d": [
        ["=", "{", "double_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "double_arr_init_content_1d": [
        ["doublelit", "double_elem_1d_tail"],
    ],
    "double_elem_1d_tail": [
        [",", "doublelit", "double_elem_1d_tail"],
        [EPSILON],
    ],
    "double_arr_init_opt_2d": [
        ["=", "{", "double_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "double_arr_init_content_2d": [
        ["{", "double_elem_list", "}", "double_elem_2d_tail"],
    ],
    "double_elem_list": [
        ["doublelit", "double_elem_1d_tail"],
    ],
    "double_elem_2d_tail": [
        [",", "{", "double_elem_list", "}", "double_elem_2d_tail"],
        [EPSILON],
    ],
    "char_array_with_init": [
        ["[", "size", "]", "char_array_init_tail"],
    ],
    "char_array_init_tail": [
        ["[", "size", "]", "char_arr_init_opt_2d"],
        ["char_arr_init_opt_1d"],
    ],
    "char_arr_init_opt_1d": [
        ["=", "{", "char_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "char_arr_init_content_1d": [
        ["charlit", "char_elem_1d_tail"],
    ],
    "char_elem_1d_tail": [
        [",", "charlit", "char_elem_1d_tail"],
        [EPSILON],
    ],
    "char_arr_init_opt_2d": [
        ["=", "{", "char_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "char_arr_init_content_2d": [
        ["{", "char_elem_list", "}", "char_elem_2d_tail"],
    ],
    "char_elem_list": [
        ["charlit", "char_elem_1d_tail"],
    ],
    "char_elem_2d_tail": [
        [",", "{", "char_elem_list", "}", "char_elem_2d_tail"],
        [EPSILON],
    ],
    "string_array_with_init": [
        ["[", "size", "]", "string_array_init_tail"],
    ],
    "string_array_init_tail": [
        ["[", "size", "]", "string_arr_init_opt_2d"],
        ["string_arr_init_opt_1d"],
    ],
    "string_arr_init_opt_1d": [
        ["=", "{", "string_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "string_arr_init_content_1d": [
        ["stringlit", "string_elem_1d_tail"],
    ],
    "string_elem_1d_tail": [
        [",", "stringlit", "string_elem_1d_tail"],
        [EPSILON],
    ],
    "string_arr_init_opt_2d": [
        ["=", "{", "string_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "string_arr_init_content_2d": [
        ["{", "string_elem_list", "}", "string_elem_2d_tail"],
    ],
    "string_elem_list": [
        ["stringlit", "string_elem_1d_tail"],
    ],
    "string_elem_2d_tail": [
        [",", "{", "string_elem_list", "}", "string_elem_2d_tail"],
        [EPSILON],
    ],
    "bool_array_with_init": [
        ["[", "size", "]", "bool_array_init_tail"],
    ],
    "bool_array_init_tail": [
        ["[", "size", "]", "bool_arr_init_opt_2d"],
        ["bool_arr_init_opt_1d"],
    ],
    "bool_arr_init_opt_1d": [
        ["=", "{", "bool_arr_init_content_1d", "}"],
        [EPSILON],
    ],
    "bool_arr_init_content_1d": [
        ["bool_lit", "bool_elem_1d_tail"],
    ],
    "bool_elem_1d_tail": [
        [",", "bool_lit", "bool_elem_1d_tail"],
        [EPSILON],
    ],
    "bool_arr_init_opt_2d": [
        ["=", "{", "bool_arr_init_content_2d", "}"],
        [EPSILON],
    ],
    "bool_arr_init_content_2d": [
        ["{", "bool_elem_list", "}", "bool_elem_2d_tail"],
    ],
    "bool_elem_list": [
        ["bool_lit", "bool_elem_1d_tail"],
    ],
    "bool_elem_2d_tail": [
        [",", "{", "bool_elem_list", "}", "bool_elem_2d_tail"],
        [EPSILON],
    ],
    "field_list": [
        ["field_dec", "field_list"],
        [EPSILON],
    ],
    "field_dec": [
        ["field_type", "id", "field_arr_opt", "field_cont", ";"],
    ],
    "field_type": [
        ["int"],
        ["long"],
        ["float"],
        ["double"],
        ["char"],
        ["string"],
        ["bool"],
        ["id"],
    ],
    "field_arr_opt": [
        ["array_dims"],
        [EPSILON],
    ],
    "field_cont": [
        [",", "id", "field_arr_opt", "field_cont"],
        [EPSILON],
    ],
    "func_ret_int": [
        ["id", "(", "param_list", ")", "{", "function_body_int", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
    ],
    "func_ret_long": [
        ["id", "(", "param_list", ")", "{", "function_body_long", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
    ],
    "func_ret_float": [
        ["id", "(", "param_list", ")", "{", "function_body_float", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
    ],
    "func_ret_double": [
        ["id", "(", "param_list", ")", "{", "function_body_double", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
    ],
    "func_ret_char": [
        ["id", "(", "param_list", ")", "{", "function_body_char", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
    ],
    "func_ret_string": [
        ["id", "(", "param_list", ")", "{", "function_body_string", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
    ],
    "func_ret_bool": [
        ["id", "(", "param_list", ")", "{", "function_body_bool", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
    ],
    "func_ret_weave": [
        ["id", "(", "param_list", ")", "{", "function_body_weave", "}"],
        ["array_dims", "id", "(", "param_list", ")", "{", "function_body_array", "}"],
        [".", "id", "id", "(", "param_list", ")", "{", "function_body_weave", "}"],
    ],
    "param_list": [
        ["param_type", "id", "param_arr_opt", "param_cont"],
        [EPSILON],
    ],
    "param_type": [
        ["int"],
        ["long"],
        ["float"],
        ["double"],
        ["char"],
        ["string"],
        ["bool"],
        ["id"],
    ],
    "param_arr_opt": [
        ["array_dims"],
        [EPSILON],
    ],
    "param_cont": [
        [",", "param_type", "id", "param_arr_opt", "param_cont"],
        [EPSILON],
    ],
    "function_body_int": [
        ["func_content_int"],
    ],
    "func_content_int": [
        ["using", "id", "using_cont", ";", "func_content_int"],
        ["local", "mutability", "local_dec_body", "func_content_int"],
        ["statement_int_no_ret", "func_content_int"],
        ["mandatory_int_return"],
    ],
    "mandatory_int_return": [
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "function_body_long": [
        ["func_content_long"],
    ],
    "func_content_long": [
        ["using", "id", "using_cont", ";", "func_content_long"],
        ["local", "mutability", "local_dec_body", "func_content_long"],
        ["statement_long_no_ret", "func_content_long"],
        ["mandatory_long_return"],
    ],
    "mandatory_long_return": [
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "function_body_float": [
        ["func_content_float"],
    ],
    "func_content_float": [
        ["using", "id", "using_cont", ";", "func_content_float"],
        ["local", "mutability", "local_dec_body", "func_content_float"],
        ["statement_float_no_ret", "func_content_float"],
        ["mandatory_float_return"],
    ],
    "mandatory_float_return": [
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "function_body_double": [
        ["func_content_double"],
    ],
    "func_content_double": [
        ["using", "id", "using_cont", ";", "func_content_double"],
        ["local", "mutability", "local_dec_body", "func_content_double"],
        ["statement_double_no_ret", "func_content_double"],
        ["mandatory_double_return"],
    ],
    "mandatory_double_return": [
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "function_body_char": [
        ["func_content_char"],
    ],
    "func_content_char": [
        ["using", "id", "using_cont", ";", "func_content_char"],
        ["local", "mutability", "local_dec_body", "func_content_char"],
        ["statement_char_no_ret", "func_content_char"],
        ["mandatory_char_return"],
    ],
    "mandatory_char_return": [
        ["return", "typed_string_ret_expr", ";"],
    ],
    "function_body_string": [
        ["func_content_string"],
    ],
    "func_content_string": [
        ["using", "id", "using_cont", ";", "func_content_string"],
        ["local", "mutability", "local_dec_body", "func_content_string"],
        ["statement_string_no_ret", "func_content_string"],
        ["mandatory_string_return"],
    ],
    "mandatory_string_return": [
        ["return", "typed_string_ret_expr", ";"],
    ],
    "function_body_bool": [
        ["func_content_bool"],
    ],
    "func_content_bool": [
        ["using", "id", "using_cont", ";", "func_content_bool"],
        ["local", "mutability", "local_dec_body", "func_content_bool"],
        ["statement_bool_no_ret", "func_content_bool"],
        ["mandatory_bool_return"],
    ],
    "mandatory_bool_return": [
        ["return", "typed_bool_ret_expr", ";"],
    ],
    "function_body_array": [
        ["func_content_array"],
    ],
    "func_content_array": [
        ["using", "id", "using_cont", ";", "func_content_array"],
        ["local", "mutability", "local_dec_body", "func_content_array"],
        ["statement_array_no_ret", "func_content_array"],
        ["mandatory_array_return"],
    ],
    "mandatory_array_return": [
        ["return", "id", ";"],
    ],
    "function_body_weave": [
        ["func_content_weave"],
    ],
    "func_content_weave": [
        ["using", "id", "using_cont", ";", "func_content_weave"],
        ["local", "mutability", "local_dec_body", "func_content_weave"],
        ["statement_weave_no_ret", "func_content_weave"],
        ["mandatory_weave_return"],
    ],
    "mandatory_weave_return": [
        ["return", "id", ";"],
    ],
    "function_body_void": [
        ["func_content_void"],
    ],
    "func_content_void": [
        ["using", "id", "using_cont", ";", "func_content_void"],
        ["local", "mutability", "local_dec_body", "func_content_void"],
        ["statement_void_no_ret", "func_content_void"],
        ["mandatory_void_return"],
    ],
    "mandatory_void_return": [
        ["return", ";"],
    ],
    "statement_int": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_int"],
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "statement_long": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_long"],
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "statement_float": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_float"],
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "statement_double": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_double"],
        ["return", "typed_numeric_ret_expr", ";"],
    ],
    "statement_char": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_char"],
        ["return", "typed_string_ret_expr", ";"],
    ],
    "statement_string": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_string"],
        ["return", "typed_string_ret_expr", ";"],
    ],
    "statement_bool": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_bool"],
        ["return", "typed_bool_ret_expr", ";"],
    ],
    "statement_array": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_array"],
        ["return", "id", ";"],
    ],
    "statement_weave": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_weave"],
        ["return", "id", ";"],
    ],
    "statement_void": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_void"],
        ["return", ";"],
    ],
    "statement_int_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_int"],
    ],
    "statement_long_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_long"],
    ],
    "statement_float_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_float"],
    ],
    "statement_double_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_double"],
    ],
    "statement_char_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_char"],
    ],
    "statement_string_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_string"],
    ],
    "statement_bool_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_bool"],
    ],
    "statement_array_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_array"],
    ],
    "statement_weave_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_weave"],
    ],
    "statement_void_no_ret": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct_void"],
    ],
    "ctrl_struct_int": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_int", "}", "else_opt_int"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_int", "default_opt_int", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_int", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_int", "}"],
        ["do", "{", "non_empty_loop_stmt_list_int", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_int": [
        ["statement_int", "stmt_list_int"],
        [EPSILON],
    ],
    "non_empty_stmt_list_int": [
        ["statement_int", "stmt_list_int"],
    ],
    "loop_statement_int": [
        ["statement_int"],
        ["break", ";"],
    ],
    "loop_stmt_list_int": [
        ["loop_statement_int", "loop_stmt_list_int"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_int": [
        ["loop_statement_int", "loop_stmt_list_int"],
    ],
    "else_opt_int": [
        ["else", "else_body_int"],
        [EPSILON],
    ],
    "else_body_int": [
        ["{", "non_empty_stmt_list_int", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_int", "}", "else_opt_int"],
    ],
    "case_list_int": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_int", "break_opt", "case_list_int"],
        [EPSILON],
    ],
    "default_opt_int": [
        ["default", ":", "non_empty_loop_stmt_list_int", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_long": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_long", "}", "else_opt_long"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_long", "default_opt_long", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_long", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_long", "}"],
        ["do", "{", "non_empty_loop_stmt_list_long", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_long": [
        ["statement_long", "stmt_list_long"],
        [EPSILON],
    ],
    "non_empty_stmt_list_long": [
        ["statement_long", "stmt_list_long"],
    ],
    "loop_statement_long": [
        ["statement_long"],
        ["break", ";"],
    ],
    "loop_stmt_list_long": [
        ["loop_statement_long", "loop_stmt_list_long"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_long": [
        ["loop_statement_long", "loop_stmt_list_long"],
    ],
    "else_opt_long": [
        ["else", "else_body_long"],
        [EPSILON],
    ],
    "else_body_long": [
        ["{", "non_empty_stmt_list_long", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_long", "}", "else_opt_long"],
    ],
    "case_list_long": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_long", "break_opt", "case_list_long"],
        [EPSILON],
    ],
    "default_opt_long": [
        ["default", ":", "non_empty_loop_stmt_list_long", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_float": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_float", "}", "else_opt_float"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_float", "default_opt_float", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_float", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_float", "}"],
        ["do", "{", "non_empty_loop_stmt_list_float", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_float": [
        ["statement_float", "stmt_list_float"],
        [EPSILON],
    ],
    "non_empty_stmt_list_float": [
        ["statement_float", "stmt_list_float"],
    ],
    "loop_statement_float": [
        ["statement_float"],
        ["break", ";"],
    ],
    "loop_stmt_list_float": [
        ["loop_statement_float", "loop_stmt_list_float"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_float": [
        ["loop_statement_float", "loop_stmt_list_float"],
    ],
    "else_opt_float": [
        ["else", "else_body_float"],
        [EPSILON],
    ],
    "else_body_float": [
        ["{", "non_empty_stmt_list_float", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_float", "}", "else_opt_float"],
    ],
    "case_list_float": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_float", "break_opt", "case_list_float"],
        [EPSILON],
    ],
    "default_opt_float": [
        ["default", ":", "non_empty_loop_stmt_list_float", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_double": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_double", "}", "else_opt_double"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_double", "default_opt_double", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_double", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_double", "}"],
        ["do", "{", "non_empty_loop_stmt_list_double", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_double": [
        ["statement_double", "stmt_list_double"],
        [EPSILON],
    ],
    "non_empty_stmt_list_double": [
        ["statement_double", "stmt_list_double"],
    ],
    "loop_statement_double": [
        ["statement_double"],
        ["break", ";"],
    ],
    "loop_stmt_list_double": [
        ["loop_statement_double", "loop_stmt_list_double"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_double": [
        ["loop_statement_double", "loop_stmt_list_double"],
    ],
    "else_opt_double": [
        ["else", "else_body_double"],
        [EPSILON],
    ],
    "else_body_double": [
        ["{", "non_empty_stmt_list_double", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_double", "}", "else_opt_double"],
    ],
    "case_list_double": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_double", "break_opt", "case_list_double"],
        [EPSILON],
    ],
    "default_opt_double": [
        ["default", ":", "non_empty_loop_stmt_list_double", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_char": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_char", "}", "else_opt_char"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_char", "default_opt_char", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_char", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_char", "}"],
        ["do", "{", "non_empty_loop_stmt_list_char", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_char": [
        ["statement_char", "stmt_list_char"],
        [EPSILON],
    ],
    "non_empty_stmt_list_char": [
        ["statement_char", "stmt_list_char"],
    ],
    "loop_statement_char": [
        ["statement_char"],
        ["break", ";"],
    ],
    "loop_stmt_list_char": [
        ["loop_statement_char", "loop_stmt_list_char"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_char": [
        ["loop_statement_char", "loop_stmt_list_char"],
    ],
    "else_opt_char": [
        ["else", "else_body_char"],
        [EPSILON],
    ],
    "else_body_char": [
        ["{", "non_empty_stmt_list_char", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_char", "}", "else_opt_char"],
    ],
    "case_list_char": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_char", "break_opt", "case_list_char"],
        [EPSILON],
    ],
    "default_opt_char": [
        ["default", ":", "non_empty_loop_stmt_list_char", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_string": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_string", "}", "else_opt_string"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_string", "default_opt_string", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_string", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_string", "}"],
        ["do", "{", "non_empty_loop_stmt_list_string", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_string": [
        ["statement_string", "stmt_list_string"],
        [EPSILON],
    ],
    "non_empty_stmt_list_string": [
        ["statement_string", "stmt_list_string"],
    ],
    "loop_statement_string": [
        ["statement_string"],
        ["break", ";"],
    ],
    "loop_stmt_list_string": [
        ["loop_statement_string", "loop_stmt_list_string"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_string": [
        ["loop_statement_string", "loop_stmt_list_string"],
    ],
    "else_opt_string": [
        ["else", "else_body_string"],
        [EPSILON],
    ],
    "else_body_string": [
        ["{", "non_empty_stmt_list_string", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_string", "}", "else_opt_string"],
    ],
    "case_list_string": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_string", "break_opt", "case_list_string"],
        [EPSILON],
    ],
    "default_opt_string": [
        ["default", ":", "non_empty_loop_stmt_list_string", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_bool": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_bool", "}", "else_opt_bool"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_bool", "default_opt_bool", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_bool", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_bool", "}"],
        ["do", "{", "non_empty_loop_stmt_list_bool", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_bool": [
        ["statement_bool", "stmt_list_bool"],
        [EPSILON],
    ],
    "non_empty_stmt_list_bool": [
        ["statement_bool", "stmt_list_bool"],
    ],
    "loop_statement_bool": [
        ["statement_bool"],
        ["break", ";"],
    ],
    "loop_stmt_list_bool": [
        ["loop_statement_bool", "loop_stmt_list_bool"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_bool": [
        ["loop_statement_bool", "loop_stmt_list_bool"],
    ],
    "else_opt_bool": [
        ["else", "else_body_bool"],
        [EPSILON],
    ],
    "else_body_bool": [
        ["{", "non_empty_stmt_list_bool", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_bool", "}", "else_opt_bool"],
    ],
    "case_list_bool": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_bool", "break_opt", "case_list_bool"],
        [EPSILON],
    ],
    "default_opt_bool": [
        ["default", ":", "non_empty_loop_stmt_list_bool", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_array": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_array", "}", "else_opt_array"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_array", "default_opt_array", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_array", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_array", "}"],
        ["do", "{", "non_empty_loop_stmt_list_array", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_array": [
        ["statement_array", "stmt_list_array"],
        [EPSILON],
    ],
    "non_empty_stmt_list_array": [
        ["statement_array", "stmt_list_array"],
    ],
    "loop_statement_array": [
        ["statement_array"],
        ["break", ";"],
    ],
    "loop_stmt_list_array": [
        ["loop_statement_array", "loop_stmt_list_array"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_array": [
        ["loop_statement_array", "loop_stmt_list_array"],
    ],
    "else_opt_array": [
        ["else", "else_body_array"],
        [EPSILON],
    ],
    "else_body_array": [
        ["{", "non_empty_stmt_list_array", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_array", "}", "else_opt_array"],
    ],
    "case_list_array": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_array", "break_opt", "case_list_array"],
        [EPSILON],
    ],
    "default_opt_array": [
        ["default", ":", "non_empty_loop_stmt_list_array", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_weave": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_weave", "}", "else_opt_weave"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_weave", "default_opt_weave", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_weave", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_weave", "}"],
        ["do", "{", "non_empty_loop_stmt_list_weave", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_weave": [
        ["statement_weave", "stmt_list_weave"],
        [EPSILON],
    ],
    "non_empty_stmt_list_weave": [
        ["statement_weave", "stmt_list_weave"],
    ],
    "loop_statement_weave": [
        ["statement_weave"],
        ["break", ";"],
    ],
    "loop_stmt_list_weave": [
        ["loop_statement_weave", "loop_stmt_list_weave"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_weave": [
        ["loop_statement_weave", "loop_stmt_list_weave"],
    ],
    "else_opt_weave": [
        ["else", "else_body_weave"],
        [EPSILON],
    ],
    "else_body_weave": [
        ["{", "non_empty_stmt_list_weave", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_weave", "}", "else_opt_weave"],
    ],
    "case_list_weave": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_weave", "break_opt", "case_list_weave"],
        [EPSILON],
    ],
    "default_opt_weave": [
        ["default", ":", "non_empty_loop_stmt_list_weave", "break_opt"],
        [EPSILON],
    ],
    "ctrl_struct_void": [
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_void", "}", "else_opt_void"],
        ["switch", "(", "arg_expr", ")", "{", "case_list_void", "default_opt_void", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_stmt_list_void", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_stmt_list_void", "}"],
        ["do", "{", "non_empty_loop_stmt_list_void", "}", "while", "(", "condition", ")", ";"],
    ],
    "stmt_list_void": [
        ["statement_void", "stmt_list_void"],
        [EPSILON],
    ],
    "non_empty_stmt_list_void": [
        ["statement_void", "stmt_list_void"],
    ],
    "loop_statement_void": [
        ["statement_void"],
        ["break", ";"],
    ],
    "loop_stmt_list_void": [
        ["loop_statement_void", "loop_stmt_list_void"],
        [EPSILON],
    ],
    "non_empty_loop_stmt_list_void": [
        ["loop_statement_void", "loop_stmt_list_void"],
    ],
    "else_opt_void": [
        ["else", "else_body_void"],
        [EPSILON],
    ],
    "else_body_void": [
        ["{", "non_empty_stmt_list_void", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_stmt_list_void", "}", "else_opt_void"],
    ],
    "case_list_void": [
        ["case", "case_val", ":", "non_empty_loop_stmt_list_void", "break_opt", "case_list_void"],
        [EPSILON],
    ],
    "default_opt_void": [
        ["default", ":", "non_empty_loop_stmt_list_void", "break_opt"],
        [EPSILON],
    ],
    "typed_numeric_ret_expr": [
        ["typed_numeric_add_expr"],
    ],
    "typed_string_ret_expr": [
        ["typed_string_ret_primary", "typed_string_cont"],
    ],
    "typed_string_ret_primary": [
        ["stringlit"],
        ["charlit"],
        ["id", "typed_postfix_chain"],
        ["string", "(", "expression", ")"],
        ["char", "(", "expression", ")"],
        ["(", "expression", ")", "typed_postfix_chain"],
    ],
    "typed_bool_ret_expr": [
        ["typed_bool_ret_primary", "typed_bool_ret_tail"],
    ],
    "typed_bool_ret_primary": [
        ["true"],
        ["false"],
        ["!", "typed_bool_factor"],
        ["id", "typed_bool_id_cont"],
        ["(", "typed_bool_paren", ")"],
        ["bool", "(", "expression", ")"],
        ["intlit", "typed_numeric_cmp_required"],
        ["longlit", "typed_numeric_cmp_required"],
        ["floatlit", "typed_numeric_cmp_required"],
        ["doublelit", "typed_numeric_cmp_required"],
        ["-", "typed_numeric_neg_cmp"],
        ["int", "(", "expression", ")", "typed_numeric_cmp_required"],
        ["long", "(", "expression", ")", "typed_numeric_cmp_required"],
        ["float", "(", "expression", ")", "typed_numeric_cmp_required"],
        ["double", "(", "expression", ")", "typed_numeric_cmp_required"],
    ],
    "typed_bool_ret_tail": [
        ["&&", "typed_bool_term", "typed_bool_and_tail", "typed_bool_or_tail_opt"],
        ["||", "typed_bool_term", "typed_bool_or_tail"],
        ["==", "typed_bool_factor", "typed_bool_eq_tail", "typed_bool_ret_tail"],
        ["!=", "typed_bool_factor", "typed_bool_eq_tail", "typed_bool_ret_tail"],
        [EPSILON],
    ],
    "using_cont": [
        [",", "id", "using_cont"],
        [EPSILON],
    ],
    "local_dec_body": [
        ["int", "id", "int_local_tail"],
        ["long", "id", "long_local_tail"],
        ["float", "id", "float_local_tail"],
        ["double", "id", "double_local_tail"],
        ["char", "id", "char_local_tail"],
        ["string", "id", "string_local_tail"],
        ["bool", "id", "bool_local_tail"],
        ["id", "id", "weave_local_tail"],
    ],
    "int_local_tail": [
        ["int_array_with_init", ";"],
        ["=", "intlit", "int_local_cont", ";"],
    ],
    "int_local_cont": [
        [",", "id", "=", "intlit", "int_local_cont"],
        [EPSILON],
    ],
    "long_local_tail": [
        ["long_array_with_init", ";"],
        ["=", "longlit", "long_local_cont", ";"],
    ],
    "long_local_cont": [
        [",", "id", "=", "longlit", "long_local_cont"],
        [EPSILON],
    ],
    "float_local_tail": [
        ["float_array_with_init", ";"],
        ["=", "floatlit", "float_local_cont", ";"],
    ],
    "float_local_cont": [
        [",", "id", "=", "floatlit", "float_local_cont"],
        [EPSILON],
    ],
    "double_local_tail": [
        ["double_array_with_init", ";"],
        ["=", "doublelit", "double_local_cont", ";"],
    ],
    "double_local_cont": [
        [",", "id", "=", "doublelit", "double_local_cont"],
        [EPSILON],
    ],
    "char_local_tail": [
        ["char_array_with_init", ";"],
        ["=", "charlit", "char_local_cont", ";"],
    ],
    "char_local_cont": [
        [",", "id", "=", "charlit", "char_local_cont"],
        [EPSILON],
    ],
    "string_local_tail": [
        ["string_array_with_init", ";"],
        ["=", "stringlit", "string_local_cont", ";"],
    ],
    "string_local_cont": [
        [",", "id", "=", "stringlit", "string_local_cont"],
        [EPSILON],
    ],
    "bool_local_tail": [
        ["bool_array_with_init", ";"],
        ["=", "bool_lit", "bool_local_cont", ";"],
    ],
    "bool_local_cont": [
        [",", "id", "=", "bool_lit", "bool_local_cont"],
        [EPSILON],
    ],
    "weave_local_tail": [
        ["=", "{", "weave_field_value", "weave_field_list_tail", "}", "weave_inst_cont", ";"],
        ["weave_array_with_init", "weave_arr_cont", ";"],
    ],
    "statement_non_return": [
        ["effect_stmt", ";"],
        ["io_stmt"],
        ["ctrl_struct"],
    ],
    "expression": [
        ["typed_assign_expr"],
    ],
    "typed_assign_expr": [
        ["typed_concat_expr", "typed_assign_tail"],
    ],
    "typed_assign_tail": [
        ["=", "typed_rhs_expr"],
        ["+=", "typed_numeric_add_expr"],
        ["-=", "typed_numeric_add_expr"],
        ["*=", "typed_numeric_add_expr"],
        ["/=", "typed_numeric_add_expr"],
        ["%=", "typed_numeric_add_expr"],
        [EPSILON],
    ],
    "assign_op": [
        ["="],
        ["+="],
        ["-="],
        ["*="],
        ["/="],
        ["%="],
    ],
    "typed_rhs_expr": [
        ["typed_concat_expr"],
    ],
    "typed_concat_expr": [
        ["stringlit", "typed_string_cont"],
        ["charlit", "typed_string_cont"],
        ["intlit", "typed_numeric_cont"],
        ["longlit", "typed_numeric_cont"],
        ["floatlit", "typed_numeric_cont"],
        ["doublelit", "typed_numeric_cont"],
        ["true", "typed_bool_cont"],
        ["false", "typed_bool_cont"],
        ["!", "typed_bool_factor", "typed_bool_tail_opt"],
        ["-", "typed_neg_numeric_cont"],
        ["id", "typed_id_cont"],
        ["(", "typed_paren_cont"],
        ["int", "(", "expression", ")", "typed_numeric_cont"],
        ["long", "(", "expression", ")", "typed_numeric_cont"],
        ["float", "(", "expression", ")", "typed_numeric_cont"],
        ["double", "(", "expression", ")", "typed_numeric_cont"],
        ["char", "(", "expression", ")", "typed_string_cont"],
        ["string", "(", "expression", ")", "typed_string_cont"],
        ["bool", "(", "expression", ")", "typed_bool_cont"],
    ],
    "typed_string_cont": [
        ["..", "typed_string_operand", "typed_string_cont"],
        [EPSILON],
    ],
    "typed_string_operand": [
        ["stringlit"],
        ["charlit"],
        ["id", "str_operand_id_tail"],
        ["string", "(", "expression", ")"],
        ["char", "(", "expression", ")"],
        ["(", "typed_string_operand", "typed_string_cont", ")"],
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["true"],
        ["false"],
        ["int", "(", "expression", ")"],
        ["long", "(", "expression", ")"],
        ["float", "(", "expression", ")"],
        ["double", "(", "expression", ")"],
        ["bool", "(", "expression", ")"],
    ],
    "str_operand_id_tail": [
        [".", "id", "str_operand_id_tail"],
        ["[", "array_index", "]", "str_operand_arr_tail"],
        ["(", "arg_list", ")", "str_operand_id_tail"],
        [EPSILON],
    ],
    "str_operand_arr_tail": [
        [".", "id", "str_operand_id_tail"],
        ["[", "array_index", "]", "str_operand_arr_tail"],
        [EPSILON],
    ],
    "typed_numeric_cont": [
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        ["typed_bool_tail_opt"],
    ],
    "typed_arith_ops": [
        ["+", "typed_numeric_mul_expr", "typed_numeric_add_ops"],
        ["-", "typed_numeric_mul_expr", "typed_numeric_add_ops"],
        ["*", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_ops"],
        ["/", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_ops"],
        ["%", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_ops"],
    ],
    "typed_numeric_add_ops": [
        ["+", "typed_numeric_mul_expr", "typed_numeric_add_ops"],
        ["-", "typed_numeric_mul_expr", "typed_numeric_add_ops"],
        [EPSILON],
    ],
    "typed_after_arith": [
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        ["typed_bool_tail_opt"],
    ],
    "typed_neg_numeric_cont": [
        ["typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_ops", "typed_after_arith"],
    ],
    "typed_bool_cont": [
        ["typed_bool_tail_opt"],
    ],
    "typed_bool_tail_opt": [
        ["&&", "typed_bool_term", "typed_bool_and_tail", "typed_bool_or_tail_opt"],
        ["||", "typed_bool_term", "typed_bool_or_tail"],
        [EPSILON],
    ],
    "typed_bool_or_tail_opt": [
        ["||", "typed_bool_term", "typed_bool_or_tail"],
        [EPSILON],
    ],
    "typed_bool_term": [
        ["typed_bool_eq", "typed_bool_and_tail"],
    ],
    "typed_bool_and_tail": [
        ["&&", "typed_bool_eq", "typed_bool_and_tail"],
        [EPSILON],
    ],
    "typed_bool_or_tail": [
        ["||", "typed_bool_term", "typed_bool_or_tail"],
        [EPSILON],
    ],
    "typed_bool_eq": [
        ["typed_bool_factor", "typed_bool_eq_tail"],
    ],
    "typed_bool_eq_tail": [
        ["==", "typed_bool_factor", "typed_bool_eq_tail"],
        ["!=", "typed_bool_factor", "typed_bool_eq_tail"],
        [EPSILON],
    ],
    "typed_bool_factor": [
        ["!", "typed_bool_factor"],
        ["typed_bool_atom"],
    ],
    "typed_bool_atom": [
        ["true"],
        ["false"],
        ["id", "typed_bool_id_cont"],
        ["intlit", "typed_numeric_cmp_required"],
        ["longlit", "typed_numeric_cmp_required"],
        ["floatlit", "typed_numeric_cmp_required"],
        ["doublelit", "typed_numeric_cmp_required"],
        ["-", "typed_numeric_neg_cmp"],
        ["(", "typed_bool_paren", ")"],
        ["int", "(", "expression", ")", "typed_numeric_cmp_required"],
        ["long", "(", "expression", ")", "typed_numeric_cmp_required"],
        ["float", "(", "expression", ")", "typed_numeric_cmp_required"],
        ["double", "(", "expression", ")", "typed_numeric_cmp_required"],
    ],
    "typed_bool_paren": [
        ["typed_bool_term", "typed_bool_and_or_tail"],
    ],
    "typed_bool_and_or_tail": [
        ["&&", "typed_bool_term", "typed_bool_and_or_tail"],
        ["||", "typed_bool_term", "typed_bool_and_or_tail"],
        [EPSILON],
    ],
    "typed_bool_id_cont": [
        ["typed_numeric_arith_cmp"],
        ["typed_postfix_chain"],
    ],
    "typed_numeric_arith_cmp": [
        ["+", "typed_numeric_mul_expr", "typed_numeric_add_cmp", "typed_cmp_op", "typed_numeric_add_expr"],
        ["-", "typed_numeric_mul_expr", "typed_numeric_add_cmp", "typed_cmp_op", "typed_numeric_add_expr"],
        ["*", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_cmp", "typed_cmp_op", "typed_numeric_add_expr"],
        ["/", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_cmp", "typed_cmp_op", "typed_numeric_add_expr"],
        ["%", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_cmp", "typed_cmp_op", "typed_numeric_add_expr"],
        ["typed_cmp_op", "typed_numeric_add_expr"],
    ],
    "typed_numeric_add_cmp": [
        ["+", "typed_numeric_mul_expr", "typed_numeric_add_cmp"],
        ["-", "typed_numeric_mul_expr", "typed_numeric_add_cmp"],
        [EPSILON],
    ],
    "typed_numeric_cmp_required": [
        ["typed_numeric_lit_arith", "typed_cmp_op", "typed_numeric_add_expr"],
    ],
    "typed_numeric_lit_arith": [
        ["*", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_cmp"],
        ["/", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_cmp"],
        ["%", "typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_cmp"],
        ["+", "typed_numeric_mul_expr", "typed_numeric_add_cmp"],
        ["-", "typed_numeric_mul_expr", "typed_numeric_add_cmp"],
        [EPSILON],
    ],
    "typed_numeric_neg_cmp": [
        ["typed_numeric_unary_expr", "typed_numeric_mul_tail", "typed_numeric_add_cmp", "typed_cmp_op", "typed_numeric_add_expr"],
    ],
    "typed_id_cont": [
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        ["++"],
        ["--"],
        ["[", "array_index", "]", "typed_id_arr_cont"],
        [".", "id", "typed_id_field_cont"],
        ["(", "arg_list", ")", "typed_id_call_cont"],
        ["..", "typed_string_operand", "typed_string_cont"],
        ["typed_bool_tail_opt"],
    ],
    "typed_id_arr_cont": [
        ["[", "array_index", "]", "typed_id_arr2_cont"],
        ["typed_id_postfix_cont"],
    ],
    "typed_id_arr2_cont": [
        ["typed_id_postfix_cont"],
    ],
    "typed_id_postfix_cont": [
        [".", "id", "typed_id_field_cont"],
        ["(", "arg_list", ")", "typed_id_call_cont"],
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        ["..", "typed_string_operand", "typed_string_cont"],
        ["typed_bool_tail_opt"],
    ],
    "typed_id_field_cont": [
        ["[", "array_index", "]", "typed_id_arr_cont"],
        [".", "id", "typed_id_field_cont"],
        ["(", "arg_list", ")", "typed_id_call_cont"],
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        ["..", "typed_string_operand", "typed_string_cont"],
        ["typed_bool_tail_opt"],
    ],
    "typed_id_call_cont": [
        ["[", "array_index", "]", "typed_id_arr_cont"],
        [".", "id", "typed_id_field_cont"],
        ["(", "arg_list", ")", "typed_id_call_cont"],
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        ["..", "typed_string_operand", "typed_string_cont"],
        ["typed_bool_tail_opt"],
    ],
    "typed_paren_cont": [
        ["typed_concat_expr", ")", "typed_paren_after"],
    ],
    "typed_paren_after": [
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        ["..", "typed_string_operand", "typed_string_cont"],
        ["[", "array_index", "]", "typed_paren_arr_cont"],
        [".", "id", "typed_paren_field_cont"],
        ["(", "arg_list", ")", "typed_paren_call_cont"],
        ["typed_bool_tail_opt"],
    ],
    "typed_paren_arr_cont": [
        ["[", "array_index", "]", "typed_paren_arr2_cont"],
        ["typed_paren_postfix_cont"],
    ],
    "typed_paren_arr2_cont": [
        ["typed_paren_postfix_cont"],
    ],
    "typed_paren_postfix_cont": [
        [".", "id", "typed_paren_field_cont"],
        ["(", "arg_list", ")", "typed_paren_call_cont"],
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        [EPSILON],
    ],
    "typed_paren_field_cont": [
        ["[", "array_index", "]", "typed_paren_arr_cont"],
        [".", "id", "typed_paren_field_cont"],
        ["(", "arg_list", ")", "typed_paren_call_cont"],
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        [EPSILON],
    ],
    "typed_paren_call_cont": [
        ["[", "array_index", "]", "typed_paren_arr_cont"],
        [".", "id", "typed_paren_field_cont"],
        ["(", "arg_list", ")", "typed_paren_call_cont"],
        ["typed_arith_ops", "typed_after_arith"],
        ["typed_cmp_op", "typed_numeric_add_expr", "typed_bool_tail_opt"],
        [EPSILON],
    ],
    "typed_numeric_add_expr": [
        ["typed_numeric_mul_expr", "typed_numeric_add_tail"],
    ],
    "typed_numeric_add_tail": [
        ["+", "typed_numeric_mul_expr", "typed_numeric_add_tail"],
        ["-", "typed_numeric_mul_expr", "typed_numeric_add_tail"],
        [EPSILON],
    ],
    "typed_numeric_mul_expr": [
        ["typed_numeric_unary_expr", "typed_numeric_mul_tail"],
    ],
    "typed_numeric_mul_tail": [
        ["*", "typed_numeric_unary_expr", "typed_numeric_mul_tail"],
        ["/", "typed_numeric_unary_expr", "typed_numeric_mul_tail"],
        ["%", "typed_numeric_unary_expr", "typed_numeric_mul_tail"],
        [EPSILON],
    ],
    "typed_numeric_unary_expr": [
        ["!", "typed_numeric_unary_expr"],
        ["-", "typed_numeric_unary_expr"],
        ["++", "typed_numeric_unary_expr"],
        ["--", "typed_numeric_unary_expr"],
        ["typed_numeric_postfix_expr"],
    ],
    "typed_numeric_postfix_expr": [
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["id", "typed_postfix_chain"],
        ["(", "expression", ")", "typed_postfix_chain"],
        ["int", "(", "expression", ")"],
        ["long", "(", "expression", ")"],
        ["float", "(", "expression", ")"],
        ["double", "(", "expression", ")"],
    ],
    "typed_cmp_op": [
        ["<"],
        [">"],
        ["<="],
        [">="],
        ["=="],
        ["!="],
    ],
    "typed_postfix_chain": [
        ["[", "array_index", "]", "typed_postfix_after_arr"],
        [".", "id", "typed_postfix_chain"],
        ["(", "arg_list", ")", "typed_postfix_chain"],
        ["++"],
        ["--"],
        [EPSILON],
    ],
    "typed_postfix_after_arr": [
        ["[", "array_index", "]", "typed_postfix_after_arr"],
        [".", "id", "typed_postfix_chain"],
        ["(", "arg_list", ")", "typed_postfix_chain"],
        ["++"],
        ["--"],
        [EPSILON],
    ],
    "array_index": [
        ["intlit"],
        ["id"],
    ],
    "arg_list": [
        ["arg_expr", "arg_tail"],
        [EPSILON],
    ],
    "arg_tail": [
        [",", "arg_expr", "arg_tail"],
        [EPSILON],
    ],
    "effect_stmt": [
        ["++", "id", "effect_pre_chain"],
        ["--", "id", "effect_pre_chain"],
        ["id", "effect_id_cont"],
    ],
    "effect_pre_chain": [
        ["[", "stmt_array_index", "]", "effect_pre_arr_chain"],
        [".", "id", "effect_pre_chain"],
        [EPSILON],
    ],
    "effect_pre_arr_chain": [
        ["[", "stmt_array_index", "]"],
        [".", "id", "effect_pre_chain"],
        [EPSILON],
    ],
    "effect_id_cont": [
        ["=", "stmt_assign_expr"],
        ["+=", "numeric_add_expr_stmt"],
        ["-=", "numeric_add_expr_stmt"],
        ["*=", "numeric_add_expr_stmt"],
        ["/=", "numeric_add_expr_stmt"],
        ["%=", "numeric_add_expr_stmt"],
        ["++"],
        ["--"],
        ["(", "stmt_arg_list", ")", "effect_post_call"],
        ["[", "stmt_array_index", "]", "effect_post_arr"],
        [".", "id", "effect_post_member"],
    ],
    "effect_post_call": [
        [".", "id", "effect_post_call_member"],
        ["[", "stmt_array_index", "]", "effect_post_call_arr"],
        [EPSILON],
    ],
    "effect_post_call_member": [
        ["(", "stmt_arg_list", ")", "effect_post_call"],
        ["[", "stmt_array_index", "]", "effect_post_call_arr"],
        [".", "id", "effect_post_call_member"],
        [EPSILON],
    ],
    "effect_post_call_arr": [
        ["[", "stmt_array_index", "]", "effect_post_call_arr_cont"],
        ["effect_post_call_arr_cont"],
    ],
    "effect_post_call_arr_cont": [
        [".", "id", "effect_post_call_member"],
        ["(", "stmt_arg_list", ")", "effect_post_call"],
        [EPSILON],
    ],
    "effect_post_arr": [
        ["[", "stmt_array_index", "]", "effect_post_arr_2d"],
        ["effect_arr_effect"],
    ],
    "effect_post_arr_2d": [
        ["effect_arr_effect"],
    ],
    "effect_arr_effect": [
        ["=", "stmt_assign_expr"],
        ["+=", "numeric_add_expr_stmt"],
        ["-=", "numeric_add_expr_stmt"],
        ["*=", "numeric_add_expr_stmt"],
        ["/=", "numeric_add_expr_stmt"],
        ["%=", "numeric_add_expr_stmt"],
        ["++"],
        ["--"],
        ["(", "stmt_arg_list", ")", "effect_post_call"],
        [".", "id", "effect_post_member"],
    ],
    "effect_post_member": [
        ["=", "stmt_assign_expr"],
        ["+=", "numeric_add_expr_stmt"],
        ["-=", "numeric_add_expr_stmt"],
        ["*=", "numeric_add_expr_stmt"],
        ["/=", "numeric_add_expr_stmt"],
        ["%=", "numeric_add_expr_stmt"],
        ["++"],
        ["--"],
        ["(", "stmt_arg_list", ")", "effect_post_call"],
        ["[", "stmt_array_index", "]", "effect_post_arr"],
        [".", "id", "effect_post_member"],
    ],
    "stmt_assign_expr": [
        ["stmt_typed_rhs"],
    ],
    "stmt_typed_rhs": [
        ["stmt_bool_or_concat"],
    ],
    "stmt_bool_or_concat": [
        ["stringlit", "stmt_concat_tail_typed"],
        ["charlit", "stmt_concat_tail_typed"],
        ["string", "(", "arg_expr", ")", "stmt_concat_tail_typed"],
        ["intlit", "stmt_numeric_or_bool"],
        ["longlit", "stmt_numeric_or_bool"],
        ["floatlit", "stmt_numeric_or_bool"],
        ["doublelit", "stmt_numeric_or_bool"],
        ["-", "stmt_neg_numeric_or_bool"],
        ["true", "stmt_bool_tail_opt"],
        ["false", "stmt_bool_tail_opt"],
        ["!", "stmt_bool_factor", "stmt_bool_tail_opt"],
        ["int", "(", "arg_expr", ")", "stmt_numeric_or_bool"],
        ["long", "(", "arg_expr", ")", "stmt_numeric_or_bool"],
        ["float", "(", "arg_expr", ")", "stmt_numeric_or_bool"],
        ["double", "(", "arg_expr", ")", "stmt_numeric_or_bool"],
        ["char", "(", "arg_expr", ")"],
        ["bool", "(", "arg_expr", ")", "stmt_bool_tail_opt"],
        ["id", "stmt_id_toplevel_cont"],
        ["(", "stmt_paren_typed_content"],
        ["++", "id", "stmt_postfix_chain", "stmt_id_after_postfix"],
        ["--", "id", "stmt_postfix_chain", "stmt_id_after_postfix"],
    ],
    "stmt_numeric_or_bool": [
        ["stmt_arith_ops", "stmt_after_arith"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_bool_tail_opt"],
        ["stmt_bool_tail_opt"],
    ],
    "stmt_arith_ops": [
        ["+", "numeric_mul_expr_stmt", "stmt_numeric_add_ops"],
        ["-", "numeric_mul_expr_stmt", "stmt_numeric_add_ops"],
        ["*", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops"],
        ["/", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops"],
        ["%", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops"],
    ],
    "stmt_numeric_add_ops": [
        ["+", "numeric_mul_expr_stmt", "stmt_numeric_add_ops"],
        ["-", "numeric_mul_expr_stmt", "stmt_numeric_add_ops"],
        [EPSILON],
    ],
    "stmt_after_arith": [
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_bool_tail_opt"],
        ["stmt_bool_tail_opt"],
    ],
    "stmt_neg_numeric_or_bool": [
        ["numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops", "stmt_after_arith"],
    ],
    "stmt_bool_tail_opt": [
        ["&&", "stmt_bool_term", "stmt_bool_and_tail", "stmt_bool_or_tail_opt"],
        ["||", "stmt_bool_term", "stmt_bool_or_tail"],
        [EPSILON],
    ],
    "stmt_bool_or_tail_opt": [
        ["||", "stmt_bool_term", "stmt_bool_or_tail"],
        [EPSILON],
    ],
    "stmt_id_toplevel_cont": [
        ["stmt_arith_ops", "stmt_after_arith"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_bool_tail_opt"],
        ["++", "stmt_id_after_postfix"],
        ["--", "stmt_id_after_postfix"],
        ["stmt_postfix_chain", "stmt_id_after_postfix"],
    ],
    "stmt_id_after_postfix": [
        ["stmt_arith_ops", "stmt_after_arith"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_bool_tail_opt"],
        ["..", "stmt_string_operand", "stmt_concat_tail_typed"],
        ["++"],
        ["--"],
        ["stmt_bool_tail_opt"],
    ],
    "stmt_paren_typed_content": [
        ["stringlit", "stmt_concat_tail_typed", ")", "stmt_paren_string_cont"],
        ["charlit", "stmt_concat_tail_typed", ")", "stmt_paren_string_cont"],
        ["string", "(", "arg_expr", ")", "stmt_concat_tail_typed", ")", "stmt_paren_string_cont"],
        ["char", "(", "arg_expr", ")", ")", "stmt_paren_string_cont"],
        ["intlit", "stmt_paren_num_start"],
        ["longlit", "stmt_paren_num_start"],
        ["floatlit", "stmt_paren_num_start"],
        ["doublelit", "stmt_paren_num_start"],
        ["-", "stmt_paren_neg_num"],
        ["int", "(", "arg_expr", ")", "stmt_paren_num_start"],
        ["long", "(", "arg_expr", ")", "stmt_paren_num_start"],
        ["float", "(", "arg_expr", ")", "stmt_paren_num_start"],
        ["double", "(", "arg_expr", ")", "stmt_paren_num_start"],
        ["true", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        ["false", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        ["!", "stmt_bool_factor", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        ["bool", "(", "arg_expr", ")", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        ["id", "stmt_paren_id_cont"],
        ["(", "stmt_paren_typed_content", ")", "stmt_paren_any_cont"],
        ["++", "id", "stmt_paren_num_after_incr"],
        ["--", "id", "stmt_paren_num_after_incr"],
    ],
    "stmt_paren_string_cont": [
        ["..", "stmt_string_operand", "stmt_concat_tail_typed"],
        [EPSILON],
    ],
    "stmt_paren_num_start": [
        ["stmt_paren_arith_ops"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        [")", "stmt_paren_num_cont"],
    ],
    "stmt_paren_arith_ops": [
        ["+", "numeric_mul_expr_stmt", "stmt_numeric_add_ops", "stmt_paren_after_arith"],
        ["-", "numeric_mul_expr_stmt", "stmt_numeric_add_ops", "stmt_paren_after_arith"],
        ["*", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops", "stmt_paren_after_arith"],
        ["/", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops", "stmt_paren_after_arith"],
        ["%", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops", "stmt_paren_after_arith"],
    ],
    "stmt_paren_after_arith": [
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        [")", "stmt_paren_num_cont"],
    ],
    "stmt_paren_neg_num": [
        ["numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_ops", "stmt_paren_after_arith"],
    ],
    "stmt_paren_num_after_incr": [
        ["stmt_paren_arith_ops"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        [")", "stmt_paren_num_cont"],
    ],
    "stmt_paren_num_cont": [
        ["stmt_arith_ops", "stmt_after_arith"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_bool_tail_opt"],
        ["stmt_bool_tail_opt"],
    ],
    "stmt_paren_bool_tail": [
        ["&&", "stmt_bool_term", "stmt_bool_and_tail", "stmt_bool_or_tail_opt"],
        ["||", "stmt_bool_term", "stmt_bool_or_tail"],
        [EPSILON],
    ],
    "stmt_paren_bool_cont": [
        ["&&", "stmt_bool_term", "stmt_bool_and_tail", "stmt_bool_or_tail_opt"],
        ["||", "stmt_bool_term", "stmt_bool_or_tail"],
        [EPSILON],
    ],
    "stmt_paren_id_cont": [
        ["stmt_paren_arith_ops"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        ["stmt_paren_postfix_nonnull", "stmt_paren_id_after_postfix"],
        ["++", "stmt_paren_id_after_postfix"],
        ["--", "stmt_paren_id_after_postfix"],
        ["&&", "stmt_bool_term", "stmt_bool_and_tail", "stmt_bool_or_tail_opt", ")", "stmt_paren_any_cont"],
        ["||", "stmt_bool_term", "stmt_bool_or_tail", ")", "stmt_paren_any_cont"],
        [")", "stmt_paren_any_cont"],
    ],
    "stmt_paren_postfix_nonnull": [
        ["[", "array_index", "]", "stmt_postfix_after_arr"],
        [".", "id", "stmt_postfix_chain"],
        ["(", "arg_list", ")", "stmt_postfix_chain"],
    ],
    "stmt_paren_id_after_postfix": [
        ["stmt_paren_arith_ops"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_paren_bool_tail", ")", "stmt_paren_bool_cont"],
        ["..", "stmt_string_operand", "stmt_concat_tail_typed", ")", "stmt_paren_string_cont"],
        ["&&", "stmt_bool_term", "stmt_bool_and_tail", "stmt_bool_or_tail_opt", ")", "stmt_paren_any_cont"],
        ["||", "stmt_bool_term", "stmt_bool_or_tail", ")", "stmt_paren_any_cont"],
        [")", "stmt_paren_any_cont"],
    ],
    "stmt_paren_any_cont": [
        ["stmt_arith_ops", "stmt_after_arith"],
        ["stmt_cmp_op", "numeric_add_expr_stmt", "stmt_bool_tail_opt"],
        ["..", "stmt_string_operand", "stmt_concat_tail_typed"],
        ["stmt_bool_tail_opt"],
    ],
    "stmt_concat_tail_typed": [
        ["..", "stmt_string_operand", "stmt_concat_tail_typed"],
        [EPSILON],
    ],
    "stmt_string_operand": [
        ["stringlit"],
        ["charlit"],
        ["id", "str_operand_id_tail"],
        ["string", "(", "arg_expr", ")"],
        ["char", "(", "arg_expr", ")"],
        ["(", "stmt_string_operand", "stmt_concat_tail_typed", ")"],
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["true"],
        ["false"],
        ["int", "(", "arg_expr", ")"],
        ["long", "(", "arg_expr", ")"],
        ["float", "(", "arg_expr", ")"],
        ["double", "(", "arg_expr", ")"],
        ["bool", "(", "arg_expr", ")"],
    ],
    "stmt_bool_term": [
        ["stmt_bool_eq", "stmt_bool_and_tail"],
    ],
    "stmt_bool_and_tail": [
        ["&&", "stmt_bool_eq", "stmt_bool_and_tail"],
        [EPSILON],
    ],
    "stmt_bool_or_tail": [
        ["||", "stmt_bool_term", "stmt_bool_or_tail"],
        [EPSILON],
    ],
    "stmt_bool_eq": [
        ["stmt_bool_factor", "stmt_bool_eq_tail"],
    ],
    "stmt_bool_eq_tail": [
        ["==", "stmt_bool_factor", "stmt_bool_eq_tail"],
        ["!=", "stmt_bool_factor", "stmt_bool_eq_tail"],
        [EPSILON],
    ],
    "stmt_bool_factor": [
        ["!", "stmt_bool_factor"],
        ["stmt_bool_atom"],
    ],
    "stmt_bool_atom": [
        ["true"],
        ["false"],
        ["id", "stmt_bool_id_cont"],
        ["intlit", "stmt_numeric_cmp_required"],
        ["longlit", "stmt_numeric_cmp_required"],
        ["floatlit", "stmt_numeric_cmp_required"],
        ["doublelit", "stmt_numeric_cmp_required"],
        ["-", "stmt_numeric_neg_cmp"],
        ["(", "stmt_bool_paren", ")"],
        ["int", "(", "arg_expr", ")", "stmt_numeric_cmp_required"],
        ["long", "(", "arg_expr", ")", "stmt_numeric_cmp_required"],
        ["float", "(", "arg_expr", ")", "stmt_numeric_cmp_required"],
        ["double", "(", "arg_expr", ")", "stmt_numeric_cmp_required"],
    ],
    "stmt_bool_id_cont": [
        ["stmt_numeric_arith_cmp"],
        ["++"],
        ["--"],
        ["stmt_postfix_chain"],
    ],
    "stmt_numeric_arith_cmp": [
        ["+", "numeric_mul_expr_stmt", "stmt_numeric_add_cmp", "stmt_cmp_op", "numeric_add_expr_stmt"],
        ["-", "numeric_mul_expr_stmt", "stmt_numeric_add_cmp", "stmt_cmp_op", "numeric_add_expr_stmt"],
        ["*", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_cmp", "stmt_cmp_op", "numeric_add_expr_stmt"],
        ["/", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_cmp", "stmt_cmp_op", "numeric_add_expr_stmt"],
        ["%", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_cmp", "stmt_cmp_op", "numeric_add_expr_stmt"],
        ["stmt_cmp_op", "numeric_add_expr_stmt"],
    ],
    "stmt_numeric_add_cmp": [
        ["+", "numeric_mul_expr_stmt", "stmt_numeric_add_cmp"],
        ["-", "numeric_mul_expr_stmt", "stmt_numeric_add_cmp"],
        [EPSILON],
    ],
    "stmt_numeric_cmp_required": [
        ["stmt_numeric_lit_arith", "stmt_cmp_op", "numeric_add_expr_stmt"],
    ],
    "stmt_numeric_lit_arith": [
        ["*", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_cmp"],
        ["/", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_cmp"],
        ["%", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_cmp"],
        ["+", "numeric_mul_expr_stmt", "stmt_numeric_add_cmp"],
        ["-", "numeric_mul_expr_stmt", "stmt_numeric_add_cmp"],
        [EPSILON],
    ],
    "stmt_numeric_neg_cmp": [
        ["numeric_unary_expr_stmt", "numeric_mul_tail_stmt", "stmt_numeric_add_cmp", "stmt_cmp_op", "numeric_add_expr_stmt"],
    ],
    "stmt_cmp_op": [
        ["<"],
        [">"],
        ["<="],
        [">="],
        ["=="],
        ["!="],
    ],
    "stmt_bool_paren": [
        ["stmt_bool_term", "stmt_bool_and_or_tail"],
    ],
    "stmt_bool_and_or_tail": [
        ["&&", "stmt_bool_term", "stmt_bool_and_or_tail"],
        ["||", "stmt_bool_term", "stmt_bool_and_or_tail"],
        [EPSILON],
    ],
    "numeric_mul_expr_stmt": [
        ["numeric_unary_expr_stmt", "numeric_mul_tail_stmt"],
    ],
    "numeric_mul_tail_stmt": [
        ["*", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt"],
        ["/", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt"],
        ["%", "numeric_unary_expr_stmt", "numeric_mul_tail_stmt"],
        [EPSILON],
    ],
    "numeric_add_expr_stmt": [
        ["numeric_mul_expr_stmt", "numeric_add_tail_stmt"],
    ],
    "numeric_add_tail_stmt": [
        ["+", "numeric_mul_expr_stmt", "numeric_add_tail_stmt"],
        ["-", "numeric_mul_expr_stmt", "numeric_add_tail_stmt"],
        [EPSILON],
    ],
    "numeric_unary_expr_stmt": [
        ["!", "numeric_unary_expr_stmt"],
        ["-", "numeric_unary_expr_stmt"],
        ["numeric_postfix_expr_stmt"],
    ],
    "numeric_postfix_expr_stmt": [
        ["(", "arg_expr", ")", "stmt_postfix_chain"],
        ["int", "(", "arg_expr", ")"],
        ["long", "(", "arg_expr", ")"],
        ["float", "(", "arg_expr", ")"],
        ["double", "(", "arg_expr", ")"],
        ["++", "id", "stmt_postfix_chain"],
        ["--", "id", "stmt_postfix_chain"],
        ["id", "stmt_id_postfix"],
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
    ],
    "stmt_id_postfix": [
        ["++"],
        ["--"],
        ["stmt_postfix_chain"],
    ],
    "stmt_postfix_chain": [
        ["stmt_array_access", "stmt_postfix_after_arr"],
        [".", "id", "stmt_postfix_chain"],
        ["(", "stmt_arg_list", ")", "stmt_postfix_chain"],
        [EPSILON],
    ],
    "stmt_array_access": [
        ["[", "stmt_array_index", "]", "stmt_array_access_dim2"],
    ],
    "stmt_array_access_dim2": [
        ["[", "stmt_array_index", "]"],
        [EPSILON],
    ],
    "stmt_postfix_after_arr": [
        [".", "id", "stmt_postfix_chain"],
        ["(", "stmt_arg_list", ")", "stmt_postfix_chain"],
        ["++"],
        ["--"],
        [EPSILON],
    ],
    "stmt_array_index": [
        ["intlit"],
        ["id"],
    ],
    "stmt_arg_list": [
        ["arg_expr", "stmt_arg_tail"],
        [EPSILON],
    ],
    "stmt_arg_tail": [
        [",", "arg_expr", "stmt_arg_tail"],
        [EPSILON],
    ],
    "arg_expr": [
        ["arg_typed_rhs", "arg_assign_tail"],
    ],
    "arg_assign_tail": [
        ["assign_op", "arg_typed_rhs"],
        [EPSILON],
    ],
    "arg_typed_rhs": [
        ["arg_bool_or_concat"],
    ],
    "arg_bool_or_concat": [
        ["stringlit", "arg_concat_tail_typed"],
        ["charlit", "arg_concat_tail_typed"],
        ["string", "(", "arg_expr", ")", "arg_concat_tail_typed"],
        ["intlit", "arg_numeric_or_bool"],
        ["longlit", "arg_numeric_or_bool"],
        ["floatlit", "arg_numeric_or_bool"],
        ["doublelit", "arg_numeric_or_bool"],
        ["-", "arg_neg_numeric_or_bool"],
        ["true", "arg_bool_tail_opt"],
        ["false", "arg_bool_tail_opt"],
        ["!", "arg_bool_factor", "arg_bool_tail_opt"],
        ["int", "(", "arg_expr", ")", "arg_numeric_or_bool"],
        ["long", "(", "arg_expr", ")", "arg_numeric_or_bool"],
        ["float", "(", "arg_expr", ")", "arg_numeric_or_bool"],
        ["double", "(", "arg_expr", ")", "arg_numeric_or_bool"],
        ["char", "(", "arg_expr", ")"],
        ["bool", "(", "arg_expr", ")", "arg_bool_tail_opt"],
        ["id", "arg_id_toplevel_cont"],
        ["(", "arg_toplevel_paren", ")", "arg_toplevel_paren_cont"],
        ["++", "id"],
        ["--", "id"],
    ],
    "arg_numeric_or_bool": [
        ["arg_arith_ops", "arg_after_arith"],
        ["arg_cmp_op", "numeric_add_expr_arg", "arg_bool_tail_opt"],
        ["arg_bool_tail_opt"],
    ],
    "arg_arith_ops": [
        ["+", "numeric_mul_expr_arg", "arg_numeric_add_ops"],
        ["-", "numeric_mul_expr_arg", "arg_numeric_add_ops"],
        ["*", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_ops"],
        ["/", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_ops"],
        ["%", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_ops"],
    ],
    "arg_numeric_add_ops": [
        ["+", "numeric_mul_expr_arg", "arg_numeric_add_ops"],
        ["-", "numeric_mul_expr_arg", "arg_numeric_add_ops"],
        [EPSILON],
    ],
    "arg_after_arith": [
        ["arg_cmp_op", "numeric_add_expr_arg", "arg_bool_tail_opt"],
        ["arg_bool_tail_opt"],
    ],
    "arg_neg_numeric_or_bool": [
        ["numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_ops", "arg_after_arith"],
    ],
    "arg_bool_tail_opt": [
        ["&&", "arg_bool_term", "arg_bool_and_tail", "arg_bool_or_tail_opt"],
        ["||", "arg_bool_term", "arg_bool_or_tail"],
        [EPSILON],
    ],
    "arg_bool_or_tail_opt": [
        ["||", "arg_bool_term", "arg_bool_or_tail"],
        [EPSILON],
    ],
    "arg_id_toplevel_cont": [
        ["arg_arith_ops", "arg_after_arith"],
        ["arg_cmp_op", "numeric_add_expr_arg", "arg_bool_tail_opt"],
        ["++"],
        ["--"],
        ["arg_postfix_chain", "arg_id_after_postfix"],
    ],
    "arg_id_after_postfix": [
        ["arg_arith_ops", "arg_after_arith"],
        ["arg_cmp_op", "numeric_add_expr_arg", "arg_bool_tail_opt"],
        ["..", "arg_string_operand", "arg_concat_tail_typed"],
        ["arg_bool_tail_opt"],
    ],
    "arg_toplevel_paren": [
        ["arg_bool_or_concat"],
    ],
    "arg_toplevel_paren_cont": [
        ["arg_arith_ops", "arg_after_arith"],
        ["arg_cmp_op", "numeric_add_expr_arg", "arg_bool_tail_opt"],
        ["..", "arg_string_operand", "arg_concat_tail_typed"],
        ["arg_bool_tail_opt"],
    ],
    "arg_concat_tail_typed": [
        ["..", "arg_string_operand", "arg_concat_tail_typed"],
        [EPSILON],
    ],
    "arg_string_operand": [
        ["stringlit"],
        ["charlit"],
        ["id", "str_operand_id_tail"],
        ["string", "(", "arg_expr", ")"],
        ["char", "(", "arg_expr", ")"],
        ["(", "arg_string_operand", "arg_concat_tail_typed", ")"],
    ],
    "arg_bool_term": [
        ["arg_bool_eq", "arg_bool_and_tail"],
    ],
    "arg_bool_and_tail": [
        ["&&", "arg_bool_eq", "arg_bool_and_tail"],
        [EPSILON],
    ],
    "arg_bool_or_tail": [
        ["||", "arg_bool_term", "arg_bool_or_tail"],
        [EPSILON],
    ],
    "arg_bool_eq": [
        ["arg_bool_factor", "arg_bool_eq_tail"],
    ],
    "arg_bool_eq_tail": [
        ["==", "arg_bool_factor", "arg_bool_eq_tail"],
        ["!=", "arg_bool_factor", "arg_bool_eq_tail"],
        [EPSILON],
    ],
    "arg_bool_factor": [
        ["!", "arg_bool_factor"],
        ["arg_bool_atom"],
    ],
    "arg_bool_atom": [
        ["true"],
        ["false"],
        ["id", "arg_bool_id_cont"],
        ["intlit", "arg_numeric_cmp_required"],
        ["longlit", "arg_numeric_cmp_required"],
        ["floatlit", "arg_numeric_cmp_required"],
        ["doublelit", "arg_numeric_cmp_required"],
        ["-", "arg_numeric_neg_cmp"],
        ["(", "arg_bool_paren", ")"],
        ["int", "(", "arg_expr", ")", "arg_numeric_cmp_required"],
        ["long", "(", "arg_expr", ")", "arg_numeric_cmp_required"],
        ["float", "(", "arg_expr", ")", "arg_numeric_cmp_required"],
        ["double", "(", "arg_expr", ")", "arg_numeric_cmp_required"],
    ],
    "arg_bool_paren": [
        ["arg_bool_term", "arg_bool_and_or_tail"],
    ],
    "arg_bool_and_or_tail": [
        ["&&", "arg_bool_term", "arg_bool_and_or_tail"],
        ["||", "arg_bool_term", "arg_bool_and_or_tail"],
        [EPSILON],
    ],
    "arg_bool_id_cont": [
        ["arg_numeric_arith_cmp"],
        ["++"],
        ["--"],
        ["arg_postfix_chain"],
    ],
    "arg_numeric_arith_cmp": [
        ["+", "numeric_mul_expr_arg", "arg_numeric_add_cmp", "arg_cmp_op", "numeric_add_expr_arg"],
        ["-", "numeric_mul_expr_arg", "arg_numeric_add_cmp", "arg_cmp_op", "numeric_add_expr_arg"],
        ["*", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_cmp", "arg_cmp_op", "numeric_add_expr_arg"],
        ["/", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_cmp", "arg_cmp_op", "numeric_add_expr_arg"],
        ["%", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_cmp", "arg_cmp_op", "numeric_add_expr_arg"],
        ["arg_cmp_op", "numeric_add_expr_arg"],
    ],
    "arg_numeric_add_cmp": [
        ["+", "numeric_mul_expr_arg", "arg_numeric_add_cmp"],
        ["-", "numeric_mul_expr_arg", "arg_numeric_add_cmp"],
        [EPSILON],
    ],
    "arg_numeric_cmp_required": [
        ["arg_numeric_lit_arith", "arg_cmp_op", "numeric_add_expr_arg"],
    ],
    "arg_numeric_lit_arith": [
        ["*", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_cmp"],
        ["/", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_cmp"],
        ["%", "numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_cmp"],
        ["+", "numeric_mul_expr_arg", "arg_numeric_add_cmp"],
        ["-", "numeric_mul_expr_arg", "arg_numeric_add_cmp"],
        [EPSILON],
    ],
    "arg_numeric_neg_cmp": [
        ["numeric_unary_expr_arg", "numeric_mul_tail_arg", "arg_numeric_add_cmp", "arg_cmp_op", "numeric_add_expr_arg"],
    ],
    "arg_cmp_op": [
        ["<"],
        [">"],
        ["<="],
        [">="],
        ["=="],
        ["!="],
    ],
    "numeric_mul_expr_arg": [
        ["numeric_unary_expr_arg", "numeric_mul_tail_arg"],
    ],
    "numeric_mul_tail_arg": [
        ["*", "numeric_unary_expr_arg", "numeric_mul_tail_arg"],
        ["/", "numeric_unary_expr_arg", "numeric_mul_tail_arg"],
        ["%", "numeric_unary_expr_arg", "numeric_mul_tail_arg"],
        [EPSILON],
    ],
    "numeric_add_expr_arg": [
        ["numeric_mul_expr_arg", "numeric_add_tail_arg"],
    ],
    "numeric_add_tail_arg": [
        ["+", "numeric_mul_expr_arg", "numeric_add_tail_arg"],
        ["-", "numeric_mul_expr_arg", "numeric_add_tail_arg"],
        [EPSILON],
    ],
    "numeric_unary_expr_arg": [
        ["!", "numeric_unary_expr_arg"],
        ["-", "numeric_unary_expr_arg"],
        ["numeric_postfix_expr_arg"],
    ],
    "numeric_postfix_expr_arg": [
        ["(", "arg_expr", ")", "arg_postfix_chain"],
        ["int", "(", "arg_expr", ")"],
        ["long", "(", "arg_expr", ")"],
        ["float", "(", "arg_expr", ")"],
        ["double", "(", "arg_expr", ")"],
        ["++", "id"],
        ["--", "id"],
        ["id", "arg_id_postfix"],
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
    ],
    "arg_id_postfix": [
        ["++"],
        ["--"],
        ["arg_postfix_chain"],
    ],
    "arg_postfix_chain": [
        ["arg_array_access", "arg_postfix_after_arr"],
        [".", "id", "arg_postfix_chain"],
        ["(", "arg_nested_list", ")", "arg_postfix_chain"],
        [EPSILON],
    ],
    "arg_array_access": [
        ["[", "arg_array_index", "]", "arg_array_access_dim2"],
    ],
    "arg_array_access_dim2": [
        ["[", "arg_array_index", "]"],
        [EPSILON],
    ],
    "arg_postfix_after_arr": [
        [".", "id", "arg_postfix_chain"],
        ["(", "arg_nested_list", ")", "arg_postfix_chain"],
        [EPSILON],
    ],
    "arg_array_index": [
        ["intlit"],
        ["id"],
    ],
    "arg_nested_list": [
        ["arg_expr", "arg_nested_tail"],
        [EPSILON],
    ],
    "arg_nested_tail": [
        [",", "arg_expr", "arg_nested_tail"],
        [EPSILON],
    ],
    "io_stmt": [
        ["trap", "(", "trap_target", ")", ";"],
        ["thread", "(", "print_args", ")", ";"],
        ["threadln", "(", "print_args", ")", ";"],
    ],
    "trap_target": [
        ["id", "trap_target_tail"],
    ],
    "trap_target_tail": [
        ["[", "arg_expr", "]"],
        [".", "id"],
        [EPSILON],
    ],
    "print_args": [
        ["arg_expr", "print_tail"],
    ],
    "print_tail": [
        [",", "arg_expr", "print_tail"],
        [EPSILON],
    ],
    "ctrl_struct": [
        ["if", "(", "condition", ")", "{", "non_empty_ctrl_stmt_list", "}", "else_opt"],
        ["switch", "(", "arg_expr", ")", "{", "case_list", "default_opt", "}"],
        ["for", "(", "for_init", ";", "for_cond", ";", "for_update", ")", "{", "non_empty_loop_ctrl_stmt_list", "}"],
        ["while", "(", "condition", ")", "{", "non_empty_loop_ctrl_stmt_list", "}"],
        ["do", "{", "non_empty_loop_ctrl_stmt_list", "}", "while", "(", "condition", ")", ";"],
    ],
    "ctrl_stmt_list": [
        ["statement_non_return", "ctrl_stmt_list"],
        [EPSILON],
    ],
    "non_empty_ctrl_stmt_list": [
        ["statement_non_return", "ctrl_stmt_list"],
    ],
    "loop_statement_non_return": [
        ["statement_non_return"],
        ["break", ";"],
    ],
    "loop_ctrl_stmt_list": [
        ["loop_statement_non_return", "loop_ctrl_stmt_list"],
        [EPSILON],
    ],
    "non_empty_loop_ctrl_stmt_list": [
        ["loop_statement_non_return", "loop_ctrl_stmt_list"],
    ],
    "else_opt": [
        ["else", "else_body"],
        [EPSILON],
    ],
    "else_body": [
        ["{", "non_empty_ctrl_stmt_list", "}"],
        ["if", "(", "condition", ")", "{", "non_empty_ctrl_stmt_list", "}", "else_opt"],
    ],
    "case_list": [
        ["case", "case_val", ":", "non_empty_loop_ctrl_stmt_list", "break_opt", "case_list"],
        [EPSILON],
    ],
    "case_val": [
        ["intlit"],
        ["longlit"],
        ["charlit"],
        ["true"],
        ["false"],
    ],
    "default_opt": [
        ["default", ":", "non_empty_loop_ctrl_stmt_list", "break_opt"],
        [EPSILON],
    ],
    "break_opt": [
        ["break", ";"],
        [EPSILON],
    ],
    "for_init": [
        ["local", "var", "for_init_type", "id", "=", "for_init_expr"],
        ["id", "for_init_assign_tail"],
        [EPSILON],
    ],
    "for_init_assign_tail": [
        ["assign_op", "for_init_expr"],
    ],
    "for_init_expr": [
        ["stmt_typed_rhs"],
    ],
    "for_init_type": [
        ["int"],
        ["long"],
        ["float"],
        ["double"],
        ["char"],
        ["string"],
        ["bool"],
    ],
    "for_cond": [
        ["condition"],
    ],
    "condition": [
        ["cond_or"],
    ],
    "cond_or": [
        ["cond_and", "cond_or_tail"],
    ],
    "cond_or_tail": [
        ["||", "cond_and", "cond_or_tail"],
        [EPSILON],
    ],
    "cond_and": [
        ["cond_not", "cond_and_tail"],
    ],
    "cond_and_tail": [
        ["&&", "cond_not", "cond_and_tail"],
        [EPSILON],
    ],
    "cond_not": [
        ["!", "cond_not"],
        ["cond_atom"],
    ],
    "cond_atom": [
        ["true"],
        ["false"],
        ["id", "cond_id_cont"],
        ["(", "cond_paren_inner", ")", "cond_paren_tail"],
        ["cond_lit_cmp"],
        ["++", "cond_lit_unary", "cond_lit_mul", "cond_lit_add", "cond_cmp", "cond_rhs"],
        ["--", "cond_lit_unary", "cond_lit_mul", "cond_lit_add", "cond_cmp", "cond_rhs"],
    ],
    "cond_paren_inner": [
        ["cond_paren_start", "cond_paren_cont"],
    ],
    "cond_paren_start": [
        ["id"],
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["true"],
        ["false"],
        ["!", "cond_not"],
        ["++", "cond_paren_unary"],
        ["--", "cond_paren_unary"],
        ["-", "cond_paren_unary"],
        ["(", "cond_paren_inner", ")"],
    ],
    "cond_paren_cont": [
        ["cond_paren_arith_ops", "cond_paren_after_arith"],
        ["cond_cmp", "cond_rhs", "cond_paren_logic"],
        ["cond_paren_logic"],
        ["++", "cond_cmp", "cond_rhs", "cond_paren_logic"],
        ["++", "cond_paren_arith_ops", "cond_paren_after_arith"],
        ["--", "cond_cmp", "cond_rhs", "cond_paren_logic"],
        ["--", "cond_paren_arith_ops", "cond_paren_after_arith"],
    ],
    "cond_paren_arith_ops": [
        ["+", "cond_paren_unary", "cond_paren_mul_ops"],
        ["-", "cond_paren_unary", "cond_paren_mul_ops"],
        ["*", "cond_paren_unary", "cond_paren_mul_ops"],
        ["/", "cond_paren_unary", "cond_paren_mul_ops"],
        ["%", "cond_paren_unary", "cond_paren_mul_ops"],
    ],
    "cond_paren_mul_ops": [
        ["*", "cond_paren_unary", "cond_paren_mul_ops"],
        ["/", "cond_paren_unary", "cond_paren_mul_ops"],
        ["%", "cond_paren_unary", "cond_paren_mul_ops"],
        ["+", "cond_paren_unary", "cond_paren_mul_ops"],
        ["-", "cond_paren_unary", "cond_paren_mul_ops"],
        [EPSILON],
    ],
    "cond_paren_unary": [
        ["++", "cond_paren_unary"],
        ["--", "cond_paren_unary"],
        ["-", "cond_paren_unary"],
        ["cond_paren_primary"],
    ],
    "cond_paren_primary": [
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["id", "cond_rhs_id_tail"],
        ["(", "cond_paren_inner", ")"],
    ],
    "cond_paren_after_arith": [
        ["cond_cmp", "cond_rhs", "cond_paren_logic"],
        [EPSILON],
    ],
    "cond_paren_logic": [
        ["&&", "cond_and"],
        ["||", "cond_or"],
        [EPSILON],
    ],
    "cond_paren_tail": [
        ["cond_cmp", "cond_rhs"],
        [EPSILON],
    ],
    "cond_id_cont": [
        ["[", "cond_arr_index", "]", "cond_id_arr_cont"],
        ["+", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["-", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["*", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["/", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["%", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["<", "cond_rhs"],
        [">", "cond_rhs"],
        ["<=", "cond_rhs"],
        [">=", "cond_rhs"],
        ["==", "cond_rhs"],
        ["!=", "cond_rhs"],
        ["++", "cond_cmp", "cond_rhs"],
        ["++", "+", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "-", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "*", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "/", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "%", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "cond_cmp", "cond_rhs"],
        ["--", "+", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "-", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "*", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "/", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "%", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        [EPSILON],
    ],
    "cond_arr_index": [
        ["cond_rhs"],
    ],
    "cond_id_arr_cont": [
        ["[", "cond_arr_index", "]", "cond_id_arr_after"],
        ["cond_id_arr_after"],
    ],
    "cond_id_arr_after": [
        ["+", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["-", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["*", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["/", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["%", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["<", "cond_rhs"],
        [">", "cond_rhs"],
        ["<=", "cond_rhs"],
        [">=", "cond_rhs"],
        ["==", "cond_rhs"],
        ["!=", "cond_rhs"],
        ["++", "cond_cmp", "cond_rhs"],
        ["++", "+", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "-", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "*", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "/", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["++", "%", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "cond_cmp", "cond_rhs"],
        ["--", "+", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "-", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "*", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "/", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        ["--", "%", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add", "cond_cmp", "cond_rhs"],
        [EPSILON],
    ],
    "cond_lit_cmp": [
        ["intlit", "cond_lit_mul", "cond_lit_add", "cond_cmp", "cond_rhs"],
        ["longlit", "cond_lit_mul", "cond_lit_add", "cond_cmp", "cond_rhs"],
        ["floatlit", "cond_lit_mul", "cond_lit_add", "cond_cmp", "cond_rhs"],
        ["doublelit", "cond_lit_mul", "cond_lit_add", "cond_cmp", "cond_rhs"],
        ["-", "cond_lit_unary", "cond_lit_mul", "cond_lit_add", "cond_cmp", "cond_rhs"],
    ],
    "cond_lit_mul": [
        ["*", "cond_lit_unary", "cond_lit_mul"],
        ["/", "cond_lit_unary", "cond_lit_mul"],
        ["%", "cond_lit_unary", "cond_lit_mul"],
        [EPSILON],
    ],
    "cond_lit_add": [
        ["+", "cond_lit_unary", "cond_lit_mul", "cond_lit_add"],
        ["-", "cond_lit_unary", "cond_lit_mul", "cond_lit_add"],
        [EPSILON],
    ],
    "cond_lit_unary": [
        ["++", "cond_lit_unary"],
        ["--", "cond_lit_unary"],
        ["-", "cond_lit_unary"],
        ["cond_lit_primary"],
    ],
    "cond_lit_primary": [
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["id", "cond_rhs_id_tail"],
        ["(", "cond_lit_expr", ")"],
    ],
    "cond_lit_expr": [
        ["cond_lit_unary", "cond_lit_mul", "cond_lit_add"],
    ],
    "cond_rhs": [
        ["cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add"],
    ],
    "cond_rhs_unary": [
        ["++", "cond_rhs_unary"],
        ["--", "cond_rhs_unary"],
        ["-", "cond_rhs_unary"],
        ["cond_rhs_primary"],
    ],
    "cond_rhs_primary": [
        ["intlit"],
        ["longlit"],
        ["floatlit"],
        ["doublelit"],
        ["id", "cond_rhs_id_tail"],
        ["(", "cond_rhs", ")"],
    ],
    "cond_rhs_id_tail": [
        ["[", "cond_arr_index", "]", "cond_rhs_arr_tail"],
        ["++"],
        ["--"],
        [EPSILON],
    ],
    "cond_rhs_arr_tail": [
        ["[", "cond_arr_index", "]"],
        ["[", "cond_arr_index", "]", "++"],
        ["[", "cond_arr_index", "]", "--"],
        ["++"],
        ["--"],
        [EPSILON],
    ],
    "cond_rhs_mul": [
        ["*", "cond_rhs_unary", "cond_rhs_mul"],
        ["/", "cond_rhs_unary", "cond_rhs_mul"],
        ["%", "cond_rhs_unary", "cond_rhs_mul"],
        [EPSILON],
    ],
    "cond_rhs_add": [
        ["+", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add"],
        ["-", "cond_rhs_unary", "cond_rhs_mul", "cond_rhs_add"],
        [EPSILON],
    ],
    "cond_cmp": [
        ["<"],
        [">"],
        ["<="],
        [">="],
        ["=="],
        ["!="],
    ],
    "for_update": [
        ["id", "for_update_tail"],
        ["++", "id"],
        ["--", "id"],
        [EPSILON],
    ],
    "for_update_tail": [
        ["++"],
        ["--"],
        ["assign_op", "arg_expr"],
    ],
    "main_body": [
        ["main_content"],
    ],
    "main_content": [
        ["using", "id", "using_cont", ";", "main_content"],
        ["local", "mutability", "local_dec_body", "main_content"],
        ["statement_non_return", "main_content"],
        ["return", "intlit", ";"],
    ],
}


# =============================================================================
# FIRST Set Computation
# =============================================================================

def compute_first(grammar: dict) -> dict:
    """
    Compute FIRST sets for all non-terminals using iterative fixpoint algorithm.
    
    FIRST(A) = set of terminals that can begin strings derived from A.
    If A can derive ε, then ε ∈ FIRST(A).
    
    Args:
        grammar: dict mapping non-terminal -> list of productions
        
    Returns:
        dict mapping non-terminal -> set of first symbols
    """
    # Initialize FIRST sets for all non-terminals as empty
    first = {nt: set() for nt in grammar}
    
    # Iterative fixpoint: repeat until no changes
    changed = True
    while changed:
        changed = False
        
        for nt, productions in grammar.items():
            for prod in productions:
                # Compute FIRST of this production and add to FIRST[nt]
                prod_first = _first_of_production(prod, first, grammar)
                
                old_size = len(first[nt])
                first[nt] |= prod_first
                if len(first[nt]) > old_size:
                    changed = True
    
    return first


def _first_of_production(prod: list, first: dict, grammar: dict) -> set:
    """
    Compute FIRST set of a production (sequence of symbols).
    
    Args:
        prod: list of symbols (terminals and non-terminals)
        first: current FIRST sets (may be incomplete during iteration)
        grammar: the grammar dict (to identify non-terminals)
        
    Returns:
        set of first symbols for this production
    """
    result = set()
    
    # Empty production -> FIRST = {ε}
    if not prod or prod == [EPSILON]:
        return {EPSILON}
    
    # Process symbols left to right
    for symbol in prod:
        if symbol == EPSILON:
            # Explicit epsilon in sequence
            result.add(EPSILON)
            break
        elif symbol not in grammar:
            # Terminal: add it and stop
            result.add(symbol)
            break
        else:
            # Non-terminal: add FIRST(symbol) - {ε}
            symbol_first = first.get(symbol, set())
            result |= (symbol_first - {EPSILON})
            
            # If symbol is not nullable, stop
            if EPSILON not in symbol_first:
                break
    else:
        # All symbols were nullable -> add ε
        result.add(EPSILON)
    
    return result


def first_of_sequence(sequence: list, first_sets: dict = None) -> set:
    """
    Compute FIRST set for an arbitrary sequence of symbols.
    
    Args:
        sequence: list of symbols (terminals and non-terminals)
        first_sets: precomputed FIRST sets (defaults to module-level FIRST)
        
    Returns:
        set of first symbols for the sequence
    """
    if first_sets is None:
        first_sets = FIRST
    
    return _first_of_production(sequence, first_sets, GRAMMAR)


# Compute FIRST sets at module load time
FIRST = compute_first(GRAMMAR)


# =============================================================================
# FOLLOW Set Computation
# =============================================================================

def compute_follow(grammar: dict, first: dict, start_symbol: str) -> dict:
    """
    Compute FOLLOW sets for all non-terminals using iterative fixpoint algorithm.
    
    FOLLOW(A) = set of terminals that can appear immediately after A in some
    sentential form. $ (end of input) is in FOLLOW(start_symbol).
    
    Rules:
    1. $ ∈ FOLLOW(S) where S is the start symbol
    2. For A → α B β: FOLLOW(B) includes FIRST(β) - {ε}
    3. For A → α B β where ε ∈ FIRST(β): FOLLOW(B) includes FOLLOW(A)
    4. For A → α B (B at end): FOLLOW(B) includes FOLLOW(A)
    
    Args:
        grammar: dict mapping non-terminal -> list of productions
        first: precomputed FIRST sets
        start_symbol: the grammar's start symbol
        
    Returns:
        dict mapping non-terminal -> set of follow symbols
    """
    # Initialize FOLLOW sets for all non-terminals as empty
    follow = {nt: set() for nt in grammar}
    
    # Rule 1: $ ∈ FOLLOW(start_symbol)
    follow[start_symbol].add("$")
    
    # Iterative fixpoint: repeat until no changes
    changed = True
    while changed:
        changed = False
        
        for nt, productions in grammar.items():
            for prod in productions:
                # Skip epsilon productions
                if prod == [EPSILON]:
                    continue
                
                # Process each position in the production
                for i, symbol in enumerate(prod):
                    # Only process non-terminals
                    if symbol not in grammar:
                        continue
                    
                    # Get β (everything after this symbol)
                    beta = prod[i + 1:]
                    
                    if beta:
                        # Rule 2: Add FIRST(β) - {ε} to FOLLOW(symbol)
                        beta_first = _first_of_production(beta, first, grammar)
                        to_add = beta_first - {EPSILON}
                        
                        old_size = len(follow[symbol])
                        follow[symbol] |= to_add
                        if len(follow[symbol]) > old_size:
                            changed = True
                        
                        # Rule 3: If β can derive ε, add FOLLOW(A) to FOLLOW(symbol)
                        if EPSILON in beta_first:
                            old_size = len(follow[symbol])
                            follow[symbol] |= follow[nt]
                            if len(follow[symbol]) > old_size:
                                changed = True
                    else:
                        # Rule 4: B is at the end, add FOLLOW(A) to FOLLOW(B)
                        old_size = len(follow[symbol])
                        follow[symbol] |= follow[nt]
                        if len(follow[symbol]) > old_size:
                            changed = True
    
    return follow


# Compute FOLLOW sets at module load time
FOLLOW = compute_follow(GRAMMAR, FIRST, START_SYMBOL)


# =============================================================================
# PREDICT Set Computation
# =============================================================================

class LL1ConflictError(Exception):
    """Raised when the grammar has an LL(1) conflict."""
    pass


def compute_predict(grammar: dict, first: dict, follow: dict, raise_on_conflict: bool = False) -> dict:
    """
    Compute PREDICT sets for all productions.
    
    For each production A → α:
        PREDICT(A → α) = FIRST(α) - {ε}
        If ε ∈ FIRST(α): PREDICT(A → α) ∪= FOLLOW(A)
    
    Args:
        grammar: dict mapping non-terminal -> list of productions
        first: precomputed FIRST sets
        follow: precomputed FOLLOW sets
        raise_on_conflict: if True, raise LL1ConflictError on first conflict
        
    Returns:
        dict mapping (non-terminal, tuple(production)) -> set of predict symbols
        
    Raises:
        LL1ConflictError: if raise_on_conflict=True and conflicts exist
    """
    predict = {}
    
    for nt, productions in grammar.items():
        for prod in productions:
            # Compute FIRST(α) for this production
            prod_first = _first_of_production(prod, first, grammar)
            
            # PREDICT = FIRST(α) - {ε}
            prod_predict = prod_first - {EPSILON}
            
            # If ε ∈ FIRST(α), add FOLLOW(A)
            if EPSILON in prod_first:
                prod_predict |= follow[nt]
            
            # Store with tuple key for hashability
            predict[(nt, tuple(prod))] = prod_predict
    
    # Check for conflicts if requested
    if raise_on_conflict:
        conflicts = detect_ll1_conflicts(grammar, predict)
        if conflicts:
            raise LL1ConflictError(
                f"Grammar has {len(conflicts)} LL(1) conflict(s). "
                f"First conflict:\n{conflicts[0]}"
            )
    
    return predict


def detect_ll1_conflicts(grammar: dict, predict: dict) -> list:
    """
    Detect all LL(1) conflicts in the grammar.
    
    For each non-terminal, check if any two productions have overlapping
    PREDICT sets.
    
    Args:
        grammar: the grammar dict
        predict: the computed PREDICT sets
        
    Returns:
        list of conflict descriptions (empty if grammar is LL(1))
    """
    conflicts = []
    
    for nt, productions in grammar.items():
        # Compare each pair of productions for this non-terminal
        prod_list = [(tuple(p), predict[(nt, tuple(p))]) for p in productions]
        
        for i in range(len(prod_list)):
            for j in range(i + 1, len(prod_list)):
                prod1, pred1 = prod_list[i]
                prod2, pred2 = prod_list[j]
                
                # Check for overlap
                overlap = pred1 & pred2
                if overlap:
                    conflict = {
                        "non_terminal": nt,
                        "production1": prod1,
                        "predict1": pred1,
                        "production2": prod2,
                        "predict2": pred2,
                        "overlap": overlap
                    }
                    conflicts.append(conflict)
    
    return conflicts


def format_conflict(conflict: dict) -> str:
    """Format a conflict dict as a readable string."""
    nt = conflict["non_terminal"]
    p1 = " ".join(conflict["production1"])
    p2 = " ".join(conflict["production2"])
    return (
        f"LL(1) conflict in '{nt}':\n"
        f"  {nt} -> {p1}\n"
        f"    PREDICT = {conflict['predict1']}\n"
        f"  {nt} -> {p2}\n"
        f"    PREDICT = {conflict['predict2']}\n"
        f"  Overlap: {conflict['overlap']}"
    )


# Compute PREDICT sets at module load time
PREDICT = compute_predict(GRAMMAR, FIRST, FOLLOW, raise_on_conflict=False)

# Detect conflicts (stored for inspection)
LL1_CONFLICTS = detect_ll1_conflicts(GRAMMAR, PREDICT)
