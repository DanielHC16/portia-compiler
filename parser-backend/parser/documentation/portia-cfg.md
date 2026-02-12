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
| 238 | `<func_content_int>` | -> | `<statement_int_no_ret>` `<func_content_int>` |
| 239 | `<func_content_int>` | -> | `<mandatory_int_return>` |
| 240 | `<mandatory_int_return>` | -> | return `<typed_numeric_ret_expr>` ; |
| 241 | `<function_body_long>` | -> | `<func_content_long>` |
| 242 | `<func_content_long>` | -> | using id `<using_cont>` ; `<func_content_long>` |
| 243 | `<func_content_long>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_long>` |
| 244 | `<func_content_long>` | -> | `<statement_long_no_ret>` `<func_content_long>` |
| 245 | `<func_content_long>` | -> | `<mandatory_long_return>` |
| 246 | `<mandatory_long_return>` | -> | return `<typed_numeric_ret_expr>` ; |
| 247 | `<function_body_float>` | -> | `<func_content_float>` |
| 248 | `<func_content_float>` | -> | using id `<using_cont>` ; `<func_content_float>` |
| 249 | `<func_content_float>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_float>` |
| 250 | `<func_content_float>` | -> | `<statement_float_no_ret>` `<func_content_float>` |
| 251 | `<func_content_float>` | -> | `<mandatory_float_return>` |
| 252 | `<mandatory_float_return>` | -> | return `<typed_numeric_ret_expr>` ; |
| 253 | `<function_body_double>` | -> | `<func_content_double>` |
| 254 | `<func_content_double>` | -> | using id `<using_cont>` ; `<func_content_double>` |
| 255 | `<func_content_double>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_double>` |
| 256 | `<func_content_double>` | -> | `<statement_double_no_ret>` `<func_content_double>` |
| 257 | `<func_content_double>` | -> | `<mandatory_double_return>` |
| 258 | `<mandatory_double_return>` | -> | return `<typed_numeric_ret_expr>` ; |
| 259 | `<function_body_char>` | -> | `<func_content_char>` |
| 260 | `<func_content_char>` | -> | using id `<using_cont>` ; `<func_content_char>` |
| 261 | `<func_content_char>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_char>` |
| 262 | `<func_content_char>` | -> | `<statement_char_no_ret>` `<func_content_char>` |
| 263 | `<func_content_char>` | -> | `<mandatory_char_return>` |
| 264 | `<mandatory_char_return>` | -> | return `<typed_string_ret_expr>` ; |
| 265 | `<function_body_string>` | -> | `<func_content_string>` |
| 266 | `<func_content_string>` | -> | using id `<using_cont>` ; `<func_content_string>` |
| 267 | `<func_content_string>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_string>` |
| 268 | `<func_content_string>` | -> | `<statement_string_no_ret>` `<func_content_string>` |
| 269 | `<func_content_string>` | -> | `<mandatory_string_return>` |
| 270 | `<mandatory_string_return>` | -> | return `<typed_string_ret_expr>` ; |
| 271 | `<function_body_bool>` | -> | `<func_content_bool>` |
| 272 | `<func_content_bool>` | -> | using id `<using_cont>` ; `<func_content_bool>` |
| 273 | `<func_content_bool>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_bool>` |
| 274 | `<func_content_bool>` | -> | `<statement_bool_no_ret>` `<func_content_bool>` |
| 275 | `<func_content_bool>` | -> | `<mandatory_bool_return>` |
| 276 | `<mandatory_bool_return>` | -> | return `<typed_bool_ret_expr>` ; |
| 277 | `<function_body_array>` | -> | `<func_content_array>` |
| 278 | `<func_content_array>` | -> | using id `<using_cont>` ; `<func_content_array>` |
| 279 | `<func_content_array>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_array>` |
| 280 | `<func_content_array>` | -> | `<statement_array_no_ret>` `<func_content_array>` |
| 281 | `<func_content_array>` | -> | `<mandatory_array_return>` |
| 282 | `<mandatory_array_return>` | -> | return id ; |
| 283 | `<function_body_weave>` | -> | `<func_content_weave>` |
| 284 | `<func_content_weave>` | -> | using id `<using_cont>` ; `<func_content_weave>` |
| 285 | `<func_content_weave>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_weave>` |
| 286 | `<func_content_weave>` | -> | `<statement_weave_no_ret>` `<func_content_weave>` |
| 287 | `<func_content_weave>` | -> | `<mandatory_weave_return>` |
| 288 | `<mandatory_weave_return>` | -> | return id ; |
| 289 | `<function_body_void>` | -> | `<func_content_void>` |
| 290 | `<func_content_void>` | -> | using id `<using_cont>` ; `<func_content_void>` |
| 291 | `<func_content_void>` | -> | local `<mutability>` `<local_dec_body>` `<func_content_void>` |
| 292 | `<func_content_void>` | -> | `<statement_void_no_ret>` `<func_content_void>` |
| 293 | `<func_content_void>` | -> | `<mandatory_void_return>` |
| 294 | `<mandatory_void_return>` | -> | return ; |
| 295 | `<statement_int>` | -> | `<effect_stmt>` ; |
| 296 | `<statement_int>` | -> | `<io_stmt>` |
| 297 | `<statement_int>` | -> | `<ctrl_struct_int>` |
| 298 | `<statement_int>` | -> | return `<typed_numeric_ret_expr>` ; |
| 299 | `<statement_long>` | -> | `<effect_stmt>` ; |
| 300 | `<statement_long>` | -> | `<io_stmt>` |
| 301 | `<statement_long>` | -> | `<ctrl_struct_long>` |
| 302 | `<statement_long>` | -> | return `<typed_numeric_ret_expr>` ; |
| 303 | `<statement_float>` | -> | `<effect_stmt>` ; |
| 304 | `<statement_float>` | -> | `<io_stmt>` |
| 305 | `<statement_float>` | -> | `<ctrl_struct_float>` |
| 306 | `<statement_float>` | -> | return `<typed_numeric_ret_expr>` ; |
| 307 | `<statement_double>` | -> | `<effect_stmt>` ; |
| 308 | `<statement_double>` | -> | `<io_stmt>` |
| 309 | `<statement_double>` | -> | `<ctrl_struct_double>` |
| 310 | `<statement_double>` | -> | return `<typed_numeric_ret_expr>` ; |
| 311 | `<statement_char>` | -> | `<effect_stmt>` ; |
| 312 | `<statement_char>` | -> | `<io_stmt>` |
| 313 | `<statement_char>` | -> | `<ctrl_struct_char>` |
| 314 | `<statement_char>` | -> | return `<typed_string_ret_expr>` ; |
| 315 | `<statement_string>` | -> | `<effect_stmt>` ; |
| 316 | `<statement_string>` | -> | `<io_stmt>` |
| 317 | `<statement_string>` | -> | `<ctrl_struct_string>` |
| 318 | `<statement_string>` | -> | return `<typed_string_ret_expr>` ; |
| 319 | `<statement_bool>` | -> | `<effect_stmt>` ; |
| 320 | `<statement_bool>` | -> | `<io_stmt>` |
| 321 | `<statement_bool>` | -> | `<ctrl_struct_bool>` |
| 322 | `<statement_bool>` | -> | return `<typed_bool_ret_expr>` ; |
| 323 | `<statement_array>` | -> | `<effect_stmt>` ; |
| 324 | `<statement_array>` | -> | `<io_stmt>` |
| 325 | `<statement_array>` | -> | `<ctrl_struct_array>` |
| 326 | `<statement_array>` | -> | return id ; |
| 327 | `<statement_weave>` | -> | `<effect_stmt>` ; |
| 328 | `<statement_weave>` | -> | `<io_stmt>` |
| 329 | `<statement_weave>` | -> | `<ctrl_struct_weave>` |
| 330 | `<statement_weave>` | -> | return id ; |
| 331 | `<statement_void>` | -> | `<effect_stmt>` ; |
| 332 | `<statement_void>` | -> | `<io_stmt>` |
| 333 | `<statement_void>` | -> | `<ctrl_struct_void>` |
| 334 | `<statement_void>` | -> | return ; |
| 335 | `<statement_int_no_ret>` | -> | `<effect_stmt>` ; |
| 336 | `<statement_int_no_ret>` | -> | `<io_stmt>` |
| 337 | `<statement_int_no_ret>` | -> | `<ctrl_struct_int>` |
| 338 | `<statement_long_no_ret>` | -> | `<effect_stmt>` ; |
| 339 | `<statement_long_no_ret>` | -> | `<io_stmt>` |
| 340 | `<statement_long_no_ret>` | -> | `<ctrl_struct_long>` |
| 341 | `<statement_float_no_ret>` | -> | `<effect_stmt>` ; |
| 342 | `<statement_float_no_ret>` | -> | `<io_stmt>` |
| 343 | `<statement_float_no_ret>` | -> | `<ctrl_struct_float>` |
| 344 | `<statement_double_no_ret>` | -> | `<effect_stmt>` ; |
| 345 | `<statement_double_no_ret>` | -> | `<io_stmt>` |
| 346 | `<statement_double_no_ret>` | -> | `<ctrl_struct_double>` |
| 347 | `<statement_char_no_ret>` | -> | `<effect_stmt>` ; |
| 348 | `<statement_char_no_ret>` | -> | `<io_stmt>` |
| 349 | `<statement_char_no_ret>` | -> | `<ctrl_struct_char>` |
| 350 | `<statement_string_no_ret>` | -> | `<effect_stmt>` ; |
| 351 | `<statement_string_no_ret>` | -> | `<io_stmt>` |
| 352 | `<statement_string_no_ret>` | -> | `<ctrl_struct_string>` |
| 353 | `<statement_bool_no_ret>` | -> | `<effect_stmt>` ; |
| 354 | `<statement_bool_no_ret>` | -> | `<io_stmt>` |
| 355 | `<statement_bool_no_ret>` | -> | `<ctrl_struct_bool>` |
| 356 | `<statement_array_no_ret>` | -> | `<effect_stmt>` ; |
| 357 | `<statement_array_no_ret>` | -> | `<io_stmt>` |
| 358 | `<statement_array_no_ret>` | -> | `<ctrl_struct_array>` |
| 359 | `<statement_weave_no_ret>` | -> | `<effect_stmt>` ; |
| 360 | `<statement_weave_no_ret>` | -> | `<io_stmt>` |
| 361 | `<statement_weave_no_ret>` | -> | `<ctrl_struct_weave>` |
| 362 | `<statement_void_no_ret>` | -> | `<effect_stmt>` ; |
| 363 | `<statement_void_no_ret>` | -> | `<io_stmt>` |
| 364 | `<statement_void_no_ret>` | -> | `<ctrl_struct_void>` |
| 365 | `<ctrl_struct_int>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_int>` } `<else_opt_int>` |
| 366 | `<ctrl_struct_int>` | -> | switch ( `<arg_expr>` ) { `<case_list_int>` `<default_opt_int>` } |
| 367 | `<ctrl_struct_int>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_int>` } |
| 368 | `<ctrl_struct_int>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_int>` } |
| 369 | `<ctrl_struct_int>` | -> | do { `<non_empty_loop_stmt_list_int>` } while ( `<condition>` ) ; |
| 370 | `<stmt_list_int>` | -> | `<statement_int>` `<stmt_list_int>` |
| 371 | `<stmt_list_int>` | -> | λ |
| 372 | `<non_empty_stmt_list_int>` | -> | `<statement_int>` `<stmt_list_int>` |
| 373 | `<loop_statement_int>` | -> | `<statement_int>` |
| 374 | `<loop_statement_int>` | -> | break ; |
| 375 | `<loop_stmt_list_int>` | -> | `<loop_statement_int>` `<loop_stmt_list_int>` |
| 376 | `<loop_stmt_list_int>` | -> | λ |
| 377 | `<non_empty_loop_stmt_list_int>` | -> | `<loop_statement_int>` `<loop_stmt_list_int>` |
| 378 | `<else_opt_int>` | -> | else `<else_body_int>` |
| 379 | `<else_opt_int>` | -> | λ |
| 380 | `<else_body_int>` | -> | { `<non_empty_stmt_list_int>` } |
| 381 | `<else_body_int>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_int>` } `<else_opt_int>` |
| 382 | `<case_list_int>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_int>` `<break_opt>` `<case_list_int>` |
| 383 | `<case_list_int>` | -> | λ |
| 384 | `<default_opt_int>` | -> | default : `<non_empty_loop_stmt_list_int>` `<break_opt>` |
| 385 | `<default_opt_int>` | -> | λ |
| 386 | `<ctrl_struct_long>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_long>` } `<else_opt_long>` |
| 387 | `<ctrl_struct_long>` | -> | switch ( `<arg_expr>` ) { `<case_list_long>` `<default_opt_long>` } |
| 388 | `<ctrl_struct_long>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_long>` } |
| 389 | `<ctrl_struct_long>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_long>` } |
| 390 | `<ctrl_struct_long>` | -> | do { `<non_empty_loop_stmt_list_long>` } while ( `<condition>` ) ; |
| 391 | `<stmt_list_long>` | -> | `<statement_long>` `<stmt_list_long>` |
| 392 | `<stmt_list_long>` | -> | λ |
| 393 | `<non_empty_stmt_list_long>` | -> | `<statement_long>` `<stmt_list_long>` |
| 394 | `<loop_statement_long>` | -> | `<statement_long>` |
| 395 | `<loop_statement_long>` | -> | break ; |
| 396 | `<loop_stmt_list_long>` | -> | `<loop_statement_long>` `<loop_stmt_list_long>` |
| 397 | `<loop_stmt_list_long>` | -> | λ |
| 398 | `<non_empty_loop_stmt_list_long>` | -> | `<loop_statement_long>` `<loop_stmt_list_long>` |
| 399 | `<else_opt_long>` | -> | else `<else_body_long>` |
| 400 | `<else_opt_long>` | -> | λ |
| 401 | `<else_body_long>` | -> | { `<non_empty_stmt_list_long>` } |
| 402 | `<else_body_long>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_long>` } `<else_opt_long>` |
| 403 | `<case_list_long>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_long>` `<break_opt>` `<case_list_long>` |
| 404 | `<case_list_long>` | -> | λ |
| 405 | `<default_opt_long>` | -> | default : `<non_empty_loop_stmt_list_long>` `<break_opt>` |
| 406 | `<default_opt_long>` | -> | λ |
| 407 | `<ctrl_struct_float>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_float>` } `<else_opt_float>` |
| 408 | `<ctrl_struct_float>` | -> | switch ( `<arg_expr>` ) { `<case_list_float>` `<default_opt_float>` } |
| 409 | `<ctrl_struct_float>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_float>` } |
| 410 | `<ctrl_struct_float>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_float>` } |
| 411 | `<ctrl_struct_float>` | -> | do { `<non_empty_loop_stmt_list_float>` } while ( `<condition>` ) ; |
| 412 | `<stmt_list_float>` | -> | `<statement_float>` `<stmt_list_float>` |
| 413 | `<stmt_list_float>` | -> | λ |
| 414 | `<non_empty_stmt_list_float>` | -> | `<statement_float>` `<stmt_list_float>` |
| 415 | `<loop_statement_float>` | -> | `<statement_float>` |
| 416 | `<loop_statement_float>` | -> | break ; |
| 417 | `<loop_stmt_list_float>` | -> | `<loop_statement_float>` `<loop_stmt_list_float>` |
| 418 | `<loop_stmt_list_float>` | -> | λ |
| 419 | `<non_empty_loop_stmt_list_float>` | -> | `<loop_statement_float>` `<loop_stmt_list_float>` |
| 420 | `<else_opt_float>` | -> | else `<else_body_float>` |
| 421 | `<else_opt_float>` | -> | λ |
| 422 | `<else_body_float>` | -> | { `<non_empty_stmt_list_float>` } |
| 423 | `<else_body_float>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_float>` } `<else_opt_float>` |
| 424 | `<case_list_float>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_float>` `<break_opt>` `<case_list_float>` |
| 425 | `<case_list_float>` | -> | λ |
| 426 | `<default_opt_float>` | -> | default : `<non_empty_loop_stmt_list_float>` `<break_opt>` |
| 427 | `<default_opt_float>` | -> | λ |
| 428 | `<ctrl_struct_double>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_double>` } `<else_opt_double>` |
| 429 | `<ctrl_struct_double>` | -> | switch ( `<arg_expr>` ) { `<case_list_double>` `<default_opt_double>` } |
| 430 | `<ctrl_struct_double>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_double>` } |
| 431 | `<ctrl_struct_double>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_double>` } |
| 432 | `<ctrl_struct_double>` | -> | do { `<non_empty_loop_stmt_list_double>` } while ( `<condition>` ) ; |
| 433 | `<stmt_list_double>` | -> | `<statement_double>` `<stmt_list_double>` |
| 434 | `<stmt_list_double>` | -> | λ |
| 435 | `<non_empty_stmt_list_double>` | -> | `<statement_double>` `<stmt_list_double>` |
| 436 | `<loop_statement_double>` | -> | `<statement_double>` |
| 437 | `<loop_statement_double>` | -> | break ; |
| 438 | `<loop_stmt_list_double>` | -> | `<loop_statement_double>` `<loop_stmt_list_double>` |
| 439 | `<loop_stmt_list_double>` | -> | λ |
| 440 | `<non_empty_loop_stmt_list_double>` | -> | `<loop_statement_double>` `<loop_stmt_list_double>` |
| 441 | `<else_opt_double>` | -> | else `<else_body_double>` |
| 442 | `<else_opt_double>` | -> | λ |
| 443 | `<else_body_double>` | -> | { `<non_empty_stmt_list_double>` } |
| 444 | `<else_body_double>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_double>` } `<else_opt_double>` |
| 445 | `<case_list_double>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_double>` `<break_opt>` `<case_list_double>` |
| 446 | `<case_list_double>` | -> | λ |
| 447 | `<default_opt_double>` | -> | default : `<non_empty_loop_stmt_list_double>` `<break_opt>` |
| 448 | `<default_opt_double>` | -> | λ |
| 449 | `<ctrl_struct_char>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_char>` } `<else_opt_char>` |
| 450 | `<ctrl_struct_char>` | -> | switch ( `<arg_expr>` ) { `<case_list_char>` `<default_opt_char>` } |
| 451 | `<ctrl_struct_char>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_char>` } |
| 452 | `<ctrl_struct_char>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_char>` } |
| 453 | `<ctrl_struct_char>` | -> | do { `<non_empty_loop_stmt_list_char>` } while ( `<condition>` ) ; |
| 454 | `<stmt_list_char>` | -> | `<statement_char>` `<stmt_list_char>` |
| 455 | `<stmt_list_char>` | -> | λ |
| 456 | `<non_empty_stmt_list_char>` | -> | `<statement_char>` `<stmt_list_char>` |
| 457 | `<loop_statement_char>` | -> | `<statement_char>` |
| 458 | `<loop_statement_char>` | -> | break ; |
| 459 | `<loop_stmt_list_char>` | -> | `<loop_statement_char>` `<loop_stmt_list_char>` |
| 460 | `<loop_stmt_list_char>` | -> | λ |
| 461 | `<non_empty_loop_stmt_list_char>` | -> | `<loop_statement_char>` `<loop_stmt_list_char>` |
| 462 | `<else_opt_char>` | -> | else `<else_body_char>` |
| 463 | `<else_opt_char>` | -> | λ |
| 464 | `<else_body_char>` | -> | { `<non_empty_stmt_list_char>` } |
| 465 | `<else_body_char>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_char>` } `<else_opt_char>` |
| 466 | `<case_list_char>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_char>` `<break_opt>` `<case_list_char>` |
| 467 | `<case_list_char>` | -> | λ |
| 468 | `<default_opt_char>` | -> | default : `<non_empty_loop_stmt_list_char>` `<break_opt>` |
| 469 | `<default_opt_char>` | -> | λ |
| 470 | `<ctrl_struct_string>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_string>` } `<else_opt_string>` |
| 471 | `<ctrl_struct_string>` | -> | switch ( `<arg_expr>` ) { `<case_list_string>` `<default_opt_string>` } |
| 472 | `<ctrl_struct_string>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_string>` } |
| 473 | `<ctrl_struct_string>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_string>` } |
| 474 | `<ctrl_struct_string>` | -> | do { `<non_empty_loop_stmt_list_string>` } while ( `<condition>` ) ; |
| 475 | `<stmt_list_string>` | -> | `<statement_string>` `<stmt_list_string>` |
| 476 | `<stmt_list_string>` | -> | λ |
| 477 | `<non_empty_stmt_list_string>` | -> | `<statement_string>` `<stmt_list_string>` |
| 478 | `<loop_statement_string>` | -> | `<statement_string>` |
| 479 | `<loop_statement_string>` | -> | break ; |
| 480 | `<loop_stmt_list_string>` | -> | `<loop_statement_string>` `<loop_stmt_list_string>` |
| 481 | `<loop_stmt_list_string>` | -> | λ |
| 482 | `<non_empty_loop_stmt_list_string>` | -> | `<loop_statement_string>` `<loop_stmt_list_string>` |
| 483 | `<else_opt_string>` | -> | else `<else_body_string>` |
| 484 | `<else_opt_string>` | -> | λ |
| 485 | `<else_body_string>` | -> | { `<non_empty_stmt_list_string>` } |
| 486 | `<else_body_string>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_string>` } `<else_opt_string>` |
| 487 | `<case_list_string>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_string>` `<break_opt>` `<case_list_string>` |
| 488 | `<case_list_string>` | -> | λ |
| 489 | `<default_opt_string>` | -> | default : `<non_empty_loop_stmt_list_string>` `<break_opt>` |
| 490 | `<default_opt_string>` | -> | λ |
| 491 | `<ctrl_struct_bool>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_bool>` } `<else_opt_bool>` |
| 492 | `<ctrl_struct_bool>` | -> | switch ( `<arg_expr>` ) { `<case_list_bool>` `<default_opt_bool>` } |
| 493 | `<ctrl_struct_bool>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_bool>` } |
| 494 | `<ctrl_struct_bool>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_bool>` } |
| 495 | `<ctrl_struct_bool>` | -> | do { `<non_empty_loop_stmt_list_bool>` } while ( `<condition>` ) ; |
| 496 | `<stmt_list_bool>` | -> | `<statement_bool>` `<stmt_list_bool>` |
| 497 | `<stmt_list_bool>` | -> | λ |
| 498 | `<non_empty_stmt_list_bool>` | -> | `<statement_bool>` `<stmt_list_bool>` |
| 499 | `<loop_statement_bool>` | -> | `<statement_bool>` |
| 500 | `<loop_statement_bool>` | -> | break ; |
| 501 | `<loop_stmt_list_bool>` | -> | `<loop_statement_bool>` `<loop_stmt_list_bool>` |
| 502 | `<loop_stmt_list_bool>` | -> | λ |
| 503 | `<non_empty_loop_stmt_list_bool>` | -> | `<loop_statement_bool>` `<loop_stmt_list_bool>` |
| 504 | `<else_opt_bool>` | -> | else `<else_body_bool>` |
| 505 | `<else_opt_bool>` | -> | λ |
| 506 | `<else_body_bool>` | -> | { `<non_empty_stmt_list_bool>` } |
| 507 | `<else_body_bool>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_bool>` } `<else_opt_bool>` |
| 508 | `<case_list_bool>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_bool>` `<break_opt>` `<case_list_bool>` |
| 509 | `<case_list_bool>` | -> | λ |
| 510 | `<default_opt_bool>` | -> | default : `<non_empty_loop_stmt_list_bool>` `<break_opt>` |
| 511 | `<default_opt_bool>` | -> | λ |
| 512 | `<ctrl_struct_array>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_array>` } `<else_opt_array>` |
| 513 | `<ctrl_struct_array>` | -> | switch ( `<arg_expr>` ) { `<case_list_array>` `<default_opt_array>` } |
| 514 | `<ctrl_struct_array>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_array>` } |
| 515 | `<ctrl_struct_array>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_array>` } |
| 516 | `<ctrl_struct_array>` | -> | do { `<non_empty_loop_stmt_list_array>` } while ( `<condition>` ) ; |
| 517 | `<stmt_list_array>` | -> | `<statement_array>` `<stmt_list_array>` |
| 518 | `<stmt_list_array>` | -> | λ |
| 519 | `<non_empty_stmt_list_array>` | -> | `<statement_array>` `<stmt_list_array>` |
| 520 | `<loop_statement_array>` | -> | `<statement_array>` |
| 521 | `<loop_statement_array>` | -> | break ; |
| 522 | `<loop_stmt_list_array>` | -> | `<loop_statement_array>` `<loop_stmt_list_array>` |
| 523 | `<loop_stmt_list_array>` | -> | λ |
| 524 | `<non_empty_loop_stmt_list_array>` | -> | `<loop_statement_array>` `<loop_stmt_list_array>` |
| 525 | `<else_opt_array>` | -> | else `<else_body_array>` |
| 526 | `<else_opt_array>` | -> | λ |
| 527 | `<else_body_array>` | -> | { `<non_empty_stmt_list_array>` } |
| 528 | `<else_body_array>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_array>` } `<else_opt_array>` |
| 529 | `<case_list_array>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_array>` `<break_opt>` `<case_list_array>` |
| 530 | `<case_list_array>` | -> | λ |
| 531 | `<default_opt_array>` | -> | default : `<non_empty_loop_stmt_list_array>` `<break_opt>` |
| 532 | `<default_opt_array>` | -> | λ |
| 533 | `<ctrl_struct_weave>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_weave>` } `<else_opt_weave>` |
| 534 | `<ctrl_struct_weave>` | -> | switch ( `<arg_expr>` ) { `<case_list_weave>` `<default_opt_weave>` } |
| 535 | `<ctrl_struct_weave>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_weave>` } |
| 536 | `<ctrl_struct_weave>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_weave>` } |
| 537 | `<ctrl_struct_weave>` | -> | do { `<non_empty_loop_stmt_list_weave>` } while ( `<condition>` ) ; |
| 538 | `<stmt_list_weave>` | -> | `<statement_weave>` `<stmt_list_weave>` |
| 539 | `<stmt_list_weave>` | -> | λ |
| 540 | `<non_empty_stmt_list_weave>` | -> | `<statement_weave>` `<stmt_list_weave>` |
| 541 | `<loop_statement_weave>` | -> | `<statement_weave>` |
| 542 | `<loop_statement_weave>` | -> | break ; |
| 543 | `<loop_stmt_list_weave>` | -> | `<loop_statement_weave>` `<loop_stmt_list_weave>` |
| 544 | `<loop_stmt_list_weave>` | -> | λ |
| 545 | `<non_empty_loop_stmt_list_weave>` | -> | `<loop_statement_weave>` `<loop_stmt_list_weave>` |
| 546 | `<else_opt_weave>` | -> | else `<else_body_weave>` |
| 547 | `<else_opt_weave>` | -> | λ |
| 548 | `<else_body_weave>` | -> | { `<non_empty_stmt_list_weave>` } |
| 549 | `<else_body_weave>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_weave>` } `<else_opt_weave>` |
| 550 | `<case_list_weave>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_weave>` `<break_opt>` `<case_list_weave>` |
| 551 | `<case_list_weave>` | -> | λ |
| 552 | `<default_opt_weave>` | -> | default : `<non_empty_loop_stmt_list_weave>` `<break_opt>` |
| 553 | `<default_opt_weave>` | -> | λ |
| 554 | `<ctrl_struct_void>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_void>` } `<else_opt_void>` |
| 555 | `<ctrl_struct_void>` | -> | switch ( `<arg_expr>` ) { `<case_list_void>` `<default_opt_void>` } |
| 556 | `<ctrl_struct_void>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_void>` } |
| 557 | `<ctrl_struct_void>` | -> | while ( `<condition>` ) { `<non_empty_loop_stmt_list_void>` } |
| 558 | `<ctrl_struct_void>` | -> | do { `<non_empty_loop_stmt_list_void>` } while ( `<condition>` ) ; |
| 559 | `<stmt_list_void>` | -> | `<statement_void>` `<stmt_list_void>` |
| 560 | `<stmt_list_void>` | -> | λ |
| 561 | `<non_empty_stmt_list_void>` | -> | `<statement_void>` `<stmt_list_void>` |
| 562 | `<loop_statement_void>` | -> | `<statement_void>` |
| 563 | `<loop_statement_void>` | -> | break ; |
| 564 | `<loop_stmt_list_void>` | -> | `<loop_statement_void>` `<loop_stmt_list_void>` |
| 565 | `<loop_stmt_list_void>` | -> | λ |
| 566 | `<non_empty_loop_stmt_list_void>` | -> | `<loop_statement_void>` `<loop_stmt_list_void>` |
| 567 | `<else_opt_void>` | -> | else `<else_body_void>` |
| 568 | `<else_opt_void>` | -> | λ |
| 569 | `<else_body_void>` | -> | { `<non_empty_stmt_list_void>` } |
| 570 | `<else_body_void>` | -> | if ( `<condition>` ) { `<non_empty_stmt_list_void>` } `<else_opt_void>` |
| 571 | `<case_list_void>` | -> | case `<case_val>` : `<non_empty_loop_stmt_list_void>` `<break_opt>` `<case_list_void>` |
| 572 | `<case_list_void>` | -> | λ |
| 573 | `<default_opt_void>` | -> | default : `<non_empty_loop_stmt_list_void>` `<break_opt>` |
| 574 | `<default_opt_void>` | -> | λ |
| 575 | `<typed_numeric_ret_expr>` | -> | `<typed_numeric_add_expr>` |
| 576 | `<typed_string_ret_expr>` | -> | `<typed_string_ret_primary>` `<typed_string_cont>` |
| 577 | `<typed_string_ret_primary>` | -> | stringlit |
| 578 | `<typed_string_ret_primary>` | -> | charlit |
| 579 | `<typed_string_ret_primary>` | -> | id `<typed_postfix_chain>` |
| 580 | `<typed_string_ret_primary>` | -> | string ( `<expression>` ) |
| 581 | `<typed_string_ret_primary>` | -> | char ( `<expression>` ) |
| 582 | `<typed_string_ret_primary>` | -> | ( `<expression>` ) `<typed_postfix_chain>` |
| 583 | `<typed_bool_ret_expr>` | -> | `<typed_bool_ret_primary>` `<typed_bool_ret_tail>` |
| 584 | `<typed_bool_ret_primary>` | -> | true |
| 585 | `<typed_bool_ret_primary>` | -> | false |
| 586 | `<typed_bool_ret_primary>` | -> | ! `<typed_bool_factor>` |
| 587 | `<typed_bool_ret_primary>` | -> | id `<typed_bool_id_cont>` |
| 588 | `<typed_bool_ret_primary>` | -> | ( `<typed_bool_paren>` ) |
| 589 | `<typed_bool_ret_primary>` | -> | bool ( `<expression>` ) |
| 590 | `<typed_bool_ret_primary>` | -> | intlit `<typed_numeric_cmp_required>` |
| 591 | `<typed_bool_ret_primary>` | -> | longlit `<typed_numeric_cmp_required>` |
| 592 | `<typed_bool_ret_primary>` | -> | floatlit `<typed_numeric_cmp_required>` |
| 593 | `<typed_bool_ret_primary>` | -> | doublelit `<typed_numeric_cmp_required>` |
| 594 | `<typed_bool_ret_primary>` | -> | - `<typed_numeric_neg_cmp>` |
| 595 | `<typed_bool_ret_primary>` | -> | int ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 596 | `<typed_bool_ret_primary>` | -> | long ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 597 | `<typed_bool_ret_primary>` | -> | float ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 598 | `<typed_bool_ret_primary>` | -> | double ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 599 | `<typed_bool_ret_tail>` | -> | && `<typed_bool_term>` `<typed_bool_and_tail>` `<typed_bool_or_tail_opt>` |
| 600 | `<typed_bool_ret_tail>` | -> | || `<typed_bool_term>` `<typed_bool_or_tail>` |
| 601 | `<typed_bool_ret_tail>` | -> | == `<typed_bool_factor>` `<typed_bool_eq_tail>` `<typed_bool_ret_tail>` |
| 602 | `<typed_bool_ret_tail>` | -> | != `<typed_bool_factor>` `<typed_bool_eq_tail>` `<typed_bool_ret_tail>` |
| 603 | `<typed_bool_ret_tail>` | -> | λ |
| 604 | `<using_cont>` | -> | , id `<using_cont>` |
| 605 | `<using_cont>` | -> | λ |
| 606 | `<local_dec_body>` | -> | int id `<int_local_tail>` |
| 607 | `<local_dec_body>` | -> | long id `<long_local_tail>` |
| 608 | `<local_dec_body>` | -> | float id `<float_local_tail>` |
| 609 | `<local_dec_body>` | -> | double id `<double_local_tail>` |
| 610 | `<local_dec_body>` | -> | char id `<char_local_tail>` |
| 611 | `<local_dec_body>` | -> | string id `<string_local_tail>` |
| 612 | `<local_dec_body>` | -> | bool id `<bool_local_tail>` |
| 613 | `<local_dec_body>` | -> | id id `<weave_local_tail>` |
| 614 | `<int_local_tail>` | -> | `<int_array_with_init>` ; |
| 615 | `<int_local_tail>` | -> | = intlit `<int_local_cont>` ; |
| 616 | `<int_local_cont>` | -> | , id = intlit `<int_local_cont>` |
| 617 | `<int_local_cont>` | -> | λ |
| 618 | `<long_local_tail>` | -> | `<long_array_with_init>` ; |
| 619 | `<long_local_tail>` | -> | = longlit `<long_local_cont>` ; |
| 620 | `<long_local_cont>` | -> | , id = longlit `<long_local_cont>` |
| 621 | `<long_local_cont>` | -> | λ |
| 622 | `<float_local_tail>` | -> | `<float_array_with_init>` ; |
| 623 | `<float_local_tail>` | -> | = floatlit `<float_local_cont>` ; |
| 624 | `<float_local_cont>` | -> | , id = floatlit `<float_local_cont>` |
| 625 | `<float_local_cont>` | -> | λ |
| 626 | `<double_local_tail>` | -> | `<double_array_with_init>` ; |
| 627 | `<double_local_tail>` | -> | = doublelit `<double_local_cont>` ; |
| 628 | `<double_local_cont>` | -> | , id = doublelit `<double_local_cont>` |
| 629 | `<double_local_cont>` | -> | λ |
| 630 | `<char_local_tail>` | -> | `<char_array_with_init>` ; |
| 631 | `<char_local_tail>` | -> | = charlit `<char_local_cont>` ; |
| 632 | `<char_local_cont>` | -> | , id = charlit `<char_local_cont>` |
| 633 | `<char_local_cont>` | -> | λ |
| 634 | `<string_local_tail>` | -> | `<string_array_with_init>` ; |
| 635 | `<string_local_tail>` | -> | = stringlit `<string_local_cont>` ; |
| 636 | `<string_local_cont>` | -> | , id = stringlit `<string_local_cont>` |
| 637 | `<string_local_cont>` | -> | λ |
| 638 | `<bool_local_tail>` | -> | `<bool_array_with_init>` ; |
| 639 | `<bool_local_tail>` | -> | = `<bool_lit>` `<bool_local_cont>` ; |
| 640 | `<bool_local_cont>` | -> | , id = `<bool_lit>` `<bool_local_cont>` |
| 641 | `<bool_local_cont>` | -> | λ |
| 642 | `<weave_local_tail>` | -> | = { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_inst_cont>` ; |
| 643 | `<weave_local_tail>` | -> | `<weave_array_with_init>` `<weave_arr_cont>` ; |
| 644 | `<statement_non_return>` | -> | `<effect_stmt>` ; |
| 645 | `<statement_non_return>` | -> | `<io_stmt>` |
| 646 | `<statement_non_return>` | -> | `<ctrl_struct>` |
| 647 | `<expression>` | -> | `<typed_assign_expr>` |
| 648 | `<typed_assign_expr>` | -> | `<typed_concat_expr>` `<typed_assign_tail>` |
| 649 | `<typed_assign_tail>` | -> | = `<typed_rhs_expr>` |
| 650 | `<typed_assign_tail>` | -> | += `<typed_numeric_add_expr>` |
| 651 | `<typed_assign_tail>` | -> | -= `<typed_numeric_add_expr>` |
| 652 | `<typed_assign_tail>` | -> | *= `<typed_numeric_add_expr>` |
| 653 | `<typed_assign_tail>` | -> | /= `<typed_numeric_add_expr>` |
| 654 | `<typed_assign_tail>` | -> | %= `<typed_numeric_add_expr>` |
| 655 | `<typed_assign_tail>` | -> | λ |
| 656 | `<assign_op>` | -> | = |
| 657 | `<assign_op>` | -> | += |
| 658 | `<assign_op>` | -> | -= |
| 659 | `<assign_op>` | -> | *= |
| 660 | `<assign_op>` | -> | /= |
| 661 | `<assign_op>` | -> | %= |
| 662 | `<typed_rhs_expr>` | -> | `<typed_concat_expr>` |
| 663 | `<typed_concat_expr>` | -> | stringlit `<typed_string_cont>` |
| 664 | `<typed_concat_expr>` | -> | charlit `<typed_string_cont>` |
| 665 | `<typed_concat_expr>` | -> | intlit `<typed_numeric_cont>` |
| 666 | `<typed_concat_expr>` | -> | longlit `<typed_numeric_cont>` |
| 667 | `<typed_concat_expr>` | -> | floatlit `<typed_numeric_cont>` |
| 668 | `<typed_concat_expr>` | -> | doublelit `<typed_numeric_cont>` |
| 669 | `<typed_concat_expr>` | -> | true `<typed_bool_cont>` |
| 670 | `<typed_concat_expr>` | -> | false `<typed_bool_cont>` |
| 671 | `<typed_concat_expr>` | -> | ! `<typed_bool_factor>` `<typed_bool_tail_opt>` |
| 672 | `<typed_concat_expr>` | -> | - `<typed_neg_numeric_cont>` |
| 673 | `<typed_concat_expr>` | -> | id `<typed_id_cont>` |
| 674 | `<typed_concat_expr>` | -> | ( `<typed_paren_cont>` |
| 675 | `<typed_concat_expr>` | -> | int ( `<expression>` ) `<typed_numeric_cont>` |
| 676 | `<typed_concat_expr>` | -> | long ( `<expression>` ) `<typed_numeric_cont>` |
| 677 | `<typed_concat_expr>` | -> | float ( `<expression>` ) `<typed_numeric_cont>` |
| 678 | `<typed_concat_expr>` | -> | double ( `<expression>` ) `<typed_numeric_cont>` |
| 679 | `<typed_concat_expr>` | -> | char ( `<expression>` ) `<typed_string_cont>` |
| 680 | `<typed_concat_expr>` | -> | string ( `<expression>` ) `<typed_string_cont>` |
| 681 | `<typed_concat_expr>` | -> | bool ( `<expression>` ) `<typed_bool_cont>` |
| 682 | `<typed_string_cont>` | -> | .. `<typed_string_operand>` `<typed_string_cont>` |
| 683 | `<typed_string_cont>` | -> | λ |
| 684 | `<typed_string_operand>` | -> | stringlit |
| 685 | `<typed_string_operand>` | -> | charlit |
| 686 | `<typed_string_operand>` | -> | id |
| 687 | `<typed_string_operand>` | -> | string ( `<expression>` ) |
| 688 | `<typed_string_operand>` | -> | char ( `<expression>` ) |
| 689 | `<typed_string_operand>` | -> | ( `<typed_string_operand>` `<typed_string_cont>` ) |
| 690 | `<typed_string_operand>` | -> | intlit |
| 691 | `<typed_string_operand>` | -> | longlit |
| 692 | `<typed_string_operand>` | -> | floatlit |
| 693 | `<typed_string_operand>` | -> | doublelit |
| 694 | `<typed_string_operand>` | -> | true |
| 695 | `<typed_string_operand>` | -> | false |
| 696 | `<typed_string_operand>` | -> | int ( `<expression>` ) |
| 697 | `<typed_string_operand>` | -> | long ( `<expression>` ) |
| 698 | `<typed_string_operand>` | -> | float ( `<expression>` ) |
| 699 | `<typed_string_operand>` | -> | double ( `<expression>` ) |
| 700 | `<typed_string_operand>` | -> | bool ( `<expression>` ) |
| 701 | `<typed_numeric_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 702 | `<typed_numeric_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 703 | `<typed_numeric_cont>` | -> | `<typed_bool_tail_opt>` |
| 704 | `<typed_arith_ops>` | -> | + `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` |
| 705 | `<typed_arith_ops>` | -> | - `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` |
| 706 | `<typed_arith_ops>` | -> | * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` |
| 707 | `<typed_arith_ops>` | -> | / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` |
| 708 | `<typed_arith_ops>` | -> | % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` |
| 709 | `<typed_numeric_add_ops>` | -> | + `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` |
| 710 | `<typed_numeric_add_ops>` | -> | - `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` |
| 711 | `<typed_numeric_add_ops>` | -> | λ |
| 712 | `<typed_after_arith>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 713 | `<typed_after_arith>` | -> | `<typed_bool_tail_opt>` |
| 714 | `<typed_neg_numeric_cont>` | -> | `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` `<typed_after_arith>` |
| 715 | `<typed_bool_cont>` | -> | `<typed_bool_tail_opt>` |
| 716 | `<typed_bool_tail_opt>` | -> | && `<typed_bool_term>` `<typed_bool_and_tail>` `<typed_bool_or_tail_opt>` |
| 717 | `<typed_bool_tail_opt>` | -> | || `<typed_bool_term>` `<typed_bool_or_tail>` |
| 718 | `<typed_bool_tail_opt>` | -> | λ |
| 719 | `<typed_bool_or_tail_opt>` | -> | || `<typed_bool_term>` `<typed_bool_or_tail>` |
| 720 | `<typed_bool_or_tail_opt>` | -> | λ |
| 721 | `<typed_bool_term>` | -> | `<typed_bool_eq>` `<typed_bool_and_tail>` |
| 722 | `<typed_bool_and_tail>` | -> | && `<typed_bool_eq>` `<typed_bool_and_tail>` |
| 723 | `<typed_bool_and_tail>` | -> | λ |
| 724 | `<typed_bool_or_tail>` | -> | || `<typed_bool_term>` `<typed_bool_or_tail>` |
| 725 | `<typed_bool_or_tail>` | -> | λ |
| 726 | `<typed_bool_eq>` | -> | `<typed_bool_factor>` `<typed_bool_eq_tail>` |
| 727 | `<typed_bool_eq_tail>` | -> | == `<typed_bool_factor>` `<typed_bool_eq_tail>` |
| 728 | `<typed_bool_eq_tail>` | -> | != `<typed_bool_factor>` `<typed_bool_eq_tail>` |
| 729 | `<typed_bool_eq_tail>` | -> | λ |
| 730 | `<typed_bool_factor>` | -> | ! `<typed_bool_factor>` |
| 731 | `<typed_bool_factor>` | -> | `<typed_bool_atom>` |
| 732 | `<typed_bool_atom>` | -> | true |
| 733 | `<typed_bool_atom>` | -> | false |
| 734 | `<typed_bool_atom>` | -> | id `<typed_bool_id_cont>` |
| 735 | `<typed_bool_atom>` | -> | intlit `<typed_numeric_cmp_required>` |
| 736 | `<typed_bool_atom>` | -> | longlit `<typed_numeric_cmp_required>` |
| 737 | `<typed_bool_atom>` | -> | floatlit `<typed_numeric_cmp_required>` |
| 738 | `<typed_bool_atom>` | -> | doublelit `<typed_numeric_cmp_required>` |
| 739 | `<typed_bool_atom>` | -> | - `<typed_numeric_neg_cmp>` |
| 740 | `<typed_bool_atom>` | -> | ( `<typed_bool_paren>` ) |
| 741 | `<typed_bool_atom>` | -> | int ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 742 | `<typed_bool_atom>` | -> | long ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 743 | `<typed_bool_atom>` | -> | float ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 744 | `<typed_bool_atom>` | -> | double ( `<expression>` ) `<typed_numeric_cmp_required>` |
| 745 | `<typed_bool_paren>` | -> | `<typed_bool_term>` `<typed_bool_and_or_tail>` |
| 746 | `<typed_bool_and_or_tail>` | -> | && `<typed_bool_term>` `<typed_bool_and_or_tail>` |
| 747 | `<typed_bool_and_or_tail>` | -> | || `<typed_bool_term>` `<typed_bool_and_or_tail>` |
| 748 | `<typed_bool_and_or_tail>` | -> | λ |
| 749 | `<typed_bool_id_cont>` | -> | `<typed_numeric_arith_cmp>` |
| 750 | `<typed_bool_id_cont>` | -> | `<typed_postfix_chain>` |
| 751 | `<typed_numeric_arith_cmp>` | -> | + `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 752 | `<typed_numeric_arith_cmp>` | -> | - `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 753 | `<typed_numeric_arith_cmp>` | -> | * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 754 | `<typed_numeric_arith_cmp>` | -> | / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 755 | `<typed_numeric_arith_cmp>` | -> | % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 756 | `<typed_numeric_arith_cmp>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 757 | `<typed_numeric_add_cmp>` | -> | + `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` |
| 758 | `<typed_numeric_add_cmp>` | -> | - `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` |
| 759 | `<typed_numeric_add_cmp>` | -> | λ |
| 760 | `<typed_numeric_cmp_required>` | -> | `<typed_numeric_lit_arith>` `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 761 | `<typed_numeric_lit_arith>` | -> | * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` |
| 762 | `<typed_numeric_lit_arith>` | -> | / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` |
| 763 | `<typed_numeric_lit_arith>` | -> | % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` |
| 764 | `<typed_numeric_lit_arith>` | -> | + `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` |
| 765 | `<typed_numeric_lit_arith>` | -> | - `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` |
| 766 | `<typed_numeric_lit_arith>` | -> | λ |
| 767 | `<typed_numeric_neg_cmp>` | -> | `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` |
| 768 | `<typed_id_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 769 | `<typed_id_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 770 | `<typed_id_cont>` | -> | ++ |
| 771 | `<typed_id_cont>` | -> | -- |
| 772 | `<typed_id_cont>` | -> | [ `<array_index>` ] `<typed_id_arr_cont>` |
| 773 | `<typed_id_cont>` | -> | . id `<typed_id_field_cont>` |
| 774 | `<typed_id_cont>` | -> | ( `<arg_list>` ) `<typed_id_call_cont>` |
| 775 | `<typed_id_cont>` | -> | .. `<typed_string_operand>` `<typed_string_cont>` |
| 776 | `<typed_id_cont>` | -> | `<typed_bool_tail_opt>` |
| 777 | `<typed_id_arr_cont>` | -> | [ `<array_index>` ] `<typed_id_arr2_cont>` |
| 778 | `<typed_id_arr_cont>` | -> | `<typed_id_postfix_cont>` |
| 779 | `<typed_id_arr2_cont>` | -> | `<typed_id_postfix_cont>` |
| 780 | `<typed_id_postfix_cont>` | -> | . id `<typed_id_field_cont>` |
| 781 | `<typed_id_postfix_cont>` | -> | ( `<arg_list>` ) `<typed_id_call_cont>` |
| 782 | `<typed_id_postfix_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 783 | `<typed_id_postfix_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 784 | `<typed_id_postfix_cont>` | -> | .. `<typed_string_operand>` `<typed_string_cont>` |
| 785 | `<typed_id_postfix_cont>` | -> | `<typed_bool_tail_opt>` |
| 786 | `<typed_id_field_cont>` | -> | [ `<array_index>` ] `<typed_id_arr_cont>` |
| 787 | `<typed_id_field_cont>` | -> | . id `<typed_id_field_cont>` |
| 788 | `<typed_id_field_cont>` | -> | ( `<arg_list>` ) `<typed_id_call_cont>` |
| 789 | `<typed_id_field_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 790 | `<typed_id_field_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 791 | `<typed_id_field_cont>` | -> | .. `<typed_string_operand>` `<typed_string_cont>` |
| 792 | `<typed_id_field_cont>` | -> | `<typed_bool_tail_opt>` |
| 793 | `<typed_id_call_cont>` | -> | [ `<array_index>` ] `<typed_id_arr_cont>` |
| 794 | `<typed_id_call_cont>` | -> | . id `<typed_id_field_cont>` |
| 795 | `<typed_id_call_cont>` | -> | ( `<arg_list>` ) `<typed_id_call_cont>` |
| 796 | `<typed_id_call_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 797 | `<typed_id_call_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 798 | `<typed_id_call_cont>` | -> | .. `<typed_string_operand>` `<typed_string_cont>` |
| 799 | `<typed_id_call_cont>` | -> | `<typed_bool_tail_opt>` |
| 800 | `<typed_paren_cont>` | -> | `<typed_concat_expr>` ) `<typed_paren_after>` |
| 801 | `<typed_paren_after>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 802 | `<typed_paren_after>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 803 | `<typed_paren_after>` | -> | .. `<typed_string_operand>` `<typed_string_cont>` |
| 804 | `<typed_paren_after>` | -> | [ `<array_index>` ] `<typed_paren_arr_cont>` |
| 805 | `<typed_paren_after>` | -> | . id `<typed_paren_field_cont>` |
| 806 | `<typed_paren_after>` | -> | ( `<arg_list>` ) `<typed_paren_call_cont>` |
| 807 | `<typed_paren_after>` | -> | `<typed_bool_tail_opt>` |
| 808 | `<typed_paren_arr_cont>` | -> | [ `<array_index>` ] `<typed_paren_arr2_cont>` |
| 809 | `<typed_paren_arr_cont>` | -> | `<typed_paren_postfix_cont>` |
| 810 | `<typed_paren_arr2_cont>` | -> | `<typed_paren_postfix_cont>` |
| 811 | `<typed_paren_postfix_cont>` | -> | . id `<typed_paren_field_cont>` |
| 812 | `<typed_paren_postfix_cont>` | -> | ( `<arg_list>` ) `<typed_paren_call_cont>` |
| 813 | `<typed_paren_postfix_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 814 | `<typed_paren_postfix_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 815 | `<typed_paren_postfix_cont>` | -> | λ |
| 816 | `<typed_paren_field_cont>` | -> | [ `<array_index>` ] `<typed_paren_arr_cont>` |
| 817 | `<typed_paren_field_cont>` | -> | . id `<typed_paren_field_cont>` |
| 818 | `<typed_paren_field_cont>` | -> | ( `<arg_list>` ) `<typed_paren_call_cont>` |
| 819 | `<typed_paren_field_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 820 | `<typed_paren_field_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 821 | `<typed_paren_field_cont>` | -> | λ |
| 822 | `<typed_paren_call_cont>` | -> | [ `<array_index>` ] `<typed_paren_arr_cont>` |
| 823 | `<typed_paren_call_cont>` | -> | . id `<typed_paren_field_cont>` |
| 824 | `<typed_paren_call_cont>` | -> | ( `<arg_list>` ) `<typed_paren_call_cont>` |
| 825 | `<typed_paren_call_cont>` | -> | `<typed_arith_ops>` `<typed_after_arith>` |
| 826 | `<typed_paren_call_cont>` | -> | `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` |
| 827 | `<typed_paren_call_cont>` | -> | λ |
| 828 | `<typed_numeric_add_expr>` | -> | `<typed_numeric_mul_expr>` `<typed_numeric_add_tail>` |
| 829 | `<typed_numeric_add_tail>` | -> | + `<typed_numeric_mul_expr>` `<typed_numeric_add_tail>` |
| 830 | `<typed_numeric_add_tail>` | -> | - `<typed_numeric_mul_expr>` `<typed_numeric_add_tail>` |
| 831 | `<typed_numeric_add_tail>` | -> | λ |
| 832 | `<typed_numeric_mul_expr>` | -> | `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` |
| 833 | `<typed_numeric_mul_tail>` | -> | * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` |
| 834 | `<typed_numeric_mul_tail>` | -> | / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` |
| 835 | `<typed_numeric_mul_tail>` | -> | % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` |
| 836 | `<typed_numeric_mul_tail>` | -> | λ |
| 837 | `<typed_numeric_unary_expr>` | -> | ! `<typed_numeric_unary_expr>` |
| 838 | `<typed_numeric_unary_expr>` | -> | - `<typed_numeric_unary_expr>` |
| 839 | `<typed_numeric_unary_expr>` | -> | ++ `<typed_numeric_unary_expr>` |
| 840 | `<typed_numeric_unary_expr>` | -> | -- `<typed_numeric_unary_expr>` |
| 841 | `<typed_numeric_unary_expr>` | -> | `<typed_numeric_postfix_expr>` |
| 842 | `<typed_numeric_postfix_expr>` | -> | intlit |
| 843 | `<typed_numeric_postfix_expr>` | -> | longlit |
| 844 | `<typed_numeric_postfix_expr>` | -> | floatlit |
| 845 | `<typed_numeric_postfix_expr>` | -> | doublelit |
| 846 | `<typed_numeric_postfix_expr>` | -> | id `<typed_postfix_chain>` |
| 847 | `<typed_numeric_postfix_expr>` | -> | ( `<expression>` ) `<typed_postfix_chain>` |
| 848 | `<typed_numeric_postfix_expr>` | -> | int ( `<expression>` ) |
| 849 | `<typed_numeric_postfix_expr>` | -> | long ( `<expression>` ) |
| 850 | `<typed_numeric_postfix_expr>` | -> | float ( `<expression>` ) |
| 851 | `<typed_numeric_postfix_expr>` | -> | double ( `<expression>` ) |
| 852 | `<typed_cmp_op>` | -> | < |
| 853 | `<typed_cmp_op>` | -> | > |
| 854 | `<typed_cmp_op>` | -> | <= |
| 855 | `<typed_cmp_op>` | -> | >= |
| 856 | `<typed_cmp_op>` | -> | == |
| 857 | `<typed_cmp_op>` | -> | != |
| 858 | `<typed_postfix_chain>` | -> | [ `<array_index>` ] `<typed_postfix_after_arr>` |
| 859 | `<typed_postfix_chain>` | -> | . id `<typed_postfix_chain>` |
| 860 | `<typed_postfix_chain>` | -> | ( `<arg_list>` ) `<typed_postfix_chain>` |
| 861 | `<typed_postfix_chain>` | -> | ++ |
| 862 | `<typed_postfix_chain>` | -> | -- |
| 863 | `<typed_postfix_chain>` | -> | λ |
| 864 | `<typed_postfix_after_arr>` | -> | [ `<array_index>` ] `<typed_postfix_after_arr>` |
| 865 | `<typed_postfix_after_arr>` | -> | . id `<typed_postfix_chain>` |
| 866 | `<typed_postfix_after_arr>` | -> | ( `<arg_list>` ) `<typed_postfix_chain>` |
| 867 | `<typed_postfix_after_arr>` | -> | ++ |
| 868 | `<typed_postfix_after_arr>` | -> | -- |
| 869 | `<typed_postfix_after_arr>` | -> | λ |
| 870 | `<array_index>` | -> | intlit |
| 871 | `<array_index>` | -> | id |
| 872 | `<arg_list>` | -> | `<arg_expr>` `<arg_tail>` |
| 873 | `<arg_list>` | -> | λ |
| 874 | `<arg_tail>` | -> | , `<arg_expr>` `<arg_tail>` |
| 875 | `<arg_tail>` | -> | λ |
| 876 | `<effect_stmt>` | -> | ++ id `<effect_pre_chain>` |
| 877 | `<effect_stmt>` | -> | -- id `<effect_pre_chain>` |
| 878 | `<effect_stmt>` | -> | id `<effect_id_cont>` |
| 879 | `<effect_pre_chain>` | -> | [ `<stmt_array_index>` ] `<effect_pre_arr_chain>` |
| 880 | `<effect_pre_chain>` | -> | . id `<effect_pre_chain>` |
| 881 | `<effect_pre_chain>` | -> | λ |
| 882 | `<effect_pre_arr_chain>` | -> | [ `<stmt_array_index>` ] |
| 883 | `<effect_pre_arr_chain>` | -> | . id `<effect_pre_chain>` |
| 884 | `<effect_pre_arr_chain>` | -> | λ |
| 885 | `<effect_id_cont>` | -> | = `<stmt_assign_expr>` |
| 886 | `<effect_id_cont>` | -> | += `<numeric_add_expr_stmt>` |
| 887 | `<effect_id_cont>` | -> | -= `<numeric_add_expr_stmt>` |
| 888 | `<effect_id_cont>` | -> | *= `<numeric_add_expr_stmt>` |
| 889 | `<effect_id_cont>` | -> | /= `<numeric_add_expr_stmt>` |
| 890 | `<effect_id_cont>` | -> | %= `<numeric_add_expr_stmt>` |
| 891 | `<effect_id_cont>` | -> | ++ |
| 892 | `<effect_id_cont>` | -> | -- |
| 893 | `<effect_id_cont>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 894 | `<effect_id_cont>` | -> | [ `<stmt_array_index>` ] `<effect_post_arr>` |
| 895 | `<effect_id_cont>` | -> | . id `<effect_post_member>` |
| 896 | `<effect_post_call>` | -> | . id `<effect_post_call_member>` |
| 897 | `<effect_post_call>` | -> | [ `<stmt_array_index>` ] `<effect_post_call_arr>` |
| 898 | `<effect_post_call>` | -> | λ |
| 899 | `<effect_post_call_member>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 900 | `<effect_post_call_member>` | -> | [ `<stmt_array_index>` ] `<effect_post_call_arr>` |
| 901 | `<effect_post_call_member>` | -> | . id `<effect_post_call_member>` |
| 902 | `<effect_post_call_member>` | -> | λ |
| 903 | `<effect_post_call_arr>` | -> | [ `<stmt_array_index>` ] `<effect_post_call_arr_cont>` |
| 904 | `<effect_post_call_arr>` | -> | `<effect_post_call_arr_cont>` |
| 905 | `<effect_post_call_arr_cont>` | -> | . id `<effect_post_call_member>` |
| 906 | `<effect_post_call_arr_cont>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 907 | `<effect_post_call_arr_cont>` | -> | λ |
| 908 | `<effect_post_arr>` | -> | [ `<stmt_array_index>` ] `<effect_post_arr_2d>` |
| 909 | `<effect_post_arr>` | -> | `<effect_arr_effect>` |
| 910 | `<effect_post_arr_2d>` | -> | `<effect_arr_effect>` |
| 911 | `<effect_arr_effect>` | -> | = `<stmt_assign_expr>` |
| 912 | `<effect_arr_effect>` | -> | += `<numeric_add_expr_stmt>` |
| 913 | `<effect_arr_effect>` | -> | -= `<numeric_add_expr_stmt>` |
| 914 | `<effect_arr_effect>` | -> | *= `<numeric_add_expr_stmt>` |
| 915 | `<effect_arr_effect>` | -> | /= `<numeric_add_expr_stmt>` |
| 916 | `<effect_arr_effect>` | -> | %= `<numeric_add_expr_stmt>` |
| 917 | `<effect_arr_effect>` | -> | ++ |
| 918 | `<effect_arr_effect>` | -> | -- |
| 919 | `<effect_arr_effect>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 920 | `<effect_arr_effect>` | -> | . id `<effect_post_member>` |
| 921 | `<effect_post_member>` | -> | = `<stmt_assign_expr>` |
| 922 | `<effect_post_member>` | -> | += `<numeric_add_expr_stmt>` |
| 923 | `<effect_post_member>` | -> | -= `<numeric_add_expr_stmt>` |
| 924 | `<effect_post_member>` | -> | *= `<numeric_add_expr_stmt>` |
| 925 | `<effect_post_member>` | -> | /= `<numeric_add_expr_stmt>` |
| 926 | `<effect_post_member>` | -> | %= `<numeric_add_expr_stmt>` |
| 927 | `<effect_post_member>` | -> | ++ |
| 928 | `<effect_post_member>` | -> | -- |
| 929 | `<effect_post_member>` | -> | ( `<stmt_arg_list>` ) `<effect_post_call>` |
| 930 | `<effect_post_member>` | -> | [ `<stmt_array_index>` ] `<effect_post_arr>` |
| 931 | `<effect_post_member>` | -> | . id `<effect_post_member>` |
| 932 | `<stmt_assign_expr>` | -> | `<stmt_typed_rhs>` |
| 933 | `<stmt_typed_rhs>` | -> | `<stmt_bool_or_concat>` |
| 934 | `<stmt_bool_or_concat>` | -> | stringlit `<stmt_concat_tail_typed>` |
| 935 | `<stmt_bool_or_concat>` | -> | charlit `<stmt_concat_tail_typed>` |
| 936 | `<stmt_bool_or_concat>` | -> | string ( `<arg_expr>` ) `<stmt_concat_tail_typed>` |
| 937 | `<stmt_bool_or_concat>` | -> | intlit `<stmt_numeric_or_bool>` |
| 938 | `<stmt_bool_or_concat>` | -> | longlit `<stmt_numeric_or_bool>` |
| 939 | `<stmt_bool_or_concat>` | -> | floatlit `<stmt_numeric_or_bool>` |
| 940 | `<stmt_bool_or_concat>` | -> | doublelit `<stmt_numeric_or_bool>` |
| 941 | `<stmt_bool_or_concat>` | -> | - `<stmt_neg_numeric_or_bool>` |
| 942 | `<stmt_bool_or_concat>` | -> | true `<stmt_bool_tail_opt>` |
| 943 | `<stmt_bool_or_concat>` | -> | false `<stmt_bool_tail_opt>` |
| 944 | `<stmt_bool_or_concat>` | -> | ! `<stmt_bool_factor>` `<stmt_bool_tail_opt>` |
| 945 | `<stmt_bool_or_concat>` | -> | int ( `<arg_expr>` ) `<stmt_numeric_or_bool>` |
| 946 | `<stmt_bool_or_concat>` | -> | long ( `<arg_expr>` ) `<stmt_numeric_or_bool>` |
| 947 | `<stmt_bool_or_concat>` | -> | float ( `<arg_expr>` ) `<stmt_numeric_or_bool>` |
| 948 | `<stmt_bool_or_concat>` | -> | double ( `<arg_expr>` ) `<stmt_numeric_or_bool>` |
| 949 | `<stmt_bool_or_concat>` | -> | char ( `<arg_expr>` ) |
| 950 | `<stmt_bool_or_concat>` | -> | bool ( `<arg_expr>` ) `<stmt_bool_tail_opt>` |
| 951 | `<stmt_bool_or_concat>` | -> | id `<stmt_id_toplevel_cont>` |
| 952 | `<stmt_bool_or_concat>` | -> | ( `<stmt_paren_typed_content>` |
| 953 | `<stmt_bool_or_concat>` | -> | ++ id `<stmt_postfix_chain>` `<stmt_id_after_postfix>` |
| 954 | `<stmt_bool_or_concat>` | -> | -- id `<stmt_postfix_chain>` `<stmt_id_after_postfix>` |
| 955 | `<stmt_numeric_or_bool>` | -> | `<stmt_arith_ops>` `<stmt_after_arith>` |
| 956 | `<stmt_numeric_or_bool>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` |
| 957 | `<stmt_numeric_or_bool>` | -> | `<stmt_bool_tail_opt>` |
| 958 | `<stmt_arith_ops>` | -> | + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` |
| 959 | `<stmt_arith_ops>` | -> | - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` |
| 960 | `<stmt_arith_ops>` | -> | * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` |
| 961 | `<stmt_arith_ops>` | -> | / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` |
| 962 | `<stmt_arith_ops>` | -> | % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` |
| 963 | `<stmt_numeric_add_ops>` | -> | + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` |
| 964 | `<stmt_numeric_add_ops>` | -> | - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` |
| 965 | `<stmt_numeric_add_ops>` | -> | λ |
| 966 | `<stmt_after_arith>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` |
| 967 | `<stmt_after_arith>` | -> | `<stmt_bool_tail_opt>` |
| 968 | `<stmt_neg_numeric_or_bool>` | -> | `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_after_arith>` |
| 969 | `<stmt_bool_tail_opt>` | -> | && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` |
| 970 | `<stmt_bool_tail_opt>` | -> | || `<stmt_bool_term>` `<stmt_bool_or_tail>` |
| 971 | `<stmt_bool_tail_opt>` | -> | λ |
| 972 | `<stmt_bool_or_tail_opt>` | -> | || `<stmt_bool_term>` `<stmt_bool_or_tail>` |
| 973 | `<stmt_bool_or_tail_opt>` | -> | λ |
| 974 | `<stmt_id_toplevel_cont>` | -> | `<stmt_arith_ops>` `<stmt_after_arith>` |
| 975 | `<stmt_id_toplevel_cont>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` |
| 976 | `<stmt_id_toplevel_cont>` | -> | ++ `<stmt_id_after_postfix>` |
| 977 | `<stmt_id_toplevel_cont>` | -> | -- `<stmt_id_after_postfix>` |
| 978 | `<stmt_id_toplevel_cont>` | -> | `<stmt_postfix_chain>` `<stmt_id_after_postfix>` |
| 979 | `<stmt_id_after_postfix>` | -> | `<stmt_arith_ops>` `<stmt_after_arith>` |
| 980 | `<stmt_id_after_postfix>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` |
| 981 | `<stmt_id_after_postfix>` | -> | .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` |
| 982 | `<stmt_id_after_postfix>` | -> | ++ |
| 983 | `<stmt_id_after_postfix>` | -> | -- |
| 984 | `<stmt_id_after_postfix>` | -> | `<stmt_bool_tail_opt>` |
| 985 | `<stmt_paren_typed_content>` | -> | stringlit `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` |
| 986 | `<stmt_paren_typed_content>` | -> | charlit `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` |
| 987 | `<stmt_paren_typed_content>` | -> | string ( `<arg_expr>` ) `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` |
| 988 | `<stmt_paren_typed_content>` | -> | char ( `<arg_expr>` ) ) `<stmt_paren_string_cont>` |
| 989 | `<stmt_paren_typed_content>` | -> | intlit `<stmt_paren_num_start>` |
| 990 | `<stmt_paren_typed_content>` | -> | longlit `<stmt_paren_num_start>` |
| 991 | `<stmt_paren_typed_content>` | -> | floatlit `<stmt_paren_num_start>` |
| 992 | `<stmt_paren_typed_content>` | -> | doublelit `<stmt_paren_num_start>` |
| 993 | `<stmt_paren_typed_content>` | -> | - `<stmt_paren_neg_num>` |
| 994 | `<stmt_paren_typed_content>` | -> | int ( `<arg_expr>` ) `<stmt_paren_num_start>` |
| 995 | `<stmt_paren_typed_content>` | -> | long ( `<arg_expr>` ) `<stmt_paren_num_start>` |
| 996 | `<stmt_paren_typed_content>` | -> | float ( `<arg_expr>` ) `<stmt_paren_num_start>` |
| 997 | `<stmt_paren_typed_content>` | -> | double ( `<arg_expr>` ) `<stmt_paren_num_start>` |
| 998 | `<stmt_paren_typed_content>` | -> | true `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 999 | `<stmt_paren_typed_content>` | -> | false `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1000 | `<stmt_paren_typed_content>` | -> | ! `<stmt_bool_factor>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1001 | `<stmt_paren_typed_content>` | -> | bool ( `<arg_expr>` ) `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1002 | `<stmt_paren_typed_content>` | -> | id `<stmt_paren_id_cont>` |
| 1003 | `<stmt_paren_typed_content>` | -> | ( `<stmt_paren_typed_content>` ) `<stmt_paren_any_cont>` |
| 1004 | `<stmt_paren_typed_content>` | -> | ++ id `<stmt_paren_num_after_incr>` |
| 1005 | `<stmt_paren_typed_content>` | -> | -- id `<stmt_paren_num_after_incr>` |
| 1006 | `<stmt_paren_string_cont>` | -> | .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` |
| 1007 | `<stmt_paren_string_cont>` | -> | λ |
| 1008 | `<stmt_paren_num_start>` | -> | `<stmt_paren_arith_ops>` |
| 1009 | `<stmt_paren_num_start>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1010 | `<stmt_paren_num_start>` | -> | ) `<stmt_paren_num_cont>` |
| 1011 | `<stmt_paren_arith_ops>` | -> | + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` |
| 1012 | `<stmt_paren_arith_ops>` | -> | - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` |
| 1013 | `<stmt_paren_arith_ops>` | -> | * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` |
| 1014 | `<stmt_paren_arith_ops>` | -> | / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` |
| 1015 | `<stmt_paren_arith_ops>` | -> | % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` |
| 1016 | `<stmt_paren_after_arith>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1017 | `<stmt_paren_after_arith>` | -> | ) `<stmt_paren_num_cont>` |
| 1018 | `<stmt_paren_neg_num>` | -> | `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` |
| 1019 | `<stmt_paren_num_after_incr>` | -> | `<stmt_paren_arith_ops>` |
| 1020 | `<stmt_paren_num_after_incr>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1021 | `<stmt_paren_num_after_incr>` | -> | ) `<stmt_paren_num_cont>` |
| 1022 | `<stmt_paren_num_cont>` | -> | `<stmt_arith_ops>` `<stmt_after_arith>` |
| 1023 | `<stmt_paren_num_cont>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` |
| 1024 | `<stmt_paren_num_cont>` | -> | `<stmt_bool_tail_opt>` |
| 1025 | `<stmt_paren_bool_tail>` | -> | && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` |
| 1026 | `<stmt_paren_bool_tail>` | -> | || `<stmt_bool_term>` `<stmt_bool_or_tail>` |
| 1027 | `<stmt_paren_bool_tail>` | -> | λ |
| 1028 | `<stmt_paren_bool_cont>` | -> | && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` |
| 1029 | `<stmt_paren_bool_cont>` | -> | || `<stmt_bool_term>` `<stmt_bool_or_tail>` |
| 1030 | `<stmt_paren_bool_cont>` | -> | λ |
| 1031 | `<stmt_paren_id_cont>` | -> | `<stmt_paren_arith_ops>` |
| 1032 | `<stmt_paren_id_cont>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1033 | `<stmt_paren_id_cont>` | -> | `<stmt_paren_postfix_nonnull>` `<stmt_paren_id_after_postfix>` |
| 1034 | `<stmt_paren_id_cont>` | -> | ++ `<stmt_paren_id_after_postfix>` |
| 1035 | `<stmt_paren_id_cont>` | -> | -- `<stmt_paren_id_after_postfix>` |
| 1036 | `<stmt_paren_id_cont>` | -> | && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` ) `<stmt_paren_any_cont>` |
| 1037 | `<stmt_paren_id_cont>` | -> | || `<stmt_bool_term>` `<stmt_bool_or_tail>` ) `<stmt_paren_any_cont>` |
| 1038 | `<stmt_paren_id_cont>` | -> | ) `<stmt_paren_any_cont>` |
| 1039 | `<stmt_paren_postfix_nonnull>` | -> | [ `<array_index>` ] `<stmt_postfix_after_arr>` |
| 1040 | `<stmt_paren_postfix_nonnull>` | -> | . id `<stmt_postfix_chain>` |
| 1041 | `<stmt_paren_postfix_nonnull>` | -> | ( `<arg_list>` ) `<stmt_postfix_chain>` |
| 1042 | `<stmt_paren_id_after_postfix>` | -> | `<stmt_paren_arith_ops>` |
| 1043 | `<stmt_paren_id_after_postfix>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` |
| 1044 | `<stmt_paren_id_after_postfix>` | -> | .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` |
| 1045 | `<stmt_paren_id_after_postfix>` | -> | && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` ) `<stmt_paren_any_cont>` |
| 1046 | `<stmt_paren_id_after_postfix>` | -> | || `<stmt_bool_term>` `<stmt_bool_or_tail>` ) `<stmt_paren_any_cont>` |
| 1047 | `<stmt_paren_id_after_postfix>` | -> | ) `<stmt_paren_any_cont>` |
| 1048 | `<stmt_paren_any_cont>` | -> | `<stmt_arith_ops>` `<stmt_after_arith>` |
| 1049 | `<stmt_paren_any_cont>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` |
| 1050 | `<stmt_paren_any_cont>` | -> | .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` |
| 1051 | `<stmt_paren_any_cont>` | -> | `<stmt_bool_tail_opt>` |
| 1052 | `<stmt_concat_tail_typed>` | -> | .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` |
| 1053 | `<stmt_concat_tail_typed>` | -> | λ |
| 1054 | `<stmt_string_operand>` | -> | stringlit |
| 1055 | `<stmt_string_operand>` | -> | charlit |
| 1056 | `<stmt_string_operand>` | -> | id |
| 1057 | `<stmt_string_operand>` | -> | string ( `<arg_expr>` ) |
| 1058 | `<stmt_string_operand>` | -> | char ( `<arg_expr>` ) |
| 1059 | `<stmt_string_operand>` | -> | ( `<stmt_string_operand>` `<stmt_concat_tail_typed>` ) |
| 1060 | `<stmt_string_operand>` | -> | intlit |
| 1061 | `<stmt_string_operand>` | -> | longlit |
| 1062 | `<stmt_string_operand>` | -> | floatlit |
| 1063 | `<stmt_string_operand>` | -> | doublelit |
| 1064 | `<stmt_string_operand>` | -> | true |
| 1065 | `<stmt_string_operand>` | -> | false |
| 1066 | `<stmt_string_operand>` | -> | int ( `<arg_expr>` ) |
| 1067 | `<stmt_string_operand>` | -> | long ( `<arg_expr>` ) |
| 1068 | `<stmt_string_operand>` | -> | float ( `<arg_expr>` ) |
| 1069 | `<stmt_string_operand>` | -> | double ( `<arg_expr>` ) |
| 1070 | `<stmt_string_operand>` | -> | bool ( `<arg_expr>` ) |
| 1071 | `<stmt_bool_term>` | -> | `<stmt_bool_eq>` `<stmt_bool_and_tail>` |
| 1072 | `<stmt_bool_and_tail>` | -> | && `<stmt_bool_eq>` `<stmt_bool_and_tail>` |
| 1073 | `<stmt_bool_and_tail>` | -> | λ |
| 1074 | `<stmt_bool_or_tail>` | -> | || `<stmt_bool_term>` `<stmt_bool_or_tail>` |
| 1075 | `<stmt_bool_or_tail>` | -> | λ |
| 1076 | `<stmt_bool_eq>` | -> | `<stmt_bool_factor>` `<stmt_bool_eq_tail>` |
| 1077 | `<stmt_bool_eq_tail>` | -> | == `<stmt_bool_factor>` `<stmt_bool_eq_tail>` |
| 1078 | `<stmt_bool_eq_tail>` | -> | != `<stmt_bool_factor>` `<stmt_bool_eq_tail>` |
| 1079 | `<stmt_bool_eq_tail>` | -> | λ |
| 1080 | `<stmt_bool_factor>` | -> | ! `<stmt_bool_factor>` |
| 1081 | `<stmt_bool_factor>` | -> | `<stmt_bool_atom>` |
| 1082 | `<stmt_bool_atom>` | -> | true |
| 1083 | `<stmt_bool_atom>` | -> | false |
| 1084 | `<stmt_bool_atom>` | -> | id `<stmt_bool_id_cont>` |
| 1085 | `<stmt_bool_atom>` | -> | intlit `<stmt_numeric_cmp_required>` |
| 1086 | `<stmt_bool_atom>` | -> | longlit `<stmt_numeric_cmp_required>` |
| 1087 | `<stmt_bool_atom>` | -> | floatlit `<stmt_numeric_cmp_required>` |
| 1088 | `<stmt_bool_atom>` | -> | doublelit `<stmt_numeric_cmp_required>` |
| 1089 | `<stmt_bool_atom>` | -> | - `<stmt_numeric_neg_cmp>` |
| 1090 | `<stmt_bool_atom>` | -> | ( `<stmt_bool_paren>` ) |
| 1091 | `<stmt_bool_atom>` | -> | int ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` |
| 1092 | `<stmt_bool_atom>` | -> | long ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` |
| 1093 | `<stmt_bool_atom>` | -> | float ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` |
| 1094 | `<stmt_bool_atom>` | -> | double ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` |
| 1095 | `<stmt_bool_id_cont>` | -> | `<stmt_numeric_arith_cmp>` |
| 1096 | `<stmt_bool_id_cont>` | -> | ++ |
| 1097 | `<stmt_bool_id_cont>` | -> | -- |
| 1098 | `<stmt_bool_id_cont>` | -> | `<stmt_postfix_chain>` |
| 1099 | `<stmt_numeric_arith_cmp>` | -> | + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1100 | `<stmt_numeric_arith_cmp>` | -> | - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1101 | `<stmt_numeric_arith_cmp>` | -> | * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1102 | `<stmt_numeric_arith_cmp>` | -> | / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1103 | `<stmt_numeric_arith_cmp>` | -> | % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1104 | `<stmt_numeric_arith_cmp>` | -> | `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1105 | `<stmt_numeric_add_cmp>` | -> | + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` |
| 1106 | `<stmt_numeric_add_cmp>` | -> | - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` |
| 1107 | `<stmt_numeric_add_cmp>` | -> | λ |
| 1108 | `<stmt_numeric_cmp_required>` | -> | `<stmt_numeric_lit_arith>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1109 | `<stmt_numeric_lit_arith>` | -> | * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` |
| 1110 | `<stmt_numeric_lit_arith>` | -> | / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` |
| 1111 | `<stmt_numeric_lit_arith>` | -> | % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` |
| 1112 | `<stmt_numeric_lit_arith>` | -> | + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` |
| 1113 | `<stmt_numeric_lit_arith>` | -> | - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` |
| 1114 | `<stmt_numeric_lit_arith>` | -> | λ |
| 1115 | `<stmt_numeric_neg_cmp>` | -> | `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` |
| 1116 | `<stmt_cmp_op>` | -> | < |
| 1117 | `<stmt_cmp_op>` | -> | > |
| 1118 | `<stmt_cmp_op>` | -> | <= |
| 1119 | `<stmt_cmp_op>` | -> | >= |
| 1120 | `<stmt_cmp_op>` | -> | == |
| 1121 | `<stmt_cmp_op>` | -> | != |
| 1122 | `<stmt_bool_paren>` | -> | `<stmt_bool_term>` `<stmt_bool_and_or_tail>` |
| 1123 | `<stmt_bool_and_or_tail>` | -> | && `<stmt_bool_term>` `<stmt_bool_and_or_tail>` |
| 1124 | `<stmt_bool_and_or_tail>` | -> | || `<stmt_bool_term>` `<stmt_bool_and_or_tail>` |
| 1125 | `<stmt_bool_and_or_tail>` | -> | λ |
| 1126 | `<numeric_mul_expr_stmt>` | -> | `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` |
| 1127 | `<numeric_mul_tail_stmt>` | -> | * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` |
| 1128 | `<numeric_mul_tail_stmt>` | -> | / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` |
| 1129 | `<numeric_mul_tail_stmt>` | -> | % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` |
| 1130 | `<numeric_mul_tail_stmt>` | -> | λ |
| 1131 | `<numeric_add_expr_stmt>` | -> | `<numeric_mul_expr_stmt>` `<numeric_add_tail_stmt>` |
| 1132 | `<numeric_add_tail_stmt>` | -> | + `<numeric_mul_expr_stmt>` `<numeric_add_tail_stmt>` |
| 1133 | `<numeric_add_tail_stmt>` | -> | - `<numeric_mul_expr_stmt>` `<numeric_add_tail_stmt>` |
| 1134 | `<numeric_add_tail_stmt>` | -> | λ |
| 1135 | `<numeric_unary_expr_stmt>` | -> | ! `<numeric_unary_expr_stmt>` |
| 1136 | `<numeric_unary_expr_stmt>` | -> | - `<numeric_unary_expr_stmt>` |
| 1137 | `<numeric_unary_expr_stmt>` | -> | `<numeric_postfix_expr_stmt>` |
| 1138 | `<numeric_postfix_expr_stmt>` | -> | ( `<arg_expr>` ) `<stmt_postfix_chain>` |
| 1139 | `<numeric_postfix_expr_stmt>` | -> | int ( `<arg_expr>` ) |
| 1140 | `<numeric_postfix_expr_stmt>` | -> | long ( `<arg_expr>` ) |
| 1141 | `<numeric_postfix_expr_stmt>` | -> | float ( `<arg_expr>` ) |
| 1142 | `<numeric_postfix_expr_stmt>` | -> | double ( `<arg_expr>` ) |
| 1143 | `<numeric_postfix_expr_stmt>` | -> | ++ id `<stmt_postfix_chain>` |
| 1144 | `<numeric_postfix_expr_stmt>` | -> | -- id `<stmt_postfix_chain>` |
| 1145 | `<numeric_postfix_expr_stmt>` | -> | id `<stmt_id_postfix>` |
| 1146 | `<numeric_postfix_expr_stmt>` | -> | intlit |
| 1147 | `<numeric_postfix_expr_stmt>` | -> | longlit |
| 1148 | `<numeric_postfix_expr_stmt>` | -> | floatlit |
| 1149 | `<numeric_postfix_expr_stmt>` | -> | doublelit |
| 1150 | `<stmt_id_postfix>` | -> | ++ |
| 1151 | `<stmt_id_postfix>` | -> | -- |
| 1152 | `<stmt_id_postfix>` | -> | `<stmt_postfix_chain>` |
| 1153 | `<stmt_postfix_chain>` | -> | `<stmt_array_access>` `<stmt_postfix_after_arr>` |
| 1154 | `<stmt_postfix_chain>` | -> | . id `<stmt_postfix_chain>` |
| 1155 | `<stmt_postfix_chain>` | -> | ( `<stmt_arg_list>` ) `<stmt_postfix_chain>` |
| 1156 | `<stmt_postfix_chain>` | -> | λ |
| 1157 | `<stmt_array_access>` | -> | [ `<stmt_array_index>` ] `<stmt_array_access_dim2>` |
| 1158 | `<stmt_array_access_dim2>` | -> | [ `<stmt_array_index>` ] |
| 1159 | `<stmt_array_access_dim2>` | -> | λ |
| 1160 | `<stmt_postfix_after_arr>` | -> | . id `<stmt_postfix_chain>` |
| 1161 | `<stmt_postfix_after_arr>` | -> | ( `<stmt_arg_list>` ) `<stmt_postfix_chain>` |
| 1162 | `<stmt_postfix_after_arr>` | -> | ++ |
| 1163 | `<stmt_postfix_after_arr>` | -> | -- |
| 1164 | `<stmt_postfix_after_arr>` | -> | λ |
| 1165 | `<stmt_array_index>` | -> | intlit |
| 1166 | `<stmt_array_index>` | -> | id |
| 1167 | `<stmt_arg_list>` | -> | `<arg_expr>` `<stmt_arg_tail>` |
| 1168 | `<stmt_arg_list>` | -> | λ |
| 1169 | `<stmt_arg_tail>` | -> | , `<arg_expr>` `<stmt_arg_tail>` |
| 1170 | `<stmt_arg_tail>` | -> | λ |
| 1171 | `<arg_expr>` | -> | `<arg_typed_rhs>` `<arg_assign_tail>` |
| 1172 | `<arg_assign_tail>` | -> | `<assign_op>` `<arg_typed_rhs>` |
| 1173 | `<arg_assign_tail>` | -> | λ |
| 1174 | `<arg_typed_rhs>` | -> | `<arg_bool_or_concat>` |
| 1175 | `<arg_bool_or_concat>` | -> | stringlit `<arg_concat_tail_typed>` |
| 1176 | `<arg_bool_or_concat>` | -> | charlit `<arg_concat_tail_typed>` |
| 1177 | `<arg_bool_or_concat>` | -> | string ( `<arg_expr>` ) `<arg_concat_tail_typed>` |
| 1178 | `<arg_bool_or_concat>` | -> | intlit `<arg_numeric_or_bool>` |
| 1179 | `<arg_bool_or_concat>` | -> | longlit `<arg_numeric_or_bool>` |
| 1180 | `<arg_bool_or_concat>` | -> | floatlit `<arg_numeric_or_bool>` |
| 1181 | `<arg_bool_or_concat>` | -> | doublelit `<arg_numeric_or_bool>` |
| 1182 | `<arg_bool_or_concat>` | -> | - `<arg_neg_numeric_or_bool>` |
| 1183 | `<arg_bool_or_concat>` | -> | true `<arg_bool_tail_opt>` |
| 1184 | `<arg_bool_or_concat>` | -> | false `<arg_bool_tail_opt>` |
| 1185 | `<arg_bool_or_concat>` | -> | ! `<arg_bool_factor>` `<arg_bool_tail_opt>` |
| 1186 | `<arg_bool_or_concat>` | -> | int ( `<arg_expr>` ) `<arg_numeric_or_bool>` |
| 1187 | `<arg_bool_or_concat>` | -> | long ( `<arg_expr>` ) `<arg_numeric_or_bool>` |
| 1188 | `<arg_bool_or_concat>` | -> | float ( `<arg_expr>` ) `<arg_numeric_or_bool>` |
| 1189 | `<arg_bool_or_concat>` | -> | double ( `<arg_expr>` ) `<arg_numeric_or_bool>` |
| 1190 | `<arg_bool_or_concat>` | -> | char ( `<arg_expr>` ) |
| 1191 | `<arg_bool_or_concat>` | -> | bool ( `<arg_expr>` ) `<arg_bool_tail_opt>` |
| 1192 | `<arg_bool_or_concat>` | -> | id `<arg_id_toplevel_cont>` |
| 1193 | `<arg_bool_or_concat>` | -> | ( `<arg_toplevel_paren>` ) `<arg_toplevel_paren_cont>` |
| 1194 | `<arg_bool_or_concat>` | -> | ++ id |
| 1195 | `<arg_bool_or_concat>` | -> | -- id |
| 1196 | `<arg_numeric_or_bool>` | -> | `<arg_arith_ops>` `<arg_after_arith>` |
| 1197 | `<arg_numeric_or_bool>` | -> | `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` |
| 1198 | `<arg_numeric_or_bool>` | -> | `<arg_bool_tail_opt>` |
| 1199 | `<arg_arith_ops>` | -> | + `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` |
| 1200 | `<arg_arith_ops>` | -> | - `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` |
| 1201 | `<arg_arith_ops>` | -> | * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` |
| 1202 | `<arg_arith_ops>` | -> | / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` |
| 1203 | `<arg_arith_ops>` | -> | % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` |
| 1204 | `<arg_numeric_add_ops>` | -> | + `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` |
| 1205 | `<arg_numeric_add_ops>` | -> | - `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` |
| 1206 | `<arg_numeric_add_ops>` | -> | λ |
| 1207 | `<arg_after_arith>` | -> | `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` |
| 1208 | `<arg_after_arith>` | -> | `<arg_bool_tail_opt>` |
| 1209 | `<arg_neg_numeric_or_bool>` | -> | `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` `<arg_after_arith>` |
| 1210 | `<arg_bool_tail_opt>` | -> | && `<arg_bool_term>` `<arg_bool_and_tail>` `<arg_bool_or_tail_opt>` |
| 1211 | `<arg_bool_tail_opt>` | -> | || `<arg_bool_term>` `<arg_bool_or_tail>` |
| 1212 | `<arg_bool_tail_opt>` | -> | λ |
| 1213 | `<arg_bool_or_tail_opt>` | -> | || `<arg_bool_term>` `<arg_bool_or_tail>` |
| 1214 | `<arg_bool_or_tail_opt>` | -> | λ |
| 1215 | `<arg_id_toplevel_cont>` | -> | `<arg_arith_ops>` `<arg_after_arith>` |
| 1216 | `<arg_id_toplevel_cont>` | -> | `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` |
| 1217 | `<arg_id_toplevel_cont>` | -> | ++ |
| 1218 | `<arg_id_toplevel_cont>` | -> | -- |
| 1219 | `<arg_id_toplevel_cont>` | -> | `<arg_postfix_chain>` `<arg_id_after_postfix>` |
| 1220 | `<arg_id_after_postfix>` | -> | `<arg_arith_ops>` `<arg_after_arith>` |
| 1221 | `<arg_id_after_postfix>` | -> | `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` |
| 1222 | `<arg_id_after_postfix>` | -> | .. `<arg_string_operand>` `<arg_concat_tail_typed>` |
| 1223 | `<arg_id_after_postfix>` | -> | `<arg_bool_tail_opt>` |
| 1224 | `<arg_toplevel_paren>` | -> | `<arg_bool_or_concat>` |
| 1225 | `<arg_toplevel_paren_cont>` | -> | `<arg_arith_ops>` `<arg_after_arith>` |
| 1226 | `<arg_toplevel_paren_cont>` | -> | `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` |
| 1227 | `<arg_toplevel_paren_cont>` | -> | .. `<arg_string_operand>` `<arg_concat_tail_typed>` |
| 1228 | `<arg_toplevel_paren_cont>` | -> | `<arg_bool_tail_opt>` |
| 1229 | `<arg_concat_tail_typed>` | -> | .. `<arg_string_operand>` `<arg_concat_tail_typed>` |
| 1230 | `<arg_concat_tail_typed>` | -> | λ |
| 1231 | `<arg_string_operand>` | -> | stringlit |
| 1232 | `<arg_string_operand>` | -> | charlit |
| 1233 | `<arg_string_operand>` | -> | id |
| 1234 | `<arg_string_operand>` | -> | string ( `<arg_expr>` ) |
| 1235 | `<arg_string_operand>` | -> | char ( `<arg_expr>` ) |
| 1236 | `<arg_string_operand>` | -> | ( `<arg_string_operand>` `<arg_concat_tail_typed>` ) |
| 1237 | `<arg_bool_term>` | -> | `<arg_bool_eq>` `<arg_bool_and_tail>` |
| 1238 | `<arg_bool_and_tail>` | -> | && `<arg_bool_eq>` `<arg_bool_and_tail>` |
| 1239 | `<arg_bool_and_tail>` | -> | λ |
| 1240 | `<arg_bool_or_tail>` | -> | || `<arg_bool_term>` `<arg_bool_or_tail>` |
| 1241 | `<arg_bool_or_tail>` | -> | λ |
| 1242 | `<arg_bool_eq>` | -> | `<arg_bool_factor>` `<arg_bool_eq_tail>` |
| 1243 | `<arg_bool_eq_tail>` | -> | == `<arg_bool_factor>` `<arg_bool_eq_tail>` |
| 1244 | `<arg_bool_eq_tail>` | -> | != `<arg_bool_factor>` `<arg_bool_eq_tail>` |
| 1245 | `<arg_bool_eq_tail>` | -> | λ |
| 1246 | `<arg_bool_factor>` | -> | ! `<arg_bool_factor>` |
| 1247 | `<arg_bool_factor>` | -> | `<arg_bool_atom>` |
| 1248 | `<arg_bool_atom>` | -> | true |
| 1249 | `<arg_bool_atom>` | -> | false |
| 1250 | `<arg_bool_atom>` | -> | id `<arg_bool_id_cont>` |
| 1251 | `<arg_bool_atom>` | -> | intlit `<arg_numeric_cmp_required>` |
| 1252 | `<arg_bool_atom>` | -> | longlit `<arg_numeric_cmp_required>` |
| 1253 | `<arg_bool_atom>` | -> | floatlit `<arg_numeric_cmp_required>` |
| 1254 | `<arg_bool_atom>` | -> | doublelit `<arg_numeric_cmp_required>` |
| 1255 | `<arg_bool_atom>` | -> | - `<arg_numeric_neg_cmp>` |
| 1256 | `<arg_bool_atom>` | -> | ( `<arg_bool_paren>` ) |
| 1257 | `<arg_bool_atom>` | -> | int ( `<arg_expr>` ) `<arg_numeric_cmp_required>` |
| 1258 | `<arg_bool_atom>` | -> | long ( `<arg_expr>` ) `<arg_numeric_cmp_required>` |
| 1259 | `<arg_bool_atom>` | -> | float ( `<arg_expr>` ) `<arg_numeric_cmp_required>` |
| 1260 | `<arg_bool_atom>` | -> | double ( `<arg_expr>` ) `<arg_numeric_cmp_required>` |
| 1261 | `<arg_bool_paren>` | -> | `<arg_bool_term>` `<arg_bool_and_or_tail>` |
| 1262 | `<arg_bool_and_or_tail>` | -> | && `<arg_bool_term>` `<arg_bool_and_or_tail>` |
| 1263 | `<arg_bool_and_or_tail>` | -> | || `<arg_bool_term>` `<arg_bool_and_or_tail>` |
| 1264 | `<arg_bool_and_or_tail>` | -> | λ |
| 1265 | `<arg_bool_id_cont>` | -> | `<arg_numeric_arith_cmp>` |
| 1266 | `<arg_bool_id_cont>` | -> | ++ |
| 1267 | `<arg_bool_id_cont>` | -> | -- |
| 1268 | `<arg_bool_id_cont>` | -> | `<arg_postfix_chain>` |
| 1269 | `<arg_numeric_arith_cmp>` | -> | + `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1270 | `<arg_numeric_arith_cmp>` | -> | - `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1271 | `<arg_numeric_arith_cmp>` | -> | * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1272 | `<arg_numeric_arith_cmp>` | -> | / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1273 | `<arg_numeric_arith_cmp>` | -> | % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1274 | `<arg_numeric_arith_cmp>` | -> | `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1275 | `<arg_numeric_add_cmp>` | -> | + `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` |
| 1276 | `<arg_numeric_add_cmp>` | -> | - `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` |
| 1277 | `<arg_numeric_add_cmp>` | -> | λ |
| 1278 | `<arg_numeric_cmp_required>` | -> | `<arg_numeric_lit_arith>` `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1279 | `<arg_numeric_lit_arith>` | -> | * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` |
| 1280 | `<arg_numeric_lit_arith>` | -> | / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` |
| 1281 | `<arg_numeric_lit_arith>` | -> | % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` |
| 1282 | `<arg_numeric_lit_arith>` | -> | + `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` |
| 1283 | `<arg_numeric_lit_arith>` | -> | - `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` |
| 1284 | `<arg_numeric_lit_arith>` | -> | λ |
| 1285 | `<arg_numeric_neg_cmp>` | -> | `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` |
| 1286 | `<arg_cmp_op>` | -> | < |
| 1287 | `<arg_cmp_op>` | -> | > |
| 1288 | `<arg_cmp_op>` | -> | <= |
| 1289 | `<arg_cmp_op>` | -> | >= |
| 1290 | `<arg_cmp_op>` | -> | == |
| 1291 | `<arg_cmp_op>` | -> | != |
| 1292 | `<numeric_mul_expr_arg>` | -> | `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` |
| 1293 | `<numeric_mul_tail_arg>` | -> | * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` |
| 1294 | `<numeric_mul_tail_arg>` | -> | / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` |
| 1295 | `<numeric_mul_tail_arg>` | -> | % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` |
| 1296 | `<numeric_mul_tail_arg>` | -> | λ |
| 1297 | `<numeric_add_expr_arg>` | -> | `<numeric_mul_expr_arg>` `<numeric_add_tail_arg>` |
| 1298 | `<numeric_add_tail_arg>` | -> | + `<numeric_mul_expr_arg>` `<numeric_add_tail_arg>` |
| 1299 | `<numeric_add_tail_arg>` | -> | - `<numeric_mul_expr_arg>` `<numeric_add_tail_arg>` |
| 1300 | `<numeric_add_tail_arg>` | -> | λ |
| 1301 | `<numeric_unary_expr_arg>` | -> | ! `<numeric_unary_expr_arg>` |
| 1302 | `<numeric_unary_expr_arg>` | -> | - `<numeric_unary_expr_arg>` |
| 1303 | `<numeric_unary_expr_arg>` | -> | `<numeric_postfix_expr_arg>` |
| 1304 | `<numeric_postfix_expr_arg>` | -> | ( `<arg_expr>` ) `<arg_postfix_chain>` |
| 1305 | `<numeric_postfix_expr_arg>` | -> | int ( `<arg_expr>` ) |
| 1306 | `<numeric_postfix_expr_arg>` | -> | long ( `<arg_expr>` ) |
| 1307 | `<numeric_postfix_expr_arg>` | -> | float ( `<arg_expr>` ) |
| 1308 | `<numeric_postfix_expr_arg>` | -> | double ( `<arg_expr>` ) |
| 1309 | `<numeric_postfix_expr_arg>` | -> | ++ id |
| 1310 | `<numeric_postfix_expr_arg>` | -> | -- id |
| 1311 | `<numeric_postfix_expr_arg>` | -> | id `<arg_id_postfix>` |
| 1312 | `<numeric_postfix_expr_arg>` | -> | intlit |
| 1313 | `<numeric_postfix_expr_arg>` | -> | longlit |
| 1314 | `<numeric_postfix_expr_arg>` | -> | floatlit |
| 1315 | `<numeric_postfix_expr_arg>` | -> | doublelit |
| 1316 | `<arg_id_postfix>` | -> | ++ |
| 1317 | `<arg_id_postfix>` | -> | -- |
| 1318 | `<arg_id_postfix>` | -> | `<arg_postfix_chain>` |
| 1319 | `<arg_postfix_chain>` | -> | `<arg_array_access>` `<arg_postfix_after_arr>` |
| 1320 | `<arg_postfix_chain>` | -> | . id `<arg_postfix_chain>` |
| 1321 | `<arg_postfix_chain>` | -> | ( `<arg_nested_list>` ) `<arg_postfix_chain>` |
| 1322 | `<arg_postfix_chain>` | -> | λ |
| 1323 | `<arg_array_access>` | -> | [ `<arg_array_index>` ] `<arg_array_access_dim2>` |
| 1324 | `<arg_array_access_dim2>` | -> | [ `<arg_array_index>` ] |
| 1325 | `<arg_array_access_dim2>` | -> | λ |
| 1326 | `<arg_postfix_after_arr>` | -> | . id `<arg_postfix_chain>` |
| 1327 | `<arg_postfix_after_arr>` | -> | ( `<arg_nested_list>` ) `<arg_postfix_chain>` |
| 1328 | `<arg_postfix_after_arr>` | -> | λ |
| 1329 | `<arg_array_index>` | -> | intlit |
| 1330 | `<arg_array_index>` | -> | id |
| 1331 | `<arg_nested_list>` | -> | `<arg_expr>` `<arg_nested_tail>` |
| 1332 | `<arg_nested_list>` | -> | λ |
| 1333 | `<arg_nested_tail>` | -> | , `<arg_expr>` `<arg_nested_tail>` |
| 1334 | `<arg_nested_tail>` | -> | λ |
| 1335 | `<io_stmt>` | -> | trap ( `<trap_target>` ) ; |
| 1336 | `<io_stmt>` | -> | thread ( `<print_args>` ) ; |
| 1337 | `<io_stmt>` | -> | threadln ( `<print_args>` ) ; |
| 1338 | `<trap_target>` | -> | id `<trap_target_tail>` |
| 1339 | `<trap_target_tail>` | -> | [ `<arg_expr>` ] |
| 1340 | `<trap_target_tail>` | -> | . id |
| 1341 | `<trap_target_tail>` | -> | λ |
| 1342 | `<print_args>` | -> | `<arg_expr>` `<print_tail>` |
| 1343 | `<print_tail>` | -> | , `<arg_expr>` `<print_tail>` |
| 1344 | `<print_tail>` | -> | λ |
| 1345 | `<ctrl_struct>` | -> | if ( `<condition>` ) { `<non_empty_ctrl_stmt_list>` } `<else_opt>` |
| 1346 | `<ctrl_struct>` | -> | switch ( `<arg_expr>` ) { `<case_list>` `<default_opt>` } |
| 1347 | `<ctrl_struct>` | -> | for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_ctrl_stmt_list>` } |
| 1348 | `<ctrl_struct>` | -> | while ( `<condition>` ) { `<non_empty_loop_ctrl_stmt_list>` } |
| 1349 | `<ctrl_struct>` | -> | do { `<non_empty_loop_ctrl_stmt_list>` } while ( `<condition>` ) ; |
| 1350 | `<ctrl_stmt_list>` | -> | `<statement_non_return>` `<ctrl_stmt_list>` |
| 1351 | `<ctrl_stmt_list>` | -> | λ |
| 1352 | `<non_empty_ctrl_stmt_list>` | -> | `<statement_non_return>` `<ctrl_stmt_list>` |
| 1353 | `<loop_statement_non_return>` | -> | `<statement_non_return>` |
| 1354 | `<loop_statement_non_return>` | -> | break ; |
| 1355 | `<loop_ctrl_stmt_list>` | -> | `<loop_statement_non_return>` `<loop_ctrl_stmt_list>` |
| 1356 | `<loop_ctrl_stmt_list>` | -> | λ |
| 1357 | `<non_empty_loop_ctrl_stmt_list>` | -> | `<loop_statement_non_return>` `<loop_ctrl_stmt_list>` |
| 1358 | `<else_opt>` | -> | else `<else_body>` |
| 1359 | `<else_opt>` | -> | λ |
| 1360 | `<else_body>` | -> | { `<non_empty_ctrl_stmt_list>` } |
| 1361 | `<else_body>` | -> | if ( `<condition>` ) { `<non_empty_ctrl_stmt_list>` } `<else_opt>` |
| 1362 | `<case_list>` | -> | case `<case_val>` : `<non_empty_loop_ctrl_stmt_list>` `<break_opt>` `<case_list>` |
| 1363 | `<case_list>` | -> | λ |
| 1364 | `<case_val>` | -> | intlit |
| 1365 | `<case_val>` | -> | longlit |
| 1366 | `<case_val>` | -> | charlit |
| 1367 | `<case_val>` | -> | true |
| 1368 | `<case_val>` | -> | false |
| 1369 | `<default_opt>` | -> | default : `<non_empty_loop_ctrl_stmt_list>` `<break_opt>` |
| 1370 | `<default_opt>` | -> | λ |
| 1371 | `<break_opt>` | -> | break ; |
| 1372 | `<break_opt>` | -> | λ |
| 1373 | `<for_init>` | -> | local var `<for_init_type>` id = `<for_init_expr>` |
| 1374 | `<for_init>` | -> | id `<for_init_assign_tail>` |
| 1375 | `<for_init>` | -> | λ |
| 1376 | `<for_init_assign_tail>` | -> | `<assign_op>` `<for_init_expr>` |
| 1377 | `<for_init_expr>` | -> | `<stmt_typed_rhs>` |
| 1378 | `<for_init_type>` | -> | int |
| 1379 | `<for_init_type>` | -> | long |
| 1380 | `<for_init_type>` | -> | float |
| 1381 | `<for_init_type>` | -> | double |
| 1382 | `<for_init_type>` | -> | char |
| 1383 | `<for_init_type>` | -> | string |
| 1384 | `<for_init_type>` | -> | bool |
| 1385 | `<for_cond>` | -> | `<condition>` |
| 1386 | `<condition>` | -> | `<cond_or>` |
| 1387 | `<cond_or>` | -> | `<cond_and>` `<cond_or_tail>` |
| 1388 | `<cond_or_tail>` | -> | || `<cond_and>` `<cond_or_tail>` |
| 1389 | `<cond_or_tail>` | -> | λ |
| 1390 | `<cond_and>` | -> | `<cond_not>` `<cond_and_tail>` |
| 1391 | `<cond_and_tail>` | -> | && `<cond_not>` `<cond_and_tail>` |
| 1392 | `<cond_and_tail>` | -> | λ |
| 1393 | `<cond_not>` | -> | ! `<cond_not>` |
| 1394 | `<cond_not>` | -> | `<cond_atom>` |
| 1395 | `<cond_atom>` | -> | true |
| 1396 | `<cond_atom>` | -> | false |
| 1397 | `<cond_atom>` | -> | id `<cond_id_cont>` |
| 1398 | `<cond_atom>` | -> | ( `<cond_paren_inner>` ) `<cond_paren_tail>` |
| 1399 | `<cond_atom>` | -> | `<cond_lit_cmp>` |
| 1400 | `<cond_atom>` | -> | ++ `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` |
| 1401 | `<cond_atom>` | -> | -- `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` |
| 1402 | `<cond_paren_inner>` | -> | `<cond_paren_start>` `<cond_paren_cont>` |
| 1403 | `<cond_paren_start>` | -> | id |
| 1404 | `<cond_paren_start>` | -> | intlit |
| 1405 | `<cond_paren_start>` | -> | longlit |
| 1406 | `<cond_paren_start>` | -> | floatlit |
| 1407 | `<cond_paren_start>` | -> | doublelit |
| 1408 | `<cond_paren_start>` | -> | true |
| 1409 | `<cond_paren_start>` | -> | false |
| 1410 | `<cond_paren_start>` | -> | ! `<cond_not>` |
| 1411 | `<cond_paren_start>` | -> | ++ `<cond_paren_unary>` |
| 1412 | `<cond_paren_start>` | -> | -- `<cond_paren_unary>` |
| 1413 | `<cond_paren_start>` | -> | - `<cond_paren_unary>` |
| 1414 | `<cond_paren_start>` | -> | ( `<cond_paren_inner>` ) |
| 1415 | `<cond_paren_cont>` | -> | `<cond_paren_arith_ops>` `<cond_paren_after_arith>` |
| 1416 | `<cond_paren_cont>` | -> | `<cond_cmp>` `<cond_rhs>` `<cond_paren_logic>` |
| 1417 | `<cond_paren_cont>` | -> | `<cond_paren_logic>` |
| 1418 | `<cond_paren_cont>` | -> | ++ `<cond_cmp>` `<cond_rhs>` `<cond_paren_logic>` |
| 1419 | `<cond_paren_cont>` | -> | ++ `<cond_paren_arith_ops>` `<cond_paren_after_arith>` |
| 1420 | `<cond_paren_cont>` | -> | -- `<cond_cmp>` `<cond_rhs>` `<cond_paren_logic>` |
| 1421 | `<cond_paren_cont>` | -> | -- `<cond_paren_arith_ops>` `<cond_paren_after_arith>` |
| 1422 | `<cond_paren_arith_ops>` | -> | + `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1423 | `<cond_paren_arith_ops>` | -> | - `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1424 | `<cond_paren_arith_ops>` | -> | * `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1425 | `<cond_paren_arith_ops>` | -> | / `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1426 | `<cond_paren_arith_ops>` | -> | % `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1427 | `<cond_paren_mul_ops>` | -> | * `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1428 | `<cond_paren_mul_ops>` | -> | / `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1429 | `<cond_paren_mul_ops>` | -> | % `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1430 | `<cond_paren_mul_ops>` | -> | + `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1431 | `<cond_paren_mul_ops>` | -> | - `<cond_paren_unary>` `<cond_paren_mul_ops>` |
| 1432 | `<cond_paren_mul_ops>` | -> | λ |
| 1433 | `<cond_paren_unary>` | -> | ++ `<cond_paren_unary>` |
| 1434 | `<cond_paren_unary>` | -> | -- `<cond_paren_unary>` |
| 1435 | `<cond_paren_unary>` | -> | - `<cond_paren_unary>` |
| 1436 | `<cond_paren_unary>` | -> | `<cond_paren_primary>` |
| 1437 | `<cond_paren_primary>` | -> | intlit |
| 1438 | `<cond_paren_primary>` | -> | longlit |
| 1439 | `<cond_paren_primary>` | -> | floatlit |
| 1440 | `<cond_paren_primary>` | -> | doublelit |
| 1441 | `<cond_paren_primary>` | -> | id `<cond_rhs_id_tail>` |
| 1442 | `<cond_paren_primary>` | -> | ( `<cond_paren_inner>` ) |
| 1443 | `<cond_paren_after_arith>` | -> | `<cond_cmp>` `<cond_rhs>` `<cond_paren_logic>` |
| 1444 | `<cond_paren_after_arith>` | -> | λ |
| 1445 | `<cond_paren_logic>` | -> | && `<cond_and>` |
| 1446 | `<cond_paren_logic>` | -> | || `<cond_or>` |
| 1447 | `<cond_paren_logic>` | -> | λ |
| 1448 | `<cond_paren_tail>` | -> | `<cond_cmp>` `<cond_rhs>` |
| 1449 | `<cond_paren_tail>` | -> | λ |
| 1450 | `<cond_id_cont>` | -> | [ `<cond_arr_index>` ] `<cond_id_arr_cont>` |
| 1451 | `<cond_id_cont>` | -> | + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1452 | `<cond_id_cont>` | -> | - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1453 | `<cond_id_cont>` | -> | * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1454 | `<cond_id_cont>` | -> | / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1455 | `<cond_id_cont>` | -> | % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1456 | `<cond_id_cont>` | -> | < `<cond_rhs>` |
| 1457 | `<cond_id_cont>` | -> | > `<cond_rhs>` |
| 1458 | `<cond_id_cont>` | -> | <= `<cond_rhs>` |
| 1459 | `<cond_id_cont>` | -> | >= `<cond_rhs>` |
| 1460 | `<cond_id_cont>` | -> | == `<cond_rhs>` |
| 1461 | `<cond_id_cont>` | -> | != `<cond_rhs>` |
| 1462 | `<cond_id_cont>` | -> | ++ `<cond_cmp>` `<cond_rhs>` |
| 1463 | `<cond_id_cont>` | -> | ++ + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1464 | `<cond_id_cont>` | -> | ++ - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1465 | `<cond_id_cont>` | -> | ++ * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1466 | `<cond_id_cont>` | -> | ++ / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1467 | `<cond_id_cont>` | -> | ++ % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1468 | `<cond_id_cont>` | -> | -- `<cond_cmp>` `<cond_rhs>` |
| 1469 | `<cond_id_cont>` | -> | -- + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1470 | `<cond_id_cont>` | -> | -- - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1471 | `<cond_id_cont>` | -> | -- * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1472 | `<cond_id_cont>` | -> | -- / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1473 | `<cond_id_cont>` | -> | -- % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1474 | `<cond_id_cont>` | -> | λ |
| 1475 | `<cond_arr_index>` | -> | `<cond_rhs>` |
| 1476 | `<cond_id_arr_cont>` | -> | [ `<cond_arr_index>` ] `<cond_id_arr_after>` |
| 1477 | `<cond_id_arr_cont>` | -> | `<cond_id_arr_after>` |
| 1478 | `<cond_id_arr_after>` | -> | + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1479 | `<cond_id_arr_after>` | -> | - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1480 | `<cond_id_arr_after>` | -> | * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1481 | `<cond_id_arr_after>` | -> | / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1482 | `<cond_id_arr_after>` | -> | % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1483 | `<cond_id_arr_after>` | -> | < `<cond_rhs>` |
| 1484 | `<cond_id_arr_after>` | -> | > `<cond_rhs>` |
| 1485 | `<cond_id_arr_after>` | -> | <= `<cond_rhs>` |
| 1486 | `<cond_id_arr_after>` | -> | >= `<cond_rhs>` |
| 1487 | `<cond_id_arr_after>` | -> | == `<cond_rhs>` |
| 1488 | `<cond_id_arr_after>` | -> | != `<cond_rhs>` |
| 1489 | `<cond_id_arr_after>` | -> | ++ `<cond_cmp>` `<cond_rhs>` |
| 1490 | `<cond_id_arr_after>` | -> | ++ + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1491 | `<cond_id_arr_after>` | -> | ++ - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1492 | `<cond_id_arr_after>` | -> | ++ * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1493 | `<cond_id_arr_after>` | -> | ++ / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1494 | `<cond_id_arr_after>` | -> | ++ % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1495 | `<cond_id_arr_after>` | -> | -- `<cond_cmp>` `<cond_rhs>` |
| 1496 | `<cond_id_arr_after>` | -> | -- + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1497 | `<cond_id_arr_after>` | -> | -- - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1498 | `<cond_id_arr_after>` | -> | -- * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1499 | `<cond_id_arr_after>` | -> | -- / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1500 | `<cond_id_arr_after>` | -> | -- % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` |
| 1501 | `<cond_id_arr_after>` | -> | λ |
| 1502 | `<cond_lit_cmp>` | -> | intlit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` |
| 1503 | `<cond_lit_cmp>` | -> | longlit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` |
| 1504 | `<cond_lit_cmp>` | -> | floatlit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` |
| 1505 | `<cond_lit_cmp>` | -> | doublelit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` |
| 1506 | `<cond_lit_cmp>` | -> | - `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` |
| 1507 | `<cond_lit_mul>` | -> | * `<cond_lit_unary>` `<cond_lit_mul>` |
| 1508 | `<cond_lit_mul>` | -> | / `<cond_lit_unary>` `<cond_lit_mul>` |
| 1509 | `<cond_lit_mul>` | -> | % `<cond_lit_unary>` `<cond_lit_mul>` |
| 1510 | `<cond_lit_mul>` | -> | λ |
| 1511 | `<cond_lit_add>` | -> | + `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` |
| 1512 | `<cond_lit_add>` | -> | - `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` |
| 1513 | `<cond_lit_add>` | -> | λ |
| 1514 | `<cond_lit_unary>` | -> | ++ `<cond_lit_unary>` |
| 1515 | `<cond_lit_unary>` | -> | -- `<cond_lit_unary>` |
| 1516 | `<cond_lit_unary>` | -> | - `<cond_lit_unary>` |
| 1517 | `<cond_lit_unary>` | -> | `<cond_lit_primary>` |
| 1518 | `<cond_lit_primary>` | -> | intlit |
| 1519 | `<cond_lit_primary>` | -> | longlit |
| 1520 | `<cond_lit_primary>` | -> | floatlit |
| 1521 | `<cond_lit_primary>` | -> | doublelit |
| 1522 | `<cond_lit_primary>` | -> | id `<cond_rhs_id_tail>` |
| 1523 | `<cond_lit_primary>` | -> | ( `<cond_lit_expr>` ) |
| 1524 | `<cond_lit_expr>` | -> | `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` |
| 1525 | `<cond_rhs>` | -> | `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` |
| 1526 | `<cond_rhs_unary>` | -> | ++ `<cond_rhs_unary>` |
| 1527 | `<cond_rhs_unary>` | -> | -- `<cond_rhs_unary>` |
| 1528 | `<cond_rhs_unary>` | -> | - `<cond_rhs_unary>` |
| 1529 | `<cond_rhs_unary>` | -> | `<cond_rhs_primary>` |
| 1530 | `<cond_rhs_primary>` | -> | intlit |
| 1531 | `<cond_rhs_primary>` | -> | longlit |
| 1532 | `<cond_rhs_primary>` | -> | floatlit |
| 1533 | `<cond_rhs_primary>` | -> | doublelit |
| 1534 | `<cond_rhs_primary>` | -> | id `<cond_rhs_id_tail>` |
| 1535 | `<cond_rhs_primary>` | -> | ( `<cond_rhs>` ) |
| 1536 | `<cond_rhs_id_tail>` | -> | [ `<cond_arr_index>` ] `<cond_rhs_arr_tail>` |
| 1537 | `<cond_rhs_id_tail>` | -> | ++ |
| 1538 | `<cond_rhs_id_tail>` | -> | -- |
| 1539 | `<cond_rhs_id_tail>` | -> | λ |
| 1540 | `<cond_rhs_arr_tail>` | -> | [ `<cond_arr_index>` ] |
| 1541 | `<cond_rhs_arr_tail>` | -> | [ `<cond_arr_index>` ] ++ |
| 1542 | `<cond_rhs_arr_tail>` | -> | [ `<cond_arr_index>` ] -- |
| 1543 | `<cond_rhs_arr_tail>` | -> | ++ |
| 1544 | `<cond_rhs_arr_tail>` | -> | -- |
| 1545 | `<cond_rhs_arr_tail>` | -> | λ |
| 1546 | `<cond_rhs_mul>` | -> | * `<cond_rhs_unary>` `<cond_rhs_mul>` |
| 1547 | `<cond_rhs_mul>` | -> | / `<cond_rhs_unary>` `<cond_rhs_mul>` |
| 1548 | `<cond_rhs_mul>` | -> | % `<cond_rhs_unary>` `<cond_rhs_mul>` |
| 1549 | `<cond_rhs_mul>` | -> | λ |
| 1550 | `<cond_rhs_add>` | -> | + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` |
| 1551 | `<cond_rhs_add>` | -> | - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` |
| 1552 | `<cond_rhs_add>` | -> | λ |
| 1553 | `<cond_cmp>` | -> | < |
| 1554 | `<cond_cmp>` | -> | > |
| 1555 | `<cond_cmp>` | -> | <= |
| 1556 | `<cond_cmp>` | -> | >= |
| 1557 | `<cond_cmp>` | -> | == |
| 1558 | `<cond_cmp>` | -> | != |
| 1559 | `<for_update>` | -> | id `<for_update_tail>` |
| 1560 | `<for_update>` | -> | ++ id |
| 1561 | `<for_update>` | -> | -- id |
| 1562 | `<for_update>` | -> | λ |
| 1563 | `<for_update_tail>` | -> | ++ |
| 1564 | `<for_update_tail>` | -> | -- |
| 1565 | `<for_update_tail>` | -> | `<assign_op>` `<arg_expr>` |
| 1566 | `<main_body>` | -> | `<main_content>` |
| 1567 | `<main_content>` | -> | using id `<using_cont>` ; `<main_content>` |
| 1568 | `<main_content>` | -> | local `<mutability>` `<local_dec_body>` `<main_content>` |
| 1569 | `<main_content>` | -> | `<statement_non_return>` `<main_content>` |
| 1570 | `<main_content>` | -> | return intlit ; |