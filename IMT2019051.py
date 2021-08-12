class stored():
    def __init__(self):
        self.PC=0
        self.MAR=0
        self.M=[""]*1000
        self.MBR=""
        self.MQ="0"
        self.AC="0"
        self.IR=""
        self.IBR=""

class opcode():
    def __init__(self):
        self.code={
            '00001010': self.LOADMQ,
            '00001001': self.LOADMQMX,
            '00000001': self.LOADMX,
            '00000101':self.ADDMX,
            '00100001':self.STORMX,
            '00000111': self.ADDABMX,
            '00000110': self.SUBMX,
            '00001000': self.SUBABMX,
            '00000010': self.LOAD_NMX,
            '00000011': self.LOAD_ABMX,
            '00000100': self.LOAD_NABMX,  
            '00001101': self.JUMP_MX019,
            '00010100': self.LSH,
            '00010101': self.RSH,
            '00001111': self.CONLEFTJUMP,
        }
    def LOADMQ(self,IAS):   #load MQ
        IAS.storage.AC=IAS.storage.MQ
    
    def LOADMQMX(self,IAS): #load MQ MX
        IAS.storage.MQ=IAS.storage.IAS[IAS.storage.MAR]

    def LOADMX(self,IAS):   #Load M(x)
        IAS.storage.AC=IAS.storage.M[IAS.storage.MAR]

    def LOAD_NMX(self,IAS): #Load -M(x)
        IAS.storage.AC=bin(-int(IAS.storage.M[IAS.storage.MAR],2))

    def LOAD_ABMX(self,IAS):    #Load |M(x)|
        IAS.storage.AC=bin(abs(int(IAS.storage.M[IAS.storage.MAR],2)))
    
    def LOAD_NABMX(self,IAS):   #Load -|M(x)|
        IAS.storage.AC=bin(-abs(int(IAS.storage.M[IAS.storage.MAR],2)))

    def ADDMX(self,IAS):   #add M(x)
        print int(IAS.storage.AC,2)
        ac=int(IAS.storage.AC,2)
        ac+=int(IAS.storage.M[IAS.storage.MAR],2)
        print ac
        IAS.storage.AC=bin(ac)

    def STORMX(self,IAS):   #store M(x)
        IAS.storage.M[IAS.storage.MAR]=IAS.storage.AC

    def ADDABMX(self,IAS):  #add |M(x)|
        print int(IAS.storage.AC,2)
        ac=int(IAS.storage.AC,2)
        ac+=abs(int(IAS.storage.M[IAS.storage.MAR],2))
        print ac
        IAS.storage.AC=bin(ac)
    
    def SUBMX(self,IAS):    #sub M(x)
        print int(IAS.storage.AC,2)
        ac=int(IAS.storage.AC,2)
        ac-=int(IAS.storage.M[IAS.storage.MAR],2)
        print ac
        IAS.storage.AC=bin(ac)

    def SUBABMX(self,IAS):  #sub |M(x)|
        print int(IAS.storage.AC,2)
        ac=int(IAS.storage.AC,2)
        ac-=abs(int(IAS.storage.M[IAS.storage.MAR],2))
        print ac
        IAS.storage.AC=bin(ac)
    
    def JUMP_MX019(self,IAS):   #unconditional left jump
        if(IAS.storage.IBR!=""):
            IAS.storage.IBR=""
            IAS.storage.PC=IAS.storage.MAR
        else:
            IAS.storage.PC=IAS.storage.MAR

    def CONLEFTJUMP(self,IAS):  #conditional left jump
        ac=int(IAS.storage.AC,2)
        if(ac>=0):
            if(IAS.storage.IBR!=""):
                IAS.storage.IBR=""
                IAS.storage.PC=IAS.storage.MAR
            else:
                IAS.storage.PC=IAS.storage.MAR



    def LSH(self,IAS):          #left shift
        ac=int(IAS.storage.AC,2)
        ac=ac<<1
        IAS.storage.AC=bin(ac)

    def RSH(self,IAS):          #right shift
        ac=int(IAS.storage.AC,2)
        ac=ac>>1
        IAS.storage.AC=bin(ac)

    def check(self,IAS):
        if IAS.storage.IR in self.code:
            return self.code[IAS.storage.IR]
        return False
    
class comp():
    def __init__(self):
        self.storage=stored()
        self.opcodes=opcode()

def fetch(IAS):
    if(IAS.storage.IBR==""):     #no next instruction in ibr
        print "NO IBR"
        IAS.storage.MAR=IAS.storage.PC
        IAS.storage.MBR=IAS.storage.M[IAS.storage.MAR]
        if(IAS.storage.MBR[0:20]=="00000000000000000000"): #no left instruction
            print "NO LEFT INST"
            IAS.storage.IR=IAS.storage.MBR[20:28]
            IAS.storage.MAR=int(IAS.storage.MBR[28:],2)
            IAS.storage.PC+=1

        elif(IAS.storage.MBR[0:20]!="00000000000000000000"):
            print "BOTH INSTR"
            IAS.storage.IBR=IAS.storage.MBR[20:]
            IAS.storage.IR=IAS.storage.MBR[0:8]
            IAS.storage.MAR=int(IAS.storage.MBR[8:20],2)
    else:                       #ibr present
        print "IBR present"
        IAS.storage.IR=IAS.storage.IBR[0:8]
        IAS.storage.MAR=int(IAS.storage.IBR[8:],2)
        IAS.storage.PC+=1
        IAS.storage.IBR=""

def execute(IAS):
    operation=IAS.opcodes.check(IAS)
    if(operation!=False):
        operation(IAS)
    else:
        print "wrong opcode given"

def cycle(IAS):
    fetch(IAS)
    execute(IAS)

if __name__=="__main__":
    IAS=comp()
    
    #sample1 hard coded program begin-------

    # IAS.storage.M[0]="0000001000000110010000000110000001100101"   #LOAD_NMX 100 SUBMX 101
    # # IAS.storage.M[1]="0000110100000000001000100001000001100100"   #JUMP_MX019 2 STORMX 100
    # IAS.storage.M[1]="0000111100000000001000100001000001100100"     #CONLEFTJUMP 2 STORMX 100
    # IAS.storage.M[2]="0000000000000000000000100001000011001000"   #NO LEFT INSTRUCTION STORMX 200
    # IAS.storage.M[3]="0000000000000000000000000000000000000000"   # HALT OR ENDOF INSTRUCTIONS

    # IAS.storage.M[100]="0000000000000000000000000000000000000011"
    # IAS.storage.M[101]="0000000000000000000000000000000000000010"
    # while(IAS.storage.M[IAS.storage.PC]!="0000000000000000000000000000000000000000"):
    #     cycle(IAS)
    #     # print IAS.storage.PC
    # print int(IAS.storage.AC,2)
    # print int(IAS.storage.M[200],2)
    # print int(IAS.storage.M[100],2)

    #sample1 hard coded program ends-------

    #sample2 hard coded program starts------
    # IAS.storage.M[0]="0000000100000110010000010101000000000000" #LOADMX 100 RSH 
    # # IAS.storage.M[0]="0000000100000110010000010100000000000000" #LOADMX 100 LSH
    # IAS.storage.M[1]="0000000000000000000000000000000000000000"
    # IAS.storage.M[100]="0000000000000000000000000000000000000011"
    # while(IAS.storage.M[IAS.storage.PC]!="0000000000000000000000000000000000000000"):
    #     cycle(IAS)
    # print int(IAS.storage.AC,2)
    #sample2 hard coded program ends-----

    #sample3 hard coded program starts-----
    # IAS.storage.M[0]="0000000100000110010000000101000001100101"
    # IAS.storage.M[1]="0000000000000000000000100001000011001000"
    # IAS.storage.M[2]="0000000000000000000000000000000000000000"
    # IAS.storage.M[100]=bin(3)
    # IAS.storage.M[101]=bin(2)
    # while(IAS.storage.M[IAS.storage.PC]!="0000000000000000000000000000000000000000"):
    #     cycle(IAS)
    # print int(IAS.storage.AC,2)
    #sample3 hard coded program ends----

    print "Assumptions:"
    print "1. The storage should contain all the instructions sequentially first and the data next"
    print '2. 40 bit string(Lets call it halt string) "0000000000000000000000000000000000000000" is the halt condition.'
    print "3. Consider the halt string too in the number of locations to be allocated for instructions."
    print "4. Follow zero based indexing for storage i.e form 0 to 999."
    print "Give the instructions in the 40 bit format.\nIf the left instruction is not present give '00000000000000000000' as left instruction."
    no1=int(input("Number of locations to be allocated for instructions:"))
    for i in range (no1):
        IAS.storage.M[i]=raw_input("storage Location "+str(i)+":")

    no2=int(input("number of data locations to be allocated:"))
    for i in range(no2):
        adr=int(input("Address(in decimal):"))
        data=int(input("Data need to be stored (in decimal):"))
        IAS.storage.M[adr]=bin(data)
 
    while(IAS.storage.M[IAS.storage.PC]!="0000000000000000000000000000000000000000"):
        cycle(IAS)
 
    print "Accumulator contains "+str(int(IAS.storage.AC,2))

 
 