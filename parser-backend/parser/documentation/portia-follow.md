## FOLLOW Set

| # | Nonterminal | FOLLOW Set |
|---|-------------|------------|
| 1 | `<program>` | { $END } |
| 2 | `<global_section>` | { $END } |
| 3 | `<func_and_main>` | { $END } |
| 4 | `<global_decl>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 5 | `<function_decl>` | { func, int } |
| 6 | `<bool_lit>` | { ,, ;, } } |
| 7 | `<int_global_cont>` | { ; } |
| 8 | `<long_global_cont>` | { ; } |
| 9 | `<float_global_cont>` | { ; } |
| 10 | `<double_global_cont>` | { ; } |
| 11 | `<char_global_cont>` | { ; } |
| 12 | `<string_global_cont>` | { ; } |
| 13 | `<bool_global_cont>` | { ; } |
| 14 | `<weave_inst_decl>` | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 15 | `<weave_inst_tail>` | { ,, ; } |
| 16 | `<weave_field_value>` | { ,, } } |
| 17 | `<weave_value_list>` | { } } |
| 18 | `<weave_value_tail>` | { } } |
| 19 | `<weave_field_list_tail>` | { } } |
| 20 | `<weave_inst_cont>` | { ; } |
| 21 | `<weave_arr_cont>` | { ; } |
| 22 | `<weave_array_with_init>` | { ,, ; } |
| 23 | `<weave_array_init_tail>` | { ,, ; } |
| 24 | `<weave_arr_init_opt_1d>` | { ,, ; } |
| 25 | `<weave_arr_init_content_1d>` | { } } |
| 26 | `<weave_init_1d_tail>` | { } } |
| 27 | `<weave_arr_init_opt_2d>` | { ,, ; } |
| 28 | `<weave_arr_init_content_2d>` | { } } |
| 29 | `<weave_init_row>` | { } } |
| 30 | `<weave_init_2d_tail>` | { } } |
| 31 | `<mutability>` | { bool, char, double, float, id, int, long, string } |
| 32 | `<array_dims>` | { ), ,, ;, id } |
| 33 | `<array_dim2_opt>` | { ), ,, ;, id } |
| 34 | `<size>` | { ] } |
| 35 | `<int_array_with_init>` | { ; } |
| 36 | `<int_array_init_tail>` | { ; } |
| 37 | `<int_arr_init_opt_1d>` | { ; } |
| 38 | `<int_arr_init_content_1d>` | { } } |
| 39 | `<int_elem_1d_tail>` | { } } |
| 40 | `<int_arr_init_opt_2d>` | { ; } |
| 41 | `<int_arr_init_content_2d>` | { } } |
| 42 | `<int_elem_list>` | { } } |
| 43 | `<int_elem_2d_tail>` | { } } |
| 44 | `<long_array_with_init>` | { ; } |
| 45 | `<long_array_init_tail>` | { ; } |
| 46 | `<long_arr_init_opt_1d>` | { ; } |
| 47 | `<long_arr_init_content_1d>` | { } } |
| 48 | `<long_elem_1d_tail>` | { } } |
| 49 | `<long_arr_init_opt_2d>` | { ; } |
| 50 | `<long_arr_init_content_2d>` | { } } |
| 51 | `<long_elem_list>` | { } } |
| 52 | `<long_elem_2d_tail>` | { } } |
| 53 | `<float_array_with_init>` | { ; } |
| 54 | `<float_array_init_tail>` | { ; } |
| 55 | `<float_arr_init_opt_1d>` | { ; } |
| 56 | `<float_arr_init_content_1d>` | { } } |
| 57 | `<float_elem_1d_tail>` | { } } |
| 58 | `<float_arr_init_opt_2d>` | { ; } |
| 59 | `<float_arr_init_content_2d>` | { } } |
| 60 | `<float_elem_list>` | { } } |
| 61 | `<float_elem_2d_tail>` | { } } |
| 62 | `<double_array_with_init>` | { ; } |
| 63 | `<double_array_init_tail>` | { ; } |
| 64 | `<double_arr_init_opt_1d>` | { ; } |
| 65 | `<double_arr_init_content_1d>` | { } } |
| 66 | `<double_elem_1d_tail>` | { } } |
| 67 | `<double_arr_init_opt_2d>` | { ; } |
| 68 | `<double_arr_init_content_2d>` | { } } |
| 69 | `<double_elem_list>` | { } } |
| 70 | `<double_elem_2d_tail>` | { } } |
| 71 | `<char_array_with_init>` | { ; } |
| 72 | `<char_array_init_tail>` | { ; } |
| 73 | `<char_arr_init_opt_1d>` | { ; } |
| 74 | `<char_arr_init_content_1d>` | { } } |
| 75 | `<char_elem_1d_tail>` | { } } |
| 76 | `<char_arr_init_opt_2d>` | { ; } |
| 77 | `<char_arr_init_content_2d>` | { } } |
| 78 | `<char_elem_list>` | { } } |
| 79 | `<char_elem_2d_tail>` | { } } |
| 80 | `<string_array_with_init>` | { ; } |
| 81 | `<string_array_init_tail>` | { ; } |
| 82 | `<string_arr_init_opt_1d>` | { ; } |
| 83 | `<string_arr_init_content_1d>` | { } } |
| 84 | `<string_elem_1d_tail>` | { } } |
| 85 | `<string_arr_init_opt_2d>` | { ; } |
| 86 | `<string_arr_init_content_2d>` | { } } |
| 87 | `<string_elem_list>` | { } } |
| 88 | `<string_elem_2d_tail>` | { } } |
| 89 | `<bool_array_with_init>` | { ; } |
| 90 | `<bool_array_init_tail>` | { ; } |
| 91 | `<bool_arr_init_opt_1d>` | { ; } |
| 92 | `<bool_arr_init_content_1d>` | { } } |
| 93 | `<bool_elem_1d_tail>` | { } } |
| 94 | `<bool_arr_init_opt_2d>` | { ; } |
| 95 | `<bool_arr_init_content_2d>` | { } } |
| 96 | `<bool_elem_list>` | { } } |
| 97 | `<bool_elem_2d_tail>` | { } } |
| 98 | `<field_list>` | { } } |
| 99 | `<field_dec>` | { bool, char, double, float, id, int, long, string, } } |
| 100 | `<field_type>` | { id } |
| 101 | `<field_arr_opt>` | { ,, ; } |
| 102 | `<field_cont>` | { ; } |
| 103 | `<func_ret_int>` | { func, int } |
| 104 | `<func_ret_long>` | { func, int } |
| 105 | `<func_ret_float>` | { func, int } |
| 106 | `<func_ret_double>` | { func, int } |
| 107 | `<func_ret_char>` | { func, int } |
| 108 | `<func_ret_string>` | { func, int } |
| 109 | `<func_ret_bool>` | { func, int } |
| 110 | `<func_ret_weave>` | { func, int } |
| 111 | `<param_list>` | { ) } |
| 112 | `<param_type>` | { id } |
| 113 | `<param_arr_opt>` | { ), , } |
| 114 | `<param_cont>` | { ) } |
| 115 | `<function_body_int>` | { } } |
| 116 | `<func_content_int>` | { } } |
| 117 | `<function_body_long>` | { } } |
| 118 | `<func_content_long>` | { } } |
| 119 | `<function_body_float>` | { } } |
| 120 | `<func_content_float>` | { } } |
| 121 | `<function_body_double>` | { } } |
| 122 | `<func_content_double>` | { } } |
| 123 | `<function_body_char>` | { } } |
| 124 | `<func_content_char>` | { } } |
| 125 | `<function_body_string>` | { } } |
| 126 | `<func_content_string>` | { } } |
| 127 | `<function_body_bool>` | { } } |
| 128 | `<func_content_bool>` | { } } |
| 129 | `<function_body_array>` | { } } |
| 130 | `<func_content_array>` | { } } |
| 131 | `<function_body_weave>` | { } } |
| 132 | `<func_content_weave>` | { } } |
| 133 | `<function_body_void>` | { } } |
| 134 | `<func_content_void>` | { } } |
| 135 | `<statement_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 136 | `<statement_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 137 | `<statement_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 138 | `<statement_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 139 | `<statement_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 140 | `<statement_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 141 | `<statement_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 142 | `<statement_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 143 | `<statement_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 144 | `<statement_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 145 | `<ctrl_struct_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 146 | `<stmt_list_int>` | { break, case, default, } } |
| 147 | `<else_opt_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 148 | `<else_body_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 149 | `<case_list_int>` | { default, } } |
| 150 | `<default_opt_int>` | { } } |
| 151 | `<ctrl_struct_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 152 | `<stmt_list_long>` | { break, case, default, } } |
| 153 | `<else_opt_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 154 | `<else_body_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 155 | `<case_list_long>` | { default, } } |
| 156 | `<default_opt_long>` | { } } |
| 157 | `<ctrl_struct_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 158 | `<stmt_list_float>` | { break, case, default, } } |
| 159 | `<else_opt_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 160 | `<else_body_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 161 | `<case_list_float>` | { default, } } |
| 162 | `<default_opt_float>` | { } } |
| 163 | `<ctrl_struct_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 164 | `<stmt_list_double>` | { break, case, default, } } |
| 165 | `<else_opt_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 166 | `<else_body_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 167 | `<case_list_double>` | { default, } } |
| 168 | `<default_opt_double>` | { } } |
| 169 | `<ctrl_struct_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 170 | `<stmt_list_char>` | { break, case, default, } } |
| 171 | `<else_opt_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 172 | `<else_body_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 173 | `<case_list_char>` | { default, } } |
| 174 | `<default_opt_char>` | { } } |
| 175 | `<ctrl_struct_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 176 | `<stmt_list_string>` | { break, case, default, } } |
| 177 | `<else_opt_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 178 | `<else_body_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 179 | `<case_list_string>` | { default, } } |
| 180 | `<default_opt_string>` | { } } |
| 181 | `<ctrl_struct_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 182 | `<stmt_list_bool>` | { break, case, default, } } |
| 183 | `<else_opt_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 184 | `<else_body_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 185 | `<case_list_bool>` | { default, } } |
| 186 | `<default_opt_bool>` | { } } |
| 187 | `<ctrl_struct_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 188 | `<stmt_list_array>` | { break, case, default, } } |
| 189 | `<else_opt_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 190 | `<else_body_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 191 | `<case_list_array>` | { default, } } |
| 192 | `<default_opt_array>` | { } } |
| 193 | `<ctrl_struct_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 194 | `<stmt_list_weave>` | { break, case, default, } } |
| 195 | `<else_opt_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 196 | `<else_body_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 197 | `<case_list_weave>` | { default, } } |
| 198 | `<default_opt_weave>` | { } } |
| 199 | `<ctrl_struct_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 200 | `<stmt_list_void>` | { break, case, default, } } |
| 201 | `<else_opt_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 202 | `<else_body_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 203 | `<case_list_void>` | { default, } } |
| 204 | `<default_opt_void>` | { } } |
| 205 | `<int_return_expr>` | { ; } |
| 206 | `<int_ret_assign>` | { ; } |
| 207 | `<int_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 208 | `<int_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 209 | `<int_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 210 | `<int_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 211 | `<int_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 212 | `<int_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 213 | `<int_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 214 | `<int_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 215 | `<int_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 216 | `<long_return_expr>` | { ; } |
| 217 | `<long_ret_assign>` | { ; } |
| 218 | `<long_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 219 | `<long_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 220 | `<long_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 221 | `<long_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 222 | `<long_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 223 | `<long_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 224 | `<long_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 225 | `<long_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 226 | `<long_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 227 | `<float_return_expr>` | { ; } |
| 228 | `<float_ret_assign>` | { ; } |
| 229 | `<float_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 230 | `<float_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 231 | `<float_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 232 | `<float_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 233 | `<float_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 234 | `<float_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 235 | `<float_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 236 | `<float_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 237 | `<float_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 238 | `<double_return_expr>` | { ; } |
| 239 | `<double_ret_assign>` | { ; } |
| 240 | `<double_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 241 | `<double_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 242 | `<double_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 243 | `<double_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 244 | `<double_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 245 | `<double_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 246 | `<double_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 247 | `<double_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 248 | `<double_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 249 | `<char_return_expr>` | { ; } |
| 250 | `<char_ret_assign>` | { ; } |
| 251 | `<char_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 252 | `<char_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 253 | `<char_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 254 | `<char_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 255 | `<char_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 256 | `<char_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 257 | `<char_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 258 | `<char_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 259 | `<char_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 260 | `<string_return_expr>` | { ; } |
| 261 | `<string_ret_assign>` | { ; } |
| 262 | `<string_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 263 | `<string_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 264 | `<string_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 265 | `<string_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 266 | `<string_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 267 | `<string_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 268 | `<string_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 269 | `<string_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 270 | `<string_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 271 | `<bool_return_expr>` | { ; } |
| 272 | `<bool_ret_assign>` | { ; } |
| 273 | `<bool_ret_concat>` | { %=, *=, +=, -=, /=, ;, = } |
| 274 | `<bool_ret_or>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 275 | `<bool_ret_and>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 276 | `<bool_ret_eq>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 277 | `<bool_ret_rel>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 278 | `<bool_ret_add>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 279 | `<bool_ret_mul>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 280 | `<bool_ret_unary>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 281 | `<bool_ret_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 282 | `<using_cont>` | { ; } |
| 283 | `<local_dec_body>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 284 | `<int_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 285 | `<int_local_cont>` | { ; } |
| 286 | `<long_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 287 | `<long_local_cont>` | { ; } |
| 288 | `<float_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 289 | `<float_local_cont>` | { ; } |
| 290 | `<double_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 291 | `<double_local_cont>` | { ; } |
| 292 | `<char_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 293 | `<char_local_cont>` | { ; } |
| 294 | `<string_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 295 | `<string_local_cont>` | { ; } |
| 296 | `<bool_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 297 | `<bool_local_cont>` | { ; } |
| 298 | `<weave_local_tail>` | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 299 | `<statement_non_return>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 300 | `<ctrl_stmt_list>` | { break, case, default, } } |
| 301 | `<effect_stmt>` | { ; } |
| 302 | `<effect_pre_chain>` | { ; } |
| 303 | `<effect_pre_arr_chain>` | { ; } |
| 304 | `<effect_id_cont>` | { ; } |
| 305 | `<effect_post_call>` | { ; } |
| 306 | `<effect_post_call_member>` | { ; } |
| 307 | `<effect_post_call_arr>` | { ; } |
| 308 | `<effect_post_call_arr_cont>` | { ; } |
| 309 | `<effect_post_arr>` | { ; } |
| 310 | `<effect_post_arr_2d>` | { ; } |
| 311 | `<effect_arr_effect>` | { ; } |
| 312 | `<effect_post_member>` | { ; } |
| 313 | `<stmt_assign_expr>` | { ; } |
| 314 | `<stmt_assign_tail>` | { ; } |
| 315 | `<stmt_concat_expr>` | { %=, *=, +=, -=, /=, ;, = } |
| 316 | `<stmt_concat_tail>` | { %=, *=, +=, -=, /=, ;, = } |
| 317 | `<stmt_or_expr>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 318 | `<stmt_or_tail>` | { %=, *=, +=, -=, .., /=, ;, = } |
| 319 | `<stmt_and_expr>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 320 | `<stmt_and_tail>` | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 321 | `<stmt_eq_expr>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 322 | `<stmt_eq_tail>` | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 323 | `<stmt_rel_expr>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 324 | `<stmt_rel_tail>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 325 | `<stmt_add_expr>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 326 | `<stmt_add_tail>` | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 327 | `<stmt_mul_expr>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 328 | `<stmt_mul_tail>` | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 329 | `<stmt_unary_expr>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 330 | `<stmt_postfix_expr>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 331 | `<stmt_id_postfix>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 332 | `<stmt_postfix_chain>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 333 | `<stmt_array_access>` | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 334 | `<stmt_array_access_dim2>` | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 335 | `<stmt_postfix_after_arr>` | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 336 | `<stmt_array_index>` | { ] } |
| 337 | `<stmt_arg_list>` | { ) } |
| 338 | `<stmt_arg_tail>` | { ) } |
| 339 | `<arg_expr>` | { ), , } |
| 340 | `<arg_assign_expr>` | { ), , } |
| 341 | `<arg_assign_tail>` | { ), , } |
| 342 | `<arg_concat_expr>` | { %=, ), *=, +=, ,, -=, /=, = } |
| 343 | `<arg_concat_tail>` | { %=, ), *=, +=, ,, -=, /=, = } |
| 344 | `<arg_or_expr>` | { %=, ), *=, +=, ,, -=, .., /=, = } |
| 345 | `<arg_or_tail>` | { %=, ), *=, +=, ,, -=, .., /=, = } |
| 346 | `<arg_and_expr>` | { %=, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 347 | `<arg_and_tail>` | { %=, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 348 | `<arg_eq_expr>` | { %=, &&, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 349 | `<arg_eq_tail>` | { %=, &&, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 350 | `<arg_rel_expr>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, =, ==, \|\| } |
| 351 | `<arg_rel_tail>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, =, ==, \|\| } |
| 352 | `<arg_add_expr>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 353 | `<arg_add_tail>` | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 354 | `<arg_mul_expr>` | { !=, %=, &&, ), *=, +, +=, ,, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 355 | `<arg_mul_tail>` | { !=, %=, &&, ), *=, +, +=, ,, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 356 | `<arg_unary_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 357 | `<arg_postfix_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 358 | `<arg_id_postfix>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 359 | `<arg_postfix_chain>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 360 | `<arg_array_access>` | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 361 | `<arg_array_access_dim2>` | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 362 | `<arg_postfix_after_arr>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 363 | `<arg_array_index>` | { ] } |
| 364 | `<arg_nested_list>` | { ) } |
| 365 | `<arg_nested_tail>` | { ) } |
| 366 | `<expression>` | { ) } |
| 367 | `<assign_expr>` | { ), ; } |
| 368 | `<assign_tail>` | { ), ; } |
| 369 | `<assign_op>` | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 370 | `<concat_expr>` | { %=, ), *=, +=, -=, /=, ;, = } |
| 371 | `<concat_tail>` | { %=, ), *=, +=, -=, /=, ;, = } |
| 372 | `<or_expr>` | { %=, ), *=, +=, -=, .., /=, ;, = } |
| 373 | `<or_tail>` | { %=, ), *=, +=, -=, .., /=, ;, = } |
| 374 | `<and_expr>` | { %=, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 375 | `<and_tail>` | { %=, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 376 | `<eq_expr>` | { %=, &&, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 377 | `<eq_tail>` | { %=, &&, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 378 | `<rel_expr>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 379 | `<rel_tail>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 380 | `<add_expr>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 381 | `<add_tail>` | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 382 | `<mul_expr>` | { !=, %=, &&, ), *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 383 | `<mul_tail>` | { !=, %=, &&, ), *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 384 | `<unary_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 385 | `<postfix_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 386 | `<id_postfix>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 387 | `<postfix_chain>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 388 | `<array_access>` | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 389 | `<array_access_dim2>` | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 390 | `<postfix_after_arr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 391 | `<array_index>` | { ] } |
| 392 | `<arg_list>` | { ) } |
| 393 | `<arg_tail>` | { ) } |
| 394 | `<io_stmt>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 395 | `<print_args>` | { ) } |
| 396 | `<print_tail>` | { ) } |
| 397 | `<ctrl_struct>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 398 | `<else_opt>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 399 | `<else_body>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 400 | `<case_list>` | { default, } } |
| 401 | `<case_val>` | { : } |
| 402 | `<default_opt>` | { } } |
| 403 | `<break_opt>` | { case, default, } } |
| 404 | `<for_init>` | { ; } |
| 405 | `<for_init_assign_tail>` | { ; } |
| 406 | `<for_init_expr>` | { ; } |
| 407 | `<for_init_type>` | { id } |
| 408 | `<for_cond>` | { ; } |
| 409 | `<for_update>` | { ) } |
| 410 | `<for_update_tail>` | { ) } |
| 411 | `<condition>` | { ), ; } |
| 412 | `<cond_or>` | { ), ; } |
| 413 | `<cond_or_tail>` | { ), ; } |
| 414 | `<cond_and>` | { ), ;, \|\| } |
| 415 | `<cond_and_tail>` | { ), ;, \|\| } |
| 416 | `<cond_comparison>` | { &&, ), ;, \|\| } |
| 417 | `<cond_primary>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 418 | `<cond_primary_continue>` | { &&, ), ;, \|\| } |
| 419 | `<cond_must_commit>` | { &&, ), ;, \|\| } |
| 420 | `<cond_postfix>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 421 | `<cond_cast_arg>` | { ) } |
| 422 | `<cond_id_post>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 423 | `<cond_post_chain>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 424 | `<cond_arr_access>` | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, \|\| } |
| 425 | `<cond_arr_access_dim2>` | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, \|\| } |
| 426 | `<cond_post_after_arr>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 427 | `<cond_arr_index>` | { ] } |
| 428 | `<cond_rhs>` | { &&, ), ;, \|\| } |
| 429 | `<comp_op>` | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 430 | `<main_body>` | { } } |
| 431 | `<main_content>` | { } } |
