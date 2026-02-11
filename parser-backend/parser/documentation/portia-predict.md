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
| 13 | `<global_section>` → int main ( ) { `<main_body>` } | FIRST(int main) | { int } |
| 14 | `<func_and_main>` → `<function_decl>` `<func_and_main>` | FIRST(`<function_decl>`) | { func } |
| 15 | `<func_and_main>` → int main ( ) { `<main_body>` } | FIRST(int main) | { int } |
| 16 | `<global_decl>` → global `<mutability>` int id = intlit `<int_global_cont>` ; | FIRST(global) | { global } |
| 17 | `<global_decl>` → global `<mutability>` long id = longlit `<long_global_cont>` ; | FIRST(global) | { global } |
| 18 | `<global_decl>` → global `<mutability>` float id = floatlit `<float_global_cont>` ; | FIRST(global) | { global } |
| 19 | `<global_decl>` → global `<mutability>` double id = doublelit `<double_global_cont>` ; | FIRST(global) | { global } |
| 20 | `<global_decl>` → global `<mutability>` char id = charlit `<char_global_cont>` ; | FIRST(global) | { global } |
| 21 | `<global_decl>` → global `<mutability>` string id = stringlit `<string_global_cont>` ; | FIRST(global) | { global } |
| 22 | `<global_decl>` → global `<mutability>` bool id = `<bool_lit>` `<bool_global_cont>` ; | FIRST(global) | { global } |
| 23 | `<function_decl>` → func int `<func_ret_int>` | FIRST(func int) | { func } |
| 24 | `<function_decl>` → func long `<func_ret_long>` | FIRST(func long) | { func } |
| 25 | `<function_decl>` → func float `<func_ret_float>` | FIRST(func float) | { func } |
| 26 | `<function_decl>` → func double `<func_ret_double>` | FIRST(func double) | { func } |
| 27 | `<function_decl>` → func char `<func_ret_char>` | FIRST(func char) | { func } |
| 28 | `<function_decl>` → func string `<func_ret_string>` | FIRST(func string) | { func } |
| 29 | `<function_decl>` → func bool `<func_ret_bool>` | FIRST(func bool) | { func } |
| 30 | `<function_decl>` → func id `<func_ret_weave>` | FIRST(func id) | { func } |
| 31 | `<function_decl>` → func void id ( ) { `<function_body_void>` } | FIRST(func void) | { func } |
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
| 71 | `<weave_array_init_tail>` → [ <size> ] <weave_arr_init_opt_2d> | FIRST([ <size> ] <weave_arr_init_opt_2d>) | { [ } |
| 72 | `<weave_array_init_tail>` → <weave_arr_init_opt_1d> | FIRST(<weave_arr_init_opt_1d>) ∪ FOLLOW(<weave_array_init_tail>) | { ,, ;, = } |
| 73 | `<weave_arr_init_opt_1d>` → = { <weave_arr_init_content_1d> } | FIRST(= { <weave_arr_init_content_1d> }) | { = } |
| 74 | `<weave_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<weave_arr_init_opt_1d>) = { λ } ∪ { ,, ; } | { ,, ; } |
| 75 | `<weave_arr_init_content_1d>` → { <weave_field_value> <weave_field_list_tail> } <weave_init_1d_tail> | FIRST({ <weave_field_value> <weave_field_list_...) | { { } |
| 76 | `<weave_init_1d_tail>` → , { <weave_field_value> <weave_field_list_tail> } <weave_init_1d_tail> | FIRST(, { <weave_field_value> <weave_field_lis...) | { , } |
| 77 | `<weave_init_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<weave_init_1d_tail>) = { λ } ∪ { } } | { } } |
| 78 | `<weave_arr_init_opt_2d>` → = { <weave_arr_init_content_2d> } | FIRST(= { <weave_arr_init_content_2d> }) | { = } |
| 79 | `<weave_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<weave_arr_init_opt_2d>) = { λ } ∪ { ,, ; } | { ,, ; } |
| 80 | `<weave_arr_init_content_2d>` → { <weave_init_row> } <weave_init_2d_tail> | FIRST({ <weave_init_row> } <weave_init_2d_tail...) | { { } |
| 81 | `<weave_init_row>` → { <weave_field_value> <weave_field_list_tail> } <weave_init_1d_tail> | FIRST({ <weave_field_value> <weave_field_list_...) | { { } |
| 82 | `<weave_init_2d_tail>` → , { <weave_init_row> } <weave_init_2d_tail> | FIRST(, { <weave_init_row> } <weave_init_2d_ta...) | { , } |
| 83 | `<weave_init_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<weave_init_2d_tail>) = { λ } ∪ { } } | { } } |
| 84 | `<mutability>` → var | FIRST(var) | { var } |
| 85 | `<mutability>` → const | FIRST(const) | { const } |
| 86 | `<array_dims>` → [ <size> ] <array_dim2_opt> | FIRST([ <size> ] <array_dim2_opt>) | { [ } |
| 87 | `<array_dim2_opt>` → [ <size> ] | FIRST([ <size> ]) | { [ } |
| 88 | `<array_dim2_opt>` → λ | FIRST(λ) ∪ FOLLOW(<array_dim2_opt>) = { λ } ∪ { ), ,, ;, id } | { ), ,, ;, id } |
| 89 | `<size>` → intlit | FIRST(intlit) | { intlit } |
| 90 | `<size>` → id | FIRST(id) | { id } |
| 91 | `<int_array_with_init>` → [ <size> ] <int_array_init_tail> | FIRST([ <size> ] <int_array_init_tail>) | { [ } |
| 92 | `<int_array_init_tail>` → [ <size> ] <int_arr_init_opt_2d> | FIRST([ <size> ] <int_arr_init_opt_2d>) | { [ } |
| 93 | `<int_array_init_tail>` → <int_arr_init_opt_1d> | FIRST(<int_arr_init_opt_1d>) ∪ FOLLOW(<int_array_init_tail>) | { ;, = } |
| 94 | `<int_arr_init_opt_1d>` → = { <int_arr_init_content_1d> } | FIRST(= { <int_arr_init_content_1d> }) | { = } |
| 95 | `<int_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<int_arr_init_opt_1d>) = { λ } ∪ { ; } | { ; } |
| 96 | `<int_arr_init_content_1d>` → intlit <int_elem_1d_tail> | FIRST(intlit <int_elem_1d_tail>) | { intlit } |
| 97 | `<int_elem_1d_tail>` → , intlit <int_elem_1d_tail> | FIRST(, intlit <int_elem_1d_tail>) | { , } |
| 98 | `<int_elem_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<int_elem_1d_tail>) = { λ } ∪ { } } | { } } |
| 99 | `<int_arr_init_opt_2d>` → = { <int_arr_init_content_2d> } | FIRST(= { <int_arr_init_content_2d> }) | { = } |
| 100 | `<int_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<int_arr_init_opt_2d>) = { λ } ∪ { ; } | { ; } |
| 101 | `<int_arr_init_content_2d>` → { <int_elem_list> } <int_elem_2d_tail> | FIRST({ <int_elem_list> } <int_elem_2d_tail>) | { { } |
| 102 | `<int_elem_list>` → intlit <int_elem_1d_tail> | FIRST(intlit <int_elem_1d_tail>) | { intlit } |
| 103 | `<int_elem_2d_tail>` → , { <int_elem_list> } <int_elem_2d_tail> | FIRST(, { <int_elem_list> } <int_elem_2d_tail>) | { , } |
| 104 | `<int_elem_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<int_elem_2d_tail>) = { λ } ∪ { } } | { } } |
| 105 | `<long_array_with_init>` → [ <size> ] <long_array_init_tail> | FIRST([ <size> ] <long_array_init_tail>) | { [ } |
| 106 | `<long_array_init_tail>` → [ <size> ] <long_arr_init_opt_2d> | FIRST([ <size> ] <long_arr_init_opt_2d>) | { [ } |
| 107 | `<long_array_init_tail>` → <long_arr_init_opt_1d> | FIRST(<long_arr_init_opt_1d>) ∪ FOLLOW(<long_array_init_tail>) | { ;, = } |
| 108 | `<long_arr_init_opt_1d>` → = { <long_arr_init_content_1d> } | FIRST(= { <long_arr_init_content_1d> }) | { = } |
| 109 | `<long_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<long_arr_init_opt_1d>) = { λ } ∪ { ; } | { ; } |
| 110 | `<long_arr_init_content_1d>` → longlit <long_elem_1d_tail> | FIRST(longlit <long_elem_1d_tail>) | { longlit } |
| 111 | `<long_elem_1d_tail>` → , longlit <long_elem_1d_tail> | FIRST(, longlit <long_elem_1d_tail>) | { , } |
| 112 | `<long_elem_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<long_elem_1d_tail>) = { λ } ∪ { } } | { } } |
| 113 | `<long_arr_init_opt_2d>` → = { <long_arr_init_content_2d> } | FIRST(= { <long_arr_init_content_2d> }) | { = } |
| 114 | `<long_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<long_arr_init_opt_2d>) = { λ } ∪ { ; } | { ; } |
| 115 | `<long_arr_init_content_2d>` → { <long_elem_list> } <long_elem_2d_tail> | FIRST({ <long_elem_list> } <long_elem_2d_tail>) | { { } |
| 116 | `<long_elem_list>` → longlit <long_elem_1d_tail> | FIRST(longlit <long_elem_1d_tail>) | { longlit } |
| 117 | `<long_elem_2d_tail>` → , { <long_elem_list> } <long_elem_2d_tail> | FIRST(, { <long_elem_list> } <long_elem_2d_tai...) | { , } |
| 118 | `<long_elem_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<long_elem_2d_tail>) = { λ } ∪ { } } | { } } |
| 119 | `<float_array_with_init>` → [ <size> ] <float_array_init_tail> | FIRST([ <size> ] <float_array_init_tail>) | { [ } |
| 120 | `<float_array_init_tail>` → [ <size> ] <float_arr_init_opt_2d> | FIRST([ <size> ] <float_arr_init_opt_2d>) | { [ } |
| 121 | `<float_array_init_tail>` → <float_arr_init_opt_1d> | FIRST(<float_arr_init_opt_1d>) ∪ FOLLOW(<float_array_init_tail>) | { ;, = } |
| 122 | `<float_arr_init_opt_1d>` → = { <float_arr_init_content_1d> } | FIRST(= { <float_arr_init_content_1d> }) | { = } |
| 123 | `<float_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<float_arr_init_opt_1d>) = { λ } ∪ { ; } | { ; } |
| 124 | `<float_arr_init_content_1d>` → floatlit <float_elem_1d_tail> | FIRST(floatlit <float_elem_1d_tail>) | { floatlit } |
| 125 | `<float_elem_1d_tail>` → , floatlit <float_elem_1d_tail> | FIRST(, floatlit <float_elem_1d_tail>) | { , } |
| 126 | `<float_elem_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<float_elem_1d_tail>) = { λ } ∪ { } } | { } } |
| 127 | `<float_arr_init_opt_2d>` → = { <float_arr_init_content_2d> } | FIRST(= { <float_arr_init_content_2d> }) | { = } |
| 128 | `<float_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<float_arr_init_opt_2d>) = { λ } ∪ { ; } | { ; } |
| 129 | `<float_arr_init_content_2d>` → { <float_elem_list> } <float_elem_2d_tail> | FIRST({ <float_elem_list> } <float_elem_2d_tai...) | { { } |
| 130 | `<float_elem_list>` → floatlit <float_elem_1d_tail> | FIRST(floatlit <float_elem_1d_tail>) | { floatlit } |
| 131 | `<float_elem_2d_tail>` → , { <float_elem_list> } <float_elem_2d_tail> | FIRST(, { <float_elem_list> } <float_elem_2d_t...) | { , } |
| 132 | `<float_elem_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<float_elem_2d_tail>) = { λ } ∪ { } } | { } } |
| 133 | `<double_array_with_init>` → [ <size> ] <double_array_init_tail> | FIRST([ <size> ] <double_array_init_tail>) | { [ } |
| 134 | `<double_array_init_tail>` → [ <size> ] <double_arr_init_opt_2d> | FIRST([ <size> ] <double_arr_init_opt_2d>) | { [ } |
| 135 | `<double_array_init_tail>` → <double_arr_init_opt_1d> | FIRST(<double_arr_init_opt_1d>) ∪ FOLLOW(<double_array_init_tail>) | { ;, = } |
| 136 | `<double_arr_init_opt_1d>` → = { <double_arr_init_content_1d> } | FIRST(= { <double_arr_init_content_1d> }) | { = } |
| 137 | `<double_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<double_arr_init_opt_1d>) = { λ } ∪ { ; } | { ; } |
| 138 | `<double_arr_init_content_1d>` → doublelit <double_elem_1d_tail> | FIRST(doublelit <double_elem_1d_tail>) | { doublelit } |
| 139 | `<double_elem_1d_tail>` → , doublelit <double_elem_1d_tail> | FIRST(, doublelit <double_elem_1d_tail>) | { , } |
| 140 | `<double_elem_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<double_elem_1d_tail>) = { λ } ∪ { } } | { } } |
| 141 | `<double_arr_init_opt_2d>` → = { <double_arr_init_content_2d> } | FIRST(= { <double_arr_init_content_2d> }) | { = } |
| 142 | `<double_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<double_arr_init_opt_2d>) = { λ } ∪ { ; } | { ; } |
| 143 | `<double_arr_init_content_2d>` → { <double_elem_list> } <double_elem_2d_tail> | FIRST({ <double_elem_list> } <double_elem_2d_t...) | { { } |
| 144 | `<double_elem_list>` → doublelit <double_elem_1d_tail> | FIRST(doublelit <double_elem_1d_tail>) | { doublelit } |
| 145 | `<double_elem_2d_tail>` → , { <double_elem_list> } <double_elem_2d_tail> | FIRST(, { <double_elem_list> } <double_elem_2d...) | { , } |
| 146 | `<double_elem_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<double_elem_2d_tail>) = { λ } ∪ { } } | { } } |
| 147 | `<char_array_with_init>` → [ <size> ] <char_array_init_tail> | FIRST([ <size> ] <char_array_init_tail>) | { [ } |
| 148 | `<char_array_init_tail>` → [ <size> ] <char_arr_init_opt_2d> | FIRST([ <size> ] <char_arr_init_opt_2d>) | { [ } |
| 149 | `<char_array_init_tail>` → <char_arr_init_opt_1d> | FIRST(<char_arr_init_opt_1d>) ∪ FOLLOW(<char_array_init_tail>) | { ;, = } |
| 150 | `<char_arr_init_opt_1d>` → = { <char_arr_init_content_1d> } | FIRST(= { <char_arr_init_content_1d> }) | { = } |
| 151 | `<char_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<char_arr_init_opt_1d>) = { λ } ∪ { ; } | { ; } |
| 152 | `<char_arr_init_content_1d>` → charlit <char_elem_1d_tail> | FIRST(charlit <char_elem_1d_tail>) | { charlit } |
| 153 | `<char_elem_1d_tail>` → , charlit <char_elem_1d_tail> | FIRST(, charlit <char_elem_1d_tail>) | { , } |
| 154 | `<char_elem_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<char_elem_1d_tail>) = { λ } ∪ { } } | { } } |
| 155 | `<char_arr_init_opt_2d>` → = { <char_arr_init_content_2d> } | FIRST(= { <char_arr_init_content_2d> }) | { = } |
| 156 | `<char_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<char_arr_init_opt_2d>) = { λ } ∪ { ; } | { ; } |
| 157 | `<char_arr_init_content_2d>` → { <char_elem_list> } <char_elem_2d_tail> | FIRST({ <char_elem_list> } <char_elem_2d_tail>) | { { } |
| 158 | `<char_elem_list>` → charlit <char_elem_1d_tail> | FIRST(charlit <char_elem_1d_tail>) | { charlit } |
| 159 | `<char_elem_2d_tail>` → , { <char_elem_list> } <char_elem_2d_tail> | FIRST(, { <char_elem_list> } <char_elem_2d_tai...) | { , } |
| 160 | `<char_elem_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<char_elem_2d_tail>) = { λ } ∪ { } } | { } } |
| 161 | `<string_array_with_init>` → [ <size> ] <string_array_init_tail> | FIRST([ <size> ] <string_array_init_tail>) | { [ } |
| 162 | `<string_array_init_tail>` → [ <size> ] <string_arr_init_opt_2d> | FIRST([ <size> ] <string_arr_init_opt_2d>) | { [ } |
| 163 | `<string_array_init_tail>` → <string_arr_init_opt_1d> | FIRST(<string_arr_init_opt_1d>) ∪ FOLLOW(<string_array_init_tail>) | { ;, = } |
| 164 | `<string_arr_init_opt_1d>` → = { <string_arr_init_content_1d> } | FIRST(= { <string_arr_init_content_1d> }) | { = } |
| 165 | `<string_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<string_arr_init_opt_1d>) = { λ } ∪ { ; } | { ; } |
| 166 | `<string_arr_init_content_1d>` → stringlit <string_elem_1d_tail> | FIRST(stringlit <string_elem_1d_tail>) | { stringlit } |
| 167 | `<string_elem_1d_tail>` → , stringlit <string_elem_1d_tail> | FIRST(, stringlit <string_elem_1d_tail>) | { , } |
| 168 | `<string_elem_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<string_elem_1d_tail>) = { λ } ∪ { } } | { } } |
| 169 | `<string_arr_init_opt_2d>` → = { <string_arr_init_content_2d> } | FIRST(= { <string_arr_init_content_2d> }) | { = } |
| 170 | `<string_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<string_arr_init_opt_2d>) = { λ } ∪ { ; } | { ; } |
| 171 | `<string_arr_init_content_2d>` → { <string_elem_list> } <string_elem_2d_tail> | FIRST({ <string_elem_list> } <string_elem_2d_t...) | { { } |
| 172 | `<string_elem_list>` → stringlit <string_elem_1d_tail> | FIRST(stringlit <string_elem_1d_tail>) | { stringlit } |
| 173 | `<string_elem_2d_tail>` → , { <string_elem_list> } <string_elem_2d_tail> | FIRST(, { <string_elem_list> } <string_elem_2d...) | { , } |
| 174 | `<string_elem_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<string_elem_2d_tail>) = { λ } ∪ { } } | { } } |
| 175 | `<bool_array_with_init>` → [ <size> ] <bool_array_init_tail> | FIRST([ <size> ] <bool_array_init_tail>) | { [ } |
| 176 | `<bool_array_init_tail>` → [ <size> ] <bool_arr_init_opt_2d> | FIRST([ <size> ] <bool_arr_init_opt_2d>) | { [ } |
| 177 | `<bool_array_init_tail>` → <bool_arr_init_opt_1d> | FIRST(<bool_arr_init_opt_1d>) ∪ FOLLOW(<bool_array_init_tail>) | { ;, = } |
| 178 | `<bool_arr_init_opt_1d>` → = { <bool_arr_init_content_1d> } | FIRST(= { <bool_arr_init_content_1d> }) | { = } |
| 179 | `<bool_arr_init_opt_1d>` → λ | FIRST(λ) ∪ FOLLOW(<bool_arr_init_opt_1d>) = { λ } ∪ { ; } | { ; } |
| 180 | `<bool_arr_init_content_1d>` → <bool_lit> <bool_elem_1d_tail> | FIRST(<bool_lit> <bool_elem_1d_tail>) | { false, true } |
| 181 | `<bool_elem_1d_tail>` → , <bool_lit> <bool_elem_1d_tail> | FIRST(, <bool_lit> <bool_elem_1d_tail>) | { , } |
| 182 | `<bool_elem_1d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<bool_elem_1d_tail>) = { λ } ∪ { } } | { } } |
| 183 | `<bool_arr_init_opt_2d>` → = { <bool_arr_init_content_2d> } | FIRST(= { <bool_arr_init_content_2d> }) | { = } |
| 184 | `<bool_arr_init_opt_2d>` → λ | FIRST(λ) ∪ FOLLOW(<bool_arr_init_opt_2d>) = { λ } ∪ { ; } | { ; } |
| 185 | `<bool_arr_init_content_2d>` → { <bool_elem_list> } <bool_elem_2d_tail> | FIRST({ <bool_elem_list> } <bool_elem_2d_tail>) | { { } |
| 186 | `<bool_elem_list>` → <bool_lit> <bool_elem_1d_tail> | FIRST(<bool_lit> <bool_elem_1d_tail>) | { false, true } |
| 187 | `<bool_elem_2d_tail>` → , { <bool_elem_list> } <bool_elem_2d_tail> | FIRST(, { <bool_elem_list> } <bool_elem_2d_tai...) | { , } |
| 188 | `<bool_elem_2d_tail>` → λ | FIRST(λ) ∪ FOLLOW(<bool_elem_2d_tail>) = { λ } ∪ { } } | { } } |
| 189 | `<field_list>` → <field_dec> <field_list> | FIRST(<field_dec> <field_list>) | { bool, char, double, float, id, int, long, string } |
| 190 | `<field_list>` → λ | FIRST(λ) ∪ FOLLOW(<field_list>) = { λ } ∪ { } } | { } } |
| 191 | `<field_dec>` → <field_type> id <field_arr_opt> <field_cont> ; | FIRST(<field_type> id <field_arr_opt> <field_c...) | { bool, char, double, float, id, int, long, string } |
| 192 | `<field_type>` → int | FIRST(int) | { int } |
| 193 | `<field_type>` → long | FIRST(long) | { long } |
| 194 | `<field_type>` → float | FIRST(float) | { float } |
| 195 | `<field_type>` → double | FIRST(double) | { double } |
| 196 | `<field_type>` → char | FIRST(char) | { char } |
| 197 | `<field_type>` → string | FIRST(string) | { string } |
| 198 | `<field_type>` → bool | FIRST(bool) | { bool } |
| 199 | `<field_type>` → id | FIRST(id) | { id } |
| 200 | `<field_arr_opt>` → <array_dims> | FIRST(<array_dims>) | { [ } |
| 201 | `<field_arr_opt>` → λ | FIRST(λ) ∪ FOLLOW(<field_arr_opt>) = { λ } ∪ { ,, ; } | { ,, ; } |
| 202 | `<field_cont>` → , id <field_arr_opt> <field_cont> | FIRST(, id <field_arr_opt> <field_cont>) | { , } |
| 203 | `<field_cont>` → λ | FIRST(λ) ∪ FOLLOW(<field_cont>) = { λ } ∪ { ; } | { ; } |
| 204 | `<func_ret_int>` → id ( <param_list> ) { <function_body_int> } | FIRST(id ( <param_list> ) { <function_body_int...) | { id } |
| 205 | `<func_ret_int>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 206 | `<func_ret_long>` → id ( <param_list> ) { <function_body_long> } | FIRST(id ( <param_list> ) { <function_body_lon...) | { id } |
| 207 | `<func_ret_long>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 208 | `<func_ret_float>` → id ( <param_list> ) { <function_body_float> } | FIRST(id ( <param_list> ) { <function_body_flo...) | { id } |
| 209 | `<func_ret_float>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 210 | `<func_ret_double>` → id ( <param_list> ) { <function_body_double> } | FIRST(id ( <param_list> ) { <function_body_dou...) | { id } |
| 211 | `<func_ret_double>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 212 | `<func_ret_char>` → id ( <param_list> ) { <function_body_char> } | FIRST(id ( <param_list> ) { <function_body_cha...) | { id } |
| 213 | `<func_ret_char>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 214 | `<func_ret_string>` → id ( <param_list> ) { <function_body_string> } | FIRST(id ( <param_list> ) { <function_body_str...) | { id } |
| 215 | `<func_ret_string>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 216 | `<func_ret_bool>` → id ( <param_list> ) { <function_body_bool> } | FIRST(id ( <param_list> ) { <function_body_boo...) | { id } |
| 217 | `<func_ret_bool>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 218 | `<func_ret_weave>` → id ( <param_list> ) { <function_body_weave> } | FIRST(id ( <param_list> ) { <function_body_wea...) | { id } |
| 219 | `<func_ret_weave>` → <array_dims> id ( <param_list> ) { <function_body_array> } | FIRST(<array_dims> id ( <param_list> ) { <func...) | { [ } |
| 220 | `<func_ret_weave>` → . id id ( <param_list> ) { <function_body_weave> } | FIRST(. id id ( <param_list> ) { <function_bod...) | { . } |
| 221 | `<param_list>` → <param_type> id <param_arr_opt> <param_cont> | FIRST(<param_type> id <param_arr_opt> <param_c...) | { bool, char, double, float, id, int, long, string } |
| 222 | `<param_list>` → λ | FIRST(λ) ∪ FOLLOW(<param_list>) = { λ } ∪ { ) } | { ) } |
| 223 | `<param_type>` → int | FIRST(int) | { int } |
| 224 | `<param_type>` → long | FIRST(long) | { long } |
| 225 | `<param_type>` → float | FIRST(float) | { float } |
| 226 | `<param_type>` → double | FIRST(double) | { double } |
| 227 | `<param_type>` → char | FIRST(char) | { char } |
| 228 | `<param_type>` → string | FIRST(string) | { string } |
| 229 | `<param_type>` → bool | FIRST(bool) | { bool } |
| 230 | `<param_type>` → id | FIRST(id) | { id } |
| 231 | `<param_arr_opt>` → <array_dims> | FIRST(<array_dims>) | { [ } |
| 232 | `<param_arr_opt>` → λ | FIRST(λ) ∪ FOLLOW(<param_arr_opt>) = { λ } ∪ { ), , } | { ), , } |
| 233 | `<param_cont>` → , <param_type> id <param_arr_opt> <param_cont> | FIRST(, <param_type> id <param_arr_opt> <param...) | { , } |
| 234 | `<param_cont>` → λ | FIRST(λ) ∪ FOLLOW(<param_cont>) = { λ } ∪ { ) } | { ) } |
| 235 | `<function_body_int>` → <func_content_int> | FIRST(<func_content_int>) ∪ FOLLOW(<function_body_int>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 236 | `<func_content_int>` → using id <using_cont> ; <func_content_int> | FIRST(using id <using_cont> ; <func_content_in...) | { using } |
| 237 | `<func_content_int>` → local <mutability> <local_dec_body> <func_content_int> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 238 | `<func_content_int>` → <statement_int> <func_content_int> | FIRST(<statement_int> <func_content_int>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 239 | `<func_content_int>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_int>) = { λ } ∪ { } } | { } } |
| 240 | `<function_body_long>` → <func_content_long> | FIRST(<func_content_long>) ∪ FOLLOW(<function_body_long>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 241 | `<func_content_long>` → using id <using_cont> ; <func_content_long> | FIRST(using id <using_cont> ; <func_content_lo...) | { using } |
| 242 | `<func_content_long>` → local <mutability> <local_dec_body> <func_content_long> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 243 | `<func_content_long>` → <statement_long> <func_content_long> | FIRST(<statement_long> <func_content_long>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 244 | `<func_content_long>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_long>) = { λ } ∪ { } } | { } } |
| 245 | `<function_body_float>` → <func_content_float> | FIRST(<func_content_float>) ∪ FOLLOW(<function_body_float>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 246 | `<func_content_float>` → using id <using_cont> ; <func_content_float> | FIRST(using id <using_cont> ; <func_content_fl...) | { using } |
| 247 | `<func_content_float>` → local <mutability> <local_dec_body> <func_content_float> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 248 | `<func_content_float>` → <statement_float> <func_content_float> | FIRST(<statement_float> <func_content_float>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 249 | `<func_content_float>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_float>) = { λ } ∪ { } } | { } } |
| 250 | `<function_body_double>` → <func_content_double> | FIRST(<func_content_double>) ∪ FOLLOW(<function_body_double>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 251 | `<func_content_double>` → using id <using_cont> ; <func_content_double> | FIRST(using id <using_cont> ; <func_content_do...) | { using } |
| 252 | `<func_content_double>` → local <mutability> <local_dec_body> <func_content_double> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 253 | `<func_content_double>` → <statement_double> <func_content_double> | FIRST(<statement_double> <func_content_double>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 254 | `<func_content_double>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_double>) = { λ } ∪ { } } | { } } |
| 255 | `<function_body_char>` → <func_content_char> | FIRST(<func_content_char>) ∪ FOLLOW(<function_body_char>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 256 | `<func_content_char>` → using id <using_cont> ; <func_content_char> | FIRST(using id <using_cont> ; <func_content_ch...) | { using } |
| 257 | `<func_content_char>` → local <mutability> <local_dec_body> <func_content_char> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 258 | `<func_content_char>` → <statement_char> <func_content_char> | FIRST(<statement_char> <func_content_char>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 259 | `<func_content_char>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_char>) = { λ } ∪ { } } | { } } |
| 260 | `<function_body_string>` → <func_content_string> | FIRST(<func_content_string>) ∪ FOLLOW(<function_body_string>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 261 | `<func_content_string>` → using id <using_cont> ; <func_content_string> | FIRST(using id <using_cont> ; <func_content_st...) | { using } |
| 262 | `<func_content_string>` → local <mutability> <local_dec_body> <func_content_string> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 263 | `<func_content_string>` → <statement_string> <func_content_string> | FIRST(<statement_string> <func_content_string>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 264 | `<func_content_string>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_string>) = { λ } ∪ { } } | { } } |
| 265 | `<function_body_bool>` → <func_content_bool> | FIRST(<func_content_bool>) ∪ FOLLOW(<function_body_bool>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 266 | `<func_content_bool>` → using id <using_cont> ; <func_content_bool> | FIRST(using id <using_cont> ; <func_content_bo...) | { using } |
| 267 | `<func_content_bool>` → local <mutability> <local_dec_body> <func_content_bool> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 268 | `<func_content_bool>` → <statement_bool> <func_content_bool> | FIRST(<statement_bool> <func_content_bool>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 269 | `<func_content_bool>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_bool>) = { λ } ∪ { } } | { } } |
| 270 | `<function_body_array>` → <func_content_array> | FIRST(<func_content_array>) ∪ FOLLOW(<function_body_array>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 271 | `<func_content_array>` → using id <using_cont> ; <func_content_array> | FIRST(using id <using_cont> ; <func_content_ar...) | { using } |
| 272 | `<func_content_array>` → local <mutability> <local_dec_body> <func_content_array> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 273 | `<func_content_array>` → <statement_array> <func_content_array> | FIRST(<statement_array> <func_content_array>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 274 | `<func_content_array>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_array>) = { λ } ∪ { } } | { } } |
| 275 | `<function_body_weave>` → <func_content_weave> | FIRST(<func_content_weave>) ∪ FOLLOW(<function_body_weave>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 276 | `<func_content_weave>` → using id <using_cont> ; <func_content_weave> | FIRST(using id <using_cont> ; <func_content_we...) | { using } |
| 277 | `<func_content_weave>` → local <mutability> <local_dec_body> <func_content_weave> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 278 | `<func_content_weave>` → <statement_weave> <func_content_weave> | FIRST(<statement_weave> <func_content_weave>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 279 | `<func_content_weave>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_weave>) = { λ } ∪ { } } | { } } |
| 280 | `<function_body_void>` → <func_content_void> | FIRST(<func_content_void>) ∪ FOLLOW(<function_body_void>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 281 | `<func_content_void>` → using id <using_cont> ; <func_content_void> | FIRST(using id <using_cont> ; <func_content_vo...) | { using } |
| 282 | `<func_content_void>` → local <mutability> <local_dec_body> <func_content_void> | FIRST(local <mutability> <local_dec_body> <fun...) | { local } |
| 283 | `<func_content_void>` → <statement_void> <func_content_void> | FIRST(<statement_void> <func_content_void>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 284 | `<func_content_void>` → λ | FIRST(λ) ∪ FOLLOW(<func_content_void>) = { λ } ∪ { } } | { } } |
| 285 | `<statement_int>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 286 | `<statement_int>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 287 | `<statement_int>` → <ctrl_struct_int> | FIRST(<ctrl_struct_int>) | { do, for, if, switch, while } |
| 288 | `<statement_int>` → break ; | FIRST(break ;) | { break } |
| 289 | `<statement_int>` → return <int_return_expr> ; | FIRST(return <int_return_expr> ;) | { return } |
| 290 | `<statement_long>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 291 | `<statement_long>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 292 | `<statement_long>` → <ctrl_struct_long> | FIRST(<ctrl_struct_long>) | { do, for, if, switch, while } |
| 293 | `<statement_long>` → break ; | FIRST(break ;) | { break } |
| 294 | `<statement_long>` → return <long_return_expr> ; | FIRST(return <long_return_expr> ;) | { return } |
| 295 | `<statement_float>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 296 | `<statement_float>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 297 | `<statement_float>` → <ctrl_struct_float> | FIRST(<ctrl_struct_float>) | { do, for, if, switch, while } |
| 298 | `<statement_float>` → break ; | FIRST(break ;) | { break } |
| 299 | `<statement_float>` → return <float_return_expr> ; | FIRST(return <float_return_expr> ;) | { return } |
| 300 | `<statement_double>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 301 | `<statement_double>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 302 | `<statement_double>` → <ctrl_struct_double> | FIRST(<ctrl_struct_double>) | { do, for, if, switch, while } |
| 303 | `<statement_double>` → break ; | FIRST(break ;) | { break } |
| 304 | `<statement_double>` → return <double_return_expr> ; | FIRST(return <double_return_expr> ;) | { return } |
| 305 | `<statement_char>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 306 | `<statement_char>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 307 | `<statement_char>` → <ctrl_struct_char> | FIRST(<ctrl_struct_char>) | { do, for, if, switch, while } |
| 308 | `<statement_char>` → break ; | FIRST(break ;) | { break } |
| 309 | `<statement_char>` → return <char_return_expr> ; | FIRST(return <char_return_expr> ;) | { return } |
| 310 | `<statement_string>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 311 | `<statement_string>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 312 | `<statement_string>` → <ctrl_struct_string> | FIRST(<ctrl_struct_string>) | { do, for, if, switch, while } |
| 313 | `<statement_string>` → break ; | FIRST(break ;) | { break } |
| 314 | `<statement_string>` → return <string_return_expr> ; | FIRST(return <string_return_expr> ;) | { return } |
| 315 | `<statement_bool>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 316 | `<statement_bool>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 317 | `<statement_bool>` → <ctrl_struct_bool> | FIRST(<ctrl_struct_bool>) | { do, for, if, switch, while } |
| 318 | `<statement_bool>` → break ; | FIRST(break ;) | { break } |
| 319 | `<statement_bool>` → return <bool_return_expr> ; | FIRST(return <bool_return_expr> ;) | { return } |
| 320 | `<statement_array>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 321 | `<statement_array>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 322 | `<statement_array>` → <ctrl_struct_array> | FIRST(<ctrl_struct_array>) | { do, for, if, switch, while } |
| 323 | `<statement_array>` → break ; | FIRST(break ;) | { break } |
| 324 | `<statement_array>` → return id ; | FIRST(return id ;) | { return } |
| 325 | `<statement_weave>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 326 | `<statement_weave>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 327 | `<statement_weave>` → <ctrl_struct_weave> | FIRST(<ctrl_struct_weave>) | { do, for, if, switch, while } |
| 328 | `<statement_weave>` → break ; | FIRST(break ;) | { break } |
| 329 | `<statement_weave>` → return id ; | FIRST(return id ;) | { return } |
| 330 | `<statement_void>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 331 | `<statement_void>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 332 | `<statement_void>` → <ctrl_struct_void> | FIRST(<ctrl_struct_void>) | { do, for, if, switch, while } |
| 333 | `<statement_void>` → break ; | FIRST(break ;) | { break } |
| 334 | `<statement_void>` → return ; | FIRST(return ;) | { return } |
| 335 | `<ctrl_struct_int>` → if ( <condition> ) { <stmt_list_int> } <else_opt_int> | FIRST(if ( <condition> ) { <stmt_list_int> } <...) | { if } |
| 336 | `<ctrl_struct_int>` → switch ( <arg_expr> ) { <case_list_int> <default_opt_int> } | FIRST(switch ( <arg_expr> ) { <case_list_int> ...) | { switch } |
| 337 | `<ctrl_struct_int>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_int> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 338 | `<ctrl_struct_int>` → while ( <condition> ) { <stmt_list_int> } | FIRST(while ( <condition> ) { <stmt_list_int> ...) | { while } |
| 339 | `<ctrl_struct_int>` → do { <stmt_list_int> } while ( <condition> ) ; | FIRST(do { <stmt_list_int> } while ( <conditio...) | { do } |
| 340 | `<stmt_list_int>` → <statement_int> <stmt_list_int> | FIRST(<statement_int> <stmt_list_int>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 341 | `<stmt_list_int>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_int>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 342 | `<else_opt_int>` → else <else_body_int> | FIRST(else <else_body_int>) | { else } |
| 343 | `<else_opt_int>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_int>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 344 | `<else_body_int>` → { <stmt_list_int> } | FIRST({ <stmt_list_int> }) | { { } |
| 345 | `<else_body_int>` → if ( <condition> ) { <stmt_list_int> } <else_opt_int> | FIRST(if ( <condition> ) { <stmt_list_int> } <...) | { if } |
| 346 | `<case_list_int>` → case <case_val> : <stmt_list_int> <break_opt> <case_list_int> | FIRST(case <case_val> : <stmt_list_int> <break...) | { case } |
| 347 | `<case_list_int>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_int>) = { λ } ∪ { default, } } | { default, } } |
| 348 | `<default_opt_int>` → default : <stmt_list_int> <break_opt> | FIRST(default : <stmt_list_int> <break_opt>) | { default } |
| 349 | `<default_opt_int>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_int>) = { λ } ∪ { } } | { } } |
| 350 | `<ctrl_struct_long>` → if ( <condition> ) { <stmt_list_long> } <else_opt_long> | FIRST(if ( <condition> ) { <stmt_list_long> } ...) | { if } |
| 351 | `<ctrl_struct_long>` → switch ( <arg_expr> ) { <case_list_long> <default_opt_long> } | FIRST(switch ( <arg_expr> ) { <case_list_long>...) | { switch } |
| 352 | `<ctrl_struct_long>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_long> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 353 | `<ctrl_struct_long>` → while ( <condition> ) { <stmt_list_long> } | FIRST(while ( <condition> ) { <stmt_list_long>...) | { while } |
| 354 | `<ctrl_struct_long>` → do { <stmt_list_long> } while ( <condition> ) ; | FIRST(do { <stmt_list_long> } while ( <conditi...) | { do } |
| 355 | `<stmt_list_long>` → <statement_long> <stmt_list_long> | FIRST(<statement_long> <stmt_list_long>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 356 | `<stmt_list_long>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_long>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 357 | `<else_opt_long>` → else <else_body_long> | FIRST(else <else_body_long>) | { else } |
| 358 | `<else_opt_long>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_long>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 359 | `<else_body_long>` → { <stmt_list_long> } | FIRST({ <stmt_list_long> }) | { { } |
| 360 | `<else_body_long>` → if ( <condition> ) { <stmt_list_long> } <else_opt_long> | FIRST(if ( <condition> ) { <stmt_list_long> } ...) | { if } |
| 361 | `<case_list_long>` → case <case_val> : <stmt_list_long> <break_opt> <case_list_long> | FIRST(case <case_val> : <stmt_list_long> <brea...) | { case } |
| 362 | `<case_list_long>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_long>) = { λ } ∪ { default, } } | { default, } } |
| 363 | `<default_opt_long>` → default : <stmt_list_long> <break_opt> | FIRST(default : <stmt_list_long> <break_opt>) | { default } |
| 364 | `<default_opt_long>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_long>) = { λ } ∪ { } } | { } } |
| 365 | `<ctrl_struct_float>` → if ( <condition> ) { <stmt_list_float> } <else_opt_float> | FIRST(if ( <condition> ) { <stmt_list_float> }...) | { if } |
| 366 | `<ctrl_struct_float>` → switch ( <arg_expr> ) { <case_list_float> <default_opt_float> } | FIRST(switch ( <arg_expr> ) { <case_list_float...) | { switch } |
| 367 | `<ctrl_struct_float>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_float> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 368 | `<ctrl_struct_float>` → while ( <condition> ) { <stmt_list_float> } | FIRST(while ( <condition> ) { <stmt_list_float...) | { while } |
| 369 | `<ctrl_struct_float>` → do { <stmt_list_float> } while ( <condition> ) ; | FIRST(do { <stmt_list_float> } while ( <condit...) | { do } |
| 370 | `<stmt_list_float>` → <statement_float> <stmt_list_float> | FIRST(<statement_float> <stmt_list_float>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 371 | `<stmt_list_float>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_float>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 372 | `<else_opt_float>` → else <else_body_float> | FIRST(else <else_body_float>) | { else } |
| 373 | `<else_opt_float>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_float>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 374 | `<else_body_float>` → { <stmt_list_float> } | FIRST({ <stmt_list_float> }) | { { } |
| 375 | `<else_body_float>` → if ( <condition> ) { <stmt_list_float> } <else_opt_float> | FIRST(if ( <condition> ) { <stmt_list_float> }...) | { if } |
| 376 | `<case_list_float>` → case <case_val> : <stmt_list_float> <break_opt> <case_list_float> | FIRST(case <case_val> : <stmt_list_float> <bre...) | { case } |
| 377 | `<case_list_float>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_float>) = { λ } ∪ { default, } } | { default, } } |
| 378 | `<default_opt_float>` → default : <stmt_list_float> <break_opt> | FIRST(default : <stmt_list_float> <break_opt>) | { default } |
| 379 | `<default_opt_float>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_float>) = { λ } ∪ { } } | { } } |
| 380 | `<ctrl_struct_double>` → if ( <condition> ) { <stmt_list_double> } <else_opt_double> | FIRST(if ( <condition> ) { <stmt_list_double> ...) | { if } |
| 381 | `<ctrl_struct_double>` → switch ( <arg_expr> ) { <case_list_double> <default_opt_double> } | FIRST(switch ( <arg_expr> ) { <case_list_doubl...) | { switch } |
| 382 | `<ctrl_struct_double>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_double> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 383 | `<ctrl_struct_double>` → while ( <condition> ) { <stmt_list_double> } | FIRST(while ( <condition> ) { <stmt_list_doubl...) | { while } |
| 384 | `<ctrl_struct_double>` → do { <stmt_list_double> } while ( <condition> ) ; | FIRST(do { <stmt_list_double> } while ( <condi...) | { do } |
| 385 | `<stmt_list_double>` → <statement_double> <stmt_list_double> | FIRST(<statement_double> <stmt_list_double>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 386 | `<stmt_list_double>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_double>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 387 | `<else_opt_double>` → else <else_body_double> | FIRST(else <else_body_double>) | { else } |
| 388 | `<else_opt_double>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_double>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 389 | `<else_body_double>` → { <stmt_list_double> } | FIRST({ <stmt_list_double> }) | { { } |
| 390 | `<else_body_double>` → if ( <condition> ) { <stmt_list_double> } <else_opt_double> | FIRST(if ( <condition> ) { <stmt_list_double> ...) | { if } |
| 391 | `<case_list_double>` → case <case_val> : <stmt_list_double> <break_opt> <case_list_double> | FIRST(case <case_val> : <stmt_list_double> <br...) | { case } |
| 392 | `<case_list_double>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_double>) = { λ } ∪ { default, } } | { default, } } |
| 393 | `<default_opt_double>` → default : <stmt_list_double> <break_opt> | FIRST(default : <stmt_list_double> <break_opt>) | { default } |
| 394 | `<default_opt_double>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_double>) = { λ } ∪ { } } | { } } |
| 395 | `<ctrl_struct_char>` → if ( <condition> ) { <stmt_list_char> } <else_opt_char> | FIRST(if ( <condition> ) { <stmt_list_char> } ...) | { if } |
| 396 | `<ctrl_struct_char>` → switch ( <arg_expr> ) { <case_list_char> <default_opt_char> } | FIRST(switch ( <arg_expr> ) { <case_list_char>...) | { switch } |
| 397 | `<ctrl_struct_char>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_char> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 398 | `<ctrl_struct_char>` → while ( <condition> ) { <stmt_list_char> } | FIRST(while ( <condition> ) { <stmt_list_char>...) | { while } |
| 399 | `<ctrl_struct_char>` → do { <stmt_list_char> } while ( <condition> ) ; | FIRST(do { <stmt_list_char> } while ( <conditi...) | { do } |
| 400 | `<stmt_list_char>` → <statement_char> <stmt_list_char> | FIRST(<statement_char> <stmt_list_char>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 401 | `<stmt_list_char>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_char>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 402 | `<else_opt_char>` → else <else_body_char> | FIRST(else <else_body_char>) | { else } |
| 403 | `<else_opt_char>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_char>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 404 | `<else_body_char>` → { <stmt_list_char> } | FIRST({ <stmt_list_char> }) | { { } |
| 405 | `<else_body_char>` → if ( <condition> ) { <stmt_list_char> } <else_opt_char> | FIRST(if ( <condition> ) { <stmt_list_char> } ...) | { if } |
| 406 | `<case_list_char>` → case <case_val> : <stmt_list_char> <break_opt> <case_list_char> | FIRST(case <case_val> : <stmt_list_char> <brea...) | { case } |
| 407 | `<case_list_char>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_char>) = { λ } ∪ { default, } } | { default, } } |
| 408 | `<default_opt_char>` → default : <stmt_list_char> <break_opt> | FIRST(default : <stmt_list_char> <break_opt>) | { default } |
| 409 | `<default_opt_char>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_char>) = { λ } ∪ { } } | { } } |
| 410 | `<ctrl_struct_string>` → if ( <condition> ) { <stmt_list_string> } <else_opt_string> | FIRST(if ( <condition> ) { <stmt_list_string> ...) | { if } |
| 411 | `<ctrl_struct_string>` → switch ( <arg_expr> ) { <case_list_string> <default_opt_string> } | FIRST(switch ( <arg_expr> ) { <case_list_strin...) | { switch } |
| 412 | `<ctrl_struct_string>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_string> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 413 | `<ctrl_struct_string>` → while ( <condition> ) { <stmt_list_string> } | FIRST(while ( <condition> ) { <stmt_list_strin...) | { while } |
| 414 | `<ctrl_struct_string>` → do { <stmt_list_string> } while ( <condition> ) ; | FIRST(do { <stmt_list_string> } while ( <condi...) | { do } |
| 415 | `<stmt_list_string>` → <statement_string> <stmt_list_string> | FIRST(<statement_string> <stmt_list_string>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 416 | `<stmt_list_string>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_string>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 417 | `<else_opt_string>` → else <else_body_string> | FIRST(else <else_body_string>) | { else } |
| 418 | `<else_opt_string>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_string>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 419 | `<else_body_string>` → { <stmt_list_string> } | FIRST({ <stmt_list_string> }) | { { } |
| 420 | `<else_body_string>` → if ( <condition> ) { <stmt_list_string> } <else_opt_string> | FIRST(if ( <condition> ) { <stmt_list_string> ...) | { if } |
| 421 | `<case_list_string>` → case <case_val> : <stmt_list_string> <break_opt> <case_list_string> | FIRST(case <case_val> : <stmt_list_string> <br...) | { case } |
| 422 | `<case_list_string>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_string>) = { λ } ∪ { default, } } | { default, } } |
| 423 | `<default_opt_string>` → default : <stmt_list_string> <break_opt> | FIRST(default : <stmt_list_string> <break_opt>) | { default } |
| 424 | `<default_opt_string>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_string>) = { λ } ∪ { } } | { } } |
| 425 | `<ctrl_struct_bool>` → if ( <condition> ) { <stmt_list_bool> } <else_opt_bool> | FIRST(if ( <condition> ) { <stmt_list_bool> } ...) | { if } |
| 426 | `<ctrl_struct_bool>` → switch ( <arg_expr> ) { <case_list_bool> <default_opt_bool> } | FIRST(switch ( <arg_expr> ) { <case_list_bool>...) | { switch } |
| 427 | `<ctrl_struct_bool>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_bool> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 428 | `<ctrl_struct_bool>` → while ( <condition> ) { <stmt_list_bool> } | FIRST(while ( <condition> ) { <stmt_list_bool>...) | { while } |
| 429 | `<ctrl_struct_bool>` → do { <stmt_list_bool> } while ( <condition> ) ; | FIRST(do { <stmt_list_bool> } while ( <conditi...) | { do } |
| 430 | `<stmt_list_bool>` → <statement_bool> <stmt_list_bool> | FIRST(<statement_bool> <stmt_list_bool>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 431 | `<stmt_list_bool>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_bool>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 432 | `<else_opt_bool>` → else <else_body_bool> | FIRST(else <else_body_bool>) | { else } |
| 433 | `<else_opt_bool>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_bool>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 434 | `<else_body_bool>` → { <stmt_list_bool> } | FIRST({ <stmt_list_bool> }) | { { } |
| 435 | `<else_body_bool>` → if ( <condition> ) { <stmt_list_bool> } <else_opt_bool> | FIRST(if ( <condition> ) { <stmt_list_bool> } ...) | { if } |
| 436 | `<case_list_bool>` → case <case_val> : <stmt_list_bool> <break_opt> <case_list_bool> | FIRST(case <case_val> : <stmt_list_bool> <brea...) | { case } |
| 437 | `<case_list_bool>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_bool>) = { λ } ∪ { default, } } | { default, } } |
| 438 | `<default_opt_bool>` → default : <stmt_list_bool> <break_opt> | FIRST(default : <stmt_list_bool> <break_opt>) | { default } |
| 439 | `<default_opt_bool>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_bool>) = { λ } ∪ { } } | { } } |
| 440 | `<ctrl_struct_array>` → if ( <condition> ) { <stmt_list_array> } <else_opt_array> | FIRST(if ( <condition> ) { <stmt_list_array> }...) | { if } |
| 441 | `<ctrl_struct_array>` → switch ( <arg_expr> ) { <case_list_array> <default_opt_array> } | FIRST(switch ( <arg_expr> ) { <case_list_array...) | { switch } |
| 442 | `<ctrl_struct_array>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_array> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 443 | `<ctrl_struct_array>` → while ( <condition> ) { <stmt_list_array> } | FIRST(while ( <condition> ) { <stmt_list_array...) | { while } |
| 444 | `<ctrl_struct_array>` → do { <stmt_list_array> } while ( <condition> ) ; | FIRST(do { <stmt_list_array> } while ( <condit...) | { do } |
| 445 | `<stmt_list_array>` → <statement_array> <stmt_list_array> | FIRST(<statement_array> <stmt_list_array>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 446 | `<stmt_list_array>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_array>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 447 | `<else_opt_array>` → else <else_body_array> | FIRST(else <else_body_array>) | { else } |
| 448 | `<else_opt_array>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_array>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 449 | `<else_body_array>` → { <stmt_list_array> } | FIRST({ <stmt_list_array> }) | { { } |
| 450 | `<else_body_array>` → if ( <condition> ) { <stmt_list_array> } <else_opt_array> | FIRST(if ( <condition> ) { <stmt_list_array> }...) | { if } |
| 451 | `<case_list_array>` → case <case_val> : <stmt_list_array> <break_opt> <case_list_array> | FIRST(case <case_val> : <stmt_list_array> <bre...) | { case } |
| 452 | `<case_list_array>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_array>) = { λ } ∪ { default, } } | { default, } } |
| 453 | `<default_opt_array>` → default : <stmt_list_array> <break_opt> | FIRST(default : <stmt_list_array> <break_opt>) | { default } |
| 454 | `<default_opt_array>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_array>) = { λ } ∪ { } } | { } } |
| 455 | `<ctrl_struct_weave>` → if ( <condition> ) { <stmt_list_weave> } <else_opt_weave> | FIRST(if ( <condition> ) { <stmt_list_weave> }...) | { if } |
| 456 | `<ctrl_struct_weave>` → switch ( <arg_expr> ) { <case_list_weave> <default_opt_weave> } | FIRST(switch ( <arg_expr> ) { <case_list_weave...) | { switch } |
| 457 | `<ctrl_struct_weave>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_weave> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 458 | `<ctrl_struct_weave>` → while ( <condition> ) { <stmt_list_weave> } | FIRST(while ( <condition> ) { <stmt_list_weave...) | { while } |
| 459 | `<ctrl_struct_weave>` → do { <stmt_list_weave> } while ( <condition> ) ; | FIRST(do { <stmt_list_weave> } while ( <condit...) | { do } |
| 460 | `<stmt_list_weave>` → <statement_weave> <stmt_list_weave> | FIRST(<statement_weave> <stmt_list_weave>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 461 | `<stmt_list_weave>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_weave>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 462 | `<else_opt_weave>` → else <else_body_weave> | FIRST(else <else_body_weave>) | { else } |
| 463 | `<else_opt_weave>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_weave>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 464 | `<else_body_weave>` → { <stmt_list_weave> } | FIRST({ <stmt_list_weave> }) | { { } |
| 465 | `<else_body_weave>` → if ( <condition> ) { <stmt_list_weave> } <else_opt_weave> | FIRST(if ( <condition> ) { <stmt_list_weave> }...) | { if } |
| 466 | `<case_list_weave>` → case <case_val> : <stmt_list_weave> <break_opt> <case_list_weave> | FIRST(case <case_val> : <stmt_list_weave> <bre...) | { case } |
| 467 | `<case_list_weave>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_weave>) = { λ } ∪ { default, } } | { default, } } |
| 468 | `<default_opt_weave>` → default : <stmt_list_weave> <break_opt> | FIRST(default : <stmt_list_weave> <break_opt>) | { default } |
| 469 | `<default_opt_weave>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_weave>) = { λ } ∪ { } } | { } } |
| 470 | `<ctrl_struct_void>` → if ( <condition> ) { <stmt_list_void> } <else_opt_void> | FIRST(if ( <condition> ) { <stmt_list_void> } ...) | { if } |
| 471 | `<ctrl_struct_void>` → switch ( <arg_expr> ) { <case_list_void> <default_opt_void> } | FIRST(switch ( <arg_expr> ) { <case_list_void>...) | { switch } |
| 472 | `<ctrl_struct_void>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <stmt_list_void> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 473 | `<ctrl_struct_void>` → while ( <condition> ) { <stmt_list_void> } | FIRST(while ( <condition> ) { <stmt_list_void>...) | { while } |
| 474 | `<ctrl_struct_void>` → do { <stmt_list_void> } while ( <condition> ) ; | FIRST(do { <stmt_list_void> } while ( <conditi...) | { do } |
| 475 | `<stmt_list_void>` → <statement_void> <stmt_list_void> | FIRST(<statement_void> <stmt_list_void>) | { ++, --, break, do, for, id, if, return, switch, thread, threadln, trap, while } |
| 476 | `<stmt_list_void>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_list_void>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 477 | `<else_opt_void>` → else <else_body_void> | FIRST(else <else_body_void>) | { else } |
| 478 | `<else_opt_void>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt_void>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 479 | `<else_body_void>` → { <stmt_list_void> } | FIRST({ <stmt_list_void> }) | { { } |
| 480 | `<else_body_void>` → if ( <condition> ) { <stmt_list_void> } <else_opt_void> | FIRST(if ( <condition> ) { <stmt_list_void> } ...) | { if } |
| 481 | `<case_list_void>` → case <case_val> : <stmt_list_void> <break_opt> <case_list_void> | FIRST(case <case_val> : <stmt_list_void> <brea...) | { case } |
| 482 | `<case_list_void>` → λ | FIRST(λ) ∪ FOLLOW(<case_list_void>) = { λ } ∪ { default, } } | { default, } } |
| 483 | `<default_opt_void>` → default : <stmt_list_void> <break_opt> | FIRST(default : <stmt_list_void> <break_opt>) | { default } |
| 484 | `<default_opt_void>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt_void>) = { λ } ∪ { } } | { } } |
| 485 | `<int_return_expr>` → <int_ret_assign> | FIRST(<int_ret_assign>) | { !, (, ++, --, id, int, intlit } |
| 486 | `<int_ret_assign>` → <int_ret_concat> <assign_tail> | FIRST(<int_ret_concat> <assign_tail>) | { !, (, ++, --, id, int, intlit } |
| 487 | `<int_ret_concat>` → <int_ret_or> <concat_tail> | FIRST(<int_ret_or> <concat_tail>) | { !, (, ++, --, id, int, intlit } |
| 488 | `<int_ret_or>` → <int_ret_and> <or_tail> | FIRST(<int_ret_and> <or_tail>) | { !, (, ++, --, id, int, intlit } |
| 489 | `<int_ret_and>` → <int_ret_eq> <and_tail> | FIRST(<int_ret_eq> <and_tail>) | { !, (, ++, --, id, int, intlit } |
| 490 | `<int_ret_eq>` → <int_ret_rel> <eq_tail> | FIRST(<int_ret_rel> <eq_tail>) | { !, (, ++, --, id, int, intlit } |
| 491 | `<int_ret_rel>` → <int_ret_add> <rel_tail> | FIRST(<int_ret_add> <rel_tail>) | { !, (, ++, --, id, int, intlit } |
| 492 | `<int_ret_add>` → <int_ret_mul> <add_tail> | FIRST(<int_ret_mul> <add_tail>) | { !, (, ++, --, id, int, intlit } |
| 493 | `<int_ret_mul>` → <int_ret_unary> <mul_tail> | FIRST(<int_ret_unary> <mul_tail>) | { !, (, ++, --, id, int, intlit } |
| 494 | `<int_ret_unary>` → ! <int_ret_unary> | FIRST(! <int_ret_unary>) | { ! } |
| 495 | `<int_ret_unary>` → <int_ret_postfix> | FIRST(<int_ret_postfix>) | { (, ++, --, id, int, intlit } |
| 496 | `<int_ret_postfix>` → intlit | FIRST(intlit) | { intlit } |
| 497 | `<int_ret_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 498 | `<int_ret_postfix>` → -- id | FIRST(-- id) | { -- } |
| 499 | `<int_ret_postfix>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 500 | `<int_ret_postfix>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 501 | `<int_ret_postfix>` → int ( <expression> ) | FIRST(int ( <expression> )) | { int } |
| 502 | `<long_return_expr>` → <long_ret_assign> | FIRST(<long_ret_assign>) | { !, (, ++, --, id, long, longlit } |
| 503 | `<long_ret_assign>` → <long_ret_concat> <assign_tail> | FIRST(<long_ret_concat> <assign_tail>) | { !, (, ++, --, id, long, longlit } |
| 504 | `<long_ret_concat>` → <long_ret_or> <concat_tail> | FIRST(<long_ret_or> <concat_tail>) | { !, (, ++, --, id, long, longlit } |
| 505 | `<long_ret_or>` → <long_ret_and> <or_tail> | FIRST(<long_ret_and> <or_tail>) | { !, (, ++, --, id, long, longlit } |
| 506 | `<long_ret_and>` → <long_ret_eq> <and_tail> | FIRST(<long_ret_eq> <and_tail>) | { !, (, ++, --, id, long, longlit } |
| 507 | `<long_ret_eq>` → <long_ret_rel> <eq_tail> | FIRST(<long_ret_rel> <eq_tail>) | { !, (, ++, --, id, long, longlit } |
| 508 | `<long_ret_rel>` → <long_ret_add> <rel_tail> | FIRST(<long_ret_add> <rel_tail>) | { !, (, ++, --, id, long, longlit } |
| 509 | `<long_ret_add>` → <long_ret_mul> <add_tail> | FIRST(<long_ret_mul> <add_tail>) | { !, (, ++, --, id, long, longlit } |
| 510 | `<long_ret_mul>` → <long_ret_unary> <mul_tail> | FIRST(<long_ret_unary> <mul_tail>) | { !, (, ++, --, id, long, longlit } |
| 511 | `<long_ret_unary>` → ! <long_ret_unary> | FIRST(! <long_ret_unary>) | { ! } |
| 512 | `<long_ret_unary>` → <long_ret_postfix> | FIRST(<long_ret_postfix>) | { (, ++, --, id, long, longlit } |
| 513 | `<long_ret_postfix>` → longlit | FIRST(longlit) | { longlit } |
| 514 | `<long_ret_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 515 | `<long_ret_postfix>` → -- id | FIRST(-- id) | { -- } |
| 516 | `<long_ret_postfix>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 517 | `<long_ret_postfix>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 518 | `<long_ret_postfix>` → long ( <expression> ) | FIRST(long ( <expression> )) | { long } |
| 519 | `<float_return_expr>` → <float_ret_assign> | FIRST(<float_ret_assign>) | { !, (, ++, --, float, floatlit, id } |
| 520 | `<float_ret_assign>` → <float_ret_concat> <assign_tail> | FIRST(<float_ret_concat> <assign_tail>) | { !, (, ++, --, float, floatlit, id } |
| 521 | `<float_ret_concat>` → <float_ret_or> <concat_tail> | FIRST(<float_ret_or> <concat_tail>) | { !, (, ++, --, float, floatlit, id } |
| 522 | `<float_ret_or>` → <float_ret_and> <or_tail> | FIRST(<float_ret_and> <or_tail>) | { !, (, ++, --, float, floatlit, id } |
| 523 | `<float_ret_and>` → <float_ret_eq> <and_tail> | FIRST(<float_ret_eq> <and_tail>) | { !, (, ++, --, float, floatlit, id } |
| 524 | `<float_ret_eq>` → <float_ret_rel> <eq_tail> | FIRST(<float_ret_rel> <eq_tail>) | { !, (, ++, --, float, floatlit, id } |
| 525 | `<float_ret_rel>` → <float_ret_add> <rel_tail> | FIRST(<float_ret_add> <rel_tail>) | { !, (, ++, --, float, floatlit, id } |
| 526 | `<float_ret_add>` → <float_ret_mul> <add_tail> | FIRST(<float_ret_mul> <add_tail>) | { !, (, ++, --, float, floatlit, id } |
| 527 | `<float_ret_mul>` → <float_ret_unary> <mul_tail> | FIRST(<float_ret_unary> <mul_tail>) | { !, (, ++, --, float, floatlit, id } |
| 528 | `<float_ret_unary>` → ! <float_ret_unary> | FIRST(! <float_ret_unary>) | { ! } |
| 529 | `<float_ret_unary>` → <float_ret_postfix> | FIRST(<float_ret_postfix>) | { (, ++, --, float, floatlit, id } |
| 530 | `<float_ret_postfix>` → floatlit | FIRST(floatlit) | { floatlit } |
| 531 | `<float_ret_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 532 | `<float_ret_postfix>` → -- id | FIRST(-- id) | { -- } |
| 533 | `<float_ret_postfix>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 534 | `<float_ret_postfix>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 535 | `<float_ret_postfix>` → float ( <expression> ) | FIRST(float ( <expression> )) | { float } |
| 536 | `<double_return_expr>` → <double_ret_assign> | FIRST(<double_ret_assign>) | { !, (, ++, --, double, doublelit, id } |
| 537 | `<double_ret_assign>` → <double_ret_concat> <assign_tail> | FIRST(<double_ret_concat> <assign_tail>) | { !, (, ++, --, double, doublelit, id } |
| 538 | `<double_ret_concat>` → <double_ret_or> <concat_tail> | FIRST(<double_ret_or> <concat_tail>) | { !, (, ++, --, double, doublelit, id } |
| 539 | `<double_ret_or>` → <double_ret_and> <or_tail> | FIRST(<double_ret_and> <or_tail>) | { !, (, ++, --, double, doublelit, id } |
| 540 | `<double_ret_and>` → <double_ret_eq> <and_tail> | FIRST(<double_ret_eq> <and_tail>) | { !, (, ++, --, double, doublelit, id } |
| 541 | `<double_ret_eq>` → <double_ret_rel> <eq_tail> | FIRST(<double_ret_rel> <eq_tail>) | { !, (, ++, --, double, doublelit, id } |
| 542 | `<double_ret_rel>` → <double_ret_add> <rel_tail> | FIRST(<double_ret_add> <rel_tail>) | { !, (, ++, --, double, doublelit, id } |
| 543 | `<double_ret_add>` → <double_ret_mul> <add_tail> | FIRST(<double_ret_mul> <add_tail>) | { !, (, ++, --, double, doublelit, id } |
| 544 | `<double_ret_mul>` → <double_ret_unary> <mul_tail> | FIRST(<double_ret_unary> <mul_tail>) | { !, (, ++, --, double, doublelit, id } |
| 545 | `<double_ret_unary>` → ! <double_ret_unary> | FIRST(! <double_ret_unary>) | { ! } |
| 546 | `<double_ret_unary>` → <double_ret_postfix> | FIRST(<double_ret_postfix>) | { (, ++, --, double, doublelit, id } |
| 547 | `<double_ret_postfix>` → doublelit | FIRST(doublelit) | { doublelit } |
| 548 | `<double_ret_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 549 | `<double_ret_postfix>` → -- id | FIRST(-- id) | { -- } |
| 550 | `<double_ret_postfix>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 551 | `<double_ret_postfix>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 552 | `<double_ret_postfix>` → double ( <expression> ) | FIRST(double ( <expression> )) | { double } |
| 553 | `<char_return_expr>` → <char_ret_assign> | FIRST(<char_ret_assign>) | { !, (, ++, --, char, charlit, id } |
| 554 | `<char_ret_assign>` → <char_ret_concat> <assign_tail> | FIRST(<char_ret_concat> <assign_tail>) | { !, (, ++, --, char, charlit, id } |
| 555 | `<char_ret_concat>` → <char_ret_or> <concat_tail> | FIRST(<char_ret_or> <concat_tail>) | { !, (, ++, --, char, charlit, id } |
| 556 | `<char_ret_or>` → <char_ret_and> <or_tail> | FIRST(<char_ret_and> <or_tail>) | { !, (, ++, --, char, charlit, id } |
| 557 | `<char_ret_and>` → <char_ret_eq> <and_tail> | FIRST(<char_ret_eq> <and_tail>) | { !, (, ++, --, char, charlit, id } |
| 558 | `<char_ret_eq>` → <char_ret_rel> <eq_tail> | FIRST(<char_ret_rel> <eq_tail>) | { !, (, ++, --, char, charlit, id } |
| 559 | `<char_ret_rel>` → <char_ret_add> <rel_tail> | FIRST(<char_ret_add> <rel_tail>) | { !, (, ++, --, char, charlit, id } |
| 560 | `<char_ret_add>` → <char_ret_mul> <add_tail> | FIRST(<char_ret_mul> <add_tail>) | { !, (, ++, --, char, charlit, id } |
| 561 | `<char_ret_mul>` → <char_ret_unary> <mul_tail> | FIRST(<char_ret_unary> <mul_tail>) | { !, (, ++, --, char, charlit, id } |
| 562 | `<char_ret_unary>` → ! <char_ret_unary> | FIRST(! <char_ret_unary>) | { ! } |
| 563 | `<char_ret_unary>` → <char_ret_postfix> | FIRST(<char_ret_postfix>) | { (, ++, --, char, charlit, id } |
| 564 | `<char_ret_postfix>` → charlit | FIRST(charlit) | { charlit } |
| 565 | `<char_ret_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 566 | `<char_ret_postfix>` → -- id | FIRST(-- id) | { -- } |
| 567 | `<char_ret_postfix>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 568 | `<char_ret_postfix>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 569 | `<char_ret_postfix>` → char ( <expression> ) | FIRST(char ( <expression> )) | { char } |
| 570 | `<string_return_expr>` → <string_ret_assign> | FIRST(<string_ret_assign>) | { !, (, ++, --, id, string, stringlit } |
| 571 | `<string_ret_assign>` → <string_ret_concat> <assign_tail> | FIRST(<string_ret_concat> <assign_tail>) | { !, (, ++, --, id, string, stringlit } |
| 572 | `<string_ret_concat>` → <string_ret_or> <concat_tail> | FIRST(<string_ret_or> <concat_tail>) | { !, (, ++, --, id, string, stringlit } |
| 573 | `<string_ret_or>` → <string_ret_and> <or_tail> | FIRST(<string_ret_and> <or_tail>) | { !, (, ++, --, id, string, stringlit } |
| 574 | `<string_ret_and>` → <string_ret_eq> <and_tail> | FIRST(<string_ret_eq> <and_tail>) | { !, (, ++, --, id, string, stringlit } |
| 575 | `<string_ret_eq>` → <string_ret_rel> <eq_tail> | FIRST(<string_ret_rel> <eq_tail>) | { !, (, ++, --, id, string, stringlit } |
| 576 | `<string_ret_rel>` → <string_ret_add> <rel_tail> | FIRST(<string_ret_add> <rel_tail>) | { !, (, ++, --, id, string, stringlit } |
| 577 | `<string_ret_add>` → <string_ret_mul> <add_tail> | FIRST(<string_ret_mul> <add_tail>) | { !, (, ++, --, id, string, stringlit } |
| 578 | `<string_ret_mul>` → <string_ret_unary> <mul_tail> | FIRST(<string_ret_unary> <mul_tail>) | { !, (, ++, --, id, string, stringlit } |
| 579 | `<string_ret_unary>` → ! <string_ret_unary> | FIRST(! <string_ret_unary>) | { ! } |
| 580 | `<string_ret_unary>` → <string_ret_postfix> | FIRST(<string_ret_postfix>) | { (, ++, --, id, string, stringlit } |
| 581 | `<string_ret_postfix>` → stringlit | FIRST(stringlit) | { stringlit } |
| 582 | `<string_ret_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 583 | `<string_ret_postfix>` → -- id | FIRST(-- id) | { -- } |
| 584 | `<string_ret_postfix>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 585 | `<string_ret_postfix>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 586 | `<string_ret_postfix>` → string ( <expression> ) | FIRST(string ( <expression> )) | { string } |
| 587 | `<bool_return_expr>` → <bool_ret_assign> | FIRST(<bool_ret_assign>) | { !, (, ++, --, bool, false, id, true } |
| 588 | `<bool_ret_assign>` → <bool_ret_concat> <assign_tail> | FIRST(<bool_ret_concat> <assign_tail>) | { !, (, ++, --, bool, false, id, true } |
| 589 | `<bool_ret_concat>` → <bool_ret_or> <concat_tail> | FIRST(<bool_ret_or> <concat_tail>) | { !, (, ++, --, bool, false, id, true } |
| 590 | `<bool_ret_or>` → <bool_ret_and> <or_tail> | FIRST(<bool_ret_and> <or_tail>) | { !, (, ++, --, bool, false, id, true } |
| 591 | `<bool_ret_and>` → <bool_ret_eq> <and_tail> | FIRST(<bool_ret_eq> <and_tail>) | { !, (, ++, --, bool, false, id, true } |
| 592 | `<bool_ret_eq>` → <bool_ret_rel> <eq_tail> | FIRST(<bool_ret_rel> <eq_tail>) | { !, (, ++, --, bool, false, id, true } |
| 593 | `<bool_ret_rel>` → <bool_ret_add> <rel_tail> | FIRST(<bool_ret_add> <rel_tail>) | { !, (, ++, --, bool, false, id, true } |
| 594 | `<bool_ret_add>` → <bool_ret_mul> <add_tail> | FIRST(<bool_ret_mul> <add_tail>) | { !, (, ++, --, bool, false, id, true } |
| 595 | `<bool_ret_mul>` → <bool_ret_unary> <mul_tail> | FIRST(<bool_ret_unary> <mul_tail>) | { !, (, ++, --, bool, false, id, true } |
| 596 | `<bool_ret_unary>` → ! <bool_ret_unary> | FIRST(! <bool_ret_unary>) | { ! } |
| 597 | `<bool_ret_unary>` → <bool_ret_postfix> | FIRST(<bool_ret_postfix>) | { (, ++, --, bool, false, id, true } |
| 598 | `<bool_ret_postfix>` → true | FIRST(true) | { true } |
| 599 | `<bool_ret_postfix>` → false | FIRST(false) | { false } |
| 600 | `<bool_ret_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 601 | `<bool_ret_postfix>` → -- id | FIRST(-- id) | { -- } |
| 602 | `<bool_ret_postfix>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 603 | `<bool_ret_postfix>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 604 | `<bool_ret_postfix>` → bool ( <expression> ) | FIRST(bool ( <expression> )) | { bool } |
| 605 | `<using_cont>` → , id <using_cont> | FIRST(, id <using_cont>) | { , } |
| 606 | `<using_cont>` → λ | FIRST(λ) ∪ FOLLOW(<using_cont>) = { λ } ∪ { ; } | { ; } |
| 607 | `<local_dec_body>` → int id <int_local_tail> | FIRST(int id <int_local_tail>) | { int } |
| 608 | `<local_dec_body>` → long id <long_local_tail> | FIRST(long id <long_local_tail>) | { long } |
| 609 | `<local_dec_body>` → float id <float_local_tail> | FIRST(float id <float_local_tail>) | { float } |
| 610 | `<local_dec_body>` → double id <double_local_tail> | FIRST(double id <double_local_tail>) | { double } |
| 611 | `<local_dec_body>` → char id <char_local_tail> | FIRST(char id <char_local_tail>) | { char } |
| 612 | `<local_dec_body>` → string id <string_local_tail> | FIRST(string id <string_local_tail>) | { string } |
| 613 | `<local_dec_body>` → bool id <bool_local_tail> | FIRST(bool id <bool_local_tail>) | { bool } |
| 614 | `<local_dec_body>` → id id <weave_local_tail> | FIRST(id id <weave_local_tail>) | { id } |
| 615 | `<int_local_tail>` → <int_array_with_init> ; | FIRST(<int_array_with_init> ;) | { [ } |
| 616 | `<int_local_tail>` → = intlit <int_local_cont> ; | FIRST(= intlit <int_local_cont> ;) | { = } |
| 617 | `<int_local_cont>` → , id = intlit <int_local_cont> | FIRST(, id = intlit <int_local_cont>) | { , } |
| 618 | `<int_local_cont>` → λ | FIRST(λ) ∪ FOLLOW(<int_local_cont>) = { λ } ∪ { ; } | { ; } |
| 619 | `<long_local_tail>` → <long_array_with_init> ; | FIRST(<long_array_with_init> ;) | { [ } |
| 620 | `<long_local_tail>` → = longlit <long_local_cont> ; | FIRST(= longlit <long_local_cont> ;) | { = } |
| 621 | `<long_local_cont>` → , id = longlit <long_local_cont> | FIRST(, id = longlit <long_local_cont>) | { , } |
| 622 | `<long_local_cont>` → λ | FIRST(λ) ∪ FOLLOW(<long_local_cont>) = { λ } ∪ { ; } | { ; } |
| 623 | `<float_local_tail>` → <float_array_with_init> ; | FIRST(<float_array_with_init> ;) | { [ } |
| 624 | `<float_local_tail>` → = floatlit <float_local_cont> ; | FIRST(= floatlit <float_local_cont> ;) | { = } |
| 625 | `<float_local_cont>` → , id = floatlit <float_local_cont> | FIRST(, id = floatlit <float_local_cont>) | { , } |
| 626 | `<float_local_cont>` → λ | FIRST(λ) ∪ FOLLOW(<float_local_cont>) = { λ } ∪ { ; } | { ; } |
| 627 | `<double_local_tail>` → <double_array_with_init> ; | FIRST(<double_array_with_init> ;) | { [ } |
| 628 | `<double_local_tail>` → = doublelit <double_local_cont> ; | FIRST(= doublelit <double_local_cont> ;) | { = } |
| 629 | `<double_local_cont>` → , id = doublelit <double_local_cont> | FIRST(, id = doublelit <double_local_cont>) | { , } |
| 630 | `<double_local_cont>` → λ | FIRST(λ) ∪ FOLLOW(<double_local_cont>) = { λ } ∪ { ; } | { ; } |
| 631 | `<char_local_tail>` → <char_array_with_init> ; | FIRST(<char_array_with_init> ;) | { [ } |
| 632 | `<char_local_tail>` → = charlit <char_local_cont> ; | FIRST(= charlit <char_local_cont> ;) | { = } |
| 633 | `<char_local_cont>` → , id = charlit <char_local_cont> | FIRST(, id = charlit <char_local_cont>) | { , } |
| 634 | `<char_local_cont>` → λ | FIRST(λ) ∪ FOLLOW(<char_local_cont>) = { λ } ∪ { ; } | { ; } |
| 635 | `<string_local_tail>` → <string_array_with_init> ; | FIRST(<string_array_with_init> ;) | { [ } |
| 636 | `<string_local_tail>` → = stringlit <string_local_cont> ; | FIRST(= stringlit <string_local_cont> ;) | { = } |
| 637 | `<string_local_cont>` → , id = stringlit <string_local_cont> | FIRST(, id = stringlit <string_local_cont>) | { , } |
| 638 | `<string_local_cont>` → λ | FIRST(λ) ∪ FOLLOW(<string_local_cont>) = { λ } ∪ { ; } | { ; } |
| 639 | `<bool_local_tail>` → <bool_array_with_init> ; | FIRST(<bool_array_with_init> ;) | { [ } |
| 640 | `<bool_local_tail>` → = <bool_lit> <bool_local_cont> ; | FIRST(= <bool_lit> <bool_local_cont> ;) | { = } |
| 641 | `<bool_local_cont>` → , id = <bool_lit> <bool_local_cont> | FIRST(, id = <bool_lit> <bool_local_cont>) | { , } |
| 642 | `<bool_local_cont>` → λ | FIRST(λ) ∪ FOLLOW(<bool_local_cont>) = { λ } ∪ { ; } | { ; } |
| 643 | `<weave_local_tail>` → = { <weave_field_value> <weave_field_list_tail> } <weave_inst_cont> ; | FIRST(= { <weave_field_value> <weave_field_lis...) | { = } |
| 644 | `<weave_local_tail>` → <weave_array_with_init> <weave_arr_cont> ; | FIRST(<weave_array_with_init> <weave_arr_cont>...) | { [ } |
| 645 | `<statement_non_return>` → <effect_stmt> ; | FIRST(<effect_stmt> ;) | { ++, --, id } |
| 646 | `<statement_non_return>` → <io_stmt> | FIRST(<io_stmt>) | { thread, threadln, trap } |
| 647 | `<statement_non_return>` → <ctrl_struct> | FIRST(<ctrl_struct>) | { do, for, if, switch, while } |
| 648 | `<statement_non_return>` → break ; | FIRST(break ;) | { break } |
| 649 | `<ctrl_stmt_list>` → <statement_non_return> <ctrl_stmt_list> | FIRST(<statement_non_return> <ctrl_stmt_list>) | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 650 | `<ctrl_stmt_list>` → λ | FIRST(λ) ∪ FOLLOW(<ctrl_stmt_list>) = { λ } ∪ { break, case, default, } } | { break, case, default, } } |
| 651 | `<effect_stmt>` → ++ id <effect_pre_chain> | FIRST(++ id <effect_pre_chain>) | { ++ } |
| 652 | `<effect_stmt>` → -- id <effect_pre_chain> | FIRST(-- id <effect_pre_chain>) | { -- } |
| 653 | `<effect_stmt>` → id <effect_id_cont> | FIRST(id <effect_id_cont>) | { id } |
| 654 | `<effect_pre_chain>` → [ <stmt_array_index> ] <effect_pre_arr_chain> | FIRST([ <stmt_array_index> ] <effect_pre_arr_c...) | { [ } |
| 655 | `<effect_pre_chain>` → . id <effect_pre_chain> | FIRST(. id <effect_pre_chain>) | { . } |
| 656 | `<effect_pre_chain>` → λ | FIRST(λ) ∪ FOLLOW(<effect_pre_chain>) = { λ } ∪ { ; } | { ; } |
| 657 | `<effect_pre_arr_chain>` → [ <stmt_array_index> ] | FIRST([ <stmt_array_index> ]) | { [ } |
| 658 | `<effect_pre_arr_chain>` → . id <effect_pre_chain> | FIRST(. id <effect_pre_chain>) | { . } |
| 659 | `<effect_pre_arr_chain>` → λ | FIRST(λ) ∪ FOLLOW(<effect_pre_arr_chain>) = { λ } ∪ { ; } | { ; } |
| 660 | `<effect_id_cont>` → <assign_op> <stmt_assign_expr> | FIRST(<assign_op> <stmt_assign_expr>) | { %=, *=, +=, -=, /=, = } |
| 661 | `<effect_id_cont>` → ++ | FIRST(++) | { ++ } |
| 662 | `<effect_id_cont>` → -- | FIRST(--) | { -- } |
| 663 | `<effect_id_cont>` → ( <stmt_arg_list> ) <effect_post_call> | FIRST(( <stmt_arg_list> ) <effect_post_call>) | { ( } |
| 664 | `<effect_id_cont>` → [ <stmt_array_index> ] <effect_post_arr> | FIRST([ <stmt_array_index> ] <effect_post_arr>) | { [ } |
| 665 | `<effect_id_cont>` → . id <effect_post_member> | FIRST(. id <effect_post_member>) | { . } |
| 666 | `<effect_post_call>` → . id <effect_post_call_member> | FIRST(. id <effect_post_call_member>) | { . } |
| 667 | `<effect_post_call>` → [ <stmt_array_index> ] <effect_post_call_arr> | FIRST([ <stmt_array_index> ] <effect_post_call...) | { [ } |
| 668 | `<effect_post_call>` → λ | FIRST(λ) ∪ FOLLOW(<effect_post_call>) = { λ } ∪ { ; } | { ; } |
| 669 | `<effect_post_call_member>` → ( <stmt_arg_list> ) <effect_post_call> | FIRST(( <stmt_arg_list> ) <effect_post_call>) | { ( } |
| 670 | `<effect_post_call_member>` → [ <stmt_array_index> ] <effect_post_call_arr> | FIRST([ <stmt_array_index> ] <effect_post_call...) | { [ } |
| 671 | `<effect_post_call_member>` → . id <effect_post_call_member> | FIRST(. id <effect_post_call_member>) | { . } |
| 672 | `<effect_post_call_member>` → λ | FIRST(λ) ∪ FOLLOW(<effect_post_call_member>) = { λ } ∪ { ; } | { ; } |
| 673 | `<effect_post_call_arr>` → [ <stmt_array_index> ] <effect_post_call_arr_cont> | FIRST([ <stmt_array_index> ] <effect_post_call...) | { [ } |
| 674 | `<effect_post_call_arr>` → <effect_post_call_arr_cont> | FIRST(<effect_post_call_arr_con...) ∪ FOLLOW(<effect_post_call_arr>) | { (, ., ; } |
| 675 | `<effect_post_call_arr_cont>` → . id <effect_post_call_member> | FIRST(. id <effect_post_call_member>) | { . } |
| 676 | `<effect_post_call_arr_cont>` → ( <stmt_arg_list> ) <effect_post_call> | FIRST(( <stmt_arg_list> ) <effect_post_call>) | { ( } |
| 677 | `<effect_post_call_arr_cont>` → λ | FIRST(λ) ∪ FOLLOW(<effect_post_call_arr_cont>) = { λ } ∪ { ; } | { ; } |
| 678 | `<effect_post_arr>` → [ <stmt_array_index> ] <effect_post_arr_2d> | FIRST([ <stmt_array_index> ] <effect_post_arr_...) | { [ } |
| 679 | `<effect_post_arr>` → <effect_arr_effect> | FIRST(<effect_arr_effect>) | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 680 | `<effect_post_arr_2d>` → <effect_arr_effect> | FIRST(<effect_arr_effect>) | { %=, (, *=, ++, +=, --, -=, ., /=, = } |
| 681 | `<effect_arr_effect>` → <assign_op> <stmt_assign_expr> | FIRST(<assign_op> <stmt_assign_expr>) | { %=, *=, +=, -=, /=, = } |
| 682 | `<effect_arr_effect>` → ++ | FIRST(++) | { ++ } |
| 683 | `<effect_arr_effect>` → -- | FIRST(--) | { -- } |
| 684 | `<effect_arr_effect>` → ( <stmt_arg_list> ) <effect_post_call> | FIRST(( <stmt_arg_list> ) <effect_post_call>) | { ( } |
| 685 | `<effect_arr_effect>` → . id <effect_post_member> | FIRST(. id <effect_post_member>) | { . } |
| 686 | `<effect_post_member>` → <assign_op> <stmt_assign_expr> | FIRST(<assign_op> <stmt_assign_expr>) | { %=, *=, +=, -=, /=, = } |
| 687 | `<effect_post_member>` → ++ | FIRST(++) | { ++ } |
| 688 | `<effect_post_member>` → -- | FIRST(--) | { -- } |
| 689 | `<effect_post_member>` → ( <stmt_arg_list> ) <effect_post_call> | FIRST(( <stmt_arg_list> ) <effect_post_call>) | { ( } |
| 690 | `<effect_post_member>` → [ <stmt_array_index> ] <effect_post_arr> | FIRST([ <stmt_array_index> ] <effect_post_arr>) | { [ } |
| 691 | `<effect_post_member>` → . id <effect_post_member> | FIRST(. id <effect_post_member>) | { . } |
| 692 | `<stmt_assign_expr>` → <stmt_concat_expr> <stmt_assign_tail> | FIRST(<stmt_concat_expr> <stmt_assign_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 693 | `<stmt_assign_tail>` → <assign_op> <stmt_assign_expr> | FIRST(<assign_op> <stmt_assign_expr>) | { %=, *=, +=, -=, /=, = } |
| 694 | `<stmt_assign_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_assign_tail>) = { λ } ∪ { ; } | { ; } |
| 695 | `<stmt_concat_expr>` → <stmt_or_expr> <stmt_concat_tail> | FIRST(<stmt_or_expr> <stmt_concat_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 696 | `<stmt_concat_tail>` → .. <stmt_or_expr> <stmt_concat_tail> | FIRST(.. <stmt_or_expr> <stmt_concat_tail>) | { .. } |
| 697 | `<stmt_concat_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_concat_tail>) = { λ } ∪ { %=, *=, +=, -=, /=, ;, = } | { %=, *=, +=, -=, /=, ;, = } |
| 698 | `<stmt_or_expr>` → <stmt_and_expr> <stmt_or_tail> | FIRST(<stmt_and_expr> <stmt_or_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 699 | `<stmt_or_tail>` → \ | FIRST(\) | \ |
| 700 | `<stmt_or_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_or_tail>) = { λ } ∪ { %=, *=, +=, -=, .., /=, ;, = } | { %=, *=, +=, -=, .., /=, ;, = } |
| 701 | `<stmt_and_expr>` → <stmt_eq_expr> <stmt_and_tail> | FIRST(<stmt_eq_expr> <stmt_and_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 702 | `<stmt_and_tail>` → && <stmt_eq_expr> <stmt_and_tail> | FIRST(&& <stmt_eq_expr> <stmt_and_tail>) | { && } |
| 703 | `<stmt_and_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_and_tail>) = { λ } ∪ { %=, *=, +=, -=, .., /=, ;, =, \ | { %=, *=, +=, -=, .., /=, ;, =, \ |
| 704 | `<stmt_eq_expr>` → <stmt_rel_expr> <stmt_eq_tail> | FIRST(<stmt_rel_expr> <stmt_eq_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 705 | `<stmt_eq_tail>` → == <stmt_rel_expr> <stmt_eq_tail> | FIRST(== <stmt_rel_expr> <stmt_eq_tail>) | { == } |
| 706 | `<stmt_eq_tail>` → != <stmt_rel_expr> <stmt_eq_tail> | FIRST(!= <stmt_rel_expr> <stmt_eq_tail>) | { != } |
| 707 | `<stmt_eq_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_eq_tail>) = { λ } ∪ { %=, &&, *=, +=, -=, .., /=, ;, =, \ | { %=, &&, *=, +=, -=, .., /=, ;, =, \ |
| 708 | `<stmt_rel_expr>` → <stmt_add_expr> <stmt_rel_tail> | FIRST(<stmt_add_expr> <stmt_rel_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 709 | `<stmt_rel_tail>` → < <stmt_add_expr> | FIRST(< <stmt_add_expr>) | { < } |
| 710 | `<stmt_rel_tail>` → > <stmt_add_expr> | FIRST(> <stmt_add_expr>) | { > } |
| 711 | `<stmt_rel_tail>` → <= <stmt_add_expr> | FIRST(<= <stmt_add_expr>) | { <= } |
| 712 | `<stmt_rel_tail>` → >= <stmt_add_expr> | FIRST(>= <stmt_add_expr>) | { >= } |
| 713 | `<stmt_rel_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_rel_tail>) = { λ } ∪ { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \ | { !=, %=, &&, *=, +=, -=, .., /=, ;, =, ==, \ |
| 714 | `<stmt_add_expr>` → <stmt_mul_expr> <stmt_add_tail> | FIRST(<stmt_mul_expr> <stmt_add_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 715 | `<stmt_add_tail>` → + <stmt_mul_expr> <stmt_add_tail> | FIRST(+ <stmt_mul_expr> <stmt_add_tail>) | { + } |
| 716 | `<stmt_add_tail>` → - <stmt_mul_expr> <stmt_add_tail> | FIRST(- <stmt_mul_expr> <stmt_add_tail>) | { - } |
| 717 | `<stmt_add_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_add_tail>) = { λ } ∪ { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \ | { !=, %=, &&, *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \ |
| 718 | `<stmt_mul_expr>` → <stmt_unary_expr> <stmt_mul_tail> | FIRST(<stmt_unary_expr> <stmt_mul_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 719 | `<stmt_mul_tail>` → * <stmt_unary_expr> <stmt_mul_tail> | FIRST(* <stmt_unary_expr> <stmt_mul_tail>) | { * } |
| 720 | `<stmt_mul_tail>` → / <stmt_unary_expr> <stmt_mul_tail> | FIRST(/ <stmt_unary_expr> <stmt_mul_tail>) | { / } |
| 721 | `<stmt_mul_tail>` → % <stmt_unary_expr> <stmt_mul_tail> | FIRST(% <stmt_unary_expr> <stmt_mul_tail>) | { % } |
| 722 | `<stmt_mul_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_mul_tail>) = { λ } ∪ { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \ | { !=, %=, &&, *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \ |
| 723 | `<stmt_unary_expr>` → ! <stmt_unary_expr> | FIRST(! <stmt_unary_expr>) | { ! } |
| 724 | `<stmt_unary_expr>` → - <stmt_unary_expr> | FIRST(- <stmt_unary_expr>) | { - } |
| 725 | `<stmt_unary_expr>` → <stmt_postfix_expr> | FIRST(<stmt_postfix_expr>) | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 726 | `<stmt_postfix_expr>` → ( <arg_expr> ) <stmt_postfix_chain> | FIRST(( <arg_expr> ) <stmt_postfix_chain>) | { ( } |
| 727 | `<stmt_postfix_expr>` → int ( <arg_expr> ) | FIRST(int ( <arg_expr> )) | { int } |
| 728 | `<stmt_postfix_expr>` → long ( <arg_expr> ) | FIRST(long ( <arg_expr> )) | { long } |
| 729 | `<stmt_postfix_expr>` → float ( <arg_expr> ) | FIRST(float ( <arg_expr> )) | { float } |
| 730 | `<stmt_postfix_expr>` → double ( <arg_expr> ) | FIRST(double ( <arg_expr> )) | { double } |
| 731 | `<stmt_postfix_expr>` → char ( <arg_expr> ) | FIRST(char ( <arg_expr> )) | { char } |
| 732 | `<stmt_postfix_expr>` → string ( <arg_expr> ) | FIRST(string ( <arg_expr> )) | { string } |
| 733 | `<stmt_postfix_expr>` → bool ( <arg_expr> ) | FIRST(bool ( <arg_expr> )) | { bool } |
| 734 | `<stmt_postfix_expr>` → ++ id | FIRST(++ id) | { ++ } |
| 735 | `<stmt_postfix_expr>` → -- id | FIRST(-- id) | { -- } |
| 736 | `<stmt_postfix_expr>` → id <stmt_id_postfix> | FIRST(id <stmt_id_postfix>) | { id } |
| 737 | `<stmt_postfix_expr>` → intlit | FIRST(intlit) | { intlit } |
| 738 | `<stmt_postfix_expr>` → longlit | FIRST(longlit) | { longlit } |
| 739 | `<stmt_postfix_expr>` → floatlit | FIRST(floatlit) | { floatlit } |
| 740 | `<stmt_postfix_expr>` → doublelit | FIRST(doublelit) | { doublelit } |
| 741 | `<stmt_postfix_expr>` → charlit | FIRST(charlit) | { charlit } |
| 742 | `<stmt_postfix_expr>` → stringlit | FIRST(stringlit) | { stringlit } |
| 743 | `<stmt_postfix_expr>` → true | FIRST(true) | { true } |
| 744 | `<stmt_postfix_expr>` → false | FIRST(false) | { false } |
| 745 | `<stmt_id_postfix>` → ++ | FIRST(++) | { ++ } |
| 746 | `<stmt_id_postfix>` → -- | FIRST(--) | { -- } |
| 747 | `<stmt_id_postfix>` → <stmt_postfix_chain> | FIRST(<stmt_postfix_chain>) ∪ FOLLOW(<stmt_id_postfix>) | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, [, \ |
| 748 | `<stmt_postfix_chain>` → <stmt_array_access> <stmt_postfix_after_arr> | FIRST(<stmt_array_access> <stmt_postfix_after_...) | { [ } |
| 749 | `<stmt_postfix_chain>` → . id <stmt_postfix_chain> | FIRST(. id <stmt_postfix_chain>) | { . } |
| 750 | `<stmt_postfix_chain>` → ( <stmt_arg_list> ) <stmt_postfix_chain> | FIRST(( <stmt_arg_list> ) <stmt_postfix_chain>) | { ( } |
| 751 | `<stmt_postfix_chain>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_postfix_chain>) = { λ } ∪ { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 752 | `<stmt_array_access>` → [ <stmt_array_index> ] <stmt_array_access_dim2> | FIRST([ <stmt_array_index> ] <stmt_array_acces...) | { [ } |
| 753 | `<stmt_array_access_dim2>` → [ <stmt_array_index> ] | FIRST([ <stmt_array_index> ]) | { [ } |
| 754 | `<stmt_array_access_dim2>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_array_access_dim2>) = { λ } ∪ { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, (, *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 755 | `<stmt_postfix_after_arr>` → . id <stmt_postfix_chain> | FIRST(. id <stmt_postfix_chain>) | { . } |
| 756 | `<stmt_postfix_after_arr>` → ( <stmt_arg_list> ) <stmt_postfix_chain> | FIRST(( <stmt_arg_list> ) <stmt_postfix_chain>) | { ( } |
| 757 | `<stmt_postfix_after_arr>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_postfix_after_arr>) = { λ } ∪ { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 758 | `<stmt_array_index>` → intlit | FIRST(intlit) | { intlit } |
| 759 | `<stmt_array_index>` → id | FIRST(id) | { id } |
| 760 | `<stmt_arg_list>` → <arg_expr> <stmt_arg_tail> | FIRST(<arg_expr> <stmt_arg_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 761 | `<stmt_arg_list>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_arg_list>) = { λ } ∪ { ) } | { ) } |
| 762 | `<stmt_arg_tail>` → , <arg_expr> <stmt_arg_tail> | FIRST(, <arg_expr> <stmt_arg_tail>) | { , } |
| 763 | `<stmt_arg_tail>` → λ | FIRST(λ) ∪ FOLLOW(<stmt_arg_tail>) = { λ } ∪ { ) } | { ) } |
| 764 | `<arg_expr>` → <arg_assign_expr> | FIRST(<arg_assign_expr>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 765 | `<arg_assign_expr>` → <arg_concat_expr> <arg_assign_tail> | FIRST(<arg_concat_expr> <arg_assign_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 766 | `<arg_assign_tail>` → <assign_op> <arg_assign_expr> | FIRST(<assign_op> <arg_assign_expr>) | { %=, *=, +=, -=, /=, = } |
| 767 | `<arg_assign_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_assign_tail>) = { λ } ∪ { ), , } | { ), , } |
| 768 | `<arg_concat_expr>` → <arg_or_expr> <arg_concat_tail> | FIRST(<arg_or_expr> <arg_concat_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 769 | `<arg_concat_tail>` → .. <arg_or_expr> <arg_concat_tail> | FIRST(.. <arg_or_expr> <arg_concat_tail>) | { .. } |
| 770 | `<arg_concat_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_concat_tail>) = { λ } ∪ { %=, ), *=, +=, ,, -=, /=, = } | { %=, ), *=, +=, ,, -=, /=, = } |
| 771 | `<arg_or_expr>` → <arg_and_expr> <arg_or_tail> | FIRST(<arg_and_expr> <arg_or_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 772 | `<arg_or_tail>` → \ | FIRST(\) | \ |
| 773 | `<arg_or_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_or_tail>) = { λ } ∪ { %=, ), *=, +=, ,, -=, .., /=, = } | { %=, ), *=, +=, ,, -=, .., /=, = } |
| 774 | `<arg_and_expr>` → <arg_eq_expr> <arg_and_tail> | FIRST(<arg_eq_expr> <arg_and_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 775 | `<arg_and_tail>` → && <arg_eq_expr> <arg_and_tail> | FIRST(&& <arg_eq_expr> <arg_and_tail>) | { && } |
| 776 | `<arg_and_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_and_tail>) = { λ } ∪ { %=, ), *=, +=, ,, -=, .., /=, =, \ | { %=, ), *=, +=, ,, -=, .., /=, =, \ |
| 777 | `<arg_eq_expr>` → <arg_rel_expr> <arg_eq_tail> | FIRST(<arg_rel_expr> <arg_eq_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 778 | `<arg_eq_tail>` → == <arg_rel_expr> <arg_eq_tail> | FIRST(== <arg_rel_expr> <arg_eq_tail>) | { == } |
| 779 | `<arg_eq_tail>` → != <arg_rel_expr> <arg_eq_tail> | FIRST(!= <arg_rel_expr> <arg_eq_tail>) | { != } |
| 780 | `<arg_eq_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_eq_tail>) = { λ } ∪ { %=, &&, ), *=, +=, ,, -=, .., /=, =, \ | { %=, &&, ), *=, +=, ,, -=, .., /=, =, \ |
| 781 | `<arg_rel_expr>` → <arg_add_expr> <arg_rel_tail> | FIRST(<arg_add_expr> <arg_rel_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 782 | `<arg_rel_tail>` → < <arg_add_expr> | FIRST(< <arg_add_expr>) | { < } |
| 783 | `<arg_rel_tail>` → > <arg_add_expr> | FIRST(> <arg_add_expr>) | { > } |
| 784 | `<arg_rel_tail>` → <= <arg_add_expr> | FIRST(<= <arg_add_expr>) | { <= } |
| 785 | `<arg_rel_tail>` → >= <arg_add_expr> | FIRST(>= <arg_add_expr>) | { >= } |
| 786 | `<arg_rel_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_rel_tail>) = { λ } ∪ { !=, %=, &&, ), *=, +=, ,, -=, .., /=, =, ==, \ | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, =, ==, \ |
| 787 | `<arg_add_expr>` → <arg_mul_expr> <arg_add_tail> | FIRST(<arg_mul_expr> <arg_add_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 788 | `<arg_add_tail>` → + <arg_mul_expr> <arg_add_tail> | FIRST(+ <arg_mul_expr> <arg_add_tail>) | { + } |
| 789 | `<arg_add_tail>` → - <arg_mul_expr> <arg_add_tail> | FIRST(- <arg_mul_expr> <arg_add_tail>) | { - } |
| 790 | `<arg_add_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_add_tail>) = { λ } ∪ { !=, %=, &&, ), *=, +=, ,, -=, .., /=, ;, <, <=, =, ==, >, >=, \ | { !=, %=, &&, ), *=, +=, ,, -=, .., /=, ;, <, <=, =, ==, >, >=, \ |
| 791 | `<arg_mul_expr>` → <arg_unary_expr> <arg_mul_tail> | FIRST(<arg_unary_expr> <arg_mul_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 792 | `<arg_mul_tail>` → * <arg_unary_expr> <arg_mul_tail> | FIRST(* <arg_unary_expr> <arg_mul_tail>) | { * } |
| 793 | `<arg_mul_tail>` → / <arg_unary_expr> <arg_mul_tail> | FIRST(/ <arg_unary_expr> <arg_mul_tail>) | { / } |
| 794 | `<arg_mul_tail>` → % <arg_unary_expr> <arg_mul_tail> | FIRST(% <arg_unary_expr> <arg_mul_tail>) | { % } |
| 795 | `<arg_mul_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_mul_tail>) = { λ } ∪ { !=, %=, &&, ), *=, +, +=, ,, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \ | { !=, %=, &&, ), *=, +, +=, ,, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \ |
| 796 | `<arg_unary_expr>` → ! <arg_unary_expr> | FIRST(! <arg_unary_expr>) | { ! } |
| 797 | `<arg_unary_expr>` → - <arg_unary_expr> | FIRST(- <arg_unary_expr>) | { - } |
| 798 | `<arg_unary_expr>` → <arg_postfix_expr> | FIRST(<arg_postfix_expr>) | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 799 | `<arg_postfix_expr>` → ( <arg_expr> ) <arg_postfix_chain> | FIRST(( <arg_expr> ) <arg_postfix_chain>) | { ( } |
| 800 | `<arg_postfix_expr>` → int ( <arg_expr> ) | FIRST(int ( <arg_expr> )) | { int } |
| 801 | `<arg_postfix_expr>` → long ( <arg_expr> ) | FIRST(long ( <arg_expr> )) | { long } |
| 802 | `<arg_postfix_expr>` → float ( <arg_expr> ) | FIRST(float ( <arg_expr> )) | { float } |
| 803 | `<arg_postfix_expr>` → double ( <arg_expr> ) | FIRST(double ( <arg_expr> )) | { double } |
| 804 | `<arg_postfix_expr>` → char ( <arg_expr> ) | FIRST(char ( <arg_expr> )) | { char } |
| 805 | `<arg_postfix_expr>` → string ( <arg_expr> ) | FIRST(string ( <arg_expr> )) | { string } |
| 806 | `<arg_postfix_expr>` → bool ( <arg_expr> ) | FIRST(bool ( <arg_expr> )) | { bool } |
| 807 | `<arg_postfix_expr>` → ++ id | FIRST(++ id) | { ++ } |
| 808 | `<arg_postfix_expr>` → -- id | FIRST(-- id) | { -- } |
| 809 | `<arg_postfix_expr>` → id <arg_id_postfix> | FIRST(id <arg_id_postfix>) | { id } |
| 810 | `<arg_postfix_expr>` → intlit | FIRST(intlit) | { intlit } |
| 811 | `<arg_postfix_expr>` → longlit | FIRST(longlit) | { longlit } |
| 812 | `<arg_postfix_expr>` → floatlit | FIRST(floatlit) | { floatlit } |
| 813 | `<arg_postfix_expr>` → doublelit | FIRST(doublelit) | { doublelit } |
| 814 | `<arg_postfix_expr>` → charlit | FIRST(charlit) | { charlit } |
| 815 | `<arg_postfix_expr>` → stringlit | FIRST(stringlit) | { stringlit } |
| 816 | `<arg_postfix_expr>` → true | FIRST(true) | { true } |
| 817 | `<arg_postfix_expr>` → false | FIRST(false) | { false } |
| 818 | `<arg_id_postfix>` → ++ | FIRST(++) | { ++ } |
| 819 | `<arg_id_postfix>` → -- | FIRST(--) | { -- } |
| 820 | `<arg_id_postfix>` → <arg_postfix_chain> | FIRST(<arg_postfix_chain>) ∪ FOLLOW(<arg_id_postfix>) | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, [, \ |
| 821 | `<arg_postfix_chain>` → <arg_array_access> <arg_postfix_after_arr> | FIRST(<arg_array_access> <arg_postfix_after_ar...) | { [ } |
| 822 | `<arg_postfix_chain>` → . id <arg_postfix_chain> | FIRST(. id <arg_postfix_chain>) | { . } |
| 823 | `<arg_postfix_chain>` → ( <arg_nested_list> ) <arg_postfix_chain> | FIRST(( <arg_nested_list> ) <arg_postfix_chain...) | { ( } |
| 824 | `<arg_postfix_chain>` → λ | FIRST(λ) ∪ FOLLOW(<arg_postfix_chain>) = { λ } ∪ { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 825 | `<arg_array_access>` → [ <arg_array_index> ] <arg_array_access_dim2> | FIRST([ <arg_array_index> ] <arg_array_access_...) | { [ } |
| 826 | `<arg_array_access_dim2>` → [ <arg_array_index> ] | FIRST([ <arg_array_index> ]) | { [ } |
| 827 | `<arg_array_access_dim2>` → λ | FIRST(λ) ∪ FOLLOW(<arg_array_access_dim2>) = { λ } ∪ { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, (, ), *, *=, +, +=, ,, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 828 | `<arg_postfix_after_arr>` → . id <arg_postfix_chain> | FIRST(. id <arg_postfix_chain>) | { . } |
| 829 | `<arg_postfix_after_arr>` → ( <arg_nested_list> ) <arg_postfix_chain> | FIRST(( <arg_nested_list> ) <arg_postfix_chain...) | { ( } |
| 830 | `<arg_postfix_after_arr>` → λ | FIRST(λ) ∪ FOLLOW(<arg_postfix_after_arr>) = { λ } ∪ { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, ), *, *=, +, +=, ,, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 831 | `<arg_array_index>` → intlit | FIRST(intlit) | { intlit } |
| 832 | `<arg_array_index>` → id | FIRST(id) | { id } |
| 833 | `<arg_nested_list>` → <arg_expr> <arg_nested_tail> | FIRST(<arg_expr> <arg_nested_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 834 | `<arg_nested_list>` → λ | FIRST(λ) ∪ FOLLOW(<arg_nested_list>) = { λ } ∪ { ) } | { ) } |
| 835 | `<arg_nested_tail>` → , <arg_expr> <arg_nested_tail> | FIRST(, <arg_expr> <arg_nested_tail>) | { , } |
| 836 | `<arg_nested_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_nested_tail>) = { λ } ∪ { ) } | { ) } |
| 837 | `<expression>` → <assign_expr> | FIRST(<assign_expr>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 838 | `<assign_expr>` → <concat_expr> <assign_tail> | FIRST(<concat_expr> <assign_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 839 | `<assign_tail>` → <assign_op> <assign_expr> | FIRST(<assign_op> <assign_expr>) | { %=, *=, +=, -=, /=, = } |
| 840 | `<assign_tail>` → λ | FIRST(λ) ∪ FOLLOW(<assign_tail>) = { λ } ∪ { ), ; } | { ), ; } |
| 841 | `<assign_op>` → = | FIRST(=) | { = } |
| 842 | `<assign_op>` → += | FIRST(+=) | { += } |
| 843 | `<assign_op>` → -= | FIRST(-=) | { -= } |
| 844 | `<assign_op>` → *= | FIRST(*=) | { *= } |
| 845 | `<assign_op>` → /= | FIRST(/=) | { /= } |
| 846 | `<assign_op>` → %= | FIRST(%=) | { %= } |
| 847 | `<concat_expr>` → <or_expr> <concat_tail> | FIRST(<or_expr> <concat_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 848 | `<concat_tail>` → .. <or_expr> <concat_tail> | FIRST(.. <or_expr> <concat_tail>) | { .. } |
| 849 | `<concat_tail>` → λ | FIRST(λ) ∪ FOLLOW(<concat_tail>) = { λ } ∪ { %=, ), *=, +=, -=, /=, ;, = } | { %=, ), *=, +=, -=, /=, ;, = } |
| 850 | `<or_expr>` → <and_expr> <or_tail> | FIRST(<and_expr> <or_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 851 | `<or_tail>` → \ | FIRST(\) | \ |
| 852 | `<or_tail>` → λ | FIRST(λ) ∪ FOLLOW(<or_tail>) = { λ } ∪ { %=, ), *=, +=, -=, .., /=, ;, = } | { %=, ), *=, +=, -=, .., /=, ;, = } |
| 853 | `<and_expr>` → <eq_expr> <and_tail> | FIRST(<eq_expr> <and_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 854 | `<and_tail>` → && <eq_expr> <and_tail> | FIRST(&& <eq_expr> <and_tail>) | { && } |
| 855 | `<and_tail>` → λ | FIRST(λ) ∪ FOLLOW(<and_tail>) = { λ } ∪ { %=, ), *=, +=, -=, .., /=, ;, =, \ | { %=, ), *=, +=, -=, .., /=, ;, =, \ |
| 856 | `<eq_expr>` → <rel_expr> <eq_tail> | FIRST(<rel_expr> <eq_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 857 | `<eq_tail>` → == <rel_expr> <eq_tail> | FIRST(== <rel_expr> <eq_tail>) | { == } |
| 858 | `<eq_tail>` → != <rel_expr> <eq_tail> | FIRST(!= <rel_expr> <eq_tail>) | { != } |
| 859 | `<eq_tail>` → λ | FIRST(λ) ∪ FOLLOW(<eq_tail>) = { λ } ∪ { %=, &&, ), *=, +=, -=, .., /=, ;, =, \ | { %=, &&, ), *=, +=, -=, .., /=, ;, =, \ |
| 860 | `<rel_expr>` → <add_expr> <rel_tail> | FIRST(<add_expr> <rel_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 861 | `<rel_tail>` → < <add_expr> | FIRST(< <add_expr>) | { < } |
| 862 | `<rel_tail>` → > <add_expr> | FIRST(> <add_expr>) | { > } |
| 863 | `<rel_tail>` → <= <add_expr> | FIRST(<= <add_expr>) | { <= } |
| 864 | `<rel_tail>` → >= <add_expr> | FIRST(>= <add_expr>) | { >= } |
| 865 | `<rel_tail>` → λ | FIRST(λ) ∪ FOLLOW(<rel_tail>) = { λ } ∪ { !=, %=, &&, ), *=, +=, -=, .., /=, ;, =, ==, \ | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, =, ==, \ |
| 866 | `<add_expr>` → <mul_expr> <add_tail> | FIRST(<mul_expr> <add_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 867 | `<add_tail>` → + <mul_expr> <add_tail> | FIRST(+ <mul_expr> <add_tail>) | { + } |
| 868 | `<add_tail>` → - <mul_expr> <add_tail> | FIRST(- <mul_expr> <add_tail>) | { - } |
| 869 | `<add_tail>` → λ | FIRST(λ) ∪ FOLLOW(<add_tail>) = { λ } ∪ { !=, %=, &&, ), *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \ | { !=, %=, &&, ), *=, +=, -=, .., /=, ;, <, <=, =, ==, >, >=, \ |
| 870 | `<mul_expr>` → <unary_expr> <mul_tail> | FIRST(<unary_expr> <mul_tail>) | { !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 871 | `<mul_tail>` → * <unary_expr> <mul_tail> | FIRST(* <unary_expr> <mul_tail>) | { * } |
| 872 | `<mul_tail>` → / <unary_expr> <mul_tail> | FIRST(/ <unary_expr> <mul_tail>) | { / } |
| 873 | `<mul_tail>` → % <unary_expr> <mul_tail> | FIRST(% <unary_expr> <mul_tail>) | { % } |
| 874 | `<mul_tail>` → λ | FIRST(λ) ∪ FOLLOW(<mul_tail>) = { λ } ∪ { !=, %=, &&, ), *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \ | { !=, %=, &&, ), *=, +, +=, -, -=, .., /=, ;, <, <=, =, ==, >, >=, \ |
| 875 | `<unary_expr>` → ! <unary_expr> | FIRST(! <unary_expr>) | { ! } |
| 876 | `<unary_expr>` → <postfix_expr> | FIRST(<postfix_expr>) | { (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 877 | `<postfix_expr>` → ( <expression> ) <postfix_chain> | FIRST(( <expression> ) <postfix_chain>) | { ( } |
| 878 | `<postfix_expr>` → int ( <expression> ) | FIRST(int ( <expression> )) | { int } |
| 879 | `<postfix_expr>` → long ( <expression> ) | FIRST(long ( <expression> )) | { long } |
| 880 | `<postfix_expr>` → float ( <expression> ) | FIRST(float ( <expression> )) | { float } |
| 881 | `<postfix_expr>` → double ( <expression> ) | FIRST(double ( <expression> )) | { double } |
| 882 | `<postfix_expr>` → char ( <expression> ) | FIRST(char ( <expression> )) | { char } |
| 883 | `<postfix_expr>` → string ( <expression> ) | FIRST(string ( <expression> )) | { string } |
| 884 | `<postfix_expr>` → bool ( <expression> ) | FIRST(bool ( <expression> )) | { bool } |
| 885 | `<postfix_expr>` → ++ id | FIRST(++ id) | { ++ } |
| 886 | `<postfix_expr>` → -- id | FIRST(-- id) | { -- } |
| 887 | `<postfix_expr>` → id <id_postfix> | FIRST(id <id_postfix>) | { id } |
| 888 | `<postfix_expr>` → intlit | FIRST(intlit) | { intlit } |
| 889 | `<postfix_expr>` → longlit | FIRST(longlit) | { longlit } |
| 890 | `<postfix_expr>` → floatlit | FIRST(floatlit) | { floatlit } |
| 891 | `<postfix_expr>` → doublelit | FIRST(doublelit) | { doublelit } |
| 892 | `<postfix_expr>` → charlit | FIRST(charlit) | { charlit } |
| 893 | `<postfix_expr>` → stringlit | FIRST(stringlit) | { stringlit } |
| 894 | `<postfix_expr>` → true | FIRST(true) | { true } |
| 895 | `<postfix_expr>` → false | FIRST(false) | { false } |
| 896 | `<id_postfix>` → ++ | FIRST(++) | { ++ } |
| 897 | `<id_postfix>` → -- | FIRST(--) | { -- } |
| 898 | `<id_postfix>` → <postfix_chain> | FIRST(<postfix_chain>) ∪ FOLLOW(<id_postfix>) | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, [, \ |
| 899 | `<postfix_chain>` → <array_access> <postfix_after_arr> | FIRST(<array_access> <postfix_after_arr>) | { [ } |
| 900 | `<postfix_chain>` → . id <postfix_chain> | FIRST(. id <postfix_chain>) | { . } |
| 901 | `<postfix_chain>` → ( <arg_list> ) <postfix_chain> | FIRST(( <arg_list> ) <postfix_chain>) | { ( } |
| 902 | `<postfix_chain>` → λ | FIRST(λ) ∪ FOLLOW(<postfix_chain>) = { λ } ∪ { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 903 | `<array_access>` → [ <array_index> ] <array_access_dim2> | FIRST([ <array_index> ] <array_access_dim2>) | { [ } |
| 904 | `<array_access_dim2>` → [ <array_index> ] | FIRST([ <array_index> ]) | { [ } |
| 905 | `<array_access_dim2>` → λ | FIRST(λ) ∪ FOLLOW(<array_access_dim2>) = { λ } ∪ { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, (, ), *, *=, +, +=, -, -=, ., .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 906 | `<postfix_after_arr>` → . id <postfix_chain> | FIRST(. id <postfix_chain>) | { . } |
| 907 | `<postfix_after_arr>` → ( <arg_list> ) <postfix_chain> | FIRST(( <arg_list> ) <postfix_chain>) | { ( } |
| 908 | `<postfix_after_arr>` → λ | FIRST(λ) ∪ FOLLOW(<postfix_after_arr>) = { λ } ∪ { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ | { !=, %, %=, &&, ), *, *=, +, +=, -, -=, .., /, /=, ;, <, <=, =, ==, >, >=, \ |
| 909 | `<array_index>` → intlit | FIRST(intlit) | { intlit } |
| 910 | `<array_index>` → id | FIRST(id) | { id } |
| 911 | `<arg_list>` → <arg_expr> <arg_tail> | FIRST(<arg_expr> <arg_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 912 | `<arg_list>` → λ | FIRST(λ) ∪ FOLLOW(<arg_list>) = { λ } ∪ { ) } | { ) } |
| 913 | `<arg_tail>` → , <arg_expr> <arg_tail> | FIRST(, <arg_expr> <arg_tail>) | { , } |
| 914 | `<arg_tail>` → λ | FIRST(λ) ∪ FOLLOW(<arg_tail>) = { λ } ∪ { ) } | { ) } |
| 915 | `<io_stmt>` → trap ( <arg_expr> ) ; | FIRST(trap ( <arg_expr> ) ;) | { trap } |
| 916 | `<io_stmt>` → thread ( <print_args> ) ; | FIRST(thread ( <print_args> ) ;) | { thread } |
| 917 | `<io_stmt>` → threadln ( <print_args> ) ; | FIRST(threadln ( <print_args> ) ;) | { threadln } |
| 918 | `<print_args>` → <arg_expr> <print_tail> | FIRST(<arg_expr> <print_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 919 | `<print_tail>` → , <arg_expr> <print_tail> | FIRST(, <arg_expr> <print_tail>) | { , } |
| 920 | `<print_tail>` → λ | FIRST(λ) ∪ FOLLOW(<print_tail>) = { λ } ∪ { ) } | { ) } |
| 921 | `<ctrl_struct>` → if ( <condition> ) { <ctrl_stmt_list> } <else_opt> | FIRST(if ( <condition> ) { <ctrl_stmt_list> } ...) | { if } |
| 922 | `<ctrl_struct>` → switch ( <arg_expr> ) { <case_list> <default_opt> } | FIRST(switch ( <arg_expr> ) { <case_list> <def...) | { switch } |
| 923 | `<ctrl_struct>` → for ( <for_init> ; <for_cond> ; <for_update> ) { <ctrl_stmt_list> } | FIRST(for ( <for_init> ; <for_cond> ; <for_upd...) | { for } |
| 924 | `<ctrl_struct>` → while ( <condition> ) { <ctrl_stmt_list> } | FIRST(while ( <condition> ) { <ctrl_stmt_list>...) | { while } |
| 925 | `<ctrl_struct>` → do { <ctrl_stmt_list> } while ( <condition> ) ; | FIRST(do { <ctrl_stmt_list> } while ( <conditi...) | { do } |
| 926 | `<else_opt>` → else <else_body> | FIRST(else <else_body>) | { else } |
| 927 | `<else_opt>` → λ | FIRST(λ) ∪ FOLLOW(<else_opt>) = { λ } ∪ { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } | { ++, --, break, case, default, do, for, id, if, local, return, switch, thread, threadln, trap, using, while, } } |
| 928 | `<else_body>` → { <ctrl_stmt_list> } | FIRST({ <ctrl_stmt_list> }) | { { } |
| 929 | `<else_body>` → if ( <condition> ) { <ctrl_stmt_list> } <else_opt> | FIRST(if ( <condition> ) { <ctrl_stmt_list> } ...) | { if } |
| 930 | `<case_list>` → case <case_val> : <ctrl_stmt_list> <break_opt> <case_list> | FIRST(case <case_val> : <ctrl_stmt_list> <brea...) | { case } |
| 931 | `<case_list>` → λ | FIRST(λ) ∪ FOLLOW(<case_list>) = { λ } ∪ { default, } } | { default, } } |
| 932 | `<case_val>` → intlit | FIRST(intlit) | { intlit } |
| 933 | `<case_val>` → longlit | FIRST(longlit) | { longlit } |
| 934 | `<case_val>` → charlit | FIRST(charlit) | { charlit } |
| 935 | `<case_val>` → true | FIRST(true) | { true } |
| 936 | `<case_val>` → false | FIRST(false) | { false } |
| 937 | `<default_opt>` → default : <ctrl_stmt_list> <break_opt> | FIRST(default : <ctrl_stmt_list> <break_opt>) | { default } |
| 938 | `<default_opt>` → λ | FIRST(λ) ∪ FOLLOW(<default_opt>) = { λ } ∪ { } } | { } } |
| 939 | `<break_opt>` → break ; | FIRST(break ;) | { break } |
| 940 | `<break_opt>` → λ | FIRST(λ) ∪ FOLLOW(<break_opt>) = { λ } ∪ { case, default, } } | { case, default, } } |
| 941 | `<for_init>` → local var <for_init_type> id = <for_init_expr> | FIRST(local var <for_init_type> id = <for_init...) | { local } |
| 942 | `<for_init>` → id <for_init_assign_tail> | FIRST(id <for_init_assign_tail>) | { id } |
| 943 | `<for_init>` → λ | FIRST(λ) ∪ FOLLOW(<for_init>) = { λ } ∪ { ; } | { ; } |
| 944 | `<for_init_assign_tail>` → <assign_op> <for_init_expr> | FIRST(<assign_op> <for_init_expr>) | { %=, *=, +=, -=, /=, = } |
| 945 | `<for_init_expr>` → <stmt_concat_expr> | FIRST(<stmt_concat_expr>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 946 | `<for_init_type>` → int | FIRST(int) | { int } |
| 947 | `<for_init_type>` → long | FIRST(long) | { long } |
| 948 | `<for_init_type>` → float | FIRST(float) | { float } |
| 949 | `<for_init_type>` → double | FIRST(double) | { double } |
| 950 | `<for_init_type>` → char | FIRST(char) | { char } |
| 951 | `<for_init_type>` → string | FIRST(string) | { string } |
| 952 | `<for_init_type>` → bool | FIRST(bool) | { bool } |
| 953 | `<for_cond>` → <condition> | FIRST(<condition>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 954 | `<for_update>` → id <for_update_tail> | FIRST(id <for_update_tail>) | { id } |
| 955 | `<for_update>` → ++ id | FIRST(++ id) | { ++ } |
| 956 | `<for_update>` → -- id | FIRST(-- id) | { -- } |
| 957 | `<for_update>` → λ | FIRST(λ) ∪ FOLLOW(<for_update>) = { λ } ∪ { ) } | { ) } |
| 958 | `<for_update_tail>` → ++ | FIRST(++) | { ++ } |
| 959 | `<for_update_tail>` → -- | FIRST(--) | { -- } |
| 960 | `<for_update_tail>` → <assign_op> <arg_expr> | FIRST(<assign_op> <arg_expr>) | { %=, *=, +=, -=, /=, = } |
| 961 | `<condition>` → <cond_or> | FIRST(<cond_or>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 962 | `<cond_or>` → <cond_and> <cond_or_tail> | FIRST(<cond_and> <cond_or_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 963 | `<cond_or_tail>` → \ | FIRST(\) | \ |
| 964 | `<cond_or_tail>` → λ | FIRST(λ) ∪ FOLLOW(<cond_or_tail>) = { λ } ∪ { ), ; } | { ), ; } |
| 965 | `<cond_and>` → <cond_comparison> <cond_and_tail> | FIRST(<cond_comparison> <cond_and_tail>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 966 | `<cond_and_tail>` → && <cond_comparison> <cond_and_tail> | FIRST(&& <cond_comparison> <cond_and_tail>) | { && } |
| 967 | `<cond_and_tail>` → λ | FIRST(λ) ∪ FOLLOW(<cond_and_tail>) = { λ } ∪ { ), ;, \ | { ), ;, \ |
| 968 | `<cond_comparison>` → ( <condition> ) | FIRST(( <condition> )) | { ( } |
| 969 | `<cond_comparison>` → ! <cond_comparison> | FIRST(! <cond_comparison>) | { ! } |
| 970 | `<cond_comparison>` → <cond_primary> <cond_primary_continue> | FIRST(<cond_primary> <cond_primary_continue>) | { ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 971 | `<cond_primary>` → - <cond_primary> | FIRST(- <cond_primary>) | { - } |
| 972 | `<cond_primary>` → <cond_postfix> | FIRST(<cond_postfix>) | { ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 973 | `<cond_primary_continue>` → + <cond_primary> <cond_must_commit> | FIRST(+ <cond_primary> <cond_must_commit>) | { + } |
| 974 | `<cond_primary_continue>` → - <cond_primary> <cond_must_commit> | FIRST(- <cond_primary> <cond_must_commit>) | { - } |
| 975 | `<cond_primary_continue>` → * <cond_primary> <cond_must_commit> | FIRST(* <cond_primary> <cond_must_commit>) | { * } |
| 976 | `<cond_primary_continue>` → / <cond_primary> <cond_must_commit> | FIRST(/ <cond_primary> <cond_must_commit>) | { / } |
| 977 | `<cond_primary_continue>` → % <cond_primary> <cond_must_commit> | FIRST(% <cond_primary> <cond_must_commit>) | { % } |
| 978 | `<cond_primary_continue>` → <comp_op> <cond_rhs> | FIRST(<comp_op> <cond_rhs>) | { !=, <, <=, ==, >, >= } |
| 979 | `<cond_primary_continue>` → λ | FIRST(λ) ∪ FOLLOW(<cond_primary_continue>) = { λ } ∪ { &&, ), ;, \ | { &&, ), ;, \ |
| 980 | `<cond_must_commit>` → + <cond_primary> <cond_must_commit> | FIRST(+ <cond_primary> <cond_must_commit>) | { + } |
| 981 | `<cond_must_commit>` → - <cond_primary> <cond_must_commit> | FIRST(- <cond_primary> <cond_must_commit>) | { - } |
| 982 | `<cond_must_commit>` → * <cond_primary> <cond_must_commit> | FIRST(* <cond_primary> <cond_must_commit>) | { * } |
| 983 | `<cond_must_commit>` → / <cond_primary> <cond_must_commit> | FIRST(/ <cond_primary> <cond_must_commit>) | { / } |
| 984 | `<cond_must_commit>` → % <cond_primary> <cond_must_commit> | FIRST(% <cond_primary> <cond_must_commit>) | { % } |
| 985 | `<cond_must_commit>` → <comp_op> <cond_rhs> | FIRST(<comp_op> <cond_rhs>) | { !=, <, <=, ==, >, >= } |
| 986 | `<cond_postfix>` → int ( <cond_cast_arg> ) | FIRST(int ( <cond_cast_arg> )) | { int } |
| 987 | `<cond_postfix>` → long ( <cond_cast_arg> ) | FIRST(long ( <cond_cast_arg> )) | { long } |
| 988 | `<cond_postfix>` → float ( <cond_cast_arg> ) | FIRST(float ( <cond_cast_arg> )) | { float } |
| 989 | `<cond_postfix>` → double ( <cond_cast_arg> ) | FIRST(double ( <cond_cast_arg> )) | { double } |
| 990 | `<cond_postfix>` → char ( <cond_cast_arg> ) | FIRST(char ( <cond_cast_arg> )) | { char } |
| 991 | `<cond_postfix>` → string ( <cond_cast_arg> ) | FIRST(string ( <cond_cast_arg> )) | { string } |
| 992 | `<cond_postfix>` → bool ( <cond_cast_arg> ) | FIRST(bool ( <cond_cast_arg> )) | { bool } |
| 993 | `<cond_postfix>` → ++ id | FIRST(++ id) | { ++ } |
| 994 | `<cond_postfix>` → -- id | FIRST(-- id) | { -- } |
| 995 | `<cond_postfix>` → id <cond_id_post> | FIRST(id <cond_id_post>) | { id } |
| 996 | `<cond_postfix>` → intlit | FIRST(intlit) | { intlit } |
| 997 | `<cond_postfix>` → longlit | FIRST(longlit) | { longlit } |
| 998 | `<cond_postfix>` → floatlit | FIRST(floatlit) | { floatlit } |
| 999 | `<cond_postfix>` → doublelit | FIRST(doublelit) | { doublelit } |
| 1000 | `<cond_postfix>` → charlit | FIRST(charlit) | { charlit } |
| 1001 | `<cond_postfix>` → stringlit | FIRST(stringlit) | { stringlit } |
| 1002 | `<cond_postfix>` → true | FIRST(true) | { true } |
| 1003 | `<cond_postfix>` → false | FIRST(false) | { false } |
| 1004 | `<cond_cast_arg>` → <arg_expr> | FIRST(<arg_expr>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1005 | `<cond_id_post>` → ++ | FIRST(++) | { ++ } |
| 1006 | `<cond_id_post>` → -- | FIRST(--) | { -- } |
| 1007 | `<cond_id_post>` → <cond_post_chain> | FIRST(<cond_post_chain>) ∪ FOLLOW(<cond_id_post>) | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, [, \ |
| 1008 | `<cond_post_chain>` → <cond_arr_access> <cond_post_after_arr> | FIRST(<cond_arr_access> <cond_post_after_arr>) | { [ } |
| 1009 | `<cond_post_chain>` → . id <cond_post_chain> | FIRST(. id <cond_post_chain>) | { . } |
| 1010 | `<cond_post_chain>` → ( <arg_list> ) <cond_post_chain> | FIRST(( <arg_list> ) <cond_post_chain>) | { ( } |
| 1011 | `<cond_post_chain>` → λ | FIRST(λ) ∪ FOLLOW(<cond_post_chain>) = { λ } ∪ { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \ | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \ |
| 1012 | `<cond_arr_access>` → [ <cond_arr_index> ] <cond_arr_access_dim2> | FIRST([ <cond_arr_index> ] <cond_arr_access_di...) | { [ } |
| 1013 | `<cond_arr_access_dim2>` → [ <cond_arr_index> ] | FIRST([ <cond_arr_index> ]) | { [ } |
| 1014 | `<cond_arr_access_dim2>` → λ | FIRST(λ) ∪ FOLLOW(<cond_arr_access_dim2>) = { λ } ∪ { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, \ | { !=, %, &&, (, ), *, +, -, ., /, ;, <, <=, ==, >, >=, \ |
| 1015 | `<cond_post_after_arr>` → . id <cond_post_chain> | FIRST(. id <cond_post_chain>) | { . } |
| 1016 | `<cond_post_after_arr>` → ( <arg_list> ) <cond_post_chain> | FIRST(( <arg_list> ) <cond_post_chain>) | { ( } |
| 1017 | `<cond_post_after_arr>` → λ | FIRST(λ) ∪ FOLLOW(<cond_post_after_arr>) = { λ } ∪ { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \ | { !=, %, &&, ), *, +, -, /, ;, <, <=, ==, >, >=, \ |
| 1018 | `<cond_arr_index>` → intlit | FIRST(intlit) | { intlit } |
| 1019 | `<cond_arr_index>` → id | FIRST(id) | { id } |
| 1020 | `<cond_rhs>` → <arg_add_expr> | FIRST(<arg_add_expr>) | { !, (, ++, -, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true } |
| 1021 | `<comp_op>` → == | FIRST(==) | { == } |
| 1022 | `<comp_op>` → != | FIRST(!=) | { != } |
| 1023 | `<comp_op>` → < | FIRST(<) | { < } |
| 1024 | `<comp_op>` → > | FIRST(>) | { > } |
| 1025 | `<comp_op>` → <= | FIRST(<=) | { <= } |
| 1026 | `<comp_op>` → >= | FIRST(>=) | { >= } |
| 1027 | `<main_body>` → <main_content> | FIRST(<main_content>) | { ++, --, break, do, for, id, if, local, return, switch, thread, threadln, trap, using, while } |
| 1028 | `<main_content>` → using id <using_cont> ; <main_content> | FIRST(using id <using_cont> ; <main_content>) | { using } |
| 1029 | `<main_content>` → local <mutability> <local_dec_body> <main_content> | FIRST(local <mutability> <local_dec_body> <mai...) | { local } |
| 1030 | `<main_content>` → <statement_non_return> <main_content> | FIRST(<statement_non_return> <main_content>) | { ++, --, break, do, for, id, if, switch, thread, threadln, trap, while } |
| 1031 | `<main_content>` → return intlit ; | FIRST(return intlit ;) | { return } |