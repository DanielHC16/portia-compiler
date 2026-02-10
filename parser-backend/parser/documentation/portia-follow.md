## FOLLOW Set

| # | Nonterminal | FOLLOW Set |
|---|-------------|------------|
| 1 | `<program>` | { $END } |
| 2 | `<decl_list>` | { $END } |
| 3 | `<int_decl_or_main>` | { $END } |
| 4 | `<other_decl>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 5 | `<bool_lit>` | { ,, ;, } } |
| 6 | `<int_global_cont>` | { ; } |
| 7 | `<long_global_cont>` | { ; } |
| 8 | `<float_global_cont>` | { ; } |
| 9 | `<double_global_cont>` | { ; } |
| 10 | `<char_global_cont>` | { ; } |
| 11 | `<string_global_cont>` | { ; } |
| 12 | `<bool_global_cont>` | { ; } |
| 13 | `<int_decl_tail>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 14 | `<int_multi_decl>` | { ; } |
| 15 | `<long_decl_tail>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 16 | `<long_multi_decl>` | { ; } |
| 17 | `<float_decl_tail>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 18 | `<float_multi_decl>` | { ; } |
| 19 | `<double_decl_tail>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 20 | `<double_multi_decl>` | { ; } |
| 21 | `<char_decl_tail>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 22 | `<char_multi_decl>` | { ; } |
| 23 | `<string_decl_tail>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 24 | `<string_multi_decl>` | { ; } |
| 25 | `<bool_decl_tail>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 26 | `<bool_multi_decl>` | { ; } |
| 27 | `<weave_inst_decl>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 28 | `<weave_inst_tail>` | { ,, ; } |
| 29 | `<weave_field_value>` | { ,, } } |
| 30 | `<weave_value_list>` | { } } |
| 31 | `<weave_value_tail>` | { } } |
| 32 | `<weave_field_list_tail>` | { } } |
| 33 | `<weave_inst_cont>` | { ; } |
| 34 | `<weave_arr_cont>` | { ; } |
| 35 | `<weave_array_with_init>` | { ,, ; } |
| 36 | `<weave_array_init_tail>` | { ,, ; } |
| 37 | `<weave_arr_init_opt_1d>` | { ,, ; } |
| 38 | `<weave_arr_init_content_1d>` | { } } |
| 39 | `<weave_init_1d_tail>` | { } } |
| 40 | `<weave_arr_init_opt_2d>` | { ,, ; } |
| 41 | `<weave_arr_init_content_2d>` | { } } |
| 42 | `<weave_init_row>` | { } } |
| 43 | `<weave_init_2d_tail>` | { } } |
| 44 | `<mutability>` | { bool, char, double, float, id, int, long, string } |
| 45 | `<array_dims>` | { ), ,, ;, id } |
| 46 | `<array_dim2_opt>` | { ), ,, ;, id } |
| 47 | `<size>` | { ] } |
| 48 | `<int_array_with_init>` | { ; } |
| 49 | `<int_array_init_tail>` | { ; } |
| 50 | `<int_arr_init_opt_1d>` | { ; } |
| 51 | `<int_arr_init_content_1d>` | { } } |
| 52 | `<int_elem_1d_tail>` | { } } |
| 53 | `<int_arr_init_opt_2d>` | { ; } |
| 54 | `<int_arr_init_content_2d>` | { } } |
| 55 | `<int_elem_list>` | { } } |
| 56 | `<int_elem_2d_tail>` | { } } |
| 57 | `<long_array_with_init>` | { ; } |
| 58 | `<long_array_init_tail>` | { ; } |
| 59 | `<long_arr_init_opt_1d>` | { ; } |
| 60 | `<long_arr_init_content_1d>` | { } } |
| 61 | `<long_elem_1d_tail>` | { } } |
| 62 | `<long_arr_init_opt_2d>` | { ; } |
| 63 | `<long_arr_init_content_2d>` | { } } |
| 64 | `<long_elem_list>` | { } } |
| 65 | `<long_elem_2d_tail>` | { } } |
| 66 | `<float_array_with_init>` | { ; } |
| 67 | `<float_array_init_tail>` | { ; } |
| 68 | `<float_arr_init_opt_1d>` | { ; } |
| 69 | `<float_arr_init_content_1d>` | { } } |
| 70 | `<float_elem_1d_tail>` | { } } |
| 71 | `<float_arr_init_opt_2d>` | { ; } |
| 72 | `<float_arr_init_content_2d>` | { } } |
| 73 | `<float_elem_list>` | { } } |
| 74 | `<float_elem_2d_tail>` | { } } |
| 75 | `<double_array_with_init>` | { ; } |
| 76 | `<double_array_init_tail>` | { ; } |
| 77 | `<double_arr_init_opt_1d>` | { ; } |
| 78 | `<double_arr_init_content_1d>` | { } } |
| 79 | `<double_elem_1d_tail>` | { } } |
| 80 | `<double_arr_init_opt_2d>` | { ; } |
| 81 | `<double_arr_init_content_2d>` | { } } |
| 82 | `<double_elem_list>` | { } } |
| 83 | `<double_elem_2d_tail>` | { } } |
| 84 | `<char_array_with_init>` | { ; } |
| 85 | `<char_array_init_tail>` | { ; } |
| 86 | `<char_arr_init_opt_1d>` | { ; } |
| 87 | `<char_arr_init_content_1d>` | { } } |
| 88 | `<char_elem_1d_tail>` | { } } |
| 89 | `<char_arr_init_opt_2d>` | { ; } |
| 90 | `<char_arr_init_content_2d>` | { } } |
| 91 | `<char_elem_list>` | { } } |
| 92 | `<char_elem_2d_tail>` | { } } |
| 93 | `<string_array_with_init>` | { ; } |
| 94 | `<string_array_init_tail>` | { ; } |
| 95 | `<string_arr_init_opt_1d>` | { ; } |
| 96 | `<string_arr_init_content_1d>` | { } } |
| 97 | `<string_elem_1d_tail>` | { } } |
| 98 | `<string_arr_init_opt_2d>` | { ; } |
| 99 | `<string_arr_init_content_2d>` | { } } |
| 100 | `<string_elem_list>` | { } } |
| 101 | `<string_elem_2d_tail>` | { } } |
| 102 | `<bool_array_with_init>` | { ; } |
| 103 | `<bool_array_init_tail>` | { ; } |
| 104 | `<bool_arr_init_opt_1d>` | { ; } |
| 105 | `<bool_arr_init_content_1d>` | { } } |
| 106 | `<bool_elem_1d_tail>` | { } } |
| 107 | `<bool_arr_init_opt_2d>` | { ; } |
| 108 | `<bool_arr_init_content_2d>` | { } } |
| 109 | `<bool_elem_list>` | { } } |
| 110 | `<bool_elem_2d_tail>` | { } } |
| 111 | `<field_list>` | { } } |
| 112 | `<field_dec>` | { bool, char, double, float, id, int, long, string, } } |
| 113 | `<field_type>` | { id } |
| 114 | `<field_arr_opt>` | { ,, ; } |
| 115 | `<field_cont>` | { ; } |
| 116 | `<func_ret_int>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 117 | `<func_ret_long>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 118 | `<func_ret_float>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 119 | `<func_ret_double>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 120 | `<func_ret_char>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 121 | `<func_ret_string>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 122 | `<func_ret_bool>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 123 | `<func_ret_weave>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 124 | `<param_list>` | { ) } |
| 125 | `<param_type>` | { id } |
| 126 | `<param_arr_opt>` | { ), , } |
| 127 | `<param_cont>` | { ) } |
| 128 | `<function_body_int>` | { } } |
| 129 | `<func_content_int>` | { } } |
| 130 | `<function_body_long>` | { } } |
| 131 | `<func_content_long>` | { } } |
| 132 | `<function_body_float>` | { } } |
| 133 | `<func_content_float>` | { } } |
| 134 | `<function_body_double>` | { } } |
| 135 | `<func_content_double>` | { } } |
| 136 | `<function_body_char>` | { } } |
| 137 | `<func_content_char>` | { } } |
| 138 | `<function_body_string>` | { } } |
| 139 | `<func_content_string>` | { } } |
| 140 | `<function_body_bool>` | { } } |
| 141 | `<func_content_bool>` | { } } |
| 142 | `<function_body_array>` | { } } |
| 143 | `<func_content_array>` | { } } |
| 144 | `<function_body_weave>` | { } } |
| 145 | `<func_content_weave>` | { } } |
| 146 | `<function_body_void>` | { } } |
| 147 | `<func_content_void>` | { } } |
| 148 | `<statement_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 149 | `<statement_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 150 | `<statement_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 151 | `<statement_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 152 | `<statement_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 153 | `<statement_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 154 | `<statement_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 155 | `<statement_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 156 | `<statement_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 157 | `<statement_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 158 | `<ctrl_struct_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 159 | `<stmt_list_int>` | { break, case, default, } } |
| 160 | `<else_opt_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 161 | `<else_body_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 162 | `<case_list_int>` | { default, } } |
| 163 | `<default_opt_int>` | { } } |
| 164 | `<ctrl_struct_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 165 | `<stmt_list_long>` | { break, case, default, } } |
| 166 | `<else_opt_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 167 | `<else_body_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 168 | `<case_list_long>` | { default, } } |
| 169 | `<default_opt_long>` | { } } |
| 170 | `<ctrl_struct_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 171 | `<stmt_list_float>` | { break, case, default, } } |
| 172 | `<else_opt_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 173 | `<else_body_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 174 | `<case_list_float>` | { default, } } |
| 175 | `<default_opt_float>` | { } } |
| 176 | `<ctrl_struct_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 177 | `<stmt_list_double>` | { break, case, default, } } |
| 178 | `<else_opt_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 179 | `<else_body_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 180 | `<case_list_double>` | { default, } } |
| 181 | `<default_opt_double>` | { } } |
| 182 | `<ctrl_struct_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 183 | `<stmt_list_char>` | { break, case, default, } } |
| 184 | `<else_opt_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 185 | `<else_body_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 186 | `<case_list_char>` | { default, } } |
| 187 | `<default_opt_char>` | { } } |
| 188 | `<ctrl_struct_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 189 | `<stmt_list_string>` | { break, case, default, } } |
| 190 | `<else_opt_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 191 | `<else_body_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 192 | `<case_list_string>` | { default, } } |
| 193 | `<default_opt_string>` | { } } |
| 194 | `<ctrl_struct_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 195 | `<stmt_list_bool>` | { break, case, default, } } |
| 196 | `<else_opt_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 197 | `<else_body_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 198 | `<case_list_bool>` | { default, } } |
| 199 | `<default_opt_bool>` | { } } |
| 200 | `<ctrl_struct_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 201 | `<stmt_list_array>` | { break, case, default, } } |
| 202 | `<else_opt_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 203 | `<else_body_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 204 | `<case_list_array>` | { default, } } |
| 205 | `<default_opt_array>` | { } } |
| 206 | `<ctrl_struct_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 207 | `<stmt_list_weave>` | { break, case, default, } } |
| 208 | `<else_opt_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 209 | `<else_body_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 210 | `<case_list_weave>` | { default, } } |
| 211 | `<default_opt_weave>` | { } } |
| 212 | `<ctrl_struct_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 213 | `<stmt_list_void>` | { break, case, default, } } |
| 214 | `<else_opt_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 215 | `<else_body_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 216 | `<case_list_void>` | { default, } } |
| 217 | `<default_opt_void>` | { } } |
| 218 | `<int_return_expr>` | { ; } |
| 219 | `<int_ret_assign>` | { ; } |
| 220 | `<int_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 221 | `<int_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 222 | `<int_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 223 | `<int_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 224 | `<int_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 225 | `<int_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 226 | `<int_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 227 | `<int_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 228 | `<int_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 229 | `<long_return_expr>` | { ; } |
| 230 | `<long_ret_assign>` | { ; } |
| 231 | `<long_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 232 | `<long_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 233 | `<long_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 234 | `<long_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 235 | `<long_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 236 | `<long_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 237 | `<long_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 238 | `<long_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 239 | `<long_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 240 | `<float_return_expr>` | { ; } |
| 241 | `<float_ret_assign>` | { ; } |
| 242 | `<float_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 243 | `<float_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 244 | `<float_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 245 | `<float_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 246 | `<float_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 247 | `<float_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 248 | `<float_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 249 | `<float_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 250 | `<float_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 251 | `<double_return_expr>` | { ; } |
| 252 | `<double_ret_assign>` | { ; } |
| 253 | `<double_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 254 | `<double_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 255 | `<double_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 256 | `<double_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 257 | `<double_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 258 | `<double_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 259 | `<double_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 260 | `<double_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 261 | `<double_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 262 | `<char_return_expr>` | { ; } |
| 263 | `<char_ret_assign>` | { ; } |
| 264 | `<char_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 265 | `<char_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 266 | `<char_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 267 | `<char_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 268 | `<char_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 269 | `<char_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 270 | `<char_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 271 | `<char_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 272 | `<char_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 273 | `<string_return_expr>` | { ; } |
| 274 | `<string_ret_assign>` | { ; } |
| 275 | `<string_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 276 | `<string_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 277 | `<string_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 278 | `<string_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 279 | `<string_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 280 | `<string_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 281 | `<string_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 282 | `<string_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 283 | `<string_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 284 | `<bool_return_expr>` | { ; } |
| 285 | `<bool_ret_assign>` | { ; } |
| 286 | `<bool_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 287 | `<bool_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 288 | `<bool_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 289 | `<bool_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 290 | `<bool_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 291 | `<bool_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 292 | `<bool_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 293 | `<bool_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 294 | `<bool_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 295 | `<using_cont>` | { ; } |
| 296 | `<local_dec_body>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 297 | `<int_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 298 | `<int_local_cont>` | { ; } |
| 299 | `<long_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 300 | `<long_local_cont>` | { ; } |
| 301 | `<float_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 302 | `<float_local_cont>` | { ; } |
| 303 | `<double_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 304 | `<double_local_cont>` | { ; } |
| 305 | `<char_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 306 | `<char_local_cont>` | { ; } |
| 307 | `<string_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 308 | `<string_local_cont>` | { ; } |
| 309 | `<bool_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 310 | `<bool_local_cont>` | { ; } |
| 311 | `<weave_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 312 | `<statement_non_return>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 313 | `<ctrl_stmt_list>` | { break, case, default, } } |
| 314 | `<effect_stmt>` | { ; } |
| 315 | `<effect_pre_chain>` | { ; } |
| 316 | `<effect_pre_arr_chain>` | { ; } |
| 317 | `<effect_id_cont>` | { ; } |
| 318 | `<effect_post_call>` | { ; } |
| 319 | `<effect_post_call_member>` | { ; } |
| 320 | `<effect_post_call_arr>` | { ; } |
| 321 | `<effect_post_call_arr_cont>` | { ; } |
| 322 | `<effect_post_arr>` | { ; } |
| 323 | `<effect_post_arr_2d>` | { ; } |
| 324 | `<effect_arr_effect>` | { ; } |
| 325 | `<effect_post_member>` | { ; } |
| 326 | `<stmt_assign_expr>` | { ; } |
| 327 | `<stmt_assign_tail>` | { ; } |
| 328 | `<stmt_concat_expr>` | { %=, *=, +=, -=, /=, ;, = } |
| 329 | `<stmt_concat_tail>` | { %=, *=, +=, -=, /=, ;, = } |
| 330 | `<stmt_or_expr>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 331 | `<stmt_or_tail>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 332 | `<stmt_and_expr>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 333 | `<stmt_and_tail>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 334 | `<stmt_eq_expr>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 335 | `<stmt_eq_tail>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 336 | `<stmt_rel_expr>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 337 | `<stmt_rel_tail>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 338 | `<stmt_add_expr>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 339 | `<stmt_add_tail>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 340 | `<stmt_mul_expr>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 341 | `<stmt_mul_tail>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 342 | `<stmt_unary_expr>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 343 | `<stmt_postfix_expr>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 344 | `<stmt_id_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 345 | `<stmt_postfix_chain>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 346 | `<stmt_array_access>` | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 347 | `<stmt_array_access_dim2>` | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 348 | `<stmt_postfix_after_arr>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 349 | `<stmt_array_index>` | { ] } |
| 350 | `<stmt_arg_list>` | { ) } |
| 351 | `<stmt_arg_tail>` | { ) } |
| 352 | `<arg_expr>` | { ), , } |
| 353 | `<arg_assign_expr>` | { ), , } |
| 354 | `<arg_assign_tail>` | { ), , } |
| 355 | `<arg_concat_expr>` | { %=, ), *=, +=, ,, -=, /=, = } |
| 356 | `<arg_concat_tail>` | { %=, ), *=, +=, ,, -=, /=, = } |
| 357 | `<arg_or_expr>` | { %=, ), *=, +=, ,, -=, .., /=, = } |
| 358 | `<arg_or_tail>` | { %=, ), *=, +=, ,, -=, .., /=, = } |
| 359 | `<arg_and_expr>` | { %=, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 360 | `<arg_and_tail>` | { %=, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 361 | `<arg_eq_expr>` | { %=, &&, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 362 | `<arg_eq_tail>` | { %=, &&, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 363 | `<arg_rel_expr>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, =, ==, \|\| } |
| 364 | `<arg_rel_tail>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, =, ==, \|\| } |
| 365 | `<arg_add_expr>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 366 | `<arg_add_tail>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 367 | `<arg_mul_expr>` | { !=, %=, &&, ), *=, +, +=, ,, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 368 | `<arg_mul_tail>` | { !=, %=, &&, ), *=, +, +=, ,, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 369 | `<arg_unary_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 370 | `<arg_postfix_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 371 | `<arg_id_postfix>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 372 | `<arg_postfix_chain>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 373 | `<arg_array_access>` | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 374 | `<arg_array_access_dim2>` | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 375 | `<arg_postfix_after_arr>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 376 | `<arg_array_index>` | { ] } |
| 377 | `<arg_nested_list>` | { ) } |
| 378 | `<arg_nested_tail>` | { ) } |
| 379 | `<expression>` | { ) } |
| 380 | `<assign_expr>` | { ), ; } |
| 381 | `<assign_tail>` | { ), ; } |
| 382 | `<assign_op>` | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 383 | `<concat_expr>` | { %=, ), *=, +=, -=, /=, ;, = } |
| 384 | `<concat_tail>` | { %=, ), *=, +=, -=, /=, ;, = } |
| 385 | `<or_expr>` | { %=, ), *=, +=, -=, .., /=, ;, = } |
| 386 | `<or_tail>` | { %=, ), *=, +=, -=, .., /=, ;, = } |
| 387 | `<and_expr>` | { %=, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 388 | `<and_tail>` | { %=, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 389 | `<eq_expr>` | { %=, &&, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 390 | `<eq_tail>` | { %=, &&, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 391 | `<rel_expr>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 392 | `<rel_tail>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 393 | `<add_expr>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 394 | `<add_tail>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 395 | `<mul_expr>` | { !=, %=, &&, ), *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 396 | `<mul_tail>` | { !=, %=, &&, ), *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 397 | `<unary_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 398 | `<postfix_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 399 | `<id_postfix>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 400 | `<postfix_chain>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 401 | `<array_access>` | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 402 | `<array_access_dim2>` | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 403 | `<postfix_after_arr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 404 | `<array_index>` | { ] } |
| 405 | `<arg_list>` | { ) } |
| 406 | `<arg_tail>` | { ) } |
| 407 | `<io_stmt>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 408 | `<print_args>` | { ) } |
| 409 | `<print_tail>` | { ) } |
| 410 | `<ctrl_struct>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 411 | `<else_opt>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 412 | `<else_body>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 413 | `<case_list>` | { default, } } |
| 414 | `<case_val>` | { : } |
| 415 | `<default_opt>` | { } } |
| 416 | `<break_opt>` | { case, default, } } |
| 417 | `<for_init>` | { ; } |
| 418 | `<for_init_assign_tail>` | { ; } |
| 419 | `<for_init_expr>` | { ; } |
| 420 | `<for_init_type>` | { id } |
| 421 | `<for_cond>` | { ; } |
| 422 | `<for_update>` | { ) } |
| 423 | `<for_update_tail>` | { ) } |
| 424 | `<condition>` | { ), ; } |
| 425 | `<cond_or>` | { ), ; } |
| 426 | `<cond_or_tail>` | { ), ; } |
| 427 | `<cond_and>` | { ), ;, \|\| } |
| 428 | `<cond_and_tail>` | { ), ;, \|\| } |
| 429 | `<cond_comparison>` | { &&, ), ;, \|\| } |
| 430 | `<cond_primary>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 431 | `<cond_primary_continue>` | { &&, ), ;, \|\| } |
| 432 | `<cond_must_commit>` | { &&, ), ;, \|\| } |
| 433 | `<cond_postfix>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 434 | `<cond_cast_arg>` | { ) } |
| 435 | `<cond_id_post>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 436 | `<cond_post_chain>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 437 | `<cond_arr_access>` | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, \|\| } |
| 438 | `<cond_arr_access_dim2>` | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, \|\| } |
| 439 | `<cond_post_after_arr>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 440 | `<cond_arr_index>` | { ] } |
| 441 | `<cond_rhs>` | { &&, ), ;, \|\| } |
| 442 | `<comp_op>` | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 443 | `<main_body>` | { } } |
| 444 | `<main_content>` | { } } |