from ..objects.QrInstruction import QrInstruction
from ..objects.QrGates import *
# AWS imports: Import Braket SDK modules
from braket.circuits import Circuit

class QrAmazonBraketManager:
    
    """
    Class that allows to transpile gates circuits developed with the Amazon Braket SDK.
    """

    def getCircuitInstructions(self, circuit):
        """
        Decompose a Amazon Braket gates circuit and returns the list of gates, its parameters and qubits affected.

        Prerequisites
        ----------
        None.

        Parameters
        ----------
        circuit : braket.circuits.Circuit
            Circuit object created with the Amazon Braket SDK

        Output
        ----------
        Array of QrInstruction objects. 
        Each Qrinstruction objetc contains a gate with its parameters and qubits where applied.
        """       
        instructions = []
        for instr in circuit.instructions:
            posSeparatorGate = str(instr.operator).find('(')
            posSeparatorAngle= str(instr.operator).find('\'angle\': ')+9
            posSeparatorAngleValue = str(instr.operator).find(',')
            gateVar = self.__getGateOperation(instr,posSeparatorGate)
            paramVar = self.__getParamOperation(instr,posSeparatorGate,posSeparatorAngle,posSeparatorAngleValue)
            qbitVar = self.__getNQubitsOperation(instr)
            if((gateVar is not None) and (paramVar is not None) and (qbitVar is not None)):
                instructions.append(QrInstruction(gateVar, paramVar, qbitVar))
        return instructions
    
    # We get the gate of the operation
    def __getGateOperation(self,instr,posSeparatorGate):
        gateTmp = str(instr.operator)[0:posSeparatorGate]
        if (gateTmp=="X"):
            return GATE_X
        elif (gateTmp=="Y"):
            return GATE_Y
        elif (gateTmp=="Z"):
            return GATE_Z
        elif (gateTmp=="H"):
            return GATE_H
        elif (gateTmp=="S"):
            return GATE_S
        elif (gateTmp=="T"):
            return GATE_T
        elif (gateTmp=="Swap"):
            return GATE_Swap
        elif (gateTmp=="Rx"):
            return GATE_Rx
        elif (gateTmp=="Ry"):
            return GATE_Ry
        elif (gateTmp=="Rz"):
            return GATE_Rz
        elif (gateTmp=="CCNot"):
            return GATE_Ccx
        elif (gateTmp=="CNot"):
            return GATE_Cx
        

    # We get the params of the operation
    def __getParamOperation(self,instr,posSeparatorGate,posSeparatorAngle,posSeparatorAngleValue):
        listGatesWithParams = ['Rx','Ry','Rz']
        if (str(instr.operator)[0:posSeparatorGate]) in listGatesWithParams:
            return str(instr.operator)[posSeparatorAngle:posSeparatorAngleValue]
        else:
            return 0

    # We obtain the qubit/s of the operation
    def __getNQubitsOperation(self,instr):
        # Return number of qubits of Instructions len(instr.target)
        if (len(instr.target)==1):
            return int(str(instr.target[0])[str(instr.target[0]).find('(')+1:str(instr.target[0]).find(')')])
        elif (len(instr.target)==2):
            return int(str(instr.target[0])[str(instr.target[0]).find('(')+1:str(instr.target[0]).find(')')]),int(str(instr.target[1])[str(instr.target[1]).find('(')+1:str(instr.target[1]).find(')')])
        elif (len(instr.target)==3):
            return int(str(instr.target[0])[str(instr.target[0]).find('(')+1:str(instr.target[0]).find(')')]),int(str(instr.target[1])[str(instr.target[1]).find('(')+1:str(instr.target[1]).find(')')]),int(str(instr.target[2])[str(instr.target[2]).find('(')+1:str(instr.target[2]).find(')')])    