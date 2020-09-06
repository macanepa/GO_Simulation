import random
import simpy
import numpy as np

dist_demand = [
                .0012,
                .2043,
                .2008,
                .1721,
                .1464,
                .085,
                .0668,
                .0682,
                .0341,
                .0114,
                .0079,
                .0016,
                ]


total_day = 4282
demand = []

for dist in dist_demand:
    demand.append((1/(total_day*dist/60)*100.0)//1/100.0)
demand = demand[:9]
demand = [12,0.07,.07,.08,.1,.16,.21,.21,.41]
#demand = [11.676786548341898, 0.06858611775824902, 0.06978159291837786, 0.08141861625804925, 0.0957113651503434, 0.1648487512707091, 0.20976263260494427, 0.20545665480953484, 0.4109133096190697]


print(demand)
input("enter to continue...")

def exp(p, lambda_):
    return ((-1/lambda_)*np.log(1 - p))

def sim(NUM_EMPLOYEES_LICENSE, NUM_EMPLOYEES_CREDIT, NUM_EMPLOYEES_OTHER, SERVICE_TIME, SIM_TIME):

    license_waiting_time = []
    credit_waiting_time = []
    other_waiting_time = []

    class CallCenterLicense(object):
        def __init__(self, env, num_employess, service_time):
            self.env = env
            self.employee = simpy.Resource(env, num_employess)
            self.service_time = service_time

        def attend(self, message):
            real_service_time = exp(random.random(), .056/4)
            yield self.env.timeout(real_service_time)



    class CallCenterCredit(object):
        def __init__(self, env, num_employess, service_time):
            self.env = env
            self.employee = simpy.Resource(env, num_employess)
            self.service_time = service_time

        def attend(self, message):
            real_service_time = exp(random.random(), .056/4)
            yield self.env.timeout(real_service_time)



    class CallCenterOther(object):
        def __init__(self, env, num_employess, service_time):
            self.env = env
            self.employee = simpy.Resource(env, num_employess)
            self.service_time = service_time

        def attend(self, message):
            real_service_time = exp(random.random(), .056/4)
            yield self.env.timeout(real_service_time)





    def message_license(env, name, cc):

        init = env.now
        with cc.employee.request() as request:
            yield request
            license_waiting_time.append(env.now - init)
            yield env.process(cc.attend(name))

    def message_credit(env, name, cc):

        init = env.now
        with cc.employee.request() as request:
            yield request
            credit_waiting_time.append(env.now - init)
            yield env.process(cc.attend(name))

    def message_other(env, name, cc):

        init = env.now
        with cc.employee.request() as request:
            yield request
            other_waiting_time.append(env.now - init)
            yield env.process(cc.attend(name))


    def setup(env, num_employees_license, num_employees_credit, num_employees_other, service_time):

        # Create the call_centers
        call_center_license = CallCenterLicense(env, num_employees_license, service_time)
        call_center_credit = CallCenterCredit(env, num_employees_credit, service_time)
        call_center_other = CallCenterOther(env, num_employees_other, service_time)


        # Create messages while the simulation is running
        i = 0
        while True:
            current_hour = int(env.now//60)
            yield env.timeout(exp(random.random(), demand[current_hour]))
            i += 1
            choice = random.random()
            if choice < 0.41:
                env.process(message_license(env, 'License Message %d' % i, call_center_license))
            elif choice < 0.84:
                env.process(message_credit(env, 'Credit Message %d' % i, call_center_credit))
            else:
                env.process(message_other(env, 'Other Message %d' % i, call_center_other))

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, NUM_EMPLOYEES_LICENSE, NUM_EMPLOYEES_CREDIT, NUM_EMPLOYEES_OTHER, SERVICE_TIME))

    # Execute!
    env.run(until=SIM_TIME)
    return_dict = {
        'license': np.average(license_waiting_time),
        'credit': np.average(credit_waiting_time),
        'other': np.average(other_waiting_time),
    }
    return return_dict