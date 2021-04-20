import numpy as np
import pandas as pd
import string
import sys

print("analyse syntaxique ... ")
# =====================================================

def get_reduction_rule(number):
    grammar = {
        #Le début du programme
        0:{"non_terminal" : "Prog", "production" : "begin VarDclr ; Code end"},

        #Le corps du programme
        1:{"non_terminal" : "Code", "production" : "Instruction Code"},
       # 2:{"non_terminal" : "Code", "production" : "Loop Code"},
        3:{"non_terminal" : "Code", "production" : ""},

        #Les instructions de déclaration
        4:{"non_terminal" : "VarDclr", "production" : "Dchar VarDclr"},
        5:{"non_terminal" : "VarDclr", "production" : "Dint VarDclr"},
        6:{"non_terminal" : "VarDclr", "production" : "Dfloat VarDclr"},
        7:{"non_terminal" : "VarDclr", "production" : "Dbool VarDclr"},

        #Les différentes méthodes de déclaration d'une variable de type char
        8:{"non_terminal" : "Dchar", "production" : "char Id"},
        9:{"non_terminal" : "Dchar", "production" : "char Id = \"Char\"" },

        # Les différentes méthodes de déclaration d'une variable de type int
        10: {"non_terminal": "Dint", "production": "int Id"},
        11: {"non_terminal": "Dint", "production": "int Id = Int"},

        # Les différentes méthodes de déclaration d'une variable de type float
        12: {"non_terminal": "Dfloat", "production": "float Id"},
        13: {"non_terminal": "Dfloat", "production": "float Id = Float"},

        # Les différentes méthodes de déclaration d'une variable de type bool
        14: {"non_terminal": "Dbool", "production": "bool Id"},
        15: {"non_terminal": "Dbool", "production": "bool Id = Cond"},

        # Les chiffres
        16: {"non_terminal": "Number", "production": "0"},
        17: {"non_terminal": "Number", "production": "1"},
        18: {"non_terminal": "Number", "production": "2"},
        19: {"non_terminal": "Number", "production": "3"},
        20: {"non_terminal": "Number", "production": "4"},
        21: {"non_terminal": "Number", "production": "5"},
        22: {"non_terminal": "Number", "production": "6"},
        23: {"non_terminal": "Number", "production": "7"},
        24: {"non_terminal": "Number", "production": "8"},
        25: {"non_terminal": "Number", "production": "9"},

        #Les nombres entiers
        26: {"non_terminal": "Int", "production": "Number Int"},
        27: {"non_terminal": "Int", "production": "Number"},
		
		#Les nombres réels
        28: {"non_terminal": "Float", "production": "Int.Int"},
		
		#Les chaines de caractères
        29: {"non_terminal": "Char", "production": "Alphabet Char"},
        30: {"non_terminal": "Char", "production": "Number Char"},
        31: {"non_terminal": "Char", "production": ""},
		
		#La structure d'un identifiant
        32: {"non_terminal": "Id", "production": "Alphabet BodyId"},
        33: {"non_terminal": "BodyId", "production": "Alphabet BodyId"},
        34: {"non_terminal": "BodyId", "production": "Number BodyId"},
		35: {"non_terminal": "BodyId", "production": "_ BodyId"},
        36: {"non_terminal": "BodyId", "production": "Alphabet"},
        37: {"non_terminal": "BodyId", "production": "Number"},
		
		#Les différentes instructions
        38: {"non_terminal": "Instruction", "production": "IfCond"},
        39: {"non_terminal": "Instruction", "production": "IfElseCond"},
        40: {"non_terminal": "Instruction", "production": "Aff ;"},
        41: {"non_terminal": "Instruction", "production": "Input"},
        42: {"non_terminal": "Instruction", "production": "Output"},
        43: {"non_terminal": "Instruction", "production": "WhileLoop"},
        44: {"non_terminal": "Instruction", "production": "ForLoop"},
		
		#La boucle while
        45: {"non_terminal": "WhileLoop", "production": "while ( Cond ) { Code }"},
		
		#La boucle for
        46: {"non_terminal": "ForLoop", "production": "for ( Id : Int ; Int) { Code }"},
        
		#La condition simple
		47: {"non_terminal": "IfCond", "production": "if ( Cond ) { Code }"},
        
		#La condition composée
		48: {"non_terminal": "IfElseCond", "production": "IfCond else { Code }"},
		
		#La définition des conditions
		49: {"non_terminal": "Cond", "production": "ExpArith OpArith ExpArith"},
		50: {"non_terminal": "Cond", "production": "ExpLog"},
		
		#L'ensemble des opérateurs de comparaison
		51: {"non_terminal": "OpArith", "production": "<"},
		52: {"non_terminal": "OpArith", "production": ">"},
		53: {"non_terminal": "OpArith", "production": "<="},
		54: {"non_terminal": "OpArith", "production": ">="},
		55: {"non_terminal": "OpArith", "production": "=="},
		56: {"non_terminal": "OpArith", "production": "!="},
		
		#L'ensemble des opérateurs logiques binaires
		57: {"non_terminal": "OpArith", "production": "&&"},
		58: {"non_terminal": "OpArith", "production": "||"},
		
		#La définition des expressions logiques
		59: {"non_terminal": "ExpLog", "production": "Cond OpLog Cond"},
		60: {"non_terminal": "ExpLog", "production": "! Cond"},
		61: {"non_terminal": "ExpLog", "production": "true"},
		62: {"non_terminal": "ExpLog", "production": "false"},
		
		#La définition des instruction d'affectation
		63: {"non_terminal": "Aff", "production": "Id = Int"},
		64: {"non_terminal": "Aff", "production": "Id = Float"},
		65: {"non_terminal": "Aff", "production": "Id = Char"},
		66: {"non_terminal": "Aff", "production": "Id = Bool"},
		67: {"non_terminal": "Aff", "production": "Id = ExpArith"},
		68: {"non_terminal": "Aff", "production": "Id =  ExpLog"},
	
		#L'instruction de lecture
		69: {"non_terminal": "Input", "production": "input : Id;"},
		
		#L'instruction d'affichage
		70: {"non_terminal": "Output", "production": "output : ( Message );"},
		
		#Les types de messages à afficher
		71: {"non_terminal": "Message", "production": "ExpArith"},
		72: {"non_terminal": "Message", "production": "ExpLog"},
		73: {"non_terminal": "Message", "production": "Id"},
	
		#La définition des expressions arithmétiques
    }
    
    return grammar.get(number,"Pas d'action")
	
# =====================================================

lr_table = pd.read_csv("helper/LR_table.csv")

# =====================================================

def get_action(action):
    if action == "acc"  :
        return {"action": "accept",
                "number":None}
    
    elif action[0] == "r" :
        return {"action": "Reduction",
                "number":action[1:]}
    
    elif action[0] == "s" :
        return {"action": "Shift",
                "number": action[1:]}
    
    elif action == '\xa0' :
        return {"action": None,
                "number":None}

# =====================================================

# test !:::::::




def syntaxique(chaine):

    chaine += "$"
    Stack = ['#',0]
    #init
    ptr = chaine[0]
    state = Stack[-1] # state = 0
    Do = get_action( lr_table[ptr][0] )

    # then do 
    while (Do["action"] != None and chaine != ['$']):
        haja = []
        if   Do["action"] == "Shift" : 
            # SHIFT ==============================::
            # D4 => S4 => shift_number = 4
            number = int(Do["number"])
            Stack.append( chaine.pop(0) )
            Stack.append(number)     

            # REDUCTION ==========================::
        elif Do["action"] == "Reduction":
            number = int( Do["number"] )        
            regle = get_reduction_rule(number)
            
            print(regle)
            
            
            right_part = regle["production"].split(sep=" ")

            right_part.reverse()
            left_part = regle["non_terminal"]
            
            #:faire la réduction:#
            while ( right_part != [] ):
                if right_part == [''] :
                    break
                if Stack[-1] != right_part[0] :
                    Stack.pop()
                elif Stack[-1] == right_part[0]: 
                    Stack.pop()
                    haja += right_part[0]
                    right_part.pop(0)
                else :
                    sys.exit(0)
            # get la relation entre Stack[-1] et le non-terminal 
            rel = lr_table[left_part][Stack[-1]]
            # empiler la partie gauche :
            Stack.append(left_part)
            # empiler la relation
            Stack.append(int(rel)) 
        print(Stack)
        #print("-------")
        #print(chaine)
            # NEXT ===============================::
        Do = get_action(lr_table[chaine[0]][int(Stack[-1])])

    if(Do["action"] == "accept" and chaine == ['$']) : 
        print("========================")
        print("  el syntaxe raho b1")
        print("========================")
    else :
        print("I will handle errors soon ! ")











