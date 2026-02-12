## FIRST Set

| # | Production | -> | FIRST Set |
|---|------------|-----|-----------|
| 1 | `<program>` | -> | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 2 | `<global_section>` | -> | { global } |
| 3 | `<global_section>` | -> | { int } |
| 4 | `<global_section>` | -> | { long } |
| 5 | `<global_section>` | -> | { float } |
| 6 | `<global_section>` | -> | { double } |
| 7 | `<global_section>` | -> | { char } |
| 8 | `<global_section>` | -> | { string } |
| 9 | `<global_section>` | -> | { bool } |
| 10 | `<global_section>` | -> | { weave } |
| 11 | `<global_section>` | -> | { id } |
| 12 | `<global_section>` | -> | { func } |
| 13 | `<global_section>` | -> | { int } |
| 14 | `<func_and_main>` | -> | { func } |
| 15 | `<func_and_main>` | -> | { int } |
| 16 | `<global_decl>` | -> | { global } |
| 17 | `<global_decl>` | -> | { global } |
| 18 | `<global_decl>` | -> | { global } |
| 19 | `<global_decl>` | -> | { global } |
| 20 | `<global_decl>` | -> | { global } |
| 21 | `<global_decl>` | -> | { global } |
| 22 | `<global_decl>` | -> | { global } |
| 23 | `<function_decl>` | -> | { func } |
| 24 | `<function_decl>` | -> | { func } |
| 25 | `<function_decl>` | -> | { func } |
| 26 | `<function_decl>` | -> | { func } |
| 27 | `<function_decl>` | -> | { func } |
| 28 | `<function_decl>` | -> | { func } |
| 29 | `<function_decl>` | -> | { func } |
| 30 | `<function_decl>` | -> | { func } |
| 31 | `<function_decl>` | -> | { func } |
| 32 | `<bool_lit>` | -> | { true } |
| 33 | `<bool_lit>` | -> | { false } |
| 34 | `<int_global_cont>` | -> | { , } |
| 35 | `<int_global_cont>` | -> | { λ } |
| 36 | `<long_global_cont>` | -> | { , } |
| 37 | `<long_global_cont>` | -> | { λ } |
| 38 | `<float_global_cont>` | -> | { , } |
| 39 | `<float_global_cont>` | -> | { λ } |
| 40 | `<double_global_cont>` | -> | { , } |
| 41 | `<double_global_cont>` | -> | { λ } |
| 42 | `<char_global_cont>` | -> | { , } |
| 43 | `<char_global_cont>` | -> | { λ } |
| 44 | `<string_global_cont>` | -> | { , } |
| 45 | `<string_global_cont>` | -> | { λ } |
| 46 | `<bool_global_cont>` | -> | { , } |
| 47 | `<bool_global_cont>` | -> | { λ } |
| 48 | `<weave_inst_decl>` | -> | { id } |
| 49 | `<weave_inst_decl>` | -> | { [ } |
| 50 | `<weave_inst_tail>` | -> | { = } |
| 51 | `<weave_inst_tail>` | -> | { [ } |
| 52 | `<weave_field_value>` | -> | { intlit } |
| 53 | `<weave_field_value>` | -> | { longlit } |
| 54 | `<weave_field_value>` | -> | { floatlit } |
| 55 | `<weave_field_value>` | -> | { doublelit } |
| 56 | `<weave_field_value>` | -> | { charlit } |
| 57 | `<weave_field_value>` | -> | { stringlit } |
| 58 | `<weave_field_value>` | -> | { true } |
| 59 | `<weave_field_value>` | -> | { false } |
| 60 | `<weave_field_value>` | -> | { { } |
| 61 | `<weave_value_list>` | -> | { charlit, doublelit, false, floatlit, intlit, longlit, stringlit, true, { } |
| 62 | `<weave_value_tail>` | -> | { , } |
| 63 | `<weave_value_tail>` | -> | { λ } |
| 64 | `<weave_field_list_tail>` | -> | { , } |
| 65 | `<weave_field_list_tail>` | -> | { λ } |
| 66 | `<weave_inst_cont>` | -> | { , } |
| 67 | `<weave_inst_cont>` | -> | { λ } |
| 68 | `<weave_arr_cont>` | -> | { , } |
| 69 | `<weave_arr_cont>` | -> | { λ } |
| 70 | `<weave_array_with_init>` | -> | { [ } |
| 71 | `<weave_array_init_tail>` | -> | { [ } |
| 72 | `<weave_array_init_tail>` | -> | { =, λ } |
| 73 | `<weave_arr_init_opt_1d>` | -> | { = } |
| 74 | `<weave_arr_init_opt_1d>` | -> | { λ } |
| 75 | `<weave_arr_init_content_1d>` | -> | { { } |
| 76 | `<weave_init_1d_tail>` | -> | { , } |
| 77 | `<weave_init_1d_tail>` | -> | { λ } |
| 78 | `<weave_arr_init_opt_2d>` | -> | { = } |
| 79 | `<weave_arr_init_opt_2d>` | -> | { λ } |
| 80 | `<weave_arr_init_content_2d>` | -> | { { } |
| 81 | `<weave_init_row>` | -> | { { } |
| 82 | `<weave_init_2d_tail>` | -> | { , } |
| 83 | `<weave_init_2d_tail>` | -> | { λ } |
| 84 | `<mutability>` | -> | { var } |
| 85 | `<mutability>` | -> | { const } |
| 86 | `<array_dims>` | -> | { [ } |
| 87 | `<array_dim2_opt>` | -> | { [ } |
| 88 | `<array_dim2_opt>` | -> | { λ } |
| 89 | `<size>` | -> | { intlit } |
| 90 | `<size>` | -> | { id } |
| 91 | `<int_array_with_init>` | -> | { [ } |
| 92 | `<int_array_init_tail>` | -> | { [ } |
| 93 | `<int_array_init_tail>` | -> | { =, λ } |
| 94 | `<int_arr_init_opt_1d>` | -> | { = } |
| 95 | `<int_arr_init_opt_1d>` | -> | { λ } |
| 96 | `<int_arr_init_content_1d>` | -> | { intlit } |
| 97 | `<int_elem_1d_tail>` | -> | { , } |
| 98 | `<int_elem_1d_tail>` | -> | { λ } |
| 99 | `<int_arr_init_opt_2d>` | -> | { = } |
| 100 | `<int_arr_init_opt_2d>` | -> | { λ } |
| 101 | `<int_arr_init_content_2d>` | -> | { { } |
| 102 | `<int_elem_list>` | -> | { intlit } |
| 103 | `<int_elem_2d_tail>` | -> | { , } |
| 104 | `<int_elem_2d_tail>` | -> | { λ } |
| 105 | `<long_array_with_init>` | -> | { [ } |
| 106 | `<long_array_init_tail>` | -> | { [ } |
| 107 | `<long_array_init_tail>` | -> | { =, λ } |
| 108 | `<long_arr_init_opt_1d>` | -> | { = } |
| 109 | `<long_arr_init_opt_1d>` | -> | { λ } |
| 110 | `<long_arr_init_content_1d>` | -> | { longlit } |
| 111 | `<long_elem_1d_tail>` | -> | { , } |
| 112 | `<long_elem_1d_tail>` | -> | { λ } |
| 113 | `<long_arr_init_opt_2d>` | -> | { = } |
| 114 | `<long_arr_init_opt_2d>` | -> | { λ } |
| 115 | `<long_arr_init_content_2d>` | -> | { { } |
| 116 | `<long_elem_list>` | -> | { longlit } |
| 117 | `<long_elem_2d_tail>` | -> | { , } |
| 118 | `<long_elem_2d_tail>` | -> | { λ } |
| 119 | `<float_array_with_init>` | -> | { [ } |
| 120 | `<float_array_init_tail>` | -> | { [ } |
| 121 | `<float_array_init_tail>` | -> | { =, λ } |
| 122 | `<float_arr_init_opt_1d>` | -> | { = } |
| 123 | `<float_arr_init_opt_1d>` | -> | { λ } |
| 124 | `<float_arr_init_content_1d>` | -> | { floatlit } |
| 125 | `<float_elem_1d_tail>` | -> | { , } |
| 126 | `<float_elem_1d_tail>` | -> | { λ } |
| 127 | `<float_arr_init_opt_2d>` | -> | { = } |
| 128 | `<float_arr_init_opt_2d>` | -> | { λ } |
| 129 | `<float_arr_init_content_2d>` | -> | { { } |
| 130 | `<float_elem_list>` | -> | { floatlit } |
| 131 | `<float_elem_2d_tail>` | -> | { , } |
| 132 | `<float_elem_2d_tail>` | -> | { λ } |
| 133 | `<double_array_with_init>` | -> | { [ } |
| 134 | `<double_array_init_tail>` | -> | { [ } |
| 135 | `<double_array_init_tail>` | -> | { =, λ } |
| 136 | `<double_arr_init_opt_1d>` | -> | { = } |
| 137 | `<double_arr_init_opt_1d>` | -> | { λ } |
| 138 | `<double_arr_init_content_1d>` | -> | { doublelit } |
| 139 | `<double_elem_1d_tail>` | -> | { , } |
| 140 | `<double_elem_1d_tail>` | -> | { λ } |
| 141 | `<double_arr_init_opt_2d>` | -> | { = } |
| 142 | `<double_arr_init_opt_2d>` | -> | { λ } |
| 143 | `<double_arr_init_content_2d>` | -> | { { } |
| 144 | `<double_elem_list>` | -> | { doublelit } |
| 145 | `<double_elem_2d_tail>` | -> | { , } |
| 146 | `<double_elem_2d_tail>` | -> | { λ } |
| 147 | `<char_array_with_init>` | -> | { [ } |
| 148 | `<char_array_init_tail>` | -> | { [ } |
| 149 | `<char_array_init_tail>` | -> | { =, λ } |
| 150 | `<char_arr_init_opt_1d>` | -> | { = } |
| 151 | `<char_arr_init_opt_1d>` | -> | { λ } |
| 152 | `<char_arr_init_content_1d>` | -> | { charlit } |
| 153 | `<char_elem_1d_tail>` | -> | { , } |
| 154 | `<char_elem_1d_tail>` | -> | { λ } |
| 155 | `<char_arr_init_opt_2d>` | -> | { = } |
| 156 | `<char_arr_init_opt_2d>` | -> | { λ } |
| 157 | `<char_arr_init_content_2d>` | -> | { { } |
| 158 | `<char_elem_list>` | -> | { charlit } |
| 159 | `<char_elem_2d_tail>` | -> | { , } |
| 160 | `<char_elem_2d_tail>` | -> | { λ } |
| 161 | `<string_array_with_init>` | -> | { [ } |
| 162 | `<string_array_init_tail>` | -> | { [ } |
| 163 | `<string_array_init_tail>` | -> | { =, λ } |
| 164 | `<string_arr_init_opt_1d>` | -> | { = } |
| 165 | `<string_arr_init_opt_1d>` | -> | { λ } |
| 166 | `<string_arr_init_content_1d>` | -> | { stringlit } |
| 167 | `<string_elem_1d_tail>` | -> | { , } |
| 168 | `<string_elem_1d_tail>` | -> | { λ } |
| 169 | `<string_arr_init_opt_2d>` | -> | { = } |
| 170 | `<string_arr_init_opt_2d>` | -> | { λ } |
| 171 | `<string_arr_init_content_2d>` | -> | { { } |
| 172 | `<string_elem_list>` | -> | { stringlit } |
| 173 | `<string_elem_2d_tail>` | -> | { , } |
| 174 | `<string_elem_2d_tail>` | -> | { λ } |
| 175 | `<bool_array_with_init>` | -> | { [ } |
| 176 | `<bool_array_init_tail>` | -> | { [ } |
| 177 | `<bool_array_init_tail>` | -> | { =, λ } |
| 178 | `<bool_arr_init_opt_1d>` | -> | { = } |
| 179 | `<bool_arr_init_opt_1d>` | -> | { λ } |
| 180 | `<bool_arr_init_content_1d>` | -> | { false, true } |
| 181 | `<bool_elem_1d_tail>` | -> | { , } |
| 182 | `<bool_elem_1d_tail>` | -> | { λ } |
| 183 | `<bool_arr_init_opt_2d>` | -> | { = } |
| 184 | `<bool_arr_init_opt_2d>` | -> | { λ } |
| 185 | `<bool_arr_init_content_2d>` | -> | { { } |
| 186 | `<bool_elem_list>` | -> | { false, true } |
| 187 | `<bool_elem_2d_tail>` | -> | { , } |
| 188 | `<bool_elem_2d_tail>` | -> | { λ } |
| 189 | `<field_list>` | -> | { bool, char, double, float, id, int, long, string } |
| 190 | `<field_list>` | -> | { λ } |
| 191 | `<field_dec>` | -> | { bool, char, double, float, id, int, long, string } |
| 192 | `<field_type>` | -> | { int } |
| 193 | `<field_type>` | -> | { long } |
| 194 | `<field_type>` | -> | { float } |
| 195 | `<field_type>` | -> | { double } |
| 196 | `<field_type>` | -> | { char } |
| 197 | `<field_type>` | -> | { string } |
| 198 | `<field_type>` | -> | { bool } |
| 199 | `<field_type>` | -> | { id } |
| 200 | `<field_arr_opt>` | -> | { [ } |
| 201 | `<field_arr_opt>` | -> | { λ } |
| 202 | `<field_cont>` | -> | { , } |
| 203 | `<field_cont>` | -> | { λ } |
| 204 | `<func_ret_int>` | -> | { id } |
| 205 | `<func_ret_int>` | -> | { [ } |
| 206 | `<func_ret_long>` | -> | { id } |
| 207 | `<func_ret_long>` | -> | { [ } |
| 208 | `<func_ret_float>` | -> | { id } |
| 209 | `<func_ret_float>` | -> | { [ } |
| 210 | `<func_ret_double>` | -> | { id } |
| 211 | `<func_ret_double>` | -> | { [ } |
| 212 | `<func_ret_char>` | -> | { id } |
| 213 | `<func_ret_char>` | -> | { [ } |
| 214 | `<func_ret_string>` | -> | { id } |
| 215 | `<func_ret_string>` | -> | { [ } |
| 216 | `<func_ret_bool>` | -> | { id } |
| 217 | `<func_ret_bool>` | -> | { [ } |
| 218 | `<func_ret_weave>` | -> | { id } |
| 219 | `<func_ret_weave>` | -> | { [ } |
| 220 | `<func_ret_weave>` | -> | { . } |
| 221 | `<param_list>` | -> | { bool, char, double, float, id, int, long, string } |
| 222 | `<param_list>` | -> | { λ } |
| 223 | `<param_type>` | -> | { int } |
| 224 | `<param_type>` | -> | { long } |
| 225 | `<param_type>` | -> | { float } |
| 226 | `<param_type>` | -> | { double } |
| 227 | `<param_type>` | -> | { char } |
| 228 | `<param_type>` | -> | { string } |
| 229 | `<param_type>` | -> | { bool } |
| 230 | `<param_type>` | -> | { id } |
| 231 | `<param_arr_opt>` | -> | { [ } |
| 232 | `<param_arr_opt>` | -> | { λ } |
| 233 | `<param_cont>` | -> | { , } |
| 234 | `<param_cont>` | -> | { λ } |
| 235 | `<function_body_int>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 236 | `<func_content_int>` | -> | { using } |
| 237 | `<func_content_int>` | -> | { local } |
| 238 | `<func_content_int>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 239 | `<func_content_int>` | -> | { return } |
| 240 | `<mandatory_int_return>` | -> | { return } |
| 241 | `<function_body_long>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 242 | `<func_content_long>` | -> | { using } |
| 243 | `<func_content_long>` | -> | { local } |
| 244 | `<func_content_long>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 245 | `<func_content_long>` | -> | { return } |
| 246 | `<mandatory_long_return>` | -> | { return } |
| 247 | `<function_body_float>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 248 | `<func_content_float>` | -> | { using } |
| 249 | `<func_content_float>` | -> | { local } |
| 250 | `<func_content_float>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 251 | `<func_content_float>` | -> | { return } |
| 252 | `<mandatory_float_return>` | -> | { return } |
| 253 | `<function_body_double>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 254 | `<func_content_double>` | -> | { using } |
| 255 | `<func_content_double>` | -> | { local } |
| 256 | `<func_content_double>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 257 | `<func_content_double>` | -> | { return } |
| 258 | `<mandatory_double_return>` | -> | { return } |
| 259 | `<function_body_char>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 260 | `<func_content_char>` | -> | { using } |
| 261 | `<func_content_char>` | -> | { local } |
| 262 | `<func_content_char>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 263 | `<func_content_char>` | -> | { return } |
| 264 | `<mandatory_char_return>` | -> | { return } |
| 265 | `<function_body_string>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 266 | `<func_content_string>` | -> | { using } |
| 267 | `<func_content_string>` | -> | { local } |
| 268 | `<func_content_string>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 269 | `<func_content_string>` | -> | { return } |
| 270 | `<mandatory_string_return>` | -> | { return } |
| 271 | `<function_body_bool>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 272 | `<func_content_bool>` | -> | { using } |
| 273 | `<func_content_bool>` | -> | { local } |
| 274 | `<func_content_bool>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 275 | `<func_content_bool>` | -> | { return } |
| 276 | `<mandatory_bool_return>` | -> | { return } |
| 277 | `<function_body_array>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 278 | `<func_content_array>` | -> | { using } |
| 279 | `<func_content_array>` | -> | { local } |
| 280 | `<func_content_array>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 281 | `<func_content_array>` | -> | { return } |
| 282 | `<mandatory_array_return>` | -> | { return } |
| 283 | `<function_body_weave>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 284 | `<func_content_weave>` | -> | { using } |
| 285 | `<func_content_weave>` | -> | { local } |
| 286 | `<func_content_weave>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 287 | `<func_content_weave>` | -> | { return } |
| 288 | `<mandatory_weave_return>` | -> | { return } |
| 289 | `<function_body_void>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 290 | `<func_content_void>` | -> | { using } |
| 291 | `<func_content_void>` | -> | { local } |
| 292 | `<func_content_void>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 293 | `<func_content_void>` | -> | { return } |
| 294 | `<mandatory_void_return>` | -> | { return } |
| 295 | `<statement_int>` | -> | { ++, --, id } |
| 296 | `<statement_int>` | -> | { thread, threadln, trap } |
| 297 | `<statement_int>` | -> | { do, for, if, switch, while } |
| 298 | `<statement_int>` | -> | { return } |
| 299 | `<statement_long>` | -> | { ++, --, id } |
| 300 | `<statement_long>` | -> | { thread, threadln, trap } |
| 301 | `<statement_long>` | -> | { do, for, if, switch, while } |
| 302 | `<statement_long>` | -> | { return } |
| 303 | `<statement_float>` | -> | { ++, --, id } |
| 304 | `<statement_float>` | -> | { thread, threadln, trap } |
| 305 | `<statement_float>` | -> | { do, for, if, switch, while } |
| 306 | `<statement_float>` | -> | { return } |
| 307 | `<statement_double>` | -> | { ++, --, id } |
| 308 | `<statement_double>` | -> | { thread, threadln, trap } |
| 309 | `<statement_double>` | -> | { do, for, if, switch, while } |
| 310 | `<statement_double>` | -> | { return } |
| 311 | `<statement_char>` | -> | { ++, --, id } |
| 312 | `<statement_char>` | -> | { thread, threadln, trap } |
| 313 | `<statement_char>` | -> | { do, for, if, switch, while } |
| 314 | `<statement_char>` | -> | { return } |
| 315 | `<statement_string>` | -> | { ++, --, id } |
| 316 | `<statement_string>` | -> | { thread, threadln, trap } |
| 317 | `<statement_string>` | -> | { do, for, if, switch, while } |
| 318 | `<statement_string>` | -> | { return } |
| 319 | `<statement_bool>` | -> | { ++, --, id } |
| 320 | `<statement_bool>` | -> | { thread, threadln, trap } |
| 321 | `<statement_bool>` | -> | { do, for, if, switch, while } |
| 322 | `<statement_bool>` | -> | { return } |
| 323 | `<statement_array>` | -> | { ++, --, id } |
| 324 | `<statement_array>` | -> | { thread, threadln, trap } |
| 325 | `<statement_array>` | -> | { do, for, if, switch, while } |
| 326 | `<statement_array>` | -> | { return } |
| 327 | `<statement_weave>` | -> | { ++, --, id } |
| 328 | `<statement_weave>` | -> | { thread, threadln, trap } |
| 329 | `<statement_weave>` | -> | { do, for, if, switch, while } |
| 330 | `<statement_weave>` | -> | { return } |
| 331 | `<statement_void>` | -> | { ++, --, id } |
| 332 | `<statement_void>` | -> | { thread, threadln, trap } |
| 333 | `<statement_void>` | -> | { do, for, if, switch, while } |
| 334 | `<statement_void>` | -> | { return } |
| 335 | `<statement_int_no_ret>` | -> | { ++, --, id } |
| 336 | `<statement_int_no_ret>` | -> | { thread, threadln, trap } |
| 337 | `<statement_int_no_ret>` | -> | { do, for, if, switch, while } |
| 338 | `<statement_long_no_ret>` | -> | { ++, --, id } |
| 339 | `<statement_long_no_ret>` | -> | { thread, threadln, trap } |
| 340 | `<statement_long_no_ret>` | -> | { do, for, if, switch, while } |
| 341 | `<statement_float_no_ret>` | -> | { ++, --, id } |
| 342 | `<statement_float_no_ret>` | -> | { thread, threadln, trap } |
| 343 | `<statement_float_no_ret>` | -> | { do, for, if, switch, while } |
| 344 | `<statement_double_no_ret>` | -> | { ++, --, id } |
| 345 | `<statement_double_no_ret>` | -> | { thread, threadln, trap } |
| 346 | `<statement_double_no_ret>` | -> | { do, for, if, switch, while } |
| 347 | `<statement_char_no_ret>` | -> | { ++, --, id } |
| 348 | `<statement_char_no_ret>` | -> | { thread, threadln, trap } |
| 349 | `<statement_char_no_ret>` | -> | { do, for, if, switch, while } |
| 350 | `<statement_string_no_ret>` | -> | { ++, --, id } |
| 351 | `<statement_string_no_ret>` | -> | { thread, threadln, trap } |
| 352 | `<statement_string_no_ret>` | -> | { do, for, if, switch, while } |
| 353 | `<statement_bool_no_ret>` | -> | { ++, --, id } |
| 354 | `<statement_bool_no_ret>` | -> | { thread, threadln, trap } |
| 355 | `<statement_bool_no_ret>` | -> | { do, for, if, switch, while } |
| 356 | `<statement_array_no_ret>` | -> | { ++, --, id } |
| 357 | `<statement_array_no_ret>` | -> | { thread, threadln, trap } |
| 358 | `<statement_array_no_ret>` | -> | { do, for, if, switch, while } |
| 359 | `<statement_weave_no_ret>` | -> | { ++, --, id } |
| 360 | `<statement_weave_no_ret>` | -> | { thread, threadln, trap } |
| 361 | `<statement_weave_no_ret>` | -> | { do, for, if, switch, while } |
| 362 | `<statement_void_no_ret>` | -> | { ++, --, id } |
| 363 | `<statement_void_no_ret>` | -> | { thread, threadln, trap } |
| 364 | `<statement_void_no_ret>` | -> | { do, for, if, switch, while } |
| 365 | `<ctrl_struct_int>` | -> | { if } |
| 366 | `<ctrl_struct_int>` | -> | { switch } |
| 367 | `<ctrl_struct_int>` | -> | { for } |
| 368 | `<ctrl_struct_int>` | -> | { while } |
| 369 | `<ctrl_struct_int>` | -> | { do } |
| 370 | `<stmt_list_int>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 371 | `<stmt_list_int>` | -> | { λ } |
| 372 | `<non_empty_stmt_list_int>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 373 | `<loop_statement_int>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 374 | `<loop_statement_int>` | -> | { break } |
| 375 | `<loop_stmt_list_int>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 376 | `<loop_stmt_list_int>` | -> | { λ } |
| 377 | `<non_empty_loop_stmt_list_int>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 378 | `<else_opt_int>` | -> | { else } |
| 379 | `<else_opt_int>` | -> | { λ } |
| 380 | `<else_body_int>` | -> | { { } |
| 381 | `<else_body_int>` | -> | { if } |
| 382 | `<case_list_int>` | -> | { case } |
| 383 | `<case_list_int>` | -> | { λ } |
| 384 | `<default_opt_int>` | -> | { default } |
| 385 | `<default_opt_int>` | -> | { λ } |
| 386 | `<ctrl_struct_long>` | -> | { if } |
| 387 | `<ctrl_struct_long>` | -> | { switch } |
| 388 | `<ctrl_struct_long>` | -> | { for } |
| 389 | `<ctrl_struct_long>` | -> | { while } |
| 390 | `<ctrl_struct_long>` | -> | { do } |
| 391 | `<stmt_list_long>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 392 | `<stmt_list_long>` | -> | { λ } |
| 393 | `<non_empty_stmt_list_long>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 394 | `<loop_statement_long>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 395 | `<loop_statement_long>` | -> | { break } |
| 396 | `<loop_stmt_list_long>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 397 | `<loop_stmt_list_long>` | -> | { λ } |
| 398 | `<non_empty_loop_stmt_list_long>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 399 | `<else_opt_long>` | -> | { else } |
| 400 | `<else_opt_long>` | -> | { λ } |
| 401 | `<else_body_long>` | -> | { { } |
| 402 | `<else_body_long>` | -> | { if } |
| 403 | `<case_list_long>` | -> | { case } |
| 404 | `<case_list_long>` | -> | { λ } |
| 405 | `<default_opt_long>` | -> | { default } |
| 406 | `<default_opt_long>` | -> | { λ } |
| 407 | `<ctrl_struct_float>` | -> | { if } |
| 408 | `<ctrl_struct_float>` | -> | { switch } |
| 409 | `<ctrl_struct_float>` | -> | { for } |
| 410 | `<ctrl_struct_float>` | -> | { while } |
| 411 | `<ctrl_struct_float>` | -> | { do } |
| 412 | `<stmt_list_float>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 413 | `<stmt_list_float>` | -> | { λ } |
| 414 | `<non_empty_stmt_list_float>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 415 | `<loop_statement_float>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 416 | `<loop_statement_float>` | -> | { break } |
| 417 | `<loop_stmt_list_float>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 418 | `<loop_stmt_list_float>` | -> | { λ } |
| 419 | `<non_empty_loop_stmt_list_float>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 420 | `<else_opt_float>` | -> | { else } |
| 421 | `<else_opt_float>` | -> | { λ } |
| 422 | `<else_body_float>` | -> | { { } |
| 423 | `<else_body_float>` | -> | { if } |
| 424 | `<case_list_float>` | -> | { case } |
| 425 | `<case_list_float>` | -> | { λ } |
| 426 | `<default_opt_float>` | -> | { default } |
| 427 | `<default_opt_float>` | -> | { λ } |
| 428 | `<ctrl_struct_double>` | -> | { if } |
| 429 | `<ctrl_struct_double>` | -> | { switch } |
| 430 | `<ctrl_struct_double>` | -> | { for } |
| 431 | `<ctrl_struct_double>` | -> | { while } |
| 432 | `<ctrl_struct_double>` | -> | { do } |
| 433 | `<stmt_list_double>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 434 | `<stmt_list_double>` | -> | { λ } |
| 435 | `<non_empty_stmt_list_double>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 436 | `<loop_statement_double>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 437 | `<loop_statement_double>` | -> | { break } |
| 438 | `<loop_stmt_list_double>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 439 | `<loop_stmt_list_double>` | -> | { λ } |
| 440 | `<non_empty_loop_stmt_list_double>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 441 | `<else_opt_double>` | -> | { else } |
| 442 | `<else_opt_double>` | -> | { λ } |
| 443 | `<else_body_double>` | -> | { { } |
| 444 | `<else_body_double>` | -> | { if } |
| 445 | `<case_list_double>` | -> | { case } |
| 446 | `<case_list_double>` | -> | { λ } |
| 447 | `<default_opt_double>` | -> | { default } |
| 448 | `<default_opt_double>` | -> | { λ } |
| 449 | `<ctrl_struct_char>` | -> | { if } |
| 450 | `<ctrl_struct_char>` | -> | { switch } |
| 451 | `<ctrl_struct_char>` | -> | { for } |
| 452 | `<ctrl_struct_char>` | -> | { while } |
| 453 | `<ctrl_struct_char>` | -> | { do } |
| 454 | `<stmt_list_char>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 455 | `<stmt_list_char>` | -> | { λ } |
| 456 | `<non_empty_stmt_list_char>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 457 | `<loop_statement_char>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 458 | `<loop_statement_char>` | -> | { break } |
| 459 | `<loop_stmt_list_char>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 460 | `<loop_stmt_list_char>` | -> | { λ } |
| 461 | `<non_empty_loop_stmt_list_char>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 462 | `<else_opt_char>` | -> | { else } |
| 463 | `<else_opt_char>` | -> | { λ } |
| 464 | `<else_body_char>` | -> | { { } |
| 465 | `<else_body_char>` | -> | { if } |
| 466 | `<case_list_char>` | -> | { case } |
| 467 | `<case_list_char>` | -> | { λ } |
| 468 | `<default_opt_char>` | -> | { default } |
| 469 | `<default_opt_char>` | -> | { λ } |
| 470 | `<ctrl_struct_string>` | -> | { if } |
| 471 | `<ctrl_struct_string>` | -> | { switch } |
| 472 | `<ctrl_struct_string>` | -> | { for } |
| 473 | `<ctrl_struct_string>` | -> | { while } |
| 474 | `<ctrl_struct_string>` | -> | { do } |
| 475 | `<stmt_list_string>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 476 | `<stmt_list_string>` | -> | { λ } |
| 477 | `<non_empty_stmt_list_string>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 478 | `<loop_statement_string>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 479 | `<loop_statement_string>` | -> | { break } |
| 480 | `<loop_stmt_list_string>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 481 | `<loop_stmt_list_string>` | -> | { λ } |
| 482 | `<non_empty_loop_stmt_list_string>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 483 | `<else_opt_string>` | -> | { else } |
| 484 | `<else_opt_string>` | -> | { λ } |
| 485 | `<else_body_string>` | -> | { { } |
| 486 | `<else_body_string>` | -> | { if } |
| 487 | `<case_list_string>` | -> | { case } |
| 488 | `<case_list_string>` | -> | { λ } |
| 489 | `<default_opt_string>` | -> | { default } |
| 490 | `<default_opt_string>` | -> | { λ } |
| 491 | `<ctrl_struct_bool>` | -> | { if } |
| 492 | `<ctrl_struct_bool>` | -> | { switch } |
| 493 | `<ctrl_struct_bool>` | -> | { for } |
| 494 | `<ctrl_struct_bool>` | -> | { while } |
| 495 | `<ctrl_struct_bool>` | -> | { do } |
| 496 | `<stmt_list_bool>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 497 | `<stmt_list_bool>` | -> | { λ } |
| 498 | `<non_empty_stmt_list_bool>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 499 | `<loop_statement_bool>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 500 | `<loop_statement_bool>` | -> | { break } |
| 501 | `<loop_stmt_list_bool>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 502 | `<loop_stmt_list_bool>` | -> | { λ } |
| 503 | `<non_empty_loop_stmt_list_bool>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 504 | `<else_opt_bool>` | -> | { else } |
| 505 | `<else_opt_bool>` | -> | { λ } |
| 506 | `<else_body_bool>` | -> | { { } |
| 507 | `<else_body_bool>` | -> | { if } |
| 508 | `<case_list_bool>` | -> | { case } |
| 509 | `<case_list_bool>` | -> | { λ } |
| 510 | `<default_opt_bool>` | -> | { default } |
| 511 | `<default_opt_bool>` | -> | { λ } |
| 512 | `<ctrl_struct_array>` | -> | { if } |
| 513 | `<ctrl_struct_array>` | -> | { switch } |
| 514 | `<ctrl_struct_array>` | -> | { for } |
| 515 | `<ctrl_struct_array>` | -> | { while } |
| 516 | `<ctrl_struct_array>` | -> | { do } |
| 517 | `<stmt_list_array>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 518 | `<stmt_list_array>` | -> | { λ } |
| 519 | `<non_empty_stmt_list_array>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 520 | `<loop_statement_array>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 521 | `<loop_statement_array>` | -> | { break } |
| 522 | `<loop_stmt_list_array>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 523 | `<loop_stmt_list_array>` | -> | { λ } |
| 524 | `<non_empty_loop_stmt_list_array>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 525 | `<else_opt_array>` | -> | { else } |
| 526 | `<else_opt_array>` | -> | { λ } |
| 527 | `<else_body_array>` | -> | { { } |
| 528 | `<else_body_array>` | -> | { if } |
| 529 | `<case_list_array>` | -> | { case } |
| 530 | `<case_list_array>` | -> | { λ } |
| 531 | `<default_opt_array>` | -> | { default } |
| 532 | `<default_opt_array>` | -> | { λ } |
| 533 | `<ctrl_struct_weave>` | -> | { if } |
| 534 | `<ctrl_struct_weave>` | -> | { switch } |
| 535 | `<ctrl_struct_weave>` | -> | { for } |
| 536 | `<ctrl_struct_weave>` | -> | { while } |
| 537 | `<ctrl_struct_weave>` | -> | { do } |
| 538 | `<stmt_list_weave>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 539 | `<stmt_list_weave>` | -> | { λ } |
| 540 | `<non_empty_stmt_list_weave>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 541 | `<loop_statement_weave>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 542 | `<loop_statement_weave>` | -> | { break } |
| 543 | `<loop_stmt_list_weave>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 544 | `<loop_stmt_list_weave>` | -> | { λ } |
| 545 | `<non_empty_loop_stmt_list_weave>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 546 | `<else_opt_weave>` | -> | { else } |
| 547 | `<else_opt_weave>` | -> | { λ } |
| 548 | `<else_body_weave>` | -> | { { } |
| 549 | `<else_body_weave>` | -> | { if } |
| 550 | `<case_list_weave>` | -> | { case } |
| 551 | `<case_list_weave>` | -> | { λ } |
| 552 | `<default_opt_weave>` | -> | { default } |
| 553 | `<default_opt_weave>` | -> | { λ } |
| 554 | `<ctrl_struct_void>` | -> | { if } |
| 555 | `<ctrl_struct_void>` | -> | { switch } |
| 556 | `<ctrl_struct_void>` | -> | { for } |
| 557 | `<ctrl_struct_void>` | -> | { while } |
| 558 | `<ctrl_struct_void>` | -> | { do } |
| 559 | `<stmt_list_void>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 560 | `<stmt_list_void>` | -> | { λ } |
| 561 | `<non_empty_stmt_list_void>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 562 | `<loop_statement_void>` | -> | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 563 | `<loop_statement_void>` | -> | { break } |
| 564 | `<loop_stmt_list_void>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 565 | `<loop_stmt_list_void>` | -> | { λ } |
| 566 | `<non_empty_loop_stmt_list_void>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 567 | `<else_opt_void>` | -> | { else } |
| 568 | `<else_opt_void>` | -> | { λ } |
| 569 | `<else_body_void>` | -> | { { } |
| 570 | `<else_body_void>` | -> | { if } |
| 571 | `<case_list_void>` | -> | { case } |
| 572 | `<case_list_void>` | -> | { λ } |
| 573 | `<default_opt_void>` | -> | { default } |
| 574 | `<default_opt_void>` | -> | { λ } |
| 575 | `<typed_numeric_ret_expr>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 576 | `<typed_string_ret_expr>` | -> | { (, char, charlit, id, string, stringlit } |
| 577 | `<typed_string_ret_primary>` | -> | { stringlit } |
| 578 | `<typed_string_ret_primary>` | -> | { charlit } |
| 579 | `<typed_string_ret_primary>` | -> | { id } |
| 580 | `<typed_string_ret_primary>` | -> | { string } |
| 581 | `<typed_string_ret_primary>` | -> | { char } |
| 582 | `<typed_string_ret_primary>` | -> | { ( } |
| 583 | `<typed_bool_ret_expr>` | -> | { !, (, -, bool, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 584 | `<typed_bool_ret_primary>` | -> | { true } |
| 585 | `<typed_bool_ret_primary>` | -> | { false } |
| 586 | `<typed_bool_ret_primary>` | -> | { ! } |
| 587 | `<typed_bool_ret_primary>` | -> | { id } |
| 588 | `<typed_bool_ret_primary>` | -> | { ( } |
| 589 | `<typed_bool_ret_primary>` | -> | { bool } |
| 590 | `<typed_bool_ret_primary>` | -> | { intlit } |
| 591 | `<typed_bool_ret_primary>` | -> | { longlit } |
| 592 | `<typed_bool_ret_primary>` | -> | { floatlit } |
| 593 | `<typed_bool_ret_primary>` | -> | { doublelit } |
| 594 | `<typed_bool_ret_primary>` | -> | { - } |
| 595 | `<typed_bool_ret_primary>` | -> | { int } |
| 596 | `<typed_bool_ret_primary>` | -> | { long } |
| 597 | `<typed_bool_ret_primary>` | -> | { float } |
| 598 | `<typed_bool_ret_primary>` | -> | { double } |
| 599 | `<typed_bool_ret_tail>` | -> | { && } |
| 600 | `<typed_bool_ret_tail>` | -> | { \|\| } |
| 601 | `<typed_bool_ret_tail>` | -> | { == } |
| 602 | `<typed_bool_ret_tail>` | -> | { != } |
| 603 | `<typed_bool_ret_tail>` | -> | { λ } |
| 604 | `<using_cont>` | -> | { , } |
| 605 | `<using_cont>` | -> | { λ } |
| 606 | `<local_dec_body>` | -> | { int } |
| 607 | `<local_dec_body>` | -> | { long } |
| 608 | `<local_dec_body>` | -> | { float } |
| 609 | `<local_dec_body>` | -> | { double } |
| 610 | `<local_dec_body>` | -> | { char } |
| 611 | `<local_dec_body>` | -> | { string } |
| 612 | `<local_dec_body>` | -> | { bool } |
| 613 | `<local_dec_body>` | -> | { id } |
| 614 | `<int_local_tail>` | -> | { [ } |
| 615 | `<int_local_tail>` | -> | { = } |
| 616 | `<int_local_cont>` | -> | { , } |
| 617 | `<int_local_cont>` | -> | { λ } |
| 618 | `<long_local_tail>` | -> | { [ } |
| 619 | `<long_local_tail>` | -> | { = } |
| 620 | `<long_local_cont>` | -> | { , } |
| 621 | `<long_local_cont>` | -> | { λ } |
| 622 | `<float_local_tail>` | -> | { [ } |
| 623 | `<float_local_tail>` | -> | { = } |
| 624 | `<float_local_cont>` | -> | { , } |
| 625 | `<float_local_cont>` | -> | { λ } |
| 626 | `<double_local_tail>` | -> | { [ } |
| 627 | `<double_local_tail>` | -> | { = } |
| 628 | `<double_local_cont>` | -> | { , } |
| 629 | `<double_local_cont>` | -> | { λ } |
| 630 | `<char_local_tail>` | -> | { [ } |
| 631 | `<char_local_tail>` | -> | { = } |
| 632 | `<char_local_cont>` | -> | { , } |
| 633 | `<char_local_cont>` | -> | { λ } |
| 634 | `<string_local_tail>` | -> | { [ } |
| 635 | `<string_local_tail>` | -> | { = } |
| 636 | `<string_local_cont>` | -> | { , } |
| 637 | `<string_local_cont>` | -> | { λ } |
| 638 | `<bool_local_tail>` | -> | { [ } |
| 639 | `<bool_local_tail>` | -> | { = } |
| 640 | `<bool_local_cont>` | -> | { , } |
| 641 | `<bool_local_cont>` | -> | { λ } |
| 642 | `<weave_local_tail>` | -> | { = } |
| 643 | `<weave_local_tail>` | -> | { [ } |
| 644 | `<statement_non_return>` | -> | { ++, --, id } |
| 645 | `<statement_non_return>` | -> | { thread, threadln, trap } |
| 646 | `<statement_non_return>` | -> | { do, for, if, switch, while } |
| 647 | `<expression>` | -> | { !, (, -, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 648 | `<typed_assign_expr>` | -> | { !, (, -, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 649 | `<typed_assign_tail>` | -> | { = } |
| 650 | `<typed_assign_tail>` | -> | { += } |
| 651 | `<typed_assign_tail>` | -> | { -= } |
| 652 | `<typed_assign_tail>` | -> | { *= } |
| 653 | `<typed_assign_tail>` | -> | { /= } |
| 654 | `<typed_assign_tail>` | -> | { %= } |
| 655 | `<typed_assign_tail>` | -> | { λ } |
| 656 | `<assign_op>` | -> | { = } |
| 657 | `<assign_op>` | -> | { += } |
| 658 | `<assign_op>` | -> | { -= } |
| 659 | `<assign_op>` | -> | { *= } |
| 660 | `<assign_op>` | -> | { /= } |
| 661 | `<assign_op>` | -> | { %= } |
| 662 | `<typed_rhs_expr>` | -> | { !, (, -, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 663 | `<typed_concat_expr>` | -> | { stringlit } |
| 664 | `<typed_concat_expr>` | -> | { charlit } |
| 665 | `<typed_concat_expr>` | -> | { intlit } |
| 666 | `<typed_concat_expr>` | -> | { longlit } |
| 667 | `<typed_concat_expr>` | -> | { floatlit } |
| 668 | `<typed_concat_expr>` | -> | { doublelit } |
| 669 | `<typed_concat_expr>` | -> | { true } |
| 670 | `<typed_concat_expr>` | -> | { false } |
| 671 | `<typed_concat_expr>` | -> | { ! } |
| 672 | `<typed_concat_expr>` | -> | { - } |
| 673 | `<typed_concat_expr>` | -> | { id } |
| 674 | `<typed_concat_expr>` | -> | { ( } |
| 675 | `<typed_concat_expr>` | -> | { int } |
| 676 | `<typed_concat_expr>` | -> | { long } |
| 677 | `<typed_concat_expr>` | -> | { float } |
| 678 | `<typed_concat_expr>` | -> | { double } |
| 679 | `<typed_concat_expr>` | -> | { char } |
| 680 | `<typed_concat_expr>` | -> | { string } |
| 681 | `<typed_concat_expr>` | -> | { bool } |
| 682 | `<typed_string_cont>` | -> | { .. } |
| 683 | `<typed_string_cont>` | -> | { λ } |
| 684 | `<typed_string_operand>` | -> | { stringlit } |
| 685 | `<typed_string_operand>` | -> | { charlit } |
| 686 | `<typed_string_operand>` | -> | { id } |
| 687 | `<typed_string_operand>` | -> | { string } |
| 688 | `<typed_string_operand>` | -> | { char } |
| 689 | `<typed_string_operand>` | -> | { ( } |
| 690 | `<typed_string_operand>` | -> | { intlit } |
| 691 | `<typed_string_operand>` | -> | { longlit } |
| 692 | `<typed_string_operand>` | -> | { floatlit } |
| 693 | `<typed_string_operand>` | -> | { doublelit } |
| 694 | `<typed_string_operand>` | -> | { true } |
| 695 | `<typed_string_operand>` | -> | { false } |
| 696 | `<typed_string_operand>` | -> | { int } |
| 697 | `<typed_string_operand>` | -> | { long } |
| 698 | `<typed_string_operand>` | -> | { float } |
| 699 | `<typed_string_operand>` | -> | { double } |
| 700 | `<typed_string_operand>` | -> | { bool } |
| 701 | `<str_operand_id_tail>` | -> | { . } |
| 702 | `<str_operand_id_tail>` | -> | { [ } |
| 703 | `<str_operand_id_tail>` | -> | { ( } |
| 704 | `<str_operand_id_tail>` | -> | { λ } |
| 705 | `<str_operand_arr_tail>` | -> | { . } |
| 706 | `<str_operand_arr_tail>` | -> | { [ } |
| 707 | `<str_operand_arr_tail>` | -> | { λ } |
| 708 | `<typed_numeric_cont>` | -> | { %, *, +, -, / } |
| 709 | `<typed_numeric_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 710 | `<typed_numeric_cont>` | -> | { &&, \|\|, λ } |
| 711 | `<typed_arith_ops>` | -> | { + } |
| 712 | `<typed_arith_ops>` | -> | { - } |
| 713 | `<typed_arith_ops>` | -> | { * } |
| 714 | `<typed_arith_ops>` | -> | { / } |
| 715 | `<typed_arith_ops>` | -> | { % } |
| 716 | `<typed_numeric_add_ops>` | -> | { + } |
| 717 | `<typed_numeric_add_ops>` | -> | { - } |
| 718 | `<typed_numeric_add_ops>` | -> | { λ } |
| 719 | `<typed_after_arith>` | -> | { !=, <, <=, ==, >, >= } |
| 720 | `<typed_after_arith>` | -> | { &&, \|\|, λ } |
| 721 | `<typed_neg_numeric_cont>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 722 | `<typed_bool_cont>` | -> | { &&, \|\|, λ } |
| 723 | `<typed_bool_tail_opt>` | -> | { && } |
| 724 | `<typed_bool_tail_opt>` | -> | { \|\| } |
| 725 | `<typed_bool_tail_opt>` | -> | { λ } |
| 726 | `<typed_bool_or_tail_opt>` | -> | { \|\| } |
| 727 | `<typed_bool_or_tail_opt>` | -> | { λ } |
| 728 | `<typed_bool_term>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 729 | `<typed_bool_and_tail>` | -> | { && } |
| 730 | `<typed_bool_and_tail>` | -> | { λ } |
| 731 | `<typed_bool_or_tail>` | -> | { \|\| } |
| 732 | `<typed_bool_or_tail>` | -> | { λ } |
| 733 | `<typed_bool_eq>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 734 | `<typed_bool_eq_tail>` | -> | { == } |
| 735 | `<typed_bool_eq_tail>` | -> | { != } |
| 736 | `<typed_bool_eq_tail>` | -> | { λ } |
| 737 | `<typed_bool_factor>` | -> | { ! } |
| 738 | `<typed_bool_factor>` | -> | { (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 739 | `<typed_bool_atom>` | -> | { true } |
| 740 | `<typed_bool_atom>` | -> | { false } |
| 741 | `<typed_bool_atom>` | -> | { id } |
| 742 | `<typed_bool_atom>` | -> | { intlit } |
| 743 | `<typed_bool_atom>` | -> | { longlit } |
| 744 | `<typed_bool_atom>` | -> | { floatlit } |
| 745 | `<typed_bool_atom>` | -> | { doublelit } |
| 746 | `<typed_bool_atom>` | -> | { - } |
| 747 | `<typed_bool_atom>` | -> | { ( } |
| 748 | `<typed_bool_atom>` | -> | { int } |
| 749 | `<typed_bool_atom>` | -> | { long } |
| 750 | `<typed_bool_atom>` | -> | { float } |
| 751 | `<typed_bool_atom>` | -> | { double } |
| 752 | `<typed_bool_paren>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 753 | `<typed_bool_and_or_tail>` | -> | { && } |
| 754 | `<typed_bool_and_or_tail>` | -> | { \|\| } |
| 755 | `<typed_bool_and_or_tail>` | -> | { λ } |
| 756 | `<typed_bool_id_cont>` | -> | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 757 | `<typed_bool_id_cont>` | -> | { (, ++, --, ., [, λ } |
| 758 | `<typed_numeric_arith_cmp>` | -> | { + } |
| 759 | `<typed_numeric_arith_cmp>` | -> | { - } |
| 760 | `<typed_numeric_arith_cmp>` | -> | { * } |
| 761 | `<typed_numeric_arith_cmp>` | -> | { / } |
| 762 | `<typed_numeric_arith_cmp>` | -> | { % } |
| 763 | `<typed_numeric_arith_cmp>` | -> | { !=, <, <=, ==, >, >= } |
| 764 | `<typed_numeric_add_cmp>` | -> | { + } |
| 765 | `<typed_numeric_add_cmp>` | -> | { - } |
| 766 | `<typed_numeric_add_cmp>` | -> | { λ } |
| 767 | `<typed_numeric_cmp_required>` | -> | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 768 | `<typed_numeric_lit_arith>` | -> | { * } |
| 769 | `<typed_numeric_lit_arith>` | -> | { / } |
| 770 | `<typed_numeric_lit_arith>` | -> | { % } |
| 771 | `<typed_numeric_lit_arith>` | -> | { + } |
| 772 | `<typed_numeric_lit_arith>` | -> | { - } |
| 773 | `<typed_numeric_lit_arith>` | -> | { λ } |
| 774 | `<typed_numeric_neg_cmp>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 775 | `<typed_id_cont>` | -> | { %, *, +, -, / } |
| 776 | `<typed_id_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 777 | `<typed_id_cont>` | -> | { ++ } |
| 778 | `<typed_id_cont>` | -> | { -- } |
| 779 | `<typed_id_cont>` | -> | { [ } |
| 780 | `<typed_id_cont>` | -> | { . } |
| 781 | `<typed_id_cont>` | -> | { ( } |
| 782 | `<typed_id_cont>` | -> | { .. } |
| 783 | `<typed_id_cont>` | -> | { &&, \|\|, λ } |
| 784 | `<typed_id_arr_cont>` | -> | { [ } |
| 785 | `<typed_id_arr_cont>` | -> | { !=, %, &&, (, *, +, -, ., .., /, <, <=, ==, >, >=, \|\|, λ } |
| 786 | `<typed_id_arr2_cont>` | -> | { !=, %, &&, (, *, +, -, ., .., /, <, <=, ==, >, >=, \|\|, λ } |
| 787 | `<typed_id_postfix_cont>` | -> | { . } |
| 788 | `<typed_id_postfix_cont>` | -> | { ( } |
| 789 | `<typed_id_postfix_cont>` | -> | { %, *, +, -, / } |
| 790 | `<typed_id_postfix_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 791 | `<typed_id_postfix_cont>` | -> | { .. } |
| 792 | `<typed_id_postfix_cont>` | -> | { &&, \|\|, λ } |
| 793 | `<typed_id_field_cont>` | -> | { [ } |
| 794 | `<typed_id_field_cont>` | -> | { . } |
| 795 | `<typed_id_field_cont>` | -> | { ( } |
| 796 | `<typed_id_field_cont>` | -> | { %, *, +, -, / } |
| 797 | `<typed_id_field_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 798 | `<typed_id_field_cont>` | -> | { .. } |
| 799 | `<typed_id_field_cont>` | -> | { &&, \|\|, λ } |
| 800 | `<typed_id_call_cont>` | -> | { [ } |
| 801 | `<typed_id_call_cont>` | -> | { . } |
| 802 | `<typed_id_call_cont>` | -> | { ( } |
| 803 | `<typed_id_call_cont>` | -> | { %, *, +, -, / } |
| 804 | `<typed_id_call_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 805 | `<typed_id_call_cont>` | -> | { .. } |
| 806 | `<typed_id_call_cont>` | -> | { &&, \|\|, λ } |
| 807 | `<typed_paren_cont>` | -> | { !, (, -, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 808 | `<typed_paren_after>` | -> | { %, *, +, -, / } |
| 809 | `<typed_paren_after>` | -> | { !=, <, <=, ==, >, >= } |
| 810 | `<typed_paren_after>` | -> | { .. } |
| 811 | `<typed_paren_after>` | -> | { [ } |
| 812 | `<typed_paren_after>` | -> | { . } |
| 813 | `<typed_paren_after>` | -> | { ( } |
| 814 | `<typed_paren_after>` | -> | { &&, \|\|, λ } |
| 815 | `<typed_paren_arr_cont>` | -> | { [ } |
| 816 | `<typed_paren_arr_cont>` | -> | { !=, %, (, *, +, -, ., /, <, <=, ==, >, >=, λ } |
| 817 | `<typed_paren_arr2_cont>` | -> | { !=, %, (, *, +, -, ., /, <, <=, ==, >, >=, λ } |
| 818 | `<typed_paren_postfix_cont>` | -> | { . } |
| 819 | `<typed_paren_postfix_cont>` | -> | { ( } |
| 820 | `<typed_paren_postfix_cont>` | -> | { %, *, +, -, / } |
| 821 | `<typed_paren_postfix_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 822 | `<typed_paren_postfix_cont>` | -> | { λ } |
| 823 | `<typed_paren_field_cont>` | -> | { [ } |
| 824 | `<typed_paren_field_cont>` | -> | { . } |
| 825 | `<typed_paren_field_cont>` | -> | { ( } |
| 826 | `<typed_paren_field_cont>` | -> | { %, *, +, -, / } |
| 827 | `<typed_paren_field_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 828 | `<typed_paren_field_cont>` | -> | { λ } |
| 829 | `<typed_paren_call_cont>` | -> | { [ } |
| 830 | `<typed_paren_call_cont>` | -> | { . } |
| 831 | `<typed_paren_call_cont>` | -> | { ( } |
| 832 | `<typed_paren_call_cont>` | -> | { %, *, +, -, / } |
| 833 | `<typed_paren_call_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 834 | `<typed_paren_call_cont>` | -> | { λ } |
| 835 | `<typed_numeric_add_expr>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 836 | `<typed_numeric_add_tail>` | -> | { + } |
| 837 | `<typed_numeric_add_tail>` | -> | { - } |
| 838 | `<typed_numeric_add_tail>` | -> | { λ } |
| 839 | `<typed_numeric_mul_expr>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 840 | `<typed_numeric_mul_tail>` | -> | { * } |
| 841 | `<typed_numeric_mul_tail>` | -> | { / } |
| 842 | `<typed_numeric_mul_tail>` | -> | { % } |
| 843 | `<typed_numeric_mul_tail>` | -> | { λ } |
| 844 | `<typed_numeric_unary_expr>` | -> | { ! } |
| 845 | `<typed_numeric_unary_expr>` | -> | { - } |
| 846 | `<typed_numeric_unary_expr>` | -> | { ++ } |
| 847 | `<typed_numeric_unary_expr>` | -> | { -- } |
| 848 | `<typed_numeric_unary_expr>` | -> | { (, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 849 | `<typed_numeric_postfix_expr>` | -> | { intlit } |
| 850 | `<typed_numeric_postfix_expr>` | -> | { longlit } |
| 851 | `<typed_numeric_postfix_expr>` | -> | { floatlit } |
| 852 | `<typed_numeric_postfix_expr>` | -> | { doublelit } |
| 853 | `<typed_numeric_postfix_expr>` | -> | { id } |
| 854 | `<typed_numeric_postfix_expr>` | -> | { ( } |
| 855 | `<typed_numeric_postfix_expr>` | -> | { int } |
| 856 | `<typed_numeric_postfix_expr>` | -> | { long } |
| 857 | `<typed_numeric_postfix_expr>` | -> | { float } |
| 858 | `<typed_numeric_postfix_expr>` | -> | { double } |
| 859 | `<typed_cmp_op>` | -> | { < } |
| 860 | `<typed_cmp_op>` | -> | { > } |
| 861 | `<typed_cmp_op>` | -> | { <= } |
| 862 | `<typed_cmp_op>` | -> | { >= } |
| 863 | `<typed_cmp_op>` | -> | { == } |
| 864 | `<typed_cmp_op>` | -> | { != } |
| 865 | `<typed_postfix_chain>` | -> | { [ } |
| 866 | `<typed_postfix_chain>` | -> | { . } |
| 867 | `<typed_postfix_chain>` | -> | { ( } |
| 868 | `<typed_postfix_chain>` | -> | { ++ } |
| 869 | `<typed_postfix_chain>` | -> | { -- } |
| 870 | `<typed_postfix_chain>` | -> | { λ } |
| 871 | `<typed_postfix_after_arr>` | -> | { [ } |
| 872 | `<typed_postfix_after_arr>` | -> | { . } |
| 873 | `<typed_postfix_after_arr>` | -> | { ( } |
| 874 | `<typed_postfix_after_arr>` | -> | { ++ } |
| 875 | `<typed_postfix_after_arr>` | -> | { -- } |
| 876 | `<typed_postfix_after_arr>` | -> | { λ } |
| 877 | `<array_index>` | -> | { intlit } |
| 878 | `<array_index>` | -> | { id } |
| 879 | `<arg_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 880 | `<arg_list>` | -> | { λ } |
| 881 | `<arg_tail>` | -> | { , } |
| 882 | `<arg_tail>` | -> | { λ } |
| 883 | `<effect_stmt>` | -> | { ++ } |
| 884 | `<effect_stmt>` | -> | { -- } |
| 885 | `<effect_stmt>` | -> | { id } |
| 886 | `<effect_pre_chain>` | -> | { [ } |
| 887 | `<effect_pre_chain>` | -> | { . } |
| 888 | `<effect_pre_chain>` | -> | { λ } |
| 889 | `<effect_pre_arr_chain>` | -> | { [ } |
| 890 | `<effect_pre_arr_chain>` | -> | { . } |
| 891 | `<effect_pre_arr_chain>` | -> | { λ } |
| 892 | `<effect_id_cont>` | -> | { = } |
| 893 | `<effect_id_cont>` | -> | { += } |
| 894 | `<effect_id_cont>` | -> | { -= } |
| 895 | `<effect_id_cont>` | -> | { *= } |
| 896 | `<effect_id_cont>` | -> | { /= } |
| 897 | `<effect_id_cont>` | -> | { %= } |
| 898 | `<effect_id_cont>` | -> | { ++ } |
| 899 | `<effect_id_cont>` | -> | { -- } |
| 900 | `<effect_id_cont>` | -> | { ( } |
| 901 | `<effect_id_cont>` | -> | { [ } |
| 902 | `<effect_id_cont>` | -> | { . } |
| 903 | `<effect_post_call>` | -> | { . } |
| 904 | `<effect_post_call>` | -> | { [ } |
| 905 | `<effect_post_call>` | -> | { λ } |
| 906 | `<effect_post_call_member>` | -> | { ( } |
| 907 | `<effect_post_call_member>` | -> | { [ } |
| 908 | `<effect_post_call_member>` | -> | { . } |
| 909 | `<effect_post_call_member>` | -> | { λ } |
| 910 | `<effect_post_call_arr>` | -> | { [ } |
| 911 | `<effect_post_call_arr>` | -> | { (, ., λ } |
| 912 | `<effect_post_call_arr_cont>` | -> | { . } |
| 913 | `<effect_post_call_arr_cont>` | -> | { ( } |
| 914 | `<effect_post_call_arr_cont>` | -> | { λ } |
| 915 | `<effect_post_arr>` | -> | { [ } |
| 916 | `<effect_post_arr>` | -> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 917 | `<effect_post_arr_2d>` | -> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 918 | `<effect_arr_effect>` | -> | { = } |
| 919 | `<effect_arr_effect>` | -> | { += } |
| 920 | `<effect_arr_effect>` | -> | { -= } |
| 921 | `<effect_arr_effect>` | -> | { *= } |
| 922 | `<effect_arr_effect>` | -> | { /= } |
| 923 | `<effect_arr_effect>` | -> | { %= } |
| 924 | `<effect_arr_effect>` | -> | { ++ } |
| 925 | `<effect_arr_effect>` | -> | { -- } |
| 926 | `<effect_arr_effect>` | -> | { ( } |
| 927 | `<effect_arr_effect>` | -> | { . } |
| 928 | `<effect_post_member>` | -> | { = } |
| 929 | `<effect_post_member>` | -> | { += } |
| 930 | `<effect_post_member>` | -> | { -= } |
| 931 | `<effect_post_member>` | -> | { *= } |
| 932 | `<effect_post_member>` | -> | { /= } |
| 933 | `<effect_post_member>` | -> | { %= } |
| 934 | `<effect_post_member>` | -> | { ++ } |
| 935 | `<effect_post_member>` | -> | { -- } |
| 936 | `<effect_post_member>` | -> | { ( } |
| 937 | `<effect_post_member>` | -> | { [ } |
| 938 | `<effect_post_member>` | -> | { . } |
| 939 | `<stmt_assign_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 940 | `<stmt_typed_rhs>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 941 | `<stmt_bool_or_concat>` | -> | { stringlit } |
| 942 | `<stmt_bool_or_concat>` | -> | { charlit } |
| 943 | `<stmt_bool_or_concat>` | -> | { string } |
| 944 | `<stmt_bool_or_concat>` | -> | { intlit } |
| 945 | `<stmt_bool_or_concat>` | -> | { longlit } |
| 946 | `<stmt_bool_or_concat>` | -> | { floatlit } |
| 947 | `<stmt_bool_or_concat>` | -> | { doublelit } |
| 948 | `<stmt_bool_or_concat>` | -> | { - } |
| 949 | `<stmt_bool_or_concat>` | -> | { true } |
| 950 | `<stmt_bool_or_concat>` | -> | { false } |
| 951 | `<stmt_bool_or_concat>` | -> | { ! } |
| 952 | `<stmt_bool_or_concat>` | -> | { int } |
| 953 | `<stmt_bool_or_concat>` | -> | { long } |
| 954 | `<stmt_bool_or_concat>` | -> | { float } |
| 955 | `<stmt_bool_or_concat>` | -> | { double } |
| 956 | `<stmt_bool_or_concat>` | -> | { char } |
| 957 | `<stmt_bool_or_concat>` | -> | { bool } |
| 958 | `<stmt_bool_or_concat>` | -> | { id } |
| 959 | `<stmt_bool_or_concat>` | -> | { ( } |
| 960 | `<stmt_bool_or_concat>` | -> | { ++ } |
| 961 | `<stmt_bool_or_concat>` | -> | { -- } |
| 962 | `<stmt_numeric_or_bool>` | -> | { %, *, +, -, / } |
| 963 | `<stmt_numeric_or_bool>` | -> | { !=, <, <=, ==, >, >= } |
| 964 | `<stmt_numeric_or_bool>` | -> | { &&, \|\|, λ } |
| 965 | `<stmt_arith_ops>` | -> | { + } |
| 966 | `<stmt_arith_ops>` | -> | { - } |
| 967 | `<stmt_arith_ops>` | -> | { * } |
| 968 | `<stmt_arith_ops>` | -> | { / } |
| 969 | `<stmt_arith_ops>` | -> | { % } |
| 970 | `<stmt_numeric_add_ops>` | -> | { + } |
| 971 | `<stmt_numeric_add_ops>` | -> | { - } |
| 972 | `<stmt_numeric_add_ops>` | -> | { λ } |
| 973 | `<stmt_after_arith>` | -> | { !=, <, <=, ==, >, >= } |
| 974 | `<stmt_after_arith>` | -> | { &&, \|\|, λ } |
| 975 | `<stmt_neg_numeric_or_bool>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 976 | `<stmt_bool_tail_opt>` | -> | { && } |
| 977 | `<stmt_bool_tail_opt>` | -> | { \|\| } |
| 978 | `<stmt_bool_tail_opt>` | -> | { λ } |
| 979 | `<stmt_bool_or_tail_opt>` | -> | { \|\| } |
| 980 | `<stmt_bool_or_tail_opt>` | -> | { λ } |
| 981 | `<stmt_id_toplevel_cont>` | -> | { %, *, +, -, / } |
| 982 | `<stmt_id_toplevel_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 983 | `<stmt_id_toplevel_cont>` | -> | { ++ } |
| 984 | `<stmt_id_toplevel_cont>` | -> | { -- } |
| 985 | `<stmt_id_toplevel_cont>` | -> | { !=, %, &&, (, *, +, ++, -, --, ., .., /, <, <=, ==, >, >=, [, \|\|, λ } |
| 986 | `<stmt_id_after_postfix>` | -> | { %, *, +, -, / } |
| 987 | `<stmt_id_after_postfix>` | -> | { !=, <, <=, ==, >, >= } |
| 988 | `<stmt_id_after_postfix>` | -> | { .. } |
| 989 | `<stmt_id_after_postfix>` | -> | { ++ } |
| 990 | `<stmt_id_after_postfix>` | -> | { -- } |
| 991 | `<stmt_id_after_postfix>` | -> | { &&, \|\|, λ } |
| 992 | `<stmt_paren_typed_content>` | -> | { stringlit } |
| 993 | `<stmt_paren_typed_content>` | -> | { charlit } |
| 994 | `<stmt_paren_typed_content>` | -> | { string } |
| 995 | `<stmt_paren_typed_content>` | -> | { char } |
| 996 | `<stmt_paren_typed_content>` | -> | { intlit } |
| 997 | `<stmt_paren_typed_content>` | -> | { longlit } |
| 998 | `<stmt_paren_typed_content>` | -> | { floatlit } |
| 999 | `<stmt_paren_typed_content>` | -> | { doublelit } |
| 1000 | `<stmt_paren_typed_content>` | -> | { - } |
| 1001 | `<stmt_paren_typed_content>` | -> | { int } |
| 1002 | `<stmt_paren_typed_content>` | -> | { long } |
| 1003 | `<stmt_paren_typed_content>` | -> | { float } |
| 1004 | `<stmt_paren_typed_content>` | -> | { double } |
| 1005 | `<stmt_paren_typed_content>` | -> | { true } |
| 1006 | `<stmt_paren_typed_content>` | -> | { false } |
| 1007 | `<stmt_paren_typed_content>` | -> | { ! } |
| 1008 | `<stmt_paren_typed_content>` | -> | { bool } |
| 1009 | `<stmt_paren_typed_content>` | -> | { id } |
| 1010 | `<stmt_paren_typed_content>` | -> | { ( } |
| 1011 | `<stmt_paren_typed_content>` | -> | { ++ } |
| 1012 | `<stmt_paren_typed_content>` | -> | { -- } |
| 1013 | `<stmt_paren_string_cont>` | -> | { .. } |
| 1014 | `<stmt_paren_string_cont>` | -> | { λ } |
| 1015 | `<stmt_paren_num_start>` | -> | { %, *, +, -, / } |
| 1016 | `<stmt_paren_num_start>` | -> | { !=, <, <=, ==, >, >= } |
| 1017 | `<stmt_paren_num_start>` | -> | { ) } |
| 1018 | `<stmt_paren_arith_ops>` | -> | { + } |
| 1019 | `<stmt_paren_arith_ops>` | -> | { - } |
| 1020 | `<stmt_paren_arith_ops>` | -> | { * } |
| 1021 | `<stmt_paren_arith_ops>` | -> | { / } |
| 1022 | `<stmt_paren_arith_ops>` | -> | { % } |
| 1023 | `<stmt_paren_after_arith>` | -> | { !=, <, <=, ==, >, >= } |
| 1024 | `<stmt_paren_after_arith>` | -> | { ) } |
| 1025 | `<stmt_paren_neg_num>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1026 | `<stmt_paren_num_after_incr>` | -> | { %, *, +, -, / } |
| 1027 | `<stmt_paren_num_after_incr>` | -> | { !=, <, <=, ==, >, >= } |
| 1028 | `<stmt_paren_num_after_incr>` | -> | { ) } |
| 1029 | `<stmt_paren_num_cont>` | -> | { %, *, +, -, / } |
| 1030 | `<stmt_paren_num_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 1031 | `<stmt_paren_num_cont>` | -> | { &&, \|\|, λ } |
| 1032 | `<stmt_paren_bool_tail>` | -> | { && } |
| 1033 | `<stmt_paren_bool_tail>` | -> | { \|\| } |
| 1034 | `<stmt_paren_bool_tail>` | -> | { λ } |
| 1035 | `<stmt_paren_bool_cont>` | -> | { && } |
| 1036 | `<stmt_paren_bool_cont>` | -> | { \|\| } |
| 1037 | `<stmt_paren_bool_cont>` | -> | { λ } |
| 1038 | `<stmt_paren_id_cont>` | -> | { %, *, +, -, / } |
| 1039 | `<stmt_paren_id_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 1040 | `<stmt_paren_id_cont>` | -> | { (, ., [ } |
| 1041 | `<stmt_paren_id_cont>` | -> | { ++ } |
| 1042 | `<stmt_paren_id_cont>` | -> | { -- } |
| 1043 | `<stmt_paren_id_cont>` | -> | { && } |
| 1044 | `<stmt_paren_id_cont>` | -> | { \|\| } |
| 1045 | `<stmt_paren_id_cont>` | -> | { ) } |
| 1046 | `<stmt_paren_postfix_nonnull>` | -> | { [ } |
| 1047 | `<stmt_paren_postfix_nonnull>` | -> | { . } |
| 1048 | `<stmt_paren_postfix_nonnull>` | -> | { ( } |
| 1049 | `<stmt_paren_id_after_postfix>` | -> | { %, *, +, -, / } |
| 1050 | `<stmt_paren_id_after_postfix>` | -> | { !=, <, <=, ==, >, >= } |
| 1051 | `<stmt_paren_id_after_postfix>` | -> | { .. } |
| 1052 | `<stmt_paren_id_after_postfix>` | -> | { && } |
| 1053 | `<stmt_paren_id_after_postfix>` | -> | { \|\| } |
| 1054 | `<stmt_paren_id_after_postfix>` | -> | { ) } |
| 1055 | `<stmt_paren_any_cont>` | -> | { %, *, +, -, / } |
| 1056 | `<stmt_paren_any_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 1057 | `<stmt_paren_any_cont>` | -> | { .. } |
| 1058 | `<stmt_paren_any_cont>` | -> | { &&, \|\|, λ } |
| 1059 | `<stmt_concat_tail_typed>` | -> | { .. } |
| 1060 | `<stmt_concat_tail_typed>` | -> | { λ } |
| 1061 | `<stmt_string_operand>` | -> | { stringlit } |
| 1062 | `<stmt_string_operand>` | -> | { charlit } |
| 1063 | `<stmt_string_operand>` | -> | { id } |
| 1064 | `<stmt_string_operand>` | -> | { string } |
| 1065 | `<stmt_string_operand>` | -> | { char } |
| 1066 | `<stmt_string_operand>` | -> | { ( } |
| 1067 | `<stmt_string_operand>` | -> | { intlit } |
| 1068 | `<stmt_string_operand>` | -> | { longlit } |
| 1069 | `<stmt_string_operand>` | -> | { floatlit } |
| 1070 | `<stmt_string_operand>` | -> | { doublelit } |
| 1071 | `<stmt_string_operand>` | -> | { true } |
| 1072 | `<stmt_string_operand>` | -> | { false } |
| 1073 | `<stmt_string_operand>` | -> | { int } |
| 1074 | `<stmt_string_operand>` | -> | { long } |
| 1075 | `<stmt_string_operand>` | -> | { float } |
| 1076 | `<stmt_string_operand>` | -> | { double } |
| 1077 | `<stmt_string_operand>` | -> | { bool } |
| 1078 | `<stmt_bool_term>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1079 | `<stmt_bool_and_tail>` | -> | { && } |
| 1080 | `<stmt_bool_and_tail>` | -> | { λ } |
| 1081 | `<stmt_bool_or_tail>` | -> | { \|\| } |
| 1082 | `<stmt_bool_or_tail>` | -> | { λ } |
| 1083 | `<stmt_bool_eq>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1084 | `<stmt_bool_eq_tail>` | -> | { == } |
| 1085 | `<stmt_bool_eq_tail>` | -> | { != } |
| 1086 | `<stmt_bool_eq_tail>` | -> | { λ } |
| 1087 | `<stmt_bool_factor>` | -> | { ! } |
| 1088 | `<stmt_bool_factor>` | -> | { (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1089 | `<stmt_bool_atom>` | -> | { true } |
| 1090 | `<stmt_bool_atom>` | -> | { false } |
| 1091 | `<stmt_bool_atom>` | -> | { id } |
| 1092 | `<stmt_bool_atom>` | -> | { intlit } |
| 1093 | `<stmt_bool_atom>` | -> | { longlit } |
| 1094 | `<stmt_bool_atom>` | -> | { floatlit } |
| 1095 | `<stmt_bool_atom>` | -> | { doublelit } |
| 1096 | `<stmt_bool_atom>` | -> | { - } |
| 1097 | `<stmt_bool_atom>` | -> | { ( } |
| 1098 | `<stmt_bool_atom>` | -> | { int } |
| 1099 | `<stmt_bool_atom>` | -> | { long } |
| 1100 | `<stmt_bool_atom>` | -> | { float } |
| 1101 | `<stmt_bool_atom>` | -> | { double } |
| 1102 | `<stmt_bool_id_cont>` | -> | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1103 | `<stmt_bool_id_cont>` | -> | { ++ } |
| 1104 | `<stmt_bool_id_cont>` | -> | { -- } |
| 1105 | `<stmt_bool_id_cont>` | -> | { (, ., [, λ } |
| 1106 | `<stmt_numeric_arith_cmp>` | -> | { + } |
| 1107 | `<stmt_numeric_arith_cmp>` | -> | { - } |
| 1108 | `<stmt_numeric_arith_cmp>` | -> | { * } |
| 1109 | `<stmt_numeric_arith_cmp>` | -> | { / } |
| 1110 | `<stmt_numeric_arith_cmp>` | -> | { % } |
| 1111 | `<stmt_numeric_arith_cmp>` | -> | { !=, <, <=, ==, >, >= } |
| 1112 | `<stmt_numeric_add_cmp>` | -> | { + } |
| 1113 | `<stmt_numeric_add_cmp>` | -> | { - } |
| 1114 | `<stmt_numeric_add_cmp>` | -> | { λ } |
| 1115 | `<stmt_numeric_cmp_required>` | -> | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1116 | `<stmt_numeric_lit_arith>` | -> | { * } |
| 1117 | `<stmt_numeric_lit_arith>` | -> | { / } |
| 1118 | `<stmt_numeric_lit_arith>` | -> | { % } |
| 1119 | `<stmt_numeric_lit_arith>` | -> | { + } |
| 1120 | `<stmt_numeric_lit_arith>` | -> | { - } |
| 1121 | `<stmt_numeric_lit_arith>` | -> | { λ } |
| 1122 | `<stmt_numeric_neg_cmp>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1123 | `<stmt_cmp_op>` | -> | { < } |
| 1124 | `<stmt_cmp_op>` | -> | { > } |
| 1125 | `<stmt_cmp_op>` | -> | { <= } |
| 1126 | `<stmt_cmp_op>` | -> | { >= } |
| 1127 | `<stmt_cmp_op>` | -> | { == } |
| 1128 | `<stmt_cmp_op>` | -> | { != } |
| 1129 | `<stmt_bool_paren>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1130 | `<stmt_bool_and_or_tail>` | -> | { && } |
| 1131 | `<stmt_bool_and_or_tail>` | -> | { \|\| } |
| 1132 | `<stmt_bool_and_or_tail>` | -> | { λ } |
| 1133 | `<numeric_mul_expr_stmt>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1134 | `<numeric_mul_tail_stmt>` | -> | { * } |
| 1135 | `<numeric_mul_tail_stmt>` | -> | { / } |
| 1136 | `<numeric_mul_tail_stmt>` | -> | { % } |
| 1137 | `<numeric_mul_tail_stmt>` | -> | { λ } |
| 1138 | `<numeric_add_expr_stmt>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1139 | `<numeric_add_tail_stmt>` | -> | { + } |
| 1140 | `<numeric_add_tail_stmt>` | -> | { - } |
| 1141 | `<numeric_add_tail_stmt>` | -> | { λ } |
| 1142 | `<numeric_unary_expr_stmt>` | -> | { ! } |
| 1143 | `<numeric_unary_expr_stmt>` | -> | { - } |
| 1144 | `<numeric_unary_expr_stmt>` | -> | { (, ++, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1145 | `<numeric_postfix_expr_stmt>` | -> | { ( } |
| 1146 | `<numeric_postfix_expr_stmt>` | -> | { int } |
| 1147 | `<numeric_postfix_expr_stmt>` | -> | { long } |
| 1148 | `<numeric_postfix_expr_stmt>` | -> | { float } |
| 1149 | `<numeric_postfix_expr_stmt>` | -> | { double } |
| 1150 | `<numeric_postfix_expr_stmt>` | -> | { ++ } |
| 1151 | `<numeric_postfix_expr_stmt>` | -> | { -- } |
| 1152 | `<numeric_postfix_expr_stmt>` | -> | { id } |
| 1153 | `<numeric_postfix_expr_stmt>` | -> | { intlit } |
| 1154 | `<numeric_postfix_expr_stmt>` | -> | { longlit } |
| 1155 | `<numeric_postfix_expr_stmt>` | -> | { floatlit } |
| 1156 | `<numeric_postfix_expr_stmt>` | -> | { doublelit } |
| 1157 | `<stmt_id_postfix>` | -> | { ++ } |
| 1158 | `<stmt_id_postfix>` | -> | { -- } |
| 1159 | `<stmt_id_postfix>` | -> | { (, ., [, λ } |
| 1160 | `<stmt_postfix_chain>` | -> | { [ } |
| 1161 | `<stmt_postfix_chain>` | -> | { . } |
| 1162 | `<stmt_postfix_chain>` | -> | { ( } |
| 1163 | `<stmt_postfix_chain>` | -> | { λ } |
| 1164 | `<stmt_array_access>` | -> | { [ } |
| 1165 | `<stmt_array_access_dim2>` | -> | { [ } |
| 1166 | `<stmt_array_access_dim2>` | -> | { λ } |
| 1167 | `<stmt_postfix_after_arr>` | -> | { . } |
| 1168 | `<stmt_postfix_after_arr>` | -> | { ( } |
| 1169 | `<stmt_postfix_after_arr>` | -> | { ++ } |
| 1170 | `<stmt_postfix_after_arr>` | -> | { -- } |
| 1171 | `<stmt_postfix_after_arr>` | -> | { λ } |
| 1172 | `<stmt_array_index>` | -> | { intlit } |
| 1173 | `<stmt_array_index>` | -> | { id } |
| 1174 | `<stmt_arg_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1175 | `<stmt_arg_list>` | -> | { λ } |
| 1176 | `<stmt_arg_tail>` | -> | { , } |
| 1177 | `<stmt_arg_tail>` | -> | { λ } |
| 1178 | `<arg_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1179 | `<arg_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 1180 | `<arg_assign_tail>` | -> | { λ } |
| 1181 | `<arg_typed_rhs>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1182 | `<arg_bool_or_concat>` | -> | { stringlit } |
| 1183 | `<arg_bool_or_concat>` | -> | { charlit } |
| 1184 | `<arg_bool_or_concat>` | -> | { string } |
| 1185 | `<arg_bool_or_concat>` | -> | { intlit } |
| 1186 | `<arg_bool_or_concat>` | -> | { longlit } |
| 1187 | `<arg_bool_or_concat>` | -> | { floatlit } |
| 1188 | `<arg_bool_or_concat>` | -> | { doublelit } |
| 1189 | `<arg_bool_or_concat>` | -> | { - } |
| 1190 | `<arg_bool_or_concat>` | -> | { true } |
| 1191 | `<arg_bool_or_concat>` | -> | { false } |
| 1192 | `<arg_bool_or_concat>` | -> | { ! } |
| 1193 | `<arg_bool_or_concat>` | -> | { int } |
| 1194 | `<arg_bool_or_concat>` | -> | { long } |
| 1195 | `<arg_bool_or_concat>` | -> | { float } |
| 1196 | `<arg_bool_or_concat>` | -> | { double } |
| 1197 | `<arg_bool_or_concat>` | -> | { char } |
| 1198 | `<arg_bool_or_concat>` | -> | { bool } |
| 1199 | `<arg_bool_or_concat>` | -> | { id } |
| 1200 | `<arg_bool_or_concat>` | -> | { ( } |
| 1201 | `<arg_bool_or_concat>` | -> | { ++ } |
| 1202 | `<arg_bool_or_concat>` | -> | { -- } |
| 1203 | `<arg_numeric_or_bool>` | -> | { %, *, +, -, / } |
| 1204 | `<arg_numeric_or_bool>` | -> | { !=, <, <=, ==, >, >= } |
| 1205 | `<arg_numeric_or_bool>` | -> | { &&, \|\|, λ } |
| 1206 | `<arg_arith_ops>` | -> | { + } |
| 1207 | `<arg_arith_ops>` | -> | { - } |
| 1208 | `<arg_arith_ops>` | -> | { * } |
| 1209 | `<arg_arith_ops>` | -> | { / } |
| 1210 | `<arg_arith_ops>` | -> | { % } |
| 1211 | `<arg_numeric_add_ops>` | -> | { + } |
| 1212 | `<arg_numeric_add_ops>` | -> | { - } |
| 1213 | `<arg_numeric_add_ops>` | -> | { λ } |
| 1214 | `<arg_after_arith>` | -> | { !=, <, <=, ==, >, >= } |
| 1215 | `<arg_after_arith>` | -> | { &&, \|\|, λ } |
| 1216 | `<arg_neg_numeric_or_bool>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1217 | `<arg_bool_tail_opt>` | -> | { && } |
| 1218 | `<arg_bool_tail_opt>` | -> | { \|\| } |
| 1219 | `<arg_bool_tail_opt>` | -> | { λ } |
| 1220 | `<arg_bool_or_tail_opt>` | -> | { \|\| } |
| 1221 | `<arg_bool_or_tail_opt>` | -> | { λ } |
| 1222 | `<arg_id_toplevel_cont>` | -> | { %, *, +, -, / } |
| 1223 | `<arg_id_toplevel_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 1224 | `<arg_id_toplevel_cont>` | -> | { ++ } |
| 1225 | `<arg_id_toplevel_cont>` | -> | { -- } |
| 1226 | `<arg_id_toplevel_cont>` | -> | { !=, %, &&, (, *, +, -, ., .., /, <, <=, ==, >, >=, [, \|\|, λ } |
| 1227 | `<arg_id_after_postfix>` | -> | { %, *, +, -, / } |
| 1228 | `<arg_id_after_postfix>` | -> | { !=, <, <=, ==, >, >= } |
| 1229 | `<arg_id_after_postfix>` | -> | { .. } |
| 1230 | `<arg_id_after_postfix>` | -> | { &&, \|\|, λ } |
| 1231 | `<arg_toplevel_paren>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1232 | `<arg_toplevel_paren_cont>` | -> | { %, *, +, -, / } |
| 1233 | `<arg_toplevel_paren_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 1234 | `<arg_toplevel_paren_cont>` | -> | { .. } |
| 1235 | `<arg_toplevel_paren_cont>` | -> | { &&, \|\|, λ } |
| 1236 | `<arg_concat_tail_typed>` | -> | { .. } |
| 1237 | `<arg_concat_tail_typed>` | -> | { λ } |
| 1238 | `<arg_string_operand>` | -> | { stringlit } |
| 1239 | `<arg_string_operand>` | -> | { charlit } |
| 1240 | `<arg_string_operand>` | -> | { id } |
| 1241 | `<arg_string_operand>` | -> | { string } |
| 1242 | `<arg_string_operand>` | -> | { char } |
| 1243 | `<arg_string_operand>` | -> | { ( } |
| 1244 | `<arg_bool_term>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1245 | `<arg_bool_and_tail>` | -> | { && } |
| 1246 | `<arg_bool_and_tail>` | -> | { λ } |
| 1247 | `<arg_bool_or_tail>` | -> | { \|\| } |
| 1248 | `<arg_bool_or_tail>` | -> | { λ } |
| 1249 | `<arg_bool_eq>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1250 | `<arg_bool_eq_tail>` | -> | { == } |
| 1251 | `<arg_bool_eq_tail>` | -> | { != } |
| 1252 | `<arg_bool_eq_tail>` | -> | { λ } |
| 1253 | `<arg_bool_factor>` | -> | { ! } |
| 1254 | `<arg_bool_factor>` | -> | { (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1255 | `<arg_bool_atom>` | -> | { true } |
| 1256 | `<arg_bool_atom>` | -> | { false } |
| 1257 | `<arg_bool_atom>` | -> | { id } |
| 1258 | `<arg_bool_atom>` | -> | { intlit } |
| 1259 | `<arg_bool_atom>` | -> | { longlit } |
| 1260 | `<arg_bool_atom>` | -> | { floatlit } |
| 1261 | `<arg_bool_atom>` | -> | { doublelit } |
| 1262 | `<arg_bool_atom>` | -> | { - } |
| 1263 | `<arg_bool_atom>` | -> | { ( } |
| 1264 | `<arg_bool_atom>` | -> | { int } |
| 1265 | `<arg_bool_atom>` | -> | { long } |
| 1266 | `<arg_bool_atom>` | -> | { float } |
| 1267 | `<arg_bool_atom>` | -> | { double } |
| 1268 | `<arg_bool_paren>` | -> | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1269 | `<arg_bool_and_or_tail>` | -> | { && } |
| 1270 | `<arg_bool_and_or_tail>` | -> | { \|\| } |
| 1271 | `<arg_bool_and_or_tail>` | -> | { λ } |
| 1272 | `<arg_bool_id_cont>` | -> | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1273 | `<arg_bool_id_cont>` | -> | { ++ } |
| 1274 | `<arg_bool_id_cont>` | -> | { -- } |
| 1275 | `<arg_bool_id_cont>` | -> | { (, ., [, λ } |
| 1276 | `<arg_numeric_arith_cmp>` | -> | { + } |
| 1277 | `<arg_numeric_arith_cmp>` | -> | { - } |
| 1278 | `<arg_numeric_arith_cmp>` | -> | { * } |
| 1279 | `<arg_numeric_arith_cmp>` | -> | { / } |
| 1280 | `<arg_numeric_arith_cmp>` | -> | { % } |
| 1281 | `<arg_numeric_arith_cmp>` | -> | { !=, <, <=, ==, >, >= } |
| 1282 | `<arg_numeric_add_cmp>` | -> | { + } |
| 1283 | `<arg_numeric_add_cmp>` | -> | { - } |
| 1284 | `<arg_numeric_add_cmp>` | -> | { λ } |
| 1285 | `<arg_numeric_cmp_required>` | -> | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1286 | `<arg_numeric_lit_arith>` | -> | { * } |
| 1287 | `<arg_numeric_lit_arith>` | -> | { / } |
| 1288 | `<arg_numeric_lit_arith>` | -> | { % } |
| 1289 | `<arg_numeric_lit_arith>` | -> | { + } |
| 1290 | `<arg_numeric_lit_arith>` | -> | { - } |
| 1291 | `<arg_numeric_lit_arith>` | -> | { λ } |
| 1292 | `<arg_numeric_neg_cmp>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1293 | `<arg_cmp_op>` | -> | { < } |
| 1294 | `<arg_cmp_op>` | -> | { > } |
| 1295 | `<arg_cmp_op>` | -> | { <= } |
| 1296 | `<arg_cmp_op>` | -> | { >= } |
| 1297 | `<arg_cmp_op>` | -> | { == } |
| 1298 | `<arg_cmp_op>` | -> | { != } |
| 1299 | `<numeric_mul_expr_arg>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1300 | `<numeric_mul_tail_arg>` | -> | { * } |
| 1301 | `<numeric_mul_tail_arg>` | -> | { / } |
| 1302 | `<numeric_mul_tail_arg>` | -> | { % } |
| 1303 | `<numeric_mul_tail_arg>` | -> | { λ } |
| 1304 | `<numeric_add_expr_arg>` | -> | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1305 | `<numeric_add_tail_arg>` | -> | { + } |
| 1306 | `<numeric_add_tail_arg>` | -> | { - } |
| 1307 | `<numeric_add_tail_arg>` | -> | { λ } |
| 1308 | `<numeric_unary_expr_arg>` | -> | { ! } |
| 1309 | `<numeric_unary_expr_arg>` | -> | { - } |
| 1310 | `<numeric_unary_expr_arg>` | -> | { (, ++, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1311 | `<numeric_postfix_expr_arg>` | -> | { ( } |
| 1312 | `<numeric_postfix_expr_arg>` | -> | { int } |
| 1313 | `<numeric_postfix_expr_arg>` | -> | { long } |
| 1314 | `<numeric_postfix_expr_arg>` | -> | { float } |
| 1315 | `<numeric_postfix_expr_arg>` | -> | { double } |
| 1316 | `<numeric_postfix_expr_arg>` | -> | { ++ } |
| 1317 | `<numeric_postfix_expr_arg>` | -> | { -- } |
| 1318 | `<numeric_postfix_expr_arg>` | -> | { id } |
| 1319 | `<numeric_postfix_expr_arg>` | -> | { intlit } |
| 1320 | `<numeric_postfix_expr_arg>` | -> | { longlit } |
| 1321 | `<numeric_postfix_expr_arg>` | -> | { floatlit } |
| 1322 | `<numeric_postfix_expr_arg>` | -> | { doublelit } |
| 1323 | `<arg_id_postfix>` | -> | { ++ } |
| 1324 | `<arg_id_postfix>` | -> | { -- } |
| 1325 | `<arg_id_postfix>` | -> | { (, ., [, λ } |
| 1326 | `<arg_postfix_chain>` | -> | { [ } |
| 1327 | `<arg_postfix_chain>` | -> | { . } |
| 1328 | `<arg_postfix_chain>` | -> | { ( } |
| 1329 | `<arg_postfix_chain>` | -> | { λ } |
| 1330 | `<arg_array_access>` | -> | { [ } |
| 1331 | `<arg_array_access_dim2>` | -> | { [ } |
| 1332 | `<arg_array_access_dim2>` | -> | { λ } |
| 1333 | `<arg_postfix_after_arr>` | -> | { . } |
| 1334 | `<arg_postfix_after_arr>` | -> | { ( } |
| 1335 | `<arg_postfix_after_arr>` | -> | { λ } |
| 1336 | `<arg_array_index>` | -> | { intlit } |
| 1337 | `<arg_array_index>` | -> | { id } |
| 1338 | `<arg_nested_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1339 | `<arg_nested_list>` | -> | { λ } |
| 1340 | `<arg_nested_tail>` | -> | { , } |
| 1341 | `<arg_nested_tail>` | -> | { λ } |
| 1342 | `<io_stmt>` | -> | { trap } |
| 1343 | `<io_stmt>` | -> | { thread } |
| 1344 | `<io_stmt>` | -> | { threadln } |
| 1345 | `<trap_target>` | -> | { id } |
| 1346 | `<trap_target_tail>` | -> | { [ } |
| 1347 | `<trap_target_tail>` | -> | { . } |
| 1348 | `<trap_target_tail>` | -> | { λ } |
| 1349 | `<print_args>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1350 | `<print_tail>` | -> | { , } |
| 1351 | `<print_tail>` | -> | { λ } |
| 1352 | `<ctrl_struct>` | -> | { if } |
| 1353 | `<ctrl_struct>` | -> | { switch } |
| 1354 | `<ctrl_struct>` | -> | { for } |
| 1355 | `<ctrl_struct>` | -> | { while } |
| 1356 | `<ctrl_struct>` | -> | { do } |
| 1357 | `<ctrl_stmt_list>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1358 | `<ctrl_stmt_list>` | -> | { λ } |
| 1359 | `<non_empty_ctrl_stmt_list>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1360 | `<loop_statement_non_return>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1361 | `<loop_statement_non_return>` | -> | { break } |
| 1362 | `<loop_ctrl_stmt_list>` | -> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1363 | `<loop_ctrl_stmt_list>` | -> | { λ } |
| 1364 | `<non_empty_loop_ctrl_stmt_list>` | -> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1365 | `<else_opt>` | -> | { else } |
| 1366 | `<else_opt>` | -> | { λ } |
| 1367 | `<else_body>` | -> | { { } |
| 1368 | `<else_body>` | -> | { if } |
| 1369 | `<case_list>` | -> | { case } |
| 1370 | `<case_list>` | -> | { λ } |
| 1371 | `<case_val>` | -> | { intlit } |
| 1372 | `<case_val>` | -> | { longlit } |
| 1373 | `<case_val>` | -> | { charlit } |
| 1374 | `<case_val>` | -> | { true } |
| 1375 | `<case_val>` | -> | { false } |
| 1376 | `<default_opt>` | -> | { default } |
| 1377 | `<default_opt>` | -> | { λ } |
| 1378 | `<break_opt>` | -> | { break } |
| 1379 | `<break_opt>` | -> | { λ } |
| 1380 | `<for_init>` | -> | { local } |
| 1381 | `<for_init>` | -> | { id } |
| 1382 | `<for_init>` | -> | { λ } |
| 1383 | `<for_init_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 1384 | `<for_init_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1385 | `<for_init_type>` | -> | { int } |
| 1386 | `<for_init_type>` | -> | { long } |
| 1387 | `<for_init_type>` | -> | { float } |
| 1388 | `<for_init_type>` | -> | { double } |
| 1389 | `<for_init_type>` | -> | { char } |
| 1390 | `<for_init_type>` | -> | { string } |
| 1391 | `<for_init_type>` | -> | { bool } |
| 1392 | `<for_cond>` | -> | { !, (, ++, -, --, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1393 | `<condition>` | -> | { !, (, ++, -, --, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1394 | `<cond_or>` | -> | { !, (, ++, -, --, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1395 | `<cond_or_tail>` | -> | { \|\| } |
| 1396 | `<cond_or_tail>` | -> | { λ } |
| 1397 | `<cond_and>` | -> | { !, (, ++, -, --, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1398 | `<cond_and_tail>` | -> | { && } |
| 1399 | `<cond_and_tail>` | -> | { λ } |
| 1400 | `<cond_not>` | -> | { ! } |
| 1401 | `<cond_not>` | -> | { (, ++, -, --, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1402 | `<cond_atom>` | -> | { true } |
| 1403 | `<cond_atom>` | -> | { false } |
| 1404 | `<cond_atom>` | -> | { id } |
| 1405 | `<cond_atom>` | -> | { ( } |
| 1406 | `<cond_atom>` | -> | { -, doublelit, floatlit, intlit, longlit } |
| 1407 | `<cond_atom>` | -> | { ++ } |
| 1408 | `<cond_atom>` | -> | { -- } |
| 1409 | `<cond_paren_inner>` | -> | { !, (, ++, -, --, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1410 | `<cond_paren_start>` | -> | { id } |
| 1411 | `<cond_paren_start>` | -> | { intlit } |
| 1412 | `<cond_paren_start>` | -> | { longlit } |
| 1413 | `<cond_paren_start>` | -> | { floatlit } |
| 1414 | `<cond_paren_start>` | -> | { doublelit } |
| 1415 | `<cond_paren_start>` | -> | { true } |
| 1416 | `<cond_paren_start>` | -> | { false } |
| 1417 | `<cond_paren_start>` | -> | { ! } |
| 1418 | `<cond_paren_start>` | -> | { ++ } |
| 1419 | `<cond_paren_start>` | -> | { -- } |
| 1420 | `<cond_paren_start>` | -> | { - } |
| 1421 | `<cond_paren_start>` | -> | { ( } |
| 1422 | `<cond_paren_cont>` | -> | { %, *, +, -, / } |
| 1423 | `<cond_paren_cont>` | -> | { !=, <, <=, ==, >, >= } |
| 1424 | `<cond_paren_cont>` | -> | { &&, \|\|, λ } |
| 1425 | `<cond_paren_cont>` | -> | { ++ } |
| 1426 | `<cond_paren_cont>` | -> | { ++ } |
| 1427 | `<cond_paren_cont>` | -> | { -- } |
| 1428 | `<cond_paren_cont>` | -> | { -- } |
| 1429 | `<cond_paren_arith_ops>` | -> | { + } |
| 1430 | `<cond_paren_arith_ops>` | -> | { - } |
| 1431 | `<cond_paren_arith_ops>` | -> | { * } |
| 1432 | `<cond_paren_arith_ops>` | -> | { / } |
| 1433 | `<cond_paren_arith_ops>` | -> | { % } |
| 1434 | `<cond_paren_mul_ops>` | -> | { * } |
| 1435 | `<cond_paren_mul_ops>` | -> | { / } |
| 1436 | `<cond_paren_mul_ops>` | -> | { % } |
| 1437 | `<cond_paren_mul_ops>` | -> | { + } |
| 1438 | `<cond_paren_mul_ops>` | -> | { - } |
| 1439 | `<cond_paren_mul_ops>` | -> | { λ } |
| 1440 | `<cond_paren_unary>` | -> | { ++ } |
| 1441 | `<cond_paren_unary>` | -> | { -- } |
| 1442 | `<cond_paren_unary>` | -> | { - } |
| 1443 | `<cond_paren_unary>` | -> | { (, doublelit, floatlit, id, intlit, longlit } |
| 1444 | `<cond_paren_primary>` | -> | { intlit } |
| 1445 | `<cond_paren_primary>` | -> | { longlit } |
| 1446 | `<cond_paren_primary>` | -> | { floatlit } |
| 1447 | `<cond_paren_primary>` | -> | { doublelit } |
| 1448 | `<cond_paren_primary>` | -> | { id } |
| 1449 | `<cond_paren_primary>` | -> | { ( } |
| 1450 | `<cond_paren_after_arith>` | -> | { !=, <, <=, ==, >, >= } |
| 1451 | `<cond_paren_after_arith>` | -> | { λ } |
| 1452 | `<cond_paren_logic>` | -> | { && } |
| 1453 | `<cond_paren_logic>` | -> | { \|\| } |
| 1454 | `<cond_paren_logic>` | -> | { λ } |
| 1455 | `<cond_paren_tail>` | -> | { !=, <, <=, ==, >, >= } |
| 1456 | `<cond_paren_tail>` | -> | { λ } |
| 1457 | `<cond_id_cont>` | -> | { [ } |
| 1458 | `<cond_id_cont>` | -> | { + } |
| 1459 | `<cond_id_cont>` | -> | { - } |
| 1460 | `<cond_id_cont>` | -> | { * } |
| 1461 | `<cond_id_cont>` | -> | { / } |
| 1462 | `<cond_id_cont>` | -> | { % } |
| 1463 | `<cond_id_cont>` | -> | { < } |
| 1464 | `<cond_id_cont>` | -> | { > } |
| 1465 | `<cond_id_cont>` | -> | { <= } |
| 1466 | `<cond_id_cont>` | -> | { >= } |
| 1467 | `<cond_id_cont>` | -> | { == } |
| 1468 | `<cond_id_cont>` | -> | { != } |
| 1469 | `<cond_id_cont>` | -> | { ++ } |
| 1470 | `<cond_id_cont>` | -> | { ++ } |
| 1471 | `<cond_id_cont>` | -> | { ++ } |
| 1472 | `<cond_id_cont>` | -> | { ++ } |
| 1473 | `<cond_id_cont>` | -> | { ++ } |
| 1474 | `<cond_id_cont>` | -> | { ++ } |
| 1475 | `<cond_id_cont>` | -> | { -- } |
| 1476 | `<cond_id_cont>` | -> | { -- } |
| 1477 | `<cond_id_cont>` | -> | { -- } |
| 1478 | `<cond_id_cont>` | -> | { -- } |
| 1479 | `<cond_id_cont>` | -> | { -- } |
| 1480 | `<cond_id_cont>` | -> | { -- } |
| 1481 | `<cond_id_cont>` | -> | { λ } |
| 1482 | `<cond_arr_index>` | -> | { (, ++, -, --, doublelit, floatlit, id, intlit, longlit } |
| 1483 | `<cond_id_arr_cont>` | -> | { [ } |
| 1484 | `<cond_id_arr_cont>` | -> | { !=, %, *, +, ++, -, --, /, <, <=, ==, >, >=, λ } |
| 1485 | `<cond_id_arr_after>` | -> | { + } |
| 1486 | `<cond_id_arr_after>` | -> | { - } |
| 1487 | `<cond_id_arr_after>` | -> | { * } |
| 1488 | `<cond_id_arr_after>` | -> | { / } |
| 1489 | `<cond_id_arr_after>` | -> | { % } |
| 1490 | `<cond_id_arr_after>` | -> | { < } |
| 1491 | `<cond_id_arr_after>` | -> | { > } |
| 1492 | `<cond_id_arr_after>` | -> | { <= } |
| 1493 | `<cond_id_arr_after>` | -> | { >= } |
| 1494 | `<cond_id_arr_after>` | -> | { == } |
| 1495 | `<cond_id_arr_after>` | -> | { != } |
| 1496 | `<cond_id_arr_after>` | -> | { ++ } |
| 1497 | `<cond_id_arr_after>` | -> | { ++ } |
| 1498 | `<cond_id_arr_after>` | -> | { ++ } |
| 1499 | `<cond_id_arr_after>` | -> | { ++ } |
| 1500 | `<cond_id_arr_after>` | -> | { ++ } |
| 1501 | `<cond_id_arr_after>` | -> | { ++ } |
| 1502 | `<cond_id_arr_after>` | -> | { -- } |
| 1503 | `<cond_id_arr_after>` | -> | { -- } |
| 1504 | `<cond_id_arr_after>` | -> | { -- } |
| 1505 | `<cond_id_arr_after>` | -> | { -- } |
| 1506 | `<cond_id_arr_after>` | -> | { -- } |
| 1507 | `<cond_id_arr_after>` | -> | { -- } |
| 1508 | `<cond_id_arr_after>` | -> | { λ } |
| 1509 | `<cond_lit_cmp>` | -> | { intlit } |
| 1510 | `<cond_lit_cmp>` | -> | { longlit } |
| 1511 | `<cond_lit_cmp>` | -> | { floatlit } |
| 1512 | `<cond_lit_cmp>` | -> | { doublelit } |
| 1513 | `<cond_lit_cmp>` | -> | { - } |
| 1514 | `<cond_lit_mul>` | -> | { * } |
| 1515 | `<cond_lit_mul>` | -> | { / } |
| 1516 | `<cond_lit_mul>` | -> | { % } |
| 1517 | `<cond_lit_mul>` | -> | { λ } |
| 1518 | `<cond_lit_add>` | -> | { + } |
| 1519 | `<cond_lit_add>` | -> | { - } |
| 1520 | `<cond_lit_add>` | -> | { λ } |
| 1521 | `<cond_lit_unary>` | -> | { ++ } |
| 1522 | `<cond_lit_unary>` | -> | { -- } |
| 1523 | `<cond_lit_unary>` | -> | { - } |
| 1524 | `<cond_lit_unary>` | -> | { (, doublelit, floatlit, id, intlit, longlit } |
| 1525 | `<cond_lit_primary>` | -> | { intlit } |
| 1526 | `<cond_lit_primary>` | -> | { longlit } |
| 1527 | `<cond_lit_primary>` | -> | { floatlit } |
| 1528 | `<cond_lit_primary>` | -> | { doublelit } |
| 1529 | `<cond_lit_primary>` | -> | { id } |
| 1530 | `<cond_lit_primary>` | -> | { ( } |
| 1531 | `<cond_lit_expr>` | -> | { (, ++, -, --, doublelit, floatlit, id, intlit, longlit } |
| 1532 | `<cond_rhs>` | -> | { (, ++, -, --, doublelit, floatlit, id, intlit, longlit } |
| 1533 | `<cond_rhs_unary>` | -> | { ++ } |
| 1534 | `<cond_rhs_unary>` | -> | { -- } |
| 1535 | `<cond_rhs_unary>` | -> | { - } |
| 1536 | `<cond_rhs_unary>` | -> | { (, doublelit, floatlit, id, intlit, longlit } |
| 1537 | `<cond_rhs_primary>` | -> | { intlit } |
| 1538 | `<cond_rhs_primary>` | -> | { longlit } |
| 1539 | `<cond_rhs_primary>` | -> | { floatlit } |
| 1540 | `<cond_rhs_primary>` | -> | { doublelit } |
| 1541 | `<cond_rhs_primary>` | -> | { id } |
| 1542 | `<cond_rhs_primary>` | -> | { ( } |
| 1543 | `<cond_rhs_id_tail>` | -> | { [ } |
| 1544 | `<cond_rhs_id_tail>` | -> | { ++ } |
| 1545 | `<cond_rhs_id_tail>` | -> | { -- } |
| 1546 | `<cond_rhs_id_tail>` | -> | { λ } |
| 1547 | `<cond_rhs_arr_tail>` | -> | { [ } |
| 1548 | `<cond_rhs_arr_tail>` | -> | { [ } |
| 1549 | `<cond_rhs_arr_tail>` | -> | { [ } |
| 1550 | `<cond_rhs_arr_tail>` | -> | { ++ } |
| 1551 | `<cond_rhs_arr_tail>` | -> | { -- } |
| 1552 | `<cond_rhs_arr_tail>` | -> | { λ } |
| 1553 | `<cond_rhs_mul>` | -> | { * } |
| 1554 | `<cond_rhs_mul>` | -> | { / } |
| 1555 | `<cond_rhs_mul>` | -> | { % } |
| 1556 | `<cond_rhs_mul>` | -> | { λ } |
| 1557 | `<cond_rhs_add>` | -> | { + } |
| 1558 | `<cond_rhs_add>` | -> | { - } |
| 1559 | `<cond_rhs_add>` | -> | { λ } |
| 1560 | `<cond_cmp>` | -> | { < } |
| 1561 | `<cond_cmp>` | -> | { > } |
| 1562 | `<cond_cmp>` | -> | { <= } |
| 1563 | `<cond_cmp>` | -> | { >= } |
| 1564 | `<cond_cmp>` | -> | { == } |
| 1565 | `<cond_cmp>` | -> | { != } |
| 1566 | `<for_update>` | -> | { id } |
| 1567 | `<for_update>` | -> | { ++ } |
| 1568 | `<for_update>` | -> | { -- } |
| 1569 | `<for_update>` | -> | { λ } |
| 1570 | `<for_update_tail>` | -> | { ++ } |
| 1571 | `<for_update_tail>` | -> | { -- } |
| 1572 | `<for_update_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 1573 | `<main_body>` | -> | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 1574 | `<main_content>` | -> | { using } |
| 1575 | `<main_content>` | -> | { local } |
| 1576 | `<main_content>` | -> | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1577 | `<main_content>` | -> | { return } |