import math
import sympy as sp
def main_func(tw,cl,turn,shape):
    center=[float(input("Enter the x coordinate:")),float(input("Enter the y coordinate:"))]    
    x=center[0]
    y=center[1]    
    ly=input("Type F.Cu for top layer B.Cu for bottom layer: ")
    net=input("Type the net port:")
    c=0  
    the=float(input("Enter the starting angle in degree :"))
    rot=int(input("Enter +1 for anti clockwise, Enter -1 for clockwise: "))   
    input("Press Enter to get the coordinates........ ") 
    if(shape==1):
        x, y, c = square_plot(tw, cl, turn, x, y, ly, net, c, the, rot)
    elif(shape==2):
        x, y, c = hex_plot(tw, cl, turn, x, y, ly, net, c, the, rot)
    elif(shape==3):
        oct_plot(tw, cl, turn, x, y, ly, net, c, the, rot) 
def oct_plot(tw, cl, turn, x, y, ly, net, c, the, rot):
    for i in range (8*turn):
        travel=abs((tw+cl)/(2*math.sin(math.radians(315))-1))
        u=x
        v=y
        if(i%4==0):
            c=c+1
        if(rot==1):
            x=x + travel*c*math.cos(math.radians(the)+i*math.radians(315))
        else:
            x=x - travel*c*math.cos(math.radians(the)+i*math.radians(315))
        y=y + travel*c*math.sin(math.radians(the)+i*math.radians(315))        
        coordinates(u,v,x,y,tw,ly,net)
def hex_plot(tw, cl, turn, x, y, ly, net, c, the, rot):
    for i in range (6*turn):
        travel=abs(((tw+cl)/2)/math.sin(math.radians(300)))
        u=x
        v=y
        if(i%3==0):
            c=c+1
        if(rot==1):
            x=x + travel*c*math.cos(math.radians(the)+i*math.radians(300))
        else:
            x=x - travel*c*math.cos(math.radians(the)+i*math.radians(300))
        y=y + travel*c*math.sin(math.radians(the)+i*math.radians(300))        
        coordinates(u,v,x,y,tw,ly,net)
    return x,y,c
def square_plot(tw, cl, turn, x, y, ly, net, c, the, rot):
    for i in range (4*turn):
        travel=abs((tw+cl)/math.sin(math.radians(270)))
        u=x
        v=y
        if(i%2==0):
            c=c+1
        if(rot==1):
            x=x + travel*c*math.cos(math.radians(the)+i*math.radians(270))
        else:
            x=x - travel*c*math.cos(math.radians(the)+i*math.radians(270))
        y=y + travel*c*math.sin(math.radians(the)+i*math.radians(270))        
        coordinates(u,v,x,y,tw,ly,net)
    return x,y,c    
def coordinates(u,v,x,y,tw,ly,net):
    print("(segment(start",u,v,")(end",x,y,")(width",tw,")(layer",ly,")(net",net,"))") 
def calc_inductance(B, a1, a2, a3, a4, a5,shape):
    tw=float(input("Enter the track width in mm :"))*1000
    cl=float(input("Enter the clearance in mm :"))*1000
    turn=int(input("Enter the number of turns :"))
    id=2*(tw+cl)
    od=turn*id
    Davg=(od+id)/2
    print("the avg diameter of the coil is ",Davg,"micro meter")
    l=B*pow(od,a1)*pow(tw,a2)*pow(Davg,a3)*pow(turn,a4)*pow(cl,a5)
    print("The inductance of the coil is ",l," nano henry")
    input("Press enter to continue.......")
    main_func(tw/1000,cl/1000,turn,shape)


def first_derivative_test(tw,cl,ind,B,a1,a2,a3,a4,a5,shape):
    turn = sp.Symbol('turn')
    # Calculate the first derivative
    k=B*pow(cl,a5)*pow(tw,a2)*pow((tw+cl),a3)
    od=pow(ind/k*(pow((turn+1),a3)*pow(turn,a4)),1/a1)
    od_prime = sp.diff(od, turn)
    # Find critical points by solving f'(x) = 0
    critical_points = sp.solve(od_prime, turn)
    critical_points = sorted(critical_points)
    tn=[]      
    odn=[]
    # Perform the first derivative test
    for point in critical_points:
        odn.append(od.subs(turn,point))
        tn.append(point)     
    # Calculate the minimum value
    minimum_value = od.subs(turn, tn[0])
    od=pow(ind/(B*pow(cl,a5)*pow(tw,a2)*pow((tw+cl)*(minimum_value+1),a3)*  (minimum_value,a4)),1/a1)
    odf=od
    #print("The outer Diameter of the pcb coil is",odf/1000,"mm")
    input("Press enter to continue.......")
    main_func(tw/1000,cl/1000,turn,shape)


def calc_OD(B, a1, a2, a3, a4, a5,shape):
    tw=float(input("Enter the track width in mm :"))*1000
    cl=0.254*1000 #change the clearance according to the application to be used
    ind=float(input("Enter the Inductance value in Nano henry : "))
    
    first_derivative_test(tw,cl,ind,B,a1,a2,a3,a4,a5,shape) 
    od=pow(ind/(B*pow(cl,a5)*pow(tw,a2)*pow((tw+cl)*(turn+1),a3)*pow(turn,a4)),1/a1)
    print("The outer Diameter of the pcb coil is",od/1000,"mm")
    input("Press enter to continue.......")
    main_func(tw/1000,cl/1000,turn,shape)



def get_parameter(B, a1, a2, a3, a4, a5,x):    
    y=int(input("Enter 1 to find the inductance \nEnter 2 to find outer diameter\nSelect the number:"))
    if (y==1):
        calc_inductance(B, a1, a2, a3, a4, a5,x)
    if (y==2):
        calc_OD(B, a1, a2, a3, a4, a5,x)
def get_shape():    
    x=int(input("Select shape using the number \n 1.Square\n 2.Octagon\n 3.Hexagon\n Seclect shape:"))
    if x==1:
        B,a1,a2,a3,a4,a5=1.62*pow(10,-3),-1.21,-0.147,2.4,1.78,-0.03
        get_parameter(B,a1,a2,a3,a4,a5,x)       
    elif x==2:
        B,a1,a2,a3,a4,a5 = 1.28*pow(10,-3),-1.24,-0.174,2.47,1.77,-0.049
        get_parameter(B,a1,a2,a3,a4,a5,x)
    elif x==3:
        B,a1,a2,a3,a4,a5 = 1.33*pow(10,-3),-1.21,-0.163,2.43,1.75,-0.049
        get_parameter(B,a1,a2,a3,a4,a5,x)
get_shape()
