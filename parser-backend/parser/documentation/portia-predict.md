## PREDICT Set

| # | Production | Calculation | Predict Set |
|---|------------|-------------|-------------|
| 1 | `<program> → <decl_list>` | `First(<decl_list>)` | `{ bool, char, double, float, func, global, id, int, long, string, weave }` |
| 2 | `<decl_list> → int <int_decl_or_main>` | `First(int)` | `{ int }` |
| 3 | `<decl_list> → <other_decl> <decl_list>` | `First(<other_decl>)` | `{ bool, char, double, float, func, global, id, long, string, weave }` |
| 4 | `<int_decl_or_main> → id <typed_decl_tail> <decl_list>` | `First(id)` | `{ id }` |
| 5 | `<int_decl_or_main> → main ( ) { <main_body> } $END` | `First(main)` | `{ main }` |
| 6 | `<other_decl> → global <mutability> <dtype> id = <expression> <multi_global> ;` | `First(global)` | `{ global }` |
| 7 | `<other_decl> → long id <typed_decl_tail>` | `First(long)` | `{ long }` |
| 8 | `<other_decl> → float id <typed_decl_tail>` | `First(float)` | `{ float }` |
| 9 | `<other_decl> → double id <typed_decl_tail>` | `First(double)` | `{ double }` |
| 10 | `<other_decl> → char id <typed_decl_tail>` | `First(char)` | `{ char }` |
| 11 | `<other_decl> → string id <typed_decl_tail>` | `First(string)` | `{ string }` |
| 12 | `<other_decl> → bool id <typed_decl_tail>` | `First(bool)` | `{ bool }` |
| 13 | `<other_decl> → weave id { <field_list> } ;` | `First(weave)` | `{ weave }` |
| 14 | `<other_decl> → id <weave_inst_decl>` | `First(id)` | `{ id }` |
| 15 | `<other_decl> → func <nonvoid_ret_type> id ( <param_list> ) { <function_body_nonvoid> }` | `First(func)` | `{ func }` |
| 16 | `<other_decl> → func void id ( <param_list> ) { <function_body_void> }` | `First(func)` | `{ func }` |
| 17 | `<main_func> → int main ( ) { <main_body> }` | `First(int)` | `{ int }` |
| 18 | `<multi_global> → , id = <expression> <multi_global>` | `First(,)` | `{ , }` |
| 19 | `<multi_global> → λ` | `First(λ) ∪ Follow(<multi_global>)` | `{ ; }` |
| 20 | `<weave_inst_decl> → id <weave_inst_tail> <weave_inst_cont> ;` | `First(id)` | `{ id }` |
| 21 | `<weave_inst_decl> → <array_with_init> <weave_arr_cont> ;` | `First(<array_with_init>)` | `{ [ }` |
| 22 | `<weave_inst_tail> → = { <weave_field_value> <weave_field_list_tail> }` | `First(=)` | `{ = }` |
| 23 | `<weave_inst_tail> → <array_with_init>` | `First(<array_with_init>)` | `{ [ }` |
| 24 | `<weave_field_value> → intlit` | `First(intlit)` | `{ intlit }` |
| 25 | `<weave_field_value> → longlit` | `First(longlit)` | `{ longlit }` |
| 26 | `<weave_field_value> → floatlit` | `First(floatlit)` | `{ floatlit }` |
| 27 | `<weave_field_value> → doublelit` | `First(doublelit)` | `{ doublelit }` |
| 28 | `<weave_field_value> → charlit` | `First(charlit)` | `{ charlit }` |
| 29 | `<weave_field_value> → stringlit` | `First(stringlit)` | `{ stringlit }` |
| 30 | `<weave_field_value> → true` | `First(true)` | `{ true }` |
| 31 | `<weave_field_value> → false` | `First(false)` | `{ false }` |
| 32 | `<weave_field_value> → { <weave_arr_content> }` | `First({)` | `{ { }` |
| 33 | `<weave_arr_content> → { <elem_list> } <elem_2d_tail>` | `First({)` | `{ { }` |
| 34 | `<weave_arr_content> → <arr_elem> <elem_1d_tail>` | `First(<arr_elem>)` | `{ bool, char, charlit, double, doublelit, false, float, floatlit, int, intlit, long, longlit, string, stringlit, true }` |
| 35 | `<weave_arr_content> → λ` | `First(λ) ∪ Follow(<weave_arr_content>)` | `{ } }` |
| 36 | `<weave_field_list_tail> → , <weave_field_value> <weave_field_list_tail>` | `First(,)` | `{ , }` |
| 37 | `<weave_field_list_tail> → λ` | `First(λ) ∪ Follow(<weave_field_list_tail>)` | `{ } }` |
| 38 | `<weave_inst_cont> → , id <weave_inst_tail> <weave_inst_cont>` | `First(,)` | `{ , }` |
| 39 | `<weave_inst_cont> → λ` | `First(λ) ∪ Follow(<weave_inst_cont>)` | `{ ; }` |
| 40 | `<weave_arr_cont> → , id <array_with_init> <weave_arr_cont>` | `First(,)` | `{ , }` |
| 41 | `<weave_arr_cont> → λ` | `First(λ) ∪ Follow(<weave_arr_cont>)` | `{ ; }` |
| 42 | `<typed_decl_tail> → <array_with_init> ;` | `First(<array_with_init>)` | `{ [ }` |
| 43 | `<typed_decl_tail> → = <expression> <multi_typed> ;` | `First(=)` | `{ = }` |
| 44 | `<multi_typed> → , id = <expression> <multi_typed>` | `First(,)` | `{ , }` |
| 45 | `<multi_typed> → λ` | `First(λ) ∪ Follow(<multi_typed>)` | `{ ; }` |
| 46 | `<mutability> → var` | `First(var)` | `{ var }` |
| 47 | `<mutability> → const` | `First(const)` | `{ const }` |
| 48 | `<dtype> → int` | `First(int)` | `{ int }` |
| 49 | `<dtype> → long` | `First(long)` | `{ long }` |
| 50 | `<dtype> → float` | `First(float)` | `{ float }` |
| 51 | `<dtype> → double` | `First(double)` | `{ double }` |
| 52 | `<dtype> → char` | `First(char)` | `{ char }` |
| 53 | `<dtype> → string` | `First(string)` | `{ string }` |
| 54 | `<dtype> → bool` | `First(bool)` | `{ bool }` |
| 55 | `<value> → intlit` | `First(intlit)` | `{ intlit }` |
| 56 | `<value> → longlit` | `First(longlit)` | `{ longlit }` |
| 57 | `<value> → floatlit` | `First(floatlit)` | `{ floatlit }` |
| 58 | `<value> → doublelit` | `First(doublelit)` | `{ doublelit }` |
| 59 | `<value> → charlit` | `First(charlit)` | `{ charlit }` |
| 60 | `<value> → stringlit` | `First(stringlit)` | `{ stringlit }` |
| 61 | `<value> → true` | `First(true)` | `{ true }` |
| 62 | `<value> → false` | `First(false)` | `{ false }` |
| 63 | `<value_list_tail> → , <value> <value_list_tail>` | `First(,)` | `{ , }` |
| 64 | `<value_list_tail> → λ` | `First(λ) ∪ Follow(<value_list_tail>)` | `{ ) }` |
| 65 | `<array_dims> → [ <size> ] <array_dim2_opt>` | `First([)` | `{ [ }` |
| 66 | `<array_dim2_opt> → [ <size> ]` | `First([)` | `{ [ }` |
| 67 | `<array_dim2_opt> → λ` | `First(λ) ∪ Follow(<array_dim2_opt>)` | `{ ,, ;, id }` |
| 68 | `<array_with_init> → [ <size> ] <array_init_tail>` | `First([)` | `{ [ }` |
| 69 | `<array_init_tail> → [ <size> ] <arr_init_opt_2d>` | `First([)` | `{ [ }` |
| 70 | `<array_init_tail> → <arr_init_opt_1d>` | `First(<arr_init_opt_1d>)` | `{ ,, ;, = }` |
| 71 | `<arr_init_opt_1d> → = { <arr_init_content_1d> }` | `First(=)` | `{ = }` |
| 72 | `<arr_init_opt_1d> → λ` | `First(λ) ∪ Follow(<arr_init_opt_1d>)` | `{ ,, ; }` |
| 73 | `<arr_init_content_1d> → <arr_elem> <elem_1d_tail>` | `First(<arr_elem>)` | `{ bool, char, charlit, double, doublelit, false, float, floatlit, int, intlit, long, longlit, string, stringlit, true }` |
| 74 | `<arr_init_content_1d> → λ` | `First(λ) ∪ Follow(<arr_init_content_1d>)` | `{ } }` |
| 75 | `<arr_init_opt_2d> → = { <arr_init_content_2d> }` | `First(=)` | `{ = }` |
| 76 | `<arr_init_opt_2d> → λ` | `First(λ) ∪ Follow(<arr_init_opt_2d>)` | `{ ,, ; }` |
| 77 | `<arr_init_content_2d> → { <elem_list> } <elem_2d_tail>` | `First({)` | `{ { }` |
| 78 | `<arr_init_content_2d> → λ` | `First(λ) ∪ Follow(<arr_init_content_2d>)` | `{ } }` |
| 79 | `<elem_2d_tail> → , { <elem_list> } <elem_2d_tail>` | `First(,)` | `{ , }` |
| 80 | `<elem_2d_tail> → λ` | `First(λ) ∪ Follow(<elem_2d_tail>)` | `{ } }` |
| 81 | `<elem_list> → <arr_elem> <elem_1d_tail>` | `First(<arr_elem>)` | `{ bool, char, charlit, double, doublelit, false, float, floatlit, int, intlit, long, longlit, string, stringlit, true }` |
| 82 | `<elem_list> → λ` | `First(λ) ∪ Follow(<elem_list>)` | `{ } }` |
| 83 | `<elem_1d_tail> → , <arr_elem> <elem_1d_tail>` | `First(,)` | `{ , }` |
| 84 | `<elem_1d_tail> → λ` | `First(λ) ∪ Follow(<elem_1d_tail>)` | `{ } }` |
| 85 | `<arr_elem> → int ( <value> )` | `First(int)` | `{ int }` |
| 86 | `<arr_elem> → long ( <value> )` | `First(long)` | `{ long }` |
| 87 | `<arr_elem> → float ( <value> )` | `First(float)` | `{ float }` |
| 88 | `<arr_elem> → double ( <value> )` | `First(double)` | `{ double }` |
| 89 | `<arr_elem> → char ( <value> )` | `First(char)` | `{ char }` |
| 90 | `<arr_elem> → string ( <value> )` | `First(string)` | `{ string }` |
| 91 | `<arr_elem> → bool ( <value> )` | `First(bool)` | `{ bool }` |
| 92 | `<arr_elem> → intlit` | `First(intlit)` | `{ intlit }` |
| 93 | `<arr_elem> → longlit` | `First(longlit)` | `{ longlit }` |
| 94 | `<arr_elem> → floatlit` | `First(floatlit)` | `{ floatlit }` |
| 95 | `<arr_elem> → doublelit` | `First(doublelit)` | `{ doublelit }` |
| 96 | `<arr_elem> → charlit` | `First(charlit)` | `{ charlit }` |
| 97 | `<arr_elem> → stringlit` | `First(stringlit)` | `{ stringlit }` |
| 98 | `<arr_elem> → true` | `First(true)` | `{ true }` |
| 99 | `<arr_elem> → false` | `First(false)` | `{ false }` |
| 100 | `<size> → intlit` | `First(intlit)` | `{ intlit }` |
| 101 | `<size> → id` | `First(id)` | `{ id }` |
| 102 | `<field_list> → <field_dec> <field_list>` | `First(<field_dec>)` | `{ bool, char, double, float, id, int, long, string }` |
| 103 | `<field_list> → λ` | `First(λ) ∪ Follow(<field_list>)` | `{ } }` |
| 104 | `<field_dec> → <field_type> id <field_arr_opt> <field_cont> ;` | `First(<field_type>)` | `{ bool, char, double, float, id, int, long, string }` |
| 105 | `<field_type> → int` | `First(int)` | `{ int }` |
| 106 | `<field_type> → long` | `First(long)` | `{ long }` |
| 107 | `<field_type> → float` | `First(float)` | `{ float }` |
| 108 | `<field_type> → double` | `First(double)` | `{ double }` |
| 109 | `<field_type> → char` | `First(char)` | `{ char }` |
| 110 | `<field_type> → string` | `First(string)` | `{ string }` |
| 111 | `<field_type> → bool` | `First(bool)` | `{ bool }` |
| 112 | `<field_type> → id` | `First(id)` | `{ id }` |
| 113 | `<field_arr_opt> → <array_dims>` | `First(<array_dims>)` | `{ [ }` |
| 114 | `<field_arr_opt> → λ` | `First(λ) ∪ Follow(<field_arr_opt>)` | `{ ,, ; }` |
| 115 | `<field_cont> → , id <field_arr_opt> <field_cont>` | `First(,)` | `{ , }` |
| 116 | `<field_cont> → λ` | `First(λ) ∪ Follow(<field_cont>)` | `{ ; }` |
| 117 | `<nonvoid_ret_type> → int <ret_type_suffix>` | `First(int)` | `{ int }` |
| 118 | `<nonvoid_ret_type> → long <ret_type_suffix>` | `First(long)` | `{ long }` |
| 119 | `<nonvoid_ret_type> → float <ret_type_suffix>` | `First(float)` | `{ float }` |
| 120 | `<nonvoid_ret_type> → double <ret_type_suffix>` | `First(double)` | `{ double }` |
| 121 | `<nonvoid_ret_type> → char <ret_type_suffix>` | `First(char)` | `{ char }` |
| 122 | `<nonvoid_ret_type> → string <ret_type_suffix>` | `First(string)` | `{ string }` |
| 123 | `<nonvoid_ret_type> → bool <ret_type_suffix>` | `First(bool)` | `{ bool }` |
| 124 | `<nonvoid_ret_type> → id <ret_id_suffix>` | `First(id)` | `{ id }` |
| 125 | `<ret_type_suffix> → <array_dims>` | `First(<array_dims>)` | `{ [ }` |
| 126 | `<ret_type_suffix> → λ` | `First(λ) ∪ Follow(<ret_type_suffix>)` | `{ id }` |
| 127 | `<ret_id_suffix> → <array_dims>` | `First(<array_dims>)` | `{ [ }` |
| 128 | `<ret_id_suffix> → . id` | `First(.)` | `{ . }` |
| 129 | `<ret_id_suffix> → λ` | `First(λ) ∪ Follow(<ret_id_suffix>)` | `{ id }` |
| 130 | `<param_list> → <param_type> id <param_arr_opt> <param_cont>` | `First(<param_type>)` | `{ bool, char, double, float, id, int, long, string }` |
| 131 | `<param_list> → λ` | `First(λ) ∪ Follow(<param_list>)` | `{ ) }` |
| 132 | `<param_type> → int` | `First(int)` | `{ int }` |
| 133 | `<param_type> → long` | `First(long)` | `{ long }` |
| 134 | `<param_type> → float` | `First(float)` | `{ float }` |
| 135 | `<param_type> → double` | `First(double)` | `{ double }` |
| 136 | `<param_type> → char` | `First(char)` | `{ char }` |
| 137 | `<param_type> → string` | `First(string)` | `{ string }` |
| 138 | `<param_type> → bool` | `First(bool)` | `{ bool }` |
| 139 | `<param_type> → id` | `First(id)` | `{ id }` |
| 140 | `<param_arr_opt> → <array_dims>` | `First(<array_dims>)` | `{ [ }` |
| 141 | `<param_arr_opt> → λ` | `First(λ) ∪ Follow(<param_arr_opt>)` | `{ ), , }` |
| 142 | `<param_cont> → , <param_type> id <param_arr_opt> <param_cont>` | `First(,)` | `{ , }` |
| 143 | `<param_cont> → λ` | `First(λ) ∪ Follow(<param_cont>)` | `{ ) }` |
| 144 | `<function_body_nonvoid> → <func_content_nonvoid>` | `First(<func_content_nonvoid>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 145 | `<func_content_nonvoid> → using id <using_cont> ; <func_content_nonvoid>` | `First(using)` | `{ using }` |
| 146 | `<func_content_nonvoid> → local <mutability> <local_dec_body> <func_content_nonvoid>` | `First(local)` | `{ local }` |
| 147 | `<func_content_nonvoid> → <statement_non_return> <func_content_nonvoid>` | `First(<statement_non_return>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, string, stringlit, switch, thread, threadln, trap, true, while }` |
| 148 | `<func_content_nonvoid> → return <expression> ;` | `First(return)` | `{ return }` |
| 149 | `<function_body_void> → <func_content_void>` | `First(<func_content_void>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 150 | `<func_content_void> → using id <using_cont> ; <func_content_void>` | `First(using)` | `{ using }` |
| 151 | `<func_content_void> → local <mutability> <local_dec_body> <func_content_void>` | `First(local)` | `{ local }` |
| 152 | `<func_content_void> → <statement_non_return> <func_content_void>` | `First(<statement_non_return>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, string, stringlit, switch, thread, threadln, trap, true, while }` |
| 153 | `<func_content_void> → return ;` | `First(return)` | `{ return }` |
| 154 | `<using_block> → using id <using_cont> ; <using_block>` | `First(using)` | `{ using }` |
| 155 | `<using_block> → λ` | `First(λ) ∪ Follow(<using_block>)` | `{ local }` |
| 156 | `<using_cont> → , id <using_cont>` | `First(,)` | `{ , }` |
| 157 | `<using_cont> → λ` | `First(λ) ∪ Follow(<using_cont>)` | `{ ; }` |
| 158 | `<local_block> → local <mutability> <local_dec_body> <local_block>` | `First(local)` | `{ local }` |
| 159 | `<local_block> → λ` | `First(λ) ∪ Follow(<local_block>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, while }` |
| 160 | `<local_dec_body> → int id <typed_local_tail>` | `First(int)` | `{ int }` |
| 161 | `<local_dec_body> → long id <typed_local_tail>` | `First(long)` | `{ long }` |
| 162 | `<local_dec_body> → float id <typed_local_tail>` | `First(float)` | `{ float }` |
| 163 | `<local_dec_body> → double id <typed_local_tail>` | `First(double)` | `{ double }` |
| 164 | `<local_dec_body> → char id <typed_local_tail>` | `First(char)` | `{ char }` |
| 165 | `<local_dec_body> → string id <typed_local_tail>` | `First(string)` | `{ string }` |
| 166 | `<local_dec_body> → bool id <typed_local_tail>` | `First(bool)` | `{ bool }` |
| 167 | `<local_dec_body> → id id <weave_local_tail>` | `First(id)` | `{ id }` |
| 168 | `<typed_local_tail> → <array_with_init> ;` | `First(<array_with_init>)` | `{ [ }` |
| 169 | `<typed_local_tail> → = <expression> <multi_local> ;` | `First(=)` | `{ = }` |
| 170 | `<multi_local> → , id = <expression> <multi_local>` | `First(,)` | `{ , }` |
| 171 | `<multi_local> → λ` | `First(λ) ∪ Follow(<multi_local>)` | `{ ; }` |
| 172 | `<weave_local_tail> → = { <weave_field_value> <weave_field_list_tail> } <weave_inst_cont> ;` | `First(=)` | `{ = }` |
| 173 | `<weave_local_tail> → <array_with_init> <weave_arr_cont> ;` | `First(<array_with_init>)` | `{ [ }` |
| 174 | `<statement_non_return> → <expression> ;` | `First(<expression>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 175 | `<statement_non_return> → <io_stmt>` | `First(<io_stmt>)` | `{ thread, threadln, trap }` |
| 176 | `<statement_non_return> → <ctrl_struct>` | `First(<ctrl_struct>)` | `{ do, for, if, switch, while }` |
| 177 | `<statement_non_return> → break ;` | `First(break)` | `{ break }` |
| 178 | `<ctrl_stmt_list> → <statement_non_return> <ctrl_stmt_list>` | `First(<statement_non_return>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, string, stringlit, switch, thread, threadln, trap, true, while }` |
| 179 | `<ctrl_stmt_list> → λ` | `First(λ) ∪ Follow(<ctrl_stmt_list>)` | `{ case, default, while, } }` |
| 180 | `<expression> → <assign_expr>` | `First(<assign_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 181 | `<assign_expr> → <concat_expr> <assign_tail>` | `First(<concat_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 182 | `<assign_tail> → <assign_op> <assign_expr>` | `First(<assign_op>)` | `{ %=, *=, +=, -=, /=, = }` |
| 183 | `<assign_tail> → λ` | `First(λ) ∪ Follow(<assign_tail>)` | `{ ), ,, ; }` |
| 184 | `<assign_op> → =` | `First(=)` | `{ = }` |
| 185 | `<assign_op> → +=` | `First(+=)` | `{ += }` |
| 186 | `<assign_op> → -=` | `First(-=)` | `{ -= }` |
| 187 | `<assign_op> → *=` | `First(*=)` | `{ *= }` |
| 188 | `<assign_op> → /=` | `First(/=)` | `{ /= }` |
| 189 | `<assign_op> → %=` | `First(%=)` | `{ %= }` |
| 190 | `<concat_expr> → <or_expr> <concat_tail>` | `First(<or_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 191 | `<concat_tail> → .. <or_expr> <concat_tail>` | `First(..)` | `{ .. }` |
| 192 | `<concat_tail> → λ` | `First(λ) ∪ Follow(<concat_tail>)` | `{ ), ,, ;, %=, *=, +=, -=, /=, = }` |
| 193 | `<or_expr> → <and_expr> <or_tail>` | `First(<and_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 194 | `<or_tail> → \|\| <and_expr> <or_tail>` | `First(\|\|)` | `{ \|\| }` |
| 195 | `<or_tail> → λ` | `First(λ) ∪ Follow(<or_tail>)` | `{ ), ,, .., ;, %=, *=, +=, -=, /=, = }` |
| 196 | `<and_expr> → <eq_expr> <and_tail>` | `First(<eq_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 197 | `<and_tail> → && <eq_expr> <and_tail>` | `First(&&)` | `{ && }` |
| 198 | `<and_tail> → λ` | `First(λ) ∪ Follow(<and_tail>)` | `{ ), ,, .., ;, %=, *=, +=, -=, /=, =, \|\| }` |
| 199 | `<eq_expr> → <rel_expr> <eq_tail>` | `First(<rel_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 200 | `<eq_tail> → == <rel_expr> <eq_tail>` | `First(==)` | `{ == }` |
| 201 | `<eq_tail> → != <rel_expr> <eq_tail>` | `First(!=)` | `{ != }` |
| 202 | `<eq_tail> → λ` | `First(λ) ∪ Follow(<eq_tail>)` | `{ &&, ), ,, .., ;, %=, *=, +=, -=, /=, =, \|\| }` |
| 203 | `<rel_expr> → <add_expr> <rel_tail>` | `First(<add_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 204 | `<rel_tail> → < <add_expr>` | `First(<)` | `{ < }` |
| 205 | `<rel_tail> → > <add_expr>` | `First(>)` | `{ > }` |
| 206 | `<rel_tail> → <= <add_expr>` | `First(<=)` | `{ <= }` |
| 207 | `<rel_tail> → >= <add_expr>` | `First(>=)` | `{ >= }` |
| 208 | `<rel_tail> → λ` | `First(λ) ∪ Follow(<rel_tail>)` | `{ !=, &&, ), ,, .., ;, %=, *=, +=, -=, /=, =, ==, \|\| }` |
| 209 | `<add_expr> → <mul_expr> <add_tail>` | `First(<mul_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 210 | `<add_tail> → + <mul_expr> <add_tail>` | `First(+)` | `{ + }` |
| 211 | `<add_tail> → - <mul_expr> <add_tail>` | `First(-)` | `{ - }` |
| 212 | `<add_tail> → λ` | `First(λ) ∪ Follow(<add_tail>)` | `{ !=, &&, ), ,, .., ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 213 | `<mul_expr> → <unary_expr> <mul_tail>` | `First(<unary_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 214 | `<mul_tail> → * <unary_expr> <mul_tail>` | `First(*)` | `{ * }` |
| 215 | `<mul_tail> → / <unary_expr> <mul_tail>` | `First(/)` | `{ / }` |
| 216 | `<mul_tail> → % <unary_expr> <mul_tail>` | `First(%)` | `{ % }` |
| 217 | `<mul_tail> → λ` | `First(λ) ∪ Follow(<mul_tail>)` | `{ !=, &&, ), +, ,, -, .., ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 218 | `<unary_expr> → ! <unary_expr>` | `First(!)` | `{ ! }` |
| 219 | `<unary_expr> → ++ <unary_expr>` | `First(++)` | `{ ++ }` |
| 220 | `<unary_expr> → -- <unary_expr>` | `First(--)` | `{ -- }` |
| 221 | `<unary_expr> → <postfix_expr>` | `First(<postfix_expr>)` | `{ (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 222 | `<postfix_expr> → ( <expression> ) <postfix_chain>` | `First(()` | `{ ( }` |
| 223 | `<postfix_expr> → int ( <expression> )` | `First(int)` | `{ int }` |
| 224 | `<postfix_expr> → long ( <expression> )` | `First(long)` | `{ long }` |
| 225 | `<postfix_expr> → float ( <expression> )` | `First(float)` | `{ float }` |
| 226 | `<postfix_expr> → double ( <expression> )` | `First(double)` | `{ double }` |
| 227 | `<postfix_expr> → char ( <expression> )` | `First(char)` | `{ char }` |
| 228 | `<postfix_expr> → string ( <expression> )` | `First(string)` | `{ string }` |
| 229 | `<postfix_expr> → bool ( <expression> )` | `First(bool)` | `{ bool }` |
| 230 | `<postfix_expr> → id <postfix_chain>` | `First(id)` | `{ id }` |
| 231 | `<postfix_expr> → intlit` | `First(intlit)` | `{ intlit }` |
| 232 | `<postfix_expr> → longlit` | `First(longlit)` | `{ longlit }` |
| 233 | `<postfix_expr> → floatlit` | `First(floatlit)` | `{ floatlit }` |
| 234 | `<postfix_expr> → doublelit` | `First(doublelit)` | `{ doublelit }` |
| 235 | `<postfix_expr> → charlit` | `First(charlit)` | `{ charlit }` |
| 236 | `<postfix_expr> → stringlit` | `First(stringlit)` | `{ stringlit }` |
| 237 | `<postfix_expr> → true` | `First(true)` | `{ true }` |
| 238 | `<postfix_expr> → false` | `First(false)` | `{ false }` |
| 239 | `<postfix_chain> → <array_access> <postfix_after_arr>` | `First(<array_access>)` | `{ [ }` |
| 240 | `<postfix_chain> → . id <postfix_chain>` | `First(.)` | `{ . }` |
| 241 | `<postfix_chain> → ( <arg_list> ) <postfix_chain>` | `First(()` | `{ ( }` |
| 242 | `<postfix_chain> → ++` | `First(++)` | `{ ++ }` |
| 243 | `<postfix_chain> → --` | `First(--)` | `{ -- }` |
| 244 | `<postfix_chain> → λ` | `First(λ) ∪ Follow(<postfix_chain>)` | `{ %, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 245 | `<array_access> → [ <array_index> ] <array_access_dim2>` | `First([)` | `{ [ }` |
| 246 | `<array_access_dim2> → [ <array_index> ]` | `First([)` | `{ [ }` |
| 247 | `<array_access_dim2> → λ` | `First(λ) ∪ Follow(<array_access_dim2>)` | `{ (, ++, --, ., %, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 248 | `<postfix_after_arr> → . id <postfix_chain>` | `First(.)` | `{ . }` |
| 249 | `<postfix_after_arr> → ( <arg_list> ) <postfix_chain>` | `First(()` | `{ ( }` |
| 250 | `<postfix_after_arr> → ++` | `First(++)` | `{ ++ }` |
| 251 | `<postfix_after_arr> → --` | `First(--)` | `{ -- }` |
| 252 | `<postfix_after_arr> → λ` | `First(λ) ∪ Follow(<postfix_after_arr>)` | `{ %, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 253 | `<array_index> → intlit` | `First(intlit)` | `{ intlit }` |
| 254 | `<array_index> → id` | `First(id)` | `{ id }` |
| 255 | `<arg_list> → <expression> <arg_tail>` | `First(<expression>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 256 | `<arg_list> → λ` | `First(λ) ∪ Follow(<arg_list>)` | `{ ) }` |
| 257 | `<arg_tail> → , <expression> <arg_tail>` | `First(,)` | `{ , }` |
| 258 | `<arg_tail> → λ` | `First(λ) ∪ Follow(<arg_tail>)` | `{ ) }` |
| 259 | `<io_stmt> → trap ( <expression> ) ;` | `First(trap)` | `{ trap }` |
| 260 | `<io_stmt> → thread ( <print_args> ) ;` | `First(thread)` | `{ thread }` |
| 261 | `<io_stmt> → threadln ( <print_args> ) ;` | `First(threadln)` | `{ threadln }` |
| 262 | `<print_args> → <expression> <print_tail>` | `First(<expression>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 263 | `<print_tail> → , <expression> <print_tail>` | `First(,)` | `{ , }` |
| 264 | `<print_tail> → λ` | `First(λ) ∪ Follow(<print_tail>)` | `{ ) }` |
| 265 | `<ctrl_struct> → if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` | `First(if)` | `{ if }` |
| 266 | `<ctrl_struct> → switch ( <expression> ) { <case_list> <default_opt> }` | `First(switch)` | `{ switch }` |
| 267 | `<ctrl_struct> → for ( <for_init> ; <for_cond> ; <for_update> ) { <ctrl_stmt_list> }` | `First(for)` | `{ for }` |
| 268 | `<ctrl_struct> → while ( <condition> ) { <ctrl_stmt_list> }` | `First(while)` | `{ while }` |
| 269 | `<ctrl_struct> → do { <ctrl_stmt_list> } while ( <condition> ) ;` | `First(do)` | `{ do }` |
| 270 | `<else_opt> → else <else_body>` | `First(else)` | `{ else }` |
| 271 | `<else_opt> → λ` | `First(λ) ∪ Follow(<else_opt>)` | `{ !, (, ++, --, bool, break, case, char, charlit, default, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while, } }` |
| 272 | `<else_body> → { <ctrl_stmt_list> }` | `First({)` | `{ { }` |
| 273 | `<else_body> → if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` | `First(if)` | `{ if }` |
| 274 | `<case_list> → case <case_val> : <ctrl_stmt_list> <break_opt> <case_list>` | `First(case)` | `{ case }` |
| 275 | `<case_list> → λ` | `First(λ) ∪ Follow(<case_list>)` | `{ default, } }` |
| 276 | `<case_val> → intlit` | `First(intlit)` | `{ intlit }` |
| 277 | `<case_val> → longlit` | `First(longlit)` | `{ longlit }` |
| 278 | `<case_val> → charlit` | `First(charlit)` | `{ charlit }` |
| 279 | `<case_val> → true` | `First(true)` | `{ true }` |
| 280 | `<case_val> → false` | `First(false)` | `{ false }` |
| 281 | `<default_opt> → default : <ctrl_stmt_list> <break_opt>` | `First(default)` | `{ default }` |
| 282 | `<default_opt> → λ` | `First(λ) ∪ Follow(<default_opt>)` | `{ } }` |
| 283 | `<break_opt> → break ;` | `First(break)` | `{ break }` |
| 284 | `<break_opt> → λ` | `First(λ) ∪ Follow(<break_opt>)` | `{ case, default, } }` |
| 285 | `<for_init> → local var <for_init_type> id = <for_init_expr>` | `First(local)` | `{ local }` |
| 286 | `<for_init> → id <for_init_assign_tail>` | `First(id)` | `{ id }` |
| 287 | `<for_init> → λ` | `First(λ) ∪ Follow(<for_init>)` | `{ ; }` |
| 288 | `<for_init_assign_tail> → <assign_op> <for_init_expr>` | `First(<assign_op>)` | `{ %=, *=, +=, -=, /=, = }` |
| 289 | `<for_init_expr> → <concat_expr>` | `First(<concat_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 290 | `<for_init_type> → int` | `First(int)` | `{ int }` |
| 291 | `<for_init_type> → long` | `First(long)` | `{ long }` |
| 292 | `<for_init_type> → float` | `First(float)` | `{ float }` |
| 293 | `<for_init_type> → double` | `First(double)` | `{ double }` |
| 294 | `<for_init_type> → char` | `First(char)` | `{ char }` |
| 295 | `<for_init_type> → string` | `First(string)` | `{ string }` |
| 296 | `<for_init_type> → bool` | `First(bool)` | `{ bool }` |
| 297 | `<for_cond> → <condition>` | `First(<condition>)` | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 298 | `<for_cond> → λ` | `First(λ) ∪ Follow(<for_cond>)` | `{ ; }` |
| 299 | `<for_update> → id <for_update_tail>` | `First(id)` | `{ id }` |
| 300 | `<for_update> → ++ id` | `First(++)` | `{ ++ }` |
| 301 | `<for_update> → -- id` | `First(--)` | `{ -- }` |
| 302 | `<for_update> → λ` | `First(λ) ∪ Follow(<for_update>)` | `{ ) }` |
| 303 | `<for_update_tail> → ++` | `First(++)` | `{ ++ }` |
| 304 | `<for_update_tail> → --` | `First(--)` | `{ -- }` |
| 305 | `<for_update_tail> → <assign_op> <expression>` | `First(<assign_op>)` | `{ %=, *=, +=, -=, /=, = }` |
| 306 | `<condition> → <cond_or>` | `First(<cond_or>)` | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 307 | `<cond_or> → <cond_and> <cond_or_tail>` | `First(<cond_and>)` | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 308 | `<cond_or_tail> → \|\| <cond_and> <cond_or_tail>` | `First(\|\|)` | `{ \|\| }` |
| 309 | `<cond_or_tail> → λ` | `First(λ) ∪ Follow(<cond_or_tail>)` | `{ ) }` |
| 310 | `<cond_and> → <cond_not> <cond_and_tail>` | `First(<cond_not>)` | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 311 | `<cond_and_tail> → && <cond_not> <cond_and_tail>` | `First(&&)` | `{ && }` |
| 312 | `<cond_and_tail> → λ` | `First(λ) ∪ Follow(<cond_and_tail>)` | `{ ), \|\| }` |
| 313 | `<cond_not> → ! <cond_not>` | `First(!)` | `{ ! }` |
| 314 | `<cond_not> → <cond_atom>` | `First(<cond_atom>)` | `{ (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 315 | `<cond_rhs_expr> → <concat_expr>` | `First(<concat_expr>)` | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 316 | `<cond_atom> → true` | `First(true)` | `{ true }` |
| 317 | `<cond_atom> → false` | `First(false)` | `{ false }` |
| 318 | `<cond_atom> → ( <condition> )` | `First(()` | `{ ( }` |
| 319 | `<cond_atom> → id <cond_after_id>` | `First(id)` | `{ id }` |
| 320 | `<cond_atom> → intlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(intlit)` | `{ intlit }` |
| 321 | `<cond_atom> → longlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(longlit)` | `{ longlit }` |
| 322 | `<cond_atom> → floatlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(floatlit)` | `{ floatlit }` |
| 323 | `<cond_atom> → doublelit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(doublelit)` | `{ doublelit }` |
| 324 | `<cond_atom> → charlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(charlit)` | `{ charlit }` |
| 325 | `<cond_atom> → stringlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(stringlit)` | `{ stringlit }` |
| 326 | `<cond_atom> → int ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(int)` | `{ int }` |
| 327 | `<cond_atom> → long ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(long)` | `{ long }` |
| 328 | `<cond_atom> → float ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(float)` | `{ float }` |
| 329 | `<cond_atom> → double ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(double)` | `{ double }` |
| 330 | `<cond_atom> → char ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(char)` | `{ char }` |
| 331 | `<cond_atom> → string ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(string)` | `{ string }` |
| 332 | `<cond_atom> → bool ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(bool)` | `{ bool }` |
| 333 | `<cond_after_id> → ( <arg_list> ) <cond_after_call>` | `First(()` | `{ ( }` |
| 334 | `<cond_after_id> → <cond_after_id_no_call> <cond_comparison_opt>` | `First(<cond_after_id_no_call>)` | `{ ++, --, ., [, !=, <, <=, ==, >, >=, &&, ), \|\| }` |
| 335 | `<cond_after_call> → λ` | `First(λ) ∪ Follow(<cond_after_call>)` | `{ &&, ), \|\| }` |
| 336 | `<cond_after_call> → <postfix_chain> <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | `First(<postfix_chain>)` | `{ (, ++, --, ., [ }` |
| 337 | `<cond_after_id_no_call> → <cond_postfix_no_call> <mul_tail> <add_tail>` | `First(<cond_postfix_no_call>)` | `{ ++, --, ., [, %, *, +, -, / }` |
| 338 | `<cond_comparison_opt> → <comp_op> <cond_rhs_expr>` | `First(<comp_op>)` | `{ !=, <, <=, ==, >, >= }` |
| 339 | `<cond_comparison_opt> → λ` | `First(λ) ∪ Follow(<cond_comparison_opt>)` | `{ &&, ), \|\| }` |
| 340 | `<cond_postfix_no_call> → [ <array_index> ] <array_access_dim2> <postfix_after_arr>` | `First([)` | `{ [ }` |
| 341 | `<cond_postfix_no_call> → . id <postfix_chain>` | `First(.)` | `{ . }` |
| 342 | `<cond_postfix_no_call> → ++` | `First(++)` | `{ ++ }` |
| 343 | `<cond_postfix_no_call> → --` | `First(--)` | `{ -- }` |
| 344 | `<cond_postfix_no_call> → λ` | `First(λ) ∪ Follow(<cond_postfix_no_call>)` | `{ %, *, +, -, / }` |
| 345 | `<comp_op> → ==` | `First(==)` | `{ == }` |
| 346 | `<comp_op> → !=` | `First(!=)` | `{ != }` |
| 347 | `<comp_op> → <` | `First(<)` | `{ < }` |
| 348 | `<comp_op> → >` | `First(>)` | `{ > }` |
| 349 | `<comp_op> → <=` | `First(<=)` | `{ <= }` |
| 350 | `<comp_op> → >=` | `First(>=)` | `{ >= }` |
| 351 | `<main_body> → <main_content>` | `First(<main_content>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 352 | `<main_content> → using id <using_cont> ; <main_content>` | `First(using)` | `{ using }` |
| 353 | `<main_content> → local <mutability> <local_dec_body> <main_content>` | `First(local)` | `{ local }` |
| 354 | `<main_content> → <statement_non_return> <main_content>` | `First(<statement_non_return>)` | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, string, stringlit, switch, thread, threadln, trap, true, while }` |
| 355 | `<main_content> → return intlit ;` | `First(return)` | `{ return }` |
