## PREDICT Set

| # | Production | Calculation | PREDICT Set |
|---|------------|-------------|-------------|
| 1 | `<program>` → `<global_section>` | FIRST(`<global_section>`) | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 2 | `<global_section>` → `<global_decl>` `<global_section>` | FIRST(`<global_decl>`) | { global } |
| 3 | `<global_section>` → int id `<int_array_with_init>` ; `<global_section>` | FIRST(int) | { int } |
| 4 | `<global_section>` → long id `<long_array_with_init>` ; `<global_section>` | FIRST(long) | { long } |
| 5 | `<global_section>` → float id `<float_array_with_init>` ; `<global_section>` | FIRST(float) | { float } |
| 6 | `<global_section>` → double id `<double_array_with_init>` ; `<global_section>` | FIRST(double) | { double } |
| 7 | `<global_section>` → char id `<char_array_with_init>` ; `<global_section>` | FIRST(char) | { char } |
| 8 | `<global_section>` → string id `<string_array_with_init>` ; `<global_section>` | FIRST(string) | { string } |
| 9 | `<global_section>` → bool id `<bool_array_with_init>` ; `<global_section>` | FIRST(bool) | { bool } |
| 10 | `<global_section>` → weave id { `<field_list>` } ; `<global_section>` | FIRST(weave) | { weave } |
| 11 | `<global_section>` → id `<weave_inst_decl>` `<global_section>` | FIRST(id) | { id } |
| 12 | `<global_section>` → `<function_decl>` `<func_and_main>` | FIRST(`<function_decl>`) | { func } |
| 13 | `<global_section>` → int main ( ) { `<main_body>` } | FIRST(int) | { int } |
| 14 | `<func_and_main>` → `<function_decl>` `<func_and_main>` | FIRST(`<function_decl>`) | { func } |
| 15 | `<func_and_main>` → int main ( ) { `<main_body>` } | FIRST(int) | { int } |
| 16 | `<global_decl>` → global `<mutability>` int id = intlit `<int_global_cont>` ; | FIRST(global) | { global } |
| 17 | `<global_decl>` → global `<mutability>` long id = longlit `<long_global_cont>` ; | FIRST(global) | { global } |
| 18 | `<global_decl>` → global `<mutability>` float id = floatlit `<float_global_cont>` ; | FIRST(global) | { global } |
| 19 | `<global_decl>` → global `<mutability>` double id = doublelit `<double_global_cont>` ; | FIRST(global) | { global } |
| 20 | `<global_decl>` → global `<mutability>` char id = charlit `<char_global_cont>` ; | FIRST(global) | { global } |
| 21 | `<global_decl>` → global `<mutability>` string id = stringlit `<string_global_cont>` ; | FIRST(global) | { global } |
| 22 | `<global_decl>` → global `<mutability>` bool id = `<bool_lit>` `<bool_global_cont>` ; | FIRST(global) | { global } |
| 23 | `<function_decl>` → func int `<func_ret_int>` | FIRST(func) | { func } |
| 24 | `<function_decl>` → func long `<func_ret_long>` | FIRST(func) | { func } |
| 25 | `<function_decl>` → func float `<func_ret_float>` | FIRST(func) | { func } |
| 26 | `<function_decl>` → func double `<func_ret_double>` | FIRST(func) | { func } |
| 27 | `<function_decl>` → func char `<func_ret_char>` | FIRST(func) | { func } |
| 28 | `<function_decl>` → func string `<func_ret_string>` | FIRST(func) | { func } |
| 29 | `<function_decl>` → func bool `<func_ret_bool>` | FIRST(func) | { func } |
| 30 | `<function_decl>` → func id `<func_ret_weave>` | FIRST(func) | { func } |
| 31 | `<function_decl>` → func void id ( ) { `<function_body_void>` } | FIRST(func) | { func } |
| 32 | `<bool_lit>` → true | FIRST(true) | { true } |
| 33 | `<bool_lit>` → false | FIRST(false) | { false } |
| 34 | `<int_global_cont>` → , id = intlit `<int_global_cont>` | FIRST(,) | { , } |
| 35 | `<int_global_cont>` → λ | FOLLOW(`<int_global_cont>`) | { ; } |
| 36 | `<long_global_cont>` → , id = longlit `<long_global_cont>` | FIRST(,) | { , } |
| 37 | `<long_global_cont>` → λ | FOLLOW(`<long_global_cont>`) | { ; } |
| 38 | `<float_global_cont>` → , id = floatlit `<float_global_cont>` | FIRST(,) | { , } |
| 39 | `<float_global_cont>` → λ | FOLLOW(`<float_global_cont>`) | { ; } |
| 40 | `<double_global_cont>` → , id = doublelit `<double_global_cont>` | FIRST(,) | { , } |
| 41 | `<double_global_cont>` → λ | FOLLOW(`<double_global_cont>`) | { ; } |
| 42 | `<char_global_cont>` → , id = charlit `<char_global_cont>` | FIRST(,) | { , } |
| 43 | `<char_global_cont>` → λ | FOLLOW(`<char_global_cont>`) | { ; } |
| 44 | `<string_global_cont>` → , id = stringlit `<string_global_cont>` | FIRST(,) | { , } |
| 45 | `<string_global_cont>` → λ | FOLLOW(`<string_global_cont>`) | { ; } |
| 46 | `<bool_global_cont>` → , id = `<bool_lit>` `<bool_global_cont>` | FIRST(,) | { , } |
| 47 | `<bool_global_cont>` → λ | FOLLOW(`<bool_global_cont>`) | { ; } |
| 48 | `<weave_inst_decl>` → id `<weave_inst_tail>` `<weave_inst_cont>` ; | FIRST(id) | { id } |
| 49 | `<weave_inst_decl>` → `<weave_array_with_init>` `<weave_arr_cont>` ; | FIRST(`<weave_array_with_init>`) | { [ } |
| 50 | `<weave_inst_tail>` → = { `<weave_field_value>` `<weave_field_list_tail>` } | FIRST(=) | { = } |
| 51 | `<weave_inst_tail>` → `<weave_array_with_init>` | FIRST(`<weave_array_with_init>`) | { [ } |
| 52 | `<weave_field_value>` → intlit | FIRST(intlit) | { intlit } |
| 53 | `<weave_field_value>` → longlit | FIRST(longlit) | { longlit } |
| 54 | `<weave_field_value>` → floatlit | FIRST(floatlit) | { floatlit } |
| 55 | `<weave_field_value>` → doublelit | FIRST(doublelit) | { doublelit } |
| 56 | `<weave_field_value>` → charlit | FIRST(charlit) | { charlit } |
| 57 | `<weave_field_value>` → stringlit | FIRST(stringlit) | { stringlit } |
| 58 | `<weave_field_value>` → true | FIRST(true) | { true } |
| 59 | `<weave_field_value>` → false | FIRST(false) | { false } |
| 60 | `<weave_field_value>` → { `<weave_value_list>` } | FIRST({) | { { } |
| 61 | `<weave_value_list>` → `<weave_field_value>` `<weave_value_tail>` | FIRST(`<weave_field_value>`) | { charlit, doublelit, false, floatlit, intlit, longlit, stringlit, true, { } |
| 62 | `<weave_value_tail>` → , `<weave_field_value>` `<weave_value_tail>` | FIRST(,) | { , } |
| 63 | `<weave_value_tail>` → λ | FOLLOW(`<weave_value_tail>`) | { } } |
| 64 | `<weave_field_list_tail>` → , `<weave_field_value>` `<weave_field_list_tail>` | FIRST(,) | { , } |
| 65 | `<weave_field_list_tail>` → λ | FOLLOW(`<weave_field_list_tail>`) | { } } |
| 66 | `<weave_inst_cont>` → , id `<weave_inst_tail>` `<weave_inst_cont>` | FIRST(,) | { , } |
| 67 | `<weave_inst_cont>` → λ | FOLLOW(`<weave_inst_cont>`) | { ; } |
| 68 | `<weave_arr_cont>` → , id `<weave_array_with_init>` `<weave_arr_cont>` | FIRST(,) | { , } |
| 69 | `<weave_arr_cont>` → λ | FOLLOW(`<weave_arr_cont>`) | { ; } |
| 70 | `<weave_array_with_init>` → [ `<size>` ] `<weave_array_init_tail>` | FIRST([) | { [ } |
| 71 | `<weave_array_init_tail>` → [ `<size>` ] `<weave_arr_init_opt_2d>` | FIRST([) | { [ } |
| 72 | `<weave_array_init_tail>` → `<weave_arr_init_opt_1d>` | FIRST(`<weave_arr_init_opt_1d>`) | { ,, ;, = } |
| 73 | `<weave_arr_init_opt_1d>` → = { `<weave_arr_init_content_1d>` } | FIRST(=) | { = } |
| 74 | `<weave_arr_init_opt_1d>` → λ | FOLLOW(`<weave_arr_init_opt_1d>`) | { ,, ; } |
| 75 | `<weave_arr_init_content_1d>` → { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_init_1d_tail>` | FIRST({) | { { } |
| 76 | `<weave_init_1d_tail>` → , { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_init_1d_tail>` | FIRST(,) | { , } |
| 77 | `<weave_init_1d_tail>` → λ | FOLLOW(`<weave_init_1d_tail>`) | { } } |
| 78 | `<weave_arr_init_opt_2d>` → = { `<weave_arr_init_content_2d>` } | FIRST(=) | { = } |
| 79 | `<weave_arr_init_opt_2d>` → λ | FOLLOW(`<weave_arr_init_opt_2d>`) | { ,, ; } |
| 80 | `<weave_arr_init_content_2d>` → { `<weave_init_row>` } `<weave_init_2d_tail>` | FIRST({) | { { } |
| 81 | `<weave_init_row>` → { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_init_1d_tail>` | FIRST({) | { { } |
| 82 | `<weave_init_2d_tail>` → , { `<weave_init_row>` } `<weave_init_2d_tail>` | FIRST(,) | { , } |
| 83 | `<weave_init_2d_tail>` → λ | FOLLOW(`<weave_init_2d_tail>`) | { } } |
| 84 | `<mutability>` → var | FIRST(var) | { var } |
| 85 | `<mutability>` → const | FIRST(const) | { const } |
| 86 | `<array_dims>` → [ `<size>` ] `<array_dim2_opt>` | FIRST([) | { [ } |
| 87 | `<array_dim2_opt>` → [ `<size>` ] | FIRST([) | { [ } |
| 88 | `<array_dim2_opt>` → λ | FOLLOW(`<array_dim2_opt>`) | { ), ,, ;, id } |
| 89 | `<size>` → intlit | FIRST(intlit) | { intlit } |
| 90 | `<size>` → id | FIRST(id) | { id } |
| 91 | `<int_array_with_init>` → [ `<size>` ] `<int_array_init_tail>` | FIRST([) | { [ } |
| 92 | `<int_array_init_tail>` → [ `<size>` ] `<int_arr_init_opt_2d>` | FIRST([) | { [ } |
| 93 | `<int_array_init_tail>` → `<int_arr_init_opt_1d>` | FIRST(`<int_arr_init_opt_1d>`) | { ;, = } |
| 94 | `<int_arr_init_opt_1d>` → = { `<int_arr_init_content_1d>` } | FIRST(=) | { = } |
| 95 | `<int_arr_init_opt_1d>` → λ | FOLLOW(`<int_arr_init_opt_1d>`) | { ; } |
| 96 | `<int_arr_init_content_1d>` → intlit `<int_elem_1d_tail>` | FIRST(intlit) | { intlit } |
| 97 | `<int_elem_1d_tail>` → , intlit `<int_elem_1d_tail>` | FIRST(,) | { , } |
| 98 | `<int_elem_1d_tail>` → λ | FOLLOW(`<int_elem_1d_tail>`) | { } } |
| 99 | `<int_arr_init_opt_2d>` → = { `<int_arr_init_content_2d>` } | FIRST(=) | { = } |
| 100 | `<int_arr_init_opt_2d>` → λ | FOLLOW(`<int_arr_init_opt_2d>`) | { ; } |
| 101 | `<int_arr_init_content_2d>` → { `<int_elem_list>` } `<int_elem_2d_tail>` | FIRST({) | { { } |
| 102 | `<int_elem_list>` → intlit `<int_elem_1d_tail>` | FIRST(intlit) | { intlit } |
| 103 | `<int_elem_2d_tail>` → , { `<int_elem_list>` } `<int_elem_2d_tail>` | FIRST(,) | { , } |
| 104 | `<int_elem_2d_tail>` → λ | FOLLOW(`<int_elem_2d_tail>`) | { } } |
| 105 | `<long_array_with_init>` → [ `<size>` ] `<long_array_init_tail>` | FIRST([) | { [ } |
| 106 | `<long_array_init_tail>` → [ `<size>` ] `<long_arr_init_opt_2d>` | FIRST([) | { [ } |
| 107 | `<long_array_init_tail>` → `<long_arr_init_opt_1d>` | FIRST(`<long_arr_init_opt_1d>`) | { ;, = } |
| 108 | `<long_arr_init_opt_1d>` → = { `<long_arr_init_content_1d>` } | FIRST(=) | { = } |
| 109 | `<long_arr_init_opt_1d>` → λ | FOLLOW(`<long_arr_init_opt_1d>`) | { ; } |
| 110 | `<long_arr_init_content_1d>` → longlit `<long_elem_1d_tail>` | FIRST(longlit) | { longlit } |
| 111 | `<long_elem_1d_tail>` → , longlit `<long_elem_1d_tail>` | FIRST(,) | { , } |
| 112 | `<long_elem_1d_tail>` → λ | FOLLOW(`<long_elem_1d_tail>`) | { } } |
| 113 | `<long_arr_init_opt_2d>` → = { `<long_arr_init_content_2d>` } | FIRST(=) | { = } |
| 114 | `<long_arr_init_opt_2d>` → λ | FOLLOW(`<long_arr_init_opt_2d>`) | { ; } |
| 115 | `<long_arr_init_content_2d>` → { `<long_elem_list>` } `<long_elem_2d_tail>` | FIRST({) | { { } |
| 116 | `<long_elem_list>` → longlit `<long_elem_1d_tail>` | FIRST(longlit) | { longlit } |
| 117 | `<long_elem_2d_tail>` → , { `<long_elem_list>` } `<long_elem_2d_tail>` | FIRST(,) | { , } |
| 118 | `<long_elem_2d_tail>` → λ | FOLLOW(`<long_elem_2d_tail>`) | { } } |
| 119 | `<float_array_with_init>` → [ `<size>` ] `<float_array_init_tail>` | FIRST([) | { [ } |
| 120 | `<float_array_init_tail>` → [ `<size>` ] `<float_arr_init_opt_2d>` | FIRST([) | { [ } |
| 121 | `<float_array_init_tail>` → `<float_arr_init_opt_1d>` | FIRST(`<float_arr_init_opt_1d>`) | { ;, = } |
| 122 | `<float_arr_init_opt_1d>` → = { `<float_arr_init_content_1d>` } | FIRST(=) | { = } |
| 123 | `<float_arr_init_opt_1d>` → λ | FOLLOW(`<float_arr_init_opt_1d>`) | { ; } |
| 124 | `<float_arr_init_content_1d>` → floatlit `<float_elem_1d_tail>` | FIRST(floatlit) | { floatlit } |
| 125 | `<float_elem_1d_tail>` → , floatlit `<float_elem_1d_tail>` | FIRST(,) | { , } |
| 126 | `<float_elem_1d_tail>` → λ | FOLLOW(`<float_elem_1d_tail>`) | { } } |
| 127 | `<float_arr_init_opt_2d>` → = { `<float_arr_init_content_2d>` } | FIRST(=) | { = } |
| 128 | `<float_arr_init_opt_2d>` → λ | FOLLOW(`<float_arr_init_opt_2d>`) | { ; } |
| 129 | `<float_arr_init_content_2d>` → { `<float_elem_list>` } `<float_elem_2d_tail>` | FIRST({) | { { } |
| 130 | `<float_elem_list>` → floatlit `<float_elem_1d_tail>` | FIRST(floatlit) | { floatlit } |
| 131 | `<float_elem_2d_tail>` → , { `<float_elem_list>` } `<float_elem_2d_tail>` | FIRST(,) | { , } |
| 132 | `<float_elem_2d_tail>` → λ | FOLLOW(`<float_elem_2d_tail>`) | { } } |
| 133 | `<double_array_with_init>` → [ `<size>` ] `<double_array_init_tail>` | FIRST([) | { [ } |
| 134 | `<double_array_init_tail>` → [ `<size>` ] `<double_arr_init_opt_2d>` | FIRST([) | { [ } |
| 135 | `<double_array_init_tail>` → `<double_arr_init_opt_1d>` | FIRST(`<double_arr_init_opt_1d>`) | { ;, = } |
| 136 | `<double_arr_init_opt_1d>` → = { `<double_arr_init_content_1d>` } | FIRST(=) | { = } |
| 137 | `<double_arr_init_opt_1d>` → λ | FOLLOW(`<double_arr_init_opt_1d>`) | { ; } |
| 138 | `<double_arr_init_content_1d>` → doublelit `<double_elem_1d_tail>` | FIRST(doublelit) | { doublelit } |
| 139 | `<double_elem_1d_tail>` → , doublelit `<double_elem_1d_tail>` | FIRST(,) | { , } |
| 140 | `<double_elem_1d_tail>` → λ | FOLLOW(`<double_elem_1d_tail>`) | { } } |
| 141 | `<double_arr_init_opt_2d>` → = { `<double_arr_init_content_2d>` } | FIRST(=) | { = } |
| 142 | `<double_arr_init_opt_2d>` → λ | FOLLOW(`<double_arr_init_opt_2d>`) | { ; } |
| 143 | `<double_arr_init_content_2d>` → { `<double_elem_list>` } `<double_elem_2d_tail>` | FIRST({) | { { } |
| 144 | `<double_elem_list>` → doublelit `<double_elem_1d_tail>` | FIRST(doublelit) | { doublelit } |
| 145 | `<double_elem_2d_tail>` → , { `<double_elem_list>` } `<double_elem_2d_tail>` | FIRST(,) | { , } |
| 146 | `<double_elem_2d_tail>` → λ | FOLLOW(`<double_elem_2d_tail>`) | { } } |
| 147 | `<char_array_with_init>` → [ `<size>` ] `<char_array_init_tail>` | FIRST([) | { [ } |
| 148 | `<char_array_init_tail>` → [ `<size>` ] `<char_arr_init_opt_2d>` | FIRST([) | { [ } |
| 149 | `<char_array_init_tail>` → `<char_arr_init_opt_1d>` | FIRST(`<char_arr_init_opt_1d>`) | { ;, = } |
| 150 | `<char_arr_init_opt_1d>` → = { `<char_arr_init_content_1d>` } | FIRST(=) | { = } |
| 151 | `<char_arr_init_opt_1d>` → λ | FOLLOW(`<char_arr_init_opt_1d>`) | { ; } |
| 152 | `<char_arr_init_content_1d>` → charlit `<char_elem_1d_tail>` | FIRST(charlit) | { charlit } |
| 153 | `<char_elem_1d_tail>` → , charlit `<char_elem_1d_tail>` | FIRST(,) | { , } |
| 154 | `<char_elem_1d_tail>` → λ | FOLLOW(`<char_elem_1d_tail>`) | { } } |
| 155 | `<char_arr_init_opt_2d>` → = { `<char_arr_init_content_2d>` } | FIRST(=) | { = } |
| 156 | `<char_arr_init_opt_2d>` → λ | FOLLOW(`<char_arr_init_opt_2d>`) | { ; } |
| 157 | `<char_arr_init_content_2d>` → { `<char_elem_list>` } `<char_elem_2d_tail>` | FIRST({) | { { } |
| 158 | `<char_elem_list>` → charlit `<char_elem_1d_tail>` | FIRST(charlit) | { charlit } |
| 159 | `<char_elem_2d_tail>` → , { `<char_elem_list>` } `<char_elem_2d_tail>` | FIRST(,) | { , } |
| 160 | `<char_elem_2d_tail>` → λ | FOLLOW(`<char_elem_2d_tail>`) | { } } |
| 161 | `<string_array_with_init>` → [ `<size>` ] `<string_array_init_tail>` | FIRST([) | { [ } |
| 162 | `<string_array_init_tail>` → [ `<size>` ] `<string_arr_init_opt_2d>` | FIRST([) | { [ } |
| 163 | `<string_array_init_tail>` → `<string_arr_init_opt_1d>` | FIRST(`<string_arr_init_opt_1d>`) | { ;, = } |
| 164 | `<string_arr_init_opt_1d>` → = { `<string_arr_init_content_1d>` } | FIRST(=) | { = } |
| 165 | `<string_arr_init_opt_1d>` → λ | FOLLOW(`<string_arr_init_opt_1d>`) | { ; } |
| 166 | `<string_arr_init_content_1d>` → stringlit `<string_elem_1d_tail>` | FIRST(stringlit) | { stringlit } |
| 167 | `<string_elem_1d_tail>` → , stringlit `<string_elem_1d_tail>` | FIRST(,) | { , } |
| 168 | `<string_elem_1d_tail>` → λ | FOLLOW(`<string_elem_1d_tail>`) | { } } |
| 169 | `<string_arr_init_opt_2d>` → = { `<string_arr_init_content_2d>` } | FIRST(=) | { = } |
| 170 | `<string_arr_init_opt_2d>` → λ | FOLLOW(`<string_arr_init_opt_2d>`) | { ; } |
| 171 | `<string_arr_init_content_2d>` → { `<string_elem_list>` } `<string_elem_2d_tail>` | FIRST({) | { { } |
| 172 | `<string_elem_list>` → stringlit `<string_elem_1d_tail>` | FIRST(stringlit) | { stringlit } |
| 173 | `<string_elem_2d_tail>` → , { `<string_elem_list>` } `<string_elem_2d_tail>` | FIRST(,) | { , } |
| 174 | `<string_elem_2d_tail>` → λ | FOLLOW(`<string_elem_2d_tail>`) | { } } |
| 175 | `<bool_array_with_init>` → [ `<size>` ] `<bool_array_init_tail>` | FIRST([) | { [ } |
| 176 | `<bool_array_init_tail>` → [ `<size>` ] `<bool_arr_init_opt_2d>` | FIRST([) | { [ } |
| 177 | `<bool_array_init_tail>` → `<bool_arr_init_opt_1d>` | FIRST(`<bool_arr_init_opt_1d>`) | { ;, = } |
| 178 | `<bool_arr_init_opt_1d>` → = { `<bool_arr_init_content_1d>` } | FIRST(=) | { = } |
| 179 | `<bool_arr_init_opt_1d>` → λ | FOLLOW(`<bool_arr_init_opt_1d>`) | { ; } |
| 180 | `<bool_arr_init_content_1d>` → `<bool_lit>` `<bool_elem_1d_tail>` | FIRST(`<bool_lit>`) | { false, true } |
| 181 | `<bool_elem_1d_tail>` → , `<bool_lit>` `<bool_elem_1d_tail>` | FIRST(,) | { , } |
| 182 | `<bool_elem_1d_tail>` → λ | FOLLOW(`<bool_elem_1d_tail>`) | { } } |
| 183 | `<bool_arr_init_opt_2d>` → = { `<bool_arr_init_content_2d>` } | FIRST(=) | { = } |
| 184 | `<bool_arr_init_opt_2d>` → λ | FOLLOW(`<bool_arr_init_opt_2d>`) | { ; } |
| 185 | `<bool_arr_init_content_2d>` → { `<bool_elem_list>` } `<bool_elem_2d_tail>` | FIRST({) | { { } |
| 186 | `<bool_elem_list>` → `<bool_lit>` `<bool_elem_1d_tail>` | FIRST(`<bool_lit>`) | { false, true } |
| 187 | `<bool_elem_2d_tail>` → , { `<bool_elem_list>` } `<bool_elem_2d_tail>` | FIRST(,) | { , } |
| 188 | `<bool_elem_2d_tail>` → λ | FOLLOW(`<bool_elem_2d_tail>`) | { } } |
| 189 | `<field_list>` → `<field_dec>` `<field_list>` | FIRST(`<field_dec>`) | { bool, char, double, float, id, int, long, string } |
| 190 | `<field_list>` → λ | FOLLOW(`<field_list>`) | { } } |
| 191 | `<field_dec>` → `<field_type>` id `<field_arr_opt>` `<field_cont>` ; | FIRST(`<field_type>`) | { bool, char, double, float, id, int, long, string } |
| 192 | `<field_type>` → int | FIRST(int) | { int } |
| 193 | `<field_type>` → long | FIRST(long) | { long } |
| 194 | `<field_type>` → float | FIRST(float) | { float } |
| 195 | `<field_type>` → double | FIRST(double) | { double } |
| 196 | `<field_type>` → char | FIRST(char) | { char } |
| 197 | `<field_type>` → string | FIRST(string) | { string } |
| 198 | `<field_type>` → bool | FIRST(bool) | { bool } |
| 199 | `<field_type>` → id | FIRST(id) | { id } |
| 200 | `<field_arr_opt>` → `<array_dims>` | FIRST(`<array_dims>`) | { [ } |
| 201 | `<field_arr_opt>` → λ | FOLLOW(`<field_arr_opt>`) | { ,, ; } |
| 202 | `<field_cont>` → , id `<field_arr_opt>` `<field_cont>` | FIRST(,) | { , } |
| 203 | `<field_cont>` → λ | FOLLOW(`<field_cont>`) | { ; } |
| 204 | `<func_ret_int>` → id ( `<param_list>` ) { `<function_body_int>` } | FIRST(id) | { id } |
| 205 | `<func_ret_int>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 206 | `<func_ret_long>` → id ( `<param_list>` ) { `<function_body_long>` } | FIRST(id) | { id } |
| 207 | `<func_ret_long>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 208 | `<func_ret_float>` → id ( `<param_list>` ) { `<function_body_float>` } | FIRST(id) | { id } |
| 209 | `<func_ret_float>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 210 | `<func_ret_double>` → id ( `<param_list>` ) { `<function_body_double>` } | FIRST(id) | { id } |
| 211 | `<func_ret_double>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 212 | `<func_ret_char>` → id ( `<param_list>` ) { `<function_body_char>` } | FIRST(id) | { id } |
| 213 | `<func_ret_char>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 214 | `<func_ret_string>` → id ( `<param_list>` ) { `<function_body_string>` } | FIRST(id) | { id } |
| 215 | `<func_ret_string>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 216 | `<func_ret_bool>` → id ( `<param_list>` ) { `<function_body_bool>` } | FIRST(id) | { id } |
| 217 | `<func_ret_bool>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 218 | `<func_ret_weave>` → id ( `<param_list>` ) { `<function_body_weave>` } | FIRST(id) | { id } |
| 219 | `<func_ret_weave>` → `<array_dims>` id ( `<param_list>` ) { `<function_body_array>` } | FIRST(`<array_dims>`) | { [ } |
| 220 | `<func_ret_weave>` → . id id ( `<param_list>` ) { `<function_body_weave>` } | FIRST(.) | { . } |
| 221 | `<param_list>` → `<param_type>` id `<param_arr_opt>` `<param_cont>` | FIRST(`<param_type>`) | { bool, char, double, float, id, int, long, string } |
| 222 | `<param_list>` → λ | FOLLOW(`<param_list>`) | { ) } |
| 223 | `<param_type>` → int | FIRST(int) | { int } |
| 224 | `<param_type>` → long | FIRST(long) | { long } |
| 225 | `<param_type>` → float | FIRST(float) | { float } |
| 226 | `<param_type>` → double | FIRST(double) | { double } |
| 227 | `<param_type>` → char | FIRST(char) | { char } |
| 228 | `<param_type>` → string | FIRST(string) | { string } |
| 229 | `<param_type>` → bool | FIRST(bool) | { bool } |
| 230 | `<param_type>` → id | FIRST(id) | { id } |
| 231 | `<param_arr_opt>` → `<array_dims>` | FIRST(`<array_dims>`) | { [ } |
| 232 | `<param_arr_opt>` → λ | FOLLOW(`<param_arr_opt>`) | { ), , } |
| 233 | `<param_cont>` → , `<param_type>` id `<param_arr_opt>` `<param_cont>` | FIRST(,) | { , } |
| 234 | `<param_cont>` → λ | FOLLOW(`<param_cont>`) | { ) } |
| 235 | `<function_body_int>` → `<func_content_int>` | FIRST(`<func_content_int>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 236 | `<func_content_int>` → using id `<using_cont>` ; `<func_content_int>` | FIRST(using) | { using } |
| 237 | `<func_content_int>` → local `<mutability>` `<local_dec_body>` `<func_content_int>` | FIRST(local) | { local } |
| 238 | `<func_content_int>` → `<statement_int_no_ret>` `<func_content_int>` | FIRST(`<statement_int_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 239 | `<func_content_int>` → `<mandatory_int_return>` | FIRST(`<mandatory_int_return>`) | { return } |
| 240 | `<mandatory_int_return>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 241 | `<function_body_long>` → `<func_content_long>` | FIRST(`<func_content_long>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 242 | `<func_content_long>` → using id `<using_cont>` ; `<func_content_long>` | FIRST(using) | { using } |
| 243 | `<func_content_long>` → local `<mutability>` `<local_dec_body>` `<func_content_long>` | FIRST(local) | { local } |
| 244 | `<func_content_long>` → `<statement_long_no_ret>` `<func_content_long>` | FIRST(`<statement_long_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 245 | `<func_content_long>` → `<mandatory_long_return>` | FIRST(`<mandatory_long_return>`) | { return } |
| 246 | `<mandatory_long_return>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 247 | `<function_body_float>` → `<func_content_float>` | FIRST(`<func_content_float>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 248 | `<func_content_float>` → using id `<using_cont>` ; `<func_content_float>` | FIRST(using) | { using } |
| 249 | `<func_content_float>` → local `<mutability>` `<local_dec_body>` `<func_content_float>` | FIRST(local) | { local } |
| 250 | `<func_content_float>` → `<statement_float_no_ret>` `<func_content_float>` | FIRST(`<statement_float_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 251 | `<func_content_float>` → `<mandatory_float_return>` | FIRST(`<mandatory_float_return>`) | { return } |
| 252 | `<mandatory_float_return>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 253 | `<function_body_double>` → `<func_content_double>` | FIRST(`<func_content_double>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 254 | `<func_content_double>` → using id `<using_cont>` ; `<func_content_double>` | FIRST(using) | { using } |
| 255 | `<func_content_double>` → local `<mutability>` `<local_dec_body>` `<func_content_double>` | FIRST(local) | { local } |
| 256 | `<func_content_double>` → `<statement_double_no_ret>` `<func_content_double>` | FIRST(`<statement_double_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 257 | `<func_content_double>` → `<mandatory_double_return>` | FIRST(`<mandatory_double_return>`) | { return } |
| 258 | `<mandatory_double_return>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 259 | `<function_body_char>` → `<func_content_char>` | FIRST(`<func_content_char>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 260 | `<func_content_char>` → using id `<using_cont>` ; `<func_content_char>` | FIRST(using) | { using } |
| 261 | `<func_content_char>` → local `<mutability>` `<local_dec_body>` `<func_content_char>` | FIRST(local) | { local } |
| 262 | `<func_content_char>` → `<statement_char_no_ret>` `<func_content_char>` | FIRST(`<statement_char_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 263 | `<func_content_char>` → `<mandatory_char_return>` | FIRST(`<mandatory_char_return>`) | { return } |
| 264 | `<mandatory_char_return>` → return `<typed_string_ret_expr>` ; | FIRST(return) | { return } |
| 265 | `<function_body_string>` → `<func_content_string>` | FIRST(`<func_content_string>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 266 | `<func_content_string>` → using id `<using_cont>` ; `<func_content_string>` | FIRST(using) | { using } |
| 267 | `<func_content_string>` → local `<mutability>` `<local_dec_body>` `<func_content_string>` | FIRST(local) | { local } |
| 268 | `<func_content_string>` → `<statement_string_no_ret>` `<func_content_string>` | FIRST(`<statement_string_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 269 | `<func_content_string>` → `<mandatory_string_return>` | FIRST(`<mandatory_string_return>`) | { return } |
| 270 | `<mandatory_string_return>` → return `<typed_string_ret_expr>` ; | FIRST(return) | { return } |
| 271 | `<function_body_bool>` → `<func_content_bool>` | FIRST(`<func_content_bool>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 272 | `<func_content_bool>` → using id `<using_cont>` ; `<func_content_bool>` | FIRST(using) | { using } |
| 273 | `<func_content_bool>` → local `<mutability>` `<local_dec_body>` `<func_content_bool>` | FIRST(local) | { local } |
| 274 | `<func_content_bool>` → `<statement_bool_no_ret>` `<func_content_bool>` | FIRST(`<statement_bool_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 275 | `<func_content_bool>` → `<mandatory_bool_return>` | FIRST(`<mandatory_bool_return>`) | { return } |
| 276 | `<mandatory_bool_return>` → return `<typed_bool_ret_expr>` ; | FIRST(return) | { return } |
| 277 | `<function_body_array>` → `<func_content_array>` | FIRST(`<func_content_array>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 278 | `<func_content_array>` → using id `<using_cont>` ; `<func_content_array>` | FIRST(using) | { using } |
| 279 | `<func_content_array>` → local `<mutability>` `<local_dec_body>` `<func_content_array>` | FIRST(local) | { local } |
| 280 | `<func_content_array>` → `<statement_array_no_ret>` `<func_content_array>` | FIRST(`<statement_array_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 281 | `<func_content_array>` → `<mandatory_array_return>` | FIRST(`<mandatory_array_return>`) | { return } |
| 282 | `<mandatory_array_return>` → return id ; | FIRST(return) | { return } |
| 283 | `<function_body_weave>` → `<func_content_weave>` | FIRST(`<func_content_weave>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 284 | `<func_content_weave>` → using id `<using_cont>` ; `<func_content_weave>` | FIRST(using) | { using } |
| 285 | `<func_content_weave>` → local `<mutability>` `<local_dec_body>` `<func_content_weave>` | FIRST(local) | { local } |
| 286 | `<func_content_weave>` → `<statement_weave_no_ret>` `<func_content_weave>` | FIRST(`<statement_weave_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 287 | `<func_content_weave>` → `<mandatory_weave_return>` | FIRST(`<mandatory_weave_return>`) | { return } |
| 288 | `<mandatory_weave_return>` → return id ; | FIRST(return) | { return } |
| 289 | `<function_body_void>` → `<func_content_void>` | FIRST(`<func_content_void>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 290 | `<func_content_void>` → using id `<using_cont>` ; `<func_content_void>` | FIRST(using) | { using } |
| 291 | `<func_content_void>` → local `<mutability>` `<local_dec_body>` `<func_content_void>` | FIRST(local) | { local } |
| 292 | `<func_content_void>` → `<statement_void_no_ret>` `<func_content_void>` | FIRST(`<statement_void_no_ret>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 293 | `<func_content_void>` → `<mandatory_void_return>` | FIRST(`<mandatory_void_return>`) | { return } |
| 294 | `<mandatory_void_return>` → return ; | FIRST(return) | { return } |
| 295 | `<statement_int>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 296 | `<statement_int>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 297 | `<statement_int>` → `<ctrl_struct_int>` | FIRST(`<ctrl_struct_int>`) | { do, for, if, switch, while } |
| 298 | `<statement_int>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 299 | `<statement_long>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 300 | `<statement_long>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 301 | `<statement_long>` → `<ctrl_struct_long>` | FIRST(`<ctrl_struct_long>`) | { do, for, if, switch, while } |
| 302 | `<statement_long>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 303 | `<statement_float>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 304 | `<statement_float>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 305 | `<statement_float>` → `<ctrl_struct_float>` | FIRST(`<ctrl_struct_float>`) | { do, for, if, switch, while } |
| 306 | `<statement_float>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 307 | `<statement_double>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 308 | `<statement_double>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 309 | `<statement_double>` → `<ctrl_struct_double>` | FIRST(`<ctrl_struct_double>`) | { do, for, if, switch, while } |
| 310 | `<statement_double>` → return `<typed_numeric_ret_expr>` ; | FIRST(return) | { return } |
| 311 | `<statement_char>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 312 | `<statement_char>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 313 | `<statement_char>` → `<ctrl_struct_char>` | FIRST(`<ctrl_struct_char>`) | { do, for, if, switch, while } |
| 314 | `<statement_char>` → return `<typed_string_ret_expr>` ; | FIRST(return) | { return } |
| 315 | `<statement_string>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 316 | `<statement_string>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 317 | `<statement_string>` → `<ctrl_struct_string>` | FIRST(`<ctrl_struct_string>`) | { do, for, if, switch, while } |
| 318 | `<statement_string>` → return `<typed_string_ret_expr>` ; | FIRST(return) | { return } |
| 319 | `<statement_bool>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 320 | `<statement_bool>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 321 | `<statement_bool>` → `<ctrl_struct_bool>` | FIRST(`<ctrl_struct_bool>`) | { do, for, if, switch, while } |
| 322 | `<statement_bool>` → return `<typed_bool_ret_expr>` ; | FIRST(return) | { return } |
| 323 | `<statement_array>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 324 | `<statement_array>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 325 | `<statement_array>` → `<ctrl_struct_array>` | FIRST(`<ctrl_struct_array>`) | { do, for, if, switch, while } |
| 326 | `<statement_array>` → return id ; | FIRST(return) | { return } |
| 327 | `<statement_weave>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 328 | `<statement_weave>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 329 | `<statement_weave>` → `<ctrl_struct_weave>` | FIRST(`<ctrl_struct_weave>`) | { do, for, if, switch, while } |
| 330 | `<statement_weave>` → return id ; | FIRST(return) | { return } |
| 331 | `<statement_void>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 332 | `<statement_void>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 333 | `<statement_void>` → `<ctrl_struct_void>` | FIRST(`<ctrl_struct_void>`) | { do, for, if, switch, while } |
| 334 | `<statement_void>` → return ; | FIRST(return) | { return } |
| 335 | `<statement_int_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 336 | `<statement_int_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 337 | `<statement_int_no_ret>` → `<ctrl_struct_int>` | FIRST(`<ctrl_struct_int>`) | { do, for, if, switch, while } |
| 338 | `<statement_long_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 339 | `<statement_long_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 340 | `<statement_long_no_ret>` → `<ctrl_struct_long>` | FIRST(`<ctrl_struct_long>`) | { do, for, if, switch, while } |
| 341 | `<statement_float_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 342 | `<statement_float_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 343 | `<statement_float_no_ret>` → `<ctrl_struct_float>` | FIRST(`<ctrl_struct_float>`) | { do, for, if, switch, while } |
| 344 | `<statement_double_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 345 | `<statement_double_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 346 | `<statement_double_no_ret>` → `<ctrl_struct_double>` | FIRST(`<ctrl_struct_double>`) | { do, for, if, switch, while } |
| 347 | `<statement_char_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 348 | `<statement_char_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 349 | `<statement_char_no_ret>` → `<ctrl_struct_char>` | FIRST(`<ctrl_struct_char>`) | { do, for, if, switch, while } |
| 350 | `<statement_string_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 351 | `<statement_string_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 352 | `<statement_string_no_ret>` → `<ctrl_struct_string>` | FIRST(`<ctrl_struct_string>`) | { do, for, if, switch, while } |
| 353 | `<statement_bool_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 354 | `<statement_bool_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 355 | `<statement_bool_no_ret>` → `<ctrl_struct_bool>` | FIRST(`<ctrl_struct_bool>`) | { do, for, if, switch, while } |
| 356 | `<statement_array_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 357 | `<statement_array_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 358 | `<statement_array_no_ret>` → `<ctrl_struct_array>` | FIRST(`<ctrl_struct_array>`) | { do, for, if, switch, while } |
| 359 | `<statement_weave_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 360 | `<statement_weave_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 361 | `<statement_weave_no_ret>` → `<ctrl_struct_weave>` | FIRST(`<ctrl_struct_weave>`) | { do, for, if, switch, while } |
| 362 | `<statement_void_no_ret>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 363 | `<statement_void_no_ret>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 364 | `<statement_void_no_ret>` → `<ctrl_struct_void>` | FIRST(`<ctrl_struct_void>`) | { do, for, if, switch, while } |
| 365 | `<ctrl_struct_int>` → if ( `<condition>` ) { `<non_empty_stmt_list_int>` } `<else_opt_int>` | FIRST(if) | { if } |
| 366 | `<ctrl_struct_int>` → switch ( `<arg_expr>` ) { `<case_list_int>` `<default_opt_int>` } | FIRST(switch) | { switch } |
| 367 | `<ctrl_struct_int>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_int>` } | FIRST(for) | { for } |
| 368 | `<ctrl_struct_int>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_int>` } | FIRST(while) | { while } |
| 369 | `<ctrl_struct_int>` → do { `<non_empty_loop_stmt_list_int>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 370 | `<stmt_list_int>` → `<statement_int>` `<stmt_list_int>` | FIRST(`<statement_int>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 371 | `<stmt_list_int>` → λ | FOLLOW(`<stmt_list_int>`) | { } } |
| 372 | `<non_empty_stmt_list_int>` → `<statement_int>` `<stmt_list_int>` | FIRST(`<statement_int>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 373 | `<loop_statement_int>` → `<statement_int>` | FIRST(`<statement_int>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 374 | `<loop_statement_int>` → break ; | FIRST(break) | { break } |
| 375 | `<loop_stmt_list_int>` → `<loop_statement_int>` `<loop_stmt_list_int>` | FIRST(`<loop_statement_int>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 376 | `<loop_stmt_list_int>` → λ | FOLLOW(`<loop_stmt_list_int>`) | { break, case, default, } } |
| 377 | `<non_empty_loop_stmt_list_int>` → `<loop_statement_int>` `<loop_stmt_list_int>` | FIRST(`<loop_statement_int>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 378 | `<else_opt_int>` → else `<else_body_int>` | FIRST(else) | { else } |
| 379 | `<else_opt_int>` → λ | FOLLOW(`<else_opt_int>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 380 | `<else_body_int>` → { `<non_empty_stmt_list_int>` } | FIRST({) | { { } |
| 381 | `<else_body_int>` → if ( `<condition>` ) { `<non_empty_stmt_list_int>` } `<else_opt_int>` | FIRST(if) | { if } |
| 382 | `<case_list_int>` → case `<case_val>` : `<non_empty_loop_stmt_list_int>` `<break_opt>` `<case_list_int>` | FIRST(case) | { case } |
| 383 | `<case_list_int>` → λ | FOLLOW(`<case_list_int>`) | { default, } } |
| 384 | `<default_opt_int>` → default : `<non_empty_loop_stmt_list_int>` `<break_opt>` | FIRST(default) | { default } |
| 385 | `<default_opt_int>` → λ | FOLLOW(`<default_opt_int>`) | { } } |
| 386 | `<ctrl_struct_long>` → if ( `<condition>` ) { `<non_empty_stmt_list_long>` } `<else_opt_long>` | FIRST(if) | { if } |
| 387 | `<ctrl_struct_long>` → switch ( `<arg_expr>` ) { `<case_list_long>` `<default_opt_long>` } | FIRST(switch) | { switch } |
| 388 | `<ctrl_struct_long>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_long>` } | FIRST(for) | { for } |
| 389 | `<ctrl_struct_long>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_long>` } | FIRST(while) | { while } |
| 390 | `<ctrl_struct_long>` → do { `<non_empty_loop_stmt_list_long>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 391 | `<stmt_list_long>` → `<statement_long>` `<stmt_list_long>` | FIRST(`<statement_long>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 392 | `<stmt_list_long>` → λ | FOLLOW(`<stmt_list_long>`) | { } } |
| 393 | `<non_empty_stmt_list_long>` → `<statement_long>` `<stmt_list_long>` | FIRST(`<statement_long>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 394 | `<loop_statement_long>` → `<statement_long>` | FIRST(`<statement_long>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 395 | `<loop_statement_long>` → break ; | FIRST(break) | { break } |
| 396 | `<loop_stmt_list_long>` → `<loop_statement_long>` `<loop_stmt_list_long>` | FIRST(`<loop_statement_long>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 397 | `<loop_stmt_list_long>` → λ | FOLLOW(`<loop_stmt_list_long>`) | { break, case, default, } } |
| 398 | `<non_empty_loop_stmt_list_long>` → `<loop_statement_long>` `<loop_stmt_list_long>` | FIRST(`<loop_statement_long>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 399 | `<else_opt_long>` → else `<else_body_long>` | FIRST(else) | { else } |
| 400 | `<else_opt_long>` → λ | FOLLOW(`<else_opt_long>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 401 | `<else_body_long>` → { `<non_empty_stmt_list_long>` } | FIRST({) | { { } |
| 402 | `<else_body_long>` → if ( `<condition>` ) { `<non_empty_stmt_list_long>` } `<else_opt_long>` | FIRST(if) | { if } |
| 403 | `<case_list_long>` → case `<case_val>` : `<non_empty_loop_stmt_list_long>` `<break_opt>` `<case_list_long>` | FIRST(case) | { case } |
| 404 | `<case_list_long>` → λ | FOLLOW(`<case_list_long>`) | { default, } } |
| 405 | `<default_opt_long>` → default : `<non_empty_loop_stmt_list_long>` `<break_opt>` | FIRST(default) | { default } |
| 406 | `<default_opt_long>` → λ | FOLLOW(`<default_opt_long>`) | { } } |
| 407 | `<ctrl_struct_float>` → if ( `<condition>` ) { `<non_empty_stmt_list_float>` } `<else_opt_float>` | FIRST(if) | { if } |
| 408 | `<ctrl_struct_float>` → switch ( `<arg_expr>` ) { `<case_list_float>` `<default_opt_float>` } | FIRST(switch) | { switch } |
| 409 | `<ctrl_struct_float>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_float>` } | FIRST(for) | { for } |
| 410 | `<ctrl_struct_float>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_float>` } | FIRST(while) | { while } |
| 411 | `<ctrl_struct_float>` → do { `<non_empty_loop_stmt_list_float>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 412 | `<stmt_list_float>` → `<statement_float>` `<stmt_list_float>` | FIRST(`<statement_float>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 413 | `<stmt_list_float>` → λ | FOLLOW(`<stmt_list_float>`) | { } } |
| 414 | `<non_empty_stmt_list_float>` → `<statement_float>` `<stmt_list_float>` | FIRST(`<statement_float>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 415 | `<loop_statement_float>` → `<statement_float>` | FIRST(`<statement_float>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 416 | `<loop_statement_float>` → break ; | FIRST(break) | { break } |
| 417 | `<loop_stmt_list_float>` → `<loop_statement_float>` `<loop_stmt_list_float>` | FIRST(`<loop_statement_float>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 418 | `<loop_stmt_list_float>` → λ | FOLLOW(`<loop_stmt_list_float>`) | { break, case, default, } } |
| 419 | `<non_empty_loop_stmt_list_float>` → `<loop_statement_float>` `<loop_stmt_list_float>` | FIRST(`<loop_statement_float>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 420 | `<else_opt_float>` → else `<else_body_float>` | FIRST(else) | { else } |
| 421 | `<else_opt_float>` → λ | FOLLOW(`<else_opt_float>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 422 | `<else_body_float>` → { `<non_empty_stmt_list_float>` } | FIRST({) | { { } |
| 423 | `<else_body_float>` → if ( `<condition>` ) { `<non_empty_stmt_list_float>` } `<else_opt_float>` | FIRST(if) | { if } |
| 424 | `<case_list_float>` → case `<case_val>` : `<non_empty_loop_stmt_list_float>` `<break_opt>` `<case_list_float>` | FIRST(case) | { case } |
| 425 | `<case_list_float>` → λ | FOLLOW(`<case_list_float>`) | { default, } } |
| 426 | `<default_opt_float>` → default : `<non_empty_loop_stmt_list_float>` `<break_opt>` | FIRST(default) | { default } |
| 427 | `<default_opt_float>` → λ | FOLLOW(`<default_opt_float>`) | { } } |
| 428 | `<ctrl_struct_double>` → if ( `<condition>` ) { `<non_empty_stmt_list_double>` } `<else_opt_double>` | FIRST(if) | { if } |
| 429 | `<ctrl_struct_double>` → switch ( `<arg_expr>` ) { `<case_list_double>` `<default_opt_double>` } | FIRST(switch) | { switch } |
| 430 | `<ctrl_struct_double>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_double>` } | FIRST(for) | { for } |
| 431 | `<ctrl_struct_double>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_double>` } | FIRST(while) | { while } |
| 432 | `<ctrl_struct_double>` → do { `<non_empty_loop_stmt_list_double>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 433 | `<stmt_list_double>` → `<statement_double>` `<stmt_list_double>` | FIRST(`<statement_double>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 434 | `<stmt_list_double>` → λ | FOLLOW(`<stmt_list_double>`) | { } } |
| 435 | `<non_empty_stmt_list_double>` → `<statement_double>` `<stmt_list_double>` | FIRST(`<statement_double>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 436 | `<loop_statement_double>` → `<statement_double>` | FIRST(`<statement_double>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 437 | `<loop_statement_double>` → break ; | FIRST(break) | { break } |
| 438 | `<loop_stmt_list_double>` → `<loop_statement_double>` `<loop_stmt_list_double>` | FIRST(`<loop_statement_double>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 439 | `<loop_stmt_list_double>` → λ | FOLLOW(`<loop_stmt_list_double>`) | { break, case, default, } } |
| 440 | `<non_empty_loop_stmt_list_double>` → `<loop_statement_double>` `<loop_stmt_list_double>` | FIRST(`<loop_statement_double>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 441 | `<else_opt_double>` → else `<else_body_double>` | FIRST(else) | { else } |
| 442 | `<else_opt_double>` → λ | FOLLOW(`<else_opt_double>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 443 | `<else_body_double>` → { `<non_empty_stmt_list_double>` } | FIRST({) | { { } |
| 444 | `<else_body_double>` → if ( `<condition>` ) { `<non_empty_stmt_list_double>` } `<else_opt_double>` | FIRST(if) | { if } |
| 445 | `<case_list_double>` → case `<case_val>` : `<non_empty_loop_stmt_list_double>` `<break_opt>` `<case_list_double>` | FIRST(case) | { case } |
| 446 | `<case_list_double>` → λ | FOLLOW(`<case_list_double>`) | { default, } } |
| 447 | `<default_opt_double>` → default : `<non_empty_loop_stmt_list_double>` `<break_opt>` | FIRST(default) | { default } |
| 448 | `<default_opt_double>` → λ | FOLLOW(`<default_opt_double>`) | { } } |
| 449 | `<ctrl_struct_char>` → if ( `<condition>` ) { `<non_empty_stmt_list_char>` } `<else_opt_char>` | FIRST(if) | { if } |
| 450 | `<ctrl_struct_char>` → switch ( `<arg_expr>` ) { `<case_list_char>` `<default_opt_char>` } | FIRST(switch) | { switch } |
| 451 | `<ctrl_struct_char>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_char>` } | FIRST(for) | { for } |
| 452 | `<ctrl_struct_char>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_char>` } | FIRST(while) | { while } |
| 453 | `<ctrl_struct_char>` → do { `<non_empty_loop_stmt_list_char>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 454 | `<stmt_list_char>` → `<statement_char>` `<stmt_list_char>` | FIRST(`<statement_char>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 455 | `<stmt_list_char>` → λ | FOLLOW(`<stmt_list_char>`) | { } } |
| 456 | `<non_empty_stmt_list_char>` → `<statement_char>` `<stmt_list_char>` | FIRST(`<statement_char>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 457 | `<loop_statement_char>` → `<statement_char>` | FIRST(`<statement_char>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 458 | `<loop_statement_char>` → break ; | FIRST(break) | { break } |
| 459 | `<loop_stmt_list_char>` → `<loop_statement_char>` `<loop_stmt_list_char>` | FIRST(`<loop_statement_char>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 460 | `<loop_stmt_list_char>` → λ | FOLLOW(`<loop_stmt_list_char>`) | { break, case, default, } } |
| 461 | `<non_empty_loop_stmt_list_char>` → `<loop_statement_char>` `<loop_stmt_list_char>` | FIRST(`<loop_statement_char>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 462 | `<else_opt_char>` → else `<else_body_char>` | FIRST(else) | { else } |
| 463 | `<else_opt_char>` → λ | FOLLOW(`<else_opt_char>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 464 | `<else_body_char>` → { `<non_empty_stmt_list_char>` } | FIRST({) | { { } |
| 465 | `<else_body_char>` → if ( `<condition>` ) { `<non_empty_stmt_list_char>` } `<else_opt_char>` | FIRST(if) | { if } |
| 466 | `<case_list_char>` → case `<case_val>` : `<non_empty_loop_stmt_list_char>` `<break_opt>` `<case_list_char>` | FIRST(case) | { case } |
| 467 | `<case_list_char>` → λ | FOLLOW(`<case_list_char>`) | { default, } } |
| 468 | `<default_opt_char>` → default : `<non_empty_loop_stmt_list_char>` `<break_opt>` | FIRST(default) | { default } |
| 469 | `<default_opt_char>` → λ | FOLLOW(`<default_opt_char>`) | { } } |
| 470 | `<ctrl_struct_string>` → if ( `<condition>` ) { `<non_empty_stmt_list_string>` } `<else_opt_string>` | FIRST(if) | { if } |
| 471 | `<ctrl_struct_string>` → switch ( `<arg_expr>` ) { `<case_list_string>` `<default_opt_string>` } | FIRST(switch) | { switch } |
| 472 | `<ctrl_struct_string>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_string>` } | FIRST(for) | { for } |
| 473 | `<ctrl_struct_string>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_string>` } | FIRST(while) | { while } |
| 474 | `<ctrl_struct_string>` → do { `<non_empty_loop_stmt_list_string>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 475 | `<stmt_list_string>` → `<statement_string>` `<stmt_list_string>` | FIRST(`<statement_string>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 476 | `<stmt_list_string>` → λ | FOLLOW(`<stmt_list_string>`) | { } } |
| 477 | `<non_empty_stmt_list_string>` → `<statement_string>` `<stmt_list_string>` | FIRST(`<statement_string>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 478 | `<loop_statement_string>` → `<statement_string>` | FIRST(`<statement_string>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 479 | `<loop_statement_string>` → break ; | FIRST(break) | { break } |
| 480 | `<loop_stmt_list_string>` → `<loop_statement_string>` `<loop_stmt_list_string>` | FIRST(`<loop_statement_string>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 481 | `<loop_stmt_list_string>` → λ | FOLLOW(`<loop_stmt_list_string>`) | { break, case, default, } } |
| 482 | `<non_empty_loop_stmt_list_string>` → `<loop_statement_string>` `<loop_stmt_list_string>` | FIRST(`<loop_statement_string>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 483 | `<else_opt_string>` → else `<else_body_string>` | FIRST(else) | { else } |
| 484 | `<else_opt_string>` → λ | FOLLOW(`<else_opt_string>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 485 | `<else_body_string>` → { `<non_empty_stmt_list_string>` } | FIRST({) | { { } |
| 486 | `<else_body_string>` → if ( `<condition>` ) { `<non_empty_stmt_list_string>` } `<else_opt_string>` | FIRST(if) | { if } |
| 487 | `<case_list_string>` → case `<case_val>` : `<non_empty_loop_stmt_list_string>` `<break_opt>` `<case_list_string>` | FIRST(case) | { case } |
| 488 | `<case_list_string>` → λ | FOLLOW(`<case_list_string>`) | { default, } } |
| 489 | `<default_opt_string>` → default : `<non_empty_loop_stmt_list_string>` `<break_opt>` | FIRST(default) | { default } |
| 490 | `<default_opt_string>` → λ | FOLLOW(`<default_opt_string>`) | { } } |
| 491 | `<ctrl_struct_bool>` → if ( `<condition>` ) { `<non_empty_stmt_list_bool>` } `<else_opt_bool>` | FIRST(if) | { if } |
| 492 | `<ctrl_struct_bool>` → switch ( `<arg_expr>` ) { `<case_list_bool>` `<default_opt_bool>` } | FIRST(switch) | { switch } |
| 493 | `<ctrl_struct_bool>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_bool>` } | FIRST(for) | { for } |
| 494 | `<ctrl_struct_bool>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_bool>` } | FIRST(while) | { while } |
| 495 | `<ctrl_struct_bool>` → do { `<non_empty_loop_stmt_list_bool>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 496 | `<stmt_list_bool>` → `<statement_bool>` `<stmt_list_bool>` | FIRST(`<statement_bool>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 497 | `<stmt_list_bool>` → λ | FOLLOW(`<stmt_list_bool>`) | { } } |
| 498 | `<non_empty_stmt_list_bool>` → `<statement_bool>` `<stmt_list_bool>` | FIRST(`<statement_bool>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 499 | `<loop_statement_bool>` → `<statement_bool>` | FIRST(`<statement_bool>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 500 | `<loop_statement_bool>` → break ; | FIRST(break) | { break } |
| 501 | `<loop_stmt_list_bool>` → `<loop_statement_bool>` `<loop_stmt_list_bool>` | FIRST(`<loop_statement_bool>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 502 | `<loop_stmt_list_bool>` → λ | FOLLOW(`<loop_stmt_list_bool>`) | { break, case, default, } } |
| 503 | `<non_empty_loop_stmt_list_bool>` → `<loop_statement_bool>` `<loop_stmt_list_bool>` | FIRST(`<loop_statement_bool>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 504 | `<else_opt_bool>` → else `<else_body_bool>` | FIRST(else) | { else } |
| 505 | `<else_opt_bool>` → λ | FOLLOW(`<else_opt_bool>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 506 | `<else_body_bool>` → { `<non_empty_stmt_list_bool>` } | FIRST({) | { { } |
| 507 | `<else_body_bool>` → if ( `<condition>` ) { `<non_empty_stmt_list_bool>` } `<else_opt_bool>` | FIRST(if) | { if } |
| 508 | `<case_list_bool>` → case `<case_val>` : `<non_empty_loop_stmt_list_bool>` `<break_opt>` `<case_list_bool>` | FIRST(case) | { case } |
| 509 | `<case_list_bool>` → λ | FOLLOW(`<case_list_bool>`) | { default, } } |
| 510 | `<default_opt_bool>` → default : `<non_empty_loop_stmt_list_bool>` `<break_opt>` | FIRST(default) | { default } |
| 511 | `<default_opt_bool>` → λ | FOLLOW(`<default_opt_bool>`) | { } } |
| 512 | `<ctrl_struct_array>` → if ( `<condition>` ) { `<non_empty_stmt_list_array>` } `<else_opt_array>` | FIRST(if) | { if } |
| 513 | `<ctrl_struct_array>` → switch ( `<arg_expr>` ) { `<case_list_array>` `<default_opt_array>` } | FIRST(switch) | { switch } |
| 514 | `<ctrl_struct_array>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_array>` } | FIRST(for) | { for } |
| 515 | `<ctrl_struct_array>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_array>` } | FIRST(while) | { while } |
| 516 | `<ctrl_struct_array>` → do { `<non_empty_loop_stmt_list_array>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 517 | `<stmt_list_array>` → `<statement_array>` `<stmt_list_array>` | FIRST(`<statement_array>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 518 | `<stmt_list_array>` → λ | FOLLOW(`<stmt_list_array>`) | { } } |
| 519 | `<non_empty_stmt_list_array>` → `<statement_array>` `<stmt_list_array>` | FIRST(`<statement_array>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 520 | `<loop_statement_array>` → `<statement_array>` | FIRST(`<statement_array>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 521 | `<loop_statement_array>` → break ; | FIRST(break) | { break } |
| 522 | `<loop_stmt_list_array>` → `<loop_statement_array>` `<loop_stmt_list_array>` | FIRST(`<loop_statement_array>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 523 | `<loop_stmt_list_array>` → λ | FOLLOW(`<loop_stmt_list_array>`) | { break, case, default, } } |
| 524 | `<non_empty_loop_stmt_list_array>` → `<loop_statement_array>` `<loop_stmt_list_array>` | FIRST(`<loop_statement_array>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 525 | `<else_opt_array>` → else `<else_body_array>` | FIRST(else) | { else } |
| 526 | `<else_opt_array>` → λ | FOLLOW(`<else_opt_array>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 527 | `<else_body_array>` → { `<non_empty_stmt_list_array>` } | FIRST({) | { { } |
| 528 | `<else_body_array>` → if ( `<condition>` ) { `<non_empty_stmt_list_array>` } `<else_opt_array>` | FIRST(if) | { if } |
| 529 | `<case_list_array>` → case `<case_val>` : `<non_empty_loop_stmt_list_array>` `<break_opt>` `<case_list_array>` | FIRST(case) | { case } |
| 530 | `<case_list_array>` → λ | FOLLOW(`<case_list_array>`) | { default, } } |
| 531 | `<default_opt_array>` → default : `<non_empty_loop_stmt_list_array>` `<break_opt>` | FIRST(default) | { default } |
| 532 | `<default_opt_array>` → λ | FOLLOW(`<default_opt_array>`) | { } } |
| 533 | `<ctrl_struct_weave>` → if ( `<condition>` ) { `<non_empty_stmt_list_weave>` } `<else_opt_weave>` | FIRST(if) | { if } |
| 534 | `<ctrl_struct_weave>` → switch ( `<arg_expr>` ) { `<case_list_weave>` `<default_opt_weave>` } | FIRST(switch) | { switch } |
| 535 | `<ctrl_struct_weave>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_weave>` } | FIRST(for) | { for } |
| 536 | `<ctrl_struct_weave>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_weave>` } | FIRST(while) | { while } |
| 537 | `<ctrl_struct_weave>` → do { `<non_empty_loop_stmt_list_weave>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 538 | `<stmt_list_weave>` → `<statement_weave>` `<stmt_list_weave>` | FIRST(`<statement_weave>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 539 | `<stmt_list_weave>` → λ | FOLLOW(`<stmt_list_weave>`) | { } } |
| 540 | `<non_empty_stmt_list_weave>` → `<statement_weave>` `<stmt_list_weave>` | FIRST(`<statement_weave>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 541 | `<loop_statement_weave>` → `<statement_weave>` | FIRST(`<statement_weave>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 542 | `<loop_statement_weave>` → break ; | FIRST(break) | { break } |
| 543 | `<loop_stmt_list_weave>` → `<loop_statement_weave>` `<loop_stmt_list_weave>` | FIRST(`<loop_statement_weave>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 544 | `<loop_stmt_list_weave>` → λ | FOLLOW(`<loop_stmt_list_weave>`) | { break, case, default, } } |
| 545 | `<non_empty_loop_stmt_list_weave>` → `<loop_statement_weave>` `<loop_stmt_list_weave>` | FIRST(`<loop_statement_weave>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 546 | `<else_opt_weave>` → else `<else_body_weave>` | FIRST(else) | { else } |
| 547 | `<else_opt_weave>` → λ | FOLLOW(`<else_opt_weave>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 548 | `<else_body_weave>` → { `<non_empty_stmt_list_weave>` } | FIRST({) | { { } |
| 549 | `<else_body_weave>` → if ( `<condition>` ) { `<non_empty_stmt_list_weave>` } `<else_opt_weave>` | FIRST(if) | { if } |
| 550 | `<case_list_weave>` → case `<case_val>` : `<non_empty_loop_stmt_list_weave>` `<break_opt>` `<case_list_weave>` | FIRST(case) | { case } |
| 551 | `<case_list_weave>` → λ | FOLLOW(`<case_list_weave>`) | { default, } } |
| 552 | `<default_opt_weave>` → default : `<non_empty_loop_stmt_list_weave>` `<break_opt>` | FIRST(default) | { default } |
| 553 | `<default_opt_weave>` → λ | FOLLOW(`<default_opt_weave>`) | { } } |
| 554 | `<ctrl_struct_void>` → if ( `<condition>` ) { `<non_empty_stmt_list_void>` } `<else_opt_void>` | FIRST(if) | { if } |
| 555 | `<ctrl_struct_void>` → switch ( `<arg_expr>` ) { `<case_list_void>` `<default_opt_void>` } | FIRST(switch) | { switch } |
| 556 | `<ctrl_struct_void>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_stmt_list_void>` } | FIRST(for) | { for } |
| 557 | `<ctrl_struct_void>` → while ( `<condition>` ) { `<non_empty_loop_stmt_list_void>` } | FIRST(while) | { while } |
| 558 | `<ctrl_struct_void>` → do { `<non_empty_loop_stmt_list_void>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 559 | `<stmt_list_void>` → `<statement_void>` `<stmt_list_void>` | FIRST(`<statement_void>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 560 | `<stmt_list_void>` → λ | FOLLOW(`<stmt_list_void>`) | { } } |
| 561 | `<non_empty_stmt_list_void>` → `<statement_void>` `<stmt_list_void>` | FIRST(`<statement_void>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 562 | `<loop_statement_void>` → `<statement_void>` | FIRST(`<statement_void>`) | { ++, --, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 563 | `<loop_statement_void>` → break ; | FIRST(break) | { break } |
| 564 | `<loop_stmt_list_void>` → `<loop_statement_void>` `<loop_stmt_list_void>` | FIRST(`<loop_statement_void>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 565 | `<loop_stmt_list_void>` → λ | FOLLOW(`<loop_stmt_list_void>`) | { break, case, default, } } |
| 566 | `<non_empty_loop_stmt_list_void>` → `<loop_statement_void>` `<loop_stmt_list_void>` | FIRST(`<loop_statement_void>`) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 567 | `<else_opt_void>` → else `<else_body_void>` | FIRST(else) | { else } |
| 568 | `<else_opt_void>` → λ | FOLLOW(`<else_opt_void>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 569 | `<else_body_void>` → { `<non_empty_stmt_list_void>` } | FIRST({) | { { } |
| 570 | `<else_body_void>` → if ( `<condition>` ) { `<non_empty_stmt_list_void>` } `<else_opt_void>` | FIRST(if) | { if } |
| 571 | `<case_list_void>` → case `<case_val>` : `<non_empty_loop_stmt_list_void>` `<break_opt>` `<case_list_void>` | FIRST(case) | { case } |
| 572 | `<case_list_void>` → λ | FOLLOW(`<case_list_void>`) | { default, } } |
| 573 | `<default_opt_void>` → default : `<non_empty_loop_stmt_list_void>` `<break_opt>` | FIRST(default) | { default } |
| 574 | `<default_opt_void>` → λ | FOLLOW(`<default_opt_void>`) | { } } |
| 575 | `<typed_numeric_ret_expr>` → `<typed_numeric_add_expr>` | FIRST(`<typed_numeric_add_expr>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 576 | `<typed_string_ret_expr>` → `<typed_string_ret_primary>` `<typed_string_cont>` | FIRST(`<typed_string_ret_primary>`) | { (, char, charlit, id, string, stringlit } |
| 577 | `<typed_string_ret_primary>` → stringlit | FIRST(stringlit) | { stringlit } |
| 578 | `<typed_string_ret_primary>` → charlit | FIRST(charlit) | { charlit } |
| 579 | `<typed_string_ret_primary>` → id `<typed_postfix_chain>` | FIRST(id) | { id } |
| 580 | `<typed_string_ret_primary>` → string ( `<expression>` ) | FIRST(string) | { string } |
| 581 | `<typed_string_ret_primary>` → char ( `<expression>` ) | FIRST(char) | { char } |
| 582 | `<typed_string_ret_primary>` → ( `<expression>` ) `<typed_postfix_chain>` | FIRST(() | { ( } |
| 583 | `<typed_bool_ret_expr>` → `<typed_bool_ret_primary>` `<typed_bool_ret_tail>` | FIRST(`<typed_bool_ret_primary>`) | { !, (, -, bool, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 584 | `<typed_bool_ret_primary>` → true | FIRST(true) | { true } |
| 585 | `<typed_bool_ret_primary>` → false | FIRST(false) | { false } |
| 586 | `<typed_bool_ret_primary>` → ! `<typed_bool_factor>` | FIRST(!) | { ! } |
| 587 | `<typed_bool_ret_primary>` → id `<typed_bool_id_cont>` | FIRST(id) | { id } |
| 588 | `<typed_bool_ret_primary>` → ( `<typed_bool_paren>` ) | FIRST(() | { ( } |
| 589 | `<typed_bool_ret_primary>` → bool ( `<expression>` ) | FIRST(bool) | { bool } |
| 590 | `<typed_bool_ret_primary>` → intlit `<typed_numeric_cmp_required>` | FIRST(intlit) | { intlit } |
| 591 | `<typed_bool_ret_primary>` → longlit `<typed_numeric_cmp_required>` | FIRST(longlit) | { longlit } |
| 592 | `<typed_bool_ret_primary>` → floatlit `<typed_numeric_cmp_required>` | FIRST(floatlit) | { floatlit } |
| 593 | `<typed_bool_ret_primary>` → doublelit `<typed_numeric_cmp_required>` | FIRST(doublelit) | { doublelit } |
| 594 | `<typed_bool_ret_primary>` → - `<typed_numeric_neg_cmp>` | FIRST(-) | { - } |
| 595 | `<typed_bool_ret_primary>` → int ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(int) | { int } |
| 596 | `<typed_bool_ret_primary>` → long ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(long) | { long } |
| 597 | `<typed_bool_ret_primary>` → float ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(float) | { float } |
| 598 | `<typed_bool_ret_primary>` → double ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(double) | { double } |
| 599 | `<typed_bool_ret_tail>` → && `<typed_bool_term>` `<typed_bool_and_tail>` `<typed_bool_or_tail_opt>` | FIRST(&&) | { && } |
| 600 | `<typed_bool_ret_tail>` → || `<typed_bool_term>` `<typed_bool_or_tail>` | FIRST(||) | { || } |
| 601 | `<typed_bool_ret_tail>` → == `<typed_bool_factor>` `<typed_bool_eq_tail>` `<typed_bool_ret_tail>` | FIRST(==) | { == } |
| 602 | `<typed_bool_ret_tail>` → != `<typed_bool_factor>` `<typed_bool_eq_tail>` `<typed_bool_ret_tail>` | FIRST(!=) | { != } |
| 603 | `<typed_bool_ret_tail>` → λ | FOLLOW(`<typed_bool_ret_tail>`) | { ; } |
| 604 | `<using_cont>` → , id `<using_cont>` | FIRST(,) | { , } |
| 605 | `<using_cont>` → λ | FOLLOW(`<using_cont>`) | { ; } |
| 606 | `<local_dec_body>` → int id `<int_local_tail>` | FIRST(int) | { int } |
| 607 | `<local_dec_body>` → long id `<long_local_tail>` | FIRST(long) | { long } |
| 608 | `<local_dec_body>` → float id `<float_local_tail>` | FIRST(float) | { float } |
| 609 | `<local_dec_body>` → double id `<double_local_tail>` | FIRST(double) | { double } |
| 610 | `<local_dec_body>` → char id `<char_local_tail>` | FIRST(char) | { char } |
| 611 | `<local_dec_body>` → string id `<string_local_tail>` | FIRST(string) | { string } |
| 612 | `<local_dec_body>` → bool id `<bool_local_tail>` | FIRST(bool) | { bool } |
| 613 | `<local_dec_body>` → id id `<weave_local_tail>` | FIRST(id) | { id } |
| 614 | `<int_local_tail>` → `<int_array_with_init>` ; | FIRST(`<int_array_with_init>`) | { [ } |
| 615 | `<int_local_tail>` → = intlit `<int_local_cont>` ; | FIRST(=) | { = } |
| 616 | `<int_local_cont>` → , id = intlit `<int_local_cont>` | FIRST(,) | { , } |
| 617 | `<int_local_cont>` → λ | FOLLOW(`<int_local_cont>`) | { ; } |
| 618 | `<long_local_tail>` → `<long_array_with_init>` ; | FIRST(`<long_array_with_init>`) | { [ } |
| 619 | `<long_local_tail>` → = longlit `<long_local_cont>` ; | FIRST(=) | { = } |
| 620 | `<long_local_cont>` → , id = longlit `<long_local_cont>` | FIRST(,) | { , } |
| 621 | `<long_local_cont>` → λ | FOLLOW(`<long_local_cont>`) | { ; } |
| 622 | `<float_local_tail>` → `<float_array_with_init>` ; | FIRST(`<float_array_with_init>`) | { [ } |
| 623 | `<float_local_tail>` → = floatlit `<float_local_cont>` ; | FIRST(=) | { = } |
| 624 | `<float_local_cont>` → , id = floatlit `<float_local_cont>` | FIRST(,) | { , } |
| 625 | `<float_local_cont>` → λ | FOLLOW(`<float_local_cont>`) | { ; } |
| 626 | `<double_local_tail>` → `<double_array_with_init>` ; | FIRST(`<double_array_with_init>`) | { [ } |
| 627 | `<double_local_tail>` → = doublelit `<double_local_cont>` ; | FIRST(=) | { = } |
| 628 | `<double_local_cont>` → , id = doublelit `<double_local_cont>` | FIRST(,) | { , } |
| 629 | `<double_local_cont>` → λ | FOLLOW(`<double_local_cont>`) | { ; } |
| 630 | `<char_local_tail>` → `<char_array_with_init>` ; | FIRST(`<char_array_with_init>`) | { [ } |
| 631 | `<char_local_tail>` → = charlit `<char_local_cont>` ; | FIRST(=) | { = } |
| 632 | `<char_local_cont>` → , id = charlit `<char_local_cont>` | FIRST(,) | { , } |
| 633 | `<char_local_cont>` → λ | FOLLOW(`<char_local_cont>`) | { ; } |
| 634 | `<string_local_tail>` → `<string_array_with_init>` ; | FIRST(`<string_array_with_init>`) | { [ } |
| 635 | `<string_local_tail>` → = stringlit `<string_local_cont>` ; | FIRST(=) | { = } |
| 636 | `<string_local_cont>` → , id = stringlit `<string_local_cont>` | FIRST(,) | { , } |
| 637 | `<string_local_cont>` → λ | FOLLOW(`<string_local_cont>`) | { ; } |
| 638 | `<bool_local_tail>` → `<bool_array_with_init>` ; | FIRST(`<bool_array_with_init>`) | { [ } |
| 639 | `<bool_local_tail>` → = `<bool_lit>` `<bool_local_cont>` ; | FIRST(=) | { = } |
| 640 | `<bool_local_cont>` → , id = `<bool_lit>` `<bool_local_cont>` | FIRST(,) | { , } |
| 641 | `<bool_local_cont>` → λ | FOLLOW(`<bool_local_cont>`) | { ; } |
| 642 | `<weave_local_tail>` → = { `<weave_field_value>` `<weave_field_list_tail>` } `<weave_inst_cont>` ; | FIRST(=) | { = } |
| 643 | `<weave_local_tail>` → `<weave_array_with_init>` `<weave_arr_cont>` ; | FIRST(`<weave_array_with_init>`) | { [ } |
| 644 | `<statement_non_return>` → `<effect_stmt>` ; | FIRST(`<effect_stmt>`) | { ++, --, id } |
| 645 | `<statement_non_return>` → `<io_stmt>` | FIRST(`<io_stmt>`) | { thread, threadln, trap } |
| 646 | `<statement_non_return>` → `<ctrl_struct>` | FIRST(`<ctrl_struct>`) | { do, for, if, switch, while } |
| 647 | `<expression>` → `<typed_assign_expr>` | FIRST(`<typed_assign_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 648 | `<typed_assign_expr>` → `<typed_concat_expr>` `<typed_assign_tail>` | FIRST(`<typed_concat_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 649 | `<typed_assign_tail>` → = `<typed_rhs_expr>` | FIRST(=) | { = } |
| 650 | `<typed_assign_tail>` → += `<typed_numeric_add_expr>` | FIRST(+=) | { += } |
| 651 | `<typed_assign_tail>` → -= `<typed_numeric_add_expr>` | FIRST(-=) | { -= } |
| 652 | `<typed_assign_tail>` → *= `<typed_numeric_add_expr>` | FIRST(*=) | { *= } |
| 653 | `<typed_assign_tail>` → /= `<typed_numeric_add_expr>` | FIRST(/=) | { /= } |
| 654 | `<typed_assign_tail>` → %= `<typed_numeric_add_expr>` | FIRST(%=) | { %= } |
| 655 | `<typed_assign_tail>` → λ | FOLLOW(`<typed_assign_tail>`) | { ) } |
| 656 | `<assign_op>` → = | FIRST(=) | { = } |
| 657 | `<assign_op>` → += | FIRST(+=) | { += } |
| 658 | `<assign_op>` → -= | FIRST(-=) | { -= } |
| 659 | `<assign_op>` → *= | FIRST(*=) | { *= } |
| 660 | `<assign_op>` → /= | FIRST(/=) | { /= } |
| 661 | `<assign_op>` → %= | FIRST(%=) | { %= } |
| 662 | `<typed_rhs_expr>` → `<typed_concat_expr>` | FIRST(`<typed_concat_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 663 | `<typed_concat_expr>` → stringlit `<typed_string_cont>` | FIRST(stringlit) | { stringlit } |
| 664 | `<typed_concat_expr>` → charlit `<typed_string_cont>` | FIRST(charlit) | { charlit } |
| 665 | `<typed_concat_expr>` → intlit `<typed_numeric_cont>` | FIRST(intlit) | { intlit } |
| 666 | `<typed_concat_expr>` → longlit `<typed_numeric_cont>` | FIRST(longlit) | { longlit } |
| 667 | `<typed_concat_expr>` → floatlit `<typed_numeric_cont>` | FIRST(floatlit) | { floatlit } |
| 668 | `<typed_concat_expr>` → doublelit `<typed_numeric_cont>` | FIRST(doublelit) | { doublelit } |
| 669 | `<typed_concat_expr>` → true `<typed_bool_cont>` | FIRST(true) | { true } |
| 670 | `<typed_concat_expr>` → false `<typed_bool_cont>` | FIRST(false) | { false } |
| 671 | `<typed_concat_expr>` → ! `<typed_bool_factor>` `<typed_bool_tail_opt>` | FIRST(!) | { ! } |
| 672 | `<typed_concat_expr>` → - `<typed_neg_numeric_cont>` | FIRST(-) | { - } |
| 673 | `<typed_concat_expr>` → id `<typed_id_cont>` | FIRST(id) | { id } |
| 674 | `<typed_concat_expr>` → ( `<typed_paren_cont>` | FIRST(() | { ( } |
| 675 | `<typed_concat_expr>` → int ( `<expression>` ) `<typed_numeric_cont>` | FIRST(int) | { int } |
| 676 | `<typed_concat_expr>` → long ( `<expression>` ) `<typed_numeric_cont>` | FIRST(long) | { long } |
| 677 | `<typed_concat_expr>` → float ( `<expression>` ) `<typed_numeric_cont>` | FIRST(float) | { float } |
| 678 | `<typed_concat_expr>` → double ( `<expression>` ) `<typed_numeric_cont>` | FIRST(double) | { double } |
| 679 | `<typed_concat_expr>` → char ( `<expression>` ) `<typed_string_cont>` | FIRST(char) | { char } |
| 680 | `<typed_concat_expr>` → string ( `<expression>` ) `<typed_string_cont>` | FIRST(string) | { string } |
| 681 | `<typed_concat_expr>` → bool ( `<expression>` ) `<typed_bool_cont>` | FIRST(bool) | { bool } |
| 682 | `<typed_concat_expr>` → ++ id | FIRST(++) | { ++ } |
| 683 | `<typed_concat_expr>` → -- id | FIRST(--) | { -- } |
| 684 | `<typed_string_cont>` → .. `<typed_string_operand>` `<typed_string_cont>` | FIRST(..) | { .. } |
| 685 | `<typed_string_cont>` → λ | FOLLOW(`<typed_string_cont>`) | { %=, ), *=, +=, -=, /=, ;, = } |
| 686 | `<typed_string_operand>` → stringlit | FIRST(stringlit) | { stringlit } |
| 687 | `<typed_string_operand>` → charlit | FIRST(charlit) | { charlit } |
| 688 | `<typed_string_operand>` → id | FIRST(id) | { id } |
| 689 | `<typed_string_operand>` → string ( `<expression>` ) | FIRST(string) | { string } |
| 690 | `<typed_string_operand>` → char ( `<expression>` ) | FIRST(char) | { char } |
| 691 | `<typed_string_operand>` → ( `<typed_string_operand>` `<typed_string_cont>` ) | FIRST(() | { ( } |
| 692 | `<typed_string_operand>` → intlit | FIRST(intlit) | { intlit } |
| 693 | `<typed_string_operand>` → longlit | FIRST(longlit) | { longlit } |
| 694 | `<typed_string_operand>` → floatlit | FIRST(floatlit) | { floatlit } |
| 695 | `<typed_string_operand>` → doublelit | FIRST(doublelit) | { doublelit } |
| 696 | `<typed_string_operand>` → true | FIRST(true) | { true } |
| 697 | `<typed_string_operand>` → false | FIRST(false) | { false } |
| 698 | `<typed_string_operand>` → int ( `<expression>` ) | FIRST(int) | { int } |
| 699 | `<typed_string_operand>` → long ( `<expression>` ) | FIRST(long) | { long } |
| 700 | `<typed_string_operand>` → float ( `<expression>` ) | FIRST(float) | { float } |
| 701 | `<typed_string_operand>` → double ( `<expression>` ) | FIRST(double) | { double } |
| 702 | `<typed_string_operand>` → bool ( `<expression>` ) | FIRST(bool) | { bool } |
| 703 | `<typed_numeric_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 704 | `<typed_numeric_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 705 | `<typed_numeric_cont>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 706 | `<typed_arith_ops>` → + `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` | FIRST(+) | { + } |
| 707 | `<typed_arith_ops>` → - `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` | FIRST(-) | { - } |
| 708 | `<typed_arith_ops>` → * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` | FIRST(*) | { * } |
| 709 | `<typed_arith_ops>` → / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` | FIRST(/) | { / } |
| 710 | `<typed_arith_ops>` → % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` | FIRST(%) | { % } |
| 711 | `<typed_numeric_add_ops>` → + `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` | FIRST(+) | { + } |
| 712 | `<typed_numeric_add_ops>` → - `<typed_numeric_mul_expr>` `<typed_numeric_add_ops>` | FIRST(-) | { - } |
| 713 | `<typed_numeric_add_ops>` → λ | FOLLOW(`<typed_numeric_add_ops>`) | { !=, %=, &&, ), *=, +=, -=, /=, <, <=, =, ==, >, >=, || } |
| 714 | `<typed_after_arith>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 715 | `<typed_after_arith>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 716 | `<typed_neg_numeric_cont>` → `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_ops>` `<typed_after_arith>` | FIRST(`<typed_numeric_unary_expr>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 717 | `<typed_bool_cont>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 718 | `<typed_bool_tail_opt>` → && `<typed_bool_term>` `<typed_bool_and_tail>` `<typed_bool_or_tail_opt>` | FIRST(&&) | { && } |
| 719 | `<typed_bool_tail_opt>` → || `<typed_bool_term>` `<typed_bool_or_tail>` | FIRST(||) | { || } |
| 720 | `<typed_bool_tail_opt>` → λ | FOLLOW(`<typed_bool_tail_opt>`) | { %=, ), *=, +=, -=, /=, = } |
| 721 | `<typed_bool_or_tail_opt>` → || `<typed_bool_term>` `<typed_bool_or_tail>` | FIRST(||) | { || } |
| 722 | `<typed_bool_or_tail_opt>` → λ | FOLLOW(`<typed_bool_or_tail_opt>`) | { %=, ), *=, +=, -=, /=, ;, = } |
| 723 | `<typed_bool_term>` → `<typed_bool_eq>` `<typed_bool_and_tail>` | FIRST(`<typed_bool_eq>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 724 | `<typed_bool_and_tail>` → && `<typed_bool_eq>` `<typed_bool_and_tail>` | FIRST(&&) | { && } |
| 725 | `<typed_bool_and_tail>` → λ | FOLLOW(`<typed_bool_and_tail>`) | { %=, &&, ), *=, +=, -=, /=, ;, =, || } |
| 726 | `<typed_bool_or_tail>` → || `<typed_bool_term>` `<typed_bool_or_tail>` | FIRST(||) | { || } |
| 727 | `<typed_bool_or_tail>` → λ | FOLLOW(`<typed_bool_or_tail>`) | { %=, ), *=, +=, -=, /=, ;, = } |
| 728 | `<typed_bool_eq>` → `<typed_bool_factor>` `<typed_bool_eq_tail>` | FIRST(`<typed_bool_factor>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 729 | `<typed_bool_eq_tail>` → == `<typed_bool_factor>` `<typed_bool_eq_tail>` | FIRST(==) | { == } |
| 730 | `<typed_bool_eq_tail>` → != `<typed_bool_factor>` `<typed_bool_eq_tail>` | FIRST(!=) | { != } |
| 731 | `<typed_bool_eq_tail>` → λ | FOLLOW(`<typed_bool_eq_tail>`) | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 732 | `<typed_bool_factor>` → ! `<typed_bool_factor>` | FIRST(!) | { ! } |
| 733 | `<typed_bool_factor>` → `<typed_bool_atom>` | FIRST(`<typed_bool_atom>`) | { (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 734 | `<typed_bool_atom>` → true | FIRST(true) | { true } |
| 735 | `<typed_bool_atom>` → false | FIRST(false) | { false } |
| 736 | `<typed_bool_atom>` → id `<typed_bool_id_cont>` | FIRST(id) | { id } |
| 737 | `<typed_bool_atom>` → intlit `<typed_numeric_cmp_required>` | FIRST(intlit) | { intlit } |
| 738 | `<typed_bool_atom>` → longlit `<typed_numeric_cmp_required>` | FIRST(longlit) | { longlit } |
| 739 | `<typed_bool_atom>` → floatlit `<typed_numeric_cmp_required>` | FIRST(floatlit) | { floatlit } |
| 740 | `<typed_bool_atom>` → doublelit `<typed_numeric_cmp_required>` | FIRST(doublelit) | { doublelit } |
| 741 | `<typed_bool_atom>` → - `<typed_numeric_neg_cmp>` | FIRST(-) | { - } |
| 742 | `<typed_bool_atom>` → ( `<typed_bool_paren>` ) | FIRST(() | { ( } |
| 743 | `<typed_bool_atom>` → int ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(int) | { int } |
| 744 | `<typed_bool_atom>` → long ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(long) | { long } |
| 745 | `<typed_bool_atom>` → float ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(float) | { float } |
| 746 | `<typed_bool_atom>` → double ( `<expression>` ) `<typed_numeric_cmp_required>` | FIRST(double) | { double } |
| 747 | `<typed_bool_paren>` → `<typed_bool_term>` `<typed_bool_and_or_tail>` | FIRST(`<typed_bool_term>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 748 | `<typed_bool_and_or_tail>` → && `<typed_bool_term>` `<typed_bool_and_or_tail>` | FIRST(&&) | { && } |
| 749 | `<typed_bool_and_or_tail>` → || `<typed_bool_term>` `<typed_bool_and_or_tail>` | FIRST(||) | { || } |
| 750 | `<typed_bool_and_or_tail>` → λ | FOLLOW(`<typed_bool_and_or_tail>`) | { ) } |
| 751 | `<typed_bool_id_cont>` → `<typed_numeric_arith_cmp>` | FIRST(`<typed_numeric_arith_cmp>`) | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 752 | `<typed_bool_id_cont>` → ++ | FIRST(++) | { ++ } |
| 753 | `<typed_bool_id_cont>` → -- | FIRST(--) | { -- } |
| 754 | `<typed_bool_id_cont>` → `<typed_postfix_chain>` | FIRST(`<typed_postfix_chain>`) | { !=, %=, &&, (, ), *=, +=, -=, ., /=, ;, =, ==, [, || } |
| 755 | `<typed_numeric_arith_cmp>` → + `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(+) | { + } |
| 756 | `<typed_numeric_arith_cmp>` → - `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(-) | { - } |
| 757 | `<typed_numeric_arith_cmp>` → * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(*) | { * } |
| 758 | `<typed_numeric_arith_cmp>` → / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(/) | { / } |
| 759 | `<typed_numeric_arith_cmp>` → % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(%) | { % } |
| 760 | `<typed_numeric_arith_cmp>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 761 | `<typed_numeric_add_cmp>` → + `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` | FIRST(+) | { + } |
| 762 | `<typed_numeric_add_cmp>` → - `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` | FIRST(-) | { - } |
| 763 | `<typed_numeric_add_cmp>` → λ | FOLLOW(`<typed_numeric_add_cmp>`) | { !=, <, <=, ==, >, >= } |
| 764 | `<typed_numeric_cmp_required>` → `<typed_numeric_lit_arith>` `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(`<typed_numeric_lit_arith>`) | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 765 | `<typed_numeric_lit_arith>` → * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` | FIRST(*) | { * } |
| 766 | `<typed_numeric_lit_arith>` → / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` | FIRST(/) | { / } |
| 767 | `<typed_numeric_lit_arith>` → % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` | FIRST(%) | { % } |
| 768 | `<typed_numeric_lit_arith>` → + `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` | FIRST(+) | { + } |
| 769 | `<typed_numeric_lit_arith>` → - `<typed_numeric_mul_expr>` `<typed_numeric_add_cmp>` | FIRST(-) | { - } |
| 770 | `<typed_numeric_lit_arith>` → λ | FOLLOW(`<typed_numeric_lit_arith>`) | { !=, <, <=, ==, >, >= } |
| 771 | `<typed_numeric_neg_cmp>` → `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` `<typed_numeric_add_cmp>` `<typed_cmp_op>` `<typed_numeric_add_expr>` | FIRST(`<typed_numeric_unary_expr>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 772 | `<typed_id_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 773 | `<typed_id_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 774 | `<typed_id_cont>` → ++ | FIRST(++) | { ++ } |
| 775 | `<typed_id_cont>` → -- | FIRST(--) | { -- } |
| 776 | `<typed_id_cont>` → [ `<array_index>` ] `<typed_id_arr_cont>` | FIRST([) | { [ } |
| 777 | `<typed_id_cont>` → . id `<typed_id_field_cont>` | FIRST(.) | { . } |
| 778 | `<typed_id_cont>` → ( `<arg_list>` ) `<typed_id_call_cont>` | FIRST(() | { ( } |
| 779 | `<typed_id_cont>` → .. `<typed_string_operand>` `<typed_string_cont>` | FIRST(..) | { .. } |
| 780 | `<typed_id_cont>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 781 | `<typed_id_arr_cont>` → [ `<array_index>` ] `<typed_id_arr2_cont>` | FIRST([) | { [ } |
| 782 | `<typed_id_arr_cont>` → `<typed_id_postfix_cont>` | FIRST(`<typed_id_postfix_cont>`) | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, <, <=, =, ==, >, >=, || } |
| 783 | `<typed_id_arr2_cont>` → `<typed_id_postfix_cont>` | FIRST(`<typed_id_postfix_cont>`) | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, <, <=, =, ==, >, >=, || } |
| 784 | `<typed_id_postfix_cont>` → . id `<typed_id_field_cont>` | FIRST(.) | { . } |
| 785 | `<typed_id_postfix_cont>` → ( `<arg_list>` ) `<typed_id_call_cont>` | FIRST(() | { ( } |
| 786 | `<typed_id_postfix_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 787 | `<typed_id_postfix_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 788 | `<typed_id_postfix_cont>` → .. `<typed_string_operand>` `<typed_string_cont>` | FIRST(..) | { .. } |
| 789 | `<typed_id_postfix_cont>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 790 | `<typed_id_field_cont>` → [ `<array_index>` ] `<typed_id_arr_cont>` | FIRST([) | { [ } |
| 791 | `<typed_id_field_cont>` → . id `<typed_id_field_cont>` | FIRST(.) | { . } |
| 792 | `<typed_id_field_cont>` → ( `<arg_list>` ) `<typed_id_call_cont>` | FIRST(() | { ( } |
| 793 | `<typed_id_field_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 794 | `<typed_id_field_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 795 | `<typed_id_field_cont>` → .. `<typed_string_operand>` `<typed_string_cont>` | FIRST(..) | { .. } |
| 796 | `<typed_id_field_cont>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 797 | `<typed_id_call_cont>` → [ `<array_index>` ] `<typed_id_arr_cont>` | FIRST([) | { [ } |
| 798 | `<typed_id_call_cont>` → . id `<typed_id_field_cont>` | FIRST(.) | { . } |
| 799 | `<typed_id_call_cont>` → ( `<arg_list>` ) `<typed_id_call_cont>` | FIRST(() | { ( } |
| 800 | `<typed_id_call_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 801 | `<typed_id_call_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 802 | `<typed_id_call_cont>` → .. `<typed_string_operand>` `<typed_string_cont>` | FIRST(..) | { .. } |
| 803 | `<typed_id_call_cont>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 804 | `<typed_paren_cont>` → `<typed_concat_expr>` ) `<typed_paren_after>` | FIRST(`<typed_concat_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 805 | `<typed_paren_after>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 806 | `<typed_paren_after>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 807 | `<typed_paren_after>` → .. `<typed_string_operand>` `<typed_string_cont>` | FIRST(..) | { .. } |
| 808 | `<typed_paren_after>` → [ `<array_index>` ] `<typed_paren_arr_cont>` | FIRST([) | { [ } |
| 809 | `<typed_paren_after>` → . id `<typed_paren_field_cont>` | FIRST(.) | { . } |
| 810 | `<typed_paren_after>` → ( `<arg_list>` ) `<typed_paren_call_cont>` | FIRST(() | { ( } |
| 811 | `<typed_paren_after>` → `<typed_bool_tail_opt>` | FIRST(`<typed_bool_tail_opt>`) | { %=, &&, ), *=, +=, -=, /=, =, || } |
| 812 | `<typed_paren_arr_cont>` → [ `<array_index>` ] `<typed_paren_arr2_cont>` | FIRST([) | { [ } |
| 813 | `<typed_paren_arr_cont>` → `<typed_paren_postfix_cont>` | FIRST(`<typed_paren_postfix_cont>`) | { !=, %, %=, (, ), *, *=, +, +=, -, -=, ., /, /=, <, <=, =, ==, >, >= } |
| 814 | `<typed_paren_arr2_cont>` → `<typed_paren_postfix_cont>` | FIRST(`<typed_paren_postfix_cont>`) | { !=, %, %=, (, ), *, *=, +, +=, -, -=, ., /, /=, <, <=, =, ==, >, >= } |
| 815 | `<typed_paren_postfix_cont>` → . id `<typed_paren_field_cont>` | FIRST(.) | { . } |
| 816 | `<typed_paren_postfix_cont>` → ( `<arg_list>` ) `<typed_paren_call_cont>` | FIRST(() | { ( } |
| 817 | `<typed_paren_postfix_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 818 | `<typed_paren_postfix_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 819 | `<typed_paren_postfix_cont>` → λ | FOLLOW(`<typed_paren_postfix_cont>`) | { %=, ), *=, +=, -=, /=, = } |
| 820 | `<typed_paren_field_cont>` → [ `<array_index>` ] `<typed_paren_arr_cont>` | FIRST([) | { [ } |
| 821 | `<typed_paren_field_cont>` → . id `<typed_paren_field_cont>` | FIRST(.) | { . } |
| 822 | `<typed_paren_field_cont>` → ( `<arg_list>` ) `<typed_paren_call_cont>` | FIRST(() | { ( } |
| 823 | `<typed_paren_field_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 824 | `<typed_paren_field_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 825 | `<typed_paren_field_cont>` → λ | FOLLOW(`<typed_paren_field_cont>`) | { %=, ), *=, +=, -=, /=, = } |
| 826 | `<typed_paren_call_cont>` → [ `<array_index>` ] `<typed_paren_arr_cont>` | FIRST([) | { [ } |
| 827 | `<typed_paren_call_cont>` → . id `<typed_paren_field_cont>` | FIRST(.) | { . } |
| 828 | `<typed_paren_call_cont>` → ( `<arg_list>` ) `<typed_paren_call_cont>` | FIRST(() | { ( } |
| 829 | `<typed_paren_call_cont>` → `<typed_arith_ops>` `<typed_after_arith>` | FIRST(`<typed_arith_ops>`) | { %, *, +, -, / } |
| 830 | `<typed_paren_call_cont>` → `<typed_cmp_op>` `<typed_numeric_add_expr>` `<typed_bool_tail_opt>` | FIRST(`<typed_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 831 | `<typed_paren_call_cont>` → λ | FOLLOW(`<typed_paren_call_cont>`) | { %=, ), *=, +=, -=, /=, = } |
| 832 | `<typed_numeric_add_expr>` → `<typed_numeric_mul_expr>` `<typed_numeric_add_tail>` | FIRST(`<typed_numeric_mul_expr>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 833 | `<typed_numeric_add_tail>` → + `<typed_numeric_mul_expr>` `<typed_numeric_add_tail>` | FIRST(+) | { + } |
| 834 | `<typed_numeric_add_tail>` → - `<typed_numeric_mul_expr>` `<typed_numeric_add_tail>` | FIRST(-) | { - } |
| 835 | `<typed_numeric_add_tail>` → λ | FOLLOW(`<typed_numeric_add_tail>`) | { !=, %=, &&, ), *=, +=, -=, /=, ;, =, ==, || } |
| 836 | `<typed_numeric_mul_expr>` → `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` | FIRST(`<typed_numeric_unary_expr>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 837 | `<typed_numeric_mul_tail>` → * `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` | FIRST(*) | { * } |
| 838 | `<typed_numeric_mul_tail>` → / `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` | FIRST(/) | { / } |
| 839 | `<typed_numeric_mul_tail>` → % `<typed_numeric_unary_expr>` `<typed_numeric_mul_tail>` | FIRST(%) | { % } |
| 840 | `<typed_numeric_mul_tail>` → λ | FOLLOW(`<typed_numeric_mul_tail>`) | { !=, %=, &&, ), *=, +, +=, -, -=, /=, ;, <, <=, =, ==, >, >=, || } |
| 841 | `<typed_numeric_unary_expr>` → ! `<typed_numeric_unary_expr>` | FIRST(!) | { ! } |
| 842 | `<typed_numeric_unary_expr>` → - `<typed_numeric_unary_expr>` | FIRST(-) | { - } |
| 843 | `<typed_numeric_unary_expr>` → `<typed_numeric_postfix_expr>` | FIRST(`<typed_numeric_postfix_expr>`) | { (, ++, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 844 | `<typed_numeric_postfix_expr>` → intlit | FIRST(intlit) | { intlit } |
| 845 | `<typed_numeric_postfix_expr>` → longlit | FIRST(longlit) | { longlit } |
| 846 | `<typed_numeric_postfix_expr>` → floatlit | FIRST(floatlit) | { floatlit } |
| 847 | `<typed_numeric_postfix_expr>` → doublelit | FIRST(doublelit) | { doublelit } |
| 848 | `<typed_numeric_postfix_expr>` → id `<typed_postfix_chain>` | FIRST(id) | { id } |
| 849 | `<typed_numeric_postfix_expr>` → ( `<expression>` ) `<typed_postfix_chain>` | FIRST(() | { ( } |
| 850 | `<typed_numeric_postfix_expr>` → int ( `<expression>` ) | FIRST(int) | { int } |
| 851 | `<typed_numeric_postfix_expr>` → long ( `<expression>` ) | FIRST(long) | { long } |
| 852 | `<typed_numeric_postfix_expr>` → float ( `<expression>` ) | FIRST(float) | { float } |
| 853 | `<typed_numeric_postfix_expr>` → double ( `<expression>` ) | FIRST(double) | { double } |
| 854 | `<typed_numeric_postfix_expr>` → ++ id | FIRST(++) | { ++ } |
| 855 | `<typed_numeric_postfix_expr>` → -- id | FIRST(--) | { -- } |
| 856 | `<typed_cmp_op>` → < | FIRST(<) | { < } |
| 857 | `<typed_cmp_op>` → > | FIRST(>) | { > } |
| 858 | `<typed_cmp_op>` → <= | FIRST(<=) | { <= } |
| 859 | `<typed_cmp_op>` → >= | FIRST(>=) | { >= } |
| 860 | `<typed_cmp_op>` → == | FIRST(==) | { == } |
| 861 | `<typed_cmp_op>` → != | FIRST(!=) | { != } |
| 862 | `<typed_postfix_chain>` → [ `<array_index>` ] `<typed_postfix_after_arr>` | FIRST([) | { [ } |
| 863 | `<typed_postfix_chain>` → . id `<typed_postfix_chain>` | FIRST(.) | { . } |
| 864 | `<typed_postfix_chain>` → ( `<arg_list>` ) `<typed_postfix_chain>` | FIRST(() | { ( } |
| 865 | `<typed_postfix_chain>` → λ | FOLLOW(`<typed_postfix_chain>`) | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, || } |
| 866 | `<typed_postfix_after_arr>` → [ `<array_index>` ] | FIRST([) | { [ } |
| 867 | `<typed_postfix_after_arr>` → . id `<typed_postfix_chain>` | FIRST(.) | { . } |
| 868 | `<typed_postfix_after_arr>` → ( `<arg_list>` ) `<typed_postfix_chain>` | FIRST(() | { ( } |
| 869 | `<typed_postfix_after_arr>` → λ | FOLLOW(`<typed_postfix_after_arr>`) | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, || } |
| 870 | `<array_index>` → intlit | FIRST(intlit) | { intlit } |
| 871 | `<array_index>` → id | FIRST(id) | { id } |
| 872 | `<arg_list>` → `<arg_expr>` `<arg_tail>` | FIRST(`<arg_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 873 | `<arg_list>` → λ | FOLLOW(`<arg_list>`) | { ) } |
| 874 | `<arg_tail>` → , `<arg_expr>` `<arg_tail>` | FIRST(,) | { , } |
| 875 | `<arg_tail>` → λ | FOLLOW(`<arg_tail>`) | { ) } |
| 876 | `<effect_stmt>` → ++ id `<effect_pre_chain>` | FIRST(++) | { ++ } |
| 877 | `<effect_stmt>` → -- id `<effect_pre_chain>` | FIRST(--) | { -- } |
| 878 | `<effect_stmt>` → id `<effect_id_cont>` | FIRST(id) | { id } |
| 879 | `<effect_pre_chain>` → [ `<stmt_array_index>` ] `<effect_pre_arr_chain>` | FIRST([) | { [ } |
| 880 | `<effect_pre_chain>` → . id `<effect_pre_chain>` | FIRST(.) | { . } |
| 881 | `<effect_pre_chain>` → λ | FOLLOW(`<effect_pre_chain>`) | { ; } |
| 882 | `<effect_pre_arr_chain>` → [ `<stmt_array_index>` ] | FIRST([) | { [ } |
| 883 | `<effect_pre_arr_chain>` → . id `<effect_pre_chain>` | FIRST(.) | { . } |
| 884 | `<effect_pre_arr_chain>` → λ | FOLLOW(`<effect_pre_arr_chain>`) | { ; } |
| 885 | `<effect_id_cont>` → = `<stmt_assign_expr>` | FIRST(=) | { = } |
| 886 | `<effect_id_cont>` → += `<numeric_add_expr_stmt>` | FIRST(+=) | { += } |
| 887 | `<effect_id_cont>` → -= `<numeric_add_expr_stmt>` | FIRST(-=) | { -= } |
| 888 | `<effect_id_cont>` → *= `<numeric_add_expr_stmt>` | FIRST(*=) | { *= } |
| 889 | `<effect_id_cont>` → /= `<numeric_add_expr_stmt>` | FIRST(/=) | { /= } |
| 890 | `<effect_id_cont>` → %= `<numeric_add_expr_stmt>` | FIRST(%=) | { %= } |
| 891 | `<effect_id_cont>` → ++ | FIRST(++) | { ++ } |
| 892 | `<effect_id_cont>` → -- | FIRST(--) | { -- } |
| 893 | `<effect_id_cont>` → ( `<stmt_arg_list>` ) `<effect_post_call>` | FIRST(() | { ( } |
| 894 | `<effect_id_cont>` → [ `<stmt_array_index>` ] `<effect_post_arr>` | FIRST([) | { [ } |
| 895 | `<effect_id_cont>` → . id `<effect_post_member>` | FIRST(.) | { . } |
| 896 | `<effect_post_call>` → . id `<effect_post_call_member>` | FIRST(.) | { . } |
| 897 | `<effect_post_call>` → [ `<stmt_array_index>` ] `<effect_post_call_arr>` | FIRST([) | { [ } |
| 898 | `<effect_post_call>` → λ | FOLLOW(`<effect_post_call>`) | { ; } |
| 899 | `<effect_post_call_member>` → ( `<stmt_arg_list>` ) `<effect_post_call>` | FIRST(() | { ( } |
| 900 | `<effect_post_call_member>` → [ `<stmt_array_index>` ] `<effect_post_call_arr>` | FIRST([) | { [ } |
| 901 | `<effect_post_call_member>` → . id `<effect_post_call_member>` | FIRST(.) | { . } |
| 902 | `<effect_post_call_member>` → λ | FOLLOW(`<effect_post_call_member>`) | { ; } |
| 903 | `<effect_post_call_arr>` → [ `<stmt_array_index>` ] `<effect_post_call_arr_cont>` | FIRST([) | { [ } |
| 904 | `<effect_post_call_arr>` → `<effect_post_call_arr_cont>` | FIRST(`<effect_post_call_arr_cont>`) | { (, ., ; } |
| 905 | `<effect_post_call_arr_cont>` → . id `<effect_post_call_member>` | FIRST(.) | { . } |
| 906 | `<effect_post_call_arr_cont>` → ( `<stmt_arg_list>` ) `<effect_post_call>` | FIRST(() | { ( } |
| 907 | `<effect_post_call_arr_cont>` → λ | FOLLOW(`<effect_post_call_arr_cont>`) | { ; } |
| 908 | `<effect_post_arr>` → [ `<stmt_array_index>` ] `<effect_post_arr_2d>` | FIRST([) | { [ } |
| 909 | `<effect_post_arr>` → `<effect_arr_effect>` | FIRST(`<effect_arr_effect>`) | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 910 | `<effect_post_arr_2d>` → `<effect_arr_effect>` | FIRST(`<effect_arr_effect>`) | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 911 | `<effect_arr_effect>` → = `<stmt_assign_expr>` | FIRST(=) | { = } |
| 912 | `<effect_arr_effect>` → += `<numeric_add_expr_stmt>` | FIRST(+=) | { += } |
| 913 | `<effect_arr_effect>` → -= `<numeric_add_expr_stmt>` | FIRST(-=) | { -= } |
| 914 | `<effect_arr_effect>` → *= `<numeric_add_expr_stmt>` | FIRST(*=) | { *= } |
| 915 | `<effect_arr_effect>` → /= `<numeric_add_expr_stmt>` | FIRST(/=) | { /= } |
| 916 | `<effect_arr_effect>` → %= `<numeric_add_expr_stmt>` | FIRST(%=) | { %= } |
| 917 | `<effect_arr_effect>` → ++ | FIRST(++) | { ++ } |
| 918 | `<effect_arr_effect>` → -- | FIRST(--) | { -- } |
| 919 | `<effect_arr_effect>` → ( `<stmt_arg_list>` ) `<effect_post_call>` | FIRST(() | { ( } |
| 920 | `<effect_arr_effect>` → . id `<effect_post_member>` | FIRST(.) | { . } |
| 921 | `<effect_post_member>` → = `<stmt_assign_expr>` | FIRST(=) | { = } |
| 922 | `<effect_post_member>` → += `<numeric_add_expr_stmt>` | FIRST(+=) | { += } |
| 923 | `<effect_post_member>` → -= `<numeric_add_expr_stmt>` | FIRST(-=) | { -= } |
| 924 | `<effect_post_member>` → *= `<numeric_add_expr_stmt>` | FIRST(*=) | { *= } |
| 925 | `<effect_post_member>` → /= `<numeric_add_expr_stmt>` | FIRST(/=) | { /= } |
| 926 | `<effect_post_member>` → %= `<numeric_add_expr_stmt>` | FIRST(%=) | { %= } |
| 927 | `<effect_post_member>` → ++ | FIRST(++) | { ++ } |
| 928 | `<effect_post_member>` → -- | FIRST(--) | { -- } |
| 929 | `<effect_post_member>` → ( `<stmt_arg_list>` ) `<effect_post_call>` | FIRST(() | { ( } |
| 930 | `<effect_post_member>` → [ `<stmt_array_index>` ] `<effect_post_arr>` | FIRST([) | { [ } |
| 931 | `<effect_post_member>` → . id `<effect_post_member>` | FIRST(.) | { . } |
| 932 | `<stmt_assign_expr>` → `<stmt_typed_rhs>` | FIRST(`<stmt_typed_rhs>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 933 | `<stmt_typed_rhs>` → `<stmt_bool_or_concat>` | FIRST(`<stmt_bool_or_concat>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 934 | `<stmt_bool_or_concat>` → stringlit `<stmt_concat_tail_typed>` | FIRST(stringlit) | { stringlit } |
| 935 | `<stmt_bool_or_concat>` → charlit `<stmt_concat_tail_typed>` | FIRST(charlit) | { charlit } |
| 936 | `<stmt_bool_or_concat>` → string ( `<arg_expr>` ) `<stmt_concat_tail_typed>` | FIRST(string) | { string } |
| 937 | `<stmt_bool_or_concat>` → intlit `<stmt_numeric_or_bool>` | FIRST(intlit) | { intlit } |
| 938 | `<stmt_bool_or_concat>` → longlit `<stmt_numeric_or_bool>` | FIRST(longlit) | { longlit } |
| 939 | `<stmt_bool_or_concat>` → floatlit `<stmt_numeric_or_bool>` | FIRST(floatlit) | { floatlit } |
| 940 | `<stmt_bool_or_concat>` → doublelit `<stmt_numeric_or_bool>` | FIRST(doublelit) | { doublelit } |
| 941 | `<stmt_bool_or_concat>` → - `<stmt_neg_numeric_or_bool>` | FIRST(-) | { - } |
| 942 | `<stmt_bool_or_concat>` → true `<stmt_bool_tail_opt>` | FIRST(true) | { true } |
| 943 | `<stmt_bool_or_concat>` → false `<stmt_bool_tail_opt>` | FIRST(false) | { false } |
| 944 | `<stmt_bool_or_concat>` → ! `<stmt_bool_factor>` `<stmt_bool_tail_opt>` | FIRST(!) | { ! } |
| 945 | `<stmt_bool_or_concat>` → int ( `<arg_expr>` ) `<stmt_numeric_or_bool>` | FIRST(int) | { int } |
| 946 | `<stmt_bool_or_concat>` → long ( `<arg_expr>` ) `<stmt_numeric_or_bool>` | FIRST(long) | { long } |
| 947 | `<stmt_bool_or_concat>` → float ( `<arg_expr>` ) `<stmt_numeric_or_bool>` | FIRST(float) | { float } |
| 948 | `<stmt_bool_or_concat>` → double ( `<arg_expr>` ) `<stmt_numeric_or_bool>` | FIRST(double) | { double } |
| 949 | `<stmt_bool_or_concat>` → char ( `<arg_expr>` ) | FIRST(char) | { char } |
| 950 | `<stmt_bool_or_concat>` → bool ( `<arg_expr>` ) `<stmt_bool_tail_opt>` | FIRST(bool) | { bool } |
| 951 | `<stmt_bool_or_concat>` → id `<stmt_id_toplevel_cont>` | FIRST(id) | { id } |
| 952 | `<stmt_bool_or_concat>` → ( `<stmt_paren_typed_content>` | FIRST(() | { ( } |
| 953 | `<stmt_bool_or_concat>` → ++ id | FIRST(++) | { ++ } |
| 954 | `<stmt_bool_or_concat>` → -- id | FIRST(--) | { -- } |
| 955 | `<stmt_numeric_or_bool>` → `<stmt_arith_ops>` `<stmt_after_arith>` | FIRST(`<stmt_arith_ops>`) | { %, *, +, -, / } |
| 956 | `<stmt_numeric_or_bool>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 957 | `<stmt_numeric_or_bool>` → `<stmt_bool_tail_opt>` | FIRST(`<stmt_bool_tail_opt>`) | { &&, ;, || } |
| 958 | `<stmt_arith_ops>` → + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` | FIRST(+) | { + } |
| 959 | `<stmt_arith_ops>` → - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` | FIRST(-) | { - } |
| 960 | `<stmt_arith_ops>` → * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` | FIRST(*) | { * } |
| 961 | `<stmt_arith_ops>` → / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` | FIRST(/) | { / } |
| 962 | `<stmt_arith_ops>` → % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` | FIRST(%) | { % } |
| 963 | `<stmt_numeric_add_ops>` → + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` | FIRST(+) | { + } |
| 964 | `<stmt_numeric_add_ops>` → - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` | FIRST(-) | { - } |
| 965 | `<stmt_numeric_add_ops>` → λ | FOLLOW(`<stmt_numeric_add_ops>`) | { !=, &&, ), ;, <, <=, ==, >, >=, || } |
| 966 | `<stmt_after_arith>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 967 | `<stmt_after_arith>` → `<stmt_bool_tail_opt>` | FIRST(`<stmt_bool_tail_opt>`) | { &&, ), ;, || } |
| 968 | `<stmt_neg_numeric_or_bool>` → `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_after_arith>` | FIRST(`<numeric_unary_expr_stmt>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 969 | `<stmt_bool_tail_opt>` → && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` | FIRST(&&) | { && } |
| 970 | `<stmt_bool_tail_opt>` → || `<stmt_bool_term>` `<stmt_bool_or_tail>` | FIRST(||) | { || } |
| 971 | `<stmt_bool_tail_opt>` → λ | FOLLOW(`<stmt_bool_tail_opt>`) | { ), ; } |
| 972 | `<stmt_bool_or_tail_opt>` → || `<stmt_bool_term>` `<stmt_bool_or_tail>` | FIRST(||) | { || } |
| 973 | `<stmt_bool_or_tail_opt>` → λ | FOLLOW(`<stmt_bool_or_tail_opt>`) | { ), ; } |
| 974 | `<stmt_id_toplevel_cont>` → `<stmt_arith_ops>` `<stmt_after_arith>` | FIRST(`<stmt_arith_ops>`) | { %, *, +, -, / } |
| 975 | `<stmt_id_toplevel_cont>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 976 | `<stmt_id_toplevel_cont>` → ++ | FIRST(++) | { ++ } |
| 977 | `<stmt_id_toplevel_cont>` → -- | FIRST(--) | { -- } |
| 978 | `<stmt_id_toplevel_cont>` → `<stmt_postfix_chain>` `<stmt_id_after_postfix>` | FIRST(`<stmt_postfix_chain>`) | { !=, %, &&, (, *, +, -, ., .., /, ;, <, <=, ==, >, >=, [, || } |
| 979 | `<stmt_id_after_postfix>` → `<stmt_arith_ops>` `<stmt_after_arith>` | FIRST(`<stmt_arith_ops>`) | { %, *, +, -, / } |
| 980 | `<stmt_id_after_postfix>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 981 | `<stmt_id_after_postfix>` → .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` | FIRST(..) | { .. } |
| 982 | `<stmt_id_after_postfix>` → `<stmt_bool_tail_opt>` | FIRST(`<stmt_bool_tail_opt>`) | { &&, ;, || } |
| 983 | `<stmt_paren_typed_content>` → stringlit `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` | FIRST(stringlit) | { stringlit } |
| 984 | `<stmt_paren_typed_content>` → charlit `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` | FIRST(charlit) | { charlit } |
| 985 | `<stmt_paren_typed_content>` → string ( `<arg_expr>` ) `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` | FIRST(string) | { string } |
| 986 | `<stmt_paren_typed_content>` → char ( `<arg_expr>` ) ) `<stmt_paren_string_cont>` | FIRST(char) | { char } |
| 987 | `<stmt_paren_typed_content>` → intlit `<stmt_paren_num_start>` | FIRST(intlit) | { intlit } |
| 988 | `<stmt_paren_typed_content>` → longlit `<stmt_paren_num_start>` | FIRST(longlit) | { longlit } |
| 989 | `<stmt_paren_typed_content>` → floatlit `<stmt_paren_num_start>` | FIRST(floatlit) | { floatlit } |
| 990 | `<stmt_paren_typed_content>` → doublelit `<stmt_paren_num_start>` | FIRST(doublelit) | { doublelit } |
| 991 | `<stmt_paren_typed_content>` → - `<stmt_paren_neg_num>` | FIRST(-) | { - } |
| 992 | `<stmt_paren_typed_content>` → int ( `<arg_expr>` ) `<stmt_paren_num_start>` | FIRST(int) | { int } |
| 993 | `<stmt_paren_typed_content>` → long ( `<arg_expr>` ) `<stmt_paren_num_start>` | FIRST(long) | { long } |
| 994 | `<stmt_paren_typed_content>` → float ( `<arg_expr>` ) `<stmt_paren_num_start>` | FIRST(float) | { float } |
| 995 | `<stmt_paren_typed_content>` → double ( `<arg_expr>` ) `<stmt_paren_num_start>` | FIRST(double) | { double } |
| 996 | `<stmt_paren_typed_content>` → true `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(true) | { true } |
| 997 | `<stmt_paren_typed_content>` → false `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(false) | { false } |
| 998 | `<stmt_paren_typed_content>` → ! `<stmt_bool_factor>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(!) | { ! } |
| 999 | `<stmt_paren_typed_content>` → bool ( `<arg_expr>` ) `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(bool) | { bool } |
| 1000 | `<stmt_paren_typed_content>` → id `<stmt_paren_id_cont>` | FIRST(id) | { id } |
| 1001 | `<stmt_paren_typed_content>` → ( `<stmt_paren_typed_content>` ) `<stmt_paren_any_cont>` | FIRST(() | { ( } |
| 1002 | `<stmt_paren_typed_content>` → ++ id `<stmt_paren_num_after_incr>` | FIRST(++) | { ++ } |
| 1003 | `<stmt_paren_typed_content>` → -- id `<stmt_paren_num_after_incr>` | FIRST(--) | { -- } |
| 1004 | `<stmt_paren_string_cont>` → .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` | FIRST(..) | { .. } |
| 1005 | `<stmt_paren_string_cont>` → λ | FOLLOW(`<stmt_paren_string_cont>`) | { ), ; } |
| 1006 | `<stmt_paren_num_start>` → `<stmt_paren_arith_ops>` | FIRST(`<stmt_paren_arith_ops>`) | { %, *, +, -, / } |
| 1007 | `<stmt_paren_num_start>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1008 | `<stmt_paren_num_start>` → ) `<stmt_paren_num_cont>` | FIRST()) | { ) } |
| 1009 | `<stmt_paren_arith_ops>` → + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` | FIRST(+) | { + } |
| 1010 | `<stmt_paren_arith_ops>` → - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` | FIRST(-) | { - } |
| 1011 | `<stmt_paren_arith_ops>` → * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` | FIRST(*) | { * } |
| 1012 | `<stmt_paren_arith_ops>` → / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` | FIRST(/) | { / } |
| 1013 | `<stmt_paren_arith_ops>` → % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` | FIRST(%) | { % } |
| 1014 | `<stmt_paren_after_arith>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1015 | `<stmt_paren_after_arith>` → ) `<stmt_paren_num_cont>` | FIRST()) | { ) } |
| 1016 | `<stmt_paren_neg_num>` → `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_ops>` `<stmt_paren_after_arith>` | FIRST(`<numeric_unary_expr_stmt>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1017 | `<stmt_paren_num_after_incr>` → `<stmt_paren_arith_ops>` | FIRST(`<stmt_paren_arith_ops>`) | { %, *, +, -, / } |
| 1018 | `<stmt_paren_num_after_incr>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1019 | `<stmt_paren_num_after_incr>` → ) `<stmt_paren_num_cont>` | FIRST()) | { ) } |
| 1020 | `<stmt_paren_num_cont>` → `<stmt_arith_ops>` `<stmt_after_arith>` | FIRST(`<stmt_arith_ops>`) | { %, *, +, -, / } |
| 1021 | `<stmt_paren_num_cont>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1022 | `<stmt_paren_num_cont>` → `<stmt_bool_tail_opt>` | FIRST(`<stmt_bool_tail_opt>`) | { &&, ), ;, || } |
| 1023 | `<stmt_paren_bool_tail>` → && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` | FIRST(&&) | { && } |
| 1024 | `<stmt_paren_bool_tail>` → || `<stmt_bool_term>` `<stmt_bool_or_tail>` | FIRST(||) | { || } |
| 1025 | `<stmt_paren_bool_tail>` → λ | FOLLOW(`<stmt_paren_bool_tail>`) | { ) } |
| 1026 | `<stmt_paren_bool_cont>` → && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` | FIRST(&&) | { && } |
| 1027 | `<stmt_paren_bool_cont>` → || `<stmt_bool_term>` `<stmt_bool_or_tail>` | FIRST(||) | { || } |
| 1028 | `<stmt_paren_bool_cont>` → λ | FOLLOW(`<stmt_paren_bool_cont>`) | { ), ; } |
| 1029 | `<stmt_paren_id_cont>` → `<stmt_paren_arith_ops>` | FIRST(`<stmt_paren_arith_ops>`) | { %, *, +, -, / } |
| 1030 | `<stmt_paren_id_cont>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1031 | `<stmt_paren_id_cont>` → `<stmt_paren_postfix_nonnull>` `<stmt_paren_id_after_postfix>` | FIRST(`<stmt_paren_postfix_nonnull>`) | { (, ., [ } |
| 1032 | `<stmt_paren_id_cont>` → ++ ) `<stmt_paren_num_cont>` | FIRST(++) | { ++ } |
| 1033 | `<stmt_paren_id_cont>` → -- ) `<stmt_paren_num_cont>` | FIRST(--) | { -- } |
| 1034 | `<stmt_paren_id_cont>` → && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` ) `<stmt_paren_any_cont>` | FIRST(&&) | { && } |
| 1035 | `<stmt_paren_id_cont>` → || `<stmt_bool_term>` `<stmt_bool_or_tail>` ) `<stmt_paren_any_cont>` | FIRST(||) | { || } |
| 1036 | `<stmt_paren_id_cont>` → ) `<stmt_paren_any_cont>` | FIRST()) | { ) } |
| 1037 | `<stmt_paren_postfix_nonnull>` → [ `<array_index>` ] `<stmt_postfix_after_arr>` | FIRST([) | { [ } |
| 1038 | `<stmt_paren_postfix_nonnull>` → . id `<stmt_postfix_chain>` | FIRST(.) | { . } |
| 1039 | `<stmt_paren_postfix_nonnull>` → ( `<arg_list>` ) `<stmt_postfix_chain>` | FIRST(() | { ( } |
| 1040 | `<stmt_paren_id_after_postfix>` → `<stmt_paren_arith_ops>` | FIRST(`<stmt_paren_arith_ops>`) | { %, *, +, -, / } |
| 1041 | `<stmt_paren_id_after_postfix>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_paren_bool_tail>` ) `<stmt_paren_bool_cont>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1042 | `<stmt_paren_id_after_postfix>` → .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` ) `<stmt_paren_string_cont>` | FIRST(..) | { .. } |
| 1043 | `<stmt_paren_id_after_postfix>` → && `<stmt_bool_term>` `<stmt_bool_and_tail>` `<stmt_bool_or_tail_opt>` ) `<stmt_paren_any_cont>` | FIRST(&&) | { && } |
| 1044 | `<stmt_paren_id_after_postfix>` → || `<stmt_bool_term>` `<stmt_bool_or_tail>` ) `<stmt_paren_any_cont>` | FIRST(||) | { || } |
| 1045 | `<stmt_paren_id_after_postfix>` → ) `<stmt_paren_any_cont>` | FIRST()) | { ) } |
| 1046 | `<stmt_paren_any_cont>` → `<stmt_arith_ops>` `<stmt_after_arith>` | FIRST(`<stmt_arith_ops>`) | { %, *, +, -, / } |
| 1047 | `<stmt_paren_any_cont>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` `<stmt_bool_tail_opt>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1048 | `<stmt_paren_any_cont>` → .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` | FIRST(..) | { .. } |
| 1049 | `<stmt_paren_any_cont>` → `<stmt_bool_tail_opt>` | FIRST(`<stmt_bool_tail_opt>`) | { &&, ), ;, || } |
| 1050 | `<stmt_concat_tail_typed>` → .. `<stmt_string_operand>` `<stmt_concat_tail_typed>` | FIRST(..) | { .. } |
| 1051 | `<stmt_concat_tail_typed>` → λ | FOLLOW(`<stmt_concat_tail_typed>`) | { ), ; } |
| 1052 | `<stmt_string_operand>` → stringlit | FIRST(stringlit) | { stringlit } |
| 1053 | `<stmt_string_operand>` → charlit | FIRST(charlit) | { charlit } |
| 1054 | `<stmt_string_operand>` → id | FIRST(id) | { id } |
| 1055 | `<stmt_string_operand>` → string ( `<arg_expr>` ) | FIRST(string) | { string } |
| 1056 | `<stmt_string_operand>` → char ( `<arg_expr>` ) | FIRST(char) | { char } |
| 1057 | `<stmt_string_operand>` → ( `<stmt_string_operand>` `<stmt_concat_tail_typed>` ) | FIRST(() | { ( } |
| 1058 | `<stmt_string_operand>` → intlit | FIRST(intlit) | { intlit } |
| 1059 | `<stmt_string_operand>` → longlit | FIRST(longlit) | { longlit } |
| 1060 | `<stmt_string_operand>` → floatlit | FIRST(floatlit) | { floatlit } |
| 1061 | `<stmt_string_operand>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1062 | `<stmt_string_operand>` → true | FIRST(true) | { true } |
| 1063 | `<stmt_string_operand>` → false | FIRST(false) | { false } |
| 1064 | `<stmt_string_operand>` → int ( `<arg_expr>` ) | FIRST(int) | { int } |
| 1065 | `<stmt_string_operand>` → long ( `<arg_expr>` ) | FIRST(long) | { long } |
| 1066 | `<stmt_string_operand>` → float ( `<arg_expr>` ) | FIRST(float) | { float } |
| 1067 | `<stmt_string_operand>` → double ( `<arg_expr>` ) | FIRST(double) | { double } |
| 1068 | `<stmt_string_operand>` → bool ( `<arg_expr>` ) | FIRST(bool) | { bool } |
| 1069 | `<stmt_bool_term>` → `<stmt_bool_eq>` `<stmt_bool_and_tail>` | FIRST(`<stmt_bool_eq>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1070 | `<stmt_bool_and_tail>` → && `<stmt_bool_eq>` `<stmt_bool_and_tail>` | FIRST(&&) | { && } |
| 1071 | `<stmt_bool_and_tail>` → λ | FOLLOW(`<stmt_bool_and_tail>`) | { &&, ), ;, || } |
| 1072 | `<stmt_bool_or_tail>` → || `<stmt_bool_term>` `<stmt_bool_or_tail>` | FIRST(||) | { || } |
| 1073 | `<stmt_bool_or_tail>` → λ | FOLLOW(`<stmt_bool_or_tail>`) | { ), ; } |
| 1074 | `<stmt_bool_eq>` → `<stmt_bool_factor>` `<stmt_bool_eq_tail>` | FIRST(`<stmt_bool_factor>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1075 | `<stmt_bool_eq_tail>` → == `<stmt_bool_factor>` `<stmt_bool_eq_tail>` | FIRST(==) | { == } |
| 1076 | `<stmt_bool_eq_tail>` → != `<stmt_bool_factor>` `<stmt_bool_eq_tail>` | FIRST(!=) | { != } |
| 1077 | `<stmt_bool_eq_tail>` → λ | FOLLOW(`<stmt_bool_eq_tail>`) | { &&, ), ;, || } |
| 1078 | `<stmt_bool_factor>` → ! `<stmt_bool_factor>` | FIRST(!) | { ! } |
| 1079 | `<stmt_bool_factor>` → `<stmt_bool_atom>` | FIRST(`<stmt_bool_atom>`) | { (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1080 | `<stmt_bool_atom>` → true | FIRST(true) | { true } |
| 1081 | `<stmt_bool_atom>` → false | FIRST(false) | { false } |
| 1082 | `<stmt_bool_atom>` → id `<stmt_bool_id_cont>` | FIRST(id) | { id } |
| 1083 | `<stmt_bool_atom>` → intlit `<stmt_numeric_cmp_required>` | FIRST(intlit) | { intlit } |
| 1084 | `<stmt_bool_atom>` → longlit `<stmt_numeric_cmp_required>` | FIRST(longlit) | { longlit } |
| 1085 | `<stmt_bool_atom>` → floatlit `<stmt_numeric_cmp_required>` | FIRST(floatlit) | { floatlit } |
| 1086 | `<stmt_bool_atom>` → doublelit `<stmt_numeric_cmp_required>` | FIRST(doublelit) | { doublelit } |
| 1087 | `<stmt_bool_atom>` → - `<stmt_numeric_neg_cmp>` | FIRST(-) | { - } |
| 1088 | `<stmt_bool_atom>` → ( `<stmt_bool_paren>` ) | FIRST(() | { ( } |
| 1089 | `<stmt_bool_atom>` → int ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` | FIRST(int) | { int } |
| 1090 | `<stmt_bool_atom>` → long ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` | FIRST(long) | { long } |
| 1091 | `<stmt_bool_atom>` → float ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` | FIRST(float) | { float } |
| 1092 | `<stmt_bool_atom>` → double ( `<arg_expr>` ) `<stmt_numeric_cmp_required>` | FIRST(double) | { double } |
| 1093 | `<stmt_bool_id_cont>` → `<stmt_numeric_arith_cmp>` | FIRST(`<stmt_numeric_arith_cmp>`) | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1094 | `<stmt_bool_id_cont>` → ++ | FIRST(++) | { ++ } |
| 1095 | `<stmt_bool_id_cont>` → -- | FIRST(--) | { -- } |
| 1096 | `<stmt_bool_id_cont>` → `<stmt_postfix_chain>` | FIRST(`<stmt_postfix_chain>`) | { !=, &&, (, ), ., ;, ==, [, || } |
| 1097 | `<stmt_numeric_arith_cmp>` → + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(+) | { + } |
| 1098 | `<stmt_numeric_arith_cmp>` → - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(-) | { - } |
| 1099 | `<stmt_numeric_arith_cmp>` → * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(*) | { * } |
| 1100 | `<stmt_numeric_arith_cmp>` → / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(/) | { / } |
| 1101 | `<stmt_numeric_arith_cmp>` → % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(%) | { % } |
| 1102 | `<stmt_numeric_arith_cmp>` → `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(`<stmt_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1103 | `<stmt_numeric_add_cmp>` → + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` | FIRST(+) | { + } |
| 1104 | `<stmt_numeric_add_cmp>` → - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` | FIRST(-) | { - } |
| 1105 | `<stmt_numeric_add_cmp>` → λ | FOLLOW(`<stmt_numeric_add_cmp>`) | { !=, <, <=, ==, >, >= } |
| 1106 | `<stmt_numeric_cmp_required>` → `<stmt_numeric_lit_arith>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(`<stmt_numeric_lit_arith>`) | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1107 | `<stmt_numeric_lit_arith>` → * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` | FIRST(*) | { * } |
| 1108 | `<stmt_numeric_lit_arith>` → / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` | FIRST(/) | { / } |
| 1109 | `<stmt_numeric_lit_arith>` → % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` | FIRST(%) | { % } |
| 1110 | `<stmt_numeric_lit_arith>` → + `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` | FIRST(+) | { + } |
| 1111 | `<stmt_numeric_lit_arith>` → - `<numeric_mul_expr_stmt>` `<stmt_numeric_add_cmp>` | FIRST(-) | { - } |
| 1112 | `<stmt_numeric_lit_arith>` → λ | FOLLOW(`<stmt_numeric_lit_arith>`) | { !=, <, <=, ==, >, >= } |
| 1113 | `<stmt_numeric_neg_cmp>` → `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` `<stmt_numeric_add_cmp>` `<stmt_cmp_op>` `<numeric_add_expr_stmt>` | FIRST(`<numeric_unary_expr_stmt>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1114 | `<stmt_cmp_op>` → < | FIRST(<) | { < } |
| 1115 | `<stmt_cmp_op>` → > | FIRST(>) | { > } |
| 1116 | `<stmt_cmp_op>` → <= | FIRST(<=) | { <= } |
| 1117 | `<stmt_cmp_op>` → >= | FIRST(>=) | { >= } |
| 1118 | `<stmt_cmp_op>` → == | FIRST(==) | { == } |
| 1119 | `<stmt_cmp_op>` → != | FIRST(!=) | { != } |
| 1120 | `<stmt_bool_paren>` → `<stmt_bool_term>` `<stmt_bool_and_or_tail>` | FIRST(`<stmt_bool_term>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1121 | `<stmt_bool_and_or_tail>` → && `<stmt_bool_term>` `<stmt_bool_and_or_tail>` | FIRST(&&) | { && } |
| 1122 | `<stmt_bool_and_or_tail>` → || `<stmt_bool_term>` `<stmt_bool_and_or_tail>` | FIRST(||) | { || } |
| 1123 | `<stmt_bool_and_or_tail>` → λ | FOLLOW(`<stmt_bool_and_or_tail>`) | { ) } |
| 1124 | `<numeric_mul_expr_stmt>` → `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` | FIRST(`<numeric_unary_expr_stmt>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1125 | `<numeric_mul_tail_stmt>` → * `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` | FIRST(*) | { * } |
| 1126 | `<numeric_mul_tail_stmt>` → / `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` | FIRST(/) | { / } |
| 1127 | `<numeric_mul_tail_stmt>` → % `<numeric_unary_expr_stmt>` `<numeric_mul_tail_stmt>` | FIRST(%) | { % } |
| 1128 | `<numeric_mul_tail_stmt>` → λ | FOLLOW(`<numeric_mul_tail_stmt>`) | { !=, &&, ), +, -, ;, <, <=, ==, >, >=, || } |
| 1129 | `<numeric_add_expr_stmt>` → `<numeric_mul_expr_stmt>` `<numeric_add_tail_stmt>` | FIRST(`<numeric_mul_expr_stmt>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1130 | `<numeric_add_tail_stmt>` → + `<numeric_mul_expr_stmt>` `<numeric_add_tail_stmt>` | FIRST(+) | { + } |
| 1131 | `<numeric_add_tail_stmt>` → - `<numeric_mul_expr_stmt>` `<numeric_add_tail_stmt>` | FIRST(-) | { - } |
| 1132 | `<numeric_add_tail_stmt>` → λ | FOLLOW(`<numeric_add_tail_stmt>`) | { !=, &&, ), ;, ==, || } |
| 1133 | `<numeric_unary_expr_stmt>` → ! `<numeric_unary_expr_stmt>` | FIRST(!) | { ! } |
| 1134 | `<numeric_unary_expr_stmt>` → - `<numeric_unary_expr_stmt>` | FIRST(-) | { - } |
| 1135 | `<numeric_unary_expr_stmt>` → `<numeric_postfix_expr_stmt>` | FIRST(`<numeric_postfix_expr_stmt>`) | { (, ++, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1136 | `<numeric_postfix_expr_stmt>` → ( `<arg_expr>` ) `<stmt_postfix_chain>` | FIRST(() | { ( } |
| 1137 | `<numeric_postfix_expr_stmt>` → int ( `<arg_expr>` ) | FIRST(int) | { int } |
| 1138 | `<numeric_postfix_expr_stmt>` → long ( `<arg_expr>` ) | FIRST(long) | { long } |
| 1139 | `<numeric_postfix_expr_stmt>` → float ( `<arg_expr>` ) | FIRST(float) | { float } |
| 1140 | `<numeric_postfix_expr_stmt>` → double ( `<arg_expr>` ) | FIRST(double) | { double } |
| 1141 | `<numeric_postfix_expr_stmt>` → ++ id | FIRST(++) | { ++ } |
| 1142 | `<numeric_postfix_expr_stmt>` → -- id | FIRST(--) | { -- } |
| 1143 | `<numeric_postfix_expr_stmt>` → id `<stmt_id_postfix>` | FIRST(id) | { id } |
| 1144 | `<numeric_postfix_expr_stmt>` → intlit | FIRST(intlit) | { intlit } |
| 1145 | `<numeric_postfix_expr_stmt>` → longlit | FIRST(longlit) | { longlit } |
| 1146 | `<numeric_postfix_expr_stmt>` → floatlit | FIRST(floatlit) | { floatlit } |
| 1147 | `<numeric_postfix_expr_stmt>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1148 | `<stmt_id_postfix>` → ++ | FIRST(++) | { ++ } |
| 1149 | `<stmt_id_postfix>` → -- | FIRST(--) | { -- } |
| 1150 | `<stmt_id_postfix>` → `<stmt_postfix_chain>` | FIRST(`<stmt_postfix_chain>`) | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, [, || } |
| 1151 | `<stmt_postfix_chain>` → `<stmt_array_access>` `<stmt_postfix_after_arr>` | FIRST(`<stmt_array_access>`) | { [ } |
| 1152 | `<stmt_postfix_chain>` → . id `<stmt_postfix_chain>` | FIRST(.) | { . } |
| 1153 | `<stmt_postfix_chain>` → ( `<stmt_arg_list>` ) `<stmt_postfix_chain>` | FIRST(() | { ( } |
| 1154 | `<stmt_postfix_chain>` → λ | FOLLOW(`<stmt_postfix_chain>`) | { !=, %, &&, ), *, +, -, .., /, ;, <, <=, ==, >, >=, || } |
| 1155 | `<stmt_array_access>` → [ `<stmt_array_index>` ] `<stmt_array_access_dim2>` | FIRST([) | { [ } |
| 1156 | `<stmt_array_access_dim2>` → [ `<stmt_array_index>` ] | FIRST([) | { [ } |
| 1157 | `<stmt_array_access_dim2>` → λ | FOLLOW(`<stmt_array_access_dim2>`) | { !=, %, &&, (, ), *, +, -, ., .., /, ;, <, <=, ==, >, >=, || } |
| 1158 | `<stmt_postfix_after_arr>` → . id `<stmt_postfix_chain>` | FIRST(.) | { . } |
| 1159 | `<stmt_postfix_after_arr>` → ( `<stmt_arg_list>` ) `<stmt_postfix_chain>` | FIRST(() | { ( } |
| 1160 | `<stmt_postfix_after_arr>` → λ | FOLLOW(`<stmt_postfix_after_arr>`) | { !=, %, &&, ), *, +, -, .., /, ;, <, <=, ==, >, >=, || } |
| 1161 | `<stmt_array_index>` → intlit | FIRST(intlit) | { intlit } |
| 1162 | `<stmt_array_index>` → id | FIRST(id) | { id } |
| 1163 | `<stmt_arg_list>` → `<arg_expr>` `<stmt_arg_tail>` | FIRST(`<arg_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1164 | `<stmt_arg_list>` → λ | FOLLOW(`<stmt_arg_list>`) | { ) } |
| 1165 | `<stmt_arg_tail>` → , `<arg_expr>` `<stmt_arg_tail>` | FIRST(,) | { , } |
| 1166 | `<stmt_arg_tail>` → λ | FOLLOW(`<stmt_arg_tail>`) | { ) } |
| 1167 | `<arg_expr>` → `<arg_typed_rhs>` `<arg_assign_tail>` | FIRST(`<arg_typed_rhs>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1168 | `<arg_assign_tail>` → `<assign_op>` `<arg_typed_rhs>` | FIRST(`<assign_op>`) | { %=, *=, +=, -=, /=, = } |
| 1169 | `<arg_assign_tail>` → λ | FOLLOW(`<arg_assign_tail>`) | { ), ,, ] } |
| 1170 | `<arg_typed_rhs>` → `<arg_bool_or_concat>` | FIRST(`<arg_bool_or_concat>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1171 | `<arg_bool_or_concat>` → stringlit `<arg_concat_tail_typed>` | FIRST(stringlit) | { stringlit } |
| 1172 | `<arg_bool_or_concat>` → charlit `<arg_concat_tail_typed>` | FIRST(charlit) | { charlit } |
| 1173 | `<arg_bool_or_concat>` → string ( `<arg_expr>` ) `<arg_concat_tail_typed>` | FIRST(string) | { string } |
| 1174 | `<arg_bool_or_concat>` → intlit `<arg_numeric_or_bool>` | FIRST(intlit) | { intlit } |
| 1175 | `<arg_bool_or_concat>` → longlit `<arg_numeric_or_bool>` | FIRST(longlit) | { longlit } |
| 1176 | `<arg_bool_or_concat>` → floatlit `<arg_numeric_or_bool>` | FIRST(floatlit) | { floatlit } |
| 1177 | `<arg_bool_or_concat>` → doublelit `<arg_numeric_or_bool>` | FIRST(doublelit) | { doublelit } |
| 1178 | `<arg_bool_or_concat>` → - `<arg_neg_numeric_or_bool>` | FIRST(-) | { - } |
| 1179 | `<arg_bool_or_concat>` → true `<arg_bool_tail_opt>` | FIRST(true) | { true } |
| 1180 | `<arg_bool_or_concat>` → false `<arg_bool_tail_opt>` | FIRST(false) | { false } |
| 1181 | `<arg_bool_or_concat>` → ! `<arg_bool_factor>` `<arg_bool_tail_opt>` | FIRST(!) | { ! } |
| 1182 | `<arg_bool_or_concat>` → int ( `<arg_expr>` ) `<arg_numeric_or_bool>` | FIRST(int) | { int } |
| 1183 | `<arg_bool_or_concat>` → long ( `<arg_expr>` ) `<arg_numeric_or_bool>` | FIRST(long) | { long } |
| 1184 | `<arg_bool_or_concat>` → float ( `<arg_expr>` ) `<arg_numeric_or_bool>` | FIRST(float) | { float } |
| 1185 | `<arg_bool_or_concat>` → double ( `<arg_expr>` ) `<arg_numeric_or_bool>` | FIRST(double) | { double } |
| 1186 | `<arg_bool_or_concat>` → char ( `<arg_expr>` ) | FIRST(char) | { char } |
| 1187 | `<arg_bool_or_concat>` → bool ( `<arg_expr>` ) `<arg_bool_tail_opt>` | FIRST(bool) | { bool } |
| 1188 | `<arg_bool_or_concat>` → id `<arg_id_toplevel_cont>` | FIRST(id) | { id } |
| 1189 | `<arg_bool_or_concat>` → ( `<arg_toplevel_paren>` ) `<arg_toplevel_paren_cont>` | FIRST(() | { ( } |
| 1190 | `<arg_bool_or_concat>` → ++ id | FIRST(++) | { ++ } |
| 1191 | `<arg_bool_or_concat>` → -- id | FIRST(--) | { -- } |
| 1192 | `<arg_numeric_or_bool>` → `<arg_arith_ops>` `<arg_after_arith>` | FIRST(`<arg_arith_ops>`) | { %, *, +, -, / } |
| 1193 | `<arg_numeric_or_bool>` → `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` | FIRST(`<arg_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1194 | `<arg_numeric_or_bool>` → `<arg_bool_tail_opt>` | FIRST(`<arg_bool_tail_opt>`) | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 1195 | `<arg_arith_ops>` → + `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` | FIRST(+) | { + } |
| 1196 | `<arg_arith_ops>` → - `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` | FIRST(-) | { - } |
| 1197 | `<arg_arith_ops>` → * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` | FIRST(*) | { * } |
| 1198 | `<arg_arith_ops>` → / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` | FIRST(/) | { / } |
| 1199 | `<arg_arith_ops>` → % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` | FIRST(%) | { % } |
| 1200 | `<arg_numeric_add_ops>` → + `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` | FIRST(+) | { + } |
| 1201 | `<arg_numeric_add_ops>` → - `<numeric_mul_expr_arg>` `<arg_numeric_add_ops>` | FIRST(-) | { - } |
| 1202 | `<arg_numeric_add_ops>` → λ | FOLLOW(`<arg_numeric_add_ops>`) | { !=, %=, &&, ), *=, +=, ,, -=, /=, <, <=, =, ==, >, >=, ], || } |
| 1203 | `<arg_after_arith>` → `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` | FIRST(`<arg_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1204 | `<arg_after_arith>` → `<arg_bool_tail_opt>` | FIRST(`<arg_bool_tail_opt>`) | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 1205 | `<arg_neg_numeric_or_bool>` → `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_ops>` `<arg_after_arith>` | FIRST(`<numeric_unary_expr_arg>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1206 | `<arg_bool_tail_opt>` → && `<arg_bool_term>` `<arg_bool_and_tail>` `<arg_bool_or_tail_opt>` | FIRST(&&) | { && } |
| 1207 | `<arg_bool_tail_opt>` → || `<arg_bool_term>` `<arg_bool_or_tail>` | FIRST(||) | { || } |
| 1208 | `<arg_bool_tail_opt>` → λ | FOLLOW(`<arg_bool_tail_opt>`) | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 1209 | `<arg_bool_or_tail_opt>` → || `<arg_bool_term>` `<arg_bool_or_tail>` | FIRST(||) | { || } |
| 1210 | `<arg_bool_or_tail_opt>` → λ | FOLLOW(`<arg_bool_or_tail_opt>`) | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 1211 | `<arg_id_toplevel_cont>` → `<arg_arith_ops>` `<arg_after_arith>` | FIRST(`<arg_arith_ops>`) | { %, *, +, -, / } |
| 1212 | `<arg_id_toplevel_cont>` → `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` | FIRST(`<arg_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1213 | `<arg_id_toplevel_cont>` → ++ | FIRST(++) | { ++ } |
| 1214 | `<arg_id_toplevel_cont>` → -- | FIRST(--) | { -- } |
| 1215 | `<arg_id_toplevel_cont>` → `<arg_postfix_chain>` `<arg_id_after_postfix>` | FIRST(`<arg_postfix_chain>`) | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, <, <=, =, ==, >, >=, [, ], || } |
| 1216 | `<arg_id_after_postfix>` → `<arg_arith_ops>` `<arg_after_arith>` | FIRST(`<arg_arith_ops>`) | { %, *, +, -, / } |
| 1217 | `<arg_id_after_postfix>` → `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` | FIRST(`<arg_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1218 | `<arg_id_after_postfix>` → .. `<arg_string_operand>` `<arg_concat_tail_typed>` | FIRST(..) | { .. } |
| 1219 | `<arg_id_after_postfix>` → `<arg_bool_tail_opt>` | FIRST(`<arg_bool_tail_opt>`) | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 1220 | `<arg_toplevel_paren>` → `<arg_bool_or_concat>` | FIRST(`<arg_bool_or_concat>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1221 | `<arg_toplevel_paren_cont>` → `<arg_arith_ops>` `<arg_after_arith>` | FIRST(`<arg_arith_ops>`) | { %, *, +, -, / } |
| 1222 | `<arg_toplevel_paren_cont>` → `<arg_cmp_op>` `<numeric_add_expr_arg>` `<arg_bool_tail_opt>` | FIRST(`<arg_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1223 | `<arg_toplevel_paren_cont>` → .. `<arg_string_operand>` `<arg_concat_tail_typed>` | FIRST(..) | { .. } |
| 1224 | `<arg_toplevel_paren_cont>` → `<arg_bool_tail_opt>` | FIRST(`<arg_bool_tail_opt>`) | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 1225 | `<arg_concat_tail_typed>` → .. `<arg_string_operand>` `<arg_concat_tail_typed>` | FIRST(..) | { .. } |
| 1226 | `<arg_concat_tail_typed>` → λ | FOLLOW(`<arg_concat_tail_typed>`) | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 1227 | `<arg_string_operand>` → stringlit | FIRST(stringlit) | { stringlit } |
| 1228 | `<arg_string_operand>` → charlit | FIRST(charlit) | { charlit } |
| 1229 | `<arg_string_operand>` → id | FIRST(id) | { id } |
| 1230 | `<arg_string_operand>` → string ( `<arg_expr>` ) | FIRST(string) | { string } |
| 1231 | `<arg_string_operand>` → char ( `<arg_expr>` ) | FIRST(char) | { char } |
| 1232 | `<arg_string_operand>` → ( `<arg_string_operand>` `<arg_concat_tail_typed>` ) | FIRST(() | { ( } |
| 1233 | `<arg_bool_term>` → `<arg_bool_eq>` `<arg_bool_and_tail>` | FIRST(`<arg_bool_eq>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1234 | `<arg_bool_and_tail>` → && `<arg_bool_eq>` `<arg_bool_and_tail>` | FIRST(&&) | { && } |
| 1235 | `<arg_bool_and_tail>` → λ | FOLLOW(`<arg_bool_and_tail>`) | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 1236 | `<arg_bool_or_tail>` → || `<arg_bool_term>` `<arg_bool_or_tail>` | FIRST(||) | { || } |
| 1237 | `<arg_bool_or_tail>` → λ | FOLLOW(`<arg_bool_or_tail>`) | { %=, ), *=, +=, ,, -=, /=, =, ] } |
| 1238 | `<arg_bool_eq>` → `<arg_bool_factor>` `<arg_bool_eq_tail>` | FIRST(`<arg_bool_factor>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1239 | `<arg_bool_eq_tail>` → == `<arg_bool_factor>` `<arg_bool_eq_tail>` | FIRST(==) | { == } |
| 1240 | `<arg_bool_eq_tail>` → != `<arg_bool_factor>` `<arg_bool_eq_tail>` | FIRST(!=) | { != } |
| 1241 | `<arg_bool_eq_tail>` → λ | FOLLOW(`<arg_bool_eq_tail>`) | { %=, &&, ), *=, +=, ,, -=, /=, =, ], || } |
| 1242 | `<arg_bool_factor>` → ! `<arg_bool_factor>` | FIRST(!) | { ! } |
| 1243 | `<arg_bool_factor>` → `<arg_bool_atom>` | FIRST(`<arg_bool_atom>`) | { (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1244 | `<arg_bool_atom>` → true | FIRST(true) | { true } |
| 1245 | `<arg_bool_atom>` → false | FIRST(false) | { false } |
| 1246 | `<arg_bool_atom>` → id `<arg_bool_id_cont>` | FIRST(id) | { id } |
| 1247 | `<arg_bool_atom>` → intlit `<arg_numeric_cmp_required>` | FIRST(intlit) | { intlit } |
| 1248 | `<arg_bool_atom>` → longlit `<arg_numeric_cmp_required>` | FIRST(longlit) | { longlit } |
| 1249 | `<arg_bool_atom>` → floatlit `<arg_numeric_cmp_required>` | FIRST(floatlit) | { floatlit } |
| 1250 | `<arg_bool_atom>` → doublelit `<arg_numeric_cmp_required>` | FIRST(doublelit) | { doublelit } |
| 1251 | `<arg_bool_atom>` → - `<arg_numeric_neg_cmp>` | FIRST(-) | { - } |
| 1252 | `<arg_bool_atom>` → ( `<arg_bool_paren>` ) | FIRST(() | { ( } |
| 1253 | `<arg_bool_atom>` → int ( `<arg_expr>` ) `<arg_numeric_cmp_required>` | FIRST(int) | { int } |
| 1254 | `<arg_bool_atom>` → long ( `<arg_expr>` ) `<arg_numeric_cmp_required>` | FIRST(long) | { long } |
| 1255 | `<arg_bool_atom>` → float ( `<arg_expr>` ) `<arg_numeric_cmp_required>` | FIRST(float) | { float } |
| 1256 | `<arg_bool_atom>` → double ( `<arg_expr>` ) `<arg_numeric_cmp_required>` | FIRST(double) | { double } |
| 1257 | `<arg_bool_paren>` → `<arg_bool_term>` `<arg_bool_and_or_tail>` | FIRST(`<arg_bool_term>`) | { !, (, -, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, true } |
| 1258 | `<arg_bool_and_or_tail>` → && `<arg_bool_term>` `<arg_bool_and_or_tail>` | FIRST(&&) | { && } |
| 1259 | `<arg_bool_and_or_tail>` → || `<arg_bool_term>` `<arg_bool_and_or_tail>` | FIRST(||) | { || } |
| 1260 | `<arg_bool_and_or_tail>` → λ | FOLLOW(`<arg_bool_and_or_tail>`) | { ) } |
| 1261 | `<arg_bool_id_cont>` → `<arg_numeric_arith_cmp>` | FIRST(`<arg_numeric_arith_cmp>`) | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1262 | `<arg_bool_id_cont>` → ++ | FIRST(++) | { ++ } |
| 1263 | `<arg_bool_id_cont>` → -- | FIRST(--) | { -- } |
| 1264 | `<arg_bool_id_cont>` → `<arg_postfix_chain>` | FIRST(`<arg_postfix_chain>`) | { !=, %=, &&, (, ), *=, +=, ,, -=, ., /=, =, ==, [, ], || } |
| 1265 | `<arg_numeric_arith_cmp>` → + `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(+) | { + } |
| 1266 | `<arg_numeric_arith_cmp>` → - `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(-) | { - } |
| 1267 | `<arg_numeric_arith_cmp>` → * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(*) | { * } |
| 1268 | `<arg_numeric_arith_cmp>` → / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(/) | { / } |
| 1269 | `<arg_numeric_arith_cmp>` → % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(%) | { % } |
| 1270 | `<arg_numeric_arith_cmp>` → `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(`<arg_cmp_op>`) | { !=, <, <=, ==, >, >= } |
| 1271 | `<arg_numeric_add_cmp>` → + `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` | FIRST(+) | { + } |
| 1272 | `<arg_numeric_add_cmp>` → - `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` | FIRST(-) | { - } |
| 1273 | `<arg_numeric_add_cmp>` → λ | FOLLOW(`<arg_numeric_add_cmp>`) | { !=, <, <=, ==, >, >= } |
| 1274 | `<arg_numeric_cmp_required>` → `<arg_numeric_lit_arith>` `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(`<arg_numeric_lit_arith>`) | { !=, %, *, +, -, /, <, <=, ==, >, >= } |
| 1275 | `<arg_numeric_lit_arith>` → * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` | FIRST(*) | { * } |
| 1276 | `<arg_numeric_lit_arith>` → / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` | FIRST(/) | { / } |
| 1277 | `<arg_numeric_lit_arith>` → % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` | FIRST(%) | { % } |
| 1278 | `<arg_numeric_lit_arith>` → + `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` | FIRST(+) | { + } |
| 1279 | `<arg_numeric_lit_arith>` → - `<numeric_mul_expr_arg>` `<arg_numeric_add_cmp>` | FIRST(-) | { - } |
| 1280 | `<arg_numeric_lit_arith>` → λ | FOLLOW(`<arg_numeric_lit_arith>`) | { !=, <, <=, ==, >, >= } |
| 1281 | `<arg_numeric_neg_cmp>` → `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` `<arg_numeric_add_cmp>` `<arg_cmp_op>` `<numeric_add_expr_arg>` | FIRST(`<numeric_unary_expr_arg>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1282 | `<arg_cmp_op>` → < | FIRST(<) | { < } |
| 1283 | `<arg_cmp_op>` → > | FIRST(>) | { > } |
| 1284 | `<arg_cmp_op>` → <= | FIRST(<=) | { <= } |
| 1285 | `<arg_cmp_op>` → >= | FIRST(>=) | { >= } |
| 1286 | `<arg_cmp_op>` → == | FIRST(==) | { == } |
| 1287 | `<arg_cmp_op>` → != | FIRST(!=) | { != } |
| 1288 | `<numeric_mul_expr_arg>` → `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` | FIRST(`<numeric_unary_expr_arg>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1289 | `<numeric_mul_tail_arg>` → * `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` | FIRST(*) | { * } |
| 1290 | `<numeric_mul_tail_arg>` → / `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` | FIRST(/) | { / } |
| 1291 | `<numeric_mul_tail_arg>` → % `<numeric_unary_expr_arg>` `<numeric_mul_tail_arg>` | FIRST(%) | { % } |
| 1292 | `<numeric_mul_tail_arg>` → λ | FOLLOW(`<numeric_mul_tail_arg>`) | { !=, %=, &&, ), *=, +, +=, ,, -, -=, /=, <, <=, =, ==, >, >=, ], || } |
| 1293 | `<numeric_add_expr_arg>` → `<numeric_mul_expr_arg>` `<numeric_add_tail_arg>` | FIRST(`<numeric_mul_expr_arg>`) | { !, (, ++, -, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1294 | `<numeric_add_tail_arg>` → + `<numeric_mul_expr_arg>` `<numeric_add_tail_arg>` | FIRST(+) | { + } |
| 1295 | `<numeric_add_tail_arg>` → - `<numeric_mul_expr_arg>` `<numeric_add_tail_arg>` | FIRST(-) | { - } |
| 1296 | `<numeric_add_tail_arg>` → λ | FOLLOW(`<numeric_add_tail_arg>`) | { !=, %=, &&, ), *=, +=, ,, -=, /=, =, ==, ], || } |
| 1297 | `<numeric_unary_expr_arg>` → ! `<numeric_unary_expr_arg>` | FIRST(!) | { ! } |
| 1298 | `<numeric_unary_expr_arg>` → - `<numeric_unary_expr_arg>` | FIRST(-) | { - } |
| 1299 | `<numeric_unary_expr_arg>` → `<numeric_postfix_expr_arg>` | FIRST(`<numeric_postfix_expr_arg>`) | { (, ++, --, double, doublelit, float, floatlit, id, int, intlit, long, longlit } |
| 1300 | `<numeric_postfix_expr_arg>` → ( `<arg_expr>` ) `<arg_postfix_chain>` | FIRST(() | { ( } |
| 1301 | `<numeric_postfix_expr_arg>` → int ( `<arg_expr>` ) | FIRST(int) | { int } |
| 1302 | `<numeric_postfix_expr_arg>` → long ( `<arg_expr>` ) | FIRST(long) | { long } |
| 1303 | `<numeric_postfix_expr_arg>` → float ( `<arg_expr>` ) | FIRST(float) | { float } |
| 1304 | `<numeric_postfix_expr_arg>` → double ( `<arg_expr>` ) | FIRST(double) | { double } |
| 1305 | `<numeric_postfix_expr_arg>` → ++ id | FIRST(++) | { ++ } |
| 1306 | `<numeric_postfix_expr_arg>` → -- id | FIRST(--) | { -- } |
| 1307 | `<numeric_postfix_expr_arg>` → id `<arg_id_postfix>` | FIRST(id) | { id } |
| 1308 | `<numeric_postfix_expr_arg>` → intlit | FIRST(intlit) | { intlit } |
| 1309 | `<numeric_postfix_expr_arg>` → longlit | FIRST(longlit) | { longlit } |
| 1310 | `<numeric_postfix_expr_arg>` → floatlit | FIRST(floatlit) | { floatlit } |
| 1311 | `<numeric_postfix_expr_arg>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1312 | `<arg_id_postfix>` → ++ | FIRST(++) | { ++ } |
| 1313 | `<arg_id_postfix>` → -- | FIRST(--) | { -- } |
| 1314 | `<arg_id_postfix>` → `<arg_postfix_chain>` | FIRST(`<arg_postfix_chain>`) | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., /, /=, <, <=, =, ==, >, >=, [, ], || } |
| 1315 | `<arg_postfix_chain>` → `<arg_array_access>` `<arg_postfix_after_arr>` | FIRST(`<arg_array_access>`) | { [ } |
| 1316 | `<arg_postfix_chain>` → . id `<arg_postfix_chain>` | FIRST(.) | { . } |
| 1317 | `<arg_postfix_chain>` → ( `<arg_nested_list>` ) `<arg_postfix_chain>` | FIRST(() | { ( } |
| 1318 | `<arg_postfix_chain>` → λ | FOLLOW(`<arg_postfix_chain>`) | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, <, <=, =, ==, >, >=, ], || } |
| 1319 | `<arg_array_access>` → [ `<arg_array_index>` ] `<arg_array_access_dim2>` | FIRST([) | { [ } |
| 1320 | `<arg_array_access_dim2>` → [ `<arg_array_index>` ] | FIRST([) | { [ } |
| 1321 | `<arg_array_access_dim2>` → λ | FOLLOW(`<arg_array_access_dim2>`) | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, <, <=, =, ==, >, >=, ], || } |
| 1322 | `<arg_postfix_after_arr>` → . id `<arg_postfix_chain>` | FIRST(.) | { . } |
| 1323 | `<arg_postfix_after_arr>` → ( `<arg_nested_list>` ) `<arg_postfix_chain>` | FIRST(() | { ( } |
| 1324 | `<arg_postfix_after_arr>` → λ | FOLLOW(`<arg_postfix_after_arr>`) | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, <, <=, =, ==, >, >=, ], || } |
| 1325 | `<arg_array_index>` → intlit | FIRST(intlit) | { intlit } |
| 1326 | `<arg_array_index>` → id | FIRST(id) | { id } |
| 1327 | `<arg_nested_list>` → `<arg_expr>` `<arg_nested_tail>` | FIRST(`<arg_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1328 | `<arg_nested_list>` → λ | FOLLOW(`<arg_nested_list>`) | { ) } |
| 1329 | `<arg_nested_tail>` → , `<arg_expr>` `<arg_nested_tail>` | FIRST(,) | { , } |
| 1330 | `<arg_nested_tail>` → λ | FOLLOW(`<arg_nested_tail>`) | { ) } |
| 1331 | `<io_stmt>` → trap ( `<trap_target>` ) ; | FIRST(trap) | { trap } |
| 1332 | `<io_stmt>` → thread ( `<print_args>` ) ; | FIRST(thread) | { thread } |
| 1333 | `<io_stmt>` → threadln ( `<print_args>` ) ; | FIRST(threadln) | { threadln } |
| 1334 | `<trap_target>` → id `<trap_target_tail>` | FIRST(id) | { id } |
| 1335 | `<trap_target_tail>` → [ `<arg_expr>` ] | FIRST([) | { [ } |
| 1336 | `<trap_target_tail>` → . id | FIRST(.) | { . } |
| 1337 | `<trap_target_tail>` → λ | FOLLOW(`<trap_target_tail>`) | { ) } |
| 1338 | `<print_args>` → `<arg_expr>` `<print_tail>` | FIRST(`<arg_expr>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1339 | `<print_tail>` → , `<arg_expr>` `<print_tail>` | FIRST(,) | { , } |
| 1340 | `<print_tail>` → λ | FOLLOW(`<print_tail>`) | { ) } |
| 1341 | `<ctrl_struct>` → if ( `<condition>` ) { `<non_empty_ctrl_stmt_list>` } `<else_opt>` | FIRST(if) | { if } |
| 1342 | `<ctrl_struct>` → switch ( `<arg_expr>` ) { `<case_list>` `<default_opt>` } | FIRST(switch) | { switch } |
| 1343 | `<ctrl_struct>` → for ( `<for_init>` ; `<for_cond>` ; `<for_update>` ) { `<non_empty_loop_ctrl_stmt_list>` } | FIRST(for) | { for } |
| 1344 | `<ctrl_struct>` → while ( `<condition>` ) { `<non_empty_loop_ctrl_stmt_list>` } | FIRST(while) | { while } |
| 1345 | `<ctrl_struct>` → do { `<non_empty_loop_ctrl_stmt_list>` } while ( `<condition>` ) ; | FIRST(do) | { do } |
| 1346 | `<ctrl_stmt_list>` → `<statement_non_return>` `<ctrl_stmt_list>` | FIRST(`<statement_non_return>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1347 | `<ctrl_stmt_list>` → λ | FOLLOW(`<ctrl_stmt_list>`) | { } } |
| 1348 | `<non_empty_ctrl_stmt_list>` → `<statement_non_return>` `<ctrl_stmt_list>` | FIRST(`<statement_non_return>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1349 | `<loop_statement_non_return>` → `<statement_non_return>` | FIRST(`<statement_non_return>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1350 | `<loop_statement_non_return>` → break ; | FIRST(break) | { break } |
| 1351 | `<loop_ctrl_stmt_list>` → `<loop_statement_non_return>` `<loop_ctrl_stmt_list>` | FIRST(`<loop_statement_non_return>`) | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1352 | `<loop_ctrl_stmt_list>` → λ | FOLLOW(`<loop_ctrl_stmt_list>`) | { break, case, default, } } |
| 1353 | `<non_empty_loop_ctrl_stmt_list>` → `<loop_statement_non_return>` `<loop_ctrl_stmt_list>` | FIRST(`<loop_statement_non_return>`) | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1354 | `<else_opt>` → else `<else_body>` | FIRST(else) | { else } |
| 1355 | `<else_opt>` → λ | FOLLOW(`<else_opt>`) | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 1356 | `<else_body>` → { `<non_empty_ctrl_stmt_list>` } | FIRST({) | { { } |
| 1357 | `<else_body>` → if ( `<condition>` ) { `<non_empty_ctrl_stmt_list>` } `<else_opt>` | FIRST(if) | { if } |
| 1358 | `<case_list>` → case `<case_val>` : `<non_empty_loop_ctrl_stmt_list>` `<break_opt>` `<case_list>` | FIRST(case) | { case } |
| 1359 | `<case_list>` → λ | FOLLOW(`<case_list>`) | { default, } } |
| 1360 | `<case_val>` → intlit | FIRST(intlit) | { intlit } |
| 1361 | `<case_val>` → longlit | FIRST(longlit) | { longlit } |
| 1362 | `<case_val>` → charlit | FIRST(charlit) | { charlit } |
| 1363 | `<case_val>` → true | FIRST(true) | { true } |
| 1364 | `<case_val>` → false | FIRST(false) | { false } |
| 1365 | `<default_opt>` → default : `<non_empty_loop_ctrl_stmt_list>` `<break_opt>` | FIRST(default) | { default } |
| 1366 | `<default_opt>` → λ | FOLLOW(`<default_opt>`) | { } } |
| 1367 | `<break_opt>` → break ; | FIRST(break) | { break } |
| 1368 | `<break_opt>` → λ | FOLLOW(`<break_opt>`) | { case, default, } } |
| 1369 | `<for_init>` → local var `<for_init_type>` id = `<for_init_expr>` | FIRST(local) | { local } |
| 1370 | `<for_init>` → id `<for_init_assign_tail>` | FIRST(id) | { id } |
| 1371 | `<for_init>` → λ | FOLLOW(`<for_init>`) | { ; } |
| 1372 | `<for_init_assign_tail>` → `<assign_op>` `<for_init_expr>` | FIRST(`<assign_op>`) | { %=, *=, +=, -=, /=, = } |
| 1373 | `<for_init_expr>` → `<stmt_typed_rhs>` | FIRST(`<stmt_typed_rhs>`) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1374 | `<for_init_type>` → int | FIRST(int) | { int } |
| 1375 | `<for_init_type>` → long | FIRST(long) | { long } |
| 1376 | `<for_init_type>` → float | FIRST(float) | { float } |
| 1377 | `<for_init_type>` → double | FIRST(double) | { double } |
| 1378 | `<for_init_type>` → char | FIRST(char) | { char } |
| 1379 | `<for_init_type>` → string | FIRST(string) | { string } |
| 1380 | `<for_init_type>` → bool | FIRST(bool) | { bool } |
| 1381 | `<for_cond>` → `<condition>` | FIRST(`<condition>`) | { !, (, -, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1382 | `<condition>` → `<cond_or>` | FIRST(`<cond_or>`) | { !, (, -, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1383 | `<cond_or>` → `<cond_and>` `<cond_or_tail>` | FIRST(`<cond_and>`) | { !, (, -, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1384 | `<cond_or_tail>` → || `<cond_and>` `<cond_or_tail>` | FIRST(||) | { || } |
| 1385 | `<cond_or_tail>` → λ | FOLLOW(`<cond_or_tail>`) | { ), ; } |
| 1386 | `<cond_and>` → `<cond_not>` `<cond_and_tail>` | FIRST(`<cond_not>`) | { !, (, -, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1387 | `<cond_and_tail>` → && `<cond_not>` `<cond_and_tail>` | FIRST(&&) | { && } |
| 1388 | `<cond_and_tail>` → λ | FOLLOW(`<cond_and_tail>`) | { ), ;, || } |
| 1389 | `<cond_not>` → ! `<cond_not>` | FIRST(!) | { ! } |
| 1390 | `<cond_not>` → `<cond_atom>` | FIRST(`<cond_atom>`) | { (, -, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1391 | `<cond_atom>` → true | FIRST(true) | { true } |
| 1392 | `<cond_atom>` → false | FIRST(false) | { false } |
| 1393 | `<cond_atom>` → id `<cond_id_cont>` | FIRST(id) | { id } |
| 1394 | `<cond_atom>` → ( `<cond_paren_inner>` ) `<cond_paren_tail>` | FIRST(() | { ( } |
| 1395 | `<cond_atom>` → `<cond_lit_cmp>` | FIRST(`<cond_lit_cmp>`) | { -, doublelit, floatlit, intlit, longlit } |
| 1396 | `<cond_paren_inner>` → `<cond_paren_start>` `<cond_paren_cont>` | FIRST(`<cond_paren_start>`) | { !, (, -, doublelit, false, floatlit, id, intlit, longlit, true } |
| 1397 | `<cond_paren_start>` → id | FIRST(id) | { id } |
| 1398 | `<cond_paren_start>` → intlit | FIRST(intlit) | { intlit } |
| 1399 | `<cond_paren_start>` → longlit | FIRST(longlit) | { longlit } |
| 1400 | `<cond_paren_start>` → floatlit | FIRST(floatlit) | { floatlit } |
| 1401 | `<cond_paren_start>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1402 | `<cond_paren_start>` → true | FIRST(true) | { true } |
| 1403 | `<cond_paren_start>` → false | FIRST(false) | { false } |
| 1404 | `<cond_paren_start>` → ! `<cond_not>` | FIRST(!) | { ! } |
| 1405 | `<cond_paren_start>` → - `<cond_paren_unary>` | FIRST(-) | { - } |
| 1406 | `<cond_paren_start>` → ( `<cond_paren_inner>` ) | FIRST(() | { ( } |
| 1407 | `<cond_paren_cont>` → `<cond_paren_arith_ops>` `<cond_paren_after_arith>` | FIRST(`<cond_paren_arith_ops>`) | { %, *, +, -, / } |
| 1408 | `<cond_paren_cont>` → `<cond_cmp>` `<cond_rhs>` `<cond_paren_logic>` | FIRST(`<cond_cmp>`) | { !=, <, <=, ==, >, >= } |
| 1409 | `<cond_paren_cont>` → `<cond_paren_logic>` | FIRST(`<cond_paren_logic>`) | { &&, ), || } |
| 1410 | `<cond_paren_arith_ops>` → + `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(+) | { + } |
| 1411 | `<cond_paren_arith_ops>` → - `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(-) | { - } |
| 1412 | `<cond_paren_arith_ops>` → * `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(*) | { * } |
| 1413 | `<cond_paren_arith_ops>` → / `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(/) | { / } |
| 1414 | `<cond_paren_arith_ops>` → % `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(%) | { % } |
| 1415 | `<cond_paren_mul_ops>` → * `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(*) | { * } |
| 1416 | `<cond_paren_mul_ops>` → / `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(/) | { / } |
| 1417 | `<cond_paren_mul_ops>` → % `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(%) | { % } |
| 1418 | `<cond_paren_mul_ops>` → + `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(+) | { + } |
| 1419 | `<cond_paren_mul_ops>` → - `<cond_paren_unary>` `<cond_paren_mul_ops>` | FIRST(-) | { - } |
| 1420 | `<cond_paren_mul_ops>` → λ | FOLLOW(`<cond_paren_mul_ops>`) | { !=, ), <, <=, ==, >, >= } |
| 1421 | `<cond_paren_unary>` → - `<cond_paren_unary>` | FIRST(-) | { - } |
| 1422 | `<cond_paren_unary>` → `<cond_paren_primary>` | FIRST(`<cond_paren_primary>`) | { (, doublelit, floatlit, id, intlit, longlit } |
| 1423 | `<cond_paren_primary>` → intlit | FIRST(intlit) | { intlit } |
| 1424 | `<cond_paren_primary>` → longlit | FIRST(longlit) | { longlit } |
| 1425 | `<cond_paren_primary>` → floatlit | FIRST(floatlit) | { floatlit } |
| 1426 | `<cond_paren_primary>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1427 | `<cond_paren_primary>` → id `<cond_rhs_id_tail>` | FIRST(id) | { id } |
| 1428 | `<cond_paren_primary>` → ( `<cond_paren_inner>` ) | FIRST(() | { ( } |
| 1429 | `<cond_paren_after_arith>` → `<cond_cmp>` `<cond_rhs>` `<cond_paren_logic>` | FIRST(`<cond_cmp>`) | { !=, <, <=, ==, >, >= } |
| 1430 | `<cond_paren_after_arith>` → λ | FOLLOW(`<cond_paren_after_arith>`) | { ) } |
| 1431 | `<cond_paren_logic>` → && `<cond_and>` | FIRST(&&) | { && } |
| 1432 | `<cond_paren_logic>` → || `<cond_or>` | FIRST(||) | { || } |
| 1433 | `<cond_paren_logic>` → λ | FOLLOW(`<cond_paren_logic>`) | { ) } |
| 1434 | `<cond_paren_tail>` → `<cond_cmp>` `<cond_rhs>` | FIRST(`<cond_cmp>`) | { !=, <, <=, ==, >, >= } |
| 1435 | `<cond_paren_tail>` → λ | FOLLOW(`<cond_paren_tail>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, || } |
| 1436 | `<cond_id_cont>` → [ `<cond_arr_index>` ] `<cond_id_arr_cont>` | FIRST([) | { [ } |
| 1437 | `<cond_id_cont>` → + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(+) | { + } |
| 1438 | `<cond_id_cont>` → - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(-) | { - } |
| 1439 | `<cond_id_cont>` → * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(*) | { * } |
| 1440 | `<cond_id_cont>` → / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(/) | { / } |
| 1441 | `<cond_id_cont>` → % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(%) | { % } |
| 1442 | `<cond_id_cont>` → < `<cond_rhs>` | FIRST(<) | { < } |
| 1443 | `<cond_id_cont>` → > `<cond_rhs>` | FIRST(>) | { > } |
| 1444 | `<cond_id_cont>` → <= `<cond_rhs>` | FIRST(<=) | { <= } |
| 1445 | `<cond_id_cont>` → >= `<cond_rhs>` | FIRST(>=) | { >= } |
| 1446 | `<cond_id_cont>` → == `<cond_rhs>` | FIRST(==) | { == } |
| 1447 | `<cond_id_cont>` → != `<cond_rhs>` | FIRST(!=) | { != } |
| 1448 | `<cond_id_cont>` → λ | FOLLOW(`<cond_id_cont>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, || } |
| 1449 | `<cond_arr_index>` → `<cond_rhs>` | FIRST(`<cond_rhs>`) | { (, -, doublelit, floatlit, id, intlit, longlit } |
| 1450 | `<cond_id_arr_cont>` → [ `<cond_arr_index>` ] `<cond_id_arr_after>` | FIRST([) | { [ } |
| 1451 | `<cond_id_arr_cont>` → `<cond_id_arr_after>` | FIRST(`<cond_id_arr_after>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, || } |
| 1452 | `<cond_id_arr_after>` → + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(+) | { + } |
| 1453 | `<cond_id_arr_after>` → - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(-) | { - } |
| 1454 | `<cond_id_arr_after>` → * `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(*) | { * } |
| 1455 | `<cond_id_arr_after>` → / `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(/) | { / } |
| 1456 | `<cond_id_arr_after>` → % `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(%) | { % } |
| 1457 | `<cond_id_arr_after>` → < `<cond_rhs>` | FIRST(<) | { < } |
| 1458 | `<cond_id_arr_after>` → > `<cond_rhs>` | FIRST(>) | { > } |
| 1459 | `<cond_id_arr_after>` → <= `<cond_rhs>` | FIRST(<=) | { <= } |
| 1460 | `<cond_id_arr_after>` → >= `<cond_rhs>` | FIRST(>=) | { >= } |
| 1461 | `<cond_id_arr_after>` → == `<cond_rhs>` | FIRST(==) | { == } |
| 1462 | `<cond_id_arr_after>` → != `<cond_rhs>` | FIRST(!=) | { != } |
| 1463 | `<cond_id_arr_after>` → λ | FOLLOW(`<cond_id_arr_after>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, || } |
| 1464 | `<cond_lit_cmp>` → intlit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(intlit) | { intlit } |
| 1465 | `<cond_lit_cmp>` → longlit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(longlit) | { longlit } |
| 1466 | `<cond_lit_cmp>` → floatlit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(floatlit) | { floatlit } |
| 1467 | `<cond_lit_cmp>` → doublelit `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(doublelit) | { doublelit } |
| 1468 | `<cond_lit_cmp>` → - `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` `<cond_cmp>` `<cond_rhs>` | FIRST(-) | { - } |
| 1469 | `<cond_lit_mul>` → * `<cond_lit_unary>` `<cond_lit_mul>` | FIRST(*) | { * } |
| 1470 | `<cond_lit_mul>` → / `<cond_lit_unary>` `<cond_lit_mul>` | FIRST(/) | { / } |
| 1471 | `<cond_lit_mul>` → % `<cond_lit_unary>` `<cond_lit_mul>` | FIRST(%) | { % } |
| 1472 | `<cond_lit_mul>` → λ | FOLLOW(`<cond_lit_mul>`) | { !=, ), +, -, <, <=, ==, >, >= } |
| 1473 | `<cond_lit_add>` → + `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` | FIRST(+) | { + } |
| 1474 | `<cond_lit_add>` → - `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` | FIRST(-) | { - } |
| 1475 | `<cond_lit_add>` → λ | FOLLOW(`<cond_lit_add>`) | { !=, ), <, <=, ==, >, >= } |
| 1476 | `<cond_lit_unary>` → - `<cond_lit_unary>` | FIRST(-) | { - } |
| 1477 | `<cond_lit_unary>` → `<cond_lit_primary>` | FIRST(`<cond_lit_primary>`) | { (, doublelit, floatlit, id, intlit, longlit } |
| 1478 | `<cond_lit_primary>` → intlit | FIRST(intlit) | { intlit } |
| 1479 | `<cond_lit_primary>` → longlit | FIRST(longlit) | { longlit } |
| 1480 | `<cond_lit_primary>` → floatlit | FIRST(floatlit) | { floatlit } |
| 1481 | `<cond_lit_primary>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1482 | `<cond_lit_primary>` → id `<cond_rhs_id_tail>` | FIRST(id) | { id } |
| 1483 | `<cond_lit_primary>` → ( `<cond_lit_expr>` ) | FIRST(() | { ( } |
| 1484 | `<cond_lit_expr>` → `<cond_lit_unary>` `<cond_lit_mul>` `<cond_lit_add>` | FIRST(`<cond_lit_unary>`) | { (, -, doublelit, floatlit, id, intlit, longlit } |
| 1485 | `<cond_rhs>` → `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` | FIRST(`<cond_rhs_unary>`) | { (, -, doublelit, floatlit, id, intlit, longlit } |
| 1486 | `<cond_rhs_unary>` → - `<cond_rhs_unary>` | FIRST(-) | { - } |
| 1487 | `<cond_rhs_unary>` → `<cond_rhs_primary>` | FIRST(`<cond_rhs_primary>`) | { (, doublelit, floatlit, id, intlit, longlit } |
| 1488 | `<cond_rhs_primary>` → intlit | FIRST(intlit) | { intlit } |
| 1489 | `<cond_rhs_primary>` → longlit | FIRST(longlit) | { longlit } |
| 1490 | `<cond_rhs_primary>` → floatlit | FIRST(floatlit) | { floatlit } |
| 1491 | `<cond_rhs_primary>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1492 | `<cond_rhs_primary>` → id `<cond_rhs_id_tail>` | FIRST(id) | { id } |
| 1493 | `<cond_rhs_primary>` → ( `<cond_rhs>` ) | FIRST(() | { ( } |
| 1494 | `<cond_rhs_id_tail>` → [ `<cond_arr_index>` ] `<cond_rhs_arr_tail>` | FIRST([) | { [ } |
| 1495 | `<cond_rhs_id_tail>` → λ | FOLLOW(`<cond_rhs_id_tail>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, ], || } |
| 1496 | `<cond_rhs_arr_tail>` → [ `<cond_arr_index>` ] | FIRST([) | { [ } |
| 1497 | `<cond_rhs_arr_tail>` → λ | FOLLOW(`<cond_rhs_arr_tail>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, ], || } |
| 1498 | `<cond_rhs_mul>` → * `<cond_rhs_unary>` `<cond_rhs_mul>` | FIRST(*) | { * } |
| 1499 | `<cond_rhs_mul>` → / `<cond_rhs_unary>` `<cond_rhs_mul>` | FIRST(/) | { / } |
| 1500 | `<cond_rhs_mul>` → % `<cond_rhs_unary>` `<cond_rhs_mul>` | FIRST(%) | { % } |
| 1501 | `<cond_rhs_mul>` → λ | FOLLOW(`<cond_rhs_mul>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, ], || } |
| 1502 | `<cond_rhs_add>` → + `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` | FIRST(+) | { + } |
| 1503 | `<cond_rhs_add>` → - `<cond_rhs_unary>` `<cond_rhs_mul>` `<cond_rhs_add>` | FIRST(-) | { - } |
| 1504 | `<cond_rhs_add>` → λ | FOLLOW(`<cond_rhs_add>`) | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, ], || } |
| 1505 | `<cond_cmp>` → < | FIRST(<) | { < } |
| 1506 | `<cond_cmp>` → > | FIRST(>) | { > } |
| 1507 | `<cond_cmp>` → <= | FIRST(<=) | { <= } |
| 1508 | `<cond_cmp>` → >= | FIRST(>=) | { >= } |
| 1509 | `<cond_cmp>` → == | FIRST(==) | { == } |
| 1510 | `<cond_cmp>` → != | FIRST(!=) | { != } |
| 1511 | `<for_update>` → id `<for_update_tail>` | FIRST(id) | { id } |
| 1512 | `<for_update>` → ++ id | FIRST(++) | { ++ } |
| 1513 | `<for_update>` → -- id | FIRST(--) | { -- } |
| 1514 | `<for_update>` → λ | FOLLOW(`<for_update>`) | { ) } |
| 1515 | `<for_update_tail>` → ++ | FIRST(++) | { ++ } |
| 1516 | `<for_update_tail>` → -- | FIRST(--) | { -- } |
| 1517 | `<for_update_tail>` → `<assign_op>` `<arg_expr>` | FIRST(`<assign_op>`) | { %=, *=, +=, -=, /=, = } |
| 1518 | `<main_body>` → `<main_content>` | FIRST(`<main_content>`) | { ++, --, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 1519 | `<main_content>` → using id `<using_cont>` ; `<main_content>` | FIRST(using) | { using } |
| 1520 | `<main_content>` → local `<mutability>` `<local_dec_body>` `<main_content>` | FIRST(local) | { local } |
| 1521 | `<main_content>` → `<statement_non_return>` `<main_content>` | FIRST(`<statement_non_return>`) | { ++, --, do, for, id, if, switch, thread, threadln, trap, while } |
| 1522 | `<main_content>` → return intlit ; | FIRST(return) | { return } |