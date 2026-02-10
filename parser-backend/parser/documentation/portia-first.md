## FIRST Set

| # | Production | -> | FIRST Set |
|---|------------|-----|-----------|
| 1 | `<program>` | -> | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 2 | `<decl_list>` | -> | { int } |
| 3 | `<decl_list>` | -> | { bool, char, double, float, func, global, id, long, string, weave } |
| 4 | `<int_decl_or_main>` | -> | { id } |
| 5 | `<int_decl_or_main>` | -> | { main } |
| 6 | `<other_decl>` | -> | { global } |
| 7 | `<other_decl>` | -> | { global } |
| 8 | `<other_decl>` | -> | { global } |
| 9 | `<other_decl>` | -> | { global } |
| 10 | `<other_decl>` | -> | { global } |
| 11 | `<other_decl>` | -> | { global } |
| 12 | `<other_decl>` | -> | { global } |
| 13 | `<other_decl>` | -> | { long } |
| 14 | `<other_decl>` | -> | { float } |
| 15 | `<other_decl>` | -> | { double } |
| 16 | `<other_decl>` | -> | { char } |
| 17 | `<other_decl>` | -> | { string } |
| 18 | `<other_decl>` | -> | { bool } |
| 19 | `<other_decl>` | -> | { weave } |
| 20 | `<other_decl>` | -> | { id } |
| 21 | `<other_decl>` | -> | { func } |
| 22 | `<other_decl>` | -> | { func } |
| 23 | `<other_decl>` | -> | { func } |
| 24 | `<other_decl>` | -> | { func } |
| 25 | `<other_decl>` | -> | { func } |
| 26 | `<other_decl>` | -> | { func } |
| 27 | `<other_decl>` | -> | { func } |
| 28 | `<other_decl>` | -> | { func } |
| 29 | `<other_decl>` | -> | { func } |
| 30 | `<bool_lit>` | -> | { true } |
| 31 | `<bool_lit>` | -> | { false } |
| 32 | `<int_global_cont>` | -> | { , } |
| 33 | `<int_global_cont>` | -> | { λ } |
| 34 | `<long_global_cont>` | -> | { , } |
| 35 | `<long_global_cont>` | -> | { λ } |
| 36 | `<float_global_cont>` | -> | { , } |
| 37 | `<float_global_cont>` | -> | { λ } |
| 38 | `<double_global_cont>` | -> | { , } |
| 39 | `<double_global_cont>` | -> | { λ } |
| 40 | `<char_global_cont>` | -> | { , } |
| 41 | `<char_global_cont>` | -> | { λ } |
| 42 | `<string_global_cont>` | -> | { , } |
| 43 | `<string_global_cont>` | -> | { λ } |
| 44 | `<bool_global_cont>` | -> | { , } |
| 45 | `<bool_global_cont>` | -> | { λ } |
| 46 | `<int_decl_tail>` | -> | { [ } |
| 47 | `<int_decl_tail>` | -> | { = } |
| 48 | `<int_multi_decl>` | -> | { , } |
| 49 | `<int_multi_decl>` | -> | { λ } |
| 50 | `<long_decl_tail>` | -> | { [ } |
| 51 | `<long_decl_tail>` | -> | { = } |
| 52 | `<long_multi_decl>` | -> | { , } |
| 53 | `<long_multi_decl>` | -> | { λ } |
| 54 | `<float_decl_tail>` | -> | { [ } |
| 55 | `<float_decl_tail>` | -> | { = } |
| 56 | `<float_multi_decl>` | -> | { , } |
| 57 | `<float_multi_decl>` | -> | { λ } |
| 58 | `<double_decl_tail>` | -> | { [ } |
| 59 | `<double_decl_tail>` | -> | { = } |
| 60 | `<double_multi_decl>` | -> | { , } |
| 61 | `<double_multi_decl>` | -> | { λ } |
| 62 | `<char_decl_tail>` | -> | { [ } |
| 63 | `<char_decl_tail>` | -> | { = } |
| 64 | `<char_multi_decl>` | -> | { , } |
| 65 | `<char_multi_decl>` | -> | { λ } |
| 66 | `<string_decl_tail>` | -> | { [ } |
| 67 | `<string_decl_tail>` | -> | { = } |
| 68 | `<string_multi_decl>` | -> | { , } |
| 69 | `<string_multi_decl>` | -> | { λ } |
| 70 | `<bool_decl_tail>` | -> | { [ } |
| 71 | `<bool_decl_tail>` | -> | { = } |
| 72 | `<bool_multi_decl>` | -> | { , } |
| 73 | `<bool_multi_decl>` | -> | { λ } |
| 74 | `<weave_inst_decl>` | -> | { id } |
| 75 | `<weave_inst_decl>` | -> | { [ } |
| 76 | `<weave_inst_tail>` | -> | { = } |
| 77 | `<weave_inst_tail>` | -> | { [ } |
| 78 | `<weave_field_value>` | -> | { intlit } |
| 79 | `<weave_field_value>` | -> | { longlit } |
| 80 | `<weave_field_value>` | -> | { floatlit } |
| 81 | `<weave_field_value>` | -> | { doublelit } |
| 82 | `<weave_field_value>` | -> | { charlit } |
| 83 | `<weave_field_value>` | -> | { stringlit } |
| 84 | `<weave_field_value>` | -> | { true } |
| 85 | `<weave_field_value>` | -> | { false } |
| 86 | `<weave_field_value>` | -> | { { } |
| 87 | `<weave_value_list>` | -> | { charlit, doublelit, false, floatlit, intlit, longlit, stringlit, true, { } |
| 88 | `<weave_value_tail>` | -> | { , } |
| 89 | `<weave_value_tail>` | -> | { λ } |
| 90 | `<weave_field_list_tail>` | -> | { , } |
| 91 | `<weave_field_list_tail>` | -> | { λ } |
| 92 | `<weave_inst_cont>` | -> | { , } |
| 93 | `<weave_inst_cont>` | -> | { λ } |
| 94 | `<weave_arr_cont>` | -> | { , } |
| 95 | `<weave_arr_cont>` | -> | { λ } |
| 96 | `<weave_array_with_init>` | -> | { [ } |
| 97 | `<weave_array_init_tail>` | -> | { [ } |
| 98 | `<weave_array_init_tail>` | -> | { =, λ } |
| 99 | `<weave_arr_init_opt_1d>` | -> | { = } |
| 100 | `<weave_arr_init_opt_1d>` | -> | { λ } |
| 101 | `<weave_arr_init_content_1d>` | -> | { { } |
| 102 | `<weave_init_1d_tail>` | -> | { , } |
| 103 | `<weave_init_1d_tail>` | -> | { λ } |
| 104 | `<weave_arr_init_opt_2d>` | -> | { = } |
| 105 | `<weave_arr_init_opt_2d>` | -> | { λ } |
| 106 | `<weave_arr_init_content_2d>` | -> | { { } |
| 107 | `<weave_init_row>` | -> | { { } |
| 108 | `<weave_init_2d_tail>` | -> | { , } |
| 109 | `<weave_init_2d_tail>` | -> | { λ } |
| 110 | `<mutability>` | -> | { var } |
| 111 | `<mutability>` | -> | { const } |
| 112 | `<array_dims>` | -> | { [ } |
| 113 | `<array_dim2_opt>` | -> | { [ } |
| 114 | `<array_dim2_opt>` | -> | { λ } |
| 115 | `<size>` | -> | { intlit } |
| 116 | `<size>` | -> | { id } |
| 117 | `<int_array_with_init>` | -> | { [ } |
| 118 | `<int_array_init_tail>` | -> | { [ } |
| 119 | `<int_array_init_tail>` | -> | { =, λ } |
| 120 | `<int_arr_init_opt_1d>` | -> | { = } |
| 121 | `<int_arr_init_opt_1d>` | -> | { λ } |
| 122 | `<int_arr_init_content_1d>` | -> | { intlit } |
| 123 | `<int_elem_1d_tail>` | -> | { , } |
| 124 | `<int_elem_1d_tail>` | -> | { λ } |
| 125 | `<int_arr_init_opt_2d>` | -> | { = } |
| 126 | `<int_arr_init_opt_2d>` | -> | { λ } |
| 127 | `<int_arr_init_content_2d>` | -> | { { } |
| 128 | `<int_elem_list>` | -> | { intlit } |
| 129 | `<int_elem_2d_tail>` | -> | { , } |
| 130 | `<int_elem_2d_tail>` | -> | { λ } |
| 131 | `<long_array_with_init>` | -> | { [ } |
| 132 | `<long_array_init_tail>` | -> | { [ } |
| 133 | `<long_array_init_tail>` | -> | { =, λ } |
| 134 | `<long_arr_init_opt_1d>` | -> | { = } |
| 135 | `<long_arr_init_opt_1d>` | -> | { λ } |
| 136 | `<long_arr_init_content_1d>` | -> | { longlit } |
| 137 | `<long_elem_1d_tail>` | -> | { , } |
| 138 | `<long_elem_1d_tail>` | -> | { λ } |
| 139 | `<long_arr_init_opt_2d>` | -> | { = } |
| 140 | `<long_arr_init_opt_2d>` | -> | { λ } |
| 141 | `<long_arr_init_content_2d>` | -> | { { } |
| 142 | `<long_elem_list>` | -> | { longlit } |
| 143 | `<long_elem_2d_tail>` | -> | { , } |
| 144 | `<long_elem_2d_tail>` | -> | { λ } |
| 145 | `<float_array_with_init>` | -> | { [ } |
| 146 | `<float_array_init_tail>` | -> | { [ } |
| 147 | `<float_array_init_tail>` | -> | { =, λ } |
| 148 | `<float_arr_init_opt_1d>` | -> | { = } |
| 149 | `<float_arr_init_opt_1d>` | -> | { λ } |
| 150 | `<float_arr_init_content_1d>` | -> | { floatlit } |
| 151 | `<float_elem_1d_tail>` | -> | { , } |
| 152 | `<float_elem_1d_tail>` | -> | { λ } |
| 153 | `<float_arr_init_opt_2d>` | -> | { = } |
| 154 | `<float_arr_init_opt_2d>` | -> | { λ } |
| 155 | `<float_arr_init_content_2d>` | -> | { { } |
| 156 | `<float_elem_list>` | -> | { floatlit } |
| 157 | `<float_elem_2d_tail>` | -> | { , } |
| 158 | `<float_elem_2d_tail>` | -> | { λ } |
| 159 | `<double_array_with_init>` | -> | { [ } |
| 160 | `<double_array_init_tail>` | -> | { [ } |
| 161 | `<double_array_init_tail>` | -> | { =, λ } |
| 162 | `<double_arr_init_opt_1d>` | -> | { = } |
| 163 | `<double_arr_init_opt_1d>` | -> | { λ } |
| 164 | `<double_arr_init_content_1d>` | -> | { doublelit } |
| 165 | `<double_elem_1d_tail>` | -> | { , } |
| 166 | `<double_elem_1d_tail>` | -> | { λ } |
| 167 | `<double_arr_init_opt_2d>` | -> | { = } |
| 168 | `<double_arr_init_opt_2d>` | -> | { λ } |
| 169 | `<double_arr_init_content_2d>` | -> | { { } |
| 170 | `<double_elem_list>` | -> | { doublelit } |
| 171 | `<double_elem_2d_tail>` | -> | { , } |
| 172 | `<double_elem_2d_tail>` | -> | { λ } |
| 173 | `<char_array_with_init>` | -> | { [ } |
| 174 | `<char_array_init_tail>` | -> | { [ } |
| 175 | `<char_array_init_tail>` | -> | { =, λ } |
| 176 | `<char_arr_init_opt_1d>` | -> | { = } |
| 177 | `<char_arr_init_opt_1d>` | -> | { λ } |
| 178 | `<char_arr_init_content_1d>` | -> | { charlit } |
| 179 | `<char_elem_1d_tail>` | -> | { , } |
| 180 | `<char_elem_1d_tail>` | -> | { λ } |
| 181 | `<char_arr_init_opt_2d>` | -> | { = } |
| 182 | `<char_arr_init_opt_2d>` | -> | { λ } |
| 183 | `<char_arr_init_content_2d>` | -> | { { } |
| 184 | `<char_elem_list>` | -> | { charlit } |
| 185 | `<char_elem_2d_tail>` | -> | { , } |
| 186 | `<char_elem_2d_tail>` | -> | { λ } |
| 187 | `<string_array_with_init>` | -> | { [ } |
| 188 | `<string_array_init_tail>` | -> | { [ } |
| 189 | `<string_array_init_tail>` | -> | { =, λ } |
| 190 | `<string_arr_init_opt_1d>` | -> | { = } |
| 191 | `<string_arr_init_opt_1d>` | -> | { λ } |
| 192 | `<string_arr_init_content_1d>` | -> | { stringlit } |
| 193 | `<string_elem_1d_tail>` | -> | { , } |
| 194 | `<string_elem_1d_tail>` | -> | { λ } |
| 195 | `<string_arr_init_opt_2d>` | -> | { = } |
| 196 | `<string_arr_init_opt_2d>` | -> | { λ } |
| 197 | `<string_arr_init_content_2d>` | -> | { { } |
| 198 | `<string_elem_list>` | -> | { stringlit } |
| 199 | `<string_elem_2d_tail>` | -> | { , } |
| 200 | `<string_elem_2d_tail>` | -> | { λ } |
| 201 | `<bool_array_with_init>` | -> | { [ } |
| 202 | `<bool_array_init_tail>` | -> | { [ } |
| 203 | `<bool_array_init_tail>` | -> | { =, λ } |
| 204 | `<bool_arr_init_opt_1d>` | -> | { = } |
| 205 | `<bool_arr_init_opt_1d>` | -> | { λ } |
| 206 | `<bool_arr_init_content_1d>` | -> | { false, true } |
| 207 | `<bool_elem_1d_tail>` | -> | { , } |
| 208 | `<bool_elem_1d_tail>` | -> | { λ } |
| 209 | `<bool_arr_init_opt_2d>` | -> | { = } |
| 210 | `<bool_arr_init_opt_2d>` | -> | { λ } |
| 211 | `<bool_arr_init_content_2d>` | -> | { { } |
| 212 | `<bool_elem_list>` | -> | { false, true } |
| 213 | `<bool_elem_2d_tail>` | -> | { , } |
| 214 | `<bool_elem_2d_tail>` | -> | { λ } |
| 215 | `<field_list>` | -> | { bool, char, double, float, id, int, long, string } |
| 216 | `<field_list>` | -> | { λ } |
| 217 | `<field_dec>` | -> | { bool, char, double, float, id, int, long, string } |
| 218 | `<field_type>` | -> | { int } |
| 219 | `<field_type>` | -> | { long } |
| 220 | `<field_type>` | -> | { float } |
| 221 | `<field_type>` | -> | { double } |
| 222 | `<field_type>` | -> | { char } |
| 223 | `<field_type>` | -> | { string } |
| 224 | `<field_type>` | -> | { bool } |
| 225 | `<field_type>` | -> | { id } |
| 226 | `<field_arr_opt>` | -> | { [ } |
| 227 | `<field_arr_opt>` | -> | { λ } |
| 228 | `<field_cont>` | -> | { , } |
| 229 | `<field_cont>` | -> | { λ } |
| 230 | `<func_ret_int>` | -> | { id } |
| 231 | `<func_ret_int>` | -> | { [ } |
| 232 | `<func_ret_long>` | -> | { id } |
| 233 | `<func_ret_long>` | -> | { [ } |
| 234 | `<func_ret_float>` | -> | { id } |
| 235 | `<func_ret_float>` | -> | { [ } |
| 236 | `<func_ret_double>` | -> | { id } |
| 237 | `<func_ret_double>` | -> | { [ } |
| 238 | `<func_ret_char>` | -> | { id } |
| 239 | `<func_ret_char>` | -> | { [ } |
| 240 | `<func_ret_string>` | -> | { id } |
| 241 | `<func_ret_string>` | -> | { [ } |
| 242 | `<func_ret_bool>` | -> | { id } |
| 243 | `<func_ret_bool>` | -> | { [ } |
| 244 | `<func_ret_weave>` | -> | { id } |
| 245 | `<func_ret_weave>` | -> | { [ } |
| 246 | `<func_ret_weave>` | -> | { . } |
| 247 | `<param_list>` | -> | { bool, char, double, float, id, int, long, string } |
| 248 | `<param_list>` | -> | { λ } |
| 249 | `<param_type>` | -> | { int } |
| 250 | `<param_type>` | -> | { long } |
| 251 | `<param_type>` | -> | { float } |
| 252 | `<param_type>` | -> | { double } |
| 253 | `<param_type>` | -> | { char } |
| 254 | `<param_type>` | -> | { string } |
| 255 | `<param_type>` | -> | { bool } |
| 256 | `<param_type>` | -> | { id } |
| 257 | `<param_arr_opt>` | -> | { [ } |
| 258 | `<param_arr_opt>` | -> | { λ } |
| 259 | `<param_cont>` | -> | { , } |
| 260 | `<param_cont>` | -> | { λ } |
| 261 | `<function_body_int>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 262 | `<func_content_int>` | -> | { using } |
| 263 | `<func_content_int>` | -> | { local } |
| 264 | `<func_content_int>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 265 | `<func_content_int>` | -> | { λ } |
| 266 | `<function_body_long>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 267 | `<func_content_long>` | -> | { using } |
| 268 | `<func_content_long>` | -> | { local } |
| 269 | `<func_content_long>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 270 | `<func_content_long>` | -> | { λ } |
| 271 | `<function_body_float>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 272 | `<func_content_float>` | -> | { using } |
| 273 | `<func_content_float>` | -> | { local } |
| 274 | `<func_content_float>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 275 | `<func_content_float>` | -> | { λ } |
| 276 | `<function_body_double>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 277 | `<func_content_double>` | -> | { using } |
| 278 | `<func_content_double>` | -> | { local } |
| 279 | `<func_content_double>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 280 | `<func_content_double>` | -> | { λ } |
| 281 | `<function_body_char>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 282 | `<func_content_char>` | -> | { using } |
| 283 | `<func_content_char>` | -> | { local } |
| 284 | `<func_content_char>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 285 | `<func_content_char>` | -> | { λ } |
| 286 | `<function_body_string>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 287 | `<func_content_string>` | -> | { using } |
| 288 | `<func_content_string>` | -> | { local } |
| 289 | `<func_content_string>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 290 | `<func_content_string>` | -> | { λ } |
| 291 | `<function_body_bool>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 292 | `<func_content_bool>` | -> | { using } |
| 293 | `<func_content_bool>` | -> | { local } |
| 294 | `<func_content_bool>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 295 | `<func_content_bool>` | -> | { λ } |
| 296 | `<function_body_array>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 297 | `<func_content_array>` | -> | { using } |
| 298 | `<func_content_array>` | -> | { local } |
| 299 | `<func_content_array>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 300 | `<func_content_array>` | -> | { λ } |
| 301 | `<function_body_weave>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 302 | `<func_content_weave>` | -> | { using } |
| 303 | `<func_content_weave>` | -> | { local } |
| 304 | `<func_content_weave>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 305 | `<func_content_weave>` | -> | { λ } |
| 306 | `<function_body_void>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, λ } |
| 307 | `<func_content_void>` | -> | { using } |
| 308 | `<func_content_void>` | -> | { local } |
| 309 | `<func_content_void>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 310 | `<func_content_void>` | -> | { λ } |
| 311 | `<statement_int>` | -> | { ++, --, id } |
| 312 | `<statement_int>` | -> | { thread, threadln, trap } |
| 313 | `<statement_int>` | -> | { do, for, if, switch, while } |
| 314 | `<statement_int>` | -> | { break } |
| 315 | `<statement_int>` | -> | { return } |
| 316 | `<statement_long>` | -> | { ++, --, id } |
| 317 | `<statement_long>` | -> | { thread, threadln, trap } |
| 318 | `<statement_long>` | -> | { do, for, if, switch, while } |
| 319 | `<statement_long>` | -> | { break } |
| 320 | `<statement_long>` | -> | { return } |
| 321 | `<statement_float>` | -> | { ++, --, id } |
| 322 | `<statement_float>` | -> | { thread, threadln, trap } |
| 323 | `<statement_float>` | -> | { do, for, if, switch, while } |
| 324 | `<statement_float>` | -> | { break } |
| 325 | `<statement_float>` | -> | { return } |
| 326 | `<statement_double>` | -> | { ++, --, id } |
| 327 | `<statement_double>` | -> | { thread, threadln, trap } |
| 328 | `<statement_double>` | -> | { do, for, if, switch, while } |
| 329 | `<statement_double>` | -> | { break } |
| 330 | `<statement_double>` | -> | { return } |
| 331 | `<statement_char>` | -> | { ++, --, id } |
| 332 | `<statement_char>` | -> | { thread, threadln, trap } |
| 333 | `<statement_char>` | -> | { do, for, if, switch, while } |
| 334 | `<statement_char>` | -> | { break } |
| 335 | `<statement_char>` | -> | { return } |
| 336 | `<statement_string>` | -> | { ++, --, id } |
| 337 | `<statement_string>` | -> | { thread, threadln, trap } |
| 338 | `<statement_string>` | -> | { do, for, if, switch, while } |
| 339 | `<statement_string>` | -> | { break } |
| 340 | `<statement_string>` | -> | { return } |
| 341 | `<statement_bool>` | -> | { ++, --, id } |
| 342 | `<statement_bool>` | -> | { thread, threadln, trap } |
| 343 | `<statement_bool>` | -> | { do, for, if, switch, while } |
| 344 | `<statement_bool>` | -> | { break } |
| 345 | `<statement_bool>` | -> | { return } |
| 346 | `<statement_array>` | -> | { ++, --, id } |
| 347 | `<statement_array>` | -> | { thread, threadln, trap } |
| 348 | `<statement_array>` | -> | { do, for, if, switch, while } |
| 349 | `<statement_array>` | -> | { break } |
| 350 | `<statement_array>` | -> | { return } |
| 351 | `<statement_weave>` | -> | { ++, --, id } |
| 352 | `<statement_weave>` | -> | { thread, threadln, trap } |
| 353 | `<statement_weave>` | -> | { do, for, if, switch, while } |
| 354 | `<statement_weave>` | -> | { break } |
| 355 | `<statement_weave>` | -> | { return } |
| 356 | `<statement_void>` | -> | { ++, --, id } |
| 357 | `<statement_void>` | -> | { thread, threadln, trap } |
| 358 | `<statement_void>` | -> | { do, for, if, switch, while } |
| 359 | `<statement_void>` | -> | { break } |
| 360 | `<statement_void>` | -> | { return } |
| 361 | `<ctrl_struct_int>` | -> | { if } |
| 362 | `<ctrl_struct_int>` | -> | { switch } |
| 363 | `<ctrl_struct_int>` | -> | { for } |
| 364 | `<ctrl_struct_int>` | -> | { while } |
| 365 | `<ctrl_struct_int>` | -> | { do } |
| 366 | `<stmt_list_int>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 367 | `<stmt_list_int>` | -> | { λ } |
| 368 | `<else_opt_int>` | -> | { else } |
| 369 | `<else_opt_int>` | -> | { λ } |
| 370 | `<else_body_int>` | -> | { { } |
| 371 | `<else_body_int>` | -> | { if } |
| 372 | `<case_list_int>` | -> | { case } |
| 373 | `<case_list_int>` | -> | { λ } |
| 374 | `<default_opt_int>` | -> | { default } |
| 375 | `<default_opt_int>` | -> | { λ } |
| 376 | `<ctrl_struct_long>` | -> | { if } |
| 377 | `<ctrl_struct_long>` | -> | { switch } |
| 378 | `<ctrl_struct_long>` | -> | { for } |
| 379 | `<ctrl_struct_long>` | -> | { while } |
| 380 | `<ctrl_struct_long>` | -> | { do } |
| 381 | `<stmt_list_long>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 382 | `<stmt_list_long>` | -> | { λ } |
| 383 | `<else_opt_long>` | -> | { else } |
| 384 | `<else_opt_long>` | -> | { λ } |
| 385 | `<else_body_long>` | -> | { { } |
| 386 | `<else_body_long>` | -> | { if } |
| 387 | `<case_list_long>` | -> | { case } |
| 388 | `<case_list_long>` | -> | { λ } |
| 389 | `<default_opt_long>` | -> | { default } |
| 390 | `<default_opt_long>` | -> | { λ } |
| 391 | `<ctrl_struct_float>` | -> | { if } |
| 392 | `<ctrl_struct_float>` | -> | { switch } |
| 393 | `<ctrl_struct_float>` | -> | { for } |
| 394 | `<ctrl_struct_float>` | -> | { while } |
| 395 | `<ctrl_struct_float>` | -> | { do } |
| 396 | `<stmt_list_float>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 397 | `<stmt_list_float>` | -> | { λ } |
| 398 | `<else_opt_float>` | -> | { else } |
| 399 | `<else_opt_float>` | -> | { λ } |
| 400 | `<else_body_float>` | -> | { { } |
| 401 | `<else_body_float>` | -> | { if } |
| 402 | `<case_list_float>` | -> | { case } |
| 403 | `<case_list_float>` | -> | { λ } |
| 404 | `<default_opt_float>` | -> | { default } |
| 405 | `<default_opt_float>` | -> | { λ } |
| 406 | `<ctrl_struct_double>` | -> | { if } |
| 407 | `<ctrl_struct_double>` | -> | { switch } |
| 408 | `<ctrl_struct_double>` | -> | { for } |
| 409 | `<ctrl_struct_double>` | -> | { while } |
| 410 | `<ctrl_struct_double>` | -> | { do } |
| 411 | `<stmt_list_double>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 412 | `<stmt_list_double>` | -> | { λ } |
| 413 | `<else_opt_double>` | -> | { else } |
| 414 | `<else_opt_double>` | -> | { λ } |
| 415 | `<else_body_double>` | -> | { { } |
| 416 | `<else_body_double>` | -> | { if } |
| 417 | `<case_list_double>` | -> | { case } |
| 418 | `<case_list_double>` | -> | { λ } |
| 419 | `<default_opt_double>` | -> | { default } |
| 420 | `<default_opt_double>` | -> | { λ } |
| 421 | `<ctrl_struct_char>` | -> | { if } |
| 422 | `<ctrl_struct_char>` | -> | { switch } |
| 423 | `<ctrl_struct_char>` | -> | { for } |
| 424 | `<ctrl_struct_char>` | -> | { while } |
| 425 | `<ctrl_struct_char>` | -> | { do } |
| 426 | `<stmt_list_char>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 427 | `<stmt_list_char>` | -> | { λ } |
| 428 | `<else_opt_char>` | -> | { else } |
| 429 | `<else_opt_char>` | -> | { λ } |
| 430 | `<else_body_char>` | -> | { { } |
| 431 | `<else_body_char>` | -> | { if } |
| 432 | `<case_list_char>` | -> | { case } |
| 433 | `<case_list_char>` | -> | { λ } |
| 434 | `<default_opt_char>` | -> | { default } |
| 435 | `<default_opt_char>` | -> | { λ } |
| 436 | `<ctrl_struct_string>` | -> | { if } |
| 437 | `<ctrl_struct_string>` | -> | { switch } |
| 438 | `<ctrl_struct_string>` | -> | { for } |
| 439 | `<ctrl_struct_string>` | -> | { while } |
| 440 | `<ctrl_struct_string>` | -> | { do } |
| 441 | `<stmt_list_string>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 442 | `<stmt_list_string>` | -> | { λ } |
| 443 | `<else_opt_string>` | -> | { else } |
| 444 | `<else_opt_string>` | -> | { λ } |
| 445 | `<else_body_string>` | -> | { { } |
| 446 | `<else_body_string>` | -> | { if } |
| 447 | `<case_list_string>` | -> | { case } |
| 448 | `<case_list_string>` | -> | { λ } |
| 449 | `<default_opt_string>` | -> | { default } |
| 450 | `<default_opt_string>` | -> | { λ } |
| 451 | `<ctrl_struct_bool>` | -> | { if } |
| 452 | `<ctrl_struct_bool>` | -> | { switch } |
| 453 | `<ctrl_struct_bool>` | -> | { for } |
| 454 | `<ctrl_struct_bool>` | -> | { while } |
| 455 | `<ctrl_struct_bool>` | -> | { do } |
| 456 | `<stmt_list_bool>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 457 | `<stmt_list_bool>` | -> | { λ } |
| 458 | `<else_opt_bool>` | -> | { else } |
| 459 | `<else_opt_bool>` | -> | { λ } |
| 460 | `<else_body_bool>` | -> | { { } |
| 461 | `<else_body_bool>` | -> | { if } |
| 462 | `<case_list_bool>` | -> | { case } |
| 463 | `<case_list_bool>` | -> | { λ } |
| 464 | `<default_opt_bool>` | -> | { default } |
| 465 | `<default_opt_bool>` | -> | { λ } |
| 466 | `<ctrl_struct_array>` | -> | { if } |
| 467 | `<ctrl_struct_array>` | -> | { switch } |
| 468 | `<ctrl_struct_array>` | -> | { for } |
| 469 | `<ctrl_struct_array>` | -> | { while } |
| 470 | `<ctrl_struct_array>` | -> | { do } |
| 471 | `<stmt_list_array>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 472 | `<stmt_list_array>` | -> | { λ } |
| 473 | `<else_opt_array>` | -> | { else } |
| 474 | `<else_opt_array>` | -> | { λ } |
| 475 | `<else_body_array>` | -> | { { } |
| 476 | `<else_body_array>` | -> | { if } |
| 477 | `<case_list_array>` | -> | { case } |
| 478 | `<case_list_array>` | -> | { λ } |
| 479 | `<default_opt_array>` | -> | { default } |
| 480 | `<default_opt_array>` | -> | { λ } |
| 481 | `<ctrl_struct_weave>` | -> | { if } |
| 482 | `<ctrl_struct_weave>` | -> | { switch } |
| 483 | `<ctrl_struct_weave>` | -> | { for } |
| 484 | `<ctrl_struct_weave>` | -> | { while } |
| 485 | `<ctrl_struct_weave>` | -> | { do } |
| 486 | `<stmt_list_weave>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 487 | `<stmt_list_weave>` | -> | { λ } |
| 488 | `<else_opt_weave>` | -> | { else } |
| 489 | `<else_opt_weave>` | -> | { λ } |
| 490 | `<else_body_weave>` | -> | { { } |
| 491 | `<else_body_weave>` | -> | { if } |
| 492 | `<case_list_weave>` | -> | { case } |
| 493 | `<case_list_weave>` | -> | { λ } |
| 494 | `<default_opt_weave>` | -> | { default } |
| 495 | `<default_opt_weave>` | -> | { λ } |
| 496 | `<ctrl_struct_void>` | -> | { if } |
| 497 | `<ctrl_struct_void>` | -> | { switch } |
| 498 | `<ctrl_struct_void>` | -> | { for } |
| 499 | `<ctrl_struct_void>` | -> | { while } |
| 500 | `<ctrl_struct_void>` | -> | { do } |
| 501 | `<stmt_list_void>` | -> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 502 | `<stmt_list_void>` | -> | { λ } |
| 503 | `<else_opt_void>` | -> | { else } |
| 504 | `<else_opt_void>` | -> | { λ } |
| 505 | `<else_body_void>` | -> | { { } |
| 506 | `<else_body_void>` | -> | { if } |
| 507 | `<case_list_void>` | -> | { case } |
| 508 | `<case_list_void>` | -> | { λ } |
| 509 | `<default_opt_void>` | -> | { default } |
| 510 | `<default_opt_void>` | -> | { λ } |
| 511 | `<int_return_expr>` | -> | { !, (, ++, --, id, int, intlit } |
| 512 | `<int_ret_assign>` | -> | { !, (, ++, --, id, int, intlit } |
| 513 | `<int_ret_concat>` | -> | { !, (, ++, --, id, int, intlit } |
| 514 | `<int_ret_or>` | -> | { !, (, ++, --, id, int, intlit } |
| 515 | `<int_ret_and>` | -> | { !, (, ++, --, id, int, intlit } |
| 516 | `<int_ret_eq>` | -> | { !, (, ++, --, id, int, intlit } |
| 517 | `<int_ret_rel>` | -> | { !, (, ++, --, id, int, intlit } |
| 518 | `<int_ret_add>` | -> | { !, (, ++, --, id, int, intlit } |
| 519 | `<int_ret_mul>` | -> | { !, (, ++, --, id, int, intlit } |
| 520 | `<int_ret_unary>` | -> | { ! } |
| 521 | `<int_ret_unary>` | -> | { (, ++, --, id, int, intlit } |
| 522 | `<int_ret_postfix>` | -> | { intlit } |
| 523 | `<int_ret_postfix>` | -> | { ++ } |
| 524 | `<int_ret_postfix>` | -> | { -- } |
| 525 | `<int_ret_postfix>` | -> | { id } |
| 526 | `<int_ret_postfix>` | -> | { ( } |
| 527 | `<int_ret_postfix>` | -> | { int } |
| 528 | `<long_return_expr>` | -> | { !, (, ++, --, id, long, longlit } |
| 529 | `<long_ret_assign>` | -> | { !, (, ++, --, id, long, longlit } |
| 530 | `<long_ret_concat>` | -> | { !, (, ++, --, id, long, longlit } |
| 531 | `<long_ret_or>` | -> | { !, (, ++, --, id, long, longlit } |
| 532 | `<long_ret_and>` | -> | { !, (, ++, --, id, long, longlit } |
| 533 | `<long_ret_eq>` | -> | { !, (, ++, --, id, long, longlit } |
| 534 | `<long_ret_rel>` | -> | { !, (, ++, --, id, long, longlit } |
| 535 | `<long_ret_add>` | -> | { !, (, ++, --, id, long, longlit } |
| 536 | `<long_ret_mul>` | -> | { !, (, ++, --, id, long, longlit } |
| 537 | `<long_ret_unary>` | -> | { ! } |
| 538 | `<long_ret_unary>` | -> | { (, ++, --, id, long, longlit } |
| 539 | `<long_ret_postfix>` | -> | { longlit } |
| 540 | `<long_ret_postfix>` | -> | { ++ } |
| 541 | `<long_ret_postfix>` | -> | { -- } |
| 542 | `<long_ret_postfix>` | -> | { id } |
| 543 | `<long_ret_postfix>` | -> | { ( } |
| 544 | `<long_ret_postfix>` | -> | { long } |
| 545 | `<float_return_expr>` | -> | { !, (, ++, --, float, floatlit, id } |
| 546 | `<float_ret_assign>` | -> | { !, (, ++, --, float, floatlit, id } |
| 547 | `<float_ret_concat>` | -> | { !, (, ++, --, float, floatlit, id } |
| 548 | `<float_ret_or>` | -> | { !, (, ++, --, float, floatlit, id } |
| 549 | `<float_ret_and>` | -> | { !, (, ++, --, float, floatlit, id } |
| 550 | `<float_ret_eq>` | -> | { !, (, ++, --, float, floatlit, id } |
| 551 | `<float_ret_rel>` | -> | { !, (, ++, --, float, floatlit, id } |
| 552 | `<float_ret_add>` | -> | { !, (, ++, --, float, floatlit, id } |
| 553 | `<float_ret_mul>` | -> | { !, (, ++, --, float, floatlit, id } |
| 554 | `<float_ret_unary>` | -> | { ! } |
| 555 | `<float_ret_unary>` | -> | { (, ++, --, float, floatlit, id } |
| 556 | `<float_ret_postfix>` | -> | { floatlit } |
| 557 | `<float_ret_postfix>` | -> | { ++ } |
| 558 | `<float_ret_postfix>` | -> | { -- } |
| 559 | `<float_ret_postfix>` | -> | { id } |
| 560 | `<float_ret_postfix>` | -> | { ( } |
| 561 | `<float_ret_postfix>` | -> | { float } |
| 562 | `<double_return_expr>` | -> | { !, (, ++, --, double, doublelit, id } |
| 563 | `<double_ret_assign>` | -> | { !, (, ++, --, double, doublelit, id } |
| 564 | `<double_ret_concat>` | -> | { !, (, ++, --, double, doublelit, id } |
| 565 | `<double_ret_or>` | -> | { !, (, ++, --, double, doublelit, id } |
| 566 | `<double_ret_and>` | -> | { !, (, ++, --, double, doublelit, id } |
| 567 | `<double_ret_eq>` | -> | { !, (, ++, --, double, doublelit, id } |
| 568 | `<double_ret_rel>` | -> | { !, (, ++, --, double, doublelit, id } |
| 569 | `<double_ret_add>` | -> | { !, (, ++, --, double, doublelit, id } |
| 570 | `<double_ret_mul>` | -> | { !, (, ++, --, double, doublelit, id } |
| 571 | `<double_ret_unary>` | -> | { ! } |
| 572 | `<double_ret_unary>` | -> | { (, ++, --, double, doublelit, id } |
| 573 | `<double_ret_postfix>` | -> | { doublelit } |
| 574 | `<double_ret_postfix>` | -> | { ++ } |
| 575 | `<double_ret_postfix>` | -> | { -- } |
| 576 | `<double_ret_postfix>` | -> | { id } |
| 577 | `<double_ret_postfix>` | -> | { ( } |
| 578 | `<double_ret_postfix>` | -> | { double } |
| 579 | `<char_return_expr>` | -> | { !, (, ++, --, char, charlit, id } |
| 580 | `<char_ret_assign>` | -> | { !, (, ++, --, char, charlit, id } |
| 581 | `<char_ret_concat>` | -> | { !, (, ++, --, char, charlit, id } |
| 582 | `<char_ret_or>` | -> | { !, (, ++, --, char, charlit, id } |
| 583 | `<char_ret_and>` | -> | { !, (, ++, --, char, charlit, id } |
| 584 | `<char_ret_eq>` | -> | { !, (, ++, --, char, charlit, id } |
| 585 | `<char_ret_rel>` | -> | { !, (, ++, --, char, charlit, id } |
| 586 | `<char_ret_add>` | -> | { !, (, ++, --, char, charlit, id } |
| 587 | `<char_ret_mul>` | -> | { !, (, ++, --, char, charlit, id } |
| 588 | `<char_ret_unary>` | -> | { ! } |
| 589 | `<char_ret_unary>` | -> | { (, ++, --, char, charlit, id } |
| 590 | `<char_ret_postfix>` | -> | { charlit } |
| 591 | `<char_ret_postfix>` | -> | { ++ } |
| 592 | `<char_ret_postfix>` | -> | { -- } |
| 593 | `<char_ret_postfix>` | -> | { id } |
| 594 | `<char_ret_postfix>` | -> | { ( } |
| 595 | `<char_ret_postfix>` | -> | { char } |
| 596 | `<string_return_expr>` | -> | { !, (, ++, --, id, string, stringlit } |
| 597 | `<string_ret_assign>` | -> | { !, (, ++, --, id, string, stringlit } |
| 598 | `<string_ret_concat>` | -> | { !, (, ++, --, id, string, stringlit } |
| 599 | `<string_ret_or>` | -> | { !, (, ++, --, id, string, stringlit } |
| 600 | `<string_ret_and>` | -> | { !, (, ++, --, id, string, stringlit } |
| 601 | `<string_ret_eq>` | -> | { !, (, ++, --, id, string, stringlit } |
| 602 | `<string_ret_rel>` | -> | { !, (, ++, --, id, string, stringlit } |
| 603 | `<string_ret_add>` | -> | { !, (, ++, --, id, string, stringlit } |
| 604 | `<string_ret_mul>` | -> | { !, (, ++, --, id, string, stringlit } |
| 605 | `<string_ret_unary>` | -> | { ! } |
| 606 | `<string_ret_unary>` | -> | { (, ++, --, id, string, stringlit } |
| 607 | `<string_ret_postfix>` | -> | { stringlit } |
| 608 | `<string_ret_postfix>` | -> | { ++ } |
| 609 | `<string_ret_postfix>` | -> | { -- } |
| 610 | `<string_ret_postfix>` | -> | { id } |
| 611 | `<string_ret_postfix>` | -> | { ( } |
| 612 | `<string_ret_postfix>` | -> | { string } |
| 613 | `<bool_return_expr>` | -> | { !, (, ++, --, bool, false, id, true } |
| 614 | `<bool_ret_assign>` | -> | { !, (, ++, --, bool, false, id, true } |
| 615 | `<bool_ret_concat>` | -> | { !, (, ++, --, bool, false, id, true } |
| 616 | `<bool_ret_or>` | -> | { !, (, ++, --, bool, false, id, true } |
| 617 | `<bool_ret_and>` | -> | { !, (, ++, --, bool, false, id, true } |
| 618 | `<bool_ret_eq>` | -> | { !, (, ++, --, bool, false, id, true } |
| 619 | `<bool_ret_rel>` | -> | { !, (, ++, --, bool, false, id, true } |
| 620 | `<bool_ret_add>` | -> | { !, (, ++, --, bool, false, id, true } |
| 621 | `<bool_ret_mul>` | -> | { !, (, ++, --, bool, false, id, true } |
| 622 | `<bool_ret_unary>` | -> | { ! } |
| 623 | `<bool_ret_unary>` | -> | { (, ++, --, bool, false, id, true } |
| 624 | `<bool_ret_postfix>` | -> | { true } |
| 625 | `<bool_ret_postfix>` | -> | { false } |
| 626 | `<bool_ret_postfix>` | -> | { ++ } |
| 627 | `<bool_ret_postfix>` | -> | { -- } |
| 628 | `<bool_ret_postfix>` | -> | { id } |
| 629 | `<bool_ret_postfix>` | -> | { ( } |
| 630 | `<bool_ret_postfix>` | -> | { bool } |
| 631 | `<using_cont>` | -> | { , } |
| 632 | `<using_cont>` | -> | { λ } |
| 633 | `<local_dec_body>` | -> | { int } |
| 634 | `<local_dec_body>` | -> | { long } |
| 635 | `<local_dec_body>` | -> | { float } |
| 636 | `<local_dec_body>` | -> | { double } |
| 637 | `<local_dec_body>` | -> | { char } |
| 638 | `<local_dec_body>` | -> | { string } |
| 639 | `<local_dec_body>` | -> | { bool } |
| 640 | `<local_dec_body>` | -> | { id } |
| 641 | `<int_local_tail>` | -> | { [ } |
| 642 | `<int_local_tail>` | -> | { = } |
| 643 | `<int_local_cont>` | -> | { , } |
| 644 | `<int_local_cont>` | -> | { λ } |
| 645 | `<long_local_tail>` | -> | { [ } |
| 646 | `<long_local_tail>` | -> | { = } |
| 647 | `<long_local_cont>` | -> | { , } |
| 648 | `<long_local_cont>` | -> | { λ } |
| 649 | `<float_local_tail>` | -> | { [ } |
| 650 | `<float_local_tail>` | -> | { = } |
| 651 | `<float_local_cont>` | -> | { , } |
| 652 | `<float_local_cont>` | -> | { λ } |
| 653 | `<double_local_tail>` | -> | { [ } |
| 654 | `<double_local_tail>` | -> | { = } |
| 655 | `<double_local_cont>` | -> | { , } |
| 656 | `<double_local_cont>` | -> | { λ } |
| 657 | `<char_local_tail>` | -> | { [ } |
| 658 | `<char_local_tail>` | -> | { = } |
| 659 | `<char_local_cont>` | -> | { , } |
| 660 | `<char_local_cont>` | -> | { λ } |
| 661 | `<string_local_tail>` | -> | { [ } |
| 662 | `<string_local_tail>` | -> | { = } |
| 663 | `<string_local_cont>` | -> | { , } |
| 664 | `<string_local_cont>` | -> | { λ } |
| 665 | `<bool_local_tail>` | -> | { [ } |
| 666 | `<bool_local_tail>` | -> | { = } |
| 667 | `<bool_local_cont>` | -> | { , } |
| 668 | `<bool_local_cont>` | -> | { λ } |
| 669 | `<weave_local_tail>` | -> | { = } |
| 670 | `<weave_local_tail>` | -> | { [ } |
| 671 | `<statement_non_return>` | -> | { ++, --, id } |
| 672 | `<statement_non_return>` | -> | { thread, threadln, trap } |
| 673 | `<statement_non_return>` | -> | { do, for, if, switch, while } |
| 674 | `<statement_non_return>` | -> | { break } |
| 675 | `<ctrl_stmt_list>` | -> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 676 | `<ctrl_stmt_list>` | -> | { λ } |
| 677 | `<effect_stmt>` | -> | { ++ } |
| 678 | `<effect_stmt>` | -> | { -- } |
| 679 | `<effect_stmt>` | -> | { id } |
| 680 | `<effect_pre_chain>` | -> | { [ } |
| 681 | `<effect_pre_chain>` | -> | { . } |
| 682 | `<effect_pre_chain>` | -> | { λ } |
| 683 | `<effect_pre_arr_chain>` | -> | { [ } |
| 684 | `<effect_pre_arr_chain>` | -> | { . } |
| 685 | `<effect_pre_arr_chain>` | -> | { λ } |
| 686 | `<effect_id_cont>` | -> | { %=, *=, +=, -=, /=, = } |
| 687 | `<effect_id_cont>` | -> | { ++ } |
| 688 | `<effect_id_cont>` | -> | { -- } |
| 689 | `<effect_id_cont>` | -> | { ( } |
| 690 | `<effect_id_cont>` | -> | { [ } |
| 691 | `<effect_id_cont>` | -> | { . } |
| 692 | `<effect_post_call>` | -> | { . } |
| 693 | `<effect_post_call>` | -> | { [ } |
| 694 | `<effect_post_call>` | -> | { λ } |
| 695 | `<effect_post_call_member>` | -> | { ( } |
| 696 | `<effect_post_call_member>` | -> | { [ } |
| 697 | `<effect_post_call_member>` | -> | { . } |
| 698 | `<effect_post_call_member>` | -> | { λ } |
| 699 | `<effect_post_call_arr>` | -> | { [ } |
| 700 | `<effect_post_call_arr>` | -> | { (, ., λ } |
| 701 | `<effect_post_call_arr_cont>` | -> | { . } |
| 702 | `<effect_post_call_arr_cont>` | -> | { ( } |
| 703 | `<effect_post_call_arr_cont>` | -> | { λ } |
| 704 | `<effect_post_arr>` | -> | { [ } |
| 705 | `<effect_post_arr>` | -> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 706 | `<effect_post_arr_2d>` | -> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 707 | `<effect_arr_effect>` | -> | { %=, *=, +=, -=, /=, = } |
| 708 | `<effect_arr_effect>` | -> | { ++ } |
| 709 | `<effect_arr_effect>` | -> | { -- } |
| 710 | `<effect_arr_effect>` | -> | { ( } |
| 711 | `<effect_arr_effect>` | -> | { . } |
| 712 | `<effect_post_member>` | -> | { %=, *=, +=, -=, /=, = } |
| 713 | `<effect_post_member>` | -> | { ++ } |
| 714 | `<effect_post_member>` | -> | { -- } |
| 715 | `<effect_post_member>` | -> | { ( } |
| 716 | `<effect_post_member>` | -> | { [ } |
| 717 | `<effect_post_member>` | -> | { . } |
| 718 | `<stmt_assign_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 719 | `<stmt_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 720 | `<stmt_assign_tail>` | -> | { λ } |
| 721 | `<stmt_concat_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 722 | `<stmt_concat_tail>` | -> | { .. } |
| 723 | `<stmt_concat_tail>` | -> | { λ } |
| 724 | `<stmt_or_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 725 | `<stmt_or_tail>` | -> | { \|\| } |
| 726 | `<stmt_or_tail>` | -> | { λ } |
| 727 | `<stmt_and_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 728 | `<stmt_and_tail>` | -> | { && } |
| 729 | `<stmt_and_tail>` | -> | { λ } |
| 730 | `<stmt_eq_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 731 | `<stmt_eq_tail>` | -> | { == } |
| 732 | `<stmt_eq_tail>` | -> | { != } |
| 733 | `<stmt_eq_tail>` | -> | { λ } |
| 734 | `<stmt_rel_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 735 | `<stmt_rel_tail>` | -> | { < } |
| 736 | `<stmt_rel_tail>` | -> | { > } |
| 737 | `<stmt_rel_tail>` | -> | { <= } |
| 738 | `<stmt_rel_tail>` | -> | { >= } |
| 739 | `<stmt_rel_tail>` | -> | { λ } |
| 740 | `<stmt_add_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 741 | `<stmt_add_tail>` | -> | { + } |
| 742 | `<stmt_add_tail>` | -> | { - } |
| 743 | `<stmt_add_tail>` | -> | { λ } |
| 744 | `<stmt_mul_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 745 | `<stmt_mul_tail>` | -> | { * } |
| 746 | `<stmt_mul_tail>` | -> | { / } |
| 747 | `<stmt_mul_tail>` | -> | { % } |
| 748 | `<stmt_mul_tail>` | -> | { λ } |
| 749 | `<stmt_unary_expr>` | -> | { ! } |
| 750 | `<stmt_unary_expr>` | -> | { - } |
| 751 | `<stmt_unary_expr>` | -> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 752 | `<stmt_postfix_expr>` | -> | { ( } |
| 753 | `<stmt_postfix_expr>` | -> | { int } |
| 754 | `<stmt_postfix_expr>` | -> | { long } |
| 755 | `<stmt_postfix_expr>` | -> | { float } |
| 756 | `<stmt_postfix_expr>` | -> | { double } |
| 757 | `<stmt_postfix_expr>` | -> | { char } |
| 758 | `<stmt_postfix_expr>` | -> | { string } |
| 759 | `<stmt_postfix_expr>` | -> | { bool } |
| 760 | `<stmt_postfix_expr>` | -> | { ++ } |
| 761 | `<stmt_postfix_expr>` | -> | { -- } |
| 762 | `<stmt_postfix_expr>` | -> | { id } |
| 763 | `<stmt_postfix_expr>` | -> | { intlit } |
| 764 | `<stmt_postfix_expr>` | -> | { longlit } |
| 765 | `<stmt_postfix_expr>` | -> | { floatlit } |
| 766 | `<stmt_postfix_expr>` | -> | { doublelit } |
| 767 | `<stmt_postfix_expr>` | -> | { charlit } |
| 768 | `<stmt_postfix_expr>` | -> | { stringlit } |
| 769 | `<stmt_postfix_expr>` | -> | { true } |
| 770 | `<stmt_postfix_expr>` | -> | { false } |
| 771 | `<stmt_id_postfix>` | -> | { ++ } |
| 772 | `<stmt_id_postfix>` | -> | { -- } |
| 773 | `<stmt_id_postfix>` | -> | { (, ., [, λ } |
| 774 | `<stmt_postfix_chain>` | -> | { [ } |
| 775 | `<stmt_postfix_chain>` | -> | { . } |
| 776 | `<stmt_postfix_chain>` | -> | { ( } |
| 777 | `<stmt_postfix_chain>` | -> | { λ } |
| 778 | `<stmt_array_access>` | -> | { [ } |
| 779 | `<stmt_array_access_dim2>` | -> | { [ } |
| 780 | `<stmt_array_access_dim2>` | -> | { λ } |
| 781 | `<stmt_postfix_after_arr>` | -> | { . } |
| 782 | `<stmt_postfix_after_arr>` | -> | { ( } |
| 783 | `<stmt_postfix_after_arr>` | -> | { λ } |
| 784 | `<stmt_array_index>` | -> | { intlit } |
| 785 | `<stmt_array_index>` | -> | { id } |
| 786 | `<stmt_arg_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 787 | `<stmt_arg_list>` | -> | { λ } |
| 788 | `<stmt_arg_tail>` | -> | { , } |
| 789 | `<stmt_arg_tail>` | -> | { λ } |
| 790 | `<arg_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 791 | `<arg_assign_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 792 | `<arg_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 793 | `<arg_assign_tail>` | -> | { λ } |
| 794 | `<arg_concat_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 795 | `<arg_concat_tail>` | -> | { .. } |
| 796 | `<arg_concat_tail>` | -> | { λ } |
| 797 | `<arg_or_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 798 | `<arg_or_tail>` | -> | { \|\| } |
| 799 | `<arg_or_tail>` | -> | { λ } |
| 800 | `<arg_and_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 801 | `<arg_and_tail>` | -> | { && } |
| 802 | `<arg_and_tail>` | -> | { λ } |
| 803 | `<arg_eq_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 804 | `<arg_eq_tail>` | -> | { == } |
| 805 | `<arg_eq_tail>` | -> | { != } |
| 806 | `<arg_eq_tail>` | -> | { λ } |
| 807 | `<arg_rel_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 808 | `<arg_rel_tail>` | -> | { < } |
| 809 | `<arg_rel_tail>` | -> | { > } |
| 810 | `<arg_rel_tail>` | -> | { <= } |
| 811 | `<arg_rel_tail>` | -> | { >= } |
| 812 | `<arg_rel_tail>` | -> | { λ } |
| 813 | `<arg_add_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 814 | `<arg_add_tail>` | -> | { + } |
| 815 | `<arg_add_tail>` | -> | { - } |
| 816 | `<arg_add_tail>` | -> | { λ } |
| 817 | `<arg_mul_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 818 | `<arg_mul_tail>` | -> | { * } |
| 819 | `<arg_mul_tail>` | -> | { / } |
| 820 | `<arg_mul_tail>` | -> | { % } |
| 821 | `<arg_mul_tail>` | -> | { λ } |
| 822 | `<arg_unary_expr>` | -> | { ! } |
| 823 | `<arg_unary_expr>` | -> | { - } |
| 824 | `<arg_unary_expr>` | -> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 825 | `<arg_postfix_expr>` | -> | { ( } |
| 826 | `<arg_postfix_expr>` | -> | { int } |
| 827 | `<arg_postfix_expr>` | -> | { long } |
| 828 | `<arg_postfix_expr>` | -> | { float } |
| 829 | `<arg_postfix_expr>` | -> | { double } |
| 830 | `<arg_postfix_expr>` | -> | { char } |
| 831 | `<arg_postfix_expr>` | -> | { string } |
| 832 | `<arg_postfix_expr>` | -> | { bool } |
| 833 | `<arg_postfix_expr>` | -> | { ++ } |
| 834 | `<arg_postfix_expr>` | -> | { -- } |
| 835 | `<arg_postfix_expr>` | -> | { id } |
| 836 | `<arg_postfix_expr>` | -> | { intlit } |
| 837 | `<arg_postfix_expr>` | -> | { longlit } |
| 838 | `<arg_postfix_expr>` | -> | { floatlit } |
| 839 | `<arg_postfix_expr>` | -> | { doublelit } |
| 840 | `<arg_postfix_expr>` | -> | { charlit } |
| 841 | `<arg_postfix_expr>` | -> | { stringlit } |
| 842 | `<arg_postfix_expr>` | -> | { true } |
| 843 | `<arg_postfix_expr>` | -> | { false } |
| 844 | `<arg_id_postfix>` | -> | { ++ } |
| 845 | `<arg_id_postfix>` | -> | { -- } |
| 846 | `<arg_id_postfix>` | -> | { (, ., [, λ } |
| 847 | `<arg_postfix_chain>` | -> | { [ } |
| 848 | `<arg_postfix_chain>` | -> | { . } |
| 849 | `<arg_postfix_chain>` | -> | { ( } |
| 850 | `<arg_postfix_chain>` | -> | { λ } |
| 851 | `<arg_array_access>` | -> | { [ } |
| 852 | `<arg_array_access_dim2>` | -> | { [ } |
| 853 | `<arg_array_access_dim2>` | -> | { λ } |
| 854 | `<arg_postfix_after_arr>` | -> | { . } |
| 855 | `<arg_postfix_after_arr>` | -> | { ( } |
| 856 | `<arg_postfix_after_arr>` | -> | { λ } |
| 857 | `<arg_array_index>` | -> | { intlit } |
| 858 | `<arg_array_index>` | -> | { id } |
| 859 | `<arg_nested_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 860 | `<arg_nested_list>` | -> | { λ } |
| 861 | `<arg_nested_tail>` | -> | { , } |
| 862 | `<arg_nested_tail>` | -> | { λ } |
| 863 | `<expression>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 864 | `<assign_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 865 | `<assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 866 | `<assign_tail>` | -> | { λ } |
| 867 | `<assign_op>` | -> | { = } |
| 868 | `<assign_op>` | -> | { += } |
| 869 | `<assign_op>` | -> | { -= } |
| 870 | `<assign_op>` | -> | { *= } |
| 871 | `<assign_op>` | -> | { /= } |
| 872 | `<assign_op>` | -> | { %= } |
| 873 | `<concat_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 874 | `<concat_tail>` | -> | { .. } |
| 875 | `<concat_tail>` | -> | { λ } |
| 876 | `<or_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 877 | `<or_tail>` | -> | { \|\| } |
| 878 | `<or_tail>` | -> | { λ } |
| 879 | `<and_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 880 | `<and_tail>` | -> | { && } |
| 881 | `<and_tail>` | -> | { λ } |
| 882 | `<eq_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 883 | `<eq_tail>` | -> | { == } |
| 884 | `<eq_tail>` | -> | { != } |
| 885 | `<eq_tail>` | -> | { λ } |
| 886 | `<rel_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 887 | `<rel_tail>` | -> | { < } |
| 888 | `<rel_tail>` | -> | { > } |
| 889 | `<rel_tail>` | -> | { <= } |
| 890 | `<rel_tail>` | -> | { >= } |
| 891 | `<rel_tail>` | -> | { λ } |
| 892 | `<add_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 893 | `<add_tail>` | -> | { + } |
| 894 | `<add_tail>` | -> | { - } |
| 895 | `<add_tail>` | -> | { λ } |
| 896 | `<mul_expr>` | -> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 897 | `<mul_tail>` | -> | { * } |
| 898 | `<mul_tail>` | -> | { / } |
| 899 | `<mul_tail>` | -> | { % } |
| 900 | `<mul_tail>` | -> | { λ } |
| 901 | `<unary_expr>` | -> | { ! } |
| 902 | `<unary_expr>` | -> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 903 | `<postfix_expr>` | -> | { ( } |
| 904 | `<postfix_expr>` | -> | { int } |
| 905 | `<postfix_expr>` | -> | { long } |
| 906 | `<postfix_expr>` | -> | { float } |
| 907 | `<postfix_expr>` | -> | { double } |
| 908 | `<postfix_expr>` | -> | { char } |
| 909 | `<postfix_expr>` | -> | { string } |
| 910 | `<postfix_expr>` | -> | { bool } |
| 911 | `<postfix_expr>` | -> | { ++ } |
| 912 | `<postfix_expr>` | -> | { -- } |
| 913 | `<postfix_expr>` | -> | { id } |
| 914 | `<postfix_expr>` | -> | { intlit } |
| 915 | `<postfix_expr>` | -> | { longlit } |
| 916 | `<postfix_expr>` | -> | { floatlit } |
| 917 | `<postfix_expr>` | -> | { doublelit } |
| 918 | `<postfix_expr>` | -> | { charlit } |
| 919 | `<postfix_expr>` | -> | { stringlit } |
| 920 | `<postfix_expr>` | -> | { true } |
| 921 | `<postfix_expr>` | -> | { false } |
| 922 | `<id_postfix>` | -> | { ++ } |
| 923 | `<id_postfix>` | -> | { -- } |
| 924 | `<id_postfix>` | -> | { (, ., [, λ } |
| 925 | `<postfix_chain>` | -> | { [ } |
| 926 | `<postfix_chain>` | -> | { . } |
| 927 | `<postfix_chain>` | -> | { ( } |
| 928 | `<postfix_chain>` | -> | { λ } |
| 929 | `<array_access>` | -> | { [ } |
| 930 | `<array_access_dim2>` | -> | { [ } |
| 931 | `<array_access_dim2>` | -> | { λ } |
| 932 | `<postfix_after_arr>` | -> | { . } |
| 933 | `<postfix_after_arr>` | -> | { ( } |
| 934 | `<postfix_after_arr>` | -> | { λ } |
| 935 | `<array_index>` | -> | { intlit } |
| 936 | `<array_index>` | -> | { id } |
| 937 | `<arg_list>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 938 | `<arg_list>` | -> | { λ } |
| 939 | `<arg_tail>` | -> | { , } |
| 940 | `<arg_tail>` | -> | { λ } |
| 941 | `<io_stmt>` | -> | { trap } |
| 942 | `<io_stmt>` | -> | { thread } |
| 943 | `<io_stmt>` | -> | { threadln } |
| 944 | `<print_args>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 945 | `<print_tail>` | -> | { , } |
| 946 | `<print_tail>` | -> | { λ } |
| 947 | `<ctrl_struct>` | -> | { if } |
| 948 | `<ctrl_struct>` | -> | { switch } |
| 949 | `<ctrl_struct>` | -> | { for } |
| 950 | `<ctrl_struct>` | -> | { while } |
| 951 | `<ctrl_struct>` | -> | { do } |
| 952 | `<else_opt>` | -> | { else } |
| 953 | `<else_opt>` | -> | { λ } |
| 954 | `<else_body>` | -> | { { } |
| 955 | `<else_body>` | -> | { if } |
| 956 | `<case_list>` | -> | { case } |
| 957 | `<case_list>` | -> | { λ } |
| 958 | `<case_val>` | -> | { intlit } |
| 959 | `<case_val>` | -> | { longlit } |
| 960 | `<case_val>` | -> | { charlit } |
| 961 | `<case_val>` | -> | { true } |
| 962 | `<case_val>` | -> | { false } |
| 963 | `<default_opt>` | -> | { default } |
| 964 | `<default_opt>` | -> | { λ } |
| 965 | `<break_opt>` | -> | { break } |
| 966 | `<break_opt>` | -> | { λ } |
| 967 | `<for_init>` | -> | { local } |
| 968 | `<for_init>` | -> | { id } |
| 969 | `<for_init>` | -> | { λ } |
| 970 | `<for_init_assign_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 971 | `<for_init_expr>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 972 | `<for_init_type>` | -> | { int } |
| 973 | `<for_init_type>` | -> | { long } |
| 974 | `<for_init_type>` | -> | { float } |
| 975 | `<for_init_type>` | -> | { double } |
| 976 | `<for_init_type>` | -> | { char } |
| 977 | `<for_init_type>` | -> | { string } |
| 978 | `<for_init_type>` | -> | { bool } |
| 979 | `<for_cond>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 980 | `<for_update>` | -> | { id } |
| 981 | `<for_update>` | -> | { ++ } |
| 982 | `<for_update>` | -> | { -- } |
| 983 | `<for_update>` | -> | { λ } |
| 984 | `<for_update_tail>` | -> | { ++ } |
| 985 | `<for_update_tail>` | -> | { -- } |
| 986 | `<for_update_tail>` | -> | { %=, *=, +=, -=, /=, = } |
| 987 | `<condition>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 988 | `<cond_or>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 989 | `<cond_or_tail>` | -> | { \|\| } |
| 990 | `<cond_or_tail>` | -> | { λ } |
| 991 | `<cond_and>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 992 | `<cond_and_tail>` | -> | { && } |
| 993 | `<cond_and_tail>` | -> | { λ } |
| 994 | `<cond_comparison>` | -> | { ( } |
| 995 | `<cond_comparison>` | -> | { ! } |
| 996 | `<cond_comparison>` | -> | { ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 997 | `<cond_primary>` | -> | { - } |
| 998 | `<cond_primary>` | -> | { ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 999 | `<cond_primary_continue>` | -> | { + } |
| 1000 | `<cond_primary_continue>` | -> | { - } |
| 1001 | `<cond_primary_continue>` | -> | { * } |
| 1002 | `<cond_primary_continue>` | -> | { / } |
| 1003 | `<cond_primary_continue>` | -> | { % } |
| 1004 | `<cond_primary_continue>` | -> | { !=, <, <=, ==, >, >= } |
| 1005 | `<cond_primary_continue>` | -> | { λ } |
| 1006 | `<cond_must_commit>` | -> | { + } |
| 1007 | `<cond_must_commit>` | -> | { - } |
| 1008 | `<cond_must_commit>` | -> | { * } |
| 1009 | `<cond_must_commit>` | -> | { / } |
| 1010 | `<cond_must_commit>` | -> | { % } |
| 1011 | `<cond_must_commit>` | -> | { !=, <, <=, ==, >, >= } |
| 1012 | `<cond_postfix>` | -> | { int } |
| 1013 | `<cond_postfix>` | -> | { long } |
| 1014 | `<cond_postfix>` | -> | { float } |
| 1015 | `<cond_postfix>` | -> | { double } |
| 1016 | `<cond_postfix>` | -> | { char } |
| 1017 | `<cond_postfix>` | -> | { string } |
| 1018 | `<cond_postfix>` | -> | { bool } |
| 1019 | `<cond_postfix>` | -> | { ++ } |
| 1020 | `<cond_postfix>` | -> | { -- } |
| 1021 | `<cond_postfix>` | -> | { id } |
| 1022 | `<cond_postfix>` | -> | { intlit } |
| 1023 | `<cond_postfix>` | -> | { longlit } |
| 1024 | `<cond_postfix>` | -> | { floatlit } |
| 1025 | `<cond_postfix>` | -> | { doublelit } |
| 1026 | `<cond_postfix>` | -> | { charlit } |
| 1027 | `<cond_postfix>` | -> | { stringlit } |
| 1028 | `<cond_postfix>` | -> | { true } |
| 1029 | `<cond_postfix>` | -> | { false } |
| 1030 | `<cond_cast_arg>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1031 | `<cond_id_post>` | -> | { ++ } |
| 1032 | `<cond_id_post>` | -> | { -- } |
| 1033 | `<cond_id_post>` | -> | { (, ., [, λ } |
| 1034 | `<cond_post_chain>` | -> | { [ } |
| 1035 | `<cond_post_chain>` | -> | { . } |
| 1036 | `<cond_post_chain>` | -> | { ( } |
| 1037 | `<cond_post_chain>` | -> | { λ } |
| 1038 | `<cond_arr_access>` | -> | { [ } |
| 1039 | `<cond_arr_access_dim2>` | -> | { [ } |
| 1040 | `<cond_arr_access_dim2>` | -> | { λ } |
| 1041 | `<cond_post_after_arr>` | -> | { . } |
| 1042 | `<cond_post_after_arr>` | -> | { ( } |
| 1043 | `<cond_post_after_arr>` | -> | { λ } |
| 1044 | `<cond_arr_index>` | -> | { intlit } |
| 1045 | `<cond_arr_index>` | -> | { id } |
| 1046 | `<cond_rhs>` | -> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1047 | `<comp_op>` | -> | { == } |
| 1048 | `<comp_op>` | -> | { != } |
| 1049 | `<comp_op>` | -> | { < } |
| 1050 | `<comp_op>` | -> | { > } |
| 1051 | `<comp_op>` | -> | { <= } |
| 1052 | `<comp_op>` | -> | { >= } |
| 1053 | `<main_body>` | -> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 1054 | `<main_content>` | -> | { using } |
| 1055 | `<main_content>` | -> | { local } |
| 1056 | `<main_content>` | -> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1057 | `<main_content>` | -> | { return } |