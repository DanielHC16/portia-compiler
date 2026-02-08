# PORTIA LL(1) Grammar Verification Document

## 1. Terminals

```
global, local, func, return, if, else, switch, case, default, for, while, do, break,
trap, thread, threadln, using, weave, main, int, long, float, double, char, string,
bool, void, var, const, true, false, id, intlit, longlit, floatlit, doublelit,
charlit, stringlit, =, +=, -=, *=, /=, %=, ==, !=, <, >, <=, >=, &&, ||, !,
+, -, *, /, %, ++, --, .., (, ), {, }, [, ], ;, ,, :, ., $END
```

---

## 2. Context-Free Grammar (CFG)

### Program Structure

| Non-terminal | Productions |
|--------------|-------------|
| `<program>` | `<decl_list>` |
| `<decl_list>` | `int <int_decl_or_main>` \| `<other_decl> <decl_list>` |
| `<int_decl_or_main>` | `id <typed_decl_tail> <decl_list>` \| `main ( ) { <main_body> } $END` |
| `<other_decl>` | `global <mutability> <dtype> id = <expression> <multi_global> ;` \| `long id <typed_decl_tail>` \| `float id <typed_decl_tail>` \| `double id <typed_decl_tail>` \| `char id <typed_decl_tail>` \| `string id <typed_decl_tail>` \| `bool id <typed_decl_tail>` \| `weave id { <field_list> } ;` \| `id <weave_inst_decl>` \| `func <nonvoid_ret_type> id ( <param_list> ) { <function_body_nonvoid> }` \| `func void id ( <param_list> ) { <function_body_void> }` |
| `<main_func>` | `int main ( ) { <main_body> }` |
| `<multi_global>` | `, id = <expression> <multi_global>` \| `λ` |
| `<weave_inst_decl>` | `id <weave_inst_tail> <weave_inst_cont> ;` \| `<array_with_init> <weave_arr_cont> ;` |
| `<weave_inst_tail>` | `= { <weave_field_value> <weave_field_list_tail> }` \| `<array_with_init>` |
| `<weave_field_value>` | `intlit` \| `longlit` \| `floatlit` \| `doublelit` \| `charlit` \| `stringlit` \| `true` \| `false` \| `{ <weave_arr_content> }` |
| `<weave_arr_content>` | `{ <elem_list> } <elem_2d_tail>` \| `<arr_elem> <elem_1d_tail>` \| `λ` |
| `<weave_field_list_tail>` | `, <weave_field_value> <weave_field_list_tail>` \| `λ` |
| `<weave_inst_cont>` | `, id <weave_inst_tail> <weave_inst_cont>` \| `λ` |
| `<weave_arr_cont>` | `, id <array_with_init> <weave_arr_cont>` \| `λ` |
| `<typed_decl_tail>` | `<array_with_init> ;` \| `= <expression> <multi_typed> ;` |
| `<multi_typed>` | `, id = <expression> <multi_typed>` \| `λ` |

### Mutability & Types

| Non-terminal | Productions |
|--------------|-------------|
| `<mutability>` | `var` \| `const` |
| `<dtype>` | `int` \| `long` \| `float` \| `double` \| `char` \| `string` \| `bool` |

### Values & Literals

| Non-terminal | Productions |
|--------------|-------------|
| `<value>` | `intlit` \| `longlit` \| `floatlit` \| `doublelit` \| `charlit` \| `stringlit` \| `true` \| `false` |
| `<value_list_tail>` | `, <value> <value_list_tail>` \| `λ` |

### Array Dimensions

| Non-terminal | Productions |
|--------------|-------------|
| `<array_dims>` | `[ <size> ] <array_dim2_opt>` |
| `<array_dim2_opt>` | `[ <size> ]` \| `λ` |
| `<array_with_init>` | `[ <size> ] <array_init_tail>` |
| `<array_init_tail>` | `[ <size> ] <arr_init_opt_2d>` \| `<arr_init_opt_1d>` |

### Array Declarations

| Non-terminal | Productions |
|--------------|-------------|
| `<arr_init_opt_1d>` | `= { <arr_init_content_1d> }` \| `λ` |
| `<arr_init_content_1d>` | `<arr_elem> <elem_1d_tail>` \| `λ` |
| `<arr_init_opt_2d>` | `= { <arr_init_content_2d> }` \| `λ` |
| `<arr_init_content_2d>` | `{ <elem_list> } <elem_2d_tail>` \| `λ` |
| `<elem_2d_tail>` | `, { <elem_list> } <elem_2d_tail>` \| `λ` |
| `<elem_list>` | `<arr_elem> <elem_1d_tail>` \| `λ` |
| `<elem_1d_tail>` | `, <arr_elem> <elem_1d_tail>` \| `λ` |
| `<arr_elem>` | `int ( <value> )` \| `long ( <value> )` \| `float ( <value> )` \| `double ( <value> )` \| `char ( <value> )` \| `string ( <value> )` \| `bool ( <value> )` \| `intlit` \| `longlit` \| `floatlit` \| `doublelit` \| `charlit` \| `stringlit` \| `true` \| `false` |
| `<size>` | `intlit` \| `id` |

### Weave (Struct) Definitions

| Non-terminal | Productions |
|--------------|-------------|
| `<field_list>` | `<field_dec> <field_list>` \| `λ` |
| `<field_dec>` | `<field_type> id <field_arr_opt> <field_cont> ;` |
| `<field_type>` | `int` \| `long` \| `float` \| `double` \| `char` \| `string` \| `bool` \| `id` |
| `<field_arr_opt>` | `<array_dims>` \| `λ` |
| `<field_cont>` | `, id <field_arr_opt> <field_cont>` \| `λ` |

### Functions

| Non-terminal | Productions |
|--------------|-------------|
| `<nonvoid_ret_type>` | `int <ret_type_suffix>` \| `long <ret_type_suffix>` \| `float <ret_type_suffix>` \| `double <ret_type_suffix>` \| `char <ret_type_suffix>` \| `string <ret_type_suffix>` \| `bool <ret_type_suffix>` \| `id <ret_id_suffix>` |
| `<ret_type_suffix>` | `<array_dims>` \| `λ` |
| `<ret_id_suffix>` | `<array_dims>` \| `. id` \| `λ` |
| `<param_list>` | `<param_type> id <param_arr_opt> <param_cont>` \| `λ` |
| `<param_type>` | `int` \| `long` \| `float` \| `double` \| `char` \| `string` \| `bool` \| `id` |
| `<param_arr_opt>` | `<array_dims>` \| `λ` |
| `<param_cont>` | `, <param_type> id <param_arr_opt> <param_cont>` \| `λ` |
| `<function_body_nonvoid>` | `<func_content_nonvoid>` |
| `<func_content_nonvoid>` | `using id <using_cont> ; <func_content_nonvoid>` \| `local <mutability> <local_dec_body> <func_content_nonvoid>` \| `<statement_non_return> <func_content_nonvoid>` \| `return <expression> ;` |
| `<function_body_void>` | `<func_content_void>` |
| `<func_content_void>` | `using id <using_cont> ; <func_content_void>` \| `local <mutability> <local_dec_body> <func_content_void>` \| `<statement_non_return> <func_content_void>` \| `return ;` |

### Using Block

| Non-terminal | Productions |
|--------------|-------------|
| `<using_block>` | `using id <using_cont> ; <using_block>` \| `λ` |
| `<using_cont>` | `, id <using_cont>` \| `λ` |

### Local Declarations

| Non-terminal | Productions |
|--------------|-------------|
| `<local_block>` | `local <mutability> <local_dec_body> <local_block>` \| `λ` |
| `<local_dec_body>` | `int id <typed_local_tail>` \| `long id <typed_local_tail>` \| `float id <typed_local_tail>` \| `double id <typed_local_tail>` \| `char id <typed_local_tail>` \| `string id <typed_local_tail>` \| `bool id <typed_local_tail>` \| `id id <weave_local_tail>` |
| `<typed_local_tail>` | `<array_with_init> ;` \| `= <expression> <multi_local> ;` |
| `<multi_local>` | `, id = <expression> <multi_local>` \| `λ` |
| `<weave_local_tail>` | `= { <weave_field_value> <weave_field_list_tail> } <weave_inst_cont> ;` \| `<array_with_init> <weave_arr_cont> ;` |

### Statements

| Non-terminal | Productions |
|--------------|-------------|
| `<statement_non_return>` | `<expression> ;` \| `<io_stmt>` \| `<ctrl_struct>` \| `break ;` |
| `<ctrl_stmt_list>` | `<statement_non_return> <ctrl_stmt_list>` \| `λ` |

### Expressions

| Non-terminal | Productions |
|--------------|-------------|
| `<expression>` | `<assign_expr>` |
| `<assign_expr>` | `<concat_expr> <assign_tail>` |
| `<assign_tail>` | `<assign_op> <assign_expr>` \| `λ` |
| `<assign_op>` | `=` \| `+=` \| `-=` \| `*=` \| `/=` \| `%=` |
| `<concat_expr>` | `<or_expr> <concat_tail>` |
| `<concat_tail>` | `.. <or_expr> <concat_tail>` \| `λ` |

### Boolean / Logical Expressions

| Non-terminal | Productions |
|--------------|-------------|
| `<or_expr>` | `<and_expr> <or_tail>` |
| `<or_tail>` | `\|\| <and_expr> <or_tail>` \| `λ` |
| `<and_expr>` | `<eq_expr> <and_tail>` |
| `<and_tail>` | `&& <eq_expr> <and_tail>` \| `λ` |
| `<eq_expr>` | `<rel_expr> <eq_tail>` |
| `<eq_tail>` | `== <rel_expr> <eq_tail>` \| `!= <rel_expr> <eq_tail>` \| `λ` |
| `<rel_expr>` | `<add_expr> <rel_tail>` |
| `<rel_tail>` | `< <add_expr>` \| `> <add_expr>` \| `<= <add_expr>` \| `>= <add_expr>` \| `λ` |

### Arithmetic Expressions

| Non-terminal | Productions |
|--------------|-------------|
| `<add_expr>` | `<mul_expr> <add_tail>` |
| `<add_tail>` | `+ <mul_expr> <add_tail>` \| `- <mul_expr> <add_tail>` \| `λ` |
| `<mul_expr>` | `<unary_expr> <mul_tail>` |
| `<mul_tail>` | `* <unary_expr> <mul_tail>` \| `/ <unary_expr> <mul_tail>` \| `% <unary_expr> <mul_tail>` \| `λ` |
| `<unary_expr>` | `! <unary_expr>` \| `++ <unary_expr>` \| `-- <unary_expr>` \| `<postfix_expr>` |
| `<postfix_expr>` | `( <expression> ) <postfix_chain>` \| `int ( <expression> )` \| `long ( <expression> )` \| `float ( <expression> )` \| `double ( <expression> )` \| `char ( <expression> )` \| `string ( <expression> )` \| `bool ( <expression> )` \| `id <postfix_chain>` \| `intlit` \| `longlit` \| `floatlit` \| `doublelit` \| `charlit` \| `stringlit` \| `true` \| `false` |

### Postfix Chain

| Non-terminal | Productions |
|--------------|-------------|
| `<postfix_chain>` | `<array_access> <postfix_after_arr>` \| `. id <postfix_chain>` \| `( <arg_list> ) <postfix_chain>` \| `++` \| `--` \| `λ` |
| `<array_access>` | `[ <array_index> ] <array_access_dim2>` |
| `<array_access_dim2>` | `[ <array_index> ]` \| `λ` |
| `<postfix_after_arr>` | `. id <postfix_chain>` \| `( <arg_list> ) <postfix_chain>` \| `++` \| `--` \| `λ` |
| `<array_index>` | `intlit` \| `id` |
| `<arg_list>` | `<expression> <arg_tail>` \| `λ` |
| `<arg_tail>` | `, <expression> <arg_tail>` \| `λ` |

### I/O Statements

| Non-terminal | Productions |
|--------------|-------------|
| `<io_stmt>` | `trap ( <expression> ) ;` \| `thread ( <print_args> ) ;` \| `threadln ( <print_args> ) ;` |
| `<print_args>` | `<expression> <print_tail>` |
| `<print_tail>` | `, <expression> <print_tail>` \| `λ` |

### Control Structures

| Non-terminal | Productions |
|--------------|-------------|
| `<ctrl_struct>` | `if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` \| `switch ( <expression> ) { <case_list> <default_opt> }` \| `for ( <for_init> ; <for_cond> ; <for_update> ) { <ctrl_stmt_list> }` \| `while ( <condition> ) { <ctrl_stmt_list> }` \| `do { <ctrl_stmt_list> } while ( <condition> ) ;` |
| `<else_opt>` | `else <else_body>` \| `λ` |
| `<else_body>` | `{ <ctrl_stmt_list> }` \| `if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` |
| `<case_list>` | `case <case_val> : <ctrl_stmt_list> <break_opt> <case_list>` \| `λ` |
| `<case_val>` | `intlit` \| `longlit` \| `charlit` \| `true` \| `false` |
| `<default_opt>` | `default : <ctrl_stmt_list> <break_opt>` \| `λ` |
| `<break_opt>` | `break ;` \| `λ` |

### For Loop

| Non-terminal | Productions |
|--------------|-------------|
| `<for_init>` | `local var <for_init_type> id = <for_init_expr>` \| `id <for_init_assign_tail>` \| `λ` |
| `<for_init_assign_tail>` | `<assign_op> <for_init_expr>` |
| `<for_init_expr>` | `<concat_expr>` |
| `<for_init_type>` | `int` \| `long` \| `float` \| `double` \| `char` \| `string` \| `bool` |
| `<for_cond>` | `<condition>` \| `λ` |
| `<for_update>` | `id <for_update_tail>` \| `++ id` \| `-- id` \| `λ` |
| `<for_update_tail>` | `++` \| `--` \| `<assign_op> <expression>` |

### Condition Expressions

| Non-terminal | Productions |
|--------------|-------------|
| `<condition>` | `<cond_or>` |
| `<cond_or>` | `<cond_and> <cond_or_tail>` |
| `<cond_or_tail>` | `\|\| <cond_and> <cond_or_tail>` \| `λ` |
| `<cond_and>` | `<cond_not> <cond_and_tail>` |
| `<cond_and_tail>` | `&& <cond_not> <cond_and_tail>` \| `λ` |
| `<cond_not>` | `! <cond_not>` \| `<cond_atom>` |
| `<cond_rhs_expr>` | `<concat_expr>` |
| `<cond_atom>` | `true` \| `false` \| `( <condition> )` \| `id <cond_after_id>` \| `intlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `longlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `floatlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `doublelit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `charlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `stringlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `int ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `long ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `float ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `double ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `char ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `string ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` \| `bool ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| `<cond_after_id>` | `( <arg_list> ) <cond_after_call>` \| `<cond_after_id_no_call> <cond_comparison_opt>` |
| `<cond_after_call>` | `λ` \| `<postfix_chain> <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` |
| `<cond_after_id_no_call>` | `<cond_postfix_no_call> <mul_tail> <add_tail>` |
| `<cond_comparison_opt>` | `<comp_op> <cond_rhs_expr>` \| `λ` |
| `<cond_postfix_no_call>` | `[ <array_index> ] <array_access_dim2> <postfix_after_arr>` \| `. id <postfix_chain>` \| `++` \| `--` \| `λ` |
| `<comp_op>` | `==` \| `!=` \| `<` \| `>` \| `<=` \| `>=` |

### Main Function Body

| Non-terminal | Productions |
|--------------|-------------|
| `<main_body>` | `<main_content>` |
| `<main_content>` | `using id <using_cont> ; <main_content>` \| `local <mutability> <local_dec_body> <main_content>` \| `<statement_non_return> <main_content>` \| `return intlit ;` |

---

## 3. FIRST Sets

| Non-terminal | FIRST Set |
|--------------|-----------|
| `<program>` | { int, global, long, float, double, char, string, bool, weave, id, func } |
| `<decl_list>` | { int, global, long, float, double, char, string, bool, weave, id, func } |
| `<int_decl_or_main>` | { id, main } |
| `<other_decl>` | { global, long, float, double, char, string, bool, weave, id, func } |
| `<main_func>` | { int } |
| `<multi_global>` | { ,, λ } |
| `<weave_inst_decl>` | { id, [ } |
| `<weave_inst_tail>` | { =, [ } |
| `<weave_field_value>` | { intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, { } |
| `<weave_arr_content>` | { {, int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, λ } |
| `<weave_field_list_tail>` | { ,, λ } |
| `<weave_inst_cont>` | { ,, λ } |
| `<weave_arr_cont>` | { ,, λ } |
| `<typed_decl_tail>` | { [, = } |
| `<multi_typed>` | { ,, λ } |
| `<mutability>` | { var, const } |
| `<dtype>` | { int, long, float, double, char, string, bool } |
| `<value>` | { intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false } |
| `<value_list_tail>` | { ,, λ } |
| `<array_dims>` | { [ } |
| `<array_dim2_opt>` | { [, λ } |
| `<array_with_init>` | { [ } |
| `<array_init_tail>` | { [, =, λ } |
| `<arr_init_opt_1d>` | { =, λ } |
| `<arr_init_content_1d>` | { int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, λ } |
| `<arr_init_opt_2d>` | { =, λ } |
| `<arr_init_content_2d>` | { {, λ } |
| `<elem_2d_tail>` | { ,, λ } |
| `<elem_list>` | { int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, λ } |
| `<elem_1d_tail>` | { ,, λ } |
| `<arr_elem>` | { int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false } |
| `<size>` | { intlit, id } |
| `<field_list>` | { int, long, float, double, char, string, bool, id, λ } |
| `<field_dec>` | { int, long, float, double, char, string, bool, id } |
| `<field_type>` | { int, long, float, double, char, string, bool, id } |
| `<field_arr_opt>` | { [, λ } |
| `<field_cont>` | { ,, λ } |
| `<nonvoid_ret_type>` | { int, long, float, double, char, string, bool, id } |
| `<ret_type_suffix>` | { [, λ } |
| `<ret_id_suffix>` | { [, ., λ } |
| `<param_list>` | { int, long, float, double, char, string, bool, id, λ } |
| `<param_type>` | { int, long, float, double, char, string, bool, id } |
| `<param_arr_opt>` | { [, λ } |
| `<param_cont>` | { ,, λ } |
| `<function_body_nonvoid>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<func_content_nonvoid>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<function_body_void>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<func_content_void>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<using_block>` | { using, λ } |
| `<using_cont>` | { ,, λ } |
| `<local_block>` | { local, λ } |
| `<local_dec_body>` | { int, long, float, double, char, string, bool, id } |
| `<typed_local_tail>` | { [, = } |
| `<multi_local>` | { ,, λ } |
| `<weave_local_tail>` | { =, [ } |
| `<statement_non_return>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break } |
| `<ctrl_stmt_list>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, λ } |
| `<expression>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<assign_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<assign_tail>` | { =, +=, -=, *=, /=, %=, λ } |
| `<assign_op>` | { =, +=, -=, *=, /=, %= } |
| `<concat_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<concat_tail>` | { .., λ } |
| `<or_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<or_tail>` | { \|\|, λ } |
| `<and_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<and_tail>` | { &&, λ } |
| `<eq_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<eq_tail>` | { ==, !=, λ } |
| `<rel_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<rel_tail>` | { <, >, <=, >=, λ } |
| `<add_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<add_tail>` | { +, -, λ } |
| `<mul_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<mul_tail>` | { *, /, %, λ } |
| `<unary_expr>` | { !, ++, --, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<postfix_expr>` | { (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<postfix_chain>` | { [, ., (, ++, --, λ } |
| `<array_access>` | { [ } |
| `<array_access_dim2>` | { [, λ } |
| `<postfix_after_arr>` | { ., (, ++, --, λ } |
| `<array_index>` | { intlit, id } |
| `<arg_list>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, λ } |
| `<arg_tail>` | { ,, λ } |
| `<io_stmt>` | { trap, thread, threadln } |
| `<print_args>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<print_tail>` | { ,, λ } |
| `<ctrl_struct>` | { if, switch, for, while, do } |
| `<else_opt>` | { else, λ } |
| `<else_body>` | { {, if } |
| `<case_list>` | { case, λ } |
| `<case_val>` | { intlit, longlit, charlit, true, false } |
| `<default_opt>` | { default, λ } |
| `<break_opt>` | { break, λ } |
| `<for_init>` | { local, id, λ } |
| `<for_init_assign_tail>` | { =, +=, -=, *=, /=, %= } |
| `<for_init_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<for_init_type>` | { int, long, float, double, char, string, bool } |
| `<for_cond>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool, λ } |
| `<for_update>` | { id, ++, --, λ } |
| `<for_update_tail>` | { ++, --, =, +=, -=, *=, /=, %= } |
| `<condition>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_or>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_or_tail>` | { \|\|, λ } |
| `<cond_and>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_and_tail>` | { &&, λ } |
| `<cond_not>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_rhs_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<cond_atom>` | { true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_after_id>` | { (, [, ., ++, --, *, /, %, +, -, ==, !=, <, >, <=, >=, &&, \|\|, ), λ } |
| `<cond_after_call>` | { [, ., (, ++, --, λ } |
| `<cond_after_id_no_call>` | { [, ., ++, --, *, /, %, +, -, λ } |
| `<cond_comparison_opt>` | { ==, !=, <, >, <=, >=, λ } |
| `<cond_postfix_no_call>` | { [, ., ++, --, λ } |
| `<comp_op>` | { ==, !=, <, >, <=, >= } |
| `<main_body>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<main_content>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |

---

## 4. FOLLOW Sets

| Non-terminal | FOLLOW Set |
|--------------|------------|
| `<program>` | { $END } |
| `<decl_list>` | { $END } |
| `<int_decl_or_main>` | { $END } |
| `<other_decl>` | { int, global, long, float, double, char, string, bool, weave, id, func } |
| `<main_func>` | { $END } |
| `<multi_global>` | { ; } |
| `<weave_inst_decl>` | { int, global, long, float, double, char, string, bool, weave, id, func } |
| `<weave_inst_tail>` | { ,, ; } |
| `<weave_field_value>` | { ,, } } |
| `<weave_arr_content>` | { } } |
| `<weave_field_list_tail>` | { } } |
| `<weave_inst_cont>` | { ; } |
| `<weave_arr_cont>` | { ; } |
| `<typed_decl_tail>` | { int, global, long, float, double, char, string, bool, weave, id, func } |
| `<multi_typed>` | { ; } |
| `<mutability>` | { int, long, float, double, char, string, bool, id } |
| `<dtype>` | { id } |
| `<value>` | { ) } |
| `<value_list_tail>` | { } } |
| `<array_dims>` | { id, ,, ;, ) } |
| `<array_dim2_opt>` | { id, ,, ;, ) } |
| `<array_with_init>` | { ;, , } |
| `<array_init_tail>` | { ;, , } |
| `<arr_init_opt_1d>` | { ;, , } |
| `<arr_init_content_1d>` | { } } |
| `<arr_init_opt_2d>` | { ;, , } |
| `<arr_init_content_2d>` | { } } |
| `<elem_2d_tail>` | { } } |
| `<elem_list>` | { } } |
| `<elem_1d_tail>` | { } } |
| `<arr_elem>` | { ,, } } |
| `<size>` | { ] } |
| `<field_list>` | { } } |
| `<field_dec>` | { int, long, float, double, char, string, bool, id, } } |
| `<field_type>` | { id } |
| `<field_arr_opt>` | { ,, ; } |
| `<field_cont>` | { ; } |
| `<nonvoid_ret_type>` | { id } |
| `<ret_type_suffix>` | { id } |
| `<ret_id_suffix>` | { id } |
| `<param_list>` | { ) } |
| `<param_type>` | { id } |
| `<param_arr_opt>` | { ,, ) } |
| `<param_cont>` | { ) } |
| `<function_body_nonvoid>` | { } } |
| `<func_content_nonvoid>` | { } } |
| `<function_body_void>` | { } } |
| `<func_content_void>` | { } } |
| `<using_block>` | { local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return, } } |
| `<using_cont>` | { ; } |
| `<local_block>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return, } } |
| `<local_dec_body>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<typed_local_tail>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<multi_local>` | { ; } |
| `<weave_local_tail>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<statement_non_return>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, }, using, local, return } |
| `<ctrl_stmt_list>` | { }, case, default } |
| `<expression>` | { ;, ), ,, } } |
| `<assign_expr>` | { ;, ), ,, } } |
| `<assign_tail>` | { ;, ), ,, } } |
| `<assign_op>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<concat_expr>` | { =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<concat_tail>` | { =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<or_expr>` | { .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<or_tail>` | { .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<and_expr>` | { \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<and_tail>` | { \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<eq_expr>` | { &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<eq_tail>` | { &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<rel_expr>` | { ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<rel_tail>` | { ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<add_expr>` | { <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<add_tail>` | { <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<mul_expr>` | { +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<mul_tail>` | { +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<unary_expr>` | { *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<postfix_expr>` | { *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<postfix_chain>` | { *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<array_access>` | { ., (, ++, --, *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<array_access_dim2>` | { ., (, ++, --, *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<postfix_after_arr>` | { *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<array_index>` | { ] } |
| `<arg_list>` | { ) } |
| `<arg_tail>` | { ) } |
| `<io_stmt>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, }, using, local, return } |
| `<print_args>` | { ) } |
| `<print_tail>` | { ) } |
| `<ctrl_struct>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, }, using, local, return } |
| `<else_opt>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, }, using, local, return } |
| `<else_body>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, }, using, local, return } |
| `<case_list>` | { default, } } |
| `<case_val>` | { : } |
| `<default_opt>` | { } } |
| `<break_opt>` | { case, default, } } |
| `<for_init>` | { ; } |
| `<for_init_assign_tail>` | { ; } |
| `<for_init_expr>` | { ; } |
| `<for_init_type>` | { id } |
| `<for_cond>` | { ; } |
| `<for_update>` | { ) } |
| `<for_update_tail>` | { ) } |
| `<condition>` | { ) } |
| `<cond_or>` | { ) } |
| `<cond_or_tail>` | { ) } |
| `<cond_and>` | { \|\|, ) } |
| `<cond_and_tail>` | { \|\|, ) } |
| `<cond_not>` | { &&, \|\|, ) } |
| `<cond_rhs_expr>` | { &&, \|\|, ) } |
| `<cond_atom>` | { &&, \|\|, ) } |
| `<cond_after_id>` | { &&, \|\|, ) } |
| `<cond_after_call>` | { &&, \|\|, ) } |
| `<cond_after_id_no_call>` | { ==, !=, <, >, <=, >=, &&, \|\|, ) } |
| `<cond_comparison_opt>` | { &&, \|\|, ) } |
| `<cond_postfix_no_call>` | { *, /, %, +, -, ==, !=, <, >, <=, >=, &&, \|\|, ) } |
| `<comp_op>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<main_body>` | { } } |
| `<main_content>` | { } } |

---

## 5. PREDICT Sets

### Program Structure

| Production | PREDICT Set |
|------------|-------------|
| `<program> → <decl_list>` | { int, global, long, float, double, char, string, bool, weave, id, func } |
| `<decl_list> → int <int_decl_or_main>` | { int } |
| `<decl_list> → <other_decl> <decl_list>` | { global, long, float, double, char, string, bool, weave, id, func } |
| `<int_decl_or_main> → id <typed_decl_tail> <decl_list>` | { id } |
| `<int_decl_or_main> → main ( ) { <main_body> } $END` | { main } |
| `<other_decl> → global <mutability> <dtype> id = <expression> <multi_global> ;` | { global } |
| `<other_decl> → long id <typed_decl_tail>` | { long } |
| `<other_decl> → float id <typed_decl_tail>` | { float } |
| `<other_decl> → double id <typed_decl_tail>` | { double } |
| `<other_decl> → char id <typed_decl_tail>` | { char } |
| `<other_decl> → string id <typed_decl_tail>` | { string } |
| `<other_decl> → bool id <typed_decl_tail>` | { bool } |
| `<other_decl> → weave id { <field_list> } ;` | { weave } |
| `<other_decl> → id <weave_inst_decl>` | { id } |
| `<other_decl> → func <nonvoid_ret_type> id ( <param_list> ) { <function_body_nonvoid> }` | { func } |
| `<other_decl> → func void id ( <param_list> ) { <function_body_void> }` | { func } |
| `<multi_global> → , id = <expression> <multi_global>` | { , } |
| `<multi_global> → λ` | { ; } |
| `<weave_inst_decl> → id <weave_inst_tail> <weave_inst_cont> ;` | { id } |
| `<weave_inst_decl> → <array_with_init> <weave_arr_cont> ;` | { [ } |
| `<weave_inst_tail> → = { <weave_field_value> <weave_field_list_tail> }` | { = } |
| `<weave_inst_tail> → <array_with_init>` | { [ } |
| `<weave_field_value> → intlit` | { intlit } |
| `<weave_field_value> → longlit` | { longlit } |
| `<weave_field_value> → floatlit` | { floatlit } |
| `<weave_field_value> → doublelit` | { doublelit } |
| `<weave_field_value> → charlit` | { charlit } |
| `<weave_field_value> → stringlit` | { stringlit } |
| `<weave_field_value> → true` | { true } |
| `<weave_field_value> → false` | { false } |
| `<weave_field_value> → { <weave_arr_content> }` | { { } |
| `<weave_arr_content> → { <elem_list> } <elem_2d_tail>` | { { } |
| `<weave_arr_content> → <arr_elem> <elem_1d_tail>` | { int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false } |
| `<weave_arr_content> → λ` | { } } |
| `<weave_field_list_tail> → , <weave_field_value> <weave_field_list_tail>` | { , } |
| `<weave_field_list_tail> → λ` | { } } |
| `<weave_inst_cont> → , id <weave_inst_tail> <weave_inst_cont>` | { , } |
| `<weave_inst_cont> → λ` | { ; } |
| `<weave_arr_cont> → , id <array_with_init> <weave_arr_cont>` | { , } |
| `<weave_arr_cont> → λ` | { ; } |
| `<typed_decl_tail> → <array_with_init> ;` | { [ } |
| `<typed_decl_tail> → = <expression> <multi_typed> ;` | { = } |
| `<multi_typed> → , id = <expression> <multi_typed>` | { , } |
| `<multi_typed> → λ` | { ; } |

### Mutability & Types

| Production | PREDICT Set |
|------------|-------------|
| `<mutability> → var` | { var } |
| `<mutability> → const` | { const } |
| `<dtype> → int` | { int } |
| `<dtype> → long` | { long } |
| `<dtype> → float` | { float } |
| `<dtype> → double` | { double } |
| `<dtype> → char` | { char } |
| `<dtype> → string` | { string } |
| `<dtype> → bool` | { bool } |

### Values & Literals

| Production | PREDICT Set |
|------------|-------------|
| `<value> → intlit` | { intlit } |
| `<value> → longlit` | { longlit } |
| `<value> → floatlit` | { floatlit } |
| `<value> → doublelit` | { doublelit } |
| `<value> → charlit` | { charlit } |
| `<value> → stringlit` | { stringlit } |
| `<value> → true` | { true } |
| `<value> → false` | { false } |
| `<value_list_tail> → , <value> <value_list_tail>` | { , } |
| `<value_list_tail> → λ` | { } } |

### Array Dimensions

| Production | PREDICT Set |
|------------|-------------|
| `<array_dims> → [ <size> ] <array_dim2_opt>` | { [ } |
| `<array_dim2_opt> → [ <size> ]` | { [ } |
| `<array_dim2_opt> → λ` | { id, ,, ;, ) } |
| `<array_with_init> → [ <size> ] <array_init_tail>` | { [ } |
| `<array_init_tail> → [ <size> ] <arr_init_opt_2d>` | { [ } |
| `<array_init_tail> → <arr_init_opt_1d>` | { =, ;, , } |

### Array Declarations

| Production | PREDICT Set |
|------------|-------------|
| `<arr_init_opt_1d> → = { <arr_init_content_1d> }` | { = } |
| `<arr_init_opt_1d> → λ` | { ;, , } |
| `<arr_init_content_1d> → <arr_elem> <elem_1d_tail>` | { int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false } |
| `<arr_init_content_1d> → λ` | { } } |
| `<arr_init_opt_2d> → = { <arr_init_content_2d> }` | { = } |
| `<arr_init_opt_2d> → λ` | { ;, , } |
| `<arr_init_content_2d> → { <elem_list> } <elem_2d_tail>` | { { } |
| `<arr_init_content_2d> → λ` | { } } |
| `<elem_2d_tail> → , { <elem_list> } <elem_2d_tail>` | { , } |
| `<elem_2d_tail> → λ` | { } } |
| `<elem_list> → <arr_elem> <elem_1d_tail>` | { int, long, float, double, char, string, bool, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false } |
| `<elem_list> → λ` | { } } |
| `<elem_1d_tail> → , <arr_elem> <elem_1d_tail>` | { , } |
| `<elem_1d_tail> → λ` | { } } |
| `<arr_elem> → int ( <value> )` | { int } |
| `<arr_elem> → long ( <value> )` | { long } |
| `<arr_elem> → float ( <value> )` | { float } |
| `<arr_elem> → double ( <value> )` | { double } |
| `<arr_elem> → char ( <value> )` | { char } |
| `<arr_elem> → string ( <value> )` | { string } |
| `<arr_elem> → bool ( <value> )` | { bool } |
| `<arr_elem> → intlit` | { intlit } |
| `<arr_elem> → longlit` | { longlit } |
| `<arr_elem> → floatlit` | { floatlit } |
| `<arr_elem> → doublelit` | { doublelit } |
| `<arr_elem> → charlit` | { charlit } |
| `<arr_elem> → stringlit` | { stringlit } |
| `<arr_elem> → true` | { true } |
| `<arr_elem> → false` | { false } |
| `<size> → intlit` | { intlit } |
| `<size> → id` | { id } |

### Weave (Struct) Definitions

| Production | PREDICT Set |
|------------|-------------|
| `<field_list> → <field_dec> <field_list>` | { int, long, float, double, char, string, bool, id } |
| `<field_list> → λ` | { } } |
| `<field_dec> → <field_type> id <field_arr_opt> <field_cont> ;` | { int, long, float, double, char, string, bool, id } |
| `<field_type> → int` | { int } |
| `<field_type> → long` | { long } |
| `<field_type> → float` | { float } |
| `<field_type> → double` | { double } |
| `<field_type> → char` | { char } |
| `<field_type> → string` | { string } |
| `<field_type> → bool` | { bool } |
| `<field_type> → id` | { id } |
| `<field_arr_opt> → <array_dims>` | { [ } |
| `<field_arr_opt> → λ` | { ,, ; } |
| `<field_cont> → , id <field_arr_opt> <field_cont>` | { , } |
| `<field_cont> → λ` | { ; } |

### Functions

| Production | PREDICT Set |
|------------|-------------|
| `<nonvoid_ret_type> → int <ret_type_suffix>` | { int } |
| `<nonvoid_ret_type> → long <ret_type_suffix>` | { long } |
| `<nonvoid_ret_type> → float <ret_type_suffix>` | { float } |
| `<nonvoid_ret_type> → double <ret_type_suffix>` | { double } |
| `<nonvoid_ret_type> → char <ret_type_suffix>` | { char } |
| `<nonvoid_ret_type> → string <ret_type_suffix>` | { string } |
| `<nonvoid_ret_type> → bool <ret_type_suffix>` | { bool } |
| `<nonvoid_ret_type> → id <ret_id_suffix>` | { id } |
| `<ret_type_suffix> → <array_dims>` | { [ } |
| `<ret_type_suffix> → λ` | { id } |
| `<ret_id_suffix> → <array_dims>` | { [ } |
| `<ret_id_suffix> → . id` | { . } |
| `<ret_id_suffix> → λ` | { id } |
| `<param_list> → <param_type> id <param_arr_opt> <param_cont>` | { int, long, float, double, char, string, bool, id } |
| `<param_list> → λ` | { ) } |
| `<param_type> → int` | { int } |
| `<param_type> → long` | { long } |
| `<param_type> → float` | { float } |
| `<param_type> → double` | { double } |
| `<param_type> → char` | { char } |
| `<param_type> → string` | { string } |
| `<param_type> → bool` | { bool } |
| `<param_type> → id` | { id } |
| `<param_arr_opt> → <array_dims>` | { [ } |
| `<param_arr_opt> → λ` | { ,, ) } |
| `<param_cont> → , <param_type> id <param_arr_opt> <param_cont>` | { , } |
| `<param_cont> → λ` | { ) } |
| `<function_body_nonvoid> → <func_content_nonvoid>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<func_content_nonvoid> → using id <using_cont> ; <func_content_nonvoid>` | { using } |
| `<func_content_nonvoid> → local <mutability> <local_dec_body> <func_content_nonvoid>` | { local } |
| `<func_content_nonvoid> → <statement_non_return> <func_content_nonvoid>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break } |
| `<func_content_nonvoid> → return <expression> ;` | { return } |
| `<function_body_void> → <func_content_void>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<func_content_void> → using id <using_cont> ; <func_content_void>` | { using } |
| `<func_content_void> → local <mutability> <local_dec_body> <func_content_void>` | { local } |
| `<func_content_void> → <statement_non_return> <func_content_void>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break } |
| `<func_content_void> → return ;` | { return } |

### Using Block

| Production | PREDICT Set |
|------------|-------------|
| `<using_block> → using id <using_cont> ; <using_block>` | { using } |
| `<using_block> → λ` | { local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return, } } |
| `<using_cont> → , id <using_cont>` | { , } |
| `<using_cont> → λ` | { ; } |

### Local Declarations

| Production | PREDICT Set |
|------------|-------------|
| `<local_block> → local <mutability> <local_dec_body> <local_block>` | { local } |
| `<local_block> → λ` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return, } } |
| `<local_dec_body> → int id <typed_local_tail>` | { int } |
| `<local_dec_body> → long id <typed_local_tail>` | { long } |
| `<local_dec_body> → float id <typed_local_tail>` | { float } |
| `<local_dec_body> → double id <typed_local_tail>` | { double } |
| `<local_dec_body> → char id <typed_local_tail>` | { char } |
| `<local_dec_body> → string id <typed_local_tail>` | { string } |
| `<local_dec_body> → bool id <typed_local_tail>` | { bool } |
| `<local_dec_body> → id id <weave_local_tail>` | { id } |
| `<typed_local_tail> → <array_with_init> ;` | { [ } |
| `<typed_local_tail> → = <expression> <multi_local> ;` | { = } |
| `<multi_local> → , id = <expression> <multi_local>` | { , } |
| `<multi_local> → λ` | { ; } |
| `<weave_local_tail> → = { <weave_field_value> <weave_field_list_tail> } <weave_inst_cont> ;` | { = } |
| `<weave_local_tail> → <array_with_init> <weave_arr_cont> ;` | { [ } |

### Statements

| Production | PREDICT Set |
|------------|-------------|
| `<statement_non_return> → <expression> ;` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<statement_non_return> → <io_stmt>` | { trap, thread, threadln } |
| `<statement_non_return> → <ctrl_struct>` | { if, switch, for, while, do } |
| `<statement_non_return> → break ;` | { break } |
| `<ctrl_stmt_list> → <statement_non_return> <ctrl_stmt_list>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break } |
| `<ctrl_stmt_list> → λ` | { }, case, default } |

### Expressions

| Production | PREDICT Set |
|------------|-------------|
| `<expression> → <assign_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<assign_expr> → <concat_expr> <assign_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<assign_tail> → <assign_op> <assign_expr>` | { =, +=, -=, *=, /=, %= } |
| `<assign_tail> → λ` | { ;, ), ,, } } |
| `<assign_op> → =` | { = } |
| `<assign_op> → +=` | { += } |
| `<assign_op> → -=` | { -= } |
| `<assign_op> → *=` | { *= } |
| `<assign_op> → /=` | { /= } |
| `<assign_op> → %=` | { %= } |
| `<concat_expr> → <or_expr> <concat_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<concat_tail> → .. <or_expr> <concat_tail>` | { .. } |
| `<concat_tail> → λ` | { =, +=, -=, *=, /=, %=, ;, ), ,, } } |

### Boolean / Logical Expressions

| Production | PREDICT Set |
|------------|-------------|
| `<or_expr> → <and_expr> <or_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<or_tail> → \|\| <and_expr> <or_tail>` | { \|\| } |
| `<or_tail> → λ` | { .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<and_expr> → <eq_expr> <and_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<and_tail> → && <eq_expr> <and_tail>` | { && } |
| `<and_tail> → λ` | { \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<eq_expr> → <rel_expr> <eq_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<eq_tail> → == <rel_expr> <eq_tail>` | { == } |
| `<eq_tail> → != <rel_expr> <eq_tail>` | { != } |
| `<eq_tail> → λ` | { &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<rel_expr> → <add_expr> <rel_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<rel_tail> → < <add_expr>` | { < } |
| `<rel_tail> → > <add_expr>` | { > } |
| `<rel_tail> → <= <add_expr>` | { <= } |
| `<rel_tail> → >= <add_expr>` | { >= } |
| `<rel_tail> → λ` | { ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |

### Arithmetic Expressions

| Production | PREDICT Set |
|------------|-------------|
| `<add_expr> → <mul_expr> <add_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<add_tail> → + <mul_expr> <add_tail>` | { + } |
| `<add_tail> → - <mul_expr> <add_tail>` | { - } |
| `<add_tail> → λ` | { <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<mul_expr> → <unary_expr> <mul_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<mul_tail> → * <unary_expr> <mul_tail>` | { * } |
| `<mul_tail> → / <unary_expr> <mul_tail>` | { / } |
| `<mul_tail> → % <unary_expr> <mul_tail>` | { % } |
| `<mul_tail> → λ` | { +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<unary_expr> → ! <unary_expr>` | { ! } |
| `<unary_expr> → ++ <unary_expr>` | { ++ } |
| `<unary_expr> → -- <unary_expr>` | { -- } |
| `<unary_expr> → <postfix_expr>` | { (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<postfix_expr> → ( <expression> ) <postfix_chain>` | { ( } |
| `<postfix_expr> → int ( <expression> )` | { int } |
| `<postfix_expr> → long ( <expression> )` | { long } |
| `<postfix_expr> → float ( <expression> )` | { float } |
| `<postfix_expr> → double ( <expression> )` | { double } |
| `<postfix_expr> → char ( <expression> )` | { char } |
| `<postfix_expr> → string ( <expression> )` | { string } |
| `<postfix_expr> → bool ( <expression> )` | { bool } |
| `<postfix_expr> → id <postfix_chain>` | { id } |
| `<postfix_expr> → intlit` | { intlit } |
| `<postfix_expr> → longlit` | { longlit } |
| `<postfix_expr> → floatlit` | { floatlit } |
| `<postfix_expr> → doublelit` | { doublelit } |
| `<postfix_expr> → charlit` | { charlit } |
| `<postfix_expr> → stringlit` | { stringlit } |
| `<postfix_expr> → true` | { true } |
| `<postfix_expr> → false` | { false } |

### Postfix Chain

| Production | PREDICT Set |
|------------|-------------|
| `<postfix_chain> → <array_access> <postfix_after_arr>` | { [ } |
| `<postfix_chain> → . id <postfix_chain>` | { . } |
| `<postfix_chain> → ( <arg_list> ) <postfix_chain>` | { ( } |
| `<postfix_chain> → ++` | { ++ } |
| `<postfix_chain> → --` | { -- } |
| `<postfix_chain> → λ` | { *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<array_access> → [ <array_index> ] <array_access_dim2>` | { [ } |
| `<array_access_dim2> → [ <array_index> ]` | { [ } |
| `<array_access_dim2> → λ` | { ., (, ++, --, *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<postfix_after_arr> → . id <postfix_chain>` | { . } |
| `<postfix_after_arr> → ( <arg_list> ) <postfix_chain>` | { ( } |
| `<postfix_after_arr> → ++` | { ++ } |
| `<postfix_after_arr> → --` | { -- } |
| `<postfix_after_arr> → λ` | { *, /, %, +, -, <, >, <=, >=, ==, !=, &&, \|\|, .., =, +=, -=, *=, /=, %=, ;, ), ,, } } |
| `<array_index> → intlit` | { intlit } |
| `<array_index> → id` | { id } |
| `<arg_list> → <expression> <arg_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<arg_list> → λ` | { ) } |
| `<arg_tail> → , <expression> <arg_tail>` | { , } |
| `<arg_tail> → λ` | { ) } |

### I/O Statements

| Production | PREDICT Set |
|------------|-------------|
| `<io_stmt> → trap ( <expression> ) ;` | { trap } |
| `<io_stmt> → thread ( <print_args> ) ;` | { thread } |
| `<io_stmt> → threadln ( <print_args> ) ;` | { threadln } |
| `<print_args> → <expression> <print_tail>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<print_tail> → , <expression> <print_tail>` | { , } |
| `<print_tail> → λ` | { ) } |

### Control Structures

| Production | PREDICT Set |
|------------|-------------|
| `<ctrl_struct> → if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` | { if } |
| `<ctrl_struct> → switch ( <expression> ) { <case_list> <default_opt> }` | { switch } |
| `<ctrl_struct> → for ( <for_init> ; <for_cond> ; <for_update> ) { <ctrl_stmt_list> }` | { for } |
| `<ctrl_struct> → while ( <condition> ) { <ctrl_stmt_list> }` | { while } |
| `<ctrl_struct> → do { <ctrl_stmt_list> } while ( <condition> ) ;` | { do } |
| `<else_opt> → else <else_body>` | { else } |
| `<else_opt> → λ` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, }, using, local, return } |
| `<else_body> → { <ctrl_stmt_list> }` | { { } |
| `<else_body> → if ( <condition> ) { <ctrl_stmt_list> } <else_opt>` | { if } |
| `<case_list> → case <case_val> : <ctrl_stmt_list> <break_opt> <case_list>` | { case } |
| `<case_list> → λ` | { default, } } |
| `<case_val> → intlit` | { intlit } |
| `<case_val> → longlit` | { longlit } |
| `<case_val> → charlit` | { charlit } |
| `<case_val> → true` | { true } |
| `<case_val> → false` | { false } |
| `<default_opt> → default : <ctrl_stmt_list> <break_opt>` | { default } |
| `<default_opt> → λ` | { } } |
| `<break_opt> → break ;` | { break } |
| `<break_opt> → λ` | { case, default, } } |

### For Loop

| Production | PREDICT Set |
|------------|-------------|
| `<for_init> → local var <for_init_type> id = <for_init_expr>` | { local } |
| `<for_init> → id <for_init_assign_tail>` | { id } |
| `<for_init> → λ` | { ; } |
| `<for_init_assign_tail> → <assign_op> <for_init_expr>` | { =, +=, -=, *=, /=, %= } |
| `<for_init_expr> → <concat_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<for_init_type> → int` | { int } |
| `<for_init_type> → long` | { long } |
| `<for_init_type> → float` | { float } |
| `<for_init_type> → double` | { double } |
| `<for_init_type> → char` | { char } |
| `<for_init_type> → string` | { string } |
| `<for_init_type> → bool` | { bool } |
| `<for_cond> → <condition>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<for_cond> → λ` | { ; } |
| `<for_update> → id <for_update_tail>` | { id } |
| `<for_update> → ++ id` | { ++ } |
| `<for_update> → -- id` | { -- } |
| `<for_update> → λ` | { ) } |
| `<for_update_tail> → ++` | { ++ } |
| `<for_update_tail> → --` | { -- } |
| `<for_update_tail> → <assign_op> <expression>` | { =, +=, -=, *=, /=, %= } |

### Condition Expressions

| Production | PREDICT Set |
|------------|-------------|
| `<condition> → <cond_or>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_or> → <cond_and> <cond_or_tail>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_or_tail> → \|\| <cond_and> <cond_or_tail>` | { \|\| } |
| `<cond_or_tail> → λ` | { ) } |
| `<cond_and> → <cond_not> <cond_and_tail>` | { !, true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_and_tail> → && <cond_not> <cond_and_tail>` | { && } |
| `<cond_and_tail> → λ` | { \|\|, ) } |
| `<cond_not> → ! <cond_not>` | { ! } |
| `<cond_not> → <cond_atom>` | { true, false, (, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, int, long, float, double, char, string, bool } |
| `<cond_rhs_expr> → <concat_expr>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool } |
| `<cond_atom> → true` | { true } |
| `<cond_atom> → false` | { false } |
| `<cond_atom> → ( <condition> )` | { ( } |
| `<cond_atom> → id <cond_after_id>` | { id } |
| `<cond_atom> → intlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { intlit } |
| `<cond_atom> → longlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { longlit } |
| `<cond_atom> → floatlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { floatlit } |
| `<cond_atom> → doublelit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { doublelit } |
| `<cond_atom> → charlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { charlit } |
| `<cond_atom> → stringlit <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { stringlit } |
| `<cond_atom> → int ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { int } |
| `<cond_atom> → long ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { long } |
| `<cond_atom> → float ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { float } |
| `<cond_atom> → double ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { double } |
| `<cond_atom> → char ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { char } |
| `<cond_atom> → string ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { string } |
| `<cond_atom> → bool ( <expression> ) <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { bool } |
| `<cond_after_id> → ( <arg_list> ) <cond_after_call>` | { ( } |
| `<cond_after_id> → <cond_after_id_no_call> <cond_comparison_opt>` | { [, ., ++, --, *, /, %, +, -, ==, !=, <, >, <=, >=, &&, \|\|, ) } |
| `<cond_after_call> → λ` | { &&, \|\|, ) } |
| `<cond_after_call> → <postfix_chain> <mul_tail> <add_tail> <comp_op> <cond_rhs_expr>` | { [, ., (, ++, -- } |
| `<cond_after_id_no_call> → <cond_postfix_no_call> <mul_tail> <add_tail>` | { [, ., ++, --, *, /, %, +, -, ==, !=, <, >, <=, >=, &&, \|\|, ) } |
| `<cond_comparison_opt> → <comp_op> <cond_rhs_expr>` | { ==, !=, <, >, <=, >= } |
| `<cond_comparison_opt> → λ` | { &&, \|\|, ) } |
| `<cond_postfix_no_call> → [ <array_index> ] <array_access_dim2> <postfix_after_arr>` | { [ } |
| `<cond_postfix_no_call> → . id <postfix_chain>` | { . } |
| `<cond_postfix_no_call> → ++` | { ++ } |
| `<cond_postfix_no_call> → --` | { -- } |
| `<cond_postfix_no_call> → λ` | { *, /, %, +, -, ==, !=, <, >, <=, >=, &&, \|\|, ) } |
| `<comp_op> → ==` | { == } |
| `<comp_op> → !=` | { != } |
| `<comp_op> → <` | { < } |
| `<comp_op> → >` | { > } |
| `<comp_op> → <=` | { <= } |
| `<comp_op> → >=` | { >= } |

### Main Function Body

| Production | PREDICT Set |
|------------|-------------|
| `<main_body> → <main_content>` | { using, local, (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break, return } |
| `<main_content> → using id <using_cont> ; <main_content>` | { using } |
| `<main_content> → local <mutability> <local_dec_body> <main_content>` | { local } |
| `<main_content> → <statement_non_return> <main_content>` | { (, !, ++, --, id, intlit, longlit, floatlit, doublelit, charlit, stringlit, true, false, int, long, float, double, char, string, bool, trap, thread, threadln, if, switch, for, while, do, break } |
| `<main_content> → return intlit ;` | { return } |

---

## 6. LL(1) Verification

### 6.1 FIRST/FIRST Conflict Check

For each non-terminal with multiple productions, the PREDICT sets must be pairwise disjoint.

| Non-terminal | Conflict Status | Details |
|--------------|-----------------|---------|
| `<decl_list>` | **NO CONFLICT** | { int } ∩ { global, long, float, double, char, string, bool, weave, id, func } = ∅ |
| `<int_decl_or_main>` | **NO CONFLICT** | { id } ∩ { main } = ∅ |
| `<other_decl>` | **POTENTIAL CONFLICT** | `func <nonvoid_ret_type>...` and `func void...` both start with `func` |
| `<multi_global>` | **NO CONFLICT** | { , } ∩ { ; } = ∅ |
| `<weave_inst_decl>` | **NO CONFLICT** | { id } ∩ { [ } = ∅ |
| `<weave_inst_tail>` | **NO CONFLICT** | { = } ∩ { [ } = ∅ |
| `<weave_field_value>` | **NO CONFLICT** | All productions start with distinct terminals |
| `<weave_arr_content>` | **NO CONFLICT** | { { } ∩ { int, long, ... } ∩ { } } = ∅ |
| `<weave_field_list_tail>` | **NO CONFLICT** | { , } ∩ { } } = ∅ |
| `<weave_inst_cont>` | **NO CONFLICT** | { , } ∩ { ; } = ∅ |
| `<weave_arr_cont>` | **NO CONFLICT** | { , } ∩ { ; } = ∅ |
| `<typed_decl_tail>` | **NO CONFLICT** | { [ } ∩ { = } = ∅ |
| `<multi_typed>` | **NO CONFLICT** | { , } ∩ { ; } = ∅ |
| `<mutability>` | **NO CONFLICT** | { var } ∩ { const } = ∅ |
| `<dtype>` | **NO CONFLICT** | All distinct terminals |
| `<value>` | **NO CONFLICT** | All distinct terminals |
| `<value_list_tail>` | **NO CONFLICT** | { , } ∩ { } } = ∅ |
| `<array_dim2_opt>` | **NO CONFLICT** | { [ } ∩ { id, ,, ;, ) } = ∅ |
| `<array_init_tail>` | **NO CONFLICT** | { [ } ∩ { =, ;, , } = ∅ |
| `<arr_init_opt_1d>` | **NO CONFLICT** | { = } ∩ { ;, , } = ∅ |
| `<arr_init_content_1d>` | **NO CONFLICT** | { int, long, ... } ∩ { } } = ∅ |
| `<arr_init_opt_2d>` | **NO CONFLICT** | { = } ∩ { ;, , } = ∅ |
| `<arr_init_content_2d>` | **NO CONFLICT** | { { } ∩ { } } = ∅ |
| `<elem_2d_tail>` | **NO CONFLICT** | { , } ∩ { } } = ∅ |
| `<elem_list>` | **NO CONFLICT** | { int, long, ... } ∩ { } } = ∅ |
| `<elem_1d_tail>` | **NO CONFLICT** | { , } ∩ { } } = ∅ |
| `<arr_elem>` | **NO CONFLICT** | All distinct terminals |
| `<size>` | **NO CONFLICT** | { intlit } ∩ { id } = ∅ |
| `<field_list>` | **NO CONFLICT** | { int, long, ... id } ∩ { } } = ∅ |
| `<field_type>` | **NO CONFLICT** | All distinct terminals |
| `<field_arr_opt>` | **NO CONFLICT** | { [ } ∩ { ,, ; } = ∅ |
| `<field_cont>` | **NO CONFLICT** | { , } ∩ { ; } = ∅ |
| `<nonvoid_ret_type>` | **NO CONFLICT** | All distinct terminals |
| `<ret_type_suffix>` | **NO CONFLICT** | { [ } ∩ { id } = ∅ |
| `<ret_id_suffix>` | **NO CONFLICT** | { [ } ∩ { . } ∩ { id } = ∅ |
| `<param_list>` | **NO CONFLICT** | { int, long, ... id } ∩ { ) } = ∅ |
| `<param_type>` | **NO CONFLICT** | All distinct terminals |
| `<param_arr_opt>` | **NO CONFLICT** | { [ } ∩ { ,, ) } = ∅ |
| `<param_cont>` | **NO CONFLICT** | { , } ∩ { ) } = ∅ |
| `<func_content_nonvoid>` | **NO CONFLICT** | { using } ∩ { local } ∩ { expr starters } ∩ { return } = ∅ |
| `<func_content_void>` | **NO CONFLICT** | { using } ∩ { local } ∩ { expr starters } ∩ { return } = ∅ |
| `<using_block>` | **NO CONFLICT** | { using } disjoint from FOLLOW |
| `<using_cont>` | **NO CONFLICT** | { , } ∩ { ; } = ∅ |
| `<local_block>` | **NO CONFLICT** | { local } disjoint from FOLLOW |
| `<local_dec_body>` | **NO CONFLICT** | All distinct terminals |
| `<typed_local_tail>` | **NO CONFLICT** | { [ } ∩ { = } = ∅ |
| `<multi_local>` | **NO CONFLICT** | { , } ∩ { ; } = ∅ |
| `<weave_local_tail>` | **NO CONFLICT** | { = } ∩ { [ } = ∅ |
| `<statement_non_return>` | **NO CONFLICT** | { expr starters } ∩ { trap, thread, threadln } ∩ { if, switch, for, while, do } ∩ { break } = ∅ |
| `<ctrl_stmt_list>` | **NO CONFLICT** | { statement starters } ∩ { }, case, default } = ∅ |
| `<assign_tail>` | **NO CONFLICT** | { =, +=, -=, *=, /=, %= } ∩ { ;, ), ,, } } = ∅ |
| `<assign_op>` | **NO CONFLICT** | All distinct terminals |
| `<concat_tail>` | **NO CONFLICT** | { .. } ∩ FOLLOW = ∅ |
| `<or_tail>` | **NO CONFLICT** | { \|\| } ∩ FOLLOW = ∅ |
| `<and_tail>` | **NO CONFLICT** | { && } ∩ FOLLOW = ∅ |
| `<eq_tail>` | **NO CONFLICT** | { ==, != } ∩ FOLLOW = ∅ |
| `<rel_tail>` | **NO CONFLICT** | { <, >, <=, >= } ∩ FOLLOW = ∅ |
| `<add_tail>` | **NO CONFLICT** | { +, - } ∩ FOLLOW = ∅ |
| `<mul_tail>` | **NO CONFLICT** | { *, /, % } ∩ FOLLOW = ∅ |
| `<unary_expr>` | **NO CONFLICT** | { ! } ∩ { ++ } ∩ { -- } ∩ { postfix starters } = ∅ |
| `<postfix_expr>` | **NO CONFLICT** | All distinct terminals |
| `<postfix_chain>` | **NO CONFLICT** | { [ } ∩ { . } ∩ { ( } ∩ { ++ } ∩ { -- } ∩ FOLLOW = ∅ |
| `<array_access_dim2>` | **NO CONFLICT** | { [ } ∩ FOLLOW = ∅ |
| `<postfix_after_arr>` | **NO CONFLICT** | { . } ∩ { ( } ∩ { ++ } ∩ { -- } ∩ FOLLOW = ∅ |
| `<array_index>` | **NO CONFLICT** | { intlit } ∩ { id } = ∅ |
| `<arg_list>` | **NO CONFLICT** | { expr starters } ∩ { ) } = ∅ |
| `<arg_tail>` | **NO CONFLICT** | { , } ∩ { ) } = ∅ |
| `<io_stmt>` | **NO CONFLICT** | { trap } ∩ { thread } ∩ { threadln } = ∅ |
| `<print_tail>` | **NO CONFLICT** | { , } ∩ { ) } = ∅ |
| `<ctrl_struct>` | **NO CONFLICT** | { if } ∩ { switch } ∩ { for } ∩ { while } ∩ { do } = ∅ |
| `<else_opt>` | **NO CONFLICT** | { else } ∩ FOLLOW = ∅ |
| `<else_body>` | **NO CONFLICT** | { { } ∩ { if } = ∅ |
| `<case_list>` | **NO CONFLICT** | { case } ∩ { default, } } = ∅ |
| `<case_val>` | **NO CONFLICT** | All distinct terminals |
| `<default_opt>` | **NO CONFLICT** | { default } ∩ { } } = ∅ |
| `<break_opt>` | **NO CONFLICT** | { break } ∩ { case, default, } } = ∅ |
| `<for_init>` | **NO CONFLICT** | { local } ∩ { id } ∩ { ; } = ∅ |
| `<for_init_type>` | **NO CONFLICT** | All distinct terminals |
| `<for_cond>` | **NO CONFLICT** | { condition starters } ∩ { ; } = ∅ |
| `<for_update>` | **NO CONFLICT** | { id } ∩ { ++ } ∩ { -- } ∩ { ) } = ∅ |
| `<for_update_tail>` | **NO CONFLICT** | { ++ } ∩ { -- } ∩ { =, +=, -=, *=, /=, %= } = ∅ |
| `<cond_or_tail>` | **NO CONFLICT** | { \|\| } ∩ { ) } = ∅ |
| `<cond_and_tail>` | **NO CONFLICT** | { && } ∩ { \|\|, ) } = ∅ |
| `<cond_not>` | **NO CONFLICT** | { ! } ∩ { true, false, (, id, ... } = ∅ |
| `<cond_atom>` | **NO CONFLICT** | All distinct first terminals |
| `<cond_after_id>` | **NO CONFLICT** | { ( } ∩ { cond_after_id_no_call starters } = ∅ |
| `<cond_after_call>` | **NO CONFLICT** | FOLLOW ∩ { postfix starters } = ∅ |
| `<cond_comparison_opt>` | **NO CONFLICT** | { ==, !=, <, >, <=, >= } ∩ { &&, \|\|, ) } = ∅ |
| `<cond_postfix_no_call>` | **NO CONFLICT** | { [ } ∩ { . } ∩ { ++ } ∩ { -- } ∩ FOLLOW = ∅ |
| `<comp_op>` | **NO CONFLICT** | All distinct terminals |
| `<main_content>` | **NO CONFLICT** | { using } ∩ { local } ∩ { statement starters } ∩ { return } = ∅ |

### 6.2 Resolution of `<other_decl>` func Productions

The productions:
- `<other_decl> → func <nonvoid_ret_type> id ( <param_list> ) { <function_body_nonvoid> }`
- `<other_decl> → func void id ( <param_list> ) { <function_body_void> }`

Both start with `func`. However, after consuming `func`, the parser sees either:
- A type keyword (`int`, `long`, `float`, `double`, `char`, `string`, `bool`, `id`) → nonvoid path
- `void` → void path

This is resolved by 1 token lookahead after `func`:
- FIRST(`<nonvoid_ret_type>`) = { int, long, float, double, char, string, bool, id }
- FIRST(void) = { void }
- { int, long, float, double, char, string, bool, id } ∩ { void } = ∅

**RESOLUTION**: The grammar is LL(1) because after consuming `func`, the next token uniquely determines which production to use.

### 6.3 FIRST/FOLLOW Conflict Check (Nullable Productions)

For nullable productions (A → λ), FIRST(α) ∩ FOLLOW(A) must be empty for all A → α where A → λ.

| Non-terminal | Nullable? | FIRST(non-λ) ∩ FOLLOW | Status |
|--------------|-----------|------------------------|--------|
| `<multi_global>` | Yes | { , } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<weave_arr_content>` | Yes | { {, arr_elem starters } ∩ { } } = ∅ | **NO CONFLICT** |
| `<weave_field_list_tail>` | Yes | { , } ∩ { } } = ∅ | **NO CONFLICT** |
| `<weave_inst_cont>` | Yes | { , } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<weave_arr_cont>` | Yes | { , } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<multi_typed>` | Yes | { , } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<value_list_tail>` | Yes | { , } ∩ { } } = ∅ | **NO CONFLICT** |
| `<array_dim2_opt>` | Yes | { [ } ∩ { id, ,, ;, ) } = ∅ | **NO CONFLICT** |
| `<arr_init_opt_1d>` | Yes | { = } ∩ { ;, , } = ∅ | **NO CONFLICT** |
| `<arr_init_content_1d>` | Yes | { arr_elem starters } ∩ { } } = ∅ | **NO CONFLICT** |
| `<arr_init_opt_2d>` | Yes | { = } ∩ { ;, , } = ∅ | **NO CONFLICT** |
| `<arr_init_content_2d>` | Yes | { { } ∩ { } } = ∅ | **NO CONFLICT** |
| `<elem_2d_tail>` | Yes | { , } ∩ { } } = ∅ | **NO CONFLICT** |
| `<elem_list>` | Yes | { arr_elem starters } ∩ { } } = ∅ | **NO CONFLICT** |
| `<elem_1d_tail>` | Yes | { , } ∩ { } } = ∅ | **NO CONFLICT** |
| `<field_list>` | Yes | { field_type starters } ∩ { } } = ∅ | **NO CONFLICT** |
| `<field_arr_opt>` | Yes | { [ } ∩ { ,, ; } = ∅ | **NO CONFLICT** |
| `<field_cont>` | Yes | { , } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<ret_type_suffix>` | Yes | { [ } ∩ { id } = ∅ | **NO CONFLICT** |
| `<ret_id_suffix>` | Yes | { [, . } ∩ { id } = ∅ | **NO CONFLICT** |
| `<param_list>` | Yes | { param_type starters } ∩ { ) } = ∅ | **NO CONFLICT** |
| `<param_arr_opt>` | Yes | { [ } ∩ { ,, ) } = ∅ | **NO CONFLICT** |
| `<param_cont>` | Yes | { , } ∩ { ) } = ∅ | **NO CONFLICT** |
| `<using_block>` | Yes | { using } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<using_cont>` | Yes | { , } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<local_block>` | Yes | { local } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<multi_local>` | Yes | { , } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<ctrl_stmt_list>` | Yes | { statement starters } ∩ { }, case, default } = ∅ | **NO CONFLICT** |
| `<assign_tail>` | Yes | { assign_op starters } ∩ { ;, ), ,, } } = ∅ | **NO CONFLICT** |
| `<concat_tail>` | Yes | { .. } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<or_tail>` | Yes | { \|\| } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<and_tail>` | Yes | { && } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<eq_tail>` | Yes | { ==, != } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<rel_tail>` | Yes | { <, >, <=, >= } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<add_tail>` | Yes | { +, - } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<mul_tail>` | Yes | { *, /, % } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<postfix_chain>` | Yes | { [, ., (, ++, -- } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<array_access_dim2>` | Yes | { [ } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<postfix_after_arr>` | Yes | { ., (, ++, -- } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<arg_list>` | Yes | { expr starters } ∩ { ) } = ∅ | **NO CONFLICT** |
| `<arg_tail>` | Yes | { , } ∩ { ) } = ∅ | **NO CONFLICT** |
| `<print_tail>` | Yes | { , } ∩ { ) } = ∅ | **NO CONFLICT** |
| `<else_opt>` | Yes | { else } ∩ FOLLOW = ∅ | **NO CONFLICT** |
| `<case_list>` | Yes | { case } ∩ { default, } } = ∅ | **NO CONFLICT** |
| `<default_opt>` | Yes | { default } ∩ { } } = ∅ | **NO CONFLICT** |
| `<break_opt>` | Yes | { break } ∩ { case, default, } } = ∅ | **NO CONFLICT** |
| `<for_init>` | Yes | { local, id } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<for_cond>` | Yes | { condition starters } ∩ { ; } = ∅ | **NO CONFLICT** |
| `<for_update>` | Yes | { id, ++, -- } ∩ { ) } = ∅ | **NO CONFLICT** |
| `<cond_or_tail>` | Yes | { \|\| } ∩ { ) } = ∅ | **NO CONFLICT** |
| `<cond_and_tail>` | Yes | { && } ∩ { \|\|, ) } = ∅ | **NO CONFLICT** |
| `<cond_after_call>` | Yes | { postfix starters } ∩ { &&, \|\|, ) } = ∅ | **NO CONFLICT** |
| `<cond_comparison_opt>` | Yes | { comp_op starters } ∩ { &&, \|\|, ) } = ∅ | **NO CONFLICT** |
| `<cond_postfix_no_call>` | Yes | { [, ., ++, -- } ∩ FOLLOW = ∅ | **NO CONFLICT** |

---

## 7. Conclusion

**The PORTIA grammar is LL(1) compliant.**

- **No FIRST/FIRST conflicts exist** among alternative productions for any non-terminal.
- **No FIRST/FOLLOW conflicts exist** for any nullable production.
- The `func` productions in `<other_decl>` are resolved by examining the token following `func` (either `void` or a non-void type), which have disjoint FIRST sets.

The grammar can be parsed by a deterministic top-down parser with single-token lookahead.
