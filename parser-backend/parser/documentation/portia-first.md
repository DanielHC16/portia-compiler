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
| 235 | `<function_body_int>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 236 | `<func_content_int>` | -> | { using } |
| 237 | `<func_content_int>` | -> | { local } |
| 238 | `<func_content_int>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 239 | `<func_content_int>` | -> | { λ } |
| 240 | `<function_body_long>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 241 | `<func_content_long>` | -> | { using } |
| 242 | `<func_content_long>` | -> | { local } |
| 243 | `<func_content_long>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 244 | `<func_content_long>` | -> | { λ } |
| 245 | `<function_body_float>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 246 | `<func_content_float>` | -> | { using } |
| 247 | `<func_content_float>` | -> | { local } |
| 248 | `<func_content_float>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 249 | `<func_content_float>` | -> | { λ } |
| 250 | `<function_body_double>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 251 | `<func_content_double>` | -> | { using } |
| 252 | `<func_content_double>` | -> | { local } |
| 253 | `<func_content_double>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 254 | `<func_content_double>` | -> | { λ } |
| 255 | `<function_body_char>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 256 | `<func_content_char>` | -> | { using } |
| 257 | `<func_content_char>` | -> | { local } |
| 258 | `<func_content_char>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 259 | `<func_content_char>` | -> | { λ } |
| 260 | `<function_body_string>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 261 | `<func_content_string>` | -> | { using } |
| 262 | `<func_content_string>` | -> | { local } |
| 263 | `<func_content_string>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 264 | `<func_content_string>` | -> | { λ } |
| 265 | `<function_body_bool>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 266 | `<func_content_bool>` | -> | { using } |
| 267 | `<func_content_bool>` | -> | { local } |
| 268 | `<func_content_bool>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 269 | `<func_content_bool>` | -> | { λ } |
| 270 | `<function_body_array>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 271 | `<func_content_array>` | -> | { using } |
| 272 | `<func_content_array>` | -> | { local } |
| 273 | `<func_content_array>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 274 | `<func_content_array>` | -> | { λ } |
| 275 | `<function_body_weave>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 276 | `<func_content_weave>` | -> | { using } |
| 277 | `<func_content_weave>` | -> | { local } |
| 278 | `<func_content_weave>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 279 | `<func_content_weave>` | -> | { λ } |
| 280 | `<function_body_void>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 281 | `<func_content_void>` | -> | { using } |
| 282 | `<func_content_void>` | -> | { local } |
| 283 | `<func_content_void>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 284 | `<func_content_void>` | -> | { λ } |
| 285 | `<statement_int>` | -> | { ++, --, id } |
| 286 | `<statement_int>` | -> | { thread, threadln, trap } |
| 287 | `<statement_int>` | -> | { do, for, if, switch, while } |
| 288 | `<statement_int>` | -> | { break } |
| 289 | `<statement_int>` | -> | { return } |
| 290 | `<statement_long>` | -> | { ++, --, id } |
| 291 | `<statement_long>` | -> | { thread, threadln, trap } |
| 292 | `<statement_long>` | -> | { do, for, if, switch, while } |
| 293 | `<statement_long>` | -> | { break } |
| 294 | `<statement_long>` | -> | { return } |
| 295 | `<statement_float>` | -> | { ++, --, id } |
| 296 | `<statement_float>` | -> | { thread, threadln, trap } |
| 297 | `<statement_float>` | -> | { do, for, if, switch, while } |
| 298 | `<statement_float>` | -> | { break } |
| 299 | `<statement_float>` | -> | { return } |
| 300 | `<statement_double>` | -> | { ++, --, id } |
| 301 | `<statement_double>` | -> | { thread, threadln, trap } |
| 302 | `<statement_double>` | -> | { do, for, if, switch, while } |
| 303 | `<statement_double>` | -> | { break } |
| 304 | `<statement_double>` | -> | { return } |
| 305 | `<statement_char>` | -> | { ++, --, id } |
| 306 | `<statement_char>` | -> | { thread, threadln, trap } |
| 307 | `<statement_char>` | -> | { do, for, if, switch, while } |
| 308 | `<statement_char>` | -> | { break } |
| 309 | `<statement_char>` | -> | { return } |
| 310 | `<statement_string>` | -> | { ++, --, id } |
| 311 | `<statement_string>` | -> | { thread, threadln, trap } |
| 312 | `<statement_string>` | -> | { do, for, if, switch, while } |
| 313 | `<statement_string>` | -> | { break } |
| 314 | `<statement_string>` | -> | { return } |
| 315 | `<statement_bool>` | -> | { ++, --, id } |
| 316 | `<statement_bool>` | -> | { thread, threadln, trap } |
| 317 | `<statement_bool>` | -> | { do, for, if, switch, while } |
| 318 | `<statement_bool>` | -> | { break } |
| 319 | `<statement_bool>` | -> | { return } |
| 320 | `<statement_array>` | -> | { ++, --, id } |
| 321 | `<statement_array>` | -> | { thread, threadln, trap } |
| 322 | `<statement_array>` | -> | { do, for, if, switch, while } |
| 323 | `<statement_array>` | -> | { break } |
| 324 | `<statement_array>` | -> | { return } |
| 325 | `<statement_weave>` | -> | { ++, --, id } |
| 326 | `<statement_weave>` | -> | { thread, threadln, trap } |
| 327 | `<statement_weave>` | -> | { do, for, if, switch, while } |
| 328 | `<statement_weave>` | -> | { break } |
| 329 | `<statement_weave>` | -> | { return } |
| 330 | `<statement_void>` | -> | { ++, --, id } |
| 331 | `<statement_void>` | -> | { thread, threadln, trap } |
| 332 | `<statement_void>` | -> | { do, for, if, switch, while } |
| 333 | `<statement_void>` | -> | { break } |
| 334 | `<statement_void>` | -> | { return } |
| 335 | `<ctrl_struct_int>` | -> | { if } |
| 336 | `<ctrl_struct_int>` | -> | { switch } |
| 337 | `<ctrl_struct_int>` | -> | { for } |
| 338 | `<ctrl_struct_int>` | -> | { while } |
| 339 | `<ctrl_struct_int>` | -> | { do } |
| 340 | `<stmt_list_int>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 341 | `<stmt_list_int>` | -> | { λ } |
| 342 | `<else_opt_int>` | -> | { else } |
| 343 | `<else_opt_int>` | -> | { λ } |
| 344 | `<else_body_int>` | -> | { { } |
| 345 | `<else_body_int>` | -> | { if } |
| 346 | `<case_list_int>` | -> | { case } |
| 347 | `<case_list_int>` | -> | { λ } |
| 348 | `<default_opt_int>` | -> | { default } |
| 349 | `<default_opt_int>` | -> | { λ } |
| 350 | `<ctrl_struct_long>` | -> | { if } |
| 351 | `<ctrl_struct_long>` | -> | { switch } |
| 352 | `<ctrl_struct_long>` | -> | { for } |
| 353 | `<ctrl_struct_long>` | -> | { while } |
| 354 | `<ctrl_struct_long>` | -> | { do } |
| 355 | `<stmt_list_long>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 356 | `<stmt_list_long>` | -> | { λ } |
| 357 | `<else_opt_long>` | -> | { else } |
| 358 | `<else_opt_long>` | -> | { λ } |
| 359 | `<else_body_long>` | -> | { { } |
| 360 | `<else_body_long>` | -> | { if } |
| 361 | `<case_list_long>` | -> | { case } |
| 362 | `<case_list_long>` | -> | { λ } |
| 363 | `<default_opt_long>` | -> | { default } |
| 364 | `<default_opt_long>` | -> | { λ } |
| 365 | `<ctrl_struct_float>` | -> | { if } |
| 366 | `<ctrl_struct_float>` | -> | { switch } |
| 367 | `<ctrl_struct_float>` | -> | { for } |
| 368 | `<ctrl_struct_float>` | -> | { while } |
| 369 | `<ctrl_struct_float>` | -> | { do } |
| 370 | `<stmt_list_float>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 371 | `<stmt_list_float>` | -> | { λ } |
| 372 | `<else_opt_float>` | -> | { else } |
| 373 | `<else_opt_float>` | -> | { λ } |
| 374 | `<else_body_float>` | -> | { { } |
| 375 | `<else_body_float>` | -> | { if } |
| 376 | `<case_list_float>` | -> | { case } |
| 377 | `<case_list_float>` | -> | { λ } |
| 378 | `<default_opt_float>` | -> | { default } |
| 379 | `<default_opt_float>` | -> | { λ } |
| 380 | `<ctrl_struct_double>` | -> | { if } |
| 381 | `<ctrl_struct_double>` | -> | { switch } |
| 382 | `<ctrl_struct_double>` | -> | { for } |
| 383 | `<ctrl_struct_double>` | -> | { while } |
| 384 | `<ctrl_struct_double>` | -> | { do } |
| 385 | `<stmt_list_double>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 386 | `<stmt_list_double>` | -> | { λ } |
| 387 | `<else_opt_double>` | -> | { else } |
| 388 | `<else_opt_double>` | -> | { λ } |
| 389 | `<else_body_double>` | -> | { { } |
| 390 | `<else_body_double>` | -> | { if } |
| 391 | `<case_list_double>` | -> | { case } |
| 392 | `<case_list_double>` | -> | { λ } |
| 393 | `<default_opt_double>` | -> | { default } |
| 394 | `<default_opt_double>` | -> | { λ } |
| 395 | `<ctrl_struct_char>` | -> | { if } |
| 396 | `<ctrl_struct_char>` | -> | { switch } |
| 397 | `<ctrl_struct_char>` | -> | { for } |
| 398 | `<ctrl_struct_char>` | -> | { while } |
| 399 | `<ctrl_struct_char>` | -> | { do } |
| 400 | `<stmt_list_char>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 401 | `<stmt_list_char>` | -> | { λ } |
| 402 | `<else_opt_char>` | -> | { else } |
| 403 | `<else_opt_char>` | -> | { λ } |
| 404 | `<else_body_char>` | -> | { { } |
| 405 | `<else_body_char>` | -> | { if } |
| 406 | `<case_list_char>` | -> | { case } |
| 407 | `<case_list_char>` | -> | { λ } |
| 408 | `<default_opt_char>` | -> | { default } |
| 409 | `<default_opt_char>` | -> | { λ } |
| 410 | `<ctrl_struct_string>` | -> | { if } |
| 411 | `<ctrl_struct_string>` | -> | { switch } |
| 412 | `<ctrl_struct_string>` | -> | { for } |
| 413 | `<ctrl_struct_string>` | -> | { while } |
| 414 | `<ctrl_struct_string>` | -> | { do } |
| 415 | `<stmt_list_string>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 416 | `<stmt_list_string>` | -> | { λ } |
| 417 | `<else_opt_string>` | -> | { else } |
| 418 | `<else_opt_string>` | -> | { λ } |
| 419 | `<else_body_string>` | -> | { { } |
| 420 | `<else_body_string>` | -> | { if } |
| 421 | `<case_list_string>` | -> | { case } |
| 422 | `<case_list_string>` | -> | { λ } |
| 423 | `<default_opt_string>` | -> | { default } |
| 424 | `<default_opt_string>` | -> | { λ } |
| 425 | `<ctrl_struct_bool>` | -> | { if } |
| 426 | `<ctrl_struct_bool>` | -> | { switch } |
| 427 | `<ctrl_struct_bool>` | -> | { for } |
| 428 | `<ctrl_struct_bool>` | -> | { while } |
| 429 | `<ctrl_struct_bool>` | -> | { do } |
| 430 | `<stmt_list_bool>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 431 | `<stmt_list_bool>` | -> | { λ } |
| 432 | `<else_opt_bool>` | -> | { else } |
| 433 | `<else_opt_bool>` | -> | { λ } |
| 434 | `<else_body_bool>` | -> | { { } |
| 435 | `<else_body_bool>` | -> | { if } |
| 436 | `<case_list_bool>` | -> | { case } |
| 437 | `<case_list_bool>` | -> | { λ } |
| 438 | `<default_opt_bool>` | -> | { default } |
| 439 | `<default_opt_bool>` | -> | { λ } |
| 440 | `<ctrl_struct_array>` | -> | { if } |
| 441 | `<ctrl_struct_array>` | -> | { switch } |
| 442 | `<ctrl_struct_array>` | -> | { for } |
| 443 | `<ctrl_struct_array>` | -> | { while } |
| 444 | `<ctrl_struct_array>` | -> | { do } |
| 445 | `<stmt_list_array>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 446 | `<stmt_list_array>` | -> | { λ } |
| 447 | `<else_opt_array>` | -> | { else } |
| 448 | `<else_opt_array>` | -> | { λ } |
| 449 | `<else_body_array>` | -> | { { } |
| 450 | `<else_body_array>` | -> | { if } |
| 451 | `<case_list_array>` | -> | { case } |
| 452 | `<case_list_array>` | -> | { λ } |
| 453 | `<default_opt_array>` | -> | { default } |
| 454 | `<default_opt_array>` | -> | { λ } |
| 455 | `<ctrl_struct_weave>` | -> | { if } |
| 456 | `<ctrl_struct_weave>` | -> | { switch } |
| 457 | `<ctrl_struct_weave>` | -> | { for } |
| 458 | `<ctrl_struct_weave>` | -> | { while } |
| 459 | `<ctrl_struct_weave>` | -> | { do } |
| 460 | `<stmt_list_weave>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 461 | `<stmt_list_weave>` | -> | { λ } |
| 462 | `<else_opt_weave>` | -> | { else } |
| 463 | `<else_opt_weave>` | -> | { λ } |
| 464 | `<else_body_weave>` | -> | { { } |
| 465 | `<else_body_weave>` | -> | { if } |
| 466 | `<case_list_weave>` | -> | { case } |
| 467 | `<case_list_weave>` | -> | { λ } |
| 468 | `<default_opt_weave>` | -> | { default } |
| 469 | `<default_opt_weave>` | -> | { λ } |
| 470 | `<ctrl_struct_void>` | -> | { if } |
| 471 | `<ctrl_struct_void>` | -> | { switch } |
| 472 | `<ctrl_struct_void>` | -> | { for } |
| 473 | `<ctrl_struct_void>` | -> | { while } |
| 474 | `<ctrl_struct_void>` | -> | { do } |
| 475 | `<stmt_list_void>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 476 | `<stmt_list_void>` | -> | { λ } |
| 477 | `<else_opt_void>` | -> | { else } |
| 478 | `<else_opt_void>` | -> | { λ } |
| 479 | `<else_body_void>` | -> | { { } |
| 480 | `<else_body_void>` | -> | { if } |
| 481 | `<case_list_void>` | -> | { case } |
| 482 | `<case_list_void>` | -> | { λ } |
| 483 | `<default_opt_void>` | -> | { default } |
| 484 | `<default_opt_void>` | -> | { λ } |
| 485 | `<int_return_expr>` | -> | { !, (, ++, --, id, int, intlit } |
| 486 | `<int_ret_assign>` | -> | { !, (, ++, --, id, int, intlit } |
| 487 | `<int_ret_concat>` | -> | { !, (, ++, --, id, int, intlit } |
| 488 | `<int_ret_or>` | -> | { !, (, ++, --, id, int, intlit } |
| 489 | `<int_ret_and>` | -> | { !, (, ++, --, id, int, intlit } |
| 490 | `<int_ret_eq>` | -> | { !, (, ++, --, id, int, intlit } |
| 491 | `<int_ret_rel>` | -> | { !, (, ++, --, id, int, intlit } |
| 492 | `<int_ret_add>` | -> | { !, (, ++, --, id, int, intlit } |
| 493 | `<int_ret_mul>` | -> | { !, (, ++, --, id, int, intlit } |
| 494 | `<int_ret_unary>` | -> | { ! } |
| 495 | `<int_ret_unary>` | -> | { (, ++, --, id, int, intlit } |
| 496 | `<int_ret_postfix>` | -> | { intlit } |
| 497 | `<int_ret_postfix>` | -> | { ++ } |
| 498 | `<int_ret_postfix>` | -> | { -- } |
| 499 | `<int_ret_postfix>` | -> | { id } |
| 500 | `<int_ret_postfix>` | -> | { ( } |
| 501 | `<int_ret_postfix>` | -> | { int } |
| 502 | `<long_return_expr>` | -> | { !, (, ++, --, id, long, longlit } |
| 503 | `<long_ret_assign>` | -> | { !, (, ++, --, id, long, longlit } |
| 504 | `<long_ret_concat>` | -> | { !, (, ++, --, id, long, longlit } |
| 505 | `<long_ret_or>` | -> | { !, (, ++, --, id, long, longlit } |
| 506 | `<long_ret_and>` | -> | { !, (, ++, --, id, long, longlit } |
| 507 | `<long_ret_eq>` | -> | { !, (, ++, --, id, long, longlit } |
| 508 | `<long_ret_rel>` | -> | { !, (, ++, --, id, long, longlit } |
| 509 | `<long_ret_add>` | -> | { !, (, ++, --, id, long, longlit } |
| 510 | `<long_ret_mul>` | -> | { !, (, ++, --, id, long, longlit } |
| 511 | `<long_ret_unary>` | -> | { ! } |
| 512 | `<long_ret_unary>` | -> | { (, ++, --, id, long, longlit } |
| 513 | `<long_ret_postfix>` | -> | { longlit } |
| 514 | `<long_ret_postfix>` | -> | { ++ } |
| 515 | `<long_ret_postfix>` | -> | { -- } |
| 516 | `<long_ret_postfix>` | -> | { id } |
| 517 | `<long_ret_postfix>` | -> | { ( } |
| 518 | `<long_ret_postfix>` | -> | { long } |
| 519 | `<float_return_expr>` | -> | { !, (, ++, --, float, floatlit, id } |
| 520 | `<float_ret_assign>` | -> | { !, (, ++, --, float, floatlit, id } |
| 521 | `<float_ret_concat>` | -> | { !, (, ++, --, float, floatlit, id } |
| 522 | `<float_ret_or>` | -> | { !, (, ++, --, float, floatlit, id } |
| 523 | `<float_ret_and>` | -> | { !, (, ++, --, float, floatlit, id } |
| 524 | `<float_ret_eq>` | -> | { !, (, ++, --, float, floatlit, id } |
| 525 | `<float_ret_rel>` | -> | { !, (, ++, --, float, floatlit, id } |
| 526 | `<float_ret_add>` | -> | { !, (, ++, --, float, floatlit, id } |
| 527 | `<float_ret_mul>` | -> | { !, (, ++, --, float, floatlit, id } |
| 528 | `<float_ret_unary>` | -> | { ! } |
| 529 | `<float_ret_unary>` | -> | { (, ++, --, float, floatlit, id } |
| 530 | `<float_ret_postfix>` | -> | { floatlit } |
| 531 | `<float_ret_postfix>` | -> | { ++ } |
| 532 | `<float_ret_postfix>` | -> | { -- } |
| 533 | `<float_ret_postfix>` | -> | { id } |
| 534 | `<float_ret_postfix>` | -> | { ( } |
| 535 | `<float_ret_postfix>` | -> | { float } |
| 536 | `<double_return_expr>` | -> | { !, (, ++, --, double, doublelit, id } |
| 537 | `<double_ret_assign>` | -> | { !, (, ++, --, double, doublelit, id } |
| 538 | `<double_ret_concat>` | -> | { !, (, ++, --, double, doublelit, id } |
| 539 | `<double_ret_or>` | -> | { !, (, ++, --, double, doublelit, id } |
| 540 | `<double_ret_and>` | -> | { !, (, ++, --, double, doublelit, id } |
| 541 | `<double_ret_eq>` | -> | { !, (, ++, --, double, doublelit, id } |
| 542 | `<double_ret_rel>` | -> | { !, (, ++, --, double, doublelit, id } |
| 543 | `<double_ret_add>` | -> | { !, (, ++, --, double, doublelit, id } |
| 544 | `<double_ret_mul>` | -> | { !, (, ++, --, double, doublelit, id } |
| 545 | `<double_ret_unary>` | -> | { ! } |
| 546 | `<double_ret_unary>` | -> | { (, ++, --, double, doublelit, id } |
| 547 | `<double_ret_postfix>` | -> | { doublelit } |
| 548 | `<double_ret_postfix>` | -> | { ++ } |
| 549 | `<double_ret_postfix>` | -> | { -- } |
| 550 | `<double_ret_postfix>` | -> | { id } |
| 551 | `<double_ret_postfix>` | -> | { ( } |
| 552 | `<double_ret_postfix>` | -> | { double } |
| 553 | `<char_return_expr>` | -> | { !, (, ++, --, char, charlit, id } |
| 554 | `<char_ret_assign>` | -> | { !, (, ++, --, char, charlit, id } |
| 555 | `<char_ret_concat>` | -> | { !, (, ++, --, char, charlit, id } |
| 556 | `<char_ret_or>` | -> | { !, (, ++, --, char, charlit, id } |
| 557 | `<char_ret_and>` | -> | { !, (, ++, --, char, charlit, id } |
| 558 | `<char_ret_eq>` | -> | { !, (, ++, --, char, charlit, id } |
| 559 | `<char_ret_rel>` | -> | { !, (, ++, --, char, charlit, id } |
| 560 | `<char_ret_add>` | -> | { !, (, ++, --, char, charlit, id } |
| 561 | `<char_ret_mul>` | -> | { !, (, ++, --, char, charlit, id } |
| 562 | `<char_ret_unary>` | -> | { ! } |
| 563 | `<char_ret_unary>` | -> | { (, ++, --, char, charlit, id } |
| 564 | `<char_ret_postfix>` | -> | { charlit } |
| 565 | `<char_ret_postfix>` | -> | { ++ } |
| 566 | `<char_ret_postfix>` | -> | { -- } |
| 567 | `<char_ret_postfix>` | -> | { id } |
| 568 | `<char_ret_postfix>` | -> | { ( } |
| 569 | `<char_ret_postfix>` | -> | { char } |
| 570 | `<string_return_expr>` | -> | { !, (, ++, --, id, string, stringlit } |
| 571 | `<string_ret_assign>` | -> | { !, (, ++, --, id, string, stringlit } |
| 572 | `<string_ret_concat>` | -> | { !, (, ++, --, id, string, stringlit } |
| 573 | `<string_ret_or>` | -> | { !, (, ++, --, id, string, stringlit } |
| 574 | `<string_ret_and>` | -> | { !, (, ++, --, id, string, stringlit } |
| 575 | `<string_ret_eq>` | -> | { !, (, ++, --, id, string, stringlit } |
| 576 | `<string_ret_rel>` | -> | { !, (, ++, --, id, string, stringlit } |
| 577 | `<string_ret_add>` | -> | { !, (, ++, --, id, string, stringlit } |
| 578 | `<string_ret_mul>` | -> | { !, (, ++, --, id, string, stringlit } |
| 579 | `<string_ret_unary>` | -> | { ! } |
| 580 | `<string_ret_unary>` | -> | { (, ++, --, id, string, stringlit } |
| 581 | `<string_ret_postfix>` | -> | { stringlit } |
| 582 | `<string_ret_postfix>` | -> | { ++ } |
| 583 | `<string_ret_postfix>` | -> | { -- } |
| 584 | `<string_ret_postfix>` | -> | { id } |
| 585 | `<string_ret_postfix>` | -> | { ( } |
| 586 | `<string_ret_postfix>` | -> | { string } |
| 587 | `<bool_return_expr>` | -> | { !, (, ++, --, bool, false, id, true } |
| 588 | `<bool_ret_assign>` | -> | { !, (, ++, --, bool, false, id, true } |
| 589 | `<bool_ret_concat>` | -> | { !, (, ++, --, bool, false, id, true } |
| 590 | `<bool_ret_or>` | -> | { !, (, ++, --, bool, false, id, true } |
| 591 | `<bool_ret_and>` | -> | { !, (, ++, --, bool, false, id, true } |
| 592 | `<bool_ret_eq>` | -> | { !, (, ++, --, bool, false, id, true } |
| 593 | `<bool_ret_rel>` | -> | { !, (, ++, --, bool, false, id, true } |
| 594 | `<bool_ret_add>` | -> | { !, (, ++, --, bool, false, id, true } |
| 595 | `<bool_ret_mul>` | -> | { !, (, ++, --, bool, false, id, true } |
| 596 | `<bool_ret_unary>` | -> | { ! } |
| 597 | `<bool_ret_unary>` | -> | { (, ++, --, bool, false, id, true } |
| 598 | `<bool_ret_postfix>` | -> | { true } |
| 599 | `<bool_ret_postfix>` | -> | { false } |
| 600 | `<bool_ret_postfix>` | -> | { ++ } |
| 601 | `<bool_ret_postfix>` | -> | { -- } |
| 602 | `<bool_ret_postfix>` | -> | { id } |
| 603 | `<bool_ret_postfix>` | -> | { ( } |
| 604 | `<bool_ret_postfix>` | -> | { bool } |
| 605 | `<using_cont>` | -> | { , } |
| 606 | `<using_cont>` | -> | { λ } |
| 607 | `<local_dec_body>` | -> | { int } |
| 608 | `<local_dec_body>` | -> | { long } |
| 609 | `<local_dec_body>` | -> | { float } |
| 610 | `<local_dec_body>` | -> | { double } |
| 611 | `<local_dec_body>` | -> | { char } |
| 612 | `<local_dec_body>` | -> | { string } |
| 613 | `<local_dec_body>` | -> | { bool } |
| 614 | `<local_dec_body>` | -> | { id } |
| 615 | `<int_local_tail>` | -> | { [ } |
| 616 | `<int_local_tail>` | -> | { = } |
| 617 | `<int_local_cont>` | -> | { , } |
| 618 | `<int_local_cont>` | -> | { λ } |
| 619 | `<long_local_tail>` | -> | { [ } |
| 620 | `<long_local_tail>` | -> | { = } |
| 621 | `<long_local_cont>` | -> | { , } |
| 622 | `<long_local_cont>` | -> | { λ } |
| 623 | `<float_local_tail>` | -> | { [ } |
| 624 | `<float_local_tail>` | -> | { = } |
| 625 | `<float_local_cont>` | -> | { , } |
| 626 | `<float_local_cont>` | -> | { λ } |
| 627 | `<double_local_tail>` | -> | { [ } |
| 628 | `<double_local_tail>` | -> | { = } |
| 629 | `<double_local_cont>` | -> | { , } |
| 630 | `<double_local_cont>` | -> | { λ } |
| 631 | `<char_local_tail>` | -> | { [ } |
| 632 | `<char_local_tail>` | -> | { = } |
| 633 | `<char_local_cont>` | -> | { , } |
| 634 | `<char_local_cont>` | -> | { λ } |
| 635 | `<string_local_tail>` | -> | { [ } |
| 636 | `<string_local_tail>` | -> | { = } |
| 637 | `<string_local_cont>` | -> | { , } |
| 638 | `<string_local_cont>` | -> | { λ } |
| 639 | `<bool_local_tail>` | -> | { [ } |
| 640 | `<bool_local_tail>` | -> | { = } |
| 641 | `<bool_local_cont>` | -> | { , } |
| 642 | `<bool_local_cont>` | -> | { λ } |
| 643 | `<weave_local_tail>` | -> | { = } |
| 644 | `<weave_local_tail>` | -> | { [ } |
| 645 | `<statement_non_return>` | -> | { ++, --, id } |
| 646 | `<statement_non_return>` | -> | { thread, threadln, trap } |
| 647 | `<statement_non_return>` | -> | { do, for, if, switch, while } |
| 648 | `<statement_non_return>` | -> | { break } |
| 649 | `<ctrl_stmt_list>` | -> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 650 | `<ctrl_stmt_list>` | -> | { λ } |
| 651 | `<effect_stmt>` | -> | { ++ } |
| 652 | `<effect_stmt>` | -> | { -- } |
| 653 | `<effect_stmt>` | -> | { id } |
| 654 | `<effect_pre_chain>` | -> | { [ } |
| 655 | `<effect_pre_chain>` | -> | { . } |
| 656 | `<effect_pre_chain>` | -> | { λ } |
| 657 | `<effect_pre_arr_chain>` | -> | { [ } |
| 658 | `<effect_pre_arr_chain>` | -> | { . } |
| 659 | `<effect_pre_arr_chain>` | -> | { λ } |
| 660 | `<effect_id_cont>` | -> | { %=, *=, +=, -=, /=, = } |
| 661 | `<effect_id_cont>` | -> | { ++ } |
| 662 | `<effect_id_cont>` | -> | { -- } |
| 663 | `<effect_id_cont>` | -> | { ( } |
| 664 | `<effect_id_cont>` | -> | { [ } |
| 665 | `<effect_id_cont>` | -> | { . } |
| 666 | `<effect_post_call>` | -> | { . } |
| 667 | `<effect_post_call>` | -> | { [ } |
| 668 | `<effect_post_call>` | -> | { λ } |
| 669 | `<effect_post_call_member>` | -> | { ( } |
| 670 | `<effect_post_call_member>` | -> | { [ } |
| 671 | `<effect_post_call_member>` | -> | { . } |
| 672 | `<effect_post_call_member>` | -> | { λ } |
| 673 | `<effect_post_call_arr>` | -> | { [ } |
| 674 | `<effect_post_call_arr>` | -> | { (, ., λ } |
| 675 | `<effect_post_call_arr_cont>` | -> | { . } |
| 676 | `<effect_post_call_arr_cont>` | -> | { ( } |
| 677 | `<effect_post_call_arr_cont>` | -> | { λ } |
| 678 | `<effect_post_arr>` | -> | { [ } |
| 679 | `<effect_post_arr>` | -> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 680 | `<effect_post_arr_2d>` | -> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 681 | `<effect_arr_effect>` | -> | { %=, *=, +=, -=, /=, = } |
| 682 | `<effect_arr_effect>` | -> | { ++ } |
| 683 | `<effect_arr_effect>` | -> | { -- } |
| 684 | `<effect_arr_effect>` | -> | { ( } |
| 685 | `<effect_arr_effect>` | -> | { . } |
| 686 | `<effect_post_member>` | -> | { %=, *=, +=, -=, /=, = } |
| 687 | `<effect_post_member>` | -> | { ++ } |
| 688 | `<effect_post_member>` | -> | { -- } |
| 689 | `<effect_post_member>` | -> | { ( } |
| 690 | `<effect_post_member>` | -> | { [ } |
| 691 | `<effect_post_member>` | -> | { . } |
| 692 | `<stmt_assign_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 693 | `<stmt_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 694 | `<stmt_assign_tail>` | -> | { λ } |
| 695 | `<stmt_concat_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 696 | `<stmt_concat_tail>` | -> | { .. } |
| 697 | `<stmt_concat_tail>` | -> | { λ } |
| 698 | `<stmt_or_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 699 | `<stmt_or_tail>` | -> | { \|\| } |
| 700 | `<stmt_or_tail>` | -> | { λ } |
| 701 | `<stmt_and_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 702 | `<stmt_and_tail>` | -> | { && } |
| 703 | `<stmt_and_tail>` | -> | { λ } |
| 704 | `<stmt_eq_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 705 | `<stmt_eq_tail>` | -> | { == } |
| 706 | `<stmt_eq_tail>` | -> | { != } |
| 707 | `<stmt_eq_tail>` | -> | { λ } |
| 708 | `<stmt_rel_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 709 | `<stmt_rel_tail>` | -> | { < } |
| 710 | `<stmt_rel_tail>` | -> | { > } |
| 711 | `<stmt_rel_tail>` | -> | { <= } |
| 712 | `<stmt_rel_tail>` | -> | { >= } |
| 713 | `<stmt_rel_tail>` | -> | { λ } |
| 714 | `<stmt_add_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 715 | `<stmt_add_tail>` | -> | { + } |
| 716 | `<stmt_add_tail>` | -> | { - } |
| 717 | `<stmt_add_tail>` | -> | { λ } |
| 718 | `<stmt_mul_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 719 | `<stmt_mul_tail>` | -> | { * } |
| 720 | `<stmt_mul_tail>` | -> | { / } |
| 721 | `<stmt_mul_tail>` | -> | { % } |
| 722 | `<stmt_mul_tail>` | -> | { λ } |
| 723 | `<stmt_unary_expr>` | -> | { ! } |
| 724 | `<stmt_unary_expr>` | -> | { - } |
| 725 | `<stmt_unary_expr>` | -> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 726 | `<stmt_postfix_expr>` | -> | { ( } |
| 727 | `<stmt_postfix_expr>` | -> | { int } |
| 728 | `<stmt_postfix_expr>` | -> | { long } |
| 729 | `<stmt_postfix_expr>` | -> | { float } |
| 730 | `<stmt_postfix_expr>` | -> | { double } |
| 731 | `<stmt_postfix_expr>` | -> | { char } |
| 732 | `<stmt_postfix_expr>` | -> | { string } |
| 733 | `<stmt_postfix_expr>` | -> | { bool } |
| 734 | `<stmt_postfix_expr>` | -> | { ++ } |
| 735 | `<stmt_postfix_expr>` | -> | { -- } |
| 736 | `<stmt_postfix_expr>` | -> | { id } |
| 737 | `<stmt_postfix_expr>` | -> | { intlit } |
| 738 | `<stmt_postfix_expr>` | -> | { longlit } |
| 739 | `<stmt_postfix_expr>` | -> | { floatlit } |
| 740 | `<stmt_postfix_expr>` | -> | { doublelit } |
| 741 | `<stmt_postfix_expr>` | -> | { charlit } |
| 742 | `<stmt_postfix_expr>` | -> | { stringlit } |
| 743 | `<stmt_postfix_expr>` | -> | { true } |
| 744 | `<stmt_postfix_expr>` | -> | { false } |
| 745 | `<stmt_id_postfix>` | -> | { ++ } |
| 746 | `<stmt_id_postfix>` | -> | { -- } |
| 747 | `<stmt_id_postfix>` | -> | { (, ., [, λ } |
| 748 | `<stmt_postfix_chain>` | -> | { [ } |
| 749 | `<stmt_postfix_chain>` | -> | { . } |
| 750 | `<stmt_postfix_chain>` | -> | { ( } |
| 751 | `<stmt_postfix_chain>` | -> | { λ } |
| 752 | `<stmt_array_access>` | -> | { [ } |
| 753 | `<stmt_array_access_dim2>` | -> | { [ } |
| 754 | `<stmt_array_access_dim2>` | -> | { λ } |
| 755 | `<stmt_postfix_after_arr>` | -> | { . } |
| 756 | `<stmt_postfix_after_arr>` | -> | { ( } |
| 757 | `<stmt_postfix_after_arr>` | -> | { λ } |
| 758 | `<stmt_array_index>` | -> | { intlit } |
| 759 | `<stmt_array_index>` | -> | { id } |
| 760 | `<stmt_arg_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 761 | `<stmt_arg_list>` | -> | { λ } |
| 762 | `<stmt_arg_tail>` | -> | { , } |
| 763 | `<stmt_arg_tail>` | -> | { λ } |
| 764 | `<arg_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 765 | `<arg_assign_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 766 | `<arg_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 767 | `<arg_assign_tail>` | -> | { λ } |
| 768 | `<arg_concat_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 769 | `<arg_concat_tail>` | -> | { .. } |
| 770 | `<arg_concat_tail>` | -> | { λ } |
| 771 | `<arg_or_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 772 | `<arg_or_tail>` | -> | { \|\| } |
| 773 | `<arg_or_tail>` | -> | { λ } |
| 774 | `<arg_and_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 775 | `<arg_and_tail>` | -> | { && } |
| 776 | `<arg_and_tail>` | -> | { λ } |
| 777 | `<arg_eq_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 778 | `<arg_eq_tail>` | -> | { == } |
| 779 | `<arg_eq_tail>` | -> | { != } |
| 780 | `<arg_eq_tail>` | -> | { λ } |
| 781 | `<arg_rel_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 782 | `<arg_rel_tail>` | -> | { < } |
| 783 | `<arg_rel_tail>` | -> | { > } |
| 784 | `<arg_rel_tail>` | -> | { <= } |
| 785 | `<arg_rel_tail>` | -> | { >= } |
| 786 | `<arg_rel_tail>` | -> | { λ } |
| 787 | `<arg_add_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 788 | `<arg_add_tail>` | -> | { + } |
| 789 | `<arg_add_tail>` | -> | { - } |
| 790 | `<arg_add_tail>` | -> | { λ } |
| 791 | `<arg_mul_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 792 | `<arg_mul_tail>` | -> | { * } |
| 793 | `<arg_mul_tail>` | -> | { / } |
| 794 | `<arg_mul_tail>` | -> | { % } |
| 795 | `<arg_mul_tail>` | -> | { λ } |
| 796 | `<arg_unary_expr>` | -> | { ! } |
| 797 | `<arg_unary_expr>` | -> | { - } |
| 798 | `<arg_unary_expr>` | -> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 799 | `<arg_postfix_expr>` | -> | { ( } |
| 800 | `<arg_postfix_expr>` | -> | { int } |
| 801 | `<arg_postfix_expr>` | -> | { long } |
| 802 | `<arg_postfix_expr>` | -> | { float } |
| 803 | `<arg_postfix_expr>` | -> | { double } |
| 804 | `<arg_postfix_expr>` | -> | { char } |
| 805 | `<arg_postfix_expr>` | -> | { string } |
| 806 | `<arg_postfix_expr>` | -> | { bool } |
| 807 | `<arg_postfix_expr>` | -> | { ++ } |
| 808 | `<arg_postfix_expr>` | -> | { -- } |
| 809 | `<arg_postfix_expr>` | -> | { id } |
| 810 | `<arg_postfix_expr>` | -> | { intlit } |
| 811 | `<arg_postfix_expr>` | -> | { longlit } |
| 812 | `<arg_postfix_expr>` | -> | { floatlit } |
| 813 | `<arg_postfix_expr>` | -> | { doublelit } |
| 814 | `<arg_postfix_expr>` | -> | { charlit } |
| 815 | `<arg_postfix_expr>` | -> | { stringlit } |
| 816 | `<arg_postfix_expr>` | -> | { true } |
| 817 | `<arg_postfix_expr>` | -> | { false } |
| 818 | `<arg_id_postfix>` | -> | { ++ } |
| 819 | `<arg_id_postfix>` | -> | { -- } |
| 820 | `<arg_id_postfix>` | -> | { (, ., [, λ } |
| 821 | `<arg_postfix_chain>` | -> | { [ } |
| 822 | `<arg_postfix_chain>` | -> | { . } |
| 823 | `<arg_postfix_chain>` | -> | { ( } |
| 824 | `<arg_postfix_chain>` | -> | { λ } |
| 825 | `<arg_array_access>` | -> | { [ } |
| 826 | `<arg_array_access_dim2>` | -> | { [ } |
| 827 | `<arg_array_access_dim2>` | -> | { λ } |
| 828 | `<arg_postfix_after_arr>` | -> | { . } |
| 829 | `<arg_postfix_after_arr>` | -> | { ( } |
| 830 | `<arg_postfix_after_arr>` | -> | { λ } |
| 831 | `<arg_array_index>` | -> | { intlit } |
| 832 | `<arg_array_index>` | -> | { id } |
| 833 | `<arg_nested_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 834 | `<arg_nested_list>` | -> | { λ } |
| 835 | `<arg_nested_tail>` | -> | { , } |
| 836 | `<arg_nested_tail>` | -> | { λ } |
| 837 | `<expression>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 838 | `<assign_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 839 | `<assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 840 | `<assign_tail>` | -> | { λ } |
| 841 | `<assign_op>` | -> | { = } |
| 842 | `<assign_op>` | -> | { += } |
| 843 | `<assign_op>` | -> | { -= } |
| 844 | `<assign_op>` | -> | { *= } |
| 845 | `<assign_op>` | -> | { /= } |
| 846 | `<assign_op>` | -> | { %= } |
| 847 | `<concat_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 848 | `<concat_tail>` | -> | { .. } |
| 849 | `<concat_tail>` | -> | { λ } |
| 850 | `<or_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 851 | `<or_tail>` | -> | { \|\| } |
| 852 | `<or_tail>` | -> | { λ } |
| 853 | `<and_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 854 | `<and_tail>` | -> | { && } |
| 855 | `<and_tail>` | -> | { λ } |
| 856 | `<eq_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 857 | `<eq_tail>` | -> | { == } |
| 858 | `<eq_tail>` | -> | { != } |
| 859 | `<eq_tail>` | -> | { λ } |
| 860 | `<rel_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 861 | `<rel_tail>` | -> | { < } |
| 862 | `<rel_tail>` | -> | { > } |
| 863 | `<rel_tail>` | -> | { <= } |
| 864 | `<rel_tail>` | -> | { >= } |
| 865 | `<rel_tail>` | -> | { λ } |
| 866 | `<add_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 867 | `<add_tail>` | -> | { + } |
| 868 | `<add_tail>` | -> | { - } |
| 869 | `<add_tail>` | -> | { λ } |
| 870 | `<mul_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 871 | `<mul_tail>` | -> | { * } |
| 872 | `<mul_tail>` | -> | { / } |
| 873 | `<mul_tail>` | -> | { % } |
| 874 | `<mul_tail>` | -> | { λ } |
| 875 | `<unary_expr>` | -> | { ! } |
| 876 | `<unary_expr>` | -> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 877 | `<postfix_expr>` | -> | { ( } |
| 878 | `<postfix_expr>` | -> | { int } |
| 879 | `<postfix_expr>` | -> | { long } |
| 880 | `<postfix_expr>` | -> | { float } |
| 881 | `<postfix_expr>` | -> | { double } |
| 882 | `<postfix_expr>` | -> | { char } |
| 883 | `<postfix_expr>` | -> | { string } |
| 884 | `<postfix_expr>` | -> | { bool } |
| 885 | `<postfix_expr>` | -> | { ++ } |
| 886 | `<postfix_expr>` | -> | { -- } |
| 887 | `<postfix_expr>` | -> | { id } |
| 888 | `<postfix_expr>` | -> | { intlit } |
| 889 | `<postfix_expr>` | -> | { longlit } |
| 890 | `<postfix_expr>` | -> | { floatlit } |
| 891 | `<postfix_expr>` | -> | { doublelit } |
| 892 | `<postfix_expr>` | -> | { charlit } |
| 893 | `<postfix_expr>` | -> | { stringlit } |
| 894 | `<postfix_expr>` | -> | { true } |
| 895 | `<postfix_expr>` | -> | { false } |
| 896 | `<id_postfix>` | -> | { ++ } |
| 897 | `<id_postfix>` | -> | { -- } |
| 898 | `<id_postfix>` | -> | { (, ., [, λ } |
| 899 | `<postfix_chain>` | -> | { [ } |
| 900 | `<postfix_chain>` | -> | { . } |
| 901 | `<postfix_chain>` | -> | { ( } |
| 902 | `<postfix_chain>` | -> | { λ } |
| 903 | `<array_access>` | -> | { [ } |
| 904 | `<array_access_dim2>` | -> | { [ } |
| 905 | `<array_access_dim2>` | -> | { λ } |
| 906 | `<postfix_after_arr>` | -> | { . } |
| 907 | `<postfix_after_arr>` | -> | { ( } |
| 908 | `<postfix_after_arr>` | -> | { λ } |
| 909 | `<array_index>` | -> | { intlit } |
| 910 | `<array_index>` | -> | { id } |
| 911 | `<arg_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 912 | `<arg_list>` | -> | { λ } |
| 913 | `<arg_tail>` | -> | { , } |
| 914 | `<arg_tail>` | -> | { λ } |
| 915 | `<io_stmt>` | -> | { trap } |
| 916 | `<io_stmt>` | -> | { thread } |
| 917 | `<io_stmt>` | -> | { threadln } |
| 918 | `<print_args>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 919 | `<print_tail>` | -> | { , } |
| 920 | `<print_tail>` | -> | { λ } |
| 921 | `<ctrl_struct>` | -> | { if } |
| 922 | `<ctrl_struct>` | -> | { switch } |
| 923 | `<ctrl_struct>` | -> | { for } |
| 924 | `<ctrl_struct>` | -> | { while } |
| 925 | `<ctrl_struct>` | -> | { do } |
| 926 | `<else_opt>` | -> | { else } |
| 927 | `<else_opt>` | -> | { λ } |
| 928 | `<else_body>` | -> | { { } |
| 929 | `<else_body>` | -> | { if } |
| 930 | `<case_list>` | -> | { case } |
| 931 | `<case_list>` | -> | { λ } |
| 932 | `<case_val>` | -> | { intlit } |
| 933 | `<case_val>` | -> | { longlit } |
| 934 | `<case_val>` | -> | { charlit } |
| 935 | `<case_val>` | -> | { true } |
| 936 | `<case_val>` | -> | { false } |
| 937 | `<default_opt>` | -> | { default } |
| 938 | `<default_opt>` | -> | { λ } |
| 939 | `<break_opt>` | -> | { break } |
| 940 | `<break_opt>` | -> | { λ } |
| 941 | `<for_init>` | -> | { local } |
| 942 | `<for_init>` | -> | { id } |
| 943 | `<for_init>` | -> | { λ } |
| 944 | `<for_init_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 945 | `<for_init_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 946 | `<for_init_type>` | -> | { int } |
| 947 | `<for_init_type>` | -> | { long } |
| 948 | `<for_init_type>` | -> | { float } |
| 949 | `<for_init_type>` | -> | { double } |
| 950 | `<for_init_type>` | -> | { char } |
| 951 | `<for_init_type>` | -> | { string } |
| 952 | `<for_init_type>` | -> | { bool } |
| 953 | `<for_cond>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 954 | `<for_update>` | -> | { id } |
| 955 | `<for_update>` | -> | { ++ } |
| 956 | `<for_update>` | -> | { -- } |
| 957 | `<for_update>` | -> | { λ } |
| 958 | `<for_update_tail>` | -> | { ++ } |
| 959 | `<for_update_tail>` | -> | { -- } |
| 960 | `<for_update_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 961 | `<condition>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 962 | `<cond_or>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 963 | `<cond_or_tail>` | -> | { \|\| } |
| 964 | `<cond_or_tail>` | -> | { λ } |
| 965 | `<cond_and>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 966 | `<cond_and_tail>` | -> | { && } |
| 967 | `<cond_and_tail>` | -> | { λ } |
| 968 | `<cond_comparison>` | -> | { ( } |
| 969 | `<cond_comparison>` | -> | { ! } |
| 970 | `<cond_comparison>` | -> | { ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 971 | `<cond_primary>` | -> | { - } |
| 972 | `<cond_primary>` | -> | { ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 973 | `<cond_primary_continue>` | -> | { + } |
| 974 | `<cond_primary_continue>` | -> | { - } |
| 975 | `<cond_primary_continue>` | -> | { * } |
| 976 | `<cond_primary_continue>` | -> | { / } |
| 977 | `<cond_primary_continue>` | -> | { % } |
| 978 | `<cond_primary_continue>` | -> | { !=, <, <=, ==, >, >= } |
| 979 | `<cond_primary_continue>` | -> | { λ } |
| 980 | `<cond_must_commit>` | -> | { + } |
| 981 | `<cond_must_commit>` | -> | { - } |
| 982 | `<cond_must_commit>` | -> | { * } |
| 983 | `<cond_must_commit>` | -> | { / } |
| 984 | `<cond_must_commit>` | -> | { % } |
| 985 | `<cond_must_commit>` | -> | { !=, <, <=, ==, >, >= } |
| 986 | `<cond_postfix>` | -> | { int } |
| 987 | `<cond_postfix>` | -> | { long } |
| 988 | `<cond_postfix>` | -> | { float } |
| 989 | `<cond_postfix>` | -> | { double } |
| 990 | `<cond_postfix>` | -> | { char } |
| 991 | `<cond_postfix>` | -> | { string } |
| 992 | `<cond_postfix>` | -> | { bool } |
| 993 | `<cond_postfix>` | -> | { ++ } |
| 994 | `<cond_postfix>` | -> | { -- } |
| 995 | `<cond_postfix>` | -> | { id } |
| 996 | `<cond_postfix>` | -> | { intlit } |
| 997 | `<cond_postfix>` | -> | { longlit } |
| 998 | `<cond_postfix>` | -> | { floatlit } |
| 999 | `<cond_postfix>` | -> | { doublelit } |
| 1000 | `<cond_postfix>` | -> | { charlit } |
| 1001 | `<cond_postfix>` | -> | { stringlit } |
| 1002 | `<cond_postfix>` | -> | { true } |
| 1003 | `<cond_postfix>` | -> | { false } |
| 1004 | `<cond_cast_arg>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1005 | `<cond_id_post>` | -> | { ++ } |
| 1006 | `<cond_id_post>` | -> | { -- } |
| 1007 | `<cond_id_post>` | -> | { (, ., [, λ } |
| 1008 | `<cond_post_chain>` | -> | { [ } |
| 1009 | `<cond_post_chain>` | -> | { . } |
| 1010 | `<cond_post_chain>` | -> | { ( } |
| 1011 | `<cond_post_chain>` | -> | { λ } |
| 1012 | `<cond_arr_access>` | -> | { [ } |
| 1013 | `<cond_arr_access_dim2>` | -> | { [ } |
| 1014 | `<cond_arr_access_dim2>` | -> | { λ } |
| 1015 | `<cond_post_after_arr>` | -> | { . } |
| 1016 | `<cond_post_after_arr>` | -> | { ( } |
| 1017 | `<cond_post_after_arr>` | -> | { λ } |
| 1018 | `<cond_arr_index>` | -> | { intlit } |
| 1019 | `<cond_arr_index>` | -> | { id } |
| 1020 | `<cond_rhs>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1021 | `<comp_op>` | -> | { == } |
| 1022 | `<comp_op>` | -> | { != } |
| 1023 | `<comp_op>` | -> | { < } |
| 1024 | `<comp_op>` | -> | { > } |
| 1025 | `<comp_op>` | -> | { <= } |
| 1026 | `<comp_op>` | -> | { >= } |
| 1027 | `<main_body>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 1028 | `<main_content>` | -> | { using } |
| 1029 | `<main_content>` | -> | { local } |
| 1030 | `<main_content>` | -> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1031 | `<main_content>` | -> | { return } |