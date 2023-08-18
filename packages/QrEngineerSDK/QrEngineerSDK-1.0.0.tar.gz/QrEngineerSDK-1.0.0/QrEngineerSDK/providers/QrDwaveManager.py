import sys
import os
import ntpath
import pathlib
from dimod import utilities
from itertools import chain

class QrDwaveManager:

    """
    Class that allows to transpile the Binary Quadratic Model of an optimization problem, generated with the Dwave Ocean SDK.
    """
    
    def generateQPathCircuit(self, bqm):
        
        quboArray = [[0 for i in range(bqm.num_variables)] for j in range(bqm.num_variables)] 

        for i in range(bqm.num_variables):
            for j in range (i, bqm.num_variables):
                if i==j:
                    quboArray[i][j] = bqm.linear[i]
                else:
                    if (j, i) in bqm.quadratic:                        
                        quboArray[i][j] = bqm.quadratic[(j, i)]
                
        circuitIL = "PARAM(NVars|@NVars@);PARAM(Offset|@Offset@);AUXDATA(C|\"@C@\");CLASS(ClassX|NVars|\"\");VARIABLE(X|{ClassX}|\"\");RULE(Rule1|\"\"|\"1\"|	{ SUMMATORY(from 1 to NVars iterate i| { SUMMATORY(from i+1 to NVars iterate j|	{ QUADRATIC(X[i]|X[j]|\"C[i,j]\")	})}),SUMMATORY(from 1 to NVars iterate i|{ LINEAR(X[i]| \"C[i,i]\")}),OFFSET(\"Offset\")});"        
        circuitIL = circuitIL.replace("@NVars@",str(bqm.num_variables))
        circuitIL = circuitIL.replace("@Offset@",str(bqm.offset))
        circuitIL = circuitIL.replace("@C@",str(quboArray))        
        return circuitIL    

    
    def __getQUBOfromBQM (vars):
        bqm = vars['bqm']
        QUBO = bqm.to_qubo()
        return QUBO
    
    def __getQUBOfromTupleWithoutOffset(vars):  
        QUBO = (vars['Q'], 0)
        return QUBO
    
    def __getQUBOfromIsing (vars):
        h = vars['h']
        J = vars['J']
        print(h)
        print(J)        
        QUBO = utilities.ising_to_qubo(h, J, 0);
        print(QUBO)
        # Q = bqm.to_qubo()
        return QUBO
    
            
    