'''
Implementation of Genetic Algorithm to solve Shakespear's Monkey Problem
By Surender Harsha and Pranay Chimmani
'''


#Import Statements
import Tkinter as tk
import random
import time



#The Character Space and Total Children for each pair in population
space="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@. "
total_children=14
splen=len(space)

##################################################################################################################################################
#Function To Remove Duplicates in a list
def Remove(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

###################################################################################################################################################
#Create the most suitable pairs from a Population
def create_pairs(tar,p):

	#Temporary variables
    pairs=[]
    selected=[]
    #Score of each string in population store in dictionary, STRING:SCORE
    pop_score={}

    #Calculate fitness for each string in the population and store in dictionary
    for i in p:
        pop_score[i]=calculate_fitness(tar,i)

    #A temporary variable to store the temporary pair
    pi=[]
    #Find the maximum score in the dictionary
    l=pop_score[max(pop_score, key=pop_score.get)]
    #Sort and get list in order from best fit members to least fit members
    p = sorted(pop_score, key=pop_score.get)
    p=p[::-1]

    #Get the first 20 Best ones to display
    best_ones=p[:20]
    
    #Run as long as the all the members in the population have a pair, ensure that Population is an even number.
    while (len(pairs)*2)<len(p):

    	#Add the pair, to 'pair' list, when a pair is formed.
        if len(pi)==2:
            pairs.append(pi)
            pi=[]
            continue

        #Search population
        for i in range(len(p)):

            if len(pi)==2:
                break
            if p[i] not in selected:
                k=random.randint(0,l)
                #Probability of selecting a member based on its score and a random number.
                if k<=pop_score[p[i]]:
                    pi.append(p[i])
                    selected.append(p[i])

    
    return pairs,best_ones

#####################################################################################################################################################
#Function to calculate fitness, Normal character to character match, or Character position evaluation along with matching.
def calculate_fitness(target,member):
    score=0
    total_score=(len(target)*(len(target)+1))/2
    #Check character by character
    for i in range(len(target)):
        if target[i]==member[i]:
        	#Remove comment and comment the second one to implement Character position evaluation.
            #score+=len(target)-i
            score+=1
    #Get percentage of score based on string length.
    return int((float(score)/len(target))*100)

#######################################################################################################################################################
#Generate Population based on size and string length.
def gen_population(size,leng):
    pop=[]
    for i in range(size):
        arc=""
        for j in range(leng):
        	#Random character from character space and create a string.
            k=random.randint(0,splen-1)
            arc+=space[k]
        pop.append(arc)
    return pop

##########################################################################################################################################################
#Important, Crossover of pairs to create children. Two best children will be picked according to fitness and rest will be discarded.
def crossover(pai,pop,target):
    global total_children
    #Storing original length
    st=len(pop)
    #New population
    po=[]
   	#Iterate through each pair
    for i in range(len(pai)):
        s=pai[i] 
        a=s[0]
        b=s[1]
        l=len(a)
        t=random.randint(0,len(a)-1)

        #Set of random jumbling and crossover, including splitting and uniform crossover and random splitting.
        x1=a[:t]+b[t:]
        y1=a[t:]+b[:t]
        x2=b[t:]+a[:t]
        y2=b[:t]+a[t:]
        a1=a[:l/2]+b[l/2:]
        b1=b[:l/2]+a[l/2:]
        c1=b[l/2:]+a[:l/2]
        d1=a[l/2:]+b[:l/2]
        for j in range(1,len(a),2):
            x=a[:j]+b[j]+a[j+1:]
            y=b[:j]+a[j]+b[j+1:]
            a=x
            b=y
   
        #Calculate fitness of each of these new children and store them in a dictionary, like in create_pairs.
        dic={}
        dic[a1]=calculate_fitness(target,a1)
        dic[b1] = calculate_fitness(target, b1)
        dic[c1] = calculate_fitness(target, c1)
        dic[d1] = calculate_fitness(target, d1)
        dic[a1[::-1]]=calculate_fitness(target,a1[::-1])
        dic[b1[::-1]] = calculate_fitness(target, b1[::-1])
        dic[c1[::-1]] = calculate_fitness(target, c1[::-1])
        dic[d1[::-1]] = calculate_fitness(target, d1[::-1])
        dic[a] = calculate_fitness(target, a)
        dic[b] = calculate_fitness(target, b)
        dic[x1] = calculate_fitness(target, x1)
        dic[y1] = calculate_fitness(target, y1)
        dic[x2] = calculate_fitness(target, x2)
        dic[y2] = calculate_fitness(target, y2)

        #Fill missing children or add extra adopted children made of complete random strings to add variation.
        for i in range(0,total_children-len(dic)):
            arc = ""
            for j in range(len(target)):
                k = random.randint(0, splen - 1)
                arc += space[k]
            dic[arc]=calculate_fitness(target,arc)

        #Children are sorted according to their fitness
        sorted_child = sorted(dic, key=dic.get)
        flag=0
        sorted_child=sorted_child[::-1]

        #Add two best children to population.
        for i in sorted_child:
        	if flag>=2:
        		break
        	if i not in po:
        		po.append(i)
                        flag+=1
        
    
    #Remove any duplicates in population.
    po=Remove(po)

    #Make sure new population length is same as old population, also adds new variation if members are missing.
    for i in range(st-len(po)):
        arc = ""
        for j in range(len(target)):
            k = random.randint(0, splen - 1)
            arc += space[k]
        if arc not in po:
            po.append(arc)

    return po

###############################################################################################################################################################
#Perform mutations according to the mutation rate on the population
def mutations(pop,mutation,target):
	#Store original length of population
    st=len(pop)

    #Iterate through population
    for i in range(len(pop)):
        s=pop[i]
        for j in range(len(s)):
        	#For each character a probability of mutation rate exists to replace it with a random character.
            k=random.randint(0,100)
            if k<=mutation:
                t=random.randint(0,splen-1)
                s=s[:j]+space[t]+s[j+1:]
        pop[i]=s

    #Check for duplicates and remove them
    pop = Remove(pop)

    #Replace missing members of population. Adds variation.
    for i in range(st - len(pop)):
        arc = ""
        for j in range(len(target)):
            k = random.randint(0, splen - 1)
            # print k
            arc += space[k]
        if arc not in pop:
            pop.append(arc)
    return pop
#############################################################################################################################################################
#The Algorithm that runs when 'Run' button is pressed.
def Algo():
   
	#Get values from fields.
    population=int(populationE.get())
    mutation=int(mutationE.get())
    target=targetE.get()
    length=len(target)

    #Initialize random population
    init_pop=gen_population(population,length)

    #Initialize best fitness and best phrase string.
    best_fitness=1
    best_phrase=""
    pop=init_pop

    #Number of generations
    k=1
    #Average fitness
    avg=0
    #Run algorithm until the fitness of 100% is found
    while best_fitness<100:
    	#Print population to python console
        print pop

        #Get the pairs and the best 20 of the population.
        pairs,best_ones = create_pairs(target, pop)
        #Crossover the pairs
        pop=crossover(pairs,pop,target)
        #Mutate members in the population.
        pop=mutations(pop,mutation,target)

        #Calculate fitness for each member in population, along with the sum. Note down, best fitness and best phrase.
        for i in pop:
            c=calculate_fitness(target,i)
            avg+=c
            if c>best_fitness:
                best_fitness=c
                best_phrase=i

        #Calculate the average fitness.
        avg=float(avg)/len(pop)

        #Update labels of fitness, average fitness, Best phrase and Generations completed, including updating of 20 best members in population.
        BestP=tk.Label(w,text=best_phrase+"           Fitness:"+str(best_fitness)+"           Average:"+str(avg))
        BestP.place(relx=0.14,rely=0.7)
        Generations=tk.Label(w,text=str(k))
        Generations.place(relx=0.15,rely=0.8)
        ListB=tk.Listbox(w,height=20)
        for i in range(len(best_ones)):
            ListB.insert(i+1,best_ones[i])
        ListB.place(relx=0.7,rely=0.25)
        w.update()
        avg=0
        k+=1
########################################################################################################################################################
#INPUT EXPECTED
'''
Target: String
Population: Even number >10
Mutation: Percentage 0-100
'''
################################################MAIN#####################################################################################################
#Main , Initialization of window
w= tk.Tk()
w.title("Genetic Algorithm")
w.geometry("1270x720")

#Labels for heading, settings and input widgets needed to create GUI.
heading=tk.Label(w,text="Genetic Algorithm Example")
heading.place(relx=0.43,rely=0.01)

settings=tk.Label(w,text="Set your variables")
settings.place(relx=0.1,rely=0.4)

targetL=tk.Label(w,text="Target String:")
targetE=tk.Entry(w)
targetL.place(relx=0.08,rely=0.45)
targetE.place(relx=0.14,rely=0.45,width=200)

populationL=tk.Label(w,text="Population:")
populationE=tk.Entry(w)
populationL.place(relx=0.08,rely=0.5)
populationE.place(relx=0.135,rely=0.5)

mutationL=tk.Label(w,text="Mutation:")
mutationE=tk.Entry(w)
mutationL.place(relx=0.08,rely=0.55)
mutationE.place(relx=0.128,rely=0.55)

#Run Algo function when button is pressed
B=tk.Button(w,text="Run",command=Algo)

#Place the widgets
B.place(relx=0.09,rely=0.6)
BP=tk.Label(w,text="Best Text:")
BP.place(relx=0.08,rely=0.7)
gen=tk.Label(w,text="Generations:")
gen.place(relx=0.09,rely=0.8)
#Run Window
w.mainloop()

################################################THE END################################################################################################
