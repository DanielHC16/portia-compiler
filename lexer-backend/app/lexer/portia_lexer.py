"""
PORTIA Lexical Analyzer
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Token:
    tokenName: str
    tokenType: str
    tokenLine: int
    tokenCol: int
    
    def to_dict(self):
        return {
            "tokenName": self.tokenName,
            "tokenType": self.tokenType,
            "tokenLine": self.tokenLine,
            "tokenCol": self.tokenCol
        }


class LexicalAnalyzer:
    # === CHARACTER CLASS DEFINITIONS ===
    alpha_small = list('abcdefghijklmnopqrstuvwxyz')
    alpha_capital = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    alphabetic_chars = alpha_small + alpha_capital
    
    zero = ['0']
    digit = list('123456789')
    numbers = zero + digit
    
    alphanum = alphabetic_chars + numbers
    
    whitespace = [' ', '\t']
    newline = ['\n']
    
    ascii = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t')
    
    # === DELIMITER DEFINITIONS ===
    whitespace_delim = whitespace + newline + ['/'] # add to docs
    block_delim = whitespace + newline + ['{', '/'] # update
    loop_delim = whitespace + newline + ['(', '/'] # update
    break_ret_cont_delim = whitespace + newline + [';', '/']
    default_delim = whitespace + newline + [':', '/']
    case_delim = whitespace + newline + ['(', '/']
    func_delim = whitespace + newline + ['(']
    
    negative_delim = alphanum + whitespace + ['(', '/', '+', '.'] + newline
    sign_delim = alphanum + whitespace + ['(', '/', '+', '-', '{', '"', '!'] + newline
    marithmetic_delim = alphanum + whitespace + ['(', '/', '+', '-'] + newline
    slash_delim = alphanum + whitespace + ['(', '+', '-', '\n']
    modulo_delim = alphanum + whitespace + ['(', '+', '-', '/'] + newline
    logical_delim = alphabetic_chars + whitespace + ['(', '/', '!'] + newline
    exclamation_delim = alphabetic_chars + whitespace + ['(', '/', '!'] + newline
    equal_delim = alphanum + whitespace + ['(', '/', '+', '-', '"', '!', '{'] + newline
    increment_delim = alphabetic_chars + whitespace + [';', ')', '/', '-', '*', '%', '(', ']', ','] + newline
    decrement_delim = alphabetic_chars + whitespace + [';', ')', '/', '+', '*', '%', '(', ']', ','] + newline
    
    open_paren_delim = alphanum + whitespace + ['"', '!', ')', '+', '-', '/', '('] + newline
    close_paren_delim = alphanum + ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '{', ';', ')', '(', ':', ']', '}', '"', ','] + whitespace + newline
    semicolon_delim = alphanum + whitespace + ['}', '/', '(', ')'] + newline
    open_bracket_delim = alphanum + whitespace + ['/', '\n', '(', ']', '+', '-']
    close_bracket_delim = ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', ')', ']', '}', ':', ';', ','] + whitespace + newline
    open_curly_delim = alphanum + whitespace + ['{', '}', '/', '"', '(', '+', '-', '!'] + newline
    close_curly_delim = alphanum + whitespace + [';', '/', ',', '}', '+', '-'] + newline
    comma_delim = alphanum + whitespace + ['/', '(', '{', '"', '+', '-'] + newline
    colon_delim = alphanum + whitespace + ['/', '}'] + newline
    dot_delim = alphanum + whitespace + ['\n', '/']
    
    iden_delim = [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', '{', '}', ':', ';'] + whitespace + newline
    nbl_delim = ['+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', ')', ']', '}', ':', ';'] + whitespace + newline
    str_lit_delim = whitespace + newline + ['!', '&', '|', '+', ')', ',', ';', '/', ':', '=', '}']
    
    multi_line_start_found = False
    
    
    def transition(self, currState: str, currChar: str) -> str:
        
        match currState:
            # === INITIAL STATE ===
            case 's0':
                match currChar:
                    # Keywords starting characters
                    case 'b': return 's1'    # bool, break
                    case 'c': return 's11'   # case, char, const
                    case 'd': return 's25'   # default, do, double
                    case 'e': return 's40'   # else
                    case 'f': return 's45'   # false, float, for, func
                    case 'g': return 's63'   # global
                    case 'i': return 's68'   # if, int
                    case 'l': return 's75'   # local, long
                    case 'm': return 's82'   # main
                    case 'r': return 's86'   # return
                    case 's': return 's91'   # string, switch
                    case 't': return 's97'   # thread, threadln, trap, true
                    case 'u': return 's115'  # using
                    case 'v': return 's120'  # var, void
                    case 'w': return 's127'  # while, weave
                    
                    # Operators
                    case '-': return 's152'
                    case '+': return 's158'
                    case '*': return 's164'
                    case '/': return 's168'
                    case '%': return 's172'
                    case '!': return 's182'
                    case '=': return 's186'
                    case '&': return 's176'
                    case '|': return 's179'
                    case '<': return 's193'
                    case '>': return 's197'
                    
                    # Delimiters
                    case '(': return 's190'
                    case ')': return 's192'
                    case '[': return 's194'
                    case ']': return 's196'
                    case '{': return 's198'
                    case '}': return 's200'
                    case ';': return 's202'
                    case ',': return 's204'
                    case ':': return 's206'
                    case '.': return 's208'
                    
                    # String
                    case '"': return 's277'
                    
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === KEYWORDS FSA - PART 1 (States 1-62) ===
            
            # BOOL (s1-s5)
            case 's1':
                match currChar:
                    case 'o': return 's2'
                    case 'r': return 's6'   # break path
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's2':
                match currChar:
                    case 'o': return 's3'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's3':
                match currChar:
                    case 'l': return 's4'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's4':  # BOOL final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # BREAK (s6-s10)
            case 's6':
                match currChar:
                    case 'e': return 's7'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's7':
                match currChar:
                    case 'a': return 's8'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's8':
                match currChar:
                    case 'k': return 's9'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's9':  # BREAK final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # CASE, CHAR, CONST (s11-s24)
            case 's11':
                match currChar:
                    case 'a': return 's12'  # case
                    case 'h': return 's16'  # char
                    case 'o': return 's20'  # const
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's12':
                match currChar:
                    case 's': return 's13'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's13':
                match currChar:
                    case 'e': return 's14'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's14':  # CASE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's16':
                match currChar:
                    case 'a': return 's17'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's17':
                match currChar:
                    case 'r': return 's18'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's18':  # CHAR final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's20':
                match currChar:
                    case 'n': return 's21'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's21':
                match currChar:
                    case 's': return 's22'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's22':
                match currChar:
                    case 't': return 's23'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's23':  # CONST final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # DEFAULT, DO, DOUBLE (s25-s39)
            case 's25':
                match currChar:
                    case 'e': return 's26'  # default
                    case 'o': return 's33'  # do, double
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's26':
                match currChar:
                    case 'f': return 's27'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's27':
                match currChar:
                    case 'a': return 's28'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's28':
                match currChar:
                    case 'u': return 's29'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's29':
                match currChar:
                    case 'l': return 's30'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's30':
                match currChar:
                    case 't': return 's31'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's31':  # DEFAULT final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's33':
                match currChar:
                    case 'u': return 's35'  # double
                    case 'ANY': return 'DEFINED'  # do
                    case _: return 'UNDEFINED'
            case 's34':  # DO final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's35':
                match currChar:
                    case 'b': return 's36'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's36':
                match currChar:
                    case 'l': return 's37'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's37':
                match currChar:
                    case 'e': return 's38'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's38':  # DOUBLE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ELSE (s40-s44)
            case 's40':
                match currChar:
                    case 'l': return 's41'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's41':
                match currChar:
                    case 's': return 's42'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's42':
                match currChar:
                    case 'e': return 's43'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's43':  # ELSE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # FALSE, FLOAT, FOR, FUNC (s45-s62)
            case 's45':
                match currChar:
                    case 'a': return 's46'  # false
                    case 'l': return 's51'  # float
                    case 'o': return 's56'  # for
                    case 'u': return 's59'  # func
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's46':
                match currChar:
                    case 'l': return 's47'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's47':
                match currChar:
                    case 's': return 's48'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's48':
                match currChar:
                    case 'e': return 's49'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's49':  # FALSE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's51':
                match currChar:
                    case 'o': return 's52'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's52':
                match currChar:
                    case 'a': return 's53'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's53':
                match currChar:
                    case 't': return 's54'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's54':  # FLOAT final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's56':
                match currChar:
                    case 'r': return 's57'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's57':  # FOR final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's59':
                match currChar:
                    case 'n': return 's60'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's60':
                match currChar:
                    case 'c': return 's61'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's61':  # FUNC final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === KEYWORDS FSA - PART 2 (States 63-126) ===
            
            # GLOBAL (s63-s68)
            case 's63':
                match currChar:
                    case 'l': return 's64'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's64':
                match currChar:
                    case 'o': return 's65'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's65':
                match currChar:
                    case 'b': return 's66'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's66':
                match currChar:
                    case 'a': return 's67'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's67':
                match currChar:
                    case 'l': return 's68'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's68':  # GLOBAL final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # IF, INT (s69-s74)
            case 's69':
                match currChar:
                    case 'f': return 's70'  # if
                    case 'n': return 's71'  # int
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's70':  # IF final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's71':
                match currChar:
                    case 't': return 's72'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's72':  # INT final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # LOCAL, LONG (s75-s85)
            case 's75':
                match currChar:
                    case 'o': return 's76'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's76':
                match currChar:
                    case 'c': return 's77'  # local
                    case 'n': return 's81'  # long
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's77':
                match currChar:
                    case 'a': return 's78'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's78':
                match currChar:
                    case 'l': return 's79'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's79':  # LOCAL final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's81':
                match currChar:
                    case 'g': return 's82'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's82':  # LONG final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # MAIN (s83-s85)
            case 's83':
                match currChar:
                    case 'a': return 's84'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's84':
                match currChar:
                    case 'i': return 's85'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's85':
                match currChar:
                    case 'n': return 's86'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's86':  # MAIN final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # RETURN (s87-s90)
            case 's87':
                match currChar:
                    case 'e': return 's88'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's88':
                match currChar:
                    case 't': return 's89'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's89':
                match currChar:
                    case 'u': return 's90'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's90':
                match currChar:
                    case 'r': return 's91'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's91':
                match currChar:
                    case 'n': return 's92'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's92':  # RETURN final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # STRING, SWITCH (s93-s102)
            case 's93':
                match currChar:
                    case 't': return 's94'  # string
                    case 'w': return 's98'  # switch
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's94':
                match currChar:
                    case 'r': return 's95'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's95':
                match currChar:
                    case 'i': return 's96'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's96':
                match currChar:
                    case 'n': return 's97'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's97':
                match currChar:
                    case 'g': return 's98'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's98':  # STRING final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's99':
                match currChar:
                    case 'i': return 's100'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's100':
                match currChar:
                    case 't': return 's101'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's101':
                match currChar:
                    case 'c': return 's102'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's102':
                match currChar:
                    case 'h': return 's103'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's103':  # SWITCH final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # THREAD, THREADLN, TRAP, TRUE (s104-s114)
            case 's104':
                match currChar:
                    case 'h': return 's105'  # thread, threadln
                    case 'r': return 's111'  # trap, true
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's105':
                match currChar:
                    case 'r': return 's106'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's106':
                match currChar:
                    case 'e': return 's107'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's107':
                match currChar:
                    case 'a': return 's108'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's108':
                match currChar:
                    case 'd': return 's109'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's109':
                match currChar:
                    case 'l': return 's110'  # threadln
                    case 'ANY': return 'DEFINED'  # thread
                    case _: return 'UNDEFINED'
            case 's110':  # THREAD final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's111':
                match currChar:
                    case 'n': return 's112'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's112':  # THREADLN final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's113':
                match currChar:
                    case 'a': return 's114'  # trap
                    case 'u': return 's115'  # true
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's114':
                match currChar:
                    case 'p': return 's115'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's115':  # TRAP final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's116':
                match currChar:
                    case 'e': return 's117'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's117':  # TRUE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === KEYWORDS FSA - PART 3 (States 115-151) ===
            
            # USING (s118-s119)
            case 's118':
                match currChar:
                    case 's': return 's119'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's119':
                match currChar:
                    case 'i': return 's120'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's120':
                match currChar:
                    case 'n': return 's121'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's121':
                match currChar:
                    case 'g': return 's122'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's122':  # USING final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # VAR, VOID (s123-s126)
            case 's123':
                match currChar:
                    case 'a': return 's124'  # var
                    case 'o': return 's125'  # void
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's124':
                match currChar:
                    case 'r': return 's125'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's125':  # VAR final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's126':
                match currChar:
                    case 'i': return 's127'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's127':
                match currChar:
                    case 'd': return 's128'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's128':  # VOID final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # WEAVE, WHILE (s129-s138)
            case 's129':
                match currChar:
                    case 'e': return 's130'  # weave
                    case 'h': return 's133'  # while
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's130':
                match currChar:
                    case 'a': return 's131'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's131':
                match currChar:
                    case 'v': return 's132'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's132':
                match currChar:
                    case 'e': return 's133'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's133':  # WEAVE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's134':
                match currChar:
                    case 'i': return 's135'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's135':
                match currChar:
                    case 'l': return 's136'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's136':
                match currChar:
                    case 'e': return 's137'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's137':  # WHILE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === OPERATORS FSA (States 152-189) ===
            
            case 's152':  # After -
                match currChar:
                    case '-': return 's154'
                    case '=': return 's156'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's154':  # After --
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's156':  # After -=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's158':  # After +
                match currChar:
                    case '+': return 's160'
                    case '=': return 's162'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's160':  # After ++
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's162':  # After +=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's164':  # After *
                match currChar:
                    case '=': return 's166'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's166':  # After *=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's168':  # After /
                match currChar:
                    case '/': return 's271'  # Single-line comment
                    case '*': return 's273'  # Multi-line comment
                    case '=': return 's170'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's170':  # After /=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's172':  # After %
                match currChar:
                    case '=': return 's174'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's174':  # After %=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's176':  # After &
                match currChar:
                    case '&': return 's177'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's177':  # After &&
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's179':  # After |
                match currChar:
                    case '|': return 's180'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's180':  # After ||
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's182':  # After !
                match currChar:
                    case '=': return 's184'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's184':  # After !=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's186':  # After =
                match currChar:
                    case '=': return 's188'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's188':  # After ==
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's193':  # After <
                match currChar:
                    case '=': return 's195'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's195':  # After <=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's197':  # After >
                match currChar:
                    case '=': return 's199'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's199':  # After >=
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === DELIMITERS FSA (States 190-218) ===
            
            case 's190' | 's192' | 's194' | 's196' | 's198' | 's200' | 's202' | 's204' | 's206' | 's208':  # Delimiters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === COMMENTS FSA (States 271-276) ===
            
            case 's271':  # Single-line comment
                match currChar:
                    case '\n': return 's272'
                    case _ if currChar in self.ascii: return 's271'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's272':  # Single comment end
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's273':  # Multi-line comment
                match currChar:
                    case '*': return 's274'
                    case _ if currChar in self.ascii or currChar == '\n': return 's273'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's274':  # After * in multi-line
                match currChar:
                    case '/': return 's275'
                    case '*': return 's274'
                    case _: return 's273'
            case 's275':  # Multi comment end
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === STRING LITERALS FSA (States 277-278) ===
            
            case 's277':  # Inside string
                match currChar:
                    case '"': return 's278'
                    case '\\': return 's279'
                    case '\n': return 'UNDEFINED'
                    case _ if currChar in self.ascii: return 's277'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's278':  # String end
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's279':  # After backslash
                match currChar:
                    case '"' | '\\' | 'n' | 't': return 's277'
                    case _: return 'UNDEFINED'
            
            # === NUMBER LITERALS FSA (States 280-337) ===
            
            case 's280':  # Number start
                match currChar:
                    case _ if currChar in self.numbers: return 's280'
                    case '.': return 's337'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's337':  # After decimal point (fractional)
                match currChar:
                    case _ if currChar in self.numbers: return 's337'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # === IDENTIFIERS FSA (State 220) ===
            
            case 's220':  # Identifier
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's220'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case _:
                return 'UNDEFINED'
        
        return 'UNDEFINED'
    
    
    def scan(self, code: str) -> Dict[str, Any]:
        """
        Main scanning function - Spec compliant tokenization with delimiter validation
        """
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        
        tokens: List[Token] = []
        errors: List[Dict[str, Any]] = []
        
        i = 0
        line = 1
        col = 1
        length = len(code)
        
        def add_token(lexeme: str, token_type: str, tok_line: int, tok_col: int):
            token = Token(tokenName=lexeme, tokenType=token_type, tokenLine=tok_line, tokenCol=tok_col)
            tokens.append(token)
        
        def add_error(message: str, start_idx: int, end_idx: int, err_line: int, err_col: int):
            errors.append({
                'message': message,
                'line': err_line,
                'column': err_col,
                'start_index': start_idx,
                'end_index': end_idx
            })
        
        def get_next_char():
            """Get the next character after current position, or None if at end"""
            return code[i] if i < length else None
        
        def check_delimiter(token_type: str, next_char: str) -> bool:
            """
            Validate that the next character is a valid delimiter for this token type
            Based on FSA delimiter specifications
            
            Returns True only if next_char matches the required delimiter for this token_type
            """
            # Binary operators that REQUIRE a right operand (cannot be followed by newline/EOF alone)
            binary_operators = ['plus', 'minus', 'multiply', 'divide', 'modulo', 'assign',
                               'equal_equal', 'not_equal', 'less_than', 'greater_than',
                               'less_equal', 'greater_equal', 'logical_and', 'logical_or',
                               'add_assign', 'minus_assign', 'mult_assign',
                               'div_assign', 'modulo_assign', 'concat']
            
            # Keywords that require specific following characters
            must_have_delimiter = ['break', 'return', 'main', 'trap', 'thread', 'threadln', 'default']
            
            # Delimiters that indicate incomplete statements at EOF
            incomplete_at_eof = ['dot', 'comma']  # . and , suggest incomplete statement
            
            # Check for incomplete expressions - operators at EOF or followed by only whitespace/newline
            if token_type in binary_operators:
                # Binary operators MUST be followed by an operand, not EOF/newline
                if next_char is None or next_char == '\n':
                    return False  # Incomplete expression
            
            # Check for incomplete statements - certain delimiters shouldn't be at EOF
            if token_type in incomplete_at_eof:
                if next_char is None:
                    return False  # Incomplete statement
            
            # End of file handling for other tokens
            if next_char is None:
                # These tokens MUST have a delimiter after them - EOF is invalid
                if token_type in must_have_delimiter:
                    return False  # These require specific delimiters
                return True  # Other tokens (identifiers, literals, etc.) can be at EOF
            
            # Define delimiter classes based on FSA spec
            # Keywords with whitespace delimiter
            whitespace_keywords = ['bool', 'char', 'const', 'double', 'float', 'func',
                                   'global', 'int', 'local', 'long', 'string', 'using',
                                   'var', 'void', 'weave']
            
            # Keywords with specific delimiters
            loop_delimiters = ['if', 'switch', 'for', 'while']  # Require ( or whitespace or /
            block_delimiters = ['do', 'else']  # Require { or whitespace or /
            special_delimiters = {
                'break': [';', ' ', '\t', '\n', '/'],  # semicolon or whitespace
                'case': [' ', '\t', '\n', '/', '('],  # whitespace or / or (
                'default': [':', ' ', '\t', '\n', '/'],  # colon or whitespace
                'main': ['('],  # must be followed by (
                'trap': ['('],
                'thread': ['('],
                'threadln': ['('],
                'return': [';', ' ', '\t', '\n', '/'],  # return_delim
                'bool_lit': self.nbl_delim,  # true, false
            }
            
            # Check keywords first
            if token_type in whitespace_keywords:
                return next_char in self.whitespace_delim
            
            if token_type in loop_delimiters:
                return next_char in self.loop_delim
            
            if token_type in block_delimiters:
                return next_char in self.block_delim
            
            if token_type in special_delimiters:
                return next_char in special_delimiters[token_type]
            
            # Identifiers
            if token_type == 'identifier':
                return next_char in self.iden_delim
            
            # Numeric literals
            if token_type in ['int_lit', 'long_lit', 'float_lit', 'double_lit']:
                return next_char in self.nbl_delim
            
            # String and char literals
            if token_type in ['string_lit']:
                return next_char in self.str_lit_delim
            
            if token_type == 'char_lit':
                return next_char in self.nbl_delim
            
            # Operators - based on FSA spec
            operator_delims = {
                'plus': self.sign_delim,
                'minus': self.negative_delim,
                'multiply': self.marithmetic_delim,
                'divide': self.slash_delim,
                'modulo': self.modulo_delim,
                'assign': self.equal_delim,
                'equal_equal': self.sign_delim,
                'not_equal': self.sign_delim,
                'less_than': self.alphanum + self.whitespace + ['=', '/', '('] + self.newline,  # asign_delim
                'greater_than': self.alphanum + self.whitespace + ['=', '/', '('] + self.newline,  # asign_delim
                'less_equal': self.alphanum + self.whitespace + ['/', '('] + self.newline,  # asign_delim
                'greater_equal': self.alphanum + self.whitespace + ['/', '('] + self.newline,  # asign_delim
                'logical_and': self.logical_delim,
                'logical_or': self.logical_delim,
                'not': self.exclamation_delim,
                'increment': self.increment_delim,
                'decrement': self.decrement_delim,
                'add_assign': self.sign_delim,
                'minus_assign': self.sign_delim,
                'mult_assign': self.sign_delim,
                'div_assign': self.sign_delim,
                'modulo_assign': self.sign_delim,
                'concat': self.alphanum + self.whitespace + self.newline + ['/'],  # concat_delim
            }
            
            if token_type in operator_delims:
                return next_char in operator_delims[token_type]
            
            # Delimiters
            delimiter_delims = {
                'open_paren': self.open_paren_delim,
                'close_paren': self.close_paren_delim,
                'open_bracket': self.open_bracket_delim,
                'close_bracket': self.close_bracket_delim,
                'open_curly': self.open_curly_delim,
                'close_curly': self.close_curly_delim,
                'semicolon': self.semicolon_delim,
                'comma': self.comma_delim,
                'colon': self.colon_delim,
                'dot': self.dot_delim,
            }
            
            if token_type in delimiter_delims:
                return next_char in delimiter_delims[token_type]
            
            # Comments - no delimiter check needed
            if token_type in ['single_comment', 'multi_comment']:
                return True
            
            # Default: allow if we don't have specific rules
            return True
        
        # All 38 PORTIA reserved words per TOKEN_REFERENCE.md
        keywords = {
            # Scope
            'local': 'local', 'global': 'global', 'using': 'using',
            # Main
            'main': 'main',
            # Data types
            'int': 'int', 'bool': 'bool', 'string': 'string',
            'float': 'float', 'double': 'double', 'long': 'long',
            'char': 'char', 'void': 'void', 'weave': 'weave',
            # Declarations
            'const': 'const', 'var': 'var',
            # I/O
            'trap': 'trap', 'thread': 'thread', 'threadln': 'threadln',
            # Boolean literals
            'true': 'bool_lit', 'false': 'bool_lit',
            # Functions
            'func': 'func', 'return': 'return',
            # Conditionals
            'if': 'if', 'else': 'else', 'switch': 'switch',
            'case': 'case', 'default': 'default',
            # Loops
            'while': 'while', 'do': 'do', 'for': 'for',
            # Loop control
            'break': 'break'
        }
        
        while i < length:
            start_line = line
            start_col = col
            start_i = i
            ch = code[i]
            
            # Skip whitespace
            if ch in self.whitespace:
                i += 1
                col += 1
                continue
            
            # Handle newline
            if ch == '\n':
                i += 1
                line += 1
                col = 1
                continue
            
            # ============ COMMENTS ============
            
            # Single-line comment: // ...
            if ch == '/' and i + 1 < length and code[i + 1] == '/':
                i += 2
                col += 2
                while i < length and code[i] != '\n':
                    i += 1
                    col += 1
                lexeme = code[start_i:i]
                add_token(lexeme, 'single_comment', start_line, start_col)
                continue
            
            # Multi-line comment: /* ... */
            if ch == '/' and i + 1 < length and code[i + 1] == '*':
                i += 2
                col += 2
                closed = False
                while i < length - 1:
                    if code[i] == '\n':
                        line += 1
                        col = 1
                    else:
                        col += 1
                    if code[i] == '*' and code[i + 1] == '/':
                        i += 2
                        col += 2
                        closed = True
                        break
                    i += 1
                lexeme = code[start_i:i]
                if not closed:
                    add_error(f"Lexical Error: Unterminated multi-line comment", start_i, i, start_line, start_col)
                add_token(lexeme, 'multi_comment', start_line, start_col)
                continue
            
            # ============ STRING LITERALS ============
            
            # String literal: "..."
            if ch == '"':
                i += 1
                col += 1
                closed = False
                has_invalid_escape = False
                while i < length:
                    if code[i] == '\\' and i + 1 < length:
                        # Check for valid escape sequences: \n, \t, \", \'
                        next_ch = code[i + 1]
                        if next_ch not in ['n', 't', '"', "'"]:
                            has_invalid_escape = True
                        i += 2
                        col += 2
                        continue
                    if code[i] == '"':
                        i += 1
                        col += 1
                        closed = True
                        break
                    if code[i] == '\n':
                        break
                    i += 1
                    col += 1
                lexeme = code[start_i:i]
                if not closed:
                    add_error(f"Lexical Error: Unterminated string literal", start_i, i, start_line, start_col)
                elif has_invalid_escape:
                    add_error(f"Lexical Error: Invalid escape sequence in string (only \\n, \\t, \\\", \\' allowed)", start_i, i, start_line, start_col)
                else:
                    # Validate delimiter for string literals
                    next_char = get_next_char()
                    if not check_delimiter('string_lit', next_char):
                        add_error(f"Lexical Error: String literal not properly delimited (expected valid delimiter, found '{next_char}')", start_i, i, start_line, start_col)
                    else:
                        add_token(lexeme, 'string_lit', start_line, start_col)
                continue
            
            # ============ CHARACTER LITERALS ============
            
            # Character literal: '.'
            if ch == "'":
                i += 1
                col += 1
                char_valid = False
                
                if i < length:
                    if code[i] == '\\' and i + 1 < length:
                        # Escape sequence
                        next_ch = code[i + 1]
                        if next_ch in ['n', 't', '"', "'"]:
                            i += 2
                            col += 2
                            char_valid = True
                        else:
                            i += 2
                            col += 2
                    elif code[i] != "'" and code[i] != '\n':
                        # Single ASCII character
                        i += 1
                        col += 1
                        char_valid = True
                
                # Check for closing quote
                if i < length and code[i] == "'":
                    i += 1
                    col += 1
                    lexeme = code[start_i:i]
                    if char_valid:
                        # Validate delimiter for char literals
                        next_char = get_next_char()
                        if not check_delimiter('char_lit', next_char):
                            add_error(f"Lexical Error: Character literal not properly delimited (expected valid delimiter, found '{next_char}')", start_i, i, start_line, start_col)
                        else:
                            add_token(lexeme, 'char_lit', start_line, start_col)
                    else:
                        add_error(f"Lexical Error: Empty or invalid character literal", start_i, i, start_line, start_col)
                else:
                    lexeme = code[start_i:i]
                    add_error(f"Lexical Error: Unterminated or invalid character literal", start_i, i, start_line, start_col)
                continue
            
            # ============ NUMERIC LITERALS ============
            
            # Numbers (whole and fractional)
            if ch in self.numbers:
                has_dot = False
                while i < length:
                    if code[i] in self.numbers:
                        i += 1
                        col += 1
                    elif code[i] == '.' and not has_dot and i + 1 < length and code[i + 1] in self.numbers:
                        has_dot = True
                        i += 1
                        col += 1
                    elif code[i] == '.' and not has_dot:
                        # Could be concatenation operator, stop here
                        break
                    else:
                        break
                
                lexeme = code[start_i:i]
                
                # Classify based on LITERALS.md specification
                if has_dot:
                    # Fractional literal
                    parts = lexeme.split('.')
                    whole_digits = len(parts[0]) if parts[0] else 0
                    frac_digits = len(parts[1]) if len(parts) > 1 else 0
                    total_digits = whole_digits + frac_digits
                    
                    # float: up to 7 significant digits
                    # double: up to 16 significant digits
                    if total_digits <= 7:
                        token_type = 'float_lit'
                    else:
                        token_type = 'double_lit'
                    
                    # Check limits per LITERALS.md
                    if whole_digits > 19 or frac_digits > 16:
                        add_error(f"Lexical Error: Fractional literal exceeds allowed precision", start_i, i, start_line, start_col)
                else:
                    # Whole literal
                    digit_count = len(lexeme)
                    
                    # int: up to 10 digits (max 2,147,483,647)
                    # long: up to 19 digits (max 9,223,372,036,854,775,807)
                    if digit_count <= 10:
                        token_type = 'int_lit'
                    elif digit_count <= 19:
                        token_type = 'long_lit'
                    else:
                        token_type = 'long_lit'
                        add_error(f"Lexical Error: Whole literal exceeds 19 digits", start_i, i, start_line, start_col)
                
                # Validate delimiter for numeric literals
                next_char = get_next_char()
                if not check_delimiter(token_type, next_char):
                    add_error(f"Lexical Error: Numeric literal '{lexeme}' not properly delimited (expected valid delimiter, found '{next_char}')", start_i, i, start_line, start_col)
                    continue
                
                add_token(lexeme, token_type, start_line, start_col)
                continue
            
            # ============ IDENTIFIERS AND KEYWORDS ============
            
            # Identifiers (start with letter or underscore)
            if ch in self.alphabetic_chars or ch == '_':
                while i < length and (code[i] in self.alphanum or code[i] == '_'):
                    i += 1
                    col += 1
                lexeme = code[start_i:i]
                
                # IDENTIFIERS.md: 1-25 characters max
                if len(lexeme) > 25:
                    add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", start_i, i, start_line, start_col)
                    continue
                
                # Check if keyword or identifier
                token_type = keywords.get(lexeme, 'identifier')
                
                # Validate delimiter for keywords and identifiers
                next_char = get_next_char()
                if not check_delimiter(token_type, next_char):
                    add_error(f"Lexical Error: Token '{lexeme}' not properly delimited (expected valid delimiter, found '{next_char}')", start_i, i, start_line, start_col)
                    continue
                
                add_token(lexeme, token_type, start_line, start_col)
                continue
            
            # ============ OPERATORS ============
            
            # Two-character operators (check first to avoid conflicts)
            if i + 1 < length:
                two_char = code[i:i+2]
                two_char_ops = {
                    '==': 'equal_equal', '!=': 'not_equal',
                    '<=': 'less_equal', '>=': 'greater_equal',
                    '&&': 'logical_and', '||': 'logical_or',
                    '++': 'increment', '--': 'decrement',
                    '+=': 'add_assign', '-=': 'minus_assign',
                    '*=': 'mult_assign', '/=': 'div_assign', '%=': 'modulo_assign',
                    '..': 'concat'  # String concatenation operator
                }
                if two_char in two_char_ops:
                    token_type = two_char_ops[two_char]
                    i += 2
                    col += 2
                    
                    # Validate delimiter for two-char operators
                    next_char = get_next_char()
                    if not check_delimiter(token_type, next_char):
                        add_error(f"Lexical Error: Operator '{two_char}' not properly delimited (expected valid delimiter, found '{next_char}')", start_i, i, start_line, start_col)
                        continue
                    
                    add_token(two_char, token_type, start_line, start_col)
                    continue
            
            # Single-character operators and delimiters
            single_char_tokens = {
                # Arithmetic operators
                '+': 'plus', '-': 'minus', '*': 'multiply', '/': 'divide', '%': 'modulo',
                # Assignment
                '=': 'assign',
                # Relational
                '<': 'less_than', '>': 'greater_than',
                # Logical
                '!': 'not',
                # Delimiters
                '(': 'open_paren', ')': 'close_paren',
                '[': 'open_bracket', ']': 'close_bracket',
                '{': 'open_curly', '}': 'close_curly',
                ';': 'semicolon', ',': 'comma', ':': 'colon', '.': 'dot'
            }
            
            if ch in single_char_tokens:
                token_type = single_char_tokens[ch]
                i += 1
                col += 1
                
                # Validate delimiter for single-char operators
                next_char = get_next_char()
                if not check_delimiter(token_type, next_char):
                    add_error(f"Lexical Error: Token '{ch}' not properly delimited (expected valid delimiter, found '{next_char}')", start_i, i, start_line, start_col)
                    continue
                
                add_token(ch, token_type, start_line, start_col)
                continue
            
            # ============ UNEXPECTED CHARACTER ============
            
            # Unexpected character - report error
            add_error(f"Lexical Error: Unexpected character '{ch}'", start_i, start_i + 1, start_line, start_col)
            i += 1
            col += 1
        
        return {
            'tokens': [t.to_dict() for t in tokens],
            'errors': errors
        }
