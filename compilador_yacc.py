#
# T = {
#     'START', 'END',
#     'INT', 'NUM','ID','ATRIB',
#     'ADD','SUB','MUL','DIV','MOD','EQ','DIFF','GRT','GEQ','LWR','LEQ',
#     'AND','OR','NOT','READ','WRITE','IF','THEN','ELSE','FOR','DO','(',')','{','}',';','-'
# }
#
#  Linguagem --> Decls START Instrs END
#
#  Decls --> Decl Decls
#          |
#
#  Decl --> INT ID DeclAtrib
#
#
#  DeclAtrib --> '=' Relac
#              | 
#
#  Instrs --> CabecaInstrs CaudaInstrs
#
#  CabecaInstrs --> Relac
#                 | WRITE '(' Relac ')'
#
#  CaudaInstrs --> CabecaInstrs CaudaInstrs
#                | 
#
#
#  Relac -->  EQ '(' Relac Exp ')'
#          |  DIFF '(' Relac Exp ')'
#          |  GRT '(' Relac Exp ')'
#          |  GEQ '(' Relac Exp ')'
#          |  LWR '(' Relac Exp ')'
#          |  LEQ '(' Relac Exp ')'
#          |  Exp
#
#
#  Exp --> ADD '(' Exp Termo ')'
#       |  SUB '(' Exp Termo ')'
#       |  Termo
#
#
#  Termo --> MUL '(' Termo Factor ')'
#         |  DIV '(' Termo Factor ')'
#         |  MOD '(' Termo Factor ')'
#         |  Factor
#
#  Factor --> '(' Relac ')'
#           |  NUM
#           |  ID
#
#
#
#
import ply.yacc as yacc
import sys

from compilador_lex import tokens

#Produção da linguagem
def p_Linguagem(p):
    "Linguagem : Decls START Instrs END"
    p[0] = p[1] + '\n\nSTART\n' + p[3] + '\n\nSTOP\n'

#Produções Decls
def p_Decls(p):
    "Decls : Decl Decls"
    p[0] = p[1] + p[2]

def p_Decls_empty(p):
    "Decls : "
    p[0] = ''

#Produções Decl
def p_Decl(p):
    "Decl : INT ID DeclAtrib"
    if(p[3] == ""):
        p[0] = '\nPUSHI 0'
    else:
        p[0] = p[3]
    p.parser.registers.update({p[2]: (p[1],p.parser.gp)})
    p.parser.gp += 1


#Produções DeclAtrib
def p_DeclAtrib(p):
    "DeclAtrib : '=' Relac"
    p[0] = p[2]

def p_DeclAtrib_empty(p):
    "DeclAtrib : "
    p[0] = ''


#Produções das instruções
def p_Instrs(p):
    "Instrs : CabecaInstrs CaudaInstrs"
    p[0] = p[1] + p[2]

#Produções de uma instrução
def p_CabecInstrs_Exp(p):
    "CabecaInstrs : Relac"
    p[0] = p[1]

def p_CabecInstrs_Write(p):
    "CabecaInstrs : WRITE '(' Relac ')'"
    p[0] = p[3] + '\nWRITEI'



#Produções cauda de instruções
def p_CaudaInstrs_Instrs(p):
    "CaudaInstrs : CabecaInstrs CaudaInstrs"
    p[0] = p[1] + p[2]

def p_CaudaInstrs_empty(p):
    "CaudaInstrs : "
    p[0] = ''

#Produções das operações relacionais
def p_Relac_EQ(p):
    "Relac : EQ '(' Relac Exp ')'"
    p[0] = p[3] + p[4] + '\nEQUAL'

def p_Relac_DIFF(p):
    "Relac : DIFF '(' Relac Exp ')'"
    p[0] = p[3] + p[4] + '\nEQUAL\nNOT'
    
def p_Relac_GRT(p):
    "Relac : GRT '(' Relac Exp ')'"
    p[0] = p[3] + p[4] + '\nSUP'
    
def p_Relac_GEQ(p):
    "Relac : GEQ '(' Relac Exp ')'"
    p[0] = p[3] + p[4] + '\nSUPEQ'

def p_Relac_LWR(p):
    "Relac : LWR '(' Relac Exp ')'"
    p[0] = p[3] + p[4] + '\nINF'

def p_Relac_LEQ(p):
    "Relac : LEQ '(' Relac Exp ')'"
    p[0] = p[3] + p[4] + '\nINFEQ'

def p_Relac_Exp(p):
    "Relac : Exp"
    p[0] = p[1]



#Produções Exp
def p_Exp_add(p):
    "Exp : ADD '(' Exp Termo ')'"
    p[0] = p[3] + p[4] + '\nADD'

def p_Exp_sub(p):
    "Exp : SUB '(' Exp Termo ')'"
    p[0] = p[3] + p[4] + '\nSUB'

def p_Exp_Termo(p):
    "Exp : Termo"
    p[0] = p[1]

#Produções Termo
def p_Termo_mul(p):
    "Termo : MUL '(' Termo Factor ')'"
    p[0] = p[3] + p[4] + '\nMUL'

def p_Termo_div(p):
    "Termo : DIV '(' Termo Factor ')'"
    p[0] = p[3] + p[4] + '\nDIV'

def p_Termo_mod(p):
    "Termo : MOD '(' Termo Factor ')'"
    p[0] = p[3] + p[4] + '\nMOD'

def p_Termo_factor(p):
    "Termo : Factor"
    p[0] = p[1]

#Produções Factor
def p_Factor_group(p):
    "Factor : '(' Relac ')'"
    p[0] = p[2]

def p_Factor_num(p):
    "Factor : NUM"
    p[0] = '\nPUSHI ' + p[1]

def p_Factor_ID(p):
    "Factor : ID"
    (_, offset) = p.parser.registers.get(p[1])
    p[0] = '\nPUSHG ' + str(offset)


# Error rule for syntax errors
def p_error(p):
    print('Syntax error in input: ', p)

# Build the parser
parser = yacc.yacc()

# Creating the model
parser.registers = {}
parser.gp = 0


path = 'testesLinguagem/Relacionais/'
print("Ficheiro para ler: ")
i = input()
pathI = path + i
file = open(pathI,"r")

cont = ''
for linha in file:
    cont += linha

print("Output: ")
o = input()
pathO = path + o

f = open(pathO,"w")
result = parser.parse(cont)

f.write(result)
