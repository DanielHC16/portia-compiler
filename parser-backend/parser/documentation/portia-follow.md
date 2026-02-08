## FOLLOW Set

| # | Production | → | FOLLOW Set |
|---|------------|---|------------|
| 1 | `<program>` | → | `{ $END }` |
| 2 | `<decl_list>` | → | `{ $END }` |
| 3 | `<int_decl_or_main>` | → | `{ $END }` |
| 4 | `<other_decl>` | → | `{ bool, char, double, float, func, global, id, int, long, string, weave }` |
| 5 | `<main_func>` | → | `{ $END }` |
| 6 | `<multi_global>` | → | `{ ; }` |
| 7 | `<weave_inst_decl>` | → | `{ bool, char, double, float, func, global, id, int, long, string, weave }` |
| 8 | `<weave_inst_tail>` | → | `{ ,, ; }` |
| 9 | `<weave_field_value>` | → | `{ ,, } }` |
| 10 | `<weave_arr_content>` | → | `{ } }` |
| 11 | `<weave_field_list_tail>` | → | `{ } }` |
| 12 | `<weave_inst_cont>` | → | `{ ; }` |
| 13 | `<weave_arr_cont>` | → | `{ ; }` |
| 14 | `<typed_decl_tail>` | → | `{ bool, char, double, float, func, global, id, int, long, string, weave }` |
| 15 | `<multi_typed>` | → | `{ ; }` |
| 16 | `<mutability>` | → | `{ bool, char, double, float, id, int, long, string }` |
| 17 | `<dtype>` | → | `{ id }` |
| 18 | `<value>` | → | `{ ) }` |
| 19 | `<value_list_tail>` | → | `{ ) }` |
| 20 | `<array_dims>` | → | `{ ,, ;, id }` |
| 21 | `<array_dim2_opt>` | → | `{ ,, ;, id }` |
| 22 | `<array_with_init>` | → | `{ ,, ; }` |
| 23 | `<array_init_tail>` | → | `{ ,, ; }` |
| 24 | `<arr_init_opt_1d>` | → | `{ ,, ; }` |
| 25 | `<arr_init_content_1d>` | → | `{ } }` |
| 26 | `<arr_init_opt_2d>` | → | `{ ,, ; }` |
| 27 | `<arr_init_content_2d>` | → | `{ } }` |
| 28 | `<elem_2d_tail>` | → | `{ } }` |
| 29 | `<elem_list>` | → | `{ } }` |
| 30 | `<elem_1d_tail>` | → | `{ } }` |
| 31 | `<arr_elem>` | → | `{ ,, } }` |
| 32 | `<size>` | → | `{ ] }` |
| 33 | `<field_list>` | → | `{ } }` |
| 34 | `<field_dec>` | → | `{ bool, char, double, float, id, int, long, string, } }` |
| 35 | `<field_type>` | → | `{ id }` |
| 36 | `<field_arr_opt>` | → | `{ ,, ; }` |
| 37 | `<field_cont>` | → | `{ ; }` |
| 38 | `<nonvoid_ret_type>` | → | `{ id }` |
| 39 | `<ret_type_suffix>` | → | `{ id }` |
| 40 | `<ret_id_suffix>` | → | `{ id }` |
| 41 | `<param_list>` | → | `{ ) }` |
| 42 | `<param_type>` | → | `{ id }` |
| 43 | `<param_arr_opt>` | → | `{ ,, ) }` |
| 44 | `<param_cont>` | → | `{ ) }` |
| 45 | `<function_body_nonvoid>` | → | `{ } }` |
| 46 | `<func_content_nonvoid>` | → | `{ } }` |
| 47 | `<function_body_void>` | → | `{ } }` |
| 48 | `<func_content_void>` | → | `{ } }` |
| 49 | `<using_block>` | → | `{ local }` |
| 50 | `<using_cont>` | → | `{ ; }` |
| 51 | `<local_block>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, while }` |
| 52 | `<local_dec_body>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 53 | `<typed_local_tail>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 54 | `<multi_local>` | → | `{ ; }` |
| 55 | `<weave_local_tail>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 56 | `<statement_non_return>` | → | `{ !, (, ++, --, bool, break, case, char, charlit, default, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while, } }` |
| 57 | `<ctrl_stmt_list>` | → | `{ case, default, }, while }` |
| 58 | `<expression>` | → | `{ ), ,, ; }` |
| 59 | `<assign_expr>` | → | `{ ), ,, ; }` |
| 60 | `<assign_tail>` | → | `{ ), ,, ; }` |
| 61 | `<assign_op>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 62 | `<concat_expr>` | → | `{ ), ,, ;, %=, *=, +=, -=, /=, = }` |
| 63 | `<concat_tail>` | → | `{ ), ,, ;, %=, *=, +=, -=, /=, = }` |
| 64 | `<or_expr>` | → | `{ ), ,, .., ;, %=, *=, +=, -=, /=, = }` |
| 65 | `<or_tail>` | → | `{ ), ,, .., ;, %=, *=, +=, -=, /=, = }` |
| 66 | `<and_expr>` | → | `{ ), ,, .., ;, %=, *=, +=, -=, /=, =, \|\| }` |
| 67 | `<and_tail>` | → | `{ ), ,, .., ;, %=, *=, +=, -=, /=, =, \|\| }` |
| 68 | `<eq_expr>` | → | `{ &&, ), ,, .., ;, %=, *=, +=, -=, /=, =, \|\| }` |
| 69 | `<eq_tail>` | → | `{ &&, ), ,, .., ;, %=, *=, +=, -=, /=, =, \|\| }` |
| 70 | `<rel_expr>` | → | `{ !=, &&, ), ,, .., ;, %=, *=, +=, -=, /=, =, ==, \|\| }` |
| 71 | `<rel_tail>` | → | `{ !=, &&, ), ,, .., ;, %=, *=, +=, -=, /=, =, ==, \|\| }` |
| 72 | `<add_expr>` | → | `{ !=, &&, ), ,, .., ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 73 | `<add_tail>` | → | `{ !=, &&, ), ,, .., ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 74 | `<mul_expr>` | → | `{ !, !=, &&, ), +, ,, -, .., ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 75 | `<mul_tail>` | → | `{ !, !=, &&, ), +, ,, -, .., ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 76 | `<unary_expr>` | → | `{ %, !, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 77 | `<postfix_expr>` | → | `{ %, !, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 78 | `<postfix_chain>` | → | `{ %, !, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 79 | `<array_access>` | → | `{ (, ++, --, ., %, !, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 80 | `<array_access_dim2>` | → | `{ (, ++, --, ., %, !, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 81 | `<postfix_after_arr>` | → | `{ %, !, !=, &&, *, ), +, ,, -, .., /, ;, <, <=, %=, *=, +=, -=, /=, =, ==, >, >=, \|\| }` |
| 82 | `<array_index>` | → | `{ ] }` |
| 83 | `<arg_list>` | → | `{ ) }` |
| 84 | `<arg_tail>` | → | `{ ) }` |
| 85 | `<io_stmt>` | → | `{ !, (, ++, --, bool, break, case, char, charlit, default, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while, } }` |
| 86 | `<print_args>` | → | `{ ) }` |
| 87 | `<print_tail>` | → | `{ ) }` |
| 88 | `<ctrl_struct>` | → | `{ !, (, ++, --, bool, break, case, char, charlit, default, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while, } }` |
| 89 | `<else_opt>` | → | `{ !, (, ++, --, bool, break, case, char, charlit, default, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while, } }` |
| 90 | `<else_body>` | → | `{ !, (, ++, --, bool, break, case, char, charlit, default, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while, } }` |
| 91 | `<case_list>` | → | `{ default, } }` |
| 92 | `<case_val>` | → | `{ : }` |
| 93 | `<default_opt>` | → | `{ } }` |
| 94 | `<break_opt>` | → | `{ case, default, } }` |
| 95 | `<for_init>` | → | `{ ; }` |
| 96 | `<for_init_assign_tail>` | → | `{ ; }` |
| 97 | `<for_init_expr>` | → | `{ ; }` |
| 98 | `<for_init_type>` | → | `{ id }` |
| 99 | `<for_cond>` | → | `{ ; }` |
| 100 | `<for_update>` | → | `{ ) }` |
| 101 | `<for_update_tail>` | → | `{ ) }` |
| 102 | `<condition>` | → | `{ ) }` |
| 103 | `<cond_or>` | → | `{ ) }` |
| 104 | `<cond_or_tail>` | → | `{ ) }` |
| 105 | `<cond_and>` | → | `{ ), \|\| }` |
| 106 | `<cond_and_tail>` | → | `{ ), \|\| }` |
| 107 | `<cond_not>` | → | `{ &&, ), \|\| }` |
| 108 | `<cond_atom>` | → | `{ &&, ), \|\| }` |
| 109 | `<cond_rhs_expr>` | → | `{ &&, ), \|\| }` |
| 110 | `<cond_after_id>` | → | `{ &&, ), \|\| }` |
| 111 | `<cond_after_call>` | → | `{ &&, ), \|\| }` |
| 112 | `<cond_after_id_no_call>` | → | `{ !=, <, <=, ==, >, >=, &&, ), \|\| }` |
| 113 | `<cond_comparison_opt>` | → | `{ &&, ), \|\| }` |
| 114 | `<cond_postfix_no_call>` | → | `{ %, *, +, -, / }` |
| 115 | `<comp_op>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 116 | `<main_body>` | → | `{ } }` |
| 117 | `<main_content>` | → | `{ } }` |
