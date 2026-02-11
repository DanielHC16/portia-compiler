## Context-Free Grammar

| # | Production | -> | Production Set |
|---|------------|-----|----------------|
| 1 | `<program>` | -> | `<global_section>` |
| 2 | `<global_section>` | -> | `<global_decl>` `<global_section>` |
| 3 | `<global_section>` | -> | int id `<int_array_with_init>` ; `<global_section>` |
| 4 | `<global_section>` | -> | long id `<long_array_with_init>` ; `<global_section>` |
| 5 | `<global_section>` | -> | float id `<float_array_with_init>` ; `<global_section>` |
| 6 | `<global_section>` | -> | double id `<double_array_with_init>` ; `<global_section>` |
| 7 | `<global_section>` | -> | char id `<char_array_with_init>` ; `<global_section>` |
| 8 | `<global_section>` | -> | string id `<string_array_with_init>` ; `<global_section>` |
| 9 | `<global_section>` | -> | bool id `<bool_array_with_init>` ; `<global_section>` |
| 10 | `<global_section>` | -> | weave id { `<field_list>` } ; `<global_section>` |
| 11 | `<global_section>` | -> | id `<weave_inst_decl>` `<global_section>` |
| 12 | `<global_section>` | -> | `<function_decl>` `<func_and_main>` |
| 13 | `<global_section>` | -> | int main ( ) { `<main_body>` } |
| 14 | `<func_and_main>` | -> | `<function_decl>` `<func_and_main>` |
| 15 | `<func_and_main>` | -> | int main ( ) { `<main_body>` } |
| 16 | `<global_decl>` | -> | global `<mutability>` int id = intlit `<int_global_cont>` ; |
| 17 | `<global_decl>` | -> | global `<mutability>` long id = longlit `<long_global_cont>` ; |
| 18 | `<global_decl>` | -> | global `<mutability>` float id = floatlit `<float_global_cont>` ; |
| 19 | `<global_decl>` | -> | global `<mutability>` double id = doublelit `<double_global_cont>` ; |
| 20 | `<global_decl>` | -> | global `<mutability>` char id = charlit `<char_global_cont>` ; |
| 21 | `<global_decl>` | -> | global `<mutability>` string id = stringlit `<string_global_cont>` ; |
| 22 | `<global_decl>` | -> | global `<mutability>` bool id = `<bool_lit>` `<bool_global_cont>` ; |
| 23 | `<function_decl>` | -> | func int `<func_ret_int>` |
| 24 | `<function_decl>` | -> | func long `<func_ret_long>` |
| 25 | `<function_decl>` | -> | func float `<func_ret_float>` |
| 26 | `<function_decl>` | -> | func double `<func_ret_double>` |
| 27 | `<function_decl>` | -> | func char `<func_ret_char>` |
| 28 | `<function_decl>` | -> | func string `<func_ret_string>` |
| 29 | `<function_decl>` | -> | func bool `<func_ret_bool>` |
| 30 | `<function_decl>` | -> | func id `<func_ret_weave>` |
| 31 | `<function_decl>` | -> | func void id ( ) { `<function_body_void>` } |
| 32 | `<bool_lit>` | -> | true |
| 33 | `<bool_lit>` | -> | false |
| 34 | `<int_global_cont>` | -> | , id = intlit `<int_global_cont>` |
| 35 | `<int_global_cont>` | -> | λ |
| 36 | `<long_global_cont>` | -> | , id = longlit `<long_global_cont>` |
| 37 | `<long_global_cont>` | -> | λ |
| 38 | `<float_global_cont>` | -> | , id = floatlit `<float_global_cont>` |
| 39 | `<float_global_cont>` | -> | λ |
| 40 | `<double_global_cont>` | -> | , id = doublelit `<double_global_cont>` |
| 41 | `<double_global_cont>` | -> | λ |
| 42 | `<char_global_cont>` | -> | , id = charlit `<char_global_cont>` |
| 43 | `<char_global_cont>` | -> | λ |
| 44 | `<string_global_cont>` | -> | , id = stringlit `<string_global_cont>` |
| 45 | `<string_global_cont>` | -> | λ |
| 46 | `<bool_global_cont>` | -> | , id = `<bool_lit>` `<bool_global_cont>` |
| 47 | `<bool_global_cont>` | -> | λ |
| 48 | `<weave_inst_decl>` | -> | id `<weave_inst_tail>` `<weave_inst_cont>` ; |
| 49 | `<weave_inst_decl>` | -> | `<weave_array_with_init>` `<weave_arr_cont>` ; |
| 50 | `<weave_inst_tail>` | -> | = { `<weave_field_value>` `<weave_field_list_tail>` } |
| 51 | `<weave_inst_tail>` | -> | `<weave_array_with_init>` |
| 52 | `<weave_field_value>` | -> | intlit |
| 53 | `<weave_field_value>` | -> | longlit |
| 54 | `<weave_field_value>` | -> | floatlit |
| 55 | `<weave_field_value>` | -> | doublelit |
| 56 | `<weave_field_value>` | -> | charlit |
| 57 | `<weave_field_value>` | -> | stringlit |
| 58 | `<weave_field_value>` | -> | true |
| 59 | `<weave_field_value>` | -> | false |
| 60 | `<weave_field_value>` | -> | { `<weave_value_list>` } |
| 61 | `<weave_value_list>` | -> | `<weave_field_value>` `<weave_value_tail>` |
| 62 | `<weave_value_tail>` | -> | , `<weave_field_value>` `<weave_value_tail>` |
| 63 | `<weave_value_tail>` | -> | λ |
| 64 | `<weave_field_list_tail>` | -> | , `<weave_field_value>` `<weave_field_list_tail>` |
| 65 | `<weave_field_list_tail>` | -> | λ |
| 66 | `<weave_inst_cont>` | -> | , id `<weave_inst_tail>` `<weave_inst_cont>` |
| 67 | `<weave_inst_cont>` | -> | λ |
| 68 | `<weave_arr_cont>` | -> | , id `<weave_array_with_init>` `<weave_arr_cont>` |
| 69 | `<weave_arr_cont>` | -> | λ |
| 70 | `<weave_array_with_init>` | -> | [ `<size>` ] `<weave_array_init_tail>` |
| 71 | `<weave_array_init_tail>` | -> | [ `<size>` ] `<weave_arr_init_opt_2d>` |
| 72 | `<weave_array_init_tail>` | -> | `<weave_arr_init_opt_1d>` |
| 73 | `<weave_arr_init_opt_1d>` | -> | = { `<weave_arr_init_content_1d>` } |
| 74 | `<weave_arr_init_opt_1d>` | -> | λ |
| 75 | `<weave_arr_init_content_1d>` | -> | { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_init_1d_tail>` |
| 76 | `<weave_init_1d_tail>` | -> | , { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_init_1d_tail>` |
| 77 | `<weave_init_1d_tail>` | -> | λ |
| 78 | `<weave_arr_init_opt_2d>` | -> | = { `<weave_arr_init_content_2d>` } |
| 79 | `<weave_arr_init_opt_2d>` | -> | λ |
| 80 | `<weave_arr_init_content_2d>` | -> | { `<weave_init_row>` } `<weave_init_2d_tail>` |
| 81 | `<weave_init_row>` | -> | { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_init_1d_tail>` |
| 82 | `<weave_init_2d_tail>` | -> | , { `<weave_init_row>` } `<weave_init_2d_tail>` |
| 83 | `<weave_init_2d_tail>` | -> | λ |
| 84 | `<mutability>` | -> | var |
| 85 | `<mutability>` | -> | const |
| 86 | `<array_dims>` | -> | [ `<size>` ] `<array_dim2_opt>` |
| 87 | `<array_dim2_opt>` | -> | [ `<size>` ] |
| 88 | `<array_dim2_opt>` | -> | λ |
| 89 | `<size>` | -> | intlit |
| 90 | `<size>` | -> | id |
| 91 | `<int_array_with_init>` | -> | [ `<size>` ] `<int_array_init_tail>` |
| 92 | `<int_array_init_tail>` | -> | [ `<size>` ] `<int_arr_init_opt_2d>` |
| 93 | `<int_array_init_tail>` | -> | `<int_arr_init_opt_1d>` |
| 94 | `<int_arr_init_opt_1d>` | -> | = { `<int_arr_init_content_1d>` } |
| 95 | `<int_arr_init_opt_1d>` | -> | λ |
| 96 | `<int_arr_init_content_1d>` | -> | intlit `<int_elem_1d_tail>` |
| 97 | `<int_elem_1d_tail>` | -> | , intlit `<int_elem_1d_tail>` |
| 98 | `<int_elem_1d_tail>` | -> | λ |
| 99 | `<int_arr_init_opt_2d>` | -> | = { `<int_arr_init_content_2d>` } |
| 100 | `<int_arr_init_opt_2d>` | -> | λ |
| 101 | `<int_arr_init_content_2d>` | -> | { `<int_elem_list>` } `<int_elem_2d_tail>` |
| 102 | `<int_elem_list>` | -> | intlit `<int_elem_1d_tail>` |
| 103 | `<int_elem_2d_tail>` | -> | , { `<int_elem_list>` } `<int_elem_2d_tail>` |
| 104 | `<int_elem_2d_tail>` | -> | λ |
| 105 | `<long_array_with_init>` | -> | [ `<size>` ] `<long_array_init_tail>` |
| 106 | `<long_array_init_tail>` | -> | [ `<size>` ] `<long_arr_init_opt_2d>` |
| 107 | `<long_array_init_tail>` | -> | `<long_arr_init_opt_1d>` |
| 108 | `<long_arr_init_opt_1d>` | -> | = { `<long_arr_init_content_1d>` } |
| 109 | `<long_arr_init_opt_1d>` | -> | λ |
| 110 | `<long_arr_init_content_1d>` | -> | longlit `<long_elem_1d_tail>` |
| 111 | `<long_elem_1d_tail>` | -> | , longlit `<long_elem_1d_tail>` |
| 112 | `<long_elem_1d_tail>` | -> | λ |
| 113 | `<long_arr_init_opt_2d>` | -> | = { `<long_arr_init_content_2d>` } |
| 114 | `<long_arr_init_opt_2d>` | -> | λ |
| 115 | `<long_arr_init_content_2d>` | -> | { `<long_elem_list>` } `<long_elem_2d_tail>` |
| 116 | `<long_elem_list>` | -> | longlit `<long_elem_1d_tail>` |
| 117 | `<long_elem_2d_tail>` | -> | , { `<long_elem_list>` } `<long_elem_2d_tail>` |
| 118 | `<long_elem_2d_tail>` | -> | λ |
| 119 | `<float_array_with_init>` | -> | [ `<size>` ] `<float_array_init_tail>` |
| 120 | `<float_array_init_tail>` | -> | [ `<size>` ] `<float_arr_init_opt_2d>` |
| 121 | `<float_array_init_tail>` | -> | `<float_arr_init_opt_1d>` |
| 122 | `<float_arr_init_opt_1d>` | -> | = { `<float_arr_init_content_1d>` } |
| 123 | `<float_arr_init_opt_1d>` | -> | λ |
| 124 | `<float_arr_init_content_1d>` | -> | floatlit `<float_elem_1d_tail>` |
| 125 | `<float_elem_1d_tail>` | -> | , floatlit `<float_elem_1d_tail>` |
| 126 | `<float_elem_1d_tail>` | -> | λ |
| 127 | `<float_arr_init_opt_2d>` | -> | = { `<float_arr_init_content_2d>` } |
| 128 | `<float_arr_init_opt_2d>` | -> | λ |
| 129 | `<float_arr_init_content_2d>` | -> | { `<float_elem_list>` } `<float_elem_2d_tail>` |
| 130 | `<float_elem_list>` | -> | floatlit `<float_elem_1d_tail>` |
| 131 | `<float_elem_2d_tail>` | -> | , { `<float_elem_list>` } `<float_elem_2d_tail>` |
| 132 | `<float_elem_2d_tail>` | -> | λ |
| 133 | `<double_array_with_init>` | -> | [ `<size>` ] `<double_array_init_tail>` |
| 134 | `<double_array_init_tail>` | -> | [ `<size>` ] `<double_arr_init_opt_2d>` |
| 135 | `<double_array_init_tail>` | -> | `<double_arr_init_opt_1d>` |
| 136 | `<double_arr_init_opt_1d>` | -> | = { `<double_arr_init_content_1d>` } |
| 137 | `<double_arr_init_opt_1d>` | -> | λ |
| 138 | `<double_arr_init_content_1d>` | -> | doublelit `<double_elem_1d_tail>` |
| 139 | `<double_elem_1d_tail>` | -> | , doublelit `<double_elem_1d_tail>` |
| 140 | `<double_elem_1d_tail>` | -> | λ |
| 141 | `<double_arr_init_opt_2d>` | -> | = { `<double_arr_init_content_2d>` } |
| 142 | `<double_arr_init_opt_2d>` | -> | λ |
| 143 | `<double_arr_init_content_2d>` | -> | { `<double_elem_list>` } `<double_elem_2d_tail>` |
| 144 | `<double_elem_list>` | -> | doublelit `<double_elem_1d_tail>` |
| 145 | `<double_elem_2d_tail>` | -> | , { `<double_elem_list>` } `<double_elem_2d_tail>` |
| 146 | `<double_elem_2d_tail>` | -> | λ |
| 147 | `<char_array_with_init>` | -> | [ `<size>` ] `<char_array_init_tail>` |
| 148 | `<char_array_init_tail>` | -> | [ `<size>` ] `<char_arr_init_opt_2d>` |
| 149 | `<char_array_init_tail>` | -> | `<char_arr_init_opt_1d>` |
| 150 | `<char_arr_init_opt_1d>` | -> | = { `<char_arr_init_content_1d>` } |
| 151 | `<char_arr_init_opt_1d>` | -> | λ |
| 152 | `<char_arr_init_content_1d>` | -> | charlit `<char_elem_1d_tail>` |
| 153 | `<char_elem_1d_tail>` | -> | , charlit `<char_elem_1d_tail>` |
| 154 | `<char_elem_1d_tail>` | -> | λ |
| 155 | `<char_arr_init_opt_2d>` | -> | = { `<char_arr_init_content_2d>` } |
| 156 | `<char_arr_init_opt_2d>` | -> | λ |
| 157 | `<char_arr_init_content_2d>` | -> | { `<char_elem_list>` } `<char_elem_2d_tail>` |
| 158 | `<char_elem_list>` | -> | charlit `<char_elem_1d_tail>` |
| 159 | `<char_elem_2d_tail>` | -> | , { `<char_elem_list>` } `<char_elem_2d_tail>` |
| 160 | `<char_elem_2d_tail>` | -> | λ |
| 161 | `<string_array_with_init>` | -> | [ `<size>` ] `<string_array_init_tail>` |
| 162 | `<string_array_init_tail>` | -> | [ `<size>` ] `<string_arr_init_opt_2d>` |
| 163 | `<string_array_init_tail>` | -> | `<string_arr_init_opt_1d>` |
| 164 | `<string_arr_init_opt_1d>` | -> | = { `<string_arr_init_content_1d>` } |
| 165 | `<string_arr_init_opt_1d>` | -> | λ |
| 166 | `<string_arr_init_content_1d>` | -> | stringlit `<string_elem_1d_tail>` |
| 167 | `<string_elem_1d_tail>` | -> | , stringlit `<string_elem_1d_tail>` |
| 168 | `<string_elem_1d_tail>` | -> | λ |
| 169 | `<string_arr_init_opt_2d>` | -> | = { `<string_arr_init_content_2d>` } |
| 170 | `<string_arr_init_opt_2d>` | -> | λ |
| 171 | `<string_arr_init_content_2d>` | -> | { `<string_elem_list>` } `<string_elem_2d_tail>` |
| 172 | `<string_elem_list>` | -> | stringlit `<string_elem_1d_tail>` |
| 173 | `<string_elem_2d_tail>` | -> | , { `<string_elem_list>` } `<string_elem_2d_tail>` |
| 174 | `<string_elem_2d_tail>` | -> | λ |
| 175 | `<bool_array_with_init>` | -> | [ `<size>` ] `<bool_array_init_tail>` |
| 176 | `<bool_array_init_tail>` | -> | [ `<size>` ] `<bool_arr_init_opt_2d>` |
| 177 | `<bool_array_init_tail>` | -> | `<bool_arr_init_opt_1d>` |
| 178 | `<bool_arr_init_opt_1d>` | -> | = { `<bool_arr_init_content_1d>` } |
| 179 | `<bool_arr_init_opt_1d>` | -> | λ |
| 180 | `<bool_arr_init_content_1d>` | -> | `<bool_lit>` `<bool_elem_1d_tail>` |
| 181 | `<bool_elem_1d_tail>` | -> | , `<bool_lit>` `<bool_elem_1d_tail>` |
| 182 | `<bool_elem_1d_tail>` | -> | λ |
| 183 | `<bool_arr_init_opt_2d>` | -> | = { `<bool_arr_init_content_2d>` } |
| 184 | `<bool_arr_init_opt_2d>` | -> | λ |
| 185 | `<bool_arr_init_content_2d>` | -> | { `<bool_elem_list>` } `<bool_elem_2d_tail>` |
| 186 | `<bool_elem_list>` | -> | `<bool_lit>` `<bool_elem_1d_tail>` |
| 187 | `<bool_elem_2d_tail>` | -> | , { `<bool_elem_list>` } `<bool_elem_2d_tail>` |
| 188 | `<bool_elem_2d_tail>` | -> | λ |
| 189 | `<field_list>` | -> | `<field_dec>` `<field_list>` |
| 190 | `<field_list>` | -> | λ |
| 191 | `<field_dec>` | -> | `<field_type>` id `<field_arr_opt>` `<field_cont>` ; |
| 192 | `<field_type>` | -> | int |
| 193 | `<field_type>` | -> | long |
| 194 | `<field_type>` | -> | float |
| 195 | `<field_type>` | -> | double |
| 196 | `<field_type>` | -> | char |
| 197 | `<field_type>` | -> | string |
| 198 | `<field_type>` | -> | bool |
| 199 | `<field_type>` | -> | id |
| 200 | `<field_arr_opt>` | -> | `<array_dims>` |
| 201 | `<field_arr_opt>` | -> | λ |
| 202 | `<field_cont>` | -> | , id `<field_arr_opt>` `<field_cont>` |
| 203 | `<field_cont>` | -> | λ |
| 204 | `<func_ret_int>` | -> | id ( `<param_list>` ) { `<function_body_int>` } |
| 205 | `<func_ret_int>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 206 | `<func_ret_long>` | -> | id ( `<param_list>` ) { `<function_body_long>` } |
| 207 | `<func_ret_long>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 208 | `<func_ret_float>` | -> | id ( `<param_list>` ) { `<function_body_float>` } |
| 209 | `<func_ret_float>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 210 | `<func_ret_double>` | -> | id ( `<param_list>` ) { `<function_body_double>` } |
| 211 | `<func_ret_double>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 212 | `<func_ret_char>` | -> | id ( `<param_list>` ) { `<function_body_char>` } |
| 213 | `<func_ret_char>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 214 | `<func_ret_string>` | -> | id ( `<param_list>` ) { `<function_body_string>` } |
| 215 | `<func_ret_string>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 216 | `<func_ret_bool>` | -> | id ( `<param_list>` ) { `<function_body_bool>` } |
| 217 | `<func_ret_bool>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 218 | `<func_ret_weave>` | -> | id ( `<param_list>` ) { `<function_body_weave>` } |
| 219 | `<func_ret_weave>` | -> | `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } |
| 220 | `<func_ret_weave>` | -> | . id id ( `<param_list>` ) { `<function_body_weave>` } |
| 221 | `<param_list>` | -> | `<param_type>` id `<param_arr_opt>` `<param_cont>` |
| 222 | `<param_list>` | -> | λ |
| 223 | `<param_type>` | -> | int |
| 224 | `<param_type>` | -> | long |
| 225 | `<param_type>` | -> | float |
| 226 | `<param_type>` | -> | double |
| 227 | `<param_type>` | -> | char |
| 228 | `<param_type>` | -> | string |
| 229 | `<param_type>` | -> | bool |
| 230 | `<param_type>` | -> | id |
| 231 | `<param_arr_opt>` | -> | `<array_dims>` |
| 232 | `<param_arr_opt>` | -> | λ |
| 233 | `<param_cont>` | -> | , `<param_type>` id `<param_arr_opt>` `<param_cont>` |
| 234 | `<param_cont>` | -> | λ |
| 235 | `<function_body_int>` | -> | `<func_content_int>` |
| 236 | `<func_content_int>` | -> | using id `<using_cont>` ; `<func_content_int>` |
| 237 | `<func_content_int>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_int>` |
| 238 | `<func_content_int>` | -> | `<statement_int>` `<func_content_int>` |
| 239 | `<func_content_int>` | -> | λ |
| 240 | `<function_body_long>` | -> | `<func_content_long>` |
| 241 | `<func_content_long>` | -> | using id `<using_cont>` ; `<func_content_long>` |
| 242 | `<func_content_long>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_long>` |
| 243 | `<func_content_long>` | -> | `<statement_long>` `<func_content_long>` |
| 244 | `<func_content_long>` | -> | λ |
| 245 | `<function_body_float>` | -> | `<func_content_float>` |
| 246 | `<func_content_float>` | -> | using id `<using_cont>` ; `<func_content_float>` |
| 247 | `<func_content_float>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_float>` |
| 248 | `<func_content_float>` | -> | `<statement_float>` `<func_content_float>` |
| 249 | `<func_content_float>` | -> | λ |
| 250 | `<function_body_double>` | -> | `<func_content_double>` |
| 251 | `<func_content_double>` | -> | using id `<using_cont>` ; `<func_content_double>` |
| 252 | `<func_content_double>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_double>` |
| 253 | `<func_content_double>` | -> | `<statement_double>` `<func_content_double>` |
| 254 | `<func_content_double>` | -> | λ |
| 255 | `<function_body_char>` | -> | `<func_content_char>` |
| 256 | `<func_content_char>` | -> | using id `<using_cont>` ; `<func_content_char>` |
| 257 | `<func_content_char>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_char>` |
| 258 | `<func_content_char>` | -> | `<statement_char>` `<func_content_char>` |
| 259 | `<func_content_char>` | -> | λ |
| 260 | `<function_body_string>` | -> | `<func_content_string>` |
| 261 | `<func_content_string>` | -> | using id `<using_cont>` ; `<func_content_string>` |
| 262 | `<func_content_string>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_string>` |
| 263 | `<func_content_string>` | -> | `<statement_string>` `<func_content_string>` |
| 264 | `<func_content_string>` | -> | λ |
| 265 | `<function_body_bool>` | -> | `<func_content_bool>` |
| 266 | `<func_content_bool>` | -> | using id `<using_cont>` ; `<func_content_bool>` |
| 267 | `<func_content_bool>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_bool>` |
| 268 | `<func_content_bool>` | -> | `<statement_bool>` `<func_content_bool>` |
| 269 | `<func_content_bool>` | -> | λ |
| 270 | `<function_body_array>` | -> | `<func_content_array>` |
| 271 | `<func_content_array>` | -> | using id `<using_cont>` ; `<func_content_array>` |
| 272 | `<func_content_array>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_array>` |
| 273 | `<func_content_array>` | -> | `<statement_array>` `<func_content_array>` |
| 274 | `<func_content_array>` | -> | λ |
| 275 | `<function_body_weave>` | -> | `<func_content_weave>` |
| 276 | `<func_content_weave>` | -> | using id `<using_cont>` ; `<func_content_weave>` |
| 277 | `<func_content_weave>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_weave>` |
| 278 | `<func_content_weave>` | -> | `<statement_weave>` `<func_content_weave>` |
| 279 | `<func_content_weave>` | -> | λ |
| 280 | `<function_body_void>` | -> | `<func_content_void>` |
| 281 | `<func_content_void>` | -> | using id `<using_cont>` ; `<func_content_void>` |
| 282 | `<func_content_void>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_void>` |
| 283 | `<func_content_void>` | -> | `<statement_void>` `<func_content_void>` |
| 284 | `<func_content_void>` | -> | λ |
| 285 | `<statement_int>` | -> | `<effect_stmt>` ; |
| 286 | `<statement_int>` | -> | `<io_stmt>` |
| 287 | `<statement_int>` | -> | `<ctrl_struct_int>` |
| 288 | `<statement_int>` | -> | break ; |
| 289 | `<statement_int>` | -> | return `<int_return_expr>` ; |
| 290 | `<statement_long>` | -> | `<effect_stmt>` ; |
| 291 | `<statement_long>` | -> | `<io_stmt>` |
| 292 | `<statement_long>` | -> | `<ctrl_struct_long>` |
| 293 | `<statement_long>` | -> | break ; |
| 294 | `<statement_long>` | -> | return `<long_return_expr>` ; |
| 295 | `<statement_float>` | -> | `<effect_stmt>` ; |
| 296 | `<statement_float>` | -> | `<io_stmt>` |
| 297 | `<statement_float>` | -> | `<ctrl_struct_float>` |
| 298 | `<statement_float>` | -> | break ; |
| 299 | `<statement_float>` | -> | return `<float_return_expr>` ; |
| 300 | `<statement_double>` | -> | `<effect_stmt>` ; |
| 301 | `<statement_double>` | -> | `<io_stmt>` |
| 302 | `<statement_double>` | -> | `<ctrl_struct_double>` |
| 303 | `<statement_double>` | -> | break ; |
| 304 | `<statement_double>` | -> | return `<double_return_expr>` ; |
| 305 | `<statement_char>` | -> | `<effect_stmt>` ; |
| 306 | `<statement_char>` | -> | `<io_stmt>` |
| 307 | `<statement_char>` | -> | `<ctrl_struct_char>` |
| 308 | `<statement_char>` | -> | break ; |
| 309 | `<statement_char>` | -> | return `<char_return_expr>` ; |
| 310 | `<statement_string>` | -> | `<effect_stmt>` ; |
| 311 | `<statement_string>` | -> | `<io_stmt>` |
| 312 | `<statement_string>` | -> | `<ctrl_struct_string>` |
| 313 | `<statement_string>` | -> | break ; |
| 314 | `<statement_string>` | -> | return `<string_return_expr>` ; |
| 315 | `<statement_bool>` | -> | `<effect_stmt>` ; |
| 316 | `<statement_bool>` | -> | `<io_stmt>` |
| 317 | `<statement_bool>` | -> | `<ctrl_struct_bool>` |
| 318 | `<statement_bool>` | -> | break ; |
| 319 | `<statement_bool>` | -> | return `<bool_return_expr>` ; |
| 320 | `<statement_array>` | -> | `<effect_stmt>` ; |
| 321 | `<statement_array>` | -> | `<io_stmt>` |
| 322 | `<statement_array>` | -> | `<ctrl_struct_array>` |
| 323 | `<statement_array>` | -> | break ; |
| 324 | `<statement_array>` | -> | return id ; |
| 325 | `<statement_weave>` | -> | `<effect_stmt>` ; |
| 326 | `<statement_weave>` | -> | `<io_stmt>` |
| 327 | `<statement_weave>` | -> | `<ctrl_struct_weave>` |
| 328 | `<statement_weave>` | -> | break ; |
| 329 | `<statement_weave>` | -> | return id ; |
| 330 | `<statement_void>` | -> | `<effect_stmt>` ; |
| 331 | `<statement_void>` | -> | `<io_stmt>` |
| 332 | `<statement_void>` | -> | `<ctrl_struct_void>` |
| 333 | `<statement_void>` | -> | break ; |
| 334 | `<statement_void>` | -> | return ; |
| 335 | `<ctrl_struct_int>` | -> | if ( `<condition>` ) { `<stmt_list_int>` } `<else_opt_int>` |
| 336 | `<ctrl_struct_int>` | -> | switch ( `<arg_expr>` ) { `<case_list_int>` `<default_opt_int>` } |
| 337 | `<ctrl_struct_int>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_int>` } |
| 338 | `<ctrl_struct_int>` | -> | while ( `<condition>` ) { `<stmt_list_int>` } |
| 339 | `<ctrl_struct_int>` | -> | do { `<stmt_list_int>` } while ( `<condition>` ) ; |
| 340 | `<stmt_list_int>` | -> | `<statement_int>` `<stmt_list_int>` |
| 341 | `<stmt_list_int>` | -> | λ |
| 342 | `<else_opt_int>` | -> | else `<else_body_int>` |
| 343 | `<else_opt_int>` | -> | λ |
| 344 | `<else_body_int>` | -> | { `<stmt_list_int>` } |
| 345 | `<else_body_int>` | -> | if ( `<condition>` ) { `<stmt_list_int>` } `<else_opt_int>` |
| 346 | `<case_list_int>` | -> | case `<case_val>` : `<stmt_list_int>` `<break_opt>` `<case_list_int>` |
| 347 | `<case_list_int>` | -> | λ |
| 348 | `<default_opt_int>` | -> | default : `<stmt_list_int>` `<break_opt>` |
| 349 | `<default_opt_int>` | -> | λ |
| 350 | `<ctrl_struct_long>` | -> | if ( `<condition>` ) { `<stmt_list_long>` } `<else_opt_long>` |
| 351 | `<ctrl_struct_long>` | -> | switch ( `<arg_expr>` ) { `<case_list_long>` `<default_opt_long>` } |
| 352 | `<ctrl_struct_long>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_long>` } |
| 353 | `<ctrl_struct_long>` | -> | while ( `<condition>` ) { `<stmt_list_long>` } |
| 354 | `<ctrl_struct_long>` | -> | do { `<stmt_list_long>` } while ( `<condition>` ) ; |
| 355 | `<stmt_list_long>` | -> | `<statement_long>` `<stmt_list_long>` |
| 356 | `<stmt_list_long>` | -> | λ |
| 357 | `<else_opt_long>` | -> | else `<else_body_long>` |
| 358 | `<else_opt_long>` | -> | λ |
| 359 | `<else_body_long>` | -> | { `<stmt_list_long>` } |
| 360 | `<else_body_long>` | -> | if ( `<condition>` ) { `<stmt_list_long>` } `<else_opt_long>` |
| 361 | `<case_list_long>` | -> | case `<case_val>` : `<stmt_list_long>` `<break_opt>` `<case_list_long>` |
| 362 | `<case_list_long>` | -> | λ |
| 363 | `<default_opt_long>` | -> | default : `<stmt_list_long>` `<break_opt>` |
| 364 | `<default_opt_long>` | -> | λ |
| 365 | `<ctrl_struct_float>` | -> | if ( `<condition>` ) { `<stmt_list_float>` } `<else_opt_float>` |
| 366 | `<ctrl_struct_float>` | -> | switch ( `<arg_expr>` ) { `<case_list_float>` `<default_opt_float>` } |
| 367 | `<ctrl_struct_float>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_float>` } |
| 368 | `<ctrl_struct_float>` | -> | while ( `<condition>` ) { `<stmt_list_float>` } |
| 369 | `<ctrl_struct_float>` | -> | do { `<stmt_list_float>` } while ( `<condition>` ) ; |
| 370 | `<stmt_list_float>` | -> | `<statement_float>` `<stmt_list_float>` |
| 371 | `<stmt_list_float>` | -> | λ |
| 372 | `<else_opt_float>` | -> | else `<else_body_float>` |
| 373 | `<else_opt_float>` | -> | λ |
| 374 | `<else_body_float>` | -> | { `<stmt_list_float>` } |
| 375 | `<else_body_float>` | -> | if ( `<condition>` ) { `<stmt_list_float>` } `<else_opt_float>` |
| 376 | `<case_list_float>` | -> | case `<case_val>` : `<stmt_list_float>` `<break_opt>` `<case_list_float>` |
| 377 | `<case_list_float>` | -> | λ |
| 378 | `<default_opt_float>` | -> | default : `<stmt_list_float>` `<break_opt>` |
| 379 | `<default_opt_float>` | -> | λ |
| 380 | `<ctrl_struct_double>` | -> | if ( `<condition>` ) { `<stmt_list_double>` } `<else_opt_double>` |
| 381 | `<ctrl_struct_double>` | -> | switch ( `<arg_expr>` ) { `<case_list_double>` `<default_opt_double>` } |
| 382 | `<ctrl_struct_double>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_double>` } |
| 383 | `<ctrl_struct_double>` | -> | while ( `<condition>` ) { `<stmt_list_double>` } |
| 384 | `<ctrl_struct_double>` | -> | do { `<stmt_list_double>` } while ( `<condition>` ) ; |
| 385 | `<stmt_list_double>` | -> | `<statement_double>` `<stmt_list_double>` |
| 386 | `<stmt_list_double>` | -> | λ |
| 387 | `<else_opt_double>` | -> | else `<else_body_double>` |
| 388 | `<else_opt_double>` | -> | λ |
| 389 | `<else_body_double>` | -> | { `<stmt_list_double>` } |
| 390 | `<else_body_double>` | -> | if ( `<condition>` ) { `<stmt_list_double>` } `<else_opt_double>` |
| 391 | `<case_list_double>` | -> | case `<case_val>` : `<stmt_list_double>` `<break_opt>` `<case_list_double>` |
| 392 | `<case_list_double>` | -> | λ |
| 393 | `<default_opt_double>` | -> | default : `<stmt_list_double>` `<break_opt>` |
| 394 | `<default_opt_double>` | -> | λ |
| 395 | `<ctrl_struct_char>` | -> | if ( `<condition>` ) { `<stmt_list_char>` } `<else_opt_char>` |
| 396 | `<ctrl_struct_char>` | -> | switch ( `<arg_expr>` ) { `<case_list_char>` `<default_opt_char>` } |
| 397 | `<ctrl_struct_char>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_char>` } |
| 398 | `<ctrl_struct_char>` | -> | while ( `<condition>` ) { `<stmt_list_char>` } |
| 399 | `<ctrl_struct_char>` | -> | do { `<stmt_list_char>` } while ( `<condition>` ) ; |
| 400 | `<stmt_list_char>` | -> | `<statement_char>` `<stmt_list_char>` |
| 401 | `<stmt_list_char>` | -> | λ |
| 402 | `<else_opt_char>` | -> | else `<else_body_char>` |
| 403 | `<else_opt_char>` | -> | λ |
| 404 | `<else_body_char>` | -> | { `<stmt_list_char>` } |
| 405 | `<else_body_char>` | -> | if ( `<condition>` ) { `<stmt_list_char>` } `<else_opt_char>` |
| 406 | `<case_list_char>` | -> | case `<case_val>` : `<stmt_list_char>` `<break_opt>` `<case_list_char>` |
| 407 | `<case_list_char>` | -> | λ |
| 408 | `<default_opt_char>` | -> | default : `<stmt_list_char>` `<break_opt>` |
| 409 | `<default_opt_char>` | -> | λ |
| 410 | `<ctrl_struct_string>` | -> | if ( `<condition>` ) { `<stmt_list_string>` } `<else_opt_string>` |
| 411 | `<ctrl_struct_string>` | -> | switch ( `<arg_expr>` ) { `<case_list_string>` `<default_opt_string>` } |
| 412 | `<ctrl_struct_string>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_string>` } |
| 413 | `<ctrl_struct_string>` | -> | while ( `<condition>` ) { `<stmt_list_string>` } |
| 414 | `<ctrl_struct_string>` | -> | do { `<stmt_list_string>` } while ( `<condition>` ) ; |
| 415 | `<stmt_list_string>` | -> | `<statement_string>` `<stmt_list_string>` |
| 416 | `<stmt_list_string>` | -> | λ |
| 417 | `<else_opt_string>` | -> | else `<else_body_string>` |
| 418 | `<else_opt_string>` | -> | λ |
| 419 | `<else_body_string>` | -> | { `<stmt_list_string>` } |
| 420 | `<else_body_string>` | -> | if ( `<condition>` ) { `<stmt_list_string>` } `<else_opt_string>` |
| 421 | `<case_list_string>` | -> | case `<case_val>` : `<stmt_list_string>` `<break_opt>` `<case_list_string>` |
| 422 | `<case_list_string>` | -> | λ |
| 423 | `<default_opt_string>` | -> | default : `<stmt_list_string>` `<break_opt>` |
| 424 | `<default_opt_string>` | -> | λ |
| 425 | `<ctrl_struct_bool>` | -> | if ( `<condition>` ) { `<stmt_list_bool>` } `<else_opt_bool>` |
| 426 | `<ctrl_struct_bool>` | -> | switch ( `<arg_expr>` ) { `<case_list_bool>` `<default_opt_bool>` } |
| 427 | `<ctrl_struct_bool>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_bool>` } |
| 428 | `<ctrl_struct_bool>` | -> | while ( `<condition>` ) { `<stmt_list_bool>` } |
| 429 | `<ctrl_struct_bool>` | -> | do { `<stmt_list_bool>` } while ( `<condition>` ) ; |
| 430 | `<stmt_list_bool>` | -> | `<statement_bool>` `<stmt_list_bool>` |
| 431 | `<stmt_list_bool>` | -> | λ |
| 432 | `<else_opt_bool>` | -> | else `<else_body_bool>` |
| 433 | `<else_opt_bool>` | -> | λ |
| 434 | `<else_body_bool>` | -> | { `<stmt_list_bool>` } |
| 435 | `<else_body_bool>` | -> | if ( `<condition>` ) { `<stmt_list_bool>` } `<else_opt_bool>` |
| 436 | `<case_list_bool>` | -> | case `<case_val>` : `<stmt_list_bool>` `<break_opt>` `<case_list_bool>` |
| 437 | `<case_list_bool>` | -> | λ |
| 438 | `<default_opt_bool>` | -> | default : `<stmt_list_bool>` `<break_opt>` |
| 439 | `<default_opt_bool>` | -> | λ |
| 440 | `<ctrl_struct_array>` | -> | if ( `<condition>` ) { `<stmt_list_array>` } `<else_opt_array>` |
| 441 | `<ctrl_struct_array>` | -> | switch ( `<arg_expr>` ) { `<case_list_array>` `<default_opt_array>` } |
| 442 | `<ctrl_struct_array>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_array>` } |
| 443 | `<ctrl_struct_array>` | -> | while ( `<condition>` ) { `<stmt_list_array>` } |
| 444 | `<ctrl_struct_array>` | -> | do { `<stmt_list_array>` } while ( `<condition>` ) ; |
| 445 | `<stmt_list_array>` | -> | `<statement_array>` `<stmt_list_array>` |
| 446 | `<stmt_list_array>` | -> | λ |
| 447 | `<else_opt_array>` | -> | else `<else_body_array>` |
| 448 | `<else_opt_array>` | -> | λ |
| 449 | `<else_body_array>` | -> | { `<stmt_list_array>` } |
| 450 | `<else_body_array>` | -> | if ( `<condition>` ) { `<stmt_list_array>` } `<else_opt_array>` |
| 451 | `<case_list_array>` | -> | case `<case_val>` : `<stmt_list_array>` `<break_opt>` `<case_list_array>` |
| 452 | `<case_list_array>` | -> | λ |
| 453 | `<default_opt_array>` | -> | default : `<stmt_list_array>` `<break_opt>` |
| 454 | `<default_opt_array>` | -> | λ |
| 455 | `<ctrl_struct_weave>` | -> | if ( `<condition>` ) { `<stmt_list_weave>` } `<else_opt_weave>` |
| 456 | `<ctrl_struct_weave>` | -> | switch ( `<arg_expr>` ) { `<case_list_weave>` `<default_opt_weave>` } |
| 457 | `<ctrl_struct_weave>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_weave>` } |
| 458 | `<ctrl_struct_weave>` | -> | while ( `<condition>` ) { `<stmt_list_weave>` } |
| 459 | `<ctrl_struct_weave>` | -> | do { `<stmt_list_weave>` } while ( `<condition>` ) ; |
| 460 | `<stmt_list_weave>` | -> | `<statement_weave>` `<stmt_list_weave>` |
| 461 | `<stmt_list_weave>` | -> | λ |
| 462 | `<else_opt_weave>` | -> | else `<else_body_weave>` |
| 463 | `<else_opt_weave>` | -> | λ |
| 464 | `<else_body_weave>` | -> | { `<stmt_list_weave>` } |
| 465 | `<else_body_weave>` | -> | if ( `<condition>` ) { `<stmt_list_weave>` } `<else_opt_weave>` |
| 466 | `<case_list_weave>` | -> | case `<case_val>` : `<stmt_list_weave>` `<break_opt>` `<case_list_weave>` |
| 467 | `<case_list_weave>` | -> | λ |
| 468 | `<default_opt_weave>` | -> | default : `<stmt_list_weave>` `<break_opt>` |
| 469 | `<default_opt_weave>` | -> | λ |
| 470 | `<ctrl_struct_void>` | -> | if ( `<condition>` ) { `<stmt_list_void>` } `<else_opt_void>` |
| 471 | `<ctrl_struct_void>` | -> | switch ( `<arg_expr>` ) { `<case_list_void>` `<default_opt_void>` } |
| 472 | `<ctrl_struct_void>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<stmt_list_void>` } |
| 473 | `<ctrl_struct_void>` | -> | while ( `<condition>` ) { `<stmt_list_void>` } |
| 474 | `<ctrl_struct_void>` | -> | do { `<stmt_list_void>` } while ( `<condition>` ) ; |
| 475 | `<stmt_list_void>` | -> | `<statement_void>` `<stmt_list_void>` |
| 476 | `<stmt_list_void>` | -> | λ |
| 477 | `<else_opt_void>` | -> | else `<else_body_void>` |
| 478 | `<else_opt_void>` | -> | λ |
| 479 | `<else_body_void>` | -> | { `<stmt_list_void>` } |
| 480 | `<else_body_void>` | -> | if ( `<condition>` ) { `<stmt_list_void>` } `<else_opt_void>` |
| 481 | `<case_list_void>` | -> | case `<case_val>` : `<stmt_list_void>` `<break_opt>` `<case_list_void>` |
| 482 | `<case_list_void>` | -> | λ |
| 483 | `<default_opt_void>` | -> | default : `<stmt_list_void>` `<break_opt>` |
| 484 | `<default_opt_void>` | -> | λ |
| 485 | `<int_return_expr>` | -> | `<int_ret_assign>` |
| 486 | `<int_ret_assign>` | -> | `<int_ret_concat>` `<assign_tail>` |
| 487 | `<int_ret_concat>` | -> | `<int_ret_or>` `<concat_tail>` |
| 488 | `<int_ret_or>` | -> | `<int_ret_and>` `<or_tail>` |
| 489 | `<int_ret_and>` | -> | `<int_ret_eq>` `<and_tail>` |
| 490 | `<int_ret_eq>` | -> | `<int_ret_rel>` `<eq_tail>` |
| 491 | `<int_ret_rel>` | -> | `<int_ret_add>` `<rel_tail>` |
| 492 | `<int_ret_add>` | -> | `<int_ret_mul>` `<add_tail>` |
| 493 | `<int_ret_mul>` | -> | `<int_ret_unary>` `<mul_tail>` |
| 494 | `<int_ret_unary>` | -> | ! `<int_ret_unary>` |
| 495 | `<int_ret_unary>` | -> | `<int_ret_postfix>` |
| 496 | `<int_ret_postfix>` | -> | intlit |
| 497 | `<int_ret_postfix>` | -> | ++ id |
| 498 | `<int_ret_postfix>` | -> | -- id |
| 499 | `<int_ret_postfix>` | -> | id `<id_postfix>` |
| 500 | `<int_ret_postfix>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 501 | `<int_ret_postfix>` | -> | int ( `<expression>` ) |
| 502 | `<long_return_expr>` | -> | `<long_ret_assign>` |
| 503 | `<long_ret_assign>` | -> | `<long_ret_concat>` `<assign_tail>` |
| 504 | `<long_ret_concat>` | -> | `<long_ret_or>` `<concat_tail>` |
| 505 | `<long_ret_or>` | -> | `<long_ret_and>` `<or_tail>` |
| 506 | `<long_ret_and>` | -> | `<long_ret_eq>` `<and_tail>` |
| 507 | `<long_ret_eq>` | -> | `<long_ret_rel>` `<eq_tail>` |
| 508 | `<long_ret_rel>` | -> | `<long_ret_add>` `<rel_tail>` |
| 509 | `<long_ret_add>` | -> | `<long_ret_mul>` `<add_tail>` |
| 510 | `<long_ret_mul>` | -> | `<long_ret_unary>` `<mul_tail>` |
| 511 | `<long_ret_unary>` | -> | ! `<long_ret_unary>` |
| 512 | `<long_ret_unary>` | -> | `<long_ret_postfix>` |
| 513 | `<long_ret_postfix>` | -> | longlit |
| 514 | `<long_ret_postfix>` | -> | ++ id |
| 515 | `<long_ret_postfix>` | -> | -- id |
| 516 | `<long_ret_postfix>` | -> | id `<id_postfix>` |
| 517 | `<long_ret_postfix>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 518 | `<long_ret_postfix>` | -> | long ( `<expression>` ) |
| 519 | `<float_return_expr>` | -> | `<float_ret_assign>` |
| 520 | `<float_ret_assign>` | -> | `<float_ret_concat>` `<assign_tail>` |
| 521 | `<float_ret_concat>` | -> | `<float_ret_or>` `<concat_tail>` |
| 522 | `<float_ret_or>` | -> | `<float_ret_and>` `<or_tail>` |
| 523 | `<float_ret_and>` | -> | `<float_ret_eq>` `<and_tail>` |
| 524 | `<float_ret_eq>` | -> | `<float_ret_rel>` `<eq_tail>` |
| 525 | `<float_ret_rel>` | -> | `<float_ret_add>` `<rel_tail>` |
| 526 | `<float_ret_add>` | -> | `<float_ret_mul>` `<add_tail>` |
| 527 | `<float_ret_mul>` | -> | `<float_ret_unary>` `<mul_tail>` |
| 528 | `<float_ret_unary>` | -> | ! `<float_ret_unary>` |
| 529 | `<float_ret_unary>` | -> | `<float_ret_postfix>` |
| 530 | `<float_ret_postfix>` | -> | floatlit |
| 531 | `<float_ret_postfix>` | -> | ++ id |
| 532 | `<float_ret_postfix>` | -> | -- id |
| 533 | `<float_ret_postfix>` | -> | id `<id_postfix>` |
| 534 | `<float_ret_postfix>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 535 | `<float_ret_postfix>` | -> | float ( `<expression>` ) |
| 536 | `<double_return_expr>` | -> | `<double_ret_assign>` |
| 537 | `<double_ret_assign>` | -> | `<double_ret_concat>` `<assign_tail>` |
| 538 | `<double_ret_concat>` | -> | `<double_ret_or>` `<concat_tail>` |
| 539 | `<double_ret_or>` | -> | `<double_ret_and>` `<or_tail>` |
| 540 | `<double_ret_and>` | -> | `<double_ret_eq>` `<and_tail>` |
| 541 | `<double_ret_eq>` | -> | `<double_ret_rel>` `<eq_tail>` |
| 542 | `<double_ret_rel>` | -> | `<double_ret_add>` `<rel_tail>` |
| 543 | `<double_ret_add>` | -> | `<double_ret_mul>` `<add_tail>` |
| 544 | `<double_ret_mul>` | -> | `<double_ret_unary>` `<mul_tail>` |
| 545 | `<double_ret_unary>` | -> | ! `<double_ret_unary>` |
| 546 | `<double_ret_unary>` | -> | `<double_ret_postfix>` |
| 547 | `<double_ret_postfix>` | -> | doublelit |
| 548 | `<double_ret_postfix>` | -> | ++ id |
| 549 | `<double_ret_postfix>` | -> | -- id |
| 550 | `<double_ret_postfix>` | -> | id `<id_postfix>` |
| 551 | `<double_ret_postfix>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 552 | `<double_ret_postfix>` | -> | double ( `<expression>` ) |
| 553 | `<char_return_expr>` | -> | `<char_ret_assign>` |
| 554 | `<char_ret_assign>` | -> | `<char_ret_concat>` `<assign_tail>` |
| 555 | `<char_ret_concat>` | -> | `<char_ret_or>` `<concat_tail>` |
| 556 | `<char_ret_or>` | -> | `<char_ret_and>` `<or_tail>` |
| 557 | `<char_ret_and>` | -> | `<char_ret_eq>` `<and_tail>` |
| 558 | `<char_ret_eq>` | -> | `<char_ret_rel>` `<eq_tail>` |
| 559 | `<char_ret_rel>` | -> | `<char_ret_add>` `<rel_tail>` |
| 560 | `<char_ret_add>` | -> | `<char_ret_mul>` `<add_tail>` |
| 561 | `<char_ret_mul>` | -> | `<char_ret_unary>` `<mul_tail>` |
| 562 | `<char_ret_unary>` | -> | ! `<char_ret_unary>` |
| 563 | `<char_ret_unary>` | -> | `<char_ret_postfix>` |
| 564 | `<char_ret_postfix>` | -> | charlit |
| 565 | `<char_ret_postfix>` | -> | ++ id |
| 566 | `<char_ret_postfix>` | -> | -- id |
| 567 | `<char_ret_postfix>` | -> | id `<id_postfix>` |
| 568 | `<char_ret_postfix>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 569 | `<char_ret_postfix>` | -> | char ( `<expression>` ) |
| 570 | `<string_return_expr>` | -> | `<string_ret_assign>` |
| 571 | `<string_ret_assign>` | -> | `<string_ret_concat>` `<assign_tail>` |
| 572 | `<string_ret_concat>` | -> | `<string_ret_or>` `<concat_tail>` |
| 573 | `<string_ret_or>` | -> | `<string_ret_and>` `<or_tail>` |
| 574 | `<string_ret_and>` | -> | `<string_ret_eq>` `<and_tail>` |
| 575 | `<string_ret_eq>` | -> | `<string_ret_rel>` `<eq_tail>` |
| 576 | `<string_ret_rel>` | -> | `<string_ret_add>` `<rel_tail>` |
| 577 | `<string_ret_add>` | -> | `<string_ret_mul>` `<add_tail>` |
| 578 | `<string_ret_mul>` | -> | `<string_ret_unary>` `<mul_tail>` |
| 579 | `<string_ret_unary>` | -> | ! `<string_ret_unary>` |
| 580 | `<string_ret_unary>` | -> | `<string_ret_postfix>` |
| 581 | `<string_ret_postfix>` | -> | stringlit |
| 582 | `<string_ret_postfix>` | -> | ++ id |
| 583 | `<string_ret_postfix>` | -> | -- id |
| 584 | `<string_ret_postfix>` | -> | id `<id_postfix>` |
| 585 | `<string_ret_postfix>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 586 | `<string_ret_postfix>` | -> | string ( `<expression>` ) |
| 587 | `<bool_return_expr>` | -> | `<bool_ret_assign>` |
| 588 | `<bool_ret_assign>` | -> | `<bool_ret_concat>` `<assign_tail>` |
| 589 | `<bool_ret_concat>` | -> | `<bool_ret_or>` `<concat_tail>` |
| 590 | `<bool_ret_or>` | -> | `<bool_ret_and>` `<or_tail>` |
| 591 | `<bool_ret_and>` | -> | `<bool_ret_eq>` `<and_tail>` |
| 592 | `<bool_ret_eq>` | -> | `<bool_ret_rel>` `<eq_tail>` |
| 593 | `<bool_ret_rel>` | -> | `<bool_ret_add>` `<rel_tail>` |
| 594 | `<bool_ret_add>` | -> | `<bool_ret_mul>` `<add_tail>` |
| 595 | `<bool_ret_mul>` | -> | `<bool_ret_unary>` `<mul_tail>` |
| 596 | `<bool_ret_unary>` | -> | ! `<bool_ret_unary>` |
| 597 | `<bool_ret_unary>` | -> | `<bool_ret_postfix>` |
| 598 | `<bool_ret_postfix>` | -> | true |
| 599 | `<bool_ret_postfix>` | -> | false |
| 600 | `<bool_ret_postfix>` | -> | ++ id |
| 601 | `<bool_ret_postfix>` | -> | -- id |
| 602 | `<bool_ret_postfix>` | -> | id `<id_postfix>` |
| 603 | `<bool_ret_postfix>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 604 | `<bool_ret_postfix>` | -> | bool ( `<expression>` ) |
| 605 | `<using_cont>` | -> | , id `<using_cont>` |
| 606 | `<using_cont>` | -> | λ |
| 607 | `<local_dec_body>` | -> | int id `<int_local_tail>` |
| 608 | `<local_dec_body>` | -> | long id `<long_local_tail>` |
| 609 | `<local_dec_body>` | -> | float id `<float_local_tail>` |
| 610 | `<local_dec_body>` | -> | double id `<double_local_tail>` |
| 611 | `<local_dec_body>` | -> | char id `<char_local_tail>` |
| 612 | `<local_dec_body>` | -> | string id `<string_local_tail>` |
| 613 | `<local_dec_body>` | -> | bool id `<bool_local_tail>` |
| 614 | `<local_dec_body>` | -> | id id `<weave_local_tail>` |
| 615 | `<int_local_tail>` | -> | `<int_array_with_init>` ; |
| 616 | `<int_local_tail>` | -> | = intlit `<int_local_cont>` ; |
| 617 | `<int_local_cont>` | -> | , id = intlit `<int_local_cont>` |
| 618 | `<int_local_cont>` | -> | λ |
| 619 | `<long_local_tail>` | -> | `<long_array_with_init>` ; |
| 620 | `<long_local_tail>` | -> | = longlit `<long_local_cont>` ; |
| 621 | `<long_local_cont>` | -> | , id = longlit `<long_local_cont>` |
| 622 | `<long_local_cont>` | -> | λ |
| 623 | `<float_local_tail>` | -> | `<float_array_with_init>` ; |
| 624 | `<float_local_tail>` | -> | = floatlit `<float_local_cont>` ; |
| 625 | `<float_local_cont>` | -> | , id = floatlit `<float_local_cont>` |
| 626 | `<float_local_cont>` | -> | λ |
| 627 | `<double_local_tail>` | -> | `<double_array_with_init>` ; |
| 628 | `<double_local_tail>` | -> | = doublelit `<double_local_cont>` ; |
| 629 | `<double_local_cont>` | -> | , id = doublelit `<double_local_cont>` |
| 630 | `<double_local_cont>` | -> | λ |
| 631 | `<char_local_tail>` | -> | `<char_array_with_init>` ; |
| 632 | `<char_local_tail>` | -> | = charlit `<char_local_cont>` ; |
| 633 | `<char_local_cont>` | -> | , id = charlit `<char_local_cont>` |
| 634 | `<char_local_cont>` | -> | λ |
| 635 | `<string_local_tail>` | -> | `<string_array_with_init>` ; |
| 636 | `<string_local_tail>` | -> | = stringlit `<string_local_cont>` ; |
| 637 | `<string_local_cont>` | -> | , id = stringlit `<string_local_cont>` |
| 638 | `<string_local_cont>` | -> | λ |
| 639 | `<bool_local_tail>` | -> | `<bool_array_with_init>` ; |
| 640 | `<bool_local_tail>` | -> | = `<bool_lit>` `<bool_local_cont>` ; |
| 641 | `<bool_local_cont>` | -> | , id = `<bool_lit>` `<bool_local_cont>` |
| 642 | `<bool_local_cont>` | -> | λ |
| 643 | `<weave_local_tail>` | -> | = { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_inst_cont>` ; |
| 644 | `<weave_local_tail>` | -> | `<weave_array_with_init>` `<weave_arr_cont>` ; |
| 645 | `<statement_non_return>` | -> | `<effect_stmt>` ; |
| 646 | `<statement_non_return>` | -> | `<io_stmt>` |
| 647 | `<statement_non_return>` | -> | `<ctrl_struct>` |
| 648 | `<statement_non_return>` | -> | break ; |
| 649 | `<ctrl_stmt_list>` | -> | `<statement_non_return>` `<ctrl_stmt_list>` |
| 650 | `<ctrl_stmt_list>` | -> | λ |
| 651 | `<effect_stmt>` | -> | ++ id `<effect_pre_chain>` |
| 652 | `<effect_stmt>` | -> | -- id `<effect_pre_chain>` |
| 653 | `<effect_stmt>` | -> | id `<effect_id_cont>` |
| 654 | `<effect_pre_chain>` | -> | [ `<stmt_array_index>` ] `<effect_pre_arr_chain>` |
| 655 | `<effect_pre_chain>` | -> | . id `<effect_pre_chain>` |
| 656 | `<effect_pre_chain>` | -> | λ |
| 657 | `<effect_pre_arr_chain>` | -> | [ `<stmt_array_index>` ] |
| 658 | `<effect_pre_arr_chain>` | -> | . id `<effect_pre_chain>` |
| 659 | `<effect_pre_arr_chain>` | -> | λ |
| 660 | `<effect_id_cont>` | -> | `<assign_op>` `<stmt_assign_expr>` |
| 661 | `<effect_id_cont>` | -> | ++ |
| 662 | `<effect_id_cont>` | -> | -- |
| 663 | `<effect_id_cont>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 664 | `<effect_id_cont>` | -> | [ `<stmt_array_index>` ] `<effect_post_arr>` |
| 665 | `<effect_id_cont>` | -> | . id `<effect_post_member>` |
| 666 | `<effect_post_call>` | -> | . id `<effect_post_call_member>` |
| 667 | `<effect_post_call>` | -> | [ `<stmt_array_index>` ] `<effect_post_call_arr>` |
| 668 | `<effect_post_call>` | -> | λ |
| 669 | `<effect_post_call_member>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 670 | `<effect_post_call_member>` | -> | [ `<stmt_array_index>` ] `<effect_post_call_arr>` |
| 671 | `<effect_post_call_member>` | -> | . id `<effect_post_call_member>` |
| 672 | `<effect_post_call_member>` | -> | λ |
| 673 | `<effect_post_call_arr>` | -> | [ `<stmt_array_index>` ] `<effect_post_call_arr_cont>` |
| 674 | `<effect_post_call_arr>` | -> | `<effect_post_call_arr_cont>` |
| 675 | `<effect_post_call_arr_cont>` | -> | . id `<effect_post_call_member>` |
| 676 | `<effect_post_call_arr_cont>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 677 | `<effect_post_call_arr_cont>` | -> | λ |
| 678 | `<effect_post_arr>` | -> | [ `<stmt_array_index>` ] `<effect_post_arr_2d>` |
| 679 | `<effect_post_arr>` | -> | `<effect_arr_effect>` |
| 680 | `<effect_post_arr_2d>` | -> | `<effect_arr_effect>` |
| 681 | `<effect_arr_effect>` | -> | `<assign_op>` `<stmt_assign_expr>` |
| 682 | `<effect_arr_effect>` | -> | ++ |
| 683 | `<effect_arr_effect>` | -> | -- |
| 684 | `<effect_arr_effect>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 685 | `<effect_arr_effect>` | -> | . id `<effect_post_member>` |
| 686 | `<effect_post_member>` | -> | `<assign_op>` `<stmt_assign_expr>` |
| 687 | `<effect_post_member>` | -> | ++ |
| 688 | `<effect_post_member>` | -> | -- |
| 689 | `<effect_post_member>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 690 | `<effect_post_member>` | -> | [ `<stmt_array_index>` ] `<effect_post_arr>` |
| 691 | `<effect_post_member>` | -> | . id `<effect_post_member>` |
| 692 | `<stmt_assign_expr>` | -> | `<stmt_concat_expr>` `<stmt_assign_tail>` |
| 693 | `<stmt_assign_tail>` | -> | `<assign_op>` `<stmt_assign_expr>` |
| 694 | `<stmt_assign_tail>` | -> | λ |
| 695 | `<stmt_concat_expr>` | -> | `<stmt_or_expr>` `<stmt_concat_tail>` |
| 696 | `<stmt_concat_tail>` | -> | .. `<stmt_or_expr>` `<stmt_concat_tail>` |
| 697 | `<stmt_concat_tail>` | -> | λ |
| 698 | `<stmt_or_expr>` | -> | `<stmt_and_expr>` `<stmt_or_tail>` |
| 699 | `<stmt_or_tail>` | -> | \|\| `<stmt_and_expr>` `<stmt_or_tail>` |
| 700 | `<stmt_or_tail>` | -> | λ |
| 701 | `<stmt_and_expr>` | -> | `<stmt_eq_expr>` `<stmt_and_tail>` |
| 702 | `<stmt_and_tail>` | -> | && `<stmt_eq_expr>` `<stmt_and_tail>` |
| 703 | `<stmt_and_tail>` | -> | λ |
| 704 | `<stmt_eq_expr>` | -> | `<stmt_rel_expr>` `<stmt_eq_tail>` |
| 705 | `<stmt_eq_tail>` | -> | == `<stmt_rel_expr>` `<stmt_eq_tail>` |
| 706 | `<stmt_eq_tail>` | -> | != `<stmt_rel_expr>` `<stmt_eq_tail>` |
| 707 | `<stmt_eq_tail>` | -> | λ |
| 708 | `<stmt_rel_expr>` | -> | `<stmt_add_expr>` `<stmt_rel_tail>` |
| 709 | `<stmt_rel_tail>` | -> | `< <stmt_add_expr>` |
| 710 | `<stmt_rel_tail>` | -> | > `<stmt_add_expr>` |
| 711 | `<stmt_rel_tail>` | -> | `<= <stmt_add_expr>` |
| 712 | `<stmt_rel_tail>` | -> | >= `<stmt_add_expr>` |
| 713 | `<stmt_rel_tail>` | -> | λ |
| 714 | `<stmt_add_expr>` | -> | `<stmt_mul_expr>` `<stmt_add_tail>` |
| 715 | `<stmt_add_tail>` | -> | + `<stmt_mul_expr>` `<stmt_add_tail>` |
| 716 | `<stmt_add_tail>` | -> | - `<stmt_mul_expr>` `<stmt_add_tail>` |
| 717 | `<stmt_add_tail>` | -> | λ |
| 718 | `<stmt_mul_expr>` | -> | `<stmt_unary_expr>` `<stmt_mul_tail>` |
| 719 | `<stmt_mul_tail>` | -> | * `<stmt_unary_expr>` `<stmt_mul_tail>` |
| 720 | `<stmt_mul_tail>` | -> | / `<stmt_unary_expr>` `<stmt_mul_tail>` |
| 721 | `<stmt_mul_tail>` | -> | % `<stmt_unary_expr>` `<stmt_mul_tail>` |
| 722 | `<stmt_mul_tail>` | -> | λ |
| 723 | `<stmt_unary_expr>` | -> | ! `<stmt_unary_expr>` |
| 724 | `<stmt_unary_expr>` | -> | - `<stmt_unary_expr>` |
| 725 | `<stmt_unary_expr>` | -> | `<stmt_postfix_expr>` |
| 726 | `<stmt_postfix_expr>` | -> | ( `<arg_expr>` ) `<stmt_postfix_chain>` |
| 727 | `<stmt_postfix_expr>` | -> | int ( `<arg_expr>` ) |
| 728 | `<stmt_postfix_expr>` | -> | long ( `<arg_expr>` ) |
| 729 | `<stmt_postfix_expr>` | -> | float ( `<arg_expr>` ) |
| 730 | `<stmt_postfix_expr>` | -> | double ( `<arg_expr>` ) |
| 731 | `<stmt_postfix_expr>` | -> | char ( `<arg_expr>` ) |
| 732 | `<stmt_postfix_expr>` | -> | string ( `<arg_expr>` ) |
| 733 | `<stmt_postfix_expr>` | -> | bool ( `<arg_expr>` ) |
| 734 | `<stmt_postfix_expr>` | -> | ++ id |
| 735 | `<stmt_postfix_expr>` | -> | -- id |
| 736 | `<stmt_postfix_expr>` | -> | id `<stmt_id_postfix>` |
| 737 | `<stmt_postfix_expr>` | -> | intlit |
| 738 | `<stmt_postfix_expr>` | -> | longlit |
| 739 | `<stmt_postfix_expr>` | -> | floatlit |
| 740 | `<stmt_postfix_expr>` | -> | doublelit |
| 741 | `<stmt_postfix_expr>` | -> | charlit |
| 742 | `<stmt_postfix_expr>` | -> | stringlit |
| 743 | `<stmt_postfix_expr>` | -> | true |
| 744 | `<stmt_postfix_expr>` | -> | false |
| 745 | `<stmt_id_postfix>` | -> | ++ |
| 746 | `<stmt_id_postfix>` | -> | -- |
| 747 | `<stmt_id_postfix>` | -> | `<stmt_postfix_chain>` |
| 748 | `<stmt_postfix_chain>` | -> | `<stmt_array_access>` `<stmt_postfix_after_arr>` |
| 749 | `<stmt_postfix_chain>` | -> | . id `<stmt_postfix_chain>` |
| 750 | `<stmt_postfix_chain>` | -> | ( `<stmt_arg_list>` ) `<stmt_postfix_chain>` |
| 751 | `<stmt_postfix_chain>` | -> | λ |
| 752 | `<stmt_array_access>` | -> | [ `<stmt_array_index>` ] `<stmt_array_access_dim2>` |
| 753 | `<stmt_array_access_dim2>` | -> | [ `<stmt_array_index>` ] |
| 754 | `<stmt_array_access_dim2>` | -> | λ |
| 755 | `<stmt_postfix_after_arr>` | -> | . id `<stmt_postfix_chain>` |
| 756 | `<stmt_postfix_after_arr>` | -> | ( `<stmt_arg_list>` ) `<stmt_postfix_chain>` |
| 757 | `<stmt_postfix_after_arr>` | -> | λ |
| 758 | `<stmt_array_index>` | -> | intlit |
| 759 | `<stmt_array_index>` | -> | id |
| 760 | `<stmt_arg_list>` | -> | `<arg_expr>` `<stmt_arg_tail>` |
| 761 | `<stmt_arg_list>` | -> | λ |
| 762 | `<stmt_arg_tail>` | -> | , `<arg_expr>` `<stmt_arg_tail>` |
| 763 | `<stmt_arg_tail>` | -> | λ |
| 764 | `<arg_expr>` | -> | `<arg_assign_expr>` |
| 765 | `<arg_assign_expr>` | -> | `<arg_concat_expr>` `<arg_assign_tail>` |
| 766 | `<arg_assign_tail>` | -> | `<assign_op>` `<arg_assign_expr>` |
| 767 | `<arg_assign_tail>` | -> | λ |
| 768 | `<arg_concat_expr>` | -> | `<arg_or_expr>` `<arg_concat_tail>` |
| 769 | `<arg_concat_tail>` | -> | .. `<arg_or_expr>` `<arg_concat_tail>` |
| 770 | `<arg_concat_tail>` | -> | λ |
| 771 | `<arg_or_expr>` | -> | `<arg_and_expr>` `<arg_or_tail>` |
| 772 | `<arg_or_tail>` | -> | \|\| `<arg_and_expr>` `<arg_or_tail>` |
| 773 | `<arg_or_tail>` | -> | λ |
| 774 | `<arg_and_expr>` | -> | `<arg_eq_expr>` `<arg_and_tail>` |
| 775 | `<arg_and_tail>` | -> | && `<arg_eq_expr>` `<arg_and_tail>` |
| 776 | `<arg_and_tail>` | -> | λ |
| 777 | `<arg_eq_expr>` | -> | `<arg_rel_expr>` `<arg_eq_tail>` |
| 778 | `<arg_eq_tail>` | -> | == `<arg_rel_expr>` `<arg_eq_tail>` |
| 779 | `<arg_eq_tail>` | -> | != `<arg_rel_expr>` `<arg_eq_tail>` |
| 780 | `<arg_eq_tail>` | -> | λ |
| 781 | `<arg_rel_expr>` | -> | `<arg_add_expr>` `<arg_rel_tail>` |
| 782 | `<arg_rel_tail>` | -> | `< <arg_add_expr>` |
| 783 | `<arg_rel_tail>` | -> | > `<arg_add_expr>` |
| 784 | `<arg_rel_tail>` | -> | `<= <arg_add_expr>` |
| 785 | `<arg_rel_tail>` | -> | >= `<arg_add_expr>` |
| 786 | `<arg_rel_tail>` | -> | λ |
| 787 | `<arg_add_expr>` | -> | `<arg_mul_expr>` `<arg_add_tail>` |
| 788 | `<arg_add_tail>` | -> | + `<arg_mul_expr>` `<arg_add_tail>` |
| 789 | `<arg_add_tail>` | -> | - `<arg_mul_expr>` `<arg_add_tail>` |
| 790 | `<arg_add_tail>` | -> | λ |
| 791 | `<arg_mul_expr>` | -> | `<arg_unary_expr>` `<arg_mul_tail>` |
| 792 | `<arg_mul_tail>` | -> | * `<arg_unary_expr>` `<arg_mul_tail>` |
| 793 | `<arg_mul_tail>` | -> | / `<arg_unary_expr>` `<arg_mul_tail>` |
| 794 | `<arg_mul_tail>` | -> | % `<arg_unary_expr>` `<arg_mul_tail>` |
| 795 | `<arg_mul_tail>` | -> | λ |
| 796 | `<arg_unary_expr>` | -> | ! `<arg_unary_expr>` |
| 797 | `<arg_unary_expr>` | -> | - `<arg_unary_expr>` |
| 798 | `<arg_unary_expr>` | -> | `<arg_postfix_expr>` |
| 799 | `<arg_postfix_expr>` | -> | ( `<arg_expr>` ) `<arg_postfix_chain>` |
| 800 | `<arg_postfix_expr>` | -> | int ( `<arg_expr>` ) |
| 801 | `<arg_postfix_expr>` | -> | long ( `<arg_expr>` ) |
| 802 | `<arg_postfix_expr>` | -> | float ( `<arg_expr>` ) |
| 803 | `<arg_postfix_expr>` | -> | double ( `<arg_expr>` ) |
| 804 | `<arg_postfix_expr>` | -> | char ( `<arg_expr>` ) |
| 805 | `<arg_postfix_expr>` | -> | string ( `<arg_expr>` ) |
| 806 | `<arg_postfix_expr>` | -> | bool ( `<arg_expr>` ) |
| 807 | `<arg_postfix_expr>` | -> | ++ id |
| 808 | `<arg_postfix_expr>` | -> | -- id |
| 809 | `<arg_postfix_expr>` | -> | id `<arg_id_postfix>` |
| 810 | `<arg_postfix_expr>` | -> | intlit |
| 811 | `<arg_postfix_expr>` | -> | longlit |
| 812 | `<arg_postfix_expr>` | -> | floatlit |
| 813 | `<arg_postfix_expr>` | -> | doublelit |
| 814 | `<arg_postfix_expr>` | -> | charlit |
| 815 | `<arg_postfix_expr>` | -> | stringlit |
| 816 | `<arg_postfix_expr>` | -> | true |
| 817 | `<arg_postfix_expr>` | -> | false |
| 818 | `<arg_id_postfix>` | -> | ++ |
| 819 | `<arg_id_postfix>` | -> | -- |
| 820 | `<arg_id_postfix>` | -> | `<arg_postfix_chain>` |
| 821 | `<arg_postfix_chain>` | -> | `<arg_array_access>` `<arg_postfix_after_arr>` |
| 822 | `<arg_postfix_chain>` | -> | . id `<arg_postfix_chain>` |
| 823 | `<arg_postfix_chain>` | -> | ( `<arg_nested_list>` ) `<arg_postfix_chain>` |
| 824 | `<arg_postfix_chain>` | -> | λ |
| 825 | `<arg_array_access>` | -> | [ `<arg_array_index>` ] `<arg_array_access_dim2>` |
| 826 | `<arg_array_access_dim2>` | -> | [ `<arg_array_index>` ] |
| 827 | `<arg_array_access_dim2>` | -> | λ |
| 828 | `<arg_postfix_after_arr>` | -> | . id `<arg_postfix_chain>` |
| 829 | `<arg_postfix_after_arr>` | -> | ( `<arg_nested_list>` ) `<arg_postfix_chain>` |
| 830 | `<arg_postfix_after_arr>` | -> | λ |
| 831 | `<arg_array_index>` | -> | intlit |
| 832 | `<arg_array_index>` | -> | id |
| 833 | `<arg_nested_list>` | -> | `<arg_expr>` `<arg_nested_tail>` |
| 834 | `<arg_nested_list>` | -> | λ |
| 835 | `<arg_nested_tail>` | -> | , `<arg_expr>` `<arg_nested_tail>` |
| 836 | `<arg_nested_tail>` | -> | λ |
| 837 | `<expression>` | -> | `<assign_expr>` |
| 838 | `<assign_expr>` | -> | `<concat_expr>` `<assign_tail>` |
| 839 | `<assign_tail>` | -> | `<assign_op>` `<assign_expr>` |
| 840 | `<assign_tail>` | -> | λ |
| 841 | `<assign_op>` | -> | = |
| 842 | `<assign_op>` | -> | += |
| 843 | `<assign_op>` | -> | -= |
| 844 | `<assign_op>` | -> | *= |
| 845 | `<assign_op>` | -> | /= |
| 846 | `<assign_op>` | -> | %= |
| 847 | `<concat_expr>` | -> | `<or_expr>` `<concat_tail>` |
| 848 | `<concat_tail>` | -> | .. `<or_expr>` `<concat_tail>` |
| 849 | `<concat_tail>` | -> | λ |
| 850 | `<or_expr>` | -> | `<and_expr>` `<or_tail>` |
| 851 | `<or_tail>` | -> | \|\| `<and_expr>` `<or_tail>` |
| 852 | `<or_tail>` | -> | λ |
| 853 | `<and_expr>` | -> | `<eq_expr>` `<and_tail>` |
| 854 | `<and_tail>` | -> | && `<eq_expr>` `<and_tail>` |
| 855 | `<and_tail>` | -> | λ |
| 856 | `<eq_expr>` | -> | `<rel_expr>` `<eq_tail>` |
| 857 | `<eq_tail>` | -> | == `<rel_expr>` `<eq_tail>` |
| 858 | `<eq_tail>` | -> | != `<rel_expr>` `<eq_tail>` |
| 859 | `<eq_tail>` | -> | λ |
| 860 | `<rel_expr>` | -> | `<add_expr>` `<rel_tail>` |
| 861 | `<rel_tail>` | -> | `< <add_expr>` |
| 862 | `<rel_tail>` | -> | > `<add_expr>` |
| 863 | `<rel_tail>` | -> | `<= <add_expr>` |
| 864 | `<rel_tail>` | -> | >= `<add_expr>` |
| 865 | `<rel_tail>` | -> | λ |
| 866 | `<add_expr>` | -> | `<mul_expr>` `<add_tail>` |
| 867 | `<add_tail>` | -> | + `<mul_expr>` `<add_tail>` |
| 868 | `<add_tail>` | -> | - `<mul_expr>` `<add_tail>` |
| 869 | `<add_tail>` | -> | λ |
| 870 | `<mul_expr>` | -> | `<unary_expr>` `<mul_tail>` |
| 871 | `<mul_tail>` | -> | * `<unary_expr>` `<mul_tail>` |
| 872 | `<mul_tail>` | -> | / `<unary_expr>` `<mul_tail>` |
| 873 | `<mul_tail>` | -> | % `<unary_expr>` `<mul_tail>` |
| 874 | `<mul_tail>` | -> | λ |
| 875 | `<unary_expr>` | -> | ! `<unary_expr>` |
| 876 | `<unary_expr>` | -> | `<postfix_expr>` |
| 877 | `<postfix_expr>` | -> | ( `<expression>` ) `<postfix_chain>` |
| 878 | `<postfix_expr>` | -> | int ( `<expression>` ) |
| 879 | `<postfix_expr>` | -> | long ( `<expression>` ) |
| 880 | `<postfix_expr>` | -> | float ( `<expression>` ) |
| 881 | `<postfix_expr>` | -> | double ( `<expression>` ) |
| 882 | `<postfix_expr>` | -> | char ( `<expression>` ) |
| 883 | `<postfix_expr>` | -> | string ( `<expression>` ) |
| 884 | `<postfix_expr>` | -> | bool ( `<expression>` ) |
| 885 | `<postfix_expr>` | -> | ++ id |
| 886 | `<postfix_expr>` | -> | -- id |
| 887 | `<postfix_expr>` | -> | id `<id_postfix>` |
| 888 | `<postfix_expr>` | -> | intlit |
| 889 | `<postfix_expr>` | -> | longlit |
| 890 | `<postfix_expr>` | -> | floatlit |
| 891 | `<postfix_expr>` | -> | doublelit |
| 892 | `<postfix_expr>` | -> | charlit |
| 893 | `<postfix_expr>` | -> | stringlit |
| 894 | `<postfix_expr>` | -> | true |
| 895 | `<postfix_expr>` | -> | false |
| 896 | `<id_postfix>` | -> | ++ |
| 897 | `<id_postfix>` | -> | -- |
| 898 | `<id_postfix>` | -> | `<postfix_chain>` |
| 899 | `<postfix_chain>` | -> | `<array_access>` `<postfix_after_arr>` |
| 900 | `<postfix_chain>` | -> | . id `<postfix_chain>` |
| 901 | `<postfix_chain>` | -> | ( `<arg_list>` ) `<postfix_chain>` |
| 902 | `<postfix_chain>` | -> | λ |
| 903 | `<array_access>` | -> | [ `<array_index>` ] `<array_access_dim2>` |
| 904 | `<array_access_dim2>` | -> | [ `<array_index>` ] |
| 905 | `<array_access_dim2>` | -> | λ |
| 906 | `<postfix_after_arr>` | -> | . id `<postfix_chain>` |
| 907 | `<postfix_after_arr>` | -> | ( `<arg_list>` ) `<postfix_chain>` |
| 908 | `<postfix_after_arr>` | -> | λ |
| 909 | `<array_index>` | -> | intlit |
| 910 | `<array_index>` | -> | id |
| 911 | `<arg_list>` | -> | `<arg_expr>` `<arg_tail>` |
| 912 | `<arg_list>` | -> | λ |
| 913 | `<arg_tail>` | -> | , `<arg_expr>` `<arg_tail>` |
| 914 | `<arg_tail>` | -> | λ |
| 915 | `<io_stmt>` | -> | trap ( `<arg_expr>` ) ; |
| 916 | `<io_stmt>` | -> | thread ( `<print_args>` ) ; |
| 917 | `<io_stmt>` | -> | threadln ( `<print_args>` ) ; |
| 918 | `<print_args>` | -> | `<arg_expr>` `<print_tail>` |
| 919 | `<print_tail>` | -> | , `<arg_expr>` `<print_tail>` |
| 920 | `<print_tail>` | -> | λ |
| 921 | `<ctrl_struct>` | -> | if ( `<condition>` ) { `<ctrl_stmt_list>` } `<else_opt>` |
| 922 | `<ctrl_struct>` | -> | switch ( `<arg_expr>` ) { `<case_list>` `<default_opt>` } |
| 923 | `<ctrl_struct>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<ctrl_stmt_list>` } |
| 924 | `<ctrl_struct>` | -> | while ( `<condition>` ) { `<ctrl_stmt_list>` } |
| 925 | `<ctrl_struct>` | -> | do { `<ctrl_stmt_list>` } while ( `<condition>` ) ; |
| 926 | `<else_opt>` | -> | else `<else_body>` |
| 927 | `<else_opt>` | -> | λ |
| 928 | `<else_body>` | -> | { `<ctrl_stmt_list>` } |
| 929 | `<else_body>` | -> | if ( `<condition>` ) { `<ctrl_stmt_list>` } `<else_opt>` |
| 930 | `<case_list>` | -> | case `<case_val>` : `<ctrl_stmt_list>` `<break_opt>` `<case_list>` |
| 931 | `<case_list>` | -> | λ |
| 932 | `<case_val>` | -> | intlit |
| 933 | `<case_val>` | -> | longlit |
| 934 | `<case_val>` | -> | charlit |
| 935 | `<case_val>` | -> | true |
| 936 | `<case_val>` | -> | false |
| 937 | `<default_opt>` | -> | default : `<ctrl_stmt_list>` `<break_opt>` |
| 938 | `<default_opt>` | -> | λ |
| 939 | `<break_opt>` | -> | break ; |
| 940 | `<break_opt>` | -> | λ |
| 941 | `<for_init>` | -> | local var `<for_init_type>` id = `<for_init_expr>` |
| 942 | `<for_init>` | -> | id `<for_init_assign_tail>` |
| 943 | `<for_init>` | -> | λ |
| 944 | `<for_init_assign_tail>` | -> | `<assign_op>` `<for_init_expr>` |
| 945 | `<for_init_expr>` | -> | `<stmt_concat_expr>` |
| 946 | `<for_init_type>` | -> | int |
| 947 | `<for_init_type>` | -> | long |
| 948 | `<for_init_type>` | -> | float |
| 949 | `<for_init_type>` | -> | double |
| 950 | `<for_init_type>` | -> | char |
| 951 | `<for_init_type>` | -> | string |
| 952 | `<for_init_type>` | -> | bool |
| 953 | `<for_cond>` | -> | `<condition>` |
| 954 | `<for_update>` | -> | id `<for_update_tail>` |
| 955 | `<for_update>` | -> | ++ id |
| 956 | `<for_update>` | -> | -- id |
| 957 | `<for_update>` | -> | λ |
| 958 | `<for_update_tail>` | -> | ++ |
| 959 | `<for_update_tail>` | -> | -- |
| 960 | `<for_update_tail>` | -> | `<assign_op>` `<arg_expr>` |
| 961 | `<condition>` | -> | `<cond_or>` |
| 962 | `<cond_or>` | -> | `<cond_and>` `<cond_or_tail>` |
| 963 | `<cond_or_tail>` | -> | \|\| `<cond_and>` `<cond_or_tail>` |
| 964 | `<cond_or_tail>` | -> | λ |
| 965 | `<cond_and>` | -> | `<cond_comparison>` `<cond_and_tail>` |
| 966 | `<cond_and_tail>` | -> | && `<cond_comparison>` `<cond_and_tail>` |
| 967 | `<cond_and_tail>` | -> | λ |
| 968 | `<cond_comparison>` | -> | ( `<condition>` ) |
| 969 | `<cond_comparison>` | -> | ! `<cond_comparison>` |
| 970 | `<cond_comparison>` | -> | `<cond_primary>` `<cond_primary_continue>` |
| 971 | `<cond_primary>` | -> | - `<cond_primary>` |
| 972 | `<cond_primary>` | -> | `<cond_postfix>` |
| 973 | `<cond_primary_continue>` | -> | + `<cond_primary>` `<cond_must_commit>` |
| 974 | `<cond_primary_continue>` | -> | - `<cond_primary>` `<cond_must_commit>` |
| 975 | `<cond_primary_continue>` | -> | * `<cond_primary>` `<cond_must_commit>` |
| 976 | `<cond_primary_continue>` | -> | / `<cond_primary>` `<cond_must_commit>` |
| 977 | `<cond_primary_continue>` | -> | % `<cond_primary>` `<cond_must_commit>` |
| 978 | `<cond_primary_continue>` | -> | `<comp_op>` `<cond_rhs>` |
| 979 | `<cond_primary_continue>` | -> | λ |
| 980 | `<cond_must_commit>` | -> | + `<cond_primary>` `<cond_must_commit>` |
| 981 | `<cond_must_commit>` | -> | - `<cond_primary>` `<cond_must_commit>` |
| 982 | `<cond_must_commit>` | -> | * `<cond_primary>` `<cond_must_commit>` |
| 983 | `<cond_must_commit>` | -> | / `<cond_primary>` `<cond_must_commit>` |
| 984 | `<cond_must_commit>` | -> | % `<cond_primary>` `<cond_must_commit>` |
| 985 | `<cond_must_commit>` | -> | `<comp_op>` `<cond_rhs>` |
| 986 | `<cond_postfix>` | -> | int ( `<cond_cast_arg>` ) |
| 987 | `<cond_postfix>` | -> | long ( `<cond_cast_arg>` ) |
| 988 | `<cond_postfix>` | -> | float ( `<cond_cast_arg>` ) |
| 989 | `<cond_postfix>` | -> | double ( `<cond_cast_arg>` ) |
| 990 | `<cond_postfix>` | -> | char ( `<cond_cast_arg>` ) |
| 991 | `<cond_postfix>` | -> | string ( `<cond_cast_arg>` ) |
| 992 | `<cond_postfix>` | -> | bool ( `<cond_cast_arg>` ) |
| 993 | `<cond_postfix>` | -> | ++ id |
| 994 | `<cond_postfix>` | -> | -- id |
| 995 | `<cond_postfix>` | -> | id `<cond_id_post>` |
| 996 | `<cond_postfix>` | -> | intlit |
| 997 | `<cond_postfix>` | -> | longlit |
| 998 | `<cond_postfix>` | -> | floatlit |
| 999 | `<cond_postfix>` | -> | doublelit |
| 1000 | `<cond_postfix>` | -> | charlit |
| 1001 | `<cond_postfix>` | -> | stringlit |
| 1002 | `<cond_postfix>` | -> | true |
| 1003 | `<cond_postfix>` | -> | false |
| 1004 | `<cond_cast_arg>` | -> | `<arg_expr>` |
| 1005 | `<cond_id_post>` | -> | ++ |
| 1006 | `<cond_id_post>` | -> | -- |
| 1007 | `<cond_id_post>` | -> | `<cond_post_chain>` |
| 1008 | `<cond_post_chain>` | -> | `<cond_arr_access>` `<cond_post_after_arr>` |
| 1009 | `<cond_post_chain>` | -> | . id `<cond_post_chain>` |
| 1010 | `<cond_post_chain>` | -> | ( `<arg_list>` ) `<cond_post_chain>` |
| 1011 | `<cond_post_chain>` | -> | λ |
| 1012 | `<cond_arr_access>` | -> | [ `<cond_arr_index>` ] `<cond_arr_access_dim2>` |
| 1013 | `<cond_arr_access_dim2>` | -> | [ `<cond_arr_index>` ] |
| 1014 | `<cond_arr_access_dim2>` | -> | λ |
| 1015 | `<cond_post_after_arr>` | -> | . id `<cond_post_chain>` |
| 1016 | `<cond_post_after_arr>` | -> | ( `<arg_list>` ) `<cond_post_chain>` |
| 1017 | `<cond_post_after_arr>` | -> | λ |
| 1018 | `<cond_arr_index>` | -> | intlit |
| 1019 | `<cond_arr_index>` | -> | id |
| 1020 | `<cond_rhs>` | -> | `<arg_add_expr>` |
| 1021 | `<comp_op>` | -> | == |
| 1022 | `<comp_op>` | -> | != |
| 1023 | `<comp_op>` | -> | < |
| 1024 | `<comp_op>` | -> | > |
| 1025 | `<comp_op>` | -> | <= |
| 1026 | `<comp_op>` | -> | >= |
| 1027 | `<main_body>` | -> | `<main_content>` |
| 1028 | `<main_content>` | -> | using id `<using_cont>` ; `<main_content>` |
| 1029 | `<main_content>` | -> | local `<mutability>` `<local_dec_body>` `<main_content>` |
| 1030 | `<main_content>` | -> | `<statement_non_return>` `<main_content>` |
| 1031 | `<main_content>` | -> | return intlit ; |