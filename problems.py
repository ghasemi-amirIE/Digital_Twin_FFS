import random
import numpy as np
from main import simulation

M=8
NJ=12
number_of_shifts=1




def env_creator(NJ,M):
   
   machines=[]
   clock_dict={}
   for i in range(M):
        machines.append("m" + str(i+1))
        clock_dict.update({machines[i]:[]})

   sol=[]
   
   for i in range(1, random.randint(8*NJ,10*NJ)):
       sol.append(i)
       


   setup_list=[]
   setup_percentage=0.5


   for i in range(round(len(sol)*setup_percentage)):
       key = tuple(random.sample(sol, 2))
       #value = np.random.gamma(shape=26.98, scale=2.448)
       setup_list.append(key)
       #setup_dict[key] = value 


   cut_points=random.sample(sol,NJ-1)
   cut_points.append(0)
   cut_points.append(sol[-1])
   cut_points=sorted(cut_points)
   
   jobs={}
   for i in range(len(cut_points)-1):
       
       name="j" + str(i+1)
       value=sol[cut_points[i]:cut_points[i+1]]

       jobs.update({name:value})


   first_ops=[]
   operations_job_dict={}
   flexiblity_dict={}
   for item in jobs.keys():
    if len(jobs[item])>0:
      first_ops.append(jobs[item][0])
      for op in jobs[item]:
         operations_job_dict.update({op: item})
         flexiblity_dict.update({op:random.sample(machines,random.randint(1,M))})
    
    
    
    plain_sheduele_plan={}
    machines_ready_dict={}

    for item in machines:
        plain_sheduele_plan.update({item:[]})
        machines_ready_dict.update({item:random.randint(0,5)*np.random.gamma(shape=26.98, scale=2.448)})   #ready times

    



   return(sol,jobs,first_ops,operations_job_dict,flexiblity_dict,machines,plain_sheduele_plan,setup_list,clock_dict,machines_ready_dict)


sol,jobs,first_ops,operations_job_dict,flexiblity_dict,machines,plain_sheduele_plan,setup_list,clock_dict,machines_ready_dict=env_creator(12,8) #create problem environment
#sol_creator(NJ,M)
# processing_times,s1_s2,operations_job_dict,first_ops,scheduele_plan,setup_dict

def chromosome_repair(chromosome,jobs):

    
    for job in jobs.keys():

        for i in range(len(jobs[job])-1):

            for j in range(i+1,len(jobs[job])):
           
                a=jobs[job][i]
                b=jobs[job][j]
                index1=chromosome.index(a)
                index2=chromosome.index(b)

                if index1>index2:
                    chromosome[index2]=a
                    chromosome[index1]=b
    
    return chromosome



def chromosome_creator(sol,jobs):

    chromosome=sol.copy()
    random.shuffle(chromosome)
    
    chromosome=chromosome_repair(chromosome,jobs)

    return chromosome


def schedule_creator(sol,jobs,flexiblity_dict,plain_sheduele_plan):
   
   sol_chr=chromosome_creator(sol,jobs)

   for item in sol_chr:
       
       mach=random.sample(flexiblity_dict[item],1)
       a=mach[0]
       plain_sheduele_plan[a].append(item)
    
   operations_machine_dict={}
   for item in plain_sheduele_plan.keys():
       for op in plain_sheduele_plan[item]:
           operations_machine_dict.update({op: item})
    
   s1_s2={"s1":sol_chr}

   return sol_chr,plain_sheduele_plan,operations_machine_dict,s1_s2




#print(chromosome_creator(sol,jobs))
#print(flexiblity_dict)
sol_chr,scheduele_plan,operations_machine_dict,s1_s2=schedule_creator(sol,jobs,flexiblity_dict,plain_sheduele_plan)



# simulation(M,jobs,processing_times,s1_s2,operations_job_dict,first_ops,scheduele_plan,setup_dict)

makespan_reps=[]
for i in range(20):

    makespan_reps.append(simulation(M,jobs,s1_s2,operations_job_dict,operations_machine_dict,first_ops,scheduele_plan,setup_list,clock_dict,machines_ready_dict))
print(setup_list,machines_ready_dict,jobs,scheduele_plan,makespan_reps)