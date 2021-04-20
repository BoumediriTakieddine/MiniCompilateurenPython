import numpy as np
import pandas as pd
import string
import sys

oprtArith = ['+','-','*','/','%','=']
opCmp = ['==','!=','<','<=','>','>=']
sep = ['(',')',';',':','{','}']

#Opérateurs Arithmétiques
ADD   = 0    # +
SUB   = 1    # -
MUL   = 2    # *
DIV   = 3    # /
MOD   = 4    # %
AFF   = 5    # =

#Opérateurs de comapraison
EQ    = 6    # ==
NEQ   = 7    # !=
LE    = 8    # <
LEQ   = 8    # <=
GT    = 9    # >
GTQ   = 10   # >=

#Séparateurs
PAR_OUV  = 11   # (
PAR_FERM = 12   # )
SEMI     = 13   # ;
DPNT     = 14   # :
ACC_OUV  = 15   # {
ACC_FERM = 16   # }

ID      = 17 # idf
CONST   = 18

#Mots-clé
KEY_BEG   = 19 # begin
KEY_END   = 20 # end

KEY_IF    = 21 # if
KEY_ELSE  = 22 # else
KEY_WHILE = 24

KEY_WH    =25 # while
KEY_EWH =26 # ewhile

KEY_LET   =27  # let


keywords_finit_stats = [5]
keywords_automata = pd.read_csv('helper/keywords.csv')


# ========================================================

def is_keyword(string):
    string += '#'
    i = 0
    current_state = 0
    current_term = string[0]
    
    while current_term != '#' and current_state != -1 :
        current_state = keywords_automata[string[i]][current_state]
        i+=1
        current_term = string[i]        
        
    if current_term == "#" and current_state in keywords_finit_stats:
        return True   # accepted
    else :
        return False  # not accepted

# ========================================================

def is_idf(string):
    i=0
    if(string[i] == '_'):
        return string[1:].isalnum()
    else:
        return False

# ========================================================

def is_const(string):
    i=0
    if(string[i] == '.' or string[len(string) - 1] == '.'):
        return False
    else:
        num = string.replace('.', '')
        return num.isdigit() and ( string.count('.') == 1 or string.count('.') == 0 )

# ========================================================

def error(msg='',sym=' ',ligne=0):
    print("Error :" + msg +" "+ sym + " at ligne " + str(ligne))
    sys.exit(1)

# ========================================================

def tok(token_type,token):
    """
    input : tocken_type , token
    output : dict of token
    """
    return {"token_type" : token_type , "value" : token}

# ========================================================

def lexical(code):
    i = 0
    num_ligne = 1
    tokens_table = []
    used_table = [] 
    while i < len(code):
        # calcule de lign ::::::::::::::::::::::::::::::::
        if(code[i] == '\n') : num_ligne += 1
        # print(num_ligne)

        # comments  ::::::::::::::::::::::::::::::::::::::
        if code[i]=='&':
            while code[i] != '\n':
                i+=1


        # skip spaces  :::::::::::::::::::::::::::::::::::
        elif code[i].isspace():
            pass


        # operateur  :::::::::::::::::::::::::::::::::::::
        elif code[i] in oprtArith:
            if  code[i] == '+' : 
                tokens_table.append(tok(ADD,None))
                used_table.append(code[i])
                #print(code[i])
            elif code[i]== '-' : 
                tokens_table.append(tok(SUB,None))
                used_table.append(code[i])
                #print(code[i])
            elif code[i]== '*' : 
                tokens_table.append(tok(MUL,None))
                used_table.append(code[i])
                #print(code[i])
            elif code[i]== '/' : 
                tokens_table.append(tok(DIV,None))
                used_table.append(code[i])
                #print(code[i])
            elif code[i]== '%' : 
                tokens_table.append(tok(MOD,None))
                used_table.append(code[i])
                #print(code[i])
            elif code[i]== '=' : 
                tokens_table.append(tok(AFF,None))
                used_table.append(code[i])
                #print(code[i])
            elif code[i]== '~' : 
                tokens_table.append(tok(EQ,None))
                used_table.append(code[i])
                #print(code[i])

            elif code[i]== '<' :
                if code[i+1] == '<':
                    tokens_table.append(tok(PRINT,None))
                    #print(code[i]+code[i+1])
                    used_table.append(code[i]+code[i+1])
                    i+=1
                elif code[i+1] == '=':
                    tokens_table.append(tok(LEQ,None)) # <=
                    used_table.append(code[i]+code[i+1])
                    #print(code[i]+code[i+1])
                    i+=1
                else :
                    tokens_table.append(tok(LE,None))  # <
                    used_table.append(code[i])
                    #print(code[i])


            elif code[i]== '>' :
                if code[i+1] == '>':
                    tokens_table.append(tok(READ,None))
                    used_table.append(code[i]+code[i+1])
                    #print(code[i]+code[i+1])
                    i+=1

                elif code[i+1] == '=':
                    tokens_table.append(tok(GTQ,None)) # <=
                    used_table.append(code[i]+code[i+1])
                    #print(code[i]+code[i+1])
                    i+=1

                else :
                    tokens_table.append(tok(GT,None)) # <
                    used_table.append(code[i])
                    #print(code[i])


        # separateur :::::::::::::::::::::::::::::::::::::       
        elif code[i] in sep :
            if code[i] == '(': 
                tokens_table.append(tok(SEP_OUV,None))
                used_table.append(code[i])
            elif code[i] == ')':
                tokens_table.append(tok(SEP_OUV,None))
                used_table.append(code[i])
            elif code[i] == ';':
                tokens_table.append(tok(SEMI,None))
                used_table.append(code[i])
            elif code[i] == ':':
                tokens_table.append(tok(DPNT,None))
                used_table.append(code[i])
            #print(code[i]) # afficher supp      


        # idf ::::::::::::::::::::::::::::::::::::::::::::
        elif code[i] == '_':
            idf=''
            while (not code[i].isspace())and(code[i] not in oprtArith)and(code[i] not in sep):
                idf += code[i]
                i+=1
            if is_idf(idf):
                tokens_table.append(tok(ID,idf))
                used_table.append(idf)
                # print(idf)
            else :
                error("INVALIDE IDF",idf,num_ligne) # : error ligne number !
            i-=1   


        # keywords :::::::::::::::::::::::::::::::::::::::
        elif code[i].isalpha():
            word = ''
            while not code[i].isspace() and  code[i] not in sep:
                word += code[i]
                i+=1
            #print(word)
            if is_keyword(word):
                if   word == "begin" :
                    tokens_table.append(tok(KEY_BEG,word))
                    used_table.append(word)
                elif word == "end" :
                    tokens_table.append(tok(KEY_END,word))
                    used_table.append(word)
                elif word == "if" :
                    tokens_table.append(tok(KEY_IF,word))
                    used_table.append(word)
                elif word == "eif" :
                    tokens_table.append(tok(KEY_EIF,word))
                    used_table.append(word)
                elif word == "else" :
                    tokens_table.append(tok(KEY_ELSE,word))
                    used_table.append(word)
                elif word == "eelse" :
                    tokens_table.append(tok(KEY_EELSE,word))
                    used_table.append(word)
                elif word == "while" :
                    tokens_table.append(tok(KEY_WH,word))
                    used_table.append(word)
                elif word == "ewhile" :
                    tokens_table.append(tok(KEY_EWH,word))
                    used_table.append(word)
                elif word == "let" :
                    tokens_table.append(tok(KEY_LET,word))
                    used_table.append(word)
            else :
                error("INVALIDE KEYWORD",word,num_ligne) # : error ligne number !

            # const (numero) :::::::::::::::::::::::::::::
        elif code[i].isnumeric():
            num = ''
            while not code[i].isspace() and code[i] not in sep: # add not in oprtArith
                num += code[i]
                i+=1
            #print(num)
            i-=1 # <----
            if is_const(num):
                tokens_table.append(tok(CONST,num))
                used_table.append(num)
            else :
                error("INVALIDE CONST",num,num_ligne)

        else:
            # num_ligne = 120
            error("INVALIDE SYMBOLE",code[i],num_ligne) 
        i+=1
    return tokens_table , used_table











































