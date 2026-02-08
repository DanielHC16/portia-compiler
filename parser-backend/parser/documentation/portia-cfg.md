## Context-Free Grammar

| # | Production | → | Production Set |
|---|------------|---|----------------|
| 1 | `<program>` | → | `<decl_list>` |
| 2 | `<decl_list>` | → | `int <int_decl_or_main>` |
| 3 | `<decl_list>` | → | `<other_decl> <decl_list>` |
| 4 | `<int_decl_or_main>` | → | `id <typed_decl_tail> <decl_list>` |
| 5 | `<int_decl_or_main>` | → | `main ( ) { <main_body> } $END` |
| 6 | `<other_decl>` | → | `global <mutability> <dtype> id = <expression> <multi_global> ;` |
| 7 | `<other_decl>` | → | `long id <typed_decl_tail>` |
| 8 | `<other_decl>` | → | `float id <typed_decl_tail>` |
| 9 | `<other_decl>` | → | `double id <typed_decl_tail>` |
| 10 | `<other_decl>` | → | `char id <typed_decl_tail>` |
| 11 | `<other_decl>` | → | `string id <typed_decl_tail>` |
| 12 | `<other_decl>` | → | `bool id <typed_decl_tail>` |
| 13 | `<other_decl>` | → | `weave id { <field_list> } ;` |
| 14 | `<other_decl>` | → | `id <weave_inst_decl>` |
| 15 | `<other_decl>` | → | `func <nonvoid_ret_type> id ( <param_list> ) { <function_body_nonvoid> }` |
| 16 | `<other_decl>` | → | `func void id ( <param_list> ) { <function_body_void> }` |
| 17 | `<main_func>` | → | `int main ( ) { <main_body> }` |
| 18 | `<multi_global>` | → | `, id = <expression> <multi_global>` |
| 19 | `<multi_global>` | → | `λ` |
| 20 | `<weave_inst_decl>` | → | `id <weave_inst_tail> <weave_inst_cont> ;` |
| 21 | `<weave_inst_decl>` | → | `<array_with_init> <weave_arr_cont> ;` |
| 22 | `<weave_inst_tail>` | → | `= { <weave_field_value> <weave_field_list_tail> }` |
| 23 | `<weave_inst_tail>` | → | `<array_with_init>` |
| 24 | `<weave_field_value>` | → | `intlit` |
| 25 | `<weave_field_value>` | → | `longlit` |
| 26 | `<weave_field_value>` | → | `floatlit` |
| 27 | `<weave_field_value>` | → | `doublelit` |
| 28 | `<weave_field_value>` | → | `charlit` |
| 29 | `<weave_field_value>` | → | `stringlit` |
| 30 | `<weave_field_value>` | → | `true` |
| 31 | `<weave_field_value>` | → | `false` |
| 32 | `<weave_field_value>` | → | `{ <weave_arr_content> }` |
| 33 | `<weave_arr_content>` | → | `{ <elem_list> } <elem_2d_tail>` |
| 34 | `<weave_arr_content>` | → | `<arr_elem> <elem_1d_tail>` |
| 35 | `<weave_arr_content>` | → | `λ` |
| 36 | `<weave_field_list_tail>` | → | `, <weave_field_value> <weave_field_list_tail>` |
| 37 | `<weave_field_list_tail>` | → | `λ` |
| 38 | `<weave_inst_cont>` | → | `, id <weave_inst_tail> <weave_inst_cont>` |
| 39 | `<weave_inst_cont>` | → | `λ` |
| 40 | `<weave_arr_cont>` | → | `, id <array_with_init> <weave_arr_cont>` |
| 41 | `<weave_arr_cont>` | → | `λ` |
| 42 | `<typed_decl_tail>` | → | `<array_with_init> ;` |
| 43 | `<typed_decl_tail>` | → | `= <expression> <multi_typed> ;` |
| 44 | `<multi_typed>` | → | `, id = <expression> <multi_typed>` |
| 45 | `<multi_typed>` | → | `λ` |
| 46 | `<mutability>` | → | `var` |
| 47 | `<mutability>` | → | `const` |
| 48 | `<dtype>` | → | `int` |
| 49 | `<dtype>` | → | `long` |
| 50 | `<dtype>` | → | `float` |
| 51 | `<dtype>` | → | `double` |
| 52 | `<dtype>` | → | `char` |
| 53 | `<dtype>` | → | `string` |
| 54 | `<dtype>` | → | `bool` |
| 55 | `<value>` | → | `intlit` |
| 56 | `<value>` | → | `longlit` |
| 57 | `<value>` | → | `floatlit` |
| 58 | `<value>` | → | `doublelit` |
| 59 | `<value>` | → | `charlit` |
| 60 | `<value>` | → | `stringlit` |
| 61 | `<value>` | → | `true` |
| 62 | `<value>` | → | `false` |
| 63 | `<value_list_tail>` | → | `, <value> <value_list_tail>` |
| 64 | `<value_list_tail>` | → | `λ` |
| 65 | `<array_dims>` | → | `[ <size> ] <array_dim2_opt>` |
| 66 | `<array_dim2_opt>` | → | `[ <size> ]` |
| 67 | `<array_dim2_opt>` | → | `λ` |
| 68 | `<array_with_init>` | → | `[ <size> ] <array_init_tail>` |
| 69 | `<array_init_tail>` | → | `[ <size> ] <arr_init_opt_2d>` |
| 70 | `<array_init_tail>` | → | `<arr_init_opt_1d>` |
| 71 | `<arr_init_opt_1d>` | → | `= { <arr_init_content_1d> }` |
| 72 | `<arr_init_opt_1d>` | → | `λ` |
| 73 | `<arr_init_content_1d>` | → | `<arr_elem> <elem_1d_tail>` |
| 74 | `<arr_init_content_1d>` | → | `λ` |
| 75 | `<arr_init_opt_2d>` | → | `= { <arr_init_content_2d> }` |
| 76 | `<arr_init_opt_2d>` | → | `λ` |
| 77 | `<arr_init_content_2d>` | → | `{ <elem_list> } <elem_2d_tail>` |
| 78 | `<arr_init_content_2d>` | → | `λ` |
| 79 | `<elem_2d_tail>` | → | `, { <elem_list> } <elem_2d_tail>` |
| 80 | `<elem_2d_tail>` | → | `λ` |
| 81 | `<elem_list>` | → | `<arr_elem> <elem_1d_tail>` |
| 82 | `<elem_list>` | → | `λ` |
| 83 | `<elem_1d_tail>` | → | `, <arr_elem> <elem_1d_tail>` |
| 84 | `<elem_1d_tail>` | → | `λ` |
| 85 | `<arr_elem>` | → | `int ( <value> )` |
| 86 | `<arr_elem>` | → | `long ( <value> )` |
| 87 | `<arr_elem>` | → | `float ( <value> )` |
| 88 | `<arr_elem>` | → | `double ( <value> )` |
| 89 | `<arr_elem>` | → | `char ( <value> )` |
| 90 | `<arr_elem>` | → | `string ( <value> )` |
| 91 | `<arr_elem>` | → | `bool ( <value> )` |
| 92 | `<arr_elem>` | → | `intlit` |
| 93 | `<arr_elem>` | → | `longlit` |
| 94 | `<arr_elem>` | → | `floatlit` |
| 95 | `<arr_elem>` | → | `doublelit` |
| 96 | `<arr_elem>` | → | `charlit` |
| 97 | `<arr_elem>` | → | `stringlit` |
| 98 | `<arr_elem>` | → | `true` |
| 99 | `<arr_elem>` | → | `false` |
| 100 | `<size>` | → | `intlit` |
| 101 | `<size>` | → | `id` |
| 102 | `<field_list>` | → | `<field_dec> <field_list>` |
| 103 | `<field_list>` | → | `λ` |
| 104 | `<field_dec>` | → | `<field_type> id <field_arr_opt> <field_cont> ;` |
| 105 | `<field_type>` | → | `int` |
| 106 | `<field_type>` | → | `long` |
| 107 | `<field_type>` | → | `float` |
| 108 | `<field_type>` | → | `double` |
| 109 | `<field_type>` | → | `char` |
| 110 | `<field_type>` | → | `string` |
| 111 | `<field_type>` | → | `bool` |
| 112 | `<field_type>` | → | `id` |
| 113 | `<field_arr_opt>` | → | `<array_dims>` |
| 114 | `<field_arr_opt>` | → | `λ` |
| 115 | `<field_cont>` | → | `, id <field_arr_opt> <field_cont>` |
| 116 | `<field_cont>` | → | `λ` |
| 117 | `<nonvoid_ret_type>` | → | `int <ret_type_suffix>` |
| 118 | `<nonvoid_ret_type>` | → | `long <ret_type_suffix>` |
| 119 | `<nonvoid_ret_type>` | → | `float <ret_type_suffix>` |
| 120 | `<nonvoid_ret_type>` | → | `double <ret_type_suffix>` |
| 121 | `<nonvoid_ret_type>` | → | `char <ret_type_suffix>` |
| 122 | `<nonvoid_ret_type>` | → | `string <ret_type_suffix>` |
| 123 | `<nonvoid_ret_type>` | → | `bool <ret_type_suffix>` |
| 124 | `<nonvoid_ret_type>` | → | `id <ret_id_suffix>` |
| 125 | `<ret_type_suffix>` | → | `<array_dims>` |
| 126 | `<ret_type_suffix>` | → | `λ` |
| 127 | `<ret_id_suffix>` | → | `<array_dims>` |
| 128 | `<ret_id_suffix>` | → | `. id` |
| 129 | `<ret_id_suffix>` | → | `λ` |
| 130 | `<param_list>` | → | `<param_type> id <param_arr_opt> <param_cont>` |
| 131 | `<param_list>` | → | `λ` |
| 132 | `<param_type>` | → | `int` |
| 133 | `<param_type>` | → | `long` |
| 134 | `<param_type>` | → | `float` |
| 135 | `<param_type>` | → | `double` |
| 136 | `<param_type>` | → | `char` |
| 137 | `<param_type>` | → | `string` |
| 138 | `<param_type>` | → | `bool` |
| 139 | `<param_type>` | → | `id` |
| 140 | `<param_arr_opt>` | → | `<array_dims>` |
| 141 | `<param_arr_opt>` | → | `λ` |
| 142 | `<param_cont>` | → | `, <param_type> id <param_arr_opt> <param_cont>` |
| 143 | `<param_cont>` | → | `λ` |
| 144 | `<function_body_nonvoid>` | → | `<func_content_nonvoid>` |
| 145 | `<func_content_nonvoid>` | → | `using id <using_cont> ; <func_content_nonvoid>` |
| 146 | `<func_content_nonvoid>` | → | `local <mutability> <local_dec_body> <func_content_nonvoid>` |
| 147 | `<func_content_nonvoid>` | → | `<statement_non_return> <func_content_nonvoid>` |
| 148 | `<func_content_nonvoid>` | → | `return <expression> ;` |
| 149 | `<function_body_void>` | → | `<func_content_void>` |
| 150 | `<func_content_void>` | → | `using id <using_cont> ; <func_content_void>` |
| 151 | `<func_content_void>` | → | `local <mutability> <local_dec_body> <func_content_void>` |
| 152 | `<func_content_void>` | → | `<statement_non_return> <func_content_void>` |
| 153 | `<func_content_void>` | → | `return ;` |
| 154 | `<using_block>` | → | `using id <using_cont> ; <using_block>` |
| 155 | `<using_block>` | → | `λ` |
| 156 | `<using_cont>` | → | `, id <using_cont>` |
| 157 | `<using_cont>` | → | `λ` |
| 158 | `<local_block>` | → | `local <mutability> <local_dec_body> <local_block>` |
| 159 | `<local_block>` | → | `λ` |
| 160 | `<local_dec_body>` | → | `int id <typed_local_tail>` |
| 161 | `<local_dec_body>` | → | `long id <typed_local_tail>` |
| 162 | `<local_dec_body>` | → | `float id <typed_local_tail>` |
| 163 | `<local_dec_body>` | → | `double id <typed_local_tail>` |
| 164 | `<local_dec_body>` | → | `char id <typed_local_tail>` |
| 165 | `<local_dec_body>` | → | `string id <typed_local_tail>` |
| 166 | `<local_dec_body>` | → | `bool id <typed_local_tail>` |
| 167 | `<local_dec_body>` | → | `id id <weave_local_tail>` |
| 168 | `<typed_local_tail>` | → | `<array_with_init> ;` |
| 169 | `<typed_local_tail>` | → | `= <expression> <multi_local> ;` |
| 170 | `<multi_local>` | → | `, id = <expression> <multi_local>` |
| 171 | `<multi_local>` | → | `λ` |
| 172 | `<weave_local_tail>` | → | `= { <weave_field_value> <weave_field_list_tail> } <weave_inst_cont> ;` |
| 173 | `<weave_local_tail>` | → | `<array_with_init> <weave_arr_cont> ;` |
| 174 | `<statement_non_return>` | → | `<expression> ;` |
| 175 | `<statement_non_return>` | → | `<io_stmt>` |
| 176 | `<statement_non_return>` | → | `<ctrl_struct>` |
| 177 | `<statement_non_return>` | → | `break ;` |
| 178 | `<ctrl_stmt_list>` | → | `<statement_non_return> <ctrl_stmt_list>` |
| 179 | `<ctrl_stmt_list>` | → | `λ` |
| 180 | `<expression>` | → | `<assign_expr>` |
| 181 | `<assign_expr>` | → | `<concat_expr> <assign_tail>` |
| 182 | `<assign_tail>` | → | `<assign_op> <assign_expr>` |
| 183 | `<assign_tail>` | → | `λ` |
| 184 | `<assign_op>` | → | `=` |
| 185 | `<assign_op>` | → | `+=` |
| 186 | `<assign_op>` | → | `-=` |
| 187 | `<assign_op>` | → | `*=` |
| 188 | `<assign_op>` | → | `/=` |
| 189 | `<assign_op>` | → | `%=` |
| 190 | `<concat_expr>` | → | `<or_expr> <concat_tail>` |
| 191 | `<concat_tail>` | → | `.. <or_expr> <concat_tail>` |
| 192 | `<concat_tail>` | → | `λ` |
| 193 | `<or_expr>` | → | `<and_expr> <or_tail>` |
| 194 | `<or_tail>` | → | `\|\| <and_expr> <or_tail>` |
| 195 | `<or_tail>` | → | `λ` |
| 196 | `<and_expr>` | → | `<eq_expr> <and_tail>` |
| 197 | `<and_tail>` | → | `&& <eq_expr> <and_tail>` |
| 198 | `<and_tail>` | → | `λ` |
| 199 | `<eq_expr>` | → | `<rel_expr> <eq_tail>` |
| 200 | `<eq_tail>` | → | `== <rel_expr> <eq_tail>` |
| 201 | `<eq_tail>` | → | `!= <rel_expr> <eq_tail>` |
| 202 | `<eq_tail>` | → | `λ` |
| 203 | `<rel_expr>` | → | `<add_expr> <rel_tail>` |
| 204 | `<rel_tail>` | → | `< <add_expr>` |
| 205 | `<rel_tail>` | → | `> <add_expr>` |
| 206 | `<rel_tail>` | → | `<= <add_expr>` |
| 207 | `<rel_tail>` | → | `>= <add_expr>` |
| 208 | `<rel_tail>` | → | `λ` |
| 209 | `<add_expr>` | → | `<mul_expr> <add_tail>` |
| 210 | `<add_tail>` | → | `+ <mul_expr> <add_tail>` |
| 211 | `<add_tail>` | → | `- <mul_expr> <add_tail>` |
| 212 | `<add_tail>` | → | `λ` |
| 213 | `<mul_expr>` | → | `<unary_expr> <mul_tail>` |
| 214 | `<mul_tail>` | → | `* <unary_expr> <mul_tail>` |
| 215 | `<mul_tail>` | → | `/ <unary_expr> <mul_tail>` |
| 216 | `<mul_tail>` | → | `% <unary_expr> <mul_tail>` |
| 217 | `<mul_tail>` | → | `λ` |
| 218 | `<unary_expr>` | → | `! <unary_expr>` |
| 219 | `<unary_expr>` | → | `++ <unary_expr>` |
| 220 | `<unary_expr>` | → | `-- <unary_expr>` |
| 221 | `<unary_expr>` | → | `<postfix_expr>` |
| 222 | `<postfix_expr>` | → | `( <expression> ) <postfix_chain>` |
| 223 | `<postfix_expr>` | → | `int ( <expression> )` |
| 224 | `<postfix_expr>` | → | `long ( <expression> )` |
| 225 | `<postfix_expr>` | → | `float ( <expression> )` |
| 226 | `<postfix_expr>` | → | `double ( <expression> )` |
| 227 | `<postfix_expr>` | → | `char ( <expression> )` |
| 228 | `<postfix_expr>` | → | `string ( <expression> )` |
| 229 | `<postfix_expr>` | → | `bool ( <expression> )` |
| 230 | `<postfix_expr>` | → | `id <postfix_chain>` |
| 231 | `<postfix_expr>` | → | `intlit` |
| 232 | `<postfix_expr>` | → | `longlit` |
| 233 | `<postfix_expr>` | → | `floatlit` |
| 234 | `<postfix_expr>` | → | `doublelit` |
| 235 | `<postfix_expr>` | → | `charlit` |
| 236 | `<postfix_expr>` | → | `stringlit` |
| 237 | `<postfix_expr>` | → | `true` |
| 238 | `<postfix_expr>` | → | `false` |
| 239 | `<postfix_chain>` | → | `<array_access> <postfix_after_arr>` |
| 240 | `<postfix_chain>` | → | `. id <postfix_chain>` |
| 241 | `<postfix_chain>` | → | `( <arg_list> ) <postfix_chain>` |
| 242 | `<postfix_chain>` | → | `++` |
| 243 | `<postfix_chain>` | → | `--` |
| 244 | `<postfix_chain>` | → | `λ` |
| 245 | `<array_access>` | → | `[ <array_index> ] <array_access_dim2>` |
| 246 | `<array_access_dim2>` | → | `[ <array_index> ]` |
| 247 | `<array_access_dim2>` | → | `λ` |
| 248 | `<postfix_after_arr>` | → | `. id <postfix_chain>` |
| 249 | `<postfix_after_arr>` | → | `( <arg_list> ) <postfix_chain>` |
| 250 | `<postfix_after_arr>` | → | `++` |
| 251 | `<postfix_after_arr>` | → | `--` |
| 252 | `<postfix_after_arr>` | → | `λ` |
| 253 | `<array_index>` | → | `intlit` |
| 254 | `<array_index>` | → | `id` |
| 255 | `<arg_list>` | → | `<expression> <arg_tail>` |
| 256 | `<arg_list>` | → | `λ` |
| 257 | `<arg_tail>` | → | `, <expression> <arg_tail>` |
| 258 | `<arg_tail>` | → | `λ` |
| 259 | `<io_stmt>` | → | `trap ( <expression> ) ;` |
| 260 | `<io_stmt>` | → | `thread ( <print_args> ) ;` |
| 261 | `<io_stmt>` | → | `threadln ( <print_args> ) ;` |
| 262 | `<print_args>` | → | `<expression> <print_tail>` |
| 263 | `<print_tail>` | → | `, <expression> <print_tail>` |
| 264 | `<print_tail>` | → | `λ` |
| 265 | `<ctrl_struct>` | → | `if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` |
| 266 | `<ctrl_struct>` | → | `switch ( <expression> ) { <case_list> <default_opt> }` |
| 267 | `<ctrl_struct>` | → | `for ( <for_init> ; <for_cond> ; <for_update> ) { <ctrl_stmt_list> }` |
| 268 | `<ctrl_struct>` | → | `while ( <condition> ) { <ctrl_stmt_list> }` |
| 269 | `<ctrl_struct>` | → | `do { <ctrl_stmt_list> } while ( <condition> ) ;` |
| 270 | `<else_opt>` | → | `else <else_body>` |
| 271 | `<else_opt>` | → | `λ` |
| 272 | `<else_body>` | → | `{ <ctrl_stmt_list> }` |
| 273 | `<else_body>` | → | `if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` |
| 274 | `<case_list>` | → | `case <case_val> : <ctrl_stmt_list> <break_opt> <case_list>` |
| 275 | `<case_list>` | → | `λ` |
| 276 | `<case_val>` | → | `intlit` |
| 277 | `<case_val>` | → | `longlit` |
| 278 | `<case_val>` | → | `charlit` |
| 279 | `<case_val>` | → | `true` |
| 280 | `<case_val>` | → | `false` |
| 281 | `<default_opt>` | → | `default : <ctrl_stmt_list> <break_opt>` |
| 282 | `<default_opt>` | → | `λ` |
| 283 | `<break_opt>` | → | `break ;` |
| 284 | `<break_opt>` | → | `λ` |
| 285 | `<for_init>` | → | `local var <for_init_type> id = <for_init_expr>` |
| 286 | `<for_init>` | → | `id <for_init_assign_tail>` |
| 287 | `<for_init>` | → | `λ` |
| 288 | `<for_init_assign_tail>` | → | `<assign_op> <for_init_expr>` |
| 289 | `<for_init_expr>` | → | `<concat_expr>` |
| 290 | `<for_init_type>` | → | `int` |
| 291 | `<for_init_type>` | → | `long` |
| 292 | `<for_init_type>` | → | `float` |
| 293 | `<for_init_type>` | → | `double` |
| 294 | `<for_init_type>` | → | `char` |
| 295 | `<for_init_type>` | → | `string` |
| 296 | `<for_init_type>` | → | `bool` |
| 297 | `<for_cond>` | → | `<condition>` |
| 298 | `<for_cond>` | → | `λ` |
| 299 | `<for_update>` | → | `id <for_update_tail>` |
| 300 | `<for_update>` | → | `++ id` |
| 301 | `<for_update>` | → | `-- id` |
| 302 | `<for_update>` | → | `λ` |
| 303 | `<for_update_tail>` | → | `++` |
| 304 | `<for_update_tail>` | → | `--` |
| 305 | `<for_update_tail>` | → | `<assign_op> <expression>` |
| 306 | `<condition>` | → | `<cond_or>` |
| 307 | `<cond_or>` | → | `<cond_and> <cond_or_tail>` |
| 308 | `<cond_or_tail>` | → | `\|\| <cond_and> <cond_or_tail>` |
| 309 | `<cond_or_tail>` | → | `λ` |
| 310 | `<cond_and>` | → | `<cond_not> <cond_and_tail>` |
| 311 | `<cond_and_tail>` | → | `&& <cond_not> <cond_and_tail>` |
| 312 | `<cond_and_tail>` | → | `λ` |
| 313 | `<cond_not>` | → | `! <cond_not>` |
| 314 | `<cond_not>` | → | `<cond_atom>` |
| 315 | `<cond_rhs_expr>` | → | `<concat_expr>` |
| 316 | `<cond_atom>` | → | `true` |
| 317 | `<cond_atom>` | → | `false` |
| 318 | `<cond_atom>` | → | `( <condition> )` |
| 319 | `<cond_atom>` | → | `id <cond_after_id>` |
| 320 | `<cond_atom>` | → | `intlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 321 | `<cond_atom>` | → | `longlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 322 | `<cond_atom>` | → | `floatlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 323 | `<cond_atom>` | → | `doublelit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 324 | `<cond_atom>` | → | `charlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 325 | `<cond_atom>` | → | `stringlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 326 | `<cond_atom>` | → | `int ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 327 | `<cond_atom>` | → | `long ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 328 | `<cond_atom>` | → | `float ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 329 | `<cond_atom>` | → | `double ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 330 | `<cond_atom>` | → | `char ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 331 | `<cond_atom>` | → | `string ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 332 | `<cond_atom>` | → | `bool ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 333 | `<cond_after_id>` | → | `( <arg_list> ) <cond_after_call>` |
| 334 | `<cond_after_id>` | → | `<cond_after_id_no_call> <cond_comparison_opt>` |
| 335 | `<cond_after_call>` | → | `λ` |
| 336 | `<cond_after_call>` | → | `<postfix_chain> <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| 337 | `<cond_after_id_no_call>` | → | `<cond_postfix_no_call> <mul_tail> <add_tail>` |
| 338 | `<cond_comparison_opt>` | → | `<comp_op> <cond_rhs_expr>` |
| 339 | `<cond_comparison_opt>` | → | `λ` |
| 340 | `<cond_postfix_no_call>` | → | `[ <array_index> ] <array_access_dim2> <postfix_after_arr>` |
| 341 | `<cond_postfix_no_call>` | → | `. id <postfix_chain>` |
| 342 | `<cond_postfix_no_call>` | → | `++` |
| 343 | `<cond_postfix_no_call>` | → | `--` |
| 344 | `<cond_postfix_no_call>` | → | `λ` |
| 345 | `<comp_op>` | → | `==` |
| 346 | `<comp_op>` | → | `!=` |
| 347 | `<comp_op>` | → | `<` |
| 348 | `<comp_op>` | → | `>` |
| 349 | `<comp_op>` | → | `<=` |
| 350 | `<comp_op>` | → | `>=` |
| 351 | `<main_body>` | → | `<main_content>` |
| 352 | `<main_content>` | → | `using id <using_cont> ; <main_content>` |
| 353 | `<main_content>` | → | `local <mutability> <local_dec_body> <main_content>` |
| 354 | `<main_content>` | → | `<statement_non_return> <main_content>` |
| 355 | `<main_content>` | → | `return intlit ;` |
