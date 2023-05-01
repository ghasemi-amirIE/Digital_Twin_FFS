import pickle
from problems import env_creator,schedule_creator
from main import simulation

instances=[]
for num in range(20000):

    instances.append("instance" + str(num))

    sol,jobs,first_ops,operations_job_dict,flexiblity_dict,machines,plain_sheduele_plan,setup_list,clock_dict,machines_ready_dict=env_creator(12,8)
    
    instances.append(jobs)
    instances.append(machines_ready_dict)
    instances.append(setup_list)

    sol_chr,scheduele_plan,operations_machine_dict,s1_s2=schedule_creator(sol,jobs,flexiblity_dict,plain_sheduele_plan)

    instances.append(scheduele_plan)

    
    makespan_reps=[]
    for i in range(100):

       makespan_reps.append(simulation(8,jobs,s1_s2,operations_job_dict,operations_machine_dict,first_ops,scheduele_plan,setup_list,clock_dict,machines_ready_dict))
    
    instances.append(makespan_reps)
 
with open('data2.pkl', 'wb') as f:
    pickle.dump(instances, f)