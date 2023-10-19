from unittest import skip
from z3 import *
import sys

i_j_of_vertical_cars = []
j_of_vertical_cars = []

i_j_of_horizontal_cars = []
i_of_horizontal_cars = []

i_j_of_mines = []

no_of_vertical_cars_in_j =[]
no_of_horizontal_cars_in_i =[]

file = open(sys.argv[1], 'r')
lines = file.read().split('\n')

m = int(lines[0].split(',')[0])
n = m-1
k = int(lines[0].split(',')[1])

red_car_i = int(lines[1].split(',')[0])
red_car_j = int(lines[1].split(',')[1])

for i in range(len(lines)-3):
    line = lines[i+2].split(',')
    
    if int(line[0]) == 0:
        i_j_of_vertical_cars.append([int(line[1]),int(line[2])])
        j_of_vertical_cars.append(int(line[2]))
    elif int(line[0]) == 1:
        i_j_of_horizontal_cars.append([int(line[1]),int(line[2])])
        i_of_horizontal_cars.append(int(line[1]))
    elif int(line[0]) == 2:
        i_j_of_mines.append([int(line[1]),int(line[2])])

for j in j_of_vertical_cars:
    a = j_of_vertical_cars.count(j)
    if [j,a] not in no_of_vertical_cars_in_j:
        no_of_vertical_cars_in_j.append([j,a])

for i in i_of_horizontal_cars:
    a = i_of_horizontal_cars.count(i)
    if [i,a] not in no_of_horizontal_cars_in_i:
        no_of_horizontal_cars_in_i.append([i,a]) 

j_of_vertical_cars = list(set(j_of_vertical_cars))
i_of_horizontal_cars = list(set(i_of_horizontal_cars))

V = [[[Bool("V[%i][%i][%i]" %(i,j,k)) for k in range(k+1)] for j in range(n+1)] for i in range(n+1)]

H = [[[Bool("H[%i][%i][%i]" %(i,j,k)) for k in range(k+1)] for j in range(n+1)] for i in range(n+1)]

R = [[[Bool("R[%i][%i][%i]" %(i,j,k)) for k in range(k+1)] for j in range(n+1)] for i in range(n+1)]

M = [[Bool("M[%i][%i]" %(i,j)) for j in range(n+1)] for i in range(n+1)]

# main part starts
temp_T_mines_0 = []
mines =[]
for i in range(n+1):
    for j in range(n+1):
        equal = False
        for no_of_M in range(len(i_j_of_mines)):
            if i==i_j_of_mines[no_of_M][0] and j==i_j_of_mines[no_of_M][1]:
                equal=True
                break
            else:
                continue
        if equal==True:
            temp_T_mines_0.append(M[i][j])
            mines.append([i,j])
        elif equal==False:
            temp_T_mines_0.append(Not(M[i][j]))    

T_mines_0 = And(temp_T_mines_0)

temp_T_vertical_0 = []
for i in range(n+1):
    for j in range(n+1):
        equal = False
        for no_of_V in range(len(i_j_of_vertical_cars)):
            if i==i_j_of_vertical_cars[no_of_V][0] and j==i_j_of_vertical_cars[no_of_V][1]:
                equal=True
                break
            else:
                continue
        if equal==True:
            temp_T_vertical_0.append(V[i][j][0])
        elif equal==False:
            temp_T_vertical_0.append(Not(V[i][j][0]))

T_vertical_0 = And(temp_T_vertical_0)

temp_T_horizontal_0 = []
for i in range(n+1):
    for j in range(n+1):
        equal = False
        for no_of_H in range(len(i_j_of_horizontal_cars)):
            if i==i_j_of_horizontal_cars[no_of_H][0] and j==i_j_of_horizontal_cars[no_of_H][1]:
                equal=True
                break
            else:
                continue
        if equal==True:
            temp_T_horizontal_0.append(H[i][j][0])
        elif equal==False:
            temp_T_horizontal_0.append(Not(H[i][j][0]))

T_horizontal_0 = And(temp_T_horizontal_0)

temp_T_red_0 = []
for i in range(n+1):
    for j in range(n+1):
        if i==red_car_i and j==red_car_j:
            temp_T_red_0.append(R[i][j][0])
        else:
            temp_T_red_0.append(Not(R[i][j][0]))

T_red_0 = And(temp_T_red_0)
temp_list = []
for s in range(k+1):
    for i in range(n+1):
        for j in range(n+1):
            if i==n  :
                temp_list.append(Not(V[i][j][s]))
            if j==n :
                temp_list.append(Not(H[i][j][s]))
                temp_list.append(Not(R[i][j][s]))

            if i not in i_of_horizontal_cars:
                temp_list.append(Not(H[i][j][s]))
            if j not in j_of_vertical_cars:
                temp_list.append(Not(V[i][j][s]))
            if i != red_car_i:
                temp_list.append(Not(R[i][j][s]))
            if [i,j] in mines:
                temp_list.append(Not(R[i][j][s]))
                temp_list.append(Not(H[i][j][s]))
                temp_list.append(Not(R[i][j-1][s]))
                temp_list.append(Not(H[i][j-1][s]))
                temp_list.append(Not(V[i][j][s]))
                temp_list.append(Not(V[i-1][j][s]))
            

T_0 = And(T_mines_0, T_horizontal_0, T_red_0, T_vertical_0, And(temp_list))         # state 0

# -------------------------------------------------input done--------------------------------------------------------

def state_p_to_p_plus_1_vertical(V,H,M,R,p):
    temp=[]
    for j in j_of_vertical_cars: #change possible
        for i in range(n-1):

            c1 = And( V[i-1][j][p] , Not(M[i+1][j]) , Not(H[i+1][j][p]) , Not(H[i+1][j-1][p]) , Not(R[i+1][j][p]) , Not(R[i+1][j-1][p]) , Not(V[i+1][j][p]))
            c2 = And( V[i+1][j][p] , Not(M[i][j]) , Not(H[i][j][p]) , Not(H[i][j-1][p]) , Not(R[i][j][p]) , Not(R[i][j-1][p]) , Not(V[i-1][j][p]))
            c3 = Or( V[i][j][p] , c1 , c2)
            ll = [V[i][j][p] , c1 , c2]
            c3p = AtMost( *ll,1)
            temp.append( Implies( V[i][j][p+1] , And(c3,c3p) ))
            
        not_to_remove_car=[]
        for i in range(n):
            not_to_remove_car.append(V[i][j][p+1])
        no_of_cars = 0
        for a in no_of_vertical_cars_in_j:
            if a[0]==j:
                no_of_cars= a[1]
                break
        temp.append(And(AtMost(*not_to_remove_car,no_of_cars),(AtLeast(*not_to_remove_car,no_of_cars)) ))

        c4 = And( V[n-2][j][p] , Not(M[n][j]) , Not(H[n][j][p]) , Not(H[n][j-1][p]) , Not(R[n][j][p]) , Not(R[n][j-1][p]) )
        l4 = [V[n-1][j][p] , c4]
        c5 = AtMost(*l4,1)
        temp.append( Implies( V[n-1][j][p+1] , And(Or(c4, V[n-1][j][p]) ,c5) ))

    return And(temp)

def state_p_to_p_plus_1_horizontal(V,H,M,R,p):
    temp=[]
    for i in i_of_horizontal_cars: #change possible
        for j in range(n-1):
            c1 = And( H[i][j-1][p] , Not(M[i][j+1]) , Not(V[i][j+1][p]) , Not(V[i-1][j+1][p]) , Not(R[i][j+1][p]) , Not(H[i][j+1][p]) )
            c2 = And( H[i][j+1][p] , Not(M[i][j]) , Not(V[i][j][p]) , Not(V[i-1][j][p]) , Not(R[i][j-1][p]) , Not(H[i][j-1][p]) )
            c3 = Or( H[i][j][p] , c1 , c2)
            li =[ H[i][j][p] , c1, c2]
            c3p = AtMost(*li ,1)
            temp.append( Implies( H[i][j][p+1] , And(c3, c3p) ) )

        c4 = And( H[i][n-2][p] , Not(M[i][n]) , Not(V[i][n][p]) , Not(V[i-1][n][p]) )
        li=[H[i][n-1][p] , c4]
        c5 = AtMost(*li,1)
        temp.append( Implies( H[i][n-1][p+1] , And(Or(c4,H[i][n-1][p]),c5) ))
        
        not_to_remove_car=[]
        for j in range(n):
            not_to_remove_car.append(H[i][j][p+1])
        no_of_cars = 0

        for a in no_of_horizontal_cars_in_i:
            if a[0]==i:
                no_of_cars= a[1]
                break
        temp.append(And(AtMost(*not_to_remove_car,no_of_cars),(AtLeast(*not_to_remove_car,no_of_cars)) ))

    return And(temp)

def state_p_to_p_plus_1_red(V,H,M,R,p):
    temp=[]
    i = red_car_i
    for j in range(n-1):
        c1 = And( R[i][j-1][p] , Not(M[i][j+1]) , Not(V[i][j+1][p]) , Not(V[i-1][j+1][p]) , Not(R[i][j+1][p]) , Not(H[i][j+1][p]) )         
        c2 = And( R[i][j+1][p] , Not(M[i][j]) , Not(V[i][j][p]) , Not(V[i-1][j][p]) , Not(R[i][j-1][p]) , Not(H[i][j-1][p]) )
        c3 = Or( R[i][j][p] , c1 , c2)
        li=[R[i][j][p] , c1, c2]
        c3p = AtMost(*li,1)
        temp.append( Implies( R[i][j][p+1] , And(c3p,c3) ))

    c4 = And( R[i][n-2][p] , Not(M[i][n]) , Not(V[i][n][p]) , Not(V[i-1][n][p]) )
    li=[R[i][n-1][p] , c4]
    c5 = AtMost(*li,1)
    temp.append( Implies( R[i][n-1][p+1] , And(Or(c4,R[i][n-1][p]),c5) ))

    not_to_remove_car=[]
    for j in range(n):
        not_to_remove_car.append(R[i][j][p+1])
    temp.append(And(AtMost(*not_to_remove_car,1),(AtLeast(*not_to_remove_car,1)) ))

    return And(temp)

def exactly_one_moves(V,H,R,p):
    temp=[]
    for j in j_of_vertical_cars: #change possible
        for i in range(n):
            temp.append( Xor( V[i][j][p] , V[i][j][p+1]  ) )

    for i in i_of_horizontal_cars: #change possible
        for j in range(n):
            temp.append(Xor( H[i][j][p] , H[i][j][p+1]  ) )

    i = red_car_i
    for j in range(n):
        temp.append( Xor( R[i][j][p] , R[i][j][p+1] ) )
    
    formula = And(AtMost(*temp,2) , AtLeast(*temp,2))
    return formula

states = []
for a in range(k):
    temp=[]
    temp.append(state_p_to_p_plus_1_vertical(V,H,M,R,a))
    temp.append(state_p_to_p_plus_1_horizontal(V,H,M,R,a))
    temp.append(state_p_to_p_plus_1_red(V,H,M,R,a))
    temp.append(exactly_one_moves(V,H,R,a))
    states.append( And(temp) )


s = Solver()
s.add(T_0)
s.add( And(states) )

finalstate = []
for a in range(k+1):
    finalstate.append( R[red_car_i][n-1][a] )
s.add( And(AtMost(*finalstate,1),AtLeast(*finalstate,1)) ) 

if s.check() == unsat:
    print(unsat)
else:
    m = s.model()
    for kk in range(k):
        if (m.evaluate(R[red_car_i][n-1][kk])):
            break
        for ii in range(n+1):
            if (m.evaluate(R[red_car_i][n-1][kk])):
                break
            for jj in range(n+1):
                if (m.evaluate(R[red_car_i][n-1][kk])):
                    break
                if(not m.evaluate(R[ii][jj][kk]) and m.evaluate(R[ii][jj][kk+1])):
                    if jj == n:
                        continue
                    if (m.evaluate(R[ii][jj+1][kk])):
                        print('%i,%i' %(ii,jj+1))
                    else:
                        print('%i,%i' %(ii,jj))
                if (not m.evaluate(H[ii][jj][kk]) and m.evaluate(H[ii][jj][kk+1])):
                    if jj == n:
                        continue
                    if (m.evaluate(H[ii][jj+1][kk])):
                        print('%i,%i' %(ii,jj+1))
                    else:
                        print('%i,%i' %(ii,jj))
                if ( not m.evaluate(V[ii][jj][kk]) and m.evaluate(V[ii][jj][kk+1])):
                    if ii == n:
                        continue
                    if (m.evaluate(V[ii+1][jj][kk])):
                        print('%i,%i' %(ii+1,jj))
                    else:
                        print('%i,%i' %(ii,jj))