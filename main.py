# import pymongo
# myclient = pymongo.MongoClient("mongodb://localhost:27017")
# mydb = myclient["DT_SchedulingDB"]
# mycol = mydb["Shift2"]
import numpy as np





def setup_needed(op1,op2,setup_list):
    if (op1,op2) in setup_list:
        return True


#def clock_forward(current_clock, move_forward):

 #   current_clock=current_clock+move_forward

  #  return current_clock



def simulation(M,jobs,s1_s2,operations_job_dict,operations_machine_dict,first_ops,scheduele_plan,setup_list,clock_dict,machines_ready_dict):

    
   processing_times=[]
   for i in range(len(s1_s2["s1"])):
       processing_times.append(np.random.gamma(shape=26.98, scale=2.448))


   events_list=[]
   assigned_ops=[]
   start_ops={}
   finish_ops={}

   for item in scheduele_plan.keys():
        
        if scheduele_plan[item][0] in first_ops:
           a=scheduele_plan[item][0]
           clock_dict[item].append(machines_ready_dict[item])
           clock_dict[item].append(machines_ready_dict[item]+processing_times[a-1])
           start_ops.update({a:machines_ready_dict[item]})
           finish_ops.update({a:machines_ready_dict[item]+processing_times[a-1]})
           assigned_ops.append(a)
           events_list.append({"event_type": "production",
                               "operation_event_type": "start",
                               "job_event_type": "start",
                               "clock": machines_ready_dict[item],
                               "operation_id": a,
                               "job_id": operations_job_dict[a],
                               "machine_id": item
                               })
           
           events_list.append({"event_type": "production",
                               "operation_event_type": "finish",
                               "job_event_type": "None",
                               "clock": clock_dict[item][-1],
                               "operation_id": a,
                               "job_id": operations_job_dict[a],
                               "machine_id": item
                               })
    
   for op in s1_s2["s1"]:
        
        if op not in assigned_ops:
            
            job= operations_job_dict[op]
            m = operations_machine_dict[op]
            if op in first_ops:

                index=scheduele_plan[m].index(op)

                if setup_needed(scheduele_plan[m][index-1],op,setup_list):
                    op_start = clock_dict[m][-1]+(5*np.random.gamma(shape=26.98, scale=2.448))   #setup_time added

                else:    
                    op_start = clock_dict[m][-1] 

                #op_start = clock_dict[m][-1]  #dont forget to include setup times
                clock_dict[m].append(op_start)
                clock_dict[m].append(op_start+processing_times[op-1])
                assigned_ops.append(op)
                start_ops.update({op:op_start})
                finish_ops.update({op:op_start+processing_times[op-1]})

                events_list.append({"event_type": "production",
                               "operation_event_type": "start",
                               "job_event_type": "None",
                               "clock": op_start,
                               "operation_id": op,
                               "job_id": operations_job_dict[op],
                               "machine_id": m
                               })
                
                events_list.append({"event_type": "production",
                               "operation_event_type": "finish",
                               "job_event_type": "None",
                               "clock": clock_dict[m][-1],
                               "operation_id": op,
                               "job_id": operations_job_dict[op],
                               "machine_id": m
                               })
            
            elif op == scheduele_plan[m][0]:
                
                start=max(finish_ops[op-1],machines_ready_dict[m])
                finish=start+processing_times[op-1]
                assigned_ops.append(op)
                
                start_ops.update({op:start})
                finish_ops.update({op:finish})


                clock_dict[m].append(start)
                clock_dict[m].append(finish)

                events_list.append({"event_type": "production",
                               "operation_event_type": "start",
                               "job_event_type": "None",
                               "clock": start,
                               "operation_id": op,
                               "job_id": job,
                               "machine_id": m
                               })
                
                events_list.append({"event_type": "production",
                               "operation_event_type": "finish",
                               "job_event_type": "None",
                               "clock": clock_dict[m][-1],
                               "operation_id": op,
                               "job_id": job,
                               "machine_id": m
                               })
                

            else:
                index=scheduele_plan[m].index(op)
                
                if setup_needed(scheduele_plan[m][index-1],op,setup_list):
                    start = max(finish_ops[op-1],clock_dict[m][-1]+
                                   (5*np.random.gamma(shape=26.98, scale=2.448)))   #setup time added
                else:    
                    start = max(finish_ops[op-1],clock_dict[m][-1])
                
                #start=max(clock_dict[m2][pos2],clock_dict[m][-1])
                finish=start+processing_times[op-1]
                assigned_ops.append(op)

                clock_dict[m].append(start)
                clock_dict[m].append(finish)

                start_ops.update({op: start})
                finish_ops.update({op: finish})


                events_list.append({"event_type": "production",
                               "operation_event_type": "start",
                               "job_event_type": "None",
                               "clock": start,
                               "operation_id": op,
                               "job_id": job,
                               "machine_id": m
                               })
                
                events_list.append({"event_type": "production",
                               "operation_event_type": "finish",
                               "job_event_type": "None",
                               "clock": clock_dict[m][-1],
                               "operation_id": op,
                               "job_id": job,
                               "machine_id": m
                               })

   makespan = max(finish_ops.values())
           
    #return(events_list,makespan)
   return(makespan)


#result= simulation(M,jobs,processing_times,s1_s2,operations_job_dict,first_ops,scheduele_plan,setup_dict)

#print(result)
#x = mycol.insert_many(result)

