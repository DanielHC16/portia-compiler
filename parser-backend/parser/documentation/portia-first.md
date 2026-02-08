## FIRST Set

| # | Production | → | FIRST Set |
|---|------------|---|-----------|
| 1 | `<program>` | → | `{ bool, char, double, float, func, global, id, int, long, string, weave }` |
| 2 | `<decl_list>` | → | `{ bool, char, double, float, func, global, id, int, long, string, weave }` |
| 3 | `<int_decl_or_main>` | → | `{ id, main }` |
| 4 | `<other_decl>` | → | `{ bool, char, double, float, func, global, id, long, string, weave }` |
| 5 | `<main_func>` | → | `{ int }` |
| 6 | `<multi_global>` | → | `{ ,, λ }` |
| 7 | `<weave_inst_decl>` | → | `{ [, id }` |
| 8 | `<weave_inst_tail>` | → | `{ =, [ }` |
| 9 | `<weave_field_value>` | → | `{ {, charlit, doublelit, false, floatlit, intlit, longlit, stringlit, true }` |
| 10 | `<weave_arr_content>` | → | `{ {, bool, char, charlit, double, doublelit, false, float, floatlit, int, intlit, long, longlit, string, stringlit, true, λ }` |
| 11 | `<weave_field_list_tail>` | → | `{ ,, λ }` |
| 12 | `<weave_inst_cont>` | → | `{ ,, λ }` |
| 13 | `<weave_arr_cont>` | → | `{ ,, λ }` |
| 14 | `<typed_decl_tail>` | → | `{ =, [ }` |
| 15 | `<multi_typed>` | → | `{ ,, λ }` |
| 16 | `<mutability>` | → | `{ const, var }` |
| 17 | `<dtype>` | → | `{ bool, char, double, float, int, long, string }` |
| 18 | `<value>` | → | `{ charlit, doublelit, false, floatlit, intlit, longlit, stringlit, true }` |
| 19 | `<value_list_tail>` | → | `{ ,, λ }` |
| 20 | `<array_dims>` | → | `{ [ }` |
| 21 | `<array_dim2_opt>` | → | `{ [, λ }` |
| 22 | `<array_with_init>` | → | `{ [ }` |
| 23 | `<array_init_tail>` | → | `{ =, [, λ }` |
| 24 | `<arr_init_opt_1d>` | → | `{ =, λ }` |
| 25 | `<arr_init_content_1d>` | → | `{ bool, char, charlit, double, doublelit, false, float, floatlit, int, intlit, long, longlit, string, stringlit, true, λ }` |
| 26 | `<arr_init_opt_2d>` | → | `{ =, λ }` |
| 27 | `<arr_init_content_2d>` | → | `{ {, λ }` |
| 28 | `<elem_2d_tail>` | → | `{ ,, λ }` |
| 29 | `<elem_list>` | → | `{ bool, char, charlit, double, doublelit, false, float, floatlit, int, intlit, long, longlit, string, stringlit, true, λ }` |
| 30 | `<elem_1d_tail>` | → | `{ ,, λ }` |
| 31 | `<arr_elem>` | → | `{ bool, char, charlit, double, doublelit, false, float, floatlit, int, intlit, long, longlit, string, stringlit, true }` |
| 32 | `<size>` | → | `{ id, intlit }` |
| 33 | `<field_list>` | → | `{ bool, char, double, float, id, int, long, string, λ }` |
| 34 | `<field_dec>` | → | `{ bool, char, double, float, id, int, long, string }` |
| 35 | `<field_type>` | → | `{ bool, char, double, float, id, int, long, string }` |
| 36 | `<field_arr_opt>` | → | `{ [, λ }` |
| 37 | `<field_cont>` | → | `{ ,, λ }` |
| 38 | `<nonvoid_ret_type>` | → | `{ bool, char, double, float, id, int, long, string }` |
| 39 | `<ret_type_suffix>` | → | `{ [, λ }` |
| 40 | `<ret_id_suffix>` | → | `{ ., [, λ }` |
| 41 | `<param_list>` | → | `{ bool, char, double, float, id, int, long, string, λ }` |
| 42 | `<param_type>` | → | `{ bool, char, double, float, id, int, long, string }` |
| 43 | `<param_arr_opt>` | → | `{ [, λ }` |
| 44 | `<param_cont>` | → | `{ ,, λ }` |
| 45 | `<function_body_nonvoid>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 46 | `<func_content_nonvoid>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 47 | `<function_body_void>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 48 | `<func_content_void>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 49 | `<using_block>` | → | `{ using, λ }` |
| 50 | `<using_cont>` | → | `{ ,, λ }` |
| 51 | `<local_block>` | → | `{ local, λ }` |
| 52 | `<local_dec_body>` | → | `{ bool, char, double, float, id, int, long, string }` |
| 53 | `<typed_local_tail>` | → | `{ =, [ }` |
| 54 | `<multi_local>` | → | `{ ,, λ }` |
| 55 | `<weave_local_tail>` | → | `{ =, [ }` |
| 56 | `<statement_non_return>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, string, stringlit, switch, thread, threadln, trap, true, while }` |
| 57 | `<ctrl_stmt_list>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, long, longlit, string, stringlit, switch, thread, threadln, trap, true, while, λ }` |
| 58 | `<expression>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 59 | `<assign_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 60 | `<assign_tail>` | → | `{ %=, *=, +=, -=, /=, =, λ }` |
| 61 | `<assign_op>` | → | `{ %=, *=, +=, -=, /=, = }` |
| 62 | `<concat_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 63 | `<concat_tail>` | → | `{ .., λ }` |
| 64 | `<or_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 65 | `<or_tail>` | → | `{ \|\|, λ }` |
| 66 | `<and_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 67 | `<and_tail>` | → | `{ &&, λ }` |
| 68 | `<eq_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 69 | `<eq_tail>` | → | `{ !=, ==, λ }` |
| 70 | `<rel_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 71 | `<rel_tail>` | → | `{ <, <=, >, >=, λ }` |
| 72 | `<add_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 73 | `<add_tail>` | → | `{ +, -, λ }` |
| 74 | `<mul_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 75 | `<mul_tail>` | → | `{ %, *, /, λ }` |
| 76 | `<unary_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 77 | `<postfix_expr>` | → | `{ (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 78 | `<postfix_chain>` | → | `{ (, ++, --, ., [, λ }` |
| 79 | `<array_access>` | → | `{ [ }` |
| 80 | `<array_access_dim2>` | → | `{ [, λ }` |
| 81 | `<postfix_after_arr>` | → | `{ (, ++, --, ., λ }` |
| 82 | `<array_index>` | → | `{ id, intlit }` |
| 83 | `<arg_list>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true, λ }` |
| 84 | `<arg_tail>` | → | `{ ,, λ }` |
| 85 | `<io_stmt>` | → | `{ thread, threadln, trap }` |
| 86 | `<print_args>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 87 | `<print_tail>` | → | `{ ,, λ }` |
| 88 | `<ctrl_struct>` | → | `{ do, for, if, switch, while }` |
| 89 | `<else_opt>` | → | `{ else, λ }` |
| 90 | `<else_body>` | → | `{ {, if }` |
| 91 | `<case_list>` | → | `{ case, λ }` |
| 92 | `<case_val>` | → | `{ charlit, false, intlit, longlit, true }` |
| 93 | `<default_opt>` | → | `{ default, λ }` |
| 94 | `<break_opt>` | → | `{ break, λ }` |
| 95 | `<for_init>` | → | `{ id, local, λ }` |
| 96 | `<for_init_assign_tail>` | → | `{ %=, *=, +=, -=, /=, = }` |
| 97 | `<for_init_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 98 | `<for_init_type>` | → | `{ bool, char, double, float, int, long, string }` |
| 99 | `<for_cond>` | → | `{ !, (, id, int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, λ }` |
| 100 | `<for_update>` | → | `{ ++, --, id, λ }` |
| 101 | `<for_update_tail>` | → | `{ %=, *=, ++, +=, --, -=, /=, = }` |
| 102 | `<condition>` | → | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 103 | `<cond_or>` | → | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 104 | `<cond_or_tail>` | → | `{ \|\|, λ }` |
| 105 | `<cond_and>` | → | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 106 | `<cond_and_tail>` | → | `{ &&, λ }` |
| 107 | `<cond_not>` | → | `{ !, (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 108 | `<cond_atom>` | → | `{ (, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 109 | `<cond_rhs_expr>` | → | `{ !, (, ++, --, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true }` |
| 110 | `<cond_after_id>` | → | `{ !, (, ++, --, ., <, <=, ==, >, >=, [, λ }` |
| 111 | `<cond_after_call>` | → | `{ (, ++, --, ., [, λ }` |
| 112 | `<cond_after_id_no_call>` | → | `{ ++, --, ., [, λ }` |
| 113 | `<cond_comparison_opt>` | → | `{ !=, <, <=, ==, >, >=, λ }` |
| 114 | `<cond_postfix_no_call>` | → | `{ ++, --, ., [, λ }` |
| 115 | `<comp_op>` | → | `{ !=, <, <=, ==, >, >= }` |
| 116 | `<main_body>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
| 117 | `<main_content>` | → | `{ !, (, ++, --, bool, break, char, charlit, do, double, doublelit, false, float, floatlit, for, id, if, int, intlit, local, long, longlit, return, string, stringlit, switch, thread, threadln, trap, true, using, while }` |
