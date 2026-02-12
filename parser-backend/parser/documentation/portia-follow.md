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
| 117 | `<mandatory_int_return>` | { } } |
| 118 | `<function_body_long>` | { } } |
| 119 | `<func_content_long>` | { } } |
| 120 | `<mandatory_long_return>` | { } } |
| 121 | `<function_body_float>` | { } } |
| 122 | `<func_content_float>` | { } } |
| 123 | `<mandatory_float_return>` | { } } |
| 124 | `<function_body_double>` | { } } |
| 125 | `<func_content_double>` | { } } |
| 126 | `<mandatory_double_return>` | { } } |
| 127 | `<function_body_char>` | { } } |
| 128 | `<func_content_char>` | { } } |
| 129 | `<mandatory_char_return>` | { } } |
| 130 | `<function_body_string>` | { } } |
| 131 | `<func_content_string>` | { } } |
| 132 | `<mandatory_string_return>` | { } } |
| 133 | `<function_body_bool>` | { } } |
| 134 | `<func_content_bool>` | { } } |
| 135 | `<mandatory_bool_return>` | { } } |
| 136 | `<function_body_array>` | { } } |
| 137 | `<func_content_array>` | { } } |
| 138 | `<mandatory_array_return>` | { } } |
| 139 | `<function_body_weave>` | { } } |
| 140 | `<func_content_weave>` | { } } |
| 141 | `<mandatory_weave_return>` | { } } |
| 142 | `<function_body_void>` | { } } |
| 143 | `<func_content_void>` | { } } |
| 144 | `<mandatory_void_return>` | { } } |
| 145 | `<statement_int>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 146 | `<statement_long>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 147 | `<statement_float>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 148 | `<statement_double>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 149 | `<statement_char>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 150 | `<statement_string>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 151 | `<statement_bool>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 152 | `<statement_array>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 153 | `<statement_weave>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 154 | `<statement_void>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 155 | `<statement_int_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 156 | `<statement_long_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 157 | `<statement_float_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 158 | `<statement_double_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 159 | `<statement_char_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 160 | `<statement_string_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 161 | `<statement_bool_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 162 | `<statement_array_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 163 | `<statement_weave_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 164 | `<statement_void_no_ret>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 165 | `<ctrl_struct_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 166 | `<stmt_list_int>` | { } } |
| 167 | `<non_empty_stmt_list_int>` | { } } |
| 168 | `<loop_statement_int>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 169 | `<loop_stmt_list_int>` | { break, case, default, } } |
| 170 | `<non_empty_loop_stmt_list_int>` | { break, case, default, } } |
| 171 | `<else_opt_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 172 | `<else_body_int>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 173 | `<case_list_int>` | { default, } } |
| 174 | `<default_opt_int>` | { } } |
| 175 | `<ctrl_struct_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 176 | `<stmt_list_long>` | { } } |
| 177 | `<non_empty_stmt_list_long>` | { } } |
| 178 | `<loop_statement_long>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 179 | `<loop_stmt_list_long>` | { break, case, default, } } |
| 180 | `<non_empty_loop_stmt_list_long>` | { break, case, default, } } |
| 181 | `<else_opt_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 182 | `<else_body_long>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 183 | `<case_list_long>` | { default, } } |
| 184 | `<default_opt_long>` | { } } |
| 185 | `<ctrl_struct_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 186 | `<stmt_list_float>` | { } } |
| 187 | `<non_empty_stmt_list_float>` | { } } |
| 188 | `<loop_statement_float>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 189 | `<loop_stmt_list_float>` | { break, case, default, } } |
| 190 | `<non_empty_loop_stmt_list_float>` | { break, case, default, } } |
| 191 | `<else_opt_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 192 | `<else_body_float>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 193 | `<case_list_float>` | { default, } } |
| 194 | `<default_opt_float>` | { } } |
| 195 | `<ctrl_struct_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 196 | `<stmt_list_double>` | { } } |
| 197 | `<non_empty_stmt_list_double>` | { } } |
| 198 | `<loop_statement_double>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 199 | `<loop_stmt_list_double>` | { break, case, default, } } |
| 200 | `<non_empty_loop_stmt_list_double>` | { break, case, default, } } |
| 201 | `<else_opt_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 202 | `<else_body_double>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 203 | `<case_list_double>` | { default, } } |
| 204 | `<default_opt_double>` | { } } |
| 205 | `<ctrl_struct_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 206 | `<stmt_list_char>` | { } } |
| 207 | `<non_empty_stmt_list_char>` | { } } |
| 208 | `<loop_statement_char>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 209 | `<loop_stmt_list_char>` | { break, case, default, } } |
| 210 | `<non_empty_loop_stmt_list_char>` | { break, case, default, } } |
| 211 | `<else_opt_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 212 | `<else_body_char>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 213 | `<case_list_char>` | { default, } } |
| 214 | `<default_opt_char>` | { } } |
| 215 | `<ctrl_struct_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 216 | `<stmt_list_string>` | { } } |
| 217 | `<non_empty_stmt_list_string>` | { } } |
| 218 | `<loop_statement_string>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 219 | `<loop_stmt_list_string>` | { break, case, default, } } |
| 220 | `<non_empty_loop_stmt_list_string>` | { break, case, default, } } |
| 221 | `<else_opt_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 222 | `<else_body_string>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 223 | `<case_list_string>` | { default, } } |
| 224 | `<default_opt_string>` | { } } |
| 225 | `<ctrl_struct_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 226 | `<stmt_list_bool>` | { } } |
| 227 | `<non_empty_stmt_list_bool>` | { } } |
| 228 | `<loop_statement_bool>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 229 | `<loop_stmt_list_bool>` | { break, case, default, } } |
| 230 | `<non_empty_loop_stmt_list_bool>` | { break, case, default, } } |
| 231 | `<else_opt_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 232 | `<else_body_bool>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 233 | `<case_list_bool>` | { default, } } |
| 234 | `<default_opt_bool>` | { } } |
| 235 | `<ctrl_struct_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 236 | `<stmt_list_array>` | { } } |
| 237 | `<non_empty_stmt_list_array>` | { } } |
| 238 | `<loop_statement_array>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 239 | `<loop_stmt_list_array>` | { break, case, default, } } |
| 240 | `<non_empty_loop_stmt_list_array>` | { break, case, default, } } |
| 241 | `<else_opt_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 242 | `<else_body_array>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 243 | `<case_list_array>` | { default, } } |
| 244 | `<default_opt_array>` | { } } |
| 245 | `<ctrl_struct_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 246 | `<stmt_list_weave>` | { } } |
| 247 | `<non_empty_stmt_list_weave>` | { } } |
| 248 | `<loop_statement_weave>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 249 | `<loop_stmt_list_weave>` | { break, case, default, } } |
| 250 | `<non_empty_loop_stmt_list_weave>` | { break, case, default, } } |
| 251 | `<else_opt_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 252 | `<else_body_weave>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 253 | `<case_list_weave>` | { default, } } |
| 254 | `<default_opt_weave>` | { } } |
| 255 | `<ctrl_struct_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 256 | `<stmt_list_void>` | { } } |
| 257 | `<non_empty_stmt_list_void>` | { } } |
| 258 | `<loop_statement_void>` | { ++, --, break, case, default, do, for, id, if, return, switch, thread, threadln, trap, while, } } |
| 259 | `<loop_stmt_list_void>` | { break, case, default, } } |
| 260 | `<non_empty_loop_stmt_list_void>` | { break, case, default, } } |
| 261 | `<else_opt_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 262 | `<else_body_void>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 263 | `<case_list_void>` | { default, } } |
| 264 | `<default_opt_void>` | { } } |
| 265 | `<typed_numeric_ret_expr>` | { ; } |
| 266 | `<typed_string_ret_expr>` | { ; } |
| 267 | `<typed_string_ret_primary>` | { .., ; } |
| 268 | `<typed_bool_ret_expr>` | { ; } |
| 269 | `<typed_bool_ret_primary>` | { !=, &&, ;, ==, || } |
| 270 | `<typed_bool_ret_tail>` | { ; } |
| 271 | `<using_cont>` | { ; } |
| 272 | `<local_dec_body>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 273 | `<int_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 274 | `<int_local_cont>` | { ; } |
| 275 | `<long_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 276 | `<long_local_cont>` | { ; } |
| 277 | `<float_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 278 | `<float_local_cont>` | { ; } |
| 279 | `<double_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 280 | `<double_local_cont>` | { ; } |
| 281 | `<char_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 282 | `<char_local_cont>` | { ; } |
| 283 | `<string_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 284 | `<string_local_cont>` | { ; } |
| 285 | `<bool_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 286 | `<bool_local_cont>` | { ; } |
| 287 | `<weave_local_tail>` | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 288 | `<statement_non_return>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 289 | `<expression>` | { ) } |
| 290 | `<typed_assign_expr>` | { ) } |
| 291 | `<typed_assign_tail>` | { ) } |
| 292 | `<assign_op>` | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 293 | `<typed_rhs_expr>` | { ) } |
| 294 | `<typed_concat_expr>` | { %=, ), *=, +=, -=, /=, = } |
| 295 | `<typed_string_cont>` | { %=, ), *=, +=, -=, /=, ;, = } |
| 296 | `<typed_string_operand>` | { %=, ), *=, +=, -=, .., /=, ;, = } |
| 297 | `<str_operand_id_tail>` | { %=, ), *=, +=, ,, -=, .., /=, ;, =, ] } |
| 298 | `<str_operand_arr_tail>` | { %=, ), *=, +=, ,, -=, .., /=, ;, =, ] } |
| 299 | `<typed_numeric_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 300 | `<typed_arith_ops>` | { !=, %=, &&, ), *=, +=, -=, /=, <, <=, =, ==, >, >=, || } |
| 301 | `<typed_numeric_add_ops>` | { !=, %=, &&, ), *=, +=, -=, /=, <, <=, =, ==, >, >=, || } |
| 302 | `<typed_after_arith>` | { %=, ), *=, +=, -=, /=, = } |
| 303 | `<typed_neg_numeric_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 304 | `<typed_bool_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 305 | `<typed_bool_tail_opt>` | { %=, ), *=, +=, -=, /=, = } |
| 306 | `<typed_bool_or_tail_opt>` | { %=, ), *=, +=, -=, /=, ;, = } |
| 307 | `<typed_bool_term>` | { %=, &&, ), *=, +=, -=, /=, ;, =, || } |
| 308 | `<typed_bool_and_tail>` | { %=, &&, ), *=, +=, -=, /=, ;, =, || } |
| 309 | `<typed_bool_or_tail>` | { %=, ), *=, +=, -=, /=, ;, = } |
| 310 | `<typed_bool_eq>` | { %=, &&, ), *=, +=, -=, /=, ;, =, || } |
| 311 | `<typed_bool_eq_tail>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 312 | `<typed_bool_factor>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 313 | `<typed_bool_atom>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 314 | `<typed_bool_paren>` | { ) } |
| 315 | `<typed_bool_and_or_tail>` | { ) } |
| 316 | `<typed_bool_id_cont>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 317 | `<typed_numeric_arith_cmp>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 318 | `<typed_numeric_add_cmp>` | { !=, <, <=, ==, >, >= } |
| 319 | `<typed_numeric_cmp_required>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 320 | `<typed_numeric_lit_arith>` | { !=, <, <=, ==, >, >= } |
| 321 | `<typed_numeric_neg_cmp>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 322 | `<typed_id_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 323 | `<typed_id_arr_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 324 | `<typed_id_arr2_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 325 | `<typed_id_postfix_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 326 | `<typed_id_field_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 327 | `<typed_id_call_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 328 | `<typed_paren_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 329 | `<typed_paren_after>` | { %=, ), *=, +=, -=, /=, = } |
| 330 | `<typed_paren_arr_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 331 | `<typed_paren_arr2_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 332 | `<typed_paren_postfix_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 333 | `<typed_paren_field_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 334 | `<typed_paren_call_cont>` | { %=, ), *=, +=, -=, /=, = } |
| 335 | `<typed_numeric_add_expr>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 336 | `<typed_numeric_add_tail>` | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 337 | `<typed_numeric_mul_expr>` | { !=, %=, &&, ), *=, +, +=, -, -=, /=, ;, <, <=, =, ==, >, >=, || } |
| 338 | `<typed_numeric_mul_tail>` | { !=, %=, &&, ), *=, +, +=, -, -=, /=, ;, <, <=, =, ==, >, >=, || } |
| 339 | `<typed_numeric_unary_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, /, /=, ;, <, <=, =, ==, >, >=, || } |
| 340 | `<typed_numeric_postfix_expr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, /, /=, ;, <, <=, =, ==, >, >=, || } |
| 341 | `<typed_cmp_op>` | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 342 | `<typed_postfix_chain>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, || } |
| 343 | `<typed_postfix_after_arr>` | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, || } |
| 344 | `<array_index>` | { ] } |
| 345 | `<arg_list>` | { ) } |
| 346 | `<arg_tail>` | { ) } |
| 347 | `<effect_stmt>` | { ; } |
| 348 | `<effect_pre_chain>` | { ; } |
| 349 | `<effect_pre_arr_chain>` | { ; } |
| 350 | `<effect_id_cont>` | { ; } |
| 351 | `<effect_post_call>` | { ; } |
| 352 | `<effect_post_call_member>` | { ; } |
| 353 | `<effect_post_call_arr>` | { ; } |
| 354 | `<effect_post_call_arr_cont>` | { ; } |
| 355 | `<effect_post_arr>` | { ; } |
| 356 | `<effect_post_arr_2d>` | { ; } |
| 357 | `<effect_arr_effect>` | { ; } |
| 358 | `<effect_post_member>` | { ; } |
| 359 | `<stmt_assign_expr>` | { ; } |
| 360 | `<stmt_typed_rhs>` | { ; } |
| 361 | `<stmt_bool_or_concat>` | { ; } |
| 362 | `<stmt_numeric_or_bool>` | { ; } |
| 363 | `<stmt_arith_ops>` | { !=, &&, ), ;, <, <=, ==, >, >=, || } |
| 364 | `<stmt_numeric_add_ops>` | { !=, &&, ), ;, <, <=, ==, >, >=, || } |
| 365 | `<stmt_after_arith>` | { ), ; } |
| 366 | `<stmt_neg_numeric_or_bool>` | { ; } |
| 367 | `<stmt_bool_tail_opt>` | { ), ; } |
| 368 | `<stmt_bool_or_tail_opt>` | { ), ; } |
| 369 | `<stmt_id_toplevel_cont>` | { ; } |
| 370 | `<stmt_id_after_postfix>` | { ; } |
| 371 | `<stmt_paren_typed_content>` | { ), ; } |
| 372 | `<stmt_paren_string_cont>` | { ), ; } |
| 373 | `<stmt_paren_num_start>` | { ), ; } |
| 374 | `<stmt_paren_arith_ops>` | { ), ; } |
| 375 | `<stmt_paren_after_arith>` | { ), ; } |
| 376 | `<stmt_paren_neg_num>` | { ), ; } |
| 377 | `<stmt_paren_num_after_incr>` | { ), ; } |
| 378 | `<stmt_paren_num_cont>` | { ), ; } |
| 379 | `<stmt_paren_bool_tail>` | { ) } |
| 380 | `<stmt_paren_bool_cont>` | { ), ; } |
| 381 | `<stmt_paren_id_cont>` | { ), ; } |
| 382 | `<stmt_paren_postfix_nonnull>` | { !=, %, &&, ), *, +, -, .., /, <, <=, ==, >, >=, || } |
| 383 | `<stmt_paren_id_after_postfix>` | { ), ; } |
| 384 | `<stmt_paren_any_cont>` | { ), ; } |
| 385 | `<stmt_concat_tail_typed>` | { ), ; } |
| 386 | `<stmt_string_operand>` | { ), .., ; } |
| 387 | `<stmt_bool_term>` | { &&, ), ;, || } |
| 388 | `<stmt_bool_and_tail>` | { &&, ), ;, || } |
| 389 | `<stmt_bool_or_tail>` | { ), ; } |
| 390 | `<stmt_bool_eq>` | { &&, ), ;, || } |
| 391 | `<stmt_bool_eq_tail>` | { &&, ), ;, || } |
| 392 | `<stmt_bool_factor>` | { !=, &&, ), ;, ==, || } |
| 393 | `<stmt_bool_atom>` | { !=, &&, ), ;, ==, || } |
| 394 | `<stmt_bool_id_cont>` | { !=, &&, ), ;, ==, || } |
| 395 | `<stmt_numeric_arith_cmp>` | { !=, &&, ), ;, ==, || } |
| 396 | `<stmt_numeric_add_cmp>` | { !=, <, <=, ==, >, >= } |
| 397 | `<stmt_numeric_cmp_required>` | { !=, &&, ), ;, ==, || } |
| 398 | `<stmt_numeric_lit_arith>` | { !=, <, <=, ==, >, >= } |
| 399 | `<stmt_numeric_neg_cmp>` | { !=, &&, ), ;, ==, || } |
| 400 | `<stmt_cmp_op>` | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 401 | `<stmt_bool_paren>` | { ) } |
| 402 | `<stmt_bool_and_or_tail>` | { ) } |
| 403 | `<numeric_mul_expr_stmt>` | { !=, &&, ), +, -, ;, <, <=, ==, >, >=, || } |
| 404 | `<numeric_mul_tail_stmt>` | { !=, &&, ), +, -, ;, <, <=, ==, >, >=, || } |
| 405 | `<numeric_add_expr_stmt>` | { !=, &&, ), ;, ==, || } |
| 406 | `<numeric_add_tail_stmt>` | { !=, &&, ), ;, ==, || } |
| 407 | `<numeric_unary_expr_stmt>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, || } |
| 408 | `<numeric_postfix_expr_stmt>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, || } |
| 409 | `<stmt_id_postfix>` | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, || } |
| 410 | `<stmt_postfix_chain>` | { !=, %, &&, ), *, +, ++, -, --, .., /, ;, <, <=, ==, >, >=, || } |
| 411 | `<stmt_array_access>` | { !=, %, &&, (, ), *, +, ++, -, --, ., .., /, ;, <, <=, ==, >, >=, || } |
| 412 | `<stmt_array_access_dim2>` | { !=, %, &&, (, ), *, +, ++, -, --, ., .., /, ;, <, <=, ==, >, >=, || } |
| 413 | `<stmt_postfix_after_arr>` | { !=, %, &&, ), *, +, ++, -, --, .., /, ;, <, <=, ==, >, >=, || } |
| 414 | `<stmt_array_index>` | { ] } |
| 415 | `<stmt_arg_list>` | { ) } |
| 416 | `<stmt_arg_tail>` | { ) } |
| 417 | `<arg_expr>` | { ), ,, ] } |
| 418 | `<arg_assign_tail>` | { ), ,, ] } |
| 419 | `<arg_typed_rhs>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 420 | `<arg_bool_or_concat>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 421 | `<arg_numeric_or_bool>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 422 | `<arg_arith_ops>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, <, <=, =, ==, >, >=, ], || } |
| 423 | `<arg_numeric_add_ops>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, <, <=, =, ==, >, >=, ], || } |
| 424 | `<arg_after_arith>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 425 | `<arg_neg_numeric_or_bool>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 426 | `<arg_bool_tail_opt>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 427 | `<arg_bool_or_tail_opt>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 428 | `<arg_id_toplevel_cont>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 429 | `<arg_id_after_postfix>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 430 | `<arg_toplevel_paren>` | { ) } |
| 431 | `<arg_toplevel_paren_cont>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 432 | `<arg_concat_tail_typed>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 433 | `<arg_string_operand>` | { %=, ), *=, +=, ,, -=, .., /=, =, ] } |
| 434 | `<arg_bool_term>` | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 435 | `<arg_bool_and_tail>` | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 436 | `<arg_bool_or_tail>` | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 437 | `<arg_bool_eq>` | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 438 | `<arg_bool_eq_tail>` | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 439 | `<arg_bool_factor>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 440 | `<arg_bool_atom>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 441 | `<arg_bool_paren>` | { ) } |
| 442 | `<arg_bool_and_or_tail>` | { ) } |
| 443 | `<arg_bool_id_cont>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 444 | `<arg_numeric_arith_cmp>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 445 | `<arg_numeric_add_cmp>` | { !=, <, <=, ==, >, >= } |
| 446 | `<arg_numeric_cmp_required>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 447 | `<arg_numeric_lit_arith>` | { !=, <, <=, ==, >, >= } |
| 448 | `<arg_numeric_neg_cmp>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 449 | `<arg_cmp_op>` | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 450 | `<numeric_mul_expr_arg>` | { !=, %=, &&, ), *=, +, +=, ,, -, -=, /=, <, <=, =, ==, >, >=, ], || } |
| 451 | `<numeric_mul_tail_arg>` | { !=, %=, &&, ), *=, +, +=, ,, -, -=, /=, <, <=, =, ==, >, >=, ], || } |
| 452 | `<numeric_add_expr_arg>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 453 | `<numeric_add_tail_arg>` | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 454 | `<numeric_unary_expr_arg>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, /, /=, <, <=, =, ==, >, >=, ], || } |
| 455 | `<numeric_postfix_expr_arg>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, /, /=, <, <=, =, ==, >, >=, ], || } |
| 456 | `<arg_id_postfix>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, /, /=, <, <=, =, ==, >, >=, ], || } |
| 457 | `<arg_postfix_chain>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, <, <=, =, ==, >, >=, ], || } |
| 458 | `<arg_array_access>` | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, <, <=, =, ==, >, >=, ], || } |
| 459 | `<arg_array_access_dim2>` | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, <, <=, =, ==, >, >=, ], || } |
| 460 | `<arg_postfix_after_arr>` | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, <, <=, =, ==, >, >=, ], || } |
| 461 | `<arg_array_index>` | { ] } |
| 462 | `<arg_nested_list>` | { ) } |
| 463 | `<arg_nested_tail>` | { ) } |
| 464 | `<io_stmt>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 465 | `<trap_target>` | { ) } |
| 466 | `<trap_target_tail>` | { ) } |
| 467 | `<print_args>` | { ) } |
| 468 | `<print_tail>` | { ) } |
| 469 | `<ctrl_struct>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 470 | `<ctrl_stmt_list>` | { } } |
| 471 | `<non_empty_ctrl_stmt_list>` | { } } |
| 472 | `<loop_statement_non_return>` | { ++, --, break, case, default, do, for, id, if, switch, thread, threadln, trap, while, } } |
| 473 | `<loop_ctrl_stmt_list>` | { break, case, default, } } |
| 474 | `<non_empty_loop_ctrl_stmt_list>` | { break, case, default, } } |
| 475 | `<else_opt>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 476 | `<else_body>` | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 477 | `<case_list>` | { default, } } |
| 478 | `<case_val>` | { : } |
| 479 | `<default_opt>` | { } } |
| 480 | `<break_opt>` | { case, default, } } |
| 481 | `<for_init>` | { ; } |
| 482 | `<for_init_assign_tail>` | { ; } |
| 483 | `<for_init_expr>` | { ; } |
| 484 | `<for_init_type>` | { id } |
| 485 | `<for_cond>` | { ; } |
| 486 | `<condition>` | { ), ; } |
| 487 | `<cond_or>` | { ), ; } |
| 488 | `<cond_or_tail>` | { ), ; } |
| 489 | `<cond_and>` | { ), ;, || } |
| 490 | `<cond_and_tail>` | { ), ;, || } |
| 491 | `<cond_not>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, || } |
| 492 | `<cond_atom>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, || } |
| 493 | `<cond_paren_inner>` | { ) } |
| 494 | `<cond_paren_start>` | { !=, %, &&, ), *, +, ++, -, --, /, <, <=, ==, >, >=, || } |
| 495 | `<cond_paren_cont>` | { ) } |
| 496 | `<cond_paren_arith_ops>` | { !=, ), <, <=, ==, >, >= } |
| 497 | `<cond_paren_mul_ops>` | { !=, ), <, <=, ==, >, >= } |
| 498 | `<cond_paren_unary>` | { !=, %, &&, ), *, +, ++, -, --, /, <, <=, ==, >, >=, || } |
| 499 | `<cond_paren_primary>` | { !=, %, &&, ), *, +, ++, -, --, /, <, <=, ==, >, >=, || } |
| 500 | `<cond_paren_after_arith>` | { ) } |
| 501 | `<cond_paren_logic>` | { ) } |
| 502 | `<cond_paren_tail>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, || } |
| 503 | `<cond_id_cont>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, || } |
| 504 | `<cond_arr_index>` | { ] } |
| 505 | `<cond_id_arr_cont>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, || } |
| 506 | `<cond_id_arr_after>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, || } |
| 507 | `<cond_lit_cmp>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, || } |
| 508 | `<cond_lit_mul>` | { !=, ), +, -, <, <=, ==, >, >= } |
| 509 | `<cond_lit_add>` | { !=, ), <, <=, ==, >, >= } |
| 510 | `<cond_lit_unary>` | { !=, %, ), *, +, -, /, <, <=, ==, >, >= } |
| 511 | `<cond_lit_primary>` | { !=, %, ), *, +, -, /, <, <=, ==, >, >= } |
| 512 | `<cond_lit_expr>` | { ) } |
| 513 | `<cond_rhs>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, ], || } |
| 514 | `<cond_rhs_unary>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, ], || } |
| 515 | `<cond_rhs_primary>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, ], || } |
| 516 | `<cond_rhs_id_tail>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, ], || } |
| 517 | `<cond_rhs_arr_tail>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, ], || } |
| 518 | `<cond_rhs_mul>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, ], || } |
| 519 | `<cond_rhs_add>` | { !=, %, &&, ), *, +, ++, -, --, /, ;, <, <=, ==, >, >=, ], || } |
| 520 | `<cond_cmp>` | { (, ++, -, --, doublelit, floatlit, id, intlit, longlit } |
| 521 | `<for_update>` | { ) } |
| 522 | `<for_update_tail>` | { ) } |
| 523 | `<main_body>` | { } } |
| 524 | `<main_content>` | { } } |