## PREDICT Set

| # | Nonterminal | -> | RHS | PREDICT Set |
|---|-------------|----|----|-------------|
| 1 | `<program>` | -> | <decl_list> | { bool, char, double, float, func, global, id, int, long, string, weave } |
| 2 | `<decl_list>` | -> | int <int_decl_or_main> | { int } |
| 3 | `<decl_list>` | -> | <other_decl> <decl_list> | { bool, char, double, float, func, global, id, long, string, weave } |
| 4 | `<int_decl_or_main>` | -> | id <int_decl_tail> <decl_list> | { id } |
| 5 | `<int_decl_or_main>` | -> | main ( ) { <main_body> } | { main } |
| 6 | `<other_decl>` | -> | global <mutability> int id = intlit <int_global_cont> ; | { global } |
| 7 | `<other_decl>` | -> | global <mutability> long id = longlit <long_global_cont> ; | { global } |
| 8 | `<other_decl>` | -> | global <mutability> float id = floatlit <float_global_cont> ; | { global } |
| 9 | `<other_decl>` | -> | global <mutability> double id = doublelit <double_global_cont> ; | { global } |
| 10 | `<other_decl>` | -> | global <mutability> char id = charlit <char_global_cont> ; | { global } |
| 11 | `<other_decl>` | -> | global <mutability> string id = stringlit <string_global_cont> ; | { global } |
| 12 | `<other_decl>` | -> | global <mutability> bool id = <bool_lit> <bool_global_cont> ; | { global } |
| 13 | `<other_decl>` | -> | long id <long_decl_tail> | { long } |
| 14 | `<other_decl>` | -> | float id <float_decl_tail> | { float } |
| 15 | `<other_decl>` | -> | double id <double_decl_tail> | { double } |
| 16 | `<other_decl>` | -> | char id <char_decl_tail> | { char } |
| 17 | `<other_decl>` | -> | string id <string_decl_tail> | { string } |
| 18 | `<other_decl>` | -> | bool id <bool_decl_tail> | { bool } |
| 19 | `<other_decl>` | -> | weave id { <field_list> } ; | { weave } |
| 20 | `<other_decl>` | -> | id <weave_inst_decl> | { id } |
| 21 | `<other_decl>` | -> | func int <func_ret_int> | { func } |
| 22 | `<other_decl>` | -> | func long <func_ret_long> | { func } |
| 23 | `<other_decl>` | -> | func float <func_ret_float> | { func } |
| 24 | `<other_decl>` | -> | func double <func_ret_double> | { func } |
| 25 | `<other_decl>` | -> | func char <func_ret_char> | { func } |
| 26 | `<other_decl>` | -> | func string <func_ret_string> | { func } |
| 27 | `<other_decl>` | -> | func bool <func_ret_bool> | { func } |
| 28 | `<other_decl>` | -> | func id <func_ret_weave> | { func } |
| 29 | `<other_decl>` | -> | func void id ( ) { <function_body_void> } | { func } |
| 30 | `<bool_lit>` | -> | true | { true } |
| 31 | `<bool_lit>` | -> | false | { false } |
| 32 | `<int_global_cont>` | -> | , id = intlit <int_global_cont> | { , } |
| 33 | `<int_global_cont>` | -> | λ | { ; } |
| 34 | `<long_global_cont>` | -> | , id = longlit <long_global_cont> | { , } |
| 35 | `<long_global_cont>` | -> | λ | { ; } |
| 36 | `<float_global_cont>` | -> | , id = floatlit <float_global_cont> | { , } |
| 37 | `<float_global_cont>` | -> | λ | { ; } |
| 38 | `<double_global_cont>` | -> | , id = doublelit <double_global_cont> | { , } |
| 39 | `<double_global_cont>` | -> | λ | { ; } |
| 40 | `<char_global_cont>` | -> | , id = charlit <char_global_cont> | { , } |
| 41 | `<char_global_cont>` | -> | λ | { ; } |
| 42 | `<string_global_cont>` | -> | , id = stringlit <string_global_cont> | { , } |
| 43 | `<string_global_cont>` | -> | λ | { ; } |
| 44 | `<bool_global_cont>` | -> | , id = <bool_lit> <bool_global_cont> | { , } |
| 45 | `<bool_global_cont>` | -> | λ | { ; } |
| 46 | `<int_decl_tail>` | -> | <int_array_with_init> ; | { [ } |
| 47 | `<int_decl_tail>` | -> | = intlit <int_multi_decl> ; | { = } |
| 48 | `<int_multi_decl>` | -> | , id = intlit <int_multi_decl> | { , } |
| 49 | `<int_multi_decl>` | -> | λ | { ; } |
| 50 | `<long_decl_tail>` | -> | <long_array_with_init> ; | { [ } |
| 51 | `<long_decl_tail>` | -> | = longlit <long_multi_decl> ; | { = } |
| 52 | `<long_multi_decl>` | -> | , id = longlit <long_multi_decl> | { , } |
| 53 | `<long_multi_decl>` | -> | λ | { ; } |
| 54 | `<float_decl_tail>` | -> | <float_array_with_init> ; | { [ } |
| 55 | `<float_decl_tail>` | -> | = floatlit <float_multi_decl> ; | { = } |
| 56 | `<float_multi_decl>` | -> | , id = floatlit <float_multi_decl> | { , } |
| 57 | `<float_multi_decl>` | -> | λ | { ; } |
| 58 | `<double_decl_tail>` | -> | <double_array_with_init> ; | { [ } |
| 59 | `<double_decl_tail>` | -> | = doublelit <double_multi_decl> ; | { = } |
| 60 | `<double_multi_decl>` | -> | , id = doublelit <double_multi_decl> | { , } |
| 61 | `<double_multi_decl>` | -> | λ | { ; } |
| 62 | `<char_decl_tail>` | -> | <char_array_with_init> ; | { [ } |
| 63 | `<char_decl_tail>` | -> | = charlit <char_multi_decl> ; | { = } |
| 64 | `<char_multi_decl>` | -> | , id = charlit <char_multi_decl> | { , } |
| 65 | `<char_multi_decl>` | -> | λ | { ; } |
| 66 | `<string_decl_tail>` | -> | <string_array_with_init> ; | { [ } |
| 67 | `<string_decl_tail>` | -> | = stringlit <string_multi_decl> ; | { = } |
| 68 | `<string_multi_decl>` | -> | , id = stringlit <string_multi_decl> | { , } |
| 69 | `<string_multi_decl>` | -> | λ | { ; } |
| 70 | `<bool_decl_tail>` | -> | <bool_array_with_init> ; | { [ } |
| 71 | `<bool_decl_tail>` | -> | = <bool_lit> <bool_multi_decl> ; | { = } |
| 72 | `<bool_multi_decl>` | -> | , id = <bool_lit> <bool_multi_decl> | { , } |
| 73 | `<bool_multi_decl>` | -> | λ | { ; } |
| 74 | `<weave_inst_decl>` | -> | id <weave_inst_tail> <weave_inst_cont> ; | { id } |
| 75 | `<weave_inst_decl>` | -> | <weave_array_with_init> <weave_arr_cont> ; | { [ } |
| 76 | `<weave_inst_tail>` | -> | = { <weave_field_value> <weave_field_list_tail> } | { = } |
| 77 | `<weave_inst_tail>` | -> | <weave_array_with_init> | { [ } |
| 78 | `<weave_field_value>` | -> | intlit | { intlit } |
| 79 | `<weave_field_value>` | -> | longlit | { longlit } |
| 80 | `<weave_field_value>` | -> | floatlit | { floatlit } |
| 81 | `<weave_field_value>` | -> | doublelit | { doublelit } |
| 82 | `<weave_field_value>` | -> | charlit | { charlit } |
| 83 | `<weave_field_value>` | -> | stringlit | { stringlit } |
| 84 | `<weave_field_value>` | -> | true | { true } |
| 85 | `<weave_field_value>` | -> | false | { false } |
| 86 | `<weave_field_value>` | -> | { <weave_value_list> } | { { } |
| 87 | `<weave_value_list>` | -> | <weave_field_value> <weave_value_tail> | { charlit, doublelit, false, floatlit, intlit, longlit, stringlit, true, { } |
| 88 | `<weave_value_tail>` | -> | , <weave_field_value> <weave_value_tail> | { , } |
| 89 | `<weave_value_tail>` | -> | λ | { } } |
| 90 | `<weave_field_list_tail>` | -> | , <weave_field_value> <weave_field_list_tail> | { , } |
| 91 | `<weave_field_list_tail>` | -> | λ | { } } |
| 92 | `<weave_inst_cont>` | -> | , id <weave_inst_tail> <weave_inst_cont> | { , } |
| 93 | `<weave_inst_cont>` | -> | λ | { ; } |
| 94 | `<weave_arr_cont>` | -> | , id <weave_array_with_init> <weave_arr_cont> | { , } |
| 95 | `<weave_arr_cont>` | -> | λ | { ; } |
| 96 | `<weave_array_with_init>` | -> | [ <size> ] <weave_array_init_tail> | { [ } |
| 97 | `<weave_array_init_tail>` | -> | [ <size> ] <weave_arr_init_opt_2d> | { [ } |
| 98 | `<weave_array_init_tail>` | -> | <weave_arr_init_opt_1d> | { ,, ;, = } |
| 99 | `<weave_arr_init_opt_1d>` | -> | = { <weave_arr_init_content_1d> } | { = } |
| 100 | `<weave_arr_init_opt_1d>` | -> | λ | { ,, ; } |
| 101 | `<weave_arr_init_content_1d>` | -> | { <weave_field_value> <weave_field_list_tail> } <weave_init_1d_tail> | { { } |
| 102 | `<weave_init_1d_tail>` | -> | , { <weave_field_value> <weave_field_list_tail> } <weave_init_1d_tail> | { , } |
| 103 | `<weave_init_1d_tail>` | -> | λ | { } } |
| 104 | `<weave_arr_init_opt_2d>` | -> | = { <weave_arr_init_content_2d> } | { = } |
| 105 | `<weave_arr_init_opt_2d>` | -> | λ | { ,, ; } |
| 106 | `<weave_arr_init_content_2d>` | -> | { <weave_init_row> } <weave_init_2d_tail> | { { } |
| 107 | `<weave_init_row>` | -> | { <weave_field_value> <weave_field_list_tail> } <weave_init_1d_tail> | { { } |
| 108 | `<weave_init_2d_tail>` | -> | , { <weave_init_row> } <weave_init_2d_tail> | { , } |
| 109 | `<weave_init_2d_tail>` | -> | λ | { } } |
| 110 | `<mutability>` | -> | var | { var } |
| 111 | `<mutability>` | -> | const | { const } |
| 112 | `<array_dims>` | -> | [ <size> ] <array_dim2_opt> | { [ } |
| 113 | `<array_dim2_opt>` | -> | [ <size> ] | { [ } |
| 114 | `<array_dim2_opt>` | -> | λ | { ), ,, ;, id } |
| 115 | `<size>` | -> | intlit | { intlit } |
| 116 | `<size>` | -> | id | { id } |
| 117 | `<int_array_with_init>` | -> | [ <size> ] <int_array_init_tail> | { [ } |
| 118 | `<int_array_init_tail>` | -> | [ <size> ] <int_arr_init_opt_2d> | { [ } |
| 119 | `<int_array_init_tail>` | -> | <int_arr_init_opt_1d> | { ;, = } |
| 120 | `<int_arr_init_opt_1d>` | -> | = { <int_arr_init_content_1d> } | { = } |
| 121 | `<int_arr_init_opt_1d>` | -> | λ | { ; } |
| 122 | `<int_arr_init_content_1d>` | -> | intlit <int_elem_1d_tail> | { intlit } |
| 123 | `<int_elem_1d_tail>` | -> | , intlit <int_elem_1d_tail> | { , } |
| 124 | `<int_elem_1d_tail>` | -> | λ | { } } |
| 125 | `<int_arr_init_opt_2d>` | -> | = { <int_arr_init_content_2d> } | { = } |
| 126 | `<int_arr_init_opt_2d>` | -> | λ | { ; } |
| 127 | `<int_arr_init_content_2d>` | -> | { <int_elem_list> } <int_elem_2d_tail> | { { } |
| 128 | `<int_elem_list>` | -> | intlit <int_elem_1d_tail> | { intlit } |
| 129 | `<int_elem_2d_tail>` | -> | , { <int_elem_list> } <int_elem_2d_tail> | { , } |
| 130 | `<int_elem_2d_tail>` | -> | λ | { } } |
| 131 | `<long_array_with_init>` | -> | [ <size> ] <long_array_init_tail> | { [ } |
| 132 | `<long_array_init_tail>` | -> | [ <size> ] <long_arr_init_opt_2d> | { [ } |
| 133 | `<long_array_init_tail>` | -> | <long_arr_init_opt_1d> | { ;, = } |
| 134 | `<long_arr_init_opt_1d>` | -> | = { <long_arr_init_content_1d> } | { = } |
| 135 | `<long_arr_init_opt_1d>` | -> | λ | { ; } |
| 136 | `<long_arr_init_content_1d>` | -> | longlit <long_elem_1d_tail> | { longlit } |
| 137 | `<long_elem_1d_tail>` | -> | , longlit <long_elem_1d_tail> | { , } |
| 138 | `<long_elem_1d_tail>` | -> | λ | { } } |
| 139 | `<long_arr_init_opt_2d>` | -> | = { <long_arr_init_content_2d> } | { = } |
| 140 | `<long_arr_init_opt_2d>` | -> | λ | { ; } |
| 141 | `<long_arr_init_content_2d>` | -> | { <long_elem_list> } <long_elem_2d_tail> | { { } |
| 142 | `<long_elem_list>` | -> | longlit <long_elem_1d_tail> | { longlit } |
| 143 | `<long_elem_2d_tail>` | -> | , { <long_elem_list> } <long_elem_2d_tail> | { , } |
| 144 | `<long_elem_2d_tail>` | -> | λ | { } } |
| 145 | `<float_array_with_init>` | -> | [ <size> ] <float_array_init_tail> | { [ } |
| 146 | `<float_array_init_tail>` | -> | [ <size> ] <float_arr_init_opt_2d> | { [ } |
| 147 | `<float_array_init_tail>` | -> | <float_arr_init_opt_1d> | { ;, = } |
| 148 | `<float_arr_init_opt_1d>` | -> | = { <float_arr_init_content_1d> } | { = } |
| 149 | `<float_arr_init_opt_1d>` | -> | λ | { ; } |
| 150 | `<float_arr_init_content_1d>` | -> | floatlit <float_elem_1d_tail> | { floatlit } |
| 151 | `<float_elem_1d_tail>` | -> | , floatlit <float_elem_1d_tail> | { , } |
| 152 | `<float_elem_1d_tail>` | -> | λ | { } } |
| 153 | `<float_arr_init_opt_2d>` | -> | = { <float_arr_init_content_2d> } | { = } |
| 154 | `<float_arr_init_opt_2d>` | -> | λ | { ; } |
| 155 | `<float_arr_init_content_2d>` | -> | { <float_elem_list> } <float_elem_2d_tail> | { { } |
| 156 | `<float_elem_list>` | -> | floatlit <float_elem_1d_tail> | { floatlit } |
| 157 | `<float_elem_2d_tail>` | -> | , { <float_elem_list> } <float_elem_2d_tail> | { , } |
| 158 | `<float_elem_2d_tail>` | -> | λ | { } } |
| 159 | `<double_array_with_init>` | -> | [ <size> ] <double_array_init_tail> | { [ } |
| 160 | `<double_array_init_tail>` | -> | [ <size> ] <double_arr_init_opt_2d> | { [ } |
| 161 | `<double_array_init_tail>` | -> | <double_arr_init_opt_1d> | { ;, = } |
| 162 | `<double_arr_init_opt_1d>` | -> | = { <double_arr_init_content_1d> } | { = } |
| 163 | `<double_arr_init_opt_1d>` | -> | λ | { ; } |
| 164 | `<double_arr_init_content_1d>` | -> | doublelit <double_elem_1d_tail> | { doublelit } |
| 165 | `<double_elem_1d_tail>` | -> | , doublelit <double_elem_1d_tail> | { , } |
| 166 | `<double_elem_1d_tail>` | -> | λ | { } } |
| 167 | `<double_arr_init_opt_2d>` | -> | = { <double_arr_init_content_2d> } | { = } |
| 168 | `<double_arr_init_opt_2d>` | -> | λ | { ; } |
| 169 | `<double_arr_init_content_2d>` | -> | { <double_elem_list> } <double_elem_2d_tail> | { { } |
| 170 | `<double_elem_list>` | -> | doublelit <double_elem_1d_tail> | { doublelit } |
| 171 | `<double_elem_2d_tail>` | -> | , { <double_elem_list> } <double_elem_2d_tail> | { , } |
| 172 | `<double_elem_2d_tail>` | -> | λ | { } } |
| 173 | `<char_array_with_init>` | -> | [ <size> ] <char_array_init_tail> | { [ } |
| 174 | `<char_array_init_tail>` | -> | [ <size> ] <char_arr_init_opt_2d> | { [ } |
| 175 | `<char_array_init_tail>` | -> | <char_arr_init_opt_1d> | { ;, = } |
| 176 | `<char_arr_init_opt_1d>` | -> | = { <char_arr_init_content_1d> } | { = } |
| 177 | `<char_arr_init_opt_1d>` | -> | λ | { ; } |
| 178 | `<char_arr_init_content_1d>` | -> | charlit <char_elem_1d_tail> | { charlit } |
| 179 | `<char_elem_1d_tail>` | -> | , charlit <char_elem_1d_tail> | { , } |
| 180 | `<char_elem_1d_tail>` | -> | λ | { } } |
| 181 | `<char_arr_init_opt_2d>` | -> | = { <char_arr_init_content_2d> } | { = } |
| 182 | `<char_arr_init_opt_2d>` | -> | λ | { ; } |
| 183 | `<char_arr_init_content_2d>` | -> | { <char_elem_list> } <char_elem_2d_tail> | { { } |
| 184 | `<char_elem_list>` | -> | charlit <char_elem_1d_tail> | { charlit } |
| 185 | `<char_elem_2d_tail>` | -> | , { <char_elem_list> } <char_elem_2d_tail> | { , } |
| 186 | `<char_elem_2d_tail>` | -> | λ | { } } |
| 187 | `<string_array_with_init>` | -> | [ <size> ] <string_array_init_tail> | { [ } |
| 188 | `<string_array_init_tail>` | -> | [ <size> ] <string_arr_init_opt_2d> | { [ } |
| 189 | `<string_array_init_tail>` | -> | <string_arr_init_opt_1d> | { ;, = } |
| 190 | `<string_arr_init_opt_1d>` | -> | = { <string_arr_init_content_1d> } | { = } |
| 191 | `<string_arr_init_opt_1d>` | -> | λ | { ; } |
| 192 | `<string_arr_init_content_1d>` | -> | stringlit <string_elem_1d_tail> | { stringlit } |
| 193 | `<string_elem_1d_tail>` | -> | , stringlit <string_elem_1d_tail> | { , } |
| 194 | `<string_elem_1d_tail>` | -> | λ | { } } |
| 195 | `<string_arr_init_opt_2d>` | -> | = { <string_arr_init_content_2d> } | { = } |
| 196 | `<string_arr_init_opt_2d>` | -> | λ | { ; } |
| 197 | `<string_arr_init_content_2d>` | -> | { <string_elem_list> } <string_elem_2d_tail> | { { } |
| 198 | `<string_elem_list>` | -> | stringlit <string_elem_1d_tail> | { stringlit } |
| 199 | `<string_elem_2d_tail>` | -> | , { <string_elem_list> } <string_elem_2d_tail> | { , } |
| 200 | `<string_elem_2d_tail>` | -> | λ | { } } |
| 201 | `<bool_array_with_init>` | -> | [ <size> ] <bool_array_init_tail> | { [ } |
| 202 | `<bool_array_init_tail>` | -> | [ <size> ] <bool_arr_init_opt_2d> | { [ } |
| 203 | `<bool_array_init_tail>` | -> | <bool_arr_init_opt_1d> | { ;, = } |
| 204 | `<bool_arr_init_opt_1d>` | -> | = { <bool_arr_init_content_1d> } | { = } |
| 205 | `<bool_arr_init_opt_1d>` | -> | λ | { ; } |
| 206 | `<bool_arr_init_content_1d>` | -> | <bool_lit> <bool_elem_1d_tail> | { false, true } |
| 207 | `<bool_elem_1d_tail>` | -> | , <bool_lit> <bool_elem_1d_tail> | { , } |
| 208 | `<bool_elem_1d_tail>` | -> | λ | { } } |
| 209 | `<bool_arr_init_opt_2d>` | -> | = { <bool_arr_init_content_2d> } | { = } |
| 210 | `<bool_arr_init_opt_2d>` | -> | λ | { ; } |
| 211 | `<bool_arr_init_content_2d>` | -> | { <bool_elem_list> } <bool_elem_2d_tail> | { { } |
| 212 | `<bool_elem_list>` | -> | <bool_lit> <bool_elem_1d_tail> | { false, true } |
| 213 | `<bool_elem_2d_tail>` | -> | , { <bool_elem_list> } <bool_elem_2d_tail> | { , } |
| 214 | `<bool_elem_2d_tail>` | -> | λ | { } } |
| 215 | `<field_list>` | -> | <field_dec> <field_list> | { bool, char, double, float, id, int, long, string } |
| 216 | `<field_list>` | -> | λ | { } } |
| 217 | `<field_dec>` | -> | <field_type> id <field_arr_opt> <field_cont> ; | { bool, char, double, float, id, int, long, string } |
| 218 | `<field_type>` | -> | int | { int } |
| 219 | `<field_type>` | -> | long | { long } |
| 220 | `<field_type>` | -> | float | { float } |
| 221 | `<field_type>` | -> | double | { double } |
| 222 | `<field_type>` | -> | char | { char } |
| 223 | `<field_type>` | -> | string | { string } |
| 224 | `<field_type>` | -> | bool | { bool } |
| 225 | `<field_type>` | -> | id | { id } |
| 226 | `<field_arr_opt>` | -> | <array_dims> | { [ } |
| 227 | `<field_arr_opt>` | -> | λ | { ,, ; } |
| 228 | `<field_cont>` | -> | , id <field_arr_opt> <field_cont> | { , } |
| 229 | `<field_cont>` | -> | λ | { ; } |
| 230 | `<func_ret_int>` | -> | id ( <param_list> ) { <function_body_int> } | { id } |
| 231 | `<func_ret_int>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 232 | `<func_ret_long>` | -> | id ( <param_list> ) { <function_body_long> } | { id } |
| 233 | `<func_ret_long>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 234 | `<func_ret_float>` | -> | id ( <param_list> ) { <function_body_float> } | { id } |
| 235 | `<func_ret_float>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 236 | `<func_ret_double>` | -> | id ( <param_list> ) { <function_body_double> } | { id } |
| 237 | `<func_ret_double>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 238 | `<func_ret_char>` | -> | id ( <param_list> ) { <function_body_char> } | { id } |
| 239 | `<func_ret_char>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 240 | `<func_ret_string>` | -> | id ( <param_list> ) { <function_body_string> } | { id } |
| 241 | `<func_ret_string>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 242 | `<func_ret_bool>` | -> | id ( <param_list> ) { <function_body_bool> } | { id } |
| 243 | `<func_ret_bool>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 244 | `<func_ret_weave>` | -> | id ( <param_list> ) { <function_body_weave> } | { id } |
| 245 | `<func_ret_weave>` | -> | <array_dims> id ( <param_list> ) { <function_body_array> } | { [ } |
| 246 | `<func_ret_weave>` | -> | . id id ( <param_list> ) { <function_body_weave> } | { . } |
| 247 | `<param_list>` | -> | <param_type> id <param_arr_opt> <param_cont> | { bool, char, double, float, id, int, long, string } |
| 248 | `<param_list>` | -> | λ | { ) } |
| 249 | `<param_type>` | -> | int | { int } |
| 250 | `<param_type>` | -> | long | { long } |
| 251 | `<param_type>` | -> | float | { float } |
| 252 | `<param_type>` | -> | double | { double } |
| 253 | `<param_type>` | -> | char | { char } |
| 254 | `<param_type>` | -> | string | { string } |
| 255 | `<param_type>` | -> | bool | { bool } |
| 256 | `<param_type>` | -> | id | { id } |
| 257 | `<param_arr_opt>` | -> | <array_dims> | { [ } |
| 258 | `<param_arr_opt>` | -> | λ | { ), , } |
| 259 | `<param_cont>` | -> | , <param_type> id <param_arr_opt> <param_cont> | { , } |
| 260 | `<param_cont>` | -> | λ | { ) } |
| 261 | `<function_body_int>` | -> | <func_content_int> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 262 | `<func_content_int>` | -> | using id <using_cont> ; <func_content_int> | { using } |
| 263 | `<func_content_int>` | -> | local <mutability> <local_dec_body> <func_content_int> | { local } |
| 264 | `<func_content_int>` | -> | <statement_int> <func_content_int> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 265 | `<func_content_int>` | -> | λ | { } } |
| 266 | `<function_body_long>` | -> | <func_content_long> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 267 | `<func_content_long>` | -> | using id <using_cont> ; <func_content_long> | { using } |
| 268 | `<func_content_long>` | -> | local <mutability> <local_dec_body> <func_content_long> | { local } |
| 269 | `<func_content_long>` | -> | <statement_long> <func_content_long> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 270 | `<func_content_long>` | -> | λ | { } } |
| 271 | `<function_body_float>` | -> | <func_content_float> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 272 | `<func_content_float>` | -> | using id <using_cont> ; <func_content_float> | { using } |
| 273 | `<func_content_float>` | -> | local <mutability> <local_dec_body> <func_content_float> | { local } |
| 274 | `<func_content_float>` | -> | <statement_float> <func_content_float> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 275 | `<func_content_float>` | -> | λ | { } } |
| 276 | `<function_body_double>` | -> | <func_content_double> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 277 | `<func_content_double>` | -> | using id <using_cont> ; <func_content_double> | { using } |
| 278 | `<func_content_double>` | -> | local <mutability> <local_dec_body> <func_content_double> | { local } |
| 279 | `<func_content_double>` | -> | <statement_double> <func_content_double> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 280 | `<func_content_double>` | -> | λ | { } } |
| 281 | `<function_body_char>` | -> | <func_content_char> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 282 | `<func_content_char>` | -> | using id <using_cont> ; <func_content_char> | { using } |
| 283 | `<func_content_char>` | -> | local <mutability> <local_dec_body> <func_content_char> | { local } |
| 284 | `<func_content_char>` | -> | <statement_char> <func_content_char> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 285 | `<func_content_char>` | -> | λ | { } } |
| 286 | `<function_body_string>` | -> | <func_content_string> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 287 | `<func_content_string>` | -> | using id <using_cont> ; <func_content_string> | { using } |
| 288 | `<func_content_string>` | -> | local <mutability> <local_dec_body> <func_content_string> | { local } |
| 289 | `<func_content_string>` | -> | <statement_string> <func_content_string> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 290 | `<func_content_string>` | -> | λ | { } } |
| 291 | `<function_body_bool>` | -> | <func_content_bool> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 292 | `<func_content_bool>` | -> | using id <using_cont> ; <func_content_bool> | { using } |
| 293 | `<func_content_bool>` | -> | local <mutability> <local_dec_body> <func_content_bool> | { local } |
| 294 | `<func_content_bool>` | -> | <statement_bool> <func_content_bool> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 295 | `<func_content_bool>` | -> | λ | { } } |
| 296 | `<function_body_array>` | -> | <func_content_array> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 297 | `<func_content_array>` | -> | using id <using_cont> ; <func_content_array> | { using } |
| 298 | `<func_content_array>` | -> | local <mutability> <local_dec_body> <func_content_array> | { local } |
| 299 | `<func_content_array>` | -> | <statement_array> <func_content_array> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 300 | `<func_content_array>` | -> | λ | { } } |
| 301 | `<function_body_weave>` | -> | <func_content_weave> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 302 | `<func_content_weave>` | -> | using id <using_cont> ; <func_content_weave> | { using } |
| 303 | `<func_content_weave>` | -> | local <mutability> <local_dec_body> <func_content_weave> | { local } |
| 304 | `<func_content_weave>` | -> | <statement_weave> <func_content_weave> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 305 | `<func_content_weave>` | -> | λ | { } } |
| 306 | `<function_body_void>` | -> | <func_content_void> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 307 | `<func_content_void>` | -> | using id <using_cont> ; <func_content_void> | { using } |
| 308 | `<func_content_void>` | -> | local <mutability> <local_dec_body> <func_content_void> | { local } |
| 309 | `<func_content_void>` | -> | <statement_void> <func_content_void> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 310 | `<func_content_void>` | -> | λ | { } } |
| 311 | `<statement_int>` | -> | <effect_stmt> ; | { ++, --, id } |
| 312 | `<statement_int>` | -> | <io_stmt> | { thread, threadln, trap } |
| 313 | `<statement_int>` | -> | <ctrl_struct_int> | { do, for, if, switch, while } |
| 314 | `<statement_int>` | -> | break ; | { break } |
| 315 | `<statement_int>` | -> | return <int_return_expr> ; | { return } |
| 316 | `<statement_long>` | -> | <effect_stmt> ; | { ++, --, id } |
| 317 | `<statement_long>` | -> | <io_stmt> | { thread, threadln, trap } |
| 318 | `<statement_long>` | -> | <ctrl_struct_long> | { do, for, if, switch, while } |
| 319 | `<statement_long>` | -> | break ; | { break } |
| 320 | `<statement_long>` | -> | return <long_return_expr> ; | { return } |
| 321 | `<statement_float>` | -> | <effect_stmt> ; | { ++, --, id } |
| 322 | `<statement_float>` | -> | <io_stmt> | { thread, threadln, trap } |
| 323 | `<statement_float>` | -> | <ctrl_struct_float> | { do, for, if, switch, while } |
| 324 | `<statement_float>` | -> | break ; | { break } |
| 325 | `<statement_float>` | -> | return <float_return_expr> ; | { return } |
| 326 | `<statement_double>` | -> | <effect_stmt> ; | { ++, --, id } |
| 327 | `<statement_double>` | -> | <io_stmt> | { thread, threadln, trap } |
| 328 | `<statement_double>` | -> | <ctrl_struct_double> | { do, for, if, switch, while } |
| 329 | `<statement_double>` | -> | break ; | { break } |
| 330 | `<statement_double>` | -> | return <double_return_expr> ; | { return } |
| 331 | `<statement_char>` | -> | <effect_stmt> ; | { ++, --, id } |
| 332 | `<statement_char>` | -> | <io_stmt> | { thread, threadln, trap } |
| 333 | `<statement_char>` | -> | <ctrl_struct_char> | { do, for, if, switch, while } |
| 334 | `<statement_char>` | -> | break ; | { break } |
| 335 | `<statement_char>` | -> | return <char_return_expr> ; | { return } |
| 336 | `<statement_string>` | -> | <effect_stmt> ; | { ++, --, id } |
| 337 | `<statement_string>` | -> | <io_stmt> | { thread, threadln, trap } |
| 338 | `<statement_string>` | -> | <ctrl_struct_string> | { do, for, if, switch, while } |
| 339 | `<statement_string>` | -> | break ; | { break } |
| 340 | `<statement_string>` | -> | return <string_return_expr> ; | { return } |
| 341 | `<statement_bool>` | -> | <effect_stmt> ; | { ++, --, id } |
| 342 | `<statement_bool>` | -> | <io_stmt> | { thread, threadln, trap } |
| 343 | `<statement_bool>` | -> | <ctrl_struct_bool> | { do, for, if, switch, while } |
| 344 | `<statement_bool>` | -> | break ; | { break } |
| 345 | `<statement_bool>` | -> | return <bool_return_expr> ; | { return } |
| 346 | `<statement_array>` | -> | <effect_stmt> ; | { ++, --, id } |
| 347 | `<statement_array>` | -> | <io_stmt> | { thread, threadln, trap } |
| 348 | `<statement_array>` | -> | <ctrl_struct_array> | { do, for, if, switch, while } |
| 349 | `<statement_array>` | -> | break ; | { break } |
| 350 | `<statement_array>` | -> | return id ; | { return } |
| 351 | `<statement_weave>` | -> | <effect_stmt> ; | { ++, --, id } |
| 352 | `<statement_weave>` | -> | <io_stmt> | { thread, threadln, trap } |
| 353 | `<statement_weave>` | -> | <ctrl_struct_weave> | { do, for, if, switch, while } |
| 354 | `<statement_weave>` | -> | break ; | { break } |
| 355 | `<statement_weave>` | -> | return id ; | { return } |
| 356 | `<statement_void>` | -> | <effect_stmt> ; | { ++, --, id } |
| 357 | `<statement_void>` | -> | <io_stmt> | { thread, threadln, trap } |
| 358 | `<statement_void>` | -> | <ctrl_struct_void> | { do, for, if, switch, while } |
| 359 | `<statement_void>` | -> | break ; | { break } |
| 360 | `<statement_void>` | -> | return ; | { return } |
| 361 | `<ctrl_struct_int>` | -> | if ( <condition> ) { <stmt_list_int> } <else_opt_int> | { if } |
| 362 | `<ctrl_struct_int>` | -> | switch ( <arg_expr> ) { <case_list_int> <default_opt_int> } | { switch } |
| 363 | `<ctrl_struct_int>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_int> } | { for } |
| 364 | `<ctrl_struct_int>` | -> | while ( <condition> ) { <stmt_list_int> } | { while } |
| 365 | `<ctrl_struct_int>` | -> | do { <stmt_list_int> } while ( <condition> ) ; | { do } |
| 366 | `<stmt_list_int>` | -> | <statement_int> <stmt_list_int> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 367 | `<stmt_list_int>` | -> | λ | { break, case, default, } } |
| 368 | `<else_opt_int>` | -> | else <else_body_int> | { else } |
| 369 | `<else_opt_int>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 370 | `<else_body_int>` | -> | { <stmt_list_int> } | { { } |
| 371 | `<else_body_int>` | -> | if ( <condition> ) { <stmt_list_int> } <else_opt_int> | { if } |
| 372 | `<case_list_int>` | -> | case <case_val> : <stmt_list_int> <break_opt> <case_list_int> | { case } |
| 373 | `<case_list_int>` | -> | λ | { default, } } |
| 374 | `<default_opt_int>` | -> | default : <stmt_list_int> <break_opt> | { default } |
| 375 | `<default_opt_int>` | -> | λ | { } } |
| 376 | `<ctrl_struct_long>` | -> | if ( <condition> ) { <stmt_list_long> } <else_opt_long> | { if } |
| 377 | `<ctrl_struct_long>` | -> | switch ( <arg_expr> ) { <case_list_long> <default_opt_long> } | { switch } |
| 378 | `<ctrl_struct_long>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_long> } | { for } |
| 379 | `<ctrl_struct_long>` | -> | while ( <condition> ) { <stmt_list_long> } | { while } |
| 380 | `<ctrl_struct_long>` | -> | do { <stmt_list_long> } while ( <condition> ) ; | { do } |
| 381 | `<stmt_list_long>` | -> | <statement_long> <stmt_list_long> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 382 | `<stmt_list_long>` | -> | λ | { break, case, default, } } |
| 383 | `<else_opt_long>` | -> | else <else_body_long> | { else } |
| 384 | `<else_opt_long>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 385 | `<else_body_long>` | -> | { <stmt_list_long> } | { { } |
| 386 | `<else_body_long>` | -> | if ( <condition> ) { <stmt_list_long> } <else_opt_long> | { if } |
| 387 | `<case_list_long>` | -> | case <case_val> : <stmt_list_long> <break_opt> <case_list_long> | { case } |
| 388 | `<case_list_long>` | -> | λ | { default, } } |
| 389 | `<default_opt_long>` | -> | default : <stmt_list_long> <break_opt> | { default } |
| 390 | `<default_opt_long>` | -> | λ | { } } |
| 391 | `<ctrl_struct_float>` | -> | if ( <condition> ) { <stmt_list_float> } <else_opt_float> | { if } |
| 392 | `<ctrl_struct_float>` | -> | switch ( <arg_expr> ) { <case_list_float> <default_opt_float> } | { switch } |
| 393 | `<ctrl_struct_float>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_float> } | { for } |
| 394 | `<ctrl_struct_float>` | -> | while ( <condition> ) { <stmt_list_float> } | { while } |
| 395 | `<ctrl_struct_float>` | -> | do { <stmt_list_float> } while ( <condition> ) ; | { do } |
| 396 | `<stmt_list_float>` | -> | <statement_float> <stmt_list_float> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 397 | `<stmt_list_float>` | -> | λ | { break, case, default, } } |
| 398 | `<else_opt_float>` | -> | else <else_body_float> | { else } |
| 399 | `<else_opt_float>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 400 | `<else_body_float>` | -> | { <stmt_list_float> } | { { } |
| 401 | `<else_body_float>` | -> | if ( <condition> ) { <stmt_list_float> } <else_opt_float> | { if } |
| 402 | `<case_list_float>` | -> | case <case_val> : <stmt_list_float> <break_opt> <case_list_float> | { case } |
| 403 | `<case_list_float>` | -> | λ | { default, } } |
| 404 | `<default_opt_float>` | -> | default : <stmt_list_float> <break_opt> | { default } |
| 405 | `<default_opt_float>` | -> | λ | { } } |
| 406 | `<ctrl_struct_double>` | -> | if ( <condition> ) { <stmt_list_double> } <else_opt_double> | { if } |
| 407 | `<ctrl_struct_double>` | -> | switch ( <arg_expr> ) { <case_list_double> <default_opt_double> } | { switch } |
| 408 | `<ctrl_struct_double>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_double> } | { for } |
| 409 | `<ctrl_struct_double>` | -> | while ( <condition> ) { <stmt_list_double> } | { while } |
| 410 | `<ctrl_struct_double>` | -> | do { <stmt_list_double> } while ( <condition> ) ; | { do } |
| 411 | `<stmt_list_double>` | -> | <statement_double> <stmt_list_double> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 412 | `<stmt_list_double>` | -> | λ | { break, case, default, } } |
| 413 | `<else_opt_double>` | -> | else <else_body_double> | { else } |
| 414 | `<else_opt_double>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 415 | `<else_body_double>` | -> | { <stmt_list_double> } | { { } |
| 416 | `<else_body_double>` | -> | if ( <condition> ) { <stmt_list_double> } <else_opt_double> | { if } |
| 417 | `<case_list_double>` | -> | case <case_val> : <stmt_list_double> <break_opt> <case_list_double> | { case } |
| 418 | `<case_list_double>` | -> | λ | { default, } } |
| 419 | `<default_opt_double>` | -> | default : <stmt_list_double> <break_opt> | { default } |
| 420 | `<default_opt_double>` | -> | λ | { } } |
| 421 | `<ctrl_struct_char>` | -> | if ( <condition> ) { <stmt_list_char> } <else_opt_char> | { if } |
| 422 | `<ctrl_struct_char>` | -> | switch ( <arg_expr> ) { <case_list_char> <default_opt_char> } | { switch } |
| 423 | `<ctrl_struct_char>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_char> } | { for } |
| 424 | `<ctrl_struct_char>` | -> | while ( <condition> ) { <stmt_list_char> } | { while } |
| 425 | `<ctrl_struct_char>` | -> | do { <stmt_list_char> } while ( <condition> ) ; | { do } |
| 426 | `<stmt_list_char>` | -> | <statement_char> <stmt_list_char> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 427 | `<stmt_list_char>` | -> | λ | { break, case, default, } } |
| 428 | `<else_opt_char>` | -> | else <else_body_char> | { else } |
| 429 | `<else_opt_char>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 430 | `<else_body_char>` | -> | { <stmt_list_char> } | { { } |
| 431 | `<else_body_char>` | -> | if ( <condition> ) { <stmt_list_char> } <else_opt_char> | { if } |
| 432 | `<case_list_char>` | -> | case <case_val> : <stmt_list_char> <break_opt> <case_list_char> | { case } |
| 433 | `<case_list_char>` | -> | λ | { default, } } |
| 434 | `<default_opt_char>` | -> | default : <stmt_list_char> <break_opt> | { default } |
| 435 | `<default_opt_char>` | -> | λ | { } } |
| 436 | `<ctrl_struct_string>` | -> | if ( <condition> ) { <stmt_list_string> } <else_opt_string> | { if } |
| 437 | `<ctrl_struct_string>` | -> | switch ( <arg_expr> ) { <case_list_string> <default_opt_string> } | { switch } |
| 438 | `<ctrl_struct_string>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_string> } | { for } |
| 439 | `<ctrl_struct_string>` | -> | while ( <condition> ) { <stmt_list_string> } | { while } |
| 440 | `<ctrl_struct_string>` | -> | do { <stmt_list_string> } while ( <condition> ) ; | { do } |
| 441 | `<stmt_list_string>` | -> | <statement_string> <stmt_list_string> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 442 | `<stmt_list_string>` | -> | λ | { break, case, default, } } |
| 443 | `<else_opt_string>` | -> | else <else_body_string> | { else } |
| 444 | `<else_opt_string>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 445 | `<else_body_string>` | -> | { <stmt_list_string> } | { { } |
| 446 | `<else_body_string>` | -> | if ( <condition> ) { <stmt_list_string> } <else_opt_string> | { if } |
| 447 | `<case_list_string>` | -> | case <case_val> : <stmt_list_string> <break_opt> <case_list_string> | { case } |
| 448 | `<case_list_string>` | -> | λ | { default, } } |
| 449 | `<default_opt_string>` | -> | default : <stmt_list_string> <break_opt> | { default } |
| 450 | `<default_opt_string>` | -> | λ | { } } |
| 451 | `<ctrl_struct_bool>` | -> | if ( <condition> ) { <stmt_list_bool> } <else_opt_bool> | { if } |
| 452 | `<ctrl_struct_bool>` | -> | switch ( <arg_expr> ) { <case_list_bool> <default_opt_bool> } | { switch } |
| 453 | `<ctrl_struct_bool>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_bool> } | { for } |
| 454 | `<ctrl_struct_bool>` | -> | while ( <condition> ) { <stmt_list_bool> } | { while } |
| 455 | `<ctrl_struct_bool>` | -> | do { <stmt_list_bool> } while ( <condition> ) ; | { do } |
| 456 | `<stmt_list_bool>` | -> | <statement_bool> <stmt_list_bool> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 457 | `<stmt_list_bool>` | -> | λ | { break, case, default, } } |
| 458 | `<else_opt_bool>` | -> | else <else_body_bool> | { else } |
| 459 | `<else_opt_bool>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 460 | `<else_body_bool>` | -> | { <stmt_list_bool> } | { { } |
| 461 | `<else_body_bool>` | -> | if ( <condition> ) { <stmt_list_bool> } <else_opt_bool> | { if } |
| 462 | `<case_list_bool>` | -> | case <case_val> : <stmt_list_bool> <break_opt> <case_list_bool> | { case } |
| 463 | `<case_list_bool>` | -> | λ | { default, } } |
| 464 | `<default_opt_bool>` | -> | default : <stmt_list_bool> <break_opt> | { default } |
| 465 | `<default_opt_bool>` | -> | λ | { } } |
| 466 | `<ctrl_struct_array>` | -> | if ( <condition> ) { <stmt_list_array> } <else_opt_array> | { if } |
| 467 | `<ctrl_struct_array>` | -> | switch ( <arg_expr> ) { <case_list_array> <default_opt_array> } | { switch } |
| 468 | `<ctrl_struct_array>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_array> } | { for } |
| 469 | `<ctrl_struct_array>` | -> | while ( <condition> ) { <stmt_list_array> } | { while } |
| 470 | `<ctrl_struct_array>` | -> | do { <stmt_list_array> } while ( <condition> ) ; | { do } |
| 471 | `<stmt_list_array>` | -> | <statement_array> <stmt_list_array> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 472 | `<stmt_list_array>` | -> | λ | { break, case, default, } } |
| 473 | `<else_opt_array>` | -> | else <else_body_array> | { else } |
| 474 | `<else_opt_array>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 475 | `<else_body_array>` | -> | { <stmt_list_array> } | { { } |
| 476 | `<else_body_array>` | -> | if ( <condition> ) { <stmt_list_array> } <else_opt_array> | { if } |
| 477 | `<case_list_array>` | -> | case <case_val> : <stmt_list_array> <break_opt> <case_list_array> | { case } |
| 478 | `<case_list_array>` | -> | λ | { default, } } |
| 479 | `<default_opt_array>` | -> | default : <stmt_list_array> <break_opt> | { default } |
| 480 | `<default_opt_array>` | -> | λ | { } } |
| 481 | `<ctrl_struct_weave>` | -> | if ( <condition> ) { <stmt_list_weave> } <else_opt_weave> | { if } |
| 482 | `<ctrl_struct_weave>` | -> | switch ( <arg_expr> ) { <case_list_weave> <default_opt_weave> } | { switch } |
| 483 | `<ctrl_struct_weave>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_weave> } | { for } |
| 484 | `<ctrl_struct_weave>` | -> | while ( <condition> ) { <stmt_list_weave> } | { while } |
| 485 | `<ctrl_struct_weave>` | -> | do { <stmt_list_weave> } while ( <condition> ) ; | { do } |
| 486 | `<stmt_list_weave>` | -> | <statement_weave> <stmt_list_weave> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 487 | `<stmt_list_weave>` | -> | λ | { break, case, default, } } |
| 488 | `<else_opt_weave>` | -> | else <else_body_weave> | { else } |
| 489 | `<else_opt_weave>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 490 | `<else_body_weave>` | -> | { <stmt_list_weave> } | { { } |
| 491 | `<else_body_weave>` | -> | if ( <condition> ) { <stmt_list_weave> } <else_opt_weave> | { if } |
| 492 | `<case_list_weave>` | -> | case <case_val> : <stmt_list_weave> <break_opt> <case_list_weave> | { case } |
| 493 | `<case_list_weave>` | -> | λ | { default, } } |
| 494 | `<default_opt_weave>` | -> | default : <stmt_list_weave> <break_opt> | { default } |
| 495 | `<default_opt_weave>` | -> | λ | { } } |
| 496 | `<ctrl_struct_void>` | -> | if ( <condition> ) { <stmt_list_void> } <else_opt_void> | { if } |
| 497 | `<ctrl_struct_void>` | -> | switch ( <arg_expr> ) { <case_list_void> <default_opt_void> } | { switch } |
| 498 | `<ctrl_struct_void>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_void> } | { for } |
| 499 | `<ctrl_struct_void>` | -> | while ( <condition> ) { <stmt_list_void> } | { while } |
| 500 | `<ctrl_struct_void>` | -> | do { <stmt_list_void> } while ( <condition> ) ; | { do } |
| 501 | `<stmt_list_void>` | -> | <statement_void> <stmt_list_void> | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 502 | `<stmt_list_void>` | -> | λ | { break, case, default, } } |
| 503 | `<else_opt_void>` | -> | else <else_body_void> | { else } |
| 504 | `<else_opt_void>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 505 | `<else_body_void>` | -> | { <stmt_list_void> } | { { } |
| 506 | `<else_body_void>` | -> | if ( <condition> ) { <stmt_list_void> } <else_opt_void> | { if } |
| 507 | `<case_list_void>` | -> | case <case_val> : <stmt_list_void> <break_opt> <case_list_void> | { case } |
| 508 | `<case_list_void>` | -> | λ | { default, } } |
| 509 | `<default_opt_void>` | -> | default : <stmt_list_void> <break_opt> | { default } |
| 510 | `<default_opt_void>` | -> | λ | { } } |
| 511 | `<int_return_expr>` | -> | <int_ret_assign> | { !, (, ++, --, id, int, intlit } |
| 512 | `<int_ret_assign>` | -> | <int_ret_concat> <assign_tail> | { !, (, ++, --, id, int, intlit } |
| 513 | `<int_ret_concat>` | -> | <int_ret_or> <concat_tail> | { !, (, ++, --, id, int, intlit } |
| 514 | `<int_ret_or>` | -> | <int_ret_and> <or_tail> | { !, (, ++, --, id, int, intlit } |
| 515 | `<int_ret_and>` | -> | <int_ret_eq> <and_tail> | { !, (, ++, --, id, int, intlit } |
| 516 | `<int_ret_eq>` | -> | <int_ret_rel> <eq_tail> | { !, (, ++, --, id, int, intlit } |
| 517 | `<int_ret_rel>` | -> | <int_ret_add> <rel_tail> | { !, (, ++, --, id, int, intlit } |
| 518 | `<int_ret_add>` | -> | <int_ret_mul> <add_tail> | { !, (, ++, --, id, int, intlit } |
| 519 | `<int_ret_mul>` | -> | <int_ret_unary> <mul_tail> | { !, (, ++, --, id, int, intlit } |
| 520 | `<int_ret_unary>` | -> | ! <int_ret_unary> | { ! } |
| 521 | `<int_ret_unary>` | -> | <int_ret_postfix> | { (, ++, --, id, int, intlit } |
| 522 | `<int_ret_postfix>` | -> | intlit | { intlit } |
| 523 | `<int_ret_postfix>` | -> | ++ id | { ++ } |
| 524 | `<int_ret_postfix>` | -> | -- id | { -- } |
| 525 | `<int_ret_postfix>` | -> | id <id_postfix> | { id } |
| 526 | `<int_ret_postfix>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 527 | `<int_ret_postfix>` | -> | int ( <expression> ) | { int } |
| 528 | `<long_return_expr>` | -> | <long_ret_assign> | { !, (, ++, --, id, long, longlit } |
| 529 | `<long_ret_assign>` | -> | <long_ret_concat> <assign_tail> | { !, (, ++, --, id, long, longlit } |
| 530 | `<long_ret_concat>` | -> | <long_ret_or> <concat_tail> | { !, (, ++, --, id, long, longlit } |
| 531 | `<long_ret_or>` | -> | <long_ret_and> <or_tail> | { !, (, ++, --, id, long, longlit } |
| 532 | `<long_ret_and>` | -> | <long_ret_eq> <and_tail> | { !, (, ++, --, id, long, longlit } |
| 533 | `<long_ret_eq>` | -> | <long_ret_rel> <eq_tail> | { !, (, ++, --, id, long, longlit } |
| 534 | `<long_ret_rel>` | -> | <long_ret_add> <rel_tail> | { !, (, ++, --, id, long, longlit } |
| 535 | `<long_ret_add>` | -> | <long_ret_mul> <add_tail> | { !, (, ++, --, id, long, longlit } |
| 536 | `<long_ret_mul>` | -> | <long_ret_unary> <mul_tail> | { !, (, ++, --, id, long, longlit } |
| 537 | `<long_ret_unary>` | -> | ! <long_ret_unary> | { ! } |
| 538 | `<long_ret_unary>` | -> | <long_ret_postfix> | { (, ++, --, id, long, longlit } |
| 539 | `<long_ret_postfix>` | -> | longlit | { longlit } |
| 540 | `<long_ret_postfix>` | -> | ++ id | { ++ } |
| 541 | `<long_ret_postfix>` | -> | -- id | { -- } |
| 542 | `<long_ret_postfix>` | -> | id <id_postfix> | { id } |
| 543 | `<long_ret_postfix>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 544 | `<long_ret_postfix>` | -> | long ( <expression> ) | { long } |
| 545 | `<float_return_expr>` | -> | <float_ret_assign> | { !, (, ++, --, float, floatlit, id } |
| 546 | `<float_ret_assign>` | -> | <float_ret_concat> <assign_tail> | { !, (, ++, --, float, floatlit, id } |
| 547 | `<float_ret_concat>` | -> | <float_ret_or> <concat_tail> | { !, (, ++, --, float, floatlit, id } |
| 548 | `<float_ret_or>` | -> | <float_ret_and> <or_tail> | { !, (, ++, --, float, floatlit, id } |
| 549 | `<float_ret_and>` | -> | <float_ret_eq> <and_tail> | { !, (, ++, --, float, floatlit, id } |
| 550 | `<float_ret_eq>` | -> | <float_ret_rel> <eq_tail> | { !, (, ++, --, float, floatlit, id } |
| 551 | `<float_ret_rel>` | -> | <float_ret_add> <rel_tail> | { !, (, ++, --, float, floatlit, id } |
| 552 | `<float_ret_add>` | -> | <float_ret_mul> <add_tail> | { !, (, ++, --, float, floatlit, id } |
| 553 | `<float_ret_mul>` | -> | <float_ret_unary> <mul_tail> | { !, (, ++, --, float, floatlit, id } |
| 554 | `<float_ret_unary>` | -> | ! <float_ret_unary> | { ! } |
| 555 | `<float_ret_unary>` | -> | <float_ret_postfix> | { (, ++, --, float, floatlit, id } |
| 556 | `<float_ret_postfix>` | -> | floatlit | { floatlit } |
| 557 | `<float_ret_postfix>` | -> | ++ id | { ++ } |
| 558 | `<float_ret_postfix>` | -> | -- id | { -- } |
| 559 | `<float_ret_postfix>` | -> | id <id_postfix> | { id } |
| 560 | `<float_ret_postfix>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 561 | `<float_ret_postfix>` | -> | float ( <expression> ) | { float } |
| 562 | `<double_return_expr>` | -> | <double_ret_assign> | { !, (, ++, --, double, doublelit, id } |
| 563 | `<double_ret_assign>` | -> | <double_ret_concat> <assign_tail> | { !, (, ++, --, double, doublelit, id } |
| 564 | `<double_ret_concat>` | -> | <double_ret_or> <concat_tail> | { !, (, ++, --, double, doublelit, id } |
| 565 | `<double_ret_or>` | -> | <double_ret_and> <or_tail> | { !, (, ++, --, double, doublelit, id } |
| 566 | `<double_ret_and>` | -> | <double_ret_eq> <and_tail> | { !, (, ++, --, double, doublelit, id } |
| 567 | `<double_ret_eq>` | -> | <double_ret_rel> <eq_tail> | { !, (, ++, --, double, doublelit, id } |
| 568 | `<double_ret_rel>` | -> | <double_ret_add> <rel_tail> | { !, (, ++, --, double, doublelit, id } |
| 569 | `<double_ret_add>` | -> | <double_ret_mul> <add_tail> | { !, (, ++, --, double, doublelit, id } |
| 570 | `<double_ret_mul>` | -> | <double_ret_unary> <mul_tail> | { !, (, ++, --, double, doublelit, id } |
| 571 | `<double_ret_unary>` | -> | ! <double_ret_unary> | { ! } |
| 572 | `<double_ret_unary>` | -> | <double_ret_postfix> | { (, ++, --, double, doublelit, id } |
| 573 | `<double_ret_postfix>` | -> | doublelit | { doublelit } |
| 574 | `<double_ret_postfix>` | -> | ++ id | { ++ } |
| 575 | `<double_ret_postfix>` | -> | -- id | { -- } |
| 576 | `<double_ret_postfix>` | -> | id <id_postfix> | { id } |
| 577 | `<double_ret_postfix>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 578 | `<double_ret_postfix>` | -> | double ( <expression> ) | { double } |
| 579 | `<char_return_expr>` | -> | <char_ret_assign> | { !, (, ++, --, char, charlit, id } |
| 580 | `<char_ret_assign>` | -> | <char_ret_concat> <assign_tail> | { !, (, ++, --, char, charlit, id } |
| 581 | `<char_ret_concat>` | -> | <char_ret_or> <concat_tail> | { !, (, ++, --, char, charlit, id } |
| 582 | `<char_ret_or>` | -> | <char_ret_and> <or_tail> | { !, (, ++, --, char, charlit, id } |
| 583 | `<char_ret_and>` | -> | <char_ret_eq> <and_tail> | { !, (, ++, --, char, charlit, id } |
| 584 | `<char_ret_eq>` | -> | <char_ret_rel> <eq_tail> | { !, (, ++, --, char, charlit, id } |
| 585 | `<char_ret_rel>` | -> | <char_ret_add> <rel_tail> | { !, (, ++, --, char, charlit, id } |
| 586 | `<char_ret_add>` | -> | <char_ret_mul> <add_tail> | { !, (, ++, --, char, charlit, id } |
| 587 | `<char_ret_mul>` | -> | <char_ret_unary> <mul_tail> | { !, (, ++, --, char, charlit, id } |
| 588 | `<char_ret_unary>` | -> | ! <char_ret_unary> | { ! } |
| 589 | `<char_ret_unary>` | -> | <char_ret_postfix> | { (, ++, --, char, charlit, id } |
| 590 | `<char_ret_postfix>` | -> | charlit | { charlit } |
| 591 | `<char_ret_postfix>` | -> | ++ id | { ++ } |
| 592 | `<char_ret_postfix>` | -> | -- id | { -- } |
| 593 | `<char_ret_postfix>` | -> | id <id_postfix> | { id } |
| 594 | `<char_ret_postfix>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 595 | `<char_ret_postfix>` | -> | char ( <expression> ) | { char } |
| 596 | `<string_return_expr>` | -> | <string_ret_assign> | { !, (, ++, --, id, string, stringlit } |
| 597 | `<string_ret_assign>` | -> | <string_ret_concat> <assign_tail> | { !, (, ++, --, id, string, stringlit } |
| 598 | `<string_ret_concat>` | -> | <string_ret_or> <concat_tail> | { !, (, ++, --, id, string, stringlit } |
| 599 | `<string_ret_or>` | -> | <string_ret_and> <or_tail> | { !, (, ++, --, id, string, stringlit } |
| 600 | `<string_ret_and>` | -> | <string_ret_eq> <and_tail> | { !, (, ++, --, id, string, stringlit } |
| 601 | `<string_ret_eq>` | -> | <string_ret_rel> <eq_tail> | { !, (, ++, --, id, string, stringlit } |
| 602 | `<string_ret_rel>` | -> | <string_ret_add> <rel_tail> | { !, (, ++, --, id, string, stringlit } |
| 603 | `<string_ret_add>` | -> | <string_ret_mul> <add_tail> | { !, (, ++, --, id, string, stringlit } |
| 604 | `<string_ret_mul>` | -> | <string_ret_unary> <mul_tail> | { !, (, ++, --, id, string, stringlit } |
| 605 | `<string_ret_unary>` | -> | ! <string_ret_unary> | { ! } |
| 606 | `<string_ret_unary>` | -> | <string_ret_postfix> | { (, ++, --, id, string, stringlit } |
| 607 | `<string_ret_postfix>` | -> | stringlit | { stringlit } |
| 608 | `<string_ret_postfix>` | -> | ++ id | { ++ } |
| 609 | `<string_ret_postfix>` | -> | -- id | { -- } |
| 610 | `<string_ret_postfix>` | -> | id <id_postfix> | { id } |
| 611 | `<string_ret_postfix>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 612 | `<string_ret_postfix>` | -> | string ( <expression> ) | { string } |
| 613 | `<bool_return_expr>` | -> | <bool_ret_assign> | { !, (, ++, --, bool, false, id, true } |
| 614 | `<bool_ret_assign>` | -> | <bool_ret_concat> <assign_tail> | { !, (, ++, --, bool, false, id, true } |
| 615 | `<bool_ret_concat>` | -> | <bool_ret_or> <concat_tail> | { !, (, ++, --, bool, false, id, true } |
| 616 | `<bool_ret_or>` | -> | <bool_ret_and> <or_tail> | { !, (, ++, --, bool, false, id, true } |
| 617 | `<bool_ret_and>` | -> | <bool_ret_eq> <and_tail> | { !, (, ++, --, bool, false, id, true } |
| 618 | `<bool_ret_eq>` | -> | <bool_ret_rel> <eq_tail> | { !, (, ++, --, bool, false, id, true } |
| 619 | `<bool_ret_rel>` | -> | <bool_ret_add> <rel_tail> | { !, (, ++, --, bool, false, id, true } |
| 620 | `<bool_ret_add>` | -> | <bool_ret_mul> <add_tail> | { !, (, ++, --, bool, false, id, true } |
| 621 | `<bool_ret_mul>` | -> | <bool_ret_unary> <mul_tail> | { !, (, ++, --, bool, false, id, true } |
| 622 | `<bool_ret_unary>` | -> | ! <bool_ret_unary> | { ! } |
| 623 | `<bool_ret_unary>` | -> | <bool_ret_postfix> | { (, ++, --, bool, false, id, true } |
| 624 | `<bool_ret_postfix>` | -> | true | { true } |
| 625 | `<bool_ret_postfix>` | -> | false | { false } |
| 626 | `<bool_ret_postfix>` | -> | ++ id | { ++ } |
| 627 | `<bool_ret_postfix>` | -> | -- id | { -- } |
| 628 | `<bool_ret_postfix>` | -> | id <id_postfix> | { id } |
| 629 | `<bool_ret_postfix>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 630 | `<bool_ret_postfix>` | -> | bool ( <expression> ) | { bool } |
| 631 | `<using_cont>` | -> | , id <using_cont> | { , } |
| 632 | `<using_cont>` | -> | λ | { ; } |
| 633 | `<local_dec_body>` | -> | int id <int_local_tail> | { int } |
| 634 | `<local_dec_body>` | -> | long id <long_local_tail> | { long } |
| 635 | `<local_dec_body>` | -> | float id <float_local_tail> | { float } |
| 636 | `<local_dec_body>` | -> | double id <double_local_tail> | { double } |
| 637 | `<local_dec_body>` | -> | char id <char_local_tail> | { char } |
| 638 | `<local_dec_body>` | -> | string id <string_local_tail> | { string } |
| 639 | `<local_dec_body>` | -> | bool id <bool_local_tail> | { bool } |
| 640 | `<local_dec_body>` | -> | id id <weave_local_tail> | { id } |
| 641 | `<int_local_tail>` | -> | <int_array_with_init> ; | { [ } |
| 642 | `<int_local_tail>` | -> | = intlit <int_local_cont> ; | { = } |
| 643 | `<int_local_cont>` | -> | , id = intlit <int_local_cont> | { , } |
| 644 | `<int_local_cont>` | -> | λ | { ; } |
| 645 | `<long_local_tail>` | -> | <long_array_with_init> ; | { [ } |
| 646 | `<long_local_tail>` | -> | = longlit <long_local_cont> ; | { = } |
| 647 | `<long_local_cont>` | -> | , id = longlit <long_local_cont> | { , } |
| 648 | `<long_local_cont>` | -> | λ | { ; } |
| 649 | `<float_local_tail>` | -> | <float_array_with_init> ; | { [ } |
| 650 | `<float_local_tail>` | -> | = floatlit <float_local_cont> ; | { = } |
| 651 | `<float_local_cont>` | -> | , id = floatlit <float_local_cont> | { , } |
| 652 | `<float_local_cont>` | -> | λ | { ; } |
| 653 | `<double_local_tail>` | -> | <double_array_with_init> ; | { [ } |
| 654 | `<double_local_tail>` | -> | = doublelit <double_local_cont> ; | { = } |
| 655 | `<double_local_cont>` | -> | , id = doublelit <double_local_cont> | { , } |
| 656 | `<double_local_cont>` | -> | λ | { ; } |
| 657 | `<char_local_tail>` | -> | <char_array_with_init> ; | { [ } |
| 658 | `<char_local_tail>` | -> | = charlit <char_local_cont> ; | { = } |
| 659 | `<char_local_cont>` | -> | , id = charlit <char_local_cont> | { , } |
| 660 | `<char_local_cont>` | -> | λ | { ; } |
| 661 | `<string_local_tail>` | -> | <string_array_with_init> ; | { [ } |
| 662 | `<string_local_tail>` | -> | = stringlit <string_local_cont> ; | { = } |
| 663 | `<string_local_cont>` | -> | , id = stringlit <string_local_cont> | { , } |
| 664 | `<string_local_cont>` | -> | λ | { ; } |
| 665 | `<bool_local_tail>` | -> | <bool_array_with_init> ; | { [ } |
| 666 | `<bool_local_tail>` | -> | = <bool_lit> <bool_local_cont> ; | { = } |
| 667 | `<bool_local_cont>` | -> | , id = <bool_lit> <bool_local_cont> | { , } |
| 668 | `<bool_local_cont>` | -> | λ | { ; } |
| 669 | `<weave_local_tail>` | -> | = { <weave_field_value> <weave_field_list_tail> } <weave_inst_cont> ; | { = } |
| 670 | `<weave_local_tail>` | -> | <weave_array_with_init> <weave_arr_cont> ; | { [ } |
| 671 | `<statement_non_return>` | -> | <effect_stmt> ; | { ++, --, id } |
| 672 | `<statement_non_return>` | -> | <io_stmt> | { thread, threadln, trap } |
| 673 | `<statement_non_return>` | -> | <ctrl_struct> | { do, for, if, switch, while } |
| 674 | `<statement_non_return>` | -> | break ; | { break } |
| 675 | `<ctrl_stmt_list>` | -> | <statement_non_return> <ctrl_stmt_list> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 676 | `<ctrl_stmt_list>` | -> | λ | { break, case, default, } } |
| 677 | `<effect_stmt>` | -> | ++ id <effect_pre_chain> | { ++ } |
| 678 | `<effect_stmt>` | -> | -- id <effect_pre_chain> | { -- } |
| 679 | `<effect_stmt>` | -> | id <effect_id_cont> | { id } |
| 680 | `<effect_pre_chain>` | -> | [ <stmt_array_index> ] <effect_pre_arr_chain> | { [ } |
| 681 | `<effect_pre_chain>` | -> | . id <effect_pre_chain> | { . } |
| 682 | `<effect_pre_chain>` | -> | λ | { ; } |
| 683 | `<effect_pre_arr_chain>` | -> | [ <stmt_array_index> ] | { [ } |
| 684 | `<effect_pre_arr_chain>` | -> | . id <effect_pre_chain> | { . } |
| 685 | `<effect_pre_arr_chain>` | -> | λ | { ; } |
| 686 | `<effect_id_cont>` | -> | <assign_op> <stmt_assign_expr> | { %=, *=, +=, -=, /=, = } |
| 687 | `<effect_id_cont>` | -> | ++ | { ++ } |
| 688 | `<effect_id_cont>` | -> | -- | { -- } |
| 689 | `<effect_id_cont>` | -> | ( <stmt_arg_list> ) <effect_post_call> | { ( } |
| 690 | `<effect_id_cont>` | -> | [ <stmt_array_index> ] <effect_post_arr> | { [ } |
| 691 | `<effect_id_cont>` | -> | . id <effect_post_member> | { . } |
| 692 | `<effect_post_call>` | -> | . id <effect_post_call_member> | { . } |
| 693 | `<effect_post_call>` | -> | [ <stmt_array_index> ] <effect_post_call_arr> | { [ } |
| 694 | `<effect_post_call>` | -> | λ | { ; } |
| 695 | `<effect_post_call_member>` | -> | ( <stmt_arg_list> ) <effect_post_call> | { ( } |
| 696 | `<effect_post_call_member>` | -> | [ <stmt_array_index> ] <effect_post_call_arr> | { [ } |
| 697 | `<effect_post_call_member>` | -> | . id <effect_post_call_member> | { . } |
| 698 | `<effect_post_call_member>` | -> | λ | { ; } |
| 699 | `<effect_post_call_arr>` | -> | [ <stmt_array_index> ] <effect_post_call_arr_cont> | { [ } |
| 700 | `<effect_post_call_arr>` | -> | <effect_post_call_arr_cont> | { (, ., ; } |
| 701 | `<effect_post_call_arr_cont>` | -> | . id <effect_post_call_member> | { . } |
| 702 | `<effect_post_call_arr_cont>` | -> | ( <stmt_arg_list> ) <effect_post_call> | { ( } |
| 703 | `<effect_post_call_arr_cont>` | -> | λ | { ; } |
| 704 | `<effect_post_arr>` | -> | [ <stmt_array_index> ] <effect_post_arr_2d> | { [ } |
| 705 | `<effect_post_arr>` | -> | <effect_arr_effect> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 706 | `<effect_post_arr_2d>` | -> | <effect_arr_effect> | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 707 | `<effect_arr_effect>` | -> | <assign_op> <stmt_assign_expr> | { %=, *=, +=, -=, /=, = } |
| 708 | `<effect_arr_effect>` | -> | ++ | { ++ } |
| 709 | `<effect_arr_effect>` | -> | -- | { -- } |
| 710 | `<effect_arr_effect>` | -> | ( <stmt_arg_list> ) <effect_post_call> | { ( } |
| 711 | `<effect_arr_effect>` | -> | . id <effect_post_member> | { . } |
| 712 | `<effect_post_member>` | -> | <assign_op> <stmt_assign_expr> | { %=, *=, +=, -=, /=, = } |
| 713 | `<effect_post_member>` | -> | ++ | { ++ } |
| 714 | `<effect_post_member>` | -> | -- | { -- } |
| 715 | `<effect_post_member>` | -> | ( <stmt_arg_list> ) <effect_post_call> | { ( } |
| 716 | `<effect_post_member>` | -> | [ <stmt_array_index> ] <effect_post_arr> | { [ } |
| 717 | `<effect_post_member>` | -> | . id <effect_post_member> | { . } |
| 718 | `<stmt_assign_expr>` | -> | <stmt_concat_expr> <stmt_assign_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 719 | `<stmt_assign_tail>` | -> | <assign_op> <stmt_assign_expr> | { %=, *=, +=, -=, /=, = } |
| 720 | `<stmt_assign_tail>` | -> | λ | { ; } |
| 721 | `<stmt_concat_expr>` | -> | <stmt_or_expr> <stmt_concat_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 722 | `<stmt_concat_tail>` | -> | .. <stmt_or_expr> <stmt_concat_tail> | { .. } |
| 723 | `<stmt_concat_tail>` | -> | λ | { %=, *=, +=, -=, /=, ;, = } |
| 724 | `<stmt_or_expr>` | -> | <stmt_and_expr> <stmt_or_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 725 | `<stmt_or_tail>` | -> | \|\| <stmt_and_expr> <stmt_or_tail> | { \|\| } |
| 726 | `<stmt_or_tail>` | -> | λ | { %=, *=, +=, -=, .., /=, ;, = } |
| 727 | `<stmt_and_expr>` | -> | <stmt_eq_expr> <stmt_and_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 728 | `<stmt_and_tail>` | -> | && <stmt_eq_expr> <stmt_and_tail> | { && } |
| 729 | `<stmt_and_tail>` | -> | λ | { %=, *=, +=, -=, .., /=, ;, =, \|\| } |
| 730 | `<stmt_eq_expr>` | -> | <stmt_rel_expr> <stmt_eq_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 731 | `<stmt_eq_tail>` | -> | == <stmt_rel_expr> <stmt_eq_tail> | { == } |
| 732 | `<stmt_eq_tail>` | -> | != <stmt_rel_expr> <stmt_eq_tail> | { != } |
| 733 | `<stmt_eq_tail>` | -> | λ | { %=, &&, *=, +=, -=, .., /=, ;, =, \|\| } |
| 734 | `<stmt_rel_expr>` | -> | <stmt_add_expr> <stmt_rel_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 735 | `<stmt_rel_tail>` | -> | < <stmt_add_expr> | { < } |
| 736 | `<stmt_rel_tail>` | -> | > <stmt_add_expr> | { > } |
| 737 | `<stmt_rel_tail>` | -> | <= <stmt_add_expr> | { <= } |
| 738 | `<stmt_rel_tail>` | -> | >= <stmt_add_expr> | { >= } |
| 739 | `<stmt_rel_tail>` | -> | λ | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 740 | `<stmt_add_expr>` | -> | <stmt_mul_expr> <stmt_add_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 741 | `<stmt_add_tail>` | -> | + <stmt_mul_expr> <stmt_add_tail> | { + } |
| 742 | `<stmt_add_tail>` | -> | - <stmt_mul_expr> <stmt_add_tail> | { - } |
| 743 | `<stmt_add_tail>` | -> | λ | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 744 | `<stmt_mul_expr>` | -> | <stmt_unary_expr> <stmt_mul_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 745 | `<stmt_mul_tail>` | -> | * <stmt_unary_expr> <stmt_mul_tail> | { * } |
| 746 | `<stmt_mul_tail>` | -> | / <stmt_unary_expr> <stmt_mul_tail> | { / } |
| 747 | `<stmt_mul_tail>` | -> | % <stmt_unary_expr> <stmt_mul_tail> | { % } |
| 748 | `<stmt_mul_tail>` | -> | λ | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 749 | `<stmt_unary_expr>` | -> | ! <stmt_unary_expr> | { ! } |
| 750 | `<stmt_unary_expr>` | -> | - <stmt_unary_expr> | { - } |
| 751 | `<stmt_unary_expr>` | -> | <stmt_postfix_expr> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 752 | `<stmt_postfix_expr>` | -> | ( <arg_expr> ) <stmt_postfix_chain> | { ( } |
| 753 | `<stmt_postfix_expr>` | -> | int ( <arg_expr> ) | { int } |
| 754 | `<stmt_postfix_expr>` | -> | long ( <arg_expr> ) | { long } |
| 755 | `<stmt_postfix_expr>` | -> | float ( <arg_expr> ) | { float } |
| 756 | `<stmt_postfix_expr>` | -> | double ( <arg_expr> ) | { double } |
| 757 | `<stmt_postfix_expr>` | -> | char ( <arg_expr> ) | { char } |
| 758 | `<stmt_postfix_expr>` | -> | string ( <arg_expr> ) | { string } |
| 759 | `<stmt_postfix_expr>` | -> | bool ( <arg_expr> ) | { bool } |
| 760 | `<stmt_postfix_expr>` | -> | ++ id | { ++ } |
| 761 | `<stmt_postfix_expr>` | -> | -- id | { -- } |
| 762 | `<stmt_postfix_expr>` | -> | id <stmt_id_postfix> | { id } |
| 763 | `<stmt_postfix_expr>` | -> | intlit | { intlit } |
| 764 | `<stmt_postfix_expr>` | -> | longlit | { longlit } |
| 765 | `<stmt_postfix_expr>` | -> | floatlit | { floatlit } |
| 766 | `<stmt_postfix_expr>` | -> | doublelit | { doublelit } |
| 767 | `<stmt_postfix_expr>` | -> | charlit | { charlit } |
| 768 | `<stmt_postfix_expr>` | -> | stringlit | { stringlit } |
| 769 | `<stmt_postfix_expr>` | -> | true | { true } |
| 770 | `<stmt_postfix_expr>` | -> | false | { false } |
| 771 | `<stmt_id_postfix>` | -> | ++ | { ++ } |
| 772 | `<stmt_id_postfix>` | -> | -- | { -- } |
| 773 | `<stmt_id_postfix>` | -> | <stmt_postfix_chain> | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, [, \|\| } |
| 774 | `<stmt_postfix_chain>` | -> | <stmt_array_access> <stmt_postfix_after_arr> | { [ } |
| 775 | `<stmt_postfix_chain>` | -> | . id <stmt_postfix_chain> | { . } |
| 776 | `<stmt_postfix_chain>` | -> | ( <stmt_arg_list> ) <stmt_postfix_chain> | { ( } |
| 777 | `<stmt_postfix_chain>` | -> | λ | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 778 | `<stmt_array_access>` | -> | [ <stmt_array_index> ] <stmt_array_access_dim2> | { [ } |
| 779 | `<stmt_array_access_dim2>` | -> | [ <stmt_array_index> ] | { [ } |
| 780 | `<stmt_array_access_dim2>` | -> | λ | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 781 | `<stmt_postfix_after_arr>` | -> | . id <stmt_postfix_chain> | { . } |
| 782 | `<stmt_postfix_after_arr>` | -> | ( <stmt_arg_list> ) <stmt_postfix_chain> | { ( } |
| 783 | `<stmt_postfix_after_arr>` | -> | λ | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 784 | `<stmt_array_index>` | -> | intlit | { intlit } |
| 785 | `<stmt_array_index>` | -> | id | { id } |
| 786 | `<stmt_arg_list>` | -> | <arg_expr> <stmt_arg_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 787 | `<stmt_arg_list>` | -> | λ | { ) } |
| 788 | `<stmt_arg_tail>` | -> | , <arg_expr> <stmt_arg_tail> | { , } |
| 789 | `<stmt_arg_tail>` | -> | λ | { ) } |
| 790 | `<arg_expr>` | -> | <arg_assign_expr> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 791 | `<arg_assign_expr>` | -> | <arg_concat_expr> <arg_assign_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 792 | `<arg_assign_tail>` | -> | <assign_op> <arg_assign_expr> | { %=, *=, +=, -=, /=, = } |
| 793 | `<arg_assign_tail>` | -> | λ | { ), , } |
| 794 | `<arg_concat_expr>` | -> | <arg_or_expr> <arg_concat_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 795 | `<arg_concat_tail>` | -> | .. <arg_or_expr> <arg_concat_tail> | { .. } |
| 796 | `<arg_concat_tail>` | -> | λ | { %=, ), *=, +=, ,, -=, /=, = } |
| 797 | `<arg_or_expr>` | -> | <arg_and_expr> <arg_or_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 798 | `<arg_or_tail>` | -> | \|\| <arg_and_expr> <arg_or_tail> | { \|\| } |
| 799 | `<arg_or_tail>` | -> | λ | { %=, ), *=, +=, ,, -=, .., /=, = } |
| 800 | `<arg_and_expr>` | -> | <arg_eq_expr> <arg_and_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 801 | `<arg_and_tail>` | -> | && <arg_eq_expr> <arg_and_tail> | { && } |
| 802 | `<arg_and_tail>` | -> | λ | { %=, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 803 | `<arg_eq_expr>` | -> | <arg_rel_expr> <arg_eq_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 804 | `<arg_eq_tail>` | -> | == <arg_rel_expr> <arg_eq_tail> | { == } |
| 805 | `<arg_eq_tail>` | -> | != <arg_rel_expr> <arg_eq_tail> | { != } |
| 806 | `<arg_eq_tail>` | -> | λ | { %=, &&, ), *=, +=, ,, -=, .., /=, =, \|\| } |
| 807 | `<arg_rel_expr>` | -> | <arg_add_expr> <arg_rel_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 808 | `<arg_rel_tail>` | -> | < <arg_add_expr> | { < } |
| 809 | `<arg_rel_tail>` | -> | > <arg_add_expr> | { > } |
| 810 | `<arg_rel_tail>` | -> | <= <arg_add_expr> | { <= } |
| 811 | `<arg_rel_tail>` | -> | >= <arg_add_expr> | { >= } |
| 812 | `<arg_rel_tail>` | -> | λ | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, =, ==, \|\| } |
| 813 | `<arg_add_expr>` | -> | <arg_mul_expr> <arg_add_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 814 | `<arg_add_tail>` | -> | + <arg_mul_expr> <arg_add_tail> | { + } |
| 815 | `<arg_add_tail>` | -> | - <arg_mul_expr> <arg_add_tail> | { - } |
| 816 | `<arg_add_tail>` | -> | λ | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 817 | `<arg_mul_expr>` | -> | <arg_unary_expr> <arg_mul_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 818 | `<arg_mul_tail>` | -> | * <arg_unary_expr> <arg_mul_tail> | { * } |
| 819 | `<arg_mul_tail>` | -> | / <arg_unary_expr> <arg_mul_tail> | { / } |
| 820 | `<arg_mul_tail>` | -> | % <arg_unary_expr> <arg_mul_tail> | { % } |
| 821 | `<arg_mul_tail>` | -> | λ | { !=, %=, &&, ), *=, +, +=, ,, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 822 | `<arg_unary_expr>` | -> | ! <arg_unary_expr> | { ! } |
| 823 | `<arg_unary_expr>` | -> | - <arg_unary_expr> | { - } |
| 824 | `<arg_unary_expr>` | -> | <arg_postfix_expr> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 825 | `<arg_postfix_expr>` | -> | ( <arg_expr> ) <arg_postfix_chain> | { ( } |
| 826 | `<arg_postfix_expr>` | -> | int ( <arg_expr> ) | { int } |
| 827 | `<arg_postfix_expr>` | -> | long ( <arg_expr> ) | { long } |
| 828 | `<arg_postfix_expr>` | -> | float ( <arg_expr> ) | { float } |
| 829 | `<arg_postfix_expr>` | -> | double ( <arg_expr> ) | { double } |
| 830 | `<arg_postfix_expr>` | -> | char ( <arg_expr> ) | { char } |
| 831 | `<arg_postfix_expr>` | -> | string ( <arg_expr> ) | { string } |
| 832 | `<arg_postfix_expr>` | -> | bool ( <arg_expr> ) | { bool } |
| 833 | `<arg_postfix_expr>` | -> | ++ id | { ++ } |
| 834 | `<arg_postfix_expr>` | -> | -- id | { -- } |
| 835 | `<arg_postfix_expr>` | -> | id <arg_id_postfix> | { id } |
| 836 | `<arg_postfix_expr>` | -> | intlit | { intlit } |
| 837 | `<arg_postfix_expr>` | -> | longlit | { longlit } |
| 838 | `<arg_postfix_expr>` | -> | floatlit | { floatlit } |
| 839 | `<arg_postfix_expr>` | -> | doublelit | { doublelit } |
| 840 | `<arg_postfix_expr>` | -> | charlit | { charlit } |
| 841 | `<arg_postfix_expr>` | -> | stringlit | { stringlit } |
| 842 | `<arg_postfix_expr>` | -> | true | { true } |
| 843 | `<arg_postfix_expr>` | -> | false | { false } |
| 844 | `<arg_id_postfix>` | -> | ++ | { ++ } |
| 845 | `<arg_id_postfix>` | -> | -- | { -- } |
| 846 | `<arg_id_postfix>` | -> | <arg_postfix_chain> | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, [, \|\| } |
| 847 | `<arg_postfix_chain>` | -> | <arg_array_access> <arg_postfix_after_arr> | { [ } |
| 848 | `<arg_postfix_chain>` | -> | . id <arg_postfix_chain> | { . } |
| 849 | `<arg_postfix_chain>` | -> | ( <arg_nested_list> ) <arg_postfix_chain> | { ( } |
| 850 | `<arg_postfix_chain>` | -> | λ | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 851 | `<arg_array_access>` | -> | [ <arg_array_index> ] <arg_array_access_dim2> | { [ } |
| 852 | `<arg_array_access_dim2>` | -> | [ <arg_array_index> ] | { [ } |
| 853 | `<arg_array_access_dim2>` | -> | λ | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 854 | `<arg_postfix_after_arr>` | -> | . id <arg_postfix_chain> | { . } |
| 855 | `<arg_postfix_after_arr>` | -> | ( <arg_nested_list> ) <arg_postfix_chain> | { ( } |
| 856 | `<arg_postfix_after_arr>` | -> | λ | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 857 | `<arg_array_index>` | -> | intlit | { intlit } |
| 858 | `<arg_array_index>` | -> | id | { id } |
| 859 | `<arg_nested_list>` | -> | <arg_expr> <arg_nested_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 860 | `<arg_nested_list>` | -> | λ | { ) } |
| 861 | `<arg_nested_tail>` | -> | , <arg_expr> <arg_nested_tail> | { , } |
| 862 | `<arg_nested_tail>` | -> | λ | { ) } |
| 863 | `<expression>` | -> | <assign_expr> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 864 | `<assign_expr>` | -> | <concat_expr> <assign_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 865 | `<assign_tail>` | -> | <assign_op> <assign_expr> | { %=, *=, +=, -=, /=, = } |
| 866 | `<assign_tail>` | -> | λ | { ), ; } |
| 867 | `<assign_op>` | -> | = | { = } |
| 868 | `<assign_op>` | -> | += | { += } |
| 869 | `<assign_op>` | -> | -= | { -= } |
| 870 | `<assign_op>` | -> | *= | { *= } |
| 871 | `<assign_op>` | -> | /= | { /= } |
| 872 | `<assign_op>` | -> | %= | { %= } |
| 873 | `<concat_expr>` | -> | <or_expr> <concat_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 874 | `<concat_tail>` | -> | .. <or_expr> <concat_tail> | { .. } |
| 875 | `<concat_tail>` | -> | λ | { %=, ), *=, +=, -=, /=, ;, = } |
| 876 | `<or_expr>` | -> | <and_expr> <or_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 877 | `<or_tail>` | -> | \|\| <and_expr> <or_tail> | { \|\| } |
| 878 | `<or_tail>` | -> | λ | { %=, ), *=, +=, -=, .., /=, ;, = } |
| 879 | `<and_expr>` | -> | <eq_expr> <and_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 880 | `<and_tail>` | -> | && <eq_expr> <and_tail> | { && } |
| 881 | `<and_tail>` | -> | λ | { %=, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 882 | `<eq_expr>` | -> | <rel_expr> <eq_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 883 | `<eq_tail>` | -> | == <rel_expr> <eq_tail> | { == } |
| 884 | `<eq_tail>` | -> | != <rel_expr> <eq_tail> | { != } |
| 885 | `<eq_tail>` | -> | λ | { %=, &&, ), *=, +=, -=, .., /=, ;, =, \|\| } |
| 886 | `<rel_expr>` | -> | <add_expr> <rel_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 887 | `<rel_tail>` | -> | < <add_expr> | { < } |
| 888 | `<rel_tail>` | -> | > <add_expr> | { > } |
| 889 | `<rel_tail>` | -> | <= <add_expr> | { <= } |
| 890 | `<rel_tail>` | -> | >= <add_expr> | { >= } |
| 891 | `<rel_tail>` | -> | λ | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, =, ==, \|\| } |
| 892 | `<add_expr>` | -> | <mul_expr> <add_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 893 | `<add_tail>` | -> | + <mul_expr> <add_tail> | { + } |
| 894 | `<add_tail>` | -> | - <mul_expr> <add_tail> | { - } |
| 895 | `<add_tail>` | -> | λ | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 896 | `<mul_expr>` | -> | <unary_expr> <mul_tail> | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 897 | `<mul_tail>` | -> | * <unary_expr> <mul_tail> | { * } |
| 898 | `<mul_tail>` | -> | / <unary_expr> <mul_tail> | { / } |
| 899 | `<mul_tail>` | -> | % <unary_expr> <mul_tail> | { % } |
| 900 | `<mul_tail>` | -> | λ | { !=, %=, &&, ), *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 901 | `<unary_expr>` | -> | ! <unary_expr> | { ! } |
| 902 | `<unary_expr>` | -> | <postfix_expr> | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 903 | `<postfix_expr>` | -> | ( <expression> ) <postfix_chain> | { ( } |
| 904 | `<postfix_expr>` | -> | int ( <expression> ) | { int } |
| 905 | `<postfix_expr>` | -> | long ( <expression> ) | { long } |
| 906 | `<postfix_expr>` | -> | float ( <expression> ) | { float } |
| 907 | `<postfix_expr>` | -> | double ( <expression> ) | { double } |
| 908 | `<postfix_expr>` | -> | char ( <expression> ) | { char } |
| 909 | `<postfix_expr>` | -> | string ( <expression> ) | { string } |
| 910 | `<postfix_expr>` | -> | bool ( <expression> ) | { bool } |
| 911 | `<postfix_expr>` | -> | ++ id | { ++ } |
| 912 | `<postfix_expr>` | -> | -- id | { -- } |
| 913 | `<postfix_expr>` | -> | id <id_postfix> | { id } |
| 914 | `<postfix_expr>` | -> | intlit | { intlit } |
| 915 | `<postfix_expr>` | -> | longlit | { longlit } |
| 916 | `<postfix_expr>` | -> | floatlit | { floatlit } |
| 917 | `<postfix_expr>` | -> | doublelit | { doublelit } |
| 918 | `<postfix_expr>` | -> | charlit | { charlit } |
| 919 | `<postfix_expr>` | -> | stringlit | { stringlit } |
| 920 | `<postfix_expr>` | -> | true | { true } |
| 921 | `<postfix_expr>` | -> | false | { false } |
| 922 | `<id_postfix>` | -> | ++ | { ++ } |
| 923 | `<id_postfix>` | -> | -- | { -- } |
| 924 | `<id_postfix>` | -> | <postfix_chain> | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, [, \|\| } |
| 925 | `<postfix_chain>` | -> | <array_access> <postfix_after_arr> | { [ } |
| 926 | `<postfix_chain>` | -> | . id <postfix_chain> | { . } |
| 927 | `<postfix_chain>` | -> | ( <arg_list> ) <postfix_chain> | { ( } |
| 928 | `<postfix_chain>` | -> | λ | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 929 | `<array_access>` | -> | [ <array_index> ] <array_access_dim2> | { [ } |
| 930 | `<array_access_dim2>` | -> | [ <array_index> ] | { [ } |
| 931 | `<array_access_dim2>` | -> | λ | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 932 | `<postfix_after_arr>` | -> | . id <postfix_chain> | { . } |
| 933 | `<postfix_after_arr>` | -> | ( <arg_list> ) <postfix_chain> | { ( } |
| 934 | `<postfix_after_arr>` | -> | λ | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \|\| } |
| 935 | `<array_index>` | -> | intlit | { intlit } |
| 936 | `<array_index>` | -> | id | { id } |
| 937 | `<arg_list>` | -> | <arg_expr> <arg_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 938 | `<arg_list>` | -> | λ | { ) } |
| 939 | `<arg_tail>` | -> | , <arg_expr> <arg_tail> | { , } |
| 940 | `<arg_tail>` | -> | λ | { ) } |
| 941 | `<io_stmt>` | -> | trap ( <arg_expr> ) ; | { trap } |
| 942 | `<io_stmt>` | -> | thread ( <print_args> ) ; | { thread } |
| 943 | `<io_stmt>` | -> | threadln ( <print_args> ) ; | { threadln } |
| 944 | `<print_args>` | -> | <arg_expr> <print_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 945 | `<print_tail>` | -> | , <arg_expr> <print_tail> | { , } |
| 946 | `<print_tail>` | -> | λ | { ) } |
| 947 | `<ctrl_struct>` | -> | if ( <condition> ) { <ctrl_stmt_list> } <else_opt> | { if } |
| 948 | `<ctrl_struct>` | -> | switch ( <arg_expr> ) { <case_list> <default_opt> } | { switch } |
| 949 | `<ctrl_struct>` | -> | for ( <for_init> ; <for_cond> ; <for_update> ) { <ctrl_stmt_list> } | { for } |
| 950 | `<ctrl_struct>` | -> | while ( <condition> ) { <ctrl_stmt_list> } | { while } |
| 951 | `<ctrl_struct>` | -> | do { <ctrl_stmt_list> } while ( <condition> ) ; | { do } |
| 952 | `<else_opt>` | -> | else <else_body> | { else } |
| 953 | `<else_opt>` | -> | λ | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 954 | `<else_body>` | -> | { <ctrl_stmt_list> } | { { } |
| 955 | `<else_body>` | -> | if ( <condition> ) { <ctrl_stmt_list> } <else_opt> | { if } |
| 956 | `<case_list>` | -> | case <case_val> : <ctrl_stmt_list> <break_opt> <case_list> | { case } |
| 957 | `<case_list>` | -> | λ | { default, } } |
| 958 | `<case_val>` | -> | intlit | { intlit } |
| 959 | `<case_val>` | -> | longlit | { longlit } |
| 960 | `<case_val>` | -> | charlit | { charlit } |
| 961 | `<case_val>` | -> | true | { true } |
| 962 | `<case_val>` | -> | false | { false } |
| 963 | `<default_opt>` | -> | default : <ctrl_stmt_list> <break_opt> | { default } |
| 964 | `<default_opt>` | -> | λ | { } } |
| 965 | `<break_opt>` | -> | break ; | { break } |
| 966 | `<break_opt>` | -> | λ | { case, default, } } |
| 967 | `<for_init>` | -> | local var <for_init_type> id = <for_init_expr> | { local } |
| 968 | `<for_init>` | -> | id <for_init_assign_tail> | { id } |
| 969 | `<for_init>` | -> | λ | { ; } |
| 970 | `<for_init_assign_tail>` | -> | <assign_op> <for_init_expr> | { %=, *=, +=, -=, /=, = } |
| 971 | `<for_init_expr>` | -> | <stmt_concat_expr> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 972 | `<for_init_type>` | -> | int | { int } |
| 973 | `<for_init_type>` | -> | long | { long } |
| 974 | `<for_init_type>` | -> | float | { float } |
| 975 | `<for_init_type>` | -> | double | { double } |
| 976 | `<for_init_type>` | -> | char | { char } |
| 977 | `<for_init_type>` | -> | string | { string } |
| 978 | `<for_init_type>` | -> | bool | { bool } |
| 979 | `<for_cond>` | -> | <condition> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 980 | `<for_update>` | -> | id <for_update_tail> | { id } |
| 981 | `<for_update>` | -> | ++ id | { ++ } |
| 982 | `<for_update>` | -> | -- id | { -- } |
| 983 | `<for_update>` | -> | λ | { ) } |
| 984 | `<for_update_tail>` | -> | ++ | { ++ } |
| 985 | `<for_update_tail>` | -> | -- | { -- } |
| 986 | `<for_update_tail>` | -> | <assign_op> <arg_expr> | { %=, *=, +=, -=, /=, = } |
| 987 | `<condition>` | -> | <cond_or> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 988 | `<cond_or>` | -> | <cond_and> <cond_or_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 989 | `<cond_or_tail>` | -> | \|\| <cond_and> <cond_or_tail> | { \|\| } |
| 990 | `<cond_or_tail>` | -> | λ | { ), ; } |
| 991 | `<cond_and>` | -> | <cond_comparison> <cond_and_tail> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 992 | `<cond_and_tail>` | -> | && <cond_comparison> <cond_and_tail> | { && } |
| 993 | `<cond_and_tail>` | -> | λ | { ), ;, \|\| } |
| 994 | `<cond_comparison>` | -> | ( <condition> ) | { ( } |
| 995 | `<cond_comparison>` | -> | ! <cond_comparison> | { ! } |
| 996 | `<cond_comparison>` | -> | <cond_primary> <cond_primary_continue> | { ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 997 | `<cond_primary>` | -> | - <cond_primary> | { - } |
| 998 | `<cond_primary>` | -> | <cond_postfix> | { ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 999 | `<cond_primary_continue>` | -> | + <cond_primary> <cond_must_commit> | { + } |
| 1000 | `<cond_primary_continue>` | -> | - <cond_primary> <cond_must_commit> | { - } |
| 1001 | `<cond_primary_continue>` | -> | * <cond_primary> <cond_must_commit> | { * } |
| 1002 | `<cond_primary_continue>` | -> | / <cond_primary> <cond_must_commit> | { / } |
| 1003 | `<cond_primary_continue>` | -> | % <cond_primary> <cond_must_commit> | { % } |
| 1004 | `<cond_primary_continue>` | -> | <comp_op> <cond_rhs> | { !=, <, <=, ==, >, >= } |
| 1005 | `<cond_primary_continue>` | -> | λ | { &&, ), ;, \|\| } |
| 1006 | `<cond_must_commit>` | -> | + <cond_primary> <cond_must_commit> | { + } |
| 1007 | `<cond_must_commit>` | -> | - <cond_primary> <cond_must_commit> | { - } |
| 1008 | `<cond_must_commit>` | -> | * <cond_primary> <cond_must_commit> | { * } |
| 1009 | `<cond_must_commit>` | -> | / <cond_primary> <cond_must_commit> | { / } |
| 1010 | `<cond_must_commit>` | -> | % <cond_primary> <cond_must_commit> | { % } |
| 1011 | `<cond_must_commit>` | -> | <comp_op> <cond_rhs> | { !=, <, <=, ==, >, >= } |
| 1012 | `<cond_postfix>` | -> | int ( <cond_cast_arg> ) | { int } |
| 1013 | `<cond_postfix>` | -> | long ( <cond_cast_arg> ) | { long } |
| 1014 | `<cond_postfix>` | -> | float ( <cond_cast_arg> ) | { float } |
| 1015 | `<cond_postfix>` | -> | double ( <cond_cast_arg> ) | { double } |
| 1016 | `<cond_postfix>` | -> | char ( <cond_cast_arg> ) | { char } |
| 1017 | `<cond_postfix>` | -> | string ( <cond_cast_arg> ) | { string } |
| 1018 | `<cond_postfix>` | -> | bool ( <cond_cast_arg> ) | { bool } |
| 1019 | `<cond_postfix>` | -> | ++ id | { ++ } |
| 1020 | `<cond_postfix>` | -> | -- id | { -- } |
| 1021 | `<cond_postfix>` | -> | id <cond_id_post> | { id } |
| 1022 | `<cond_postfix>` | -> | intlit | { intlit } |
| 1023 | `<cond_postfix>` | -> | longlit | { longlit } |
| 1024 | `<cond_postfix>` | -> | floatlit | { floatlit } |
| 1025 | `<cond_postfix>` | -> | doublelit | { doublelit } |
| 1026 | `<cond_postfix>` | -> | charlit | { charlit } |
| 1027 | `<cond_postfix>` | -> | stringlit | { stringlit } |
| 1028 | `<cond_postfix>` | -> | true | { true } |
| 1029 | `<cond_postfix>` | -> | false | { false } |
| 1030 | `<cond_cast_arg>` | -> | <arg_expr> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1031 | `<cond_id_post>` | -> | ++ | { ++ } |
| 1032 | `<cond_id_post>` | -> | -- | { -- } |
| 1033 | `<cond_id_post>` | -> | <cond_post_chain> | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, [, \|\| } |
| 1034 | `<cond_post_chain>` | -> | <cond_arr_access> <cond_post_after_arr> | { [ } |
| 1035 | `<cond_post_chain>` | -> | . id <cond_post_chain> | { . } |
| 1036 | `<cond_post_chain>` | -> | ( <arg_list> ) <cond_post_chain> | { ( } |
| 1037 | `<cond_post_chain>` | -> | λ | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 1038 | `<cond_arr_access>` | -> | [ <cond_arr_index> ] <cond_arr_access_dim2> | { [ } |
| 1039 | `<cond_arr_access_dim2>` | -> | [ <cond_arr_index> ] | { [ } |
| 1040 | `<cond_arr_access_dim2>` | -> | λ | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, \|\| } |
| 1041 | `<cond_post_after_arr>` | -> | . id <cond_post_chain> | { . } |
| 1042 | `<cond_post_after_arr>` | -> | ( <arg_list> ) <cond_post_chain> | { ( } |
| 1043 | `<cond_post_after_arr>` | -> | λ | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \|\| } |
| 1044 | `<cond_arr_index>` | -> | intlit | { intlit } |
| 1045 | `<cond_arr_index>` | -> | id | { id } |
| 1046 | `<cond_rhs>` | -> | <arg_add_expr> | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1047 | `<comp_op>` | -> | == | { == } |
| 1048 | `<comp_op>` | -> | != | { != } |
| 1049 | `<comp_op>` | -> | < | { < } |
| 1050 | `<comp_op>` | -> | > | { > } |
| 1051 | `<comp_op>` | -> | <= | { <= } |
| 1052 | `<comp_op>` | -> | >= | { >= } |
| 1053 | `<main_body>` | -> | <main_content> | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 1054 | `<main_content>` | -> | using id <using_cont> ; <main_content> | { using } |
| 1055 | `<main_content>` | -> | local <mutability> <local_dec_body> <main_content> | { local } |
| 1056 | `<main_content>` | -> | <statement_non_return> <main_content> | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1057 | `<main_content>` | -> | return intlit ; | { return } |