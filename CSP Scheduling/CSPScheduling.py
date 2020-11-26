from constraint import *

#We will divide the problem into two subproblems.
#First problem: assigning Subjects to days
#Second subproblem: assigning Teachers to subjects

Scheduling = Problem()

#Therefore, we can define a constraint network as a tuple (X, D, R)

#The set of variables X is defined as follows:
Scheduling.addVariables(['M1', 'M2', 'M3', 'T1', 'T2', 'T3', 'W1', 'W2', 'W3', 'Th1', 'Th2'], ['PE', 'Naturals', 'Socials', 'Maths', 'Spanish', 'English'])

#The valid domain D for those variables is defined as follows
Scheduling.addVariables(['PE', 'Naturals', 'Socials', 'Maths', 'Spanish', 'English'], ['Lucia', 'Andrea', 'Juan'])

#The set of constraints R will be implemented in Python functions, and then added to the problem with the variables which it affects

#Constraint 1: each lecture lasts one hour, and only one subject can be lectured
#it is inferred within the problem

#Constraint 2: all Domain should be lectured two hours every week but PE, that should only be assigned only one hour
def everySubject(m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2):
    Timetable = [m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2]
    if Timetable.count('English')!=2: return False
    if Timetable.count('Spanish')!=2: return False
    if Timetable.count('Maths')!=2: return False
    if Timetable.count('Socials')!=2: return False
    if Timetable.count('Naturals')!=2: return False
    if Timetable.count('PE')!=1: return False
    return True


#Constraint 3: Socials should have consecutive hours
def consecutiveSocial(m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2):
    Timetable = [m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2]
    index=Timetable.index('Socials')
    if index==2 or index==5 or index==8: return False
    return Timetable[Timetable.index('Socials') +1]=='Socials'


#Constraint 5: Maths should be first in the morning & Naturals last
def firstMathsLastNat(m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2):
    Timetable = [m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2]
    for i in range(len(Timetable)):
        if Timetable[i]=='Maths':
            if not (i==0 or i==3 or i==6 or i==9):
                return False
        if Timetable[i]=='Naturals':
            if not (i==2 or i==5 or i==8 or i==10):
                return False
    return True




#Constraint 4: Maths cannot be on same day than Naturals or English
def mathsNat(m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2):
    Timetable = [m1,m2,m3,t1,t2,t3,w1,w2,w3,th1,th2]
    for i in range(0, len(Timetable), 3):
        if Timetable[i]=='Maths':
            #mondays, tuesdays and wednesday
            if i!=9:
                if Timetable[i+1]=='English' or Timetable[i+2]=='English' or Timetable[i+2]=='Naturals':
                    return False
            else: 
                if Timetable[i+1]=='English' or Timetable[i+1]=='Naturals':
                    return False

    return True      


#Constraint 6: Each teacher should lecture two subjects
def DiffDomainPerTeacher(PE, Naturals, Socials, Maths, Spanish, English):
    Subjects = [PE, Naturals, Socials, Maths, Spanish, English]
    l=0
    a=0
    j=0
    for i in range (len(Subjects)):
        if Subjects[i]=='Lucia':
            l+=1
        if Subjects[i]=='Andrea':
            a+=1
        if Subjects[i]=='Juan':
            j+=1
    if l==2 and a==2 and j==2:
        return True
    else:
        return False




#Constraint 7: Lucia will take care of Socials provided that Andrea takes care of PE
def LuciaSocialsAndreaPE(PE, Socials):
    if PE=='Andrea':
        if not (Socials == 'Lucia'):
            return False
    return True


#Constraint 8: Juan wants to lecture neither Natural Sciences nor Social and Human Sciences, if any of these are allocated first in the morning either on Monday or Thursday.
#naturals at first is already prevented by constraint 5
def JuanNotMornings(m1,th1,Socials):
    if m1=='Socials' or th1=='Socials':
        if Socials=='Juan':
            return False
    return True
    


#Here, we add all the different constraints to the problem
Scheduling.addConstraint(everySubject, ('M1', 'M2', 'M3', 'T1', 'T2', 'T3', 'W1', 'W2', 'W3', 'Th1', 'Th2'))
Scheduling.addConstraint(consecutiveSocial, ('M1', 'M2', 'M3', 'T1', 'T2', 'T3', 'W1', 'W2', 'W3', 'Th1', 'Th2'))
Scheduling.addConstraint(mathsNat, ('M1', 'M2', 'M3', 'T1', 'T2', 'T3', 'W1', 'W2', 'W3', 'Th1', 'Th2'))
Scheduling.addConstraint(firstMathsLastNat, ('M1', 'M2', 'M3', 'T1', 'T2', 'T3', 'W1', 'W2', 'W3', 'Th1', 'Th2'))
Scheduling.addConstraint(DiffDomainPerTeacher, ('PE', 'Naturals', 'Socials', 'Maths', 'Spanish', 'English'))
Scheduling.addConstraint(LuciaSocialsAndreaPE, ('PE', 'Socials'))
Scheduling.addConstraint(JuanNotMornings, ('M1','Th1','Socials'))


print(Scheduling.getSolution())
#printSolutions()
