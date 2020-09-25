import random
import simpy
import numpy as np

demand_distribution_o = [
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

demand_distribution = []

total_daily_messages = 6000
hourly_parameter = []

def generate_hourly_param():
    global hourly_parameter
    hourly_parameter = []
    for dist in demand_distribution:
        hourly_parameter.append(((total_daily_messages * dist / 60)))
    #hourly_parameter = hourly_parameter[:9]
    #hourly_parameter = [12, 0.07, .07, .08, .1, .16, .21, .21, .41]
    #print(hourly_parameter)

def exp(p, lambda_):
    return ((-1/lambda_)*np.log(1 - p))

def sim(NUM_EMPLOYEES_LICENSE, NUM_EMPLOYEES_CREDIT, NUM_EMPLOYEES_OTHER, SERVICE_TIME, SIM_TIME, morning, total_daily):
    global demand_distribution_o, demand_distribution
    if morning:
        demand_distribution = demand_distribution_o
    else:
        demand_distribution = demand_distribution_o
    generate_hourly_param()
    license_waiting_time = []
    credit_waiting_time = []
    other_waiting_time = []

    class CallCenterLicense(object):
        def __init__(self, env, num_employess, service_time):
            self.env = env
            self.employee = simpy.Resource(env, num_employess)
            self.service_time = service_time

        def attend(self, message):
            real_service_time = exp(random.random(), .056)
            yield self.env.timeout(real_service_time)

    class CallCenterCredit(object):
        def __init__(self, env, num_employess, service_time):
            self.env = env
            self.employee = simpy.Resource(env, num_employess)
            self.service_time = service_time

        def attend(self, message):
            real_service_time = exp(random.random(), .056)
            yield self.env.timeout(real_service_time)

    class CallCenterOther(object):
        def __init__(self, env, num_employess, service_time):
            self.env = env
            self.employee = simpy.Resource(env, num_employess)
            self.service_time = service_time

        def attend(self, message):
            real_service_time = exp(random.random(), .056)
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


    def setup(env, num_employees_license, num_employees_credit, num_employees_other, service_time, total_daily):

        # Create the call_centers
        call_center_license = CallCenterLicense(env, num_employees_license, service_time)
        call_center_credit = CallCenterCredit(env, num_employees_credit, service_time)
        call_center_other = CallCenterOther(env, num_employees_other, service_time)

        global total_daily_messages
        total_daily_messages = total_daily

        mm = .5
        if not morning:
            mm += .5

        # Create messages while the simulation is running
        i = 0
        while True:
            current_hour = int(env.now//60)
            yield env.timeout(exp(random.random(), hourly_parameter[current_hour])*mm)
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
    env.process(setup(env, NUM_EMPLOYEES_LICENSE, NUM_EMPLOYEES_CREDIT, NUM_EMPLOYEES_OTHER, SERVICE_TIME, total_daily))

    # Execute!
    env.run(until=SIM_TIME)
    return_dict = {
        'license': np.average(license_waiting_time),
        'credit': np.average(credit_waiting_time),
        'other': np.average(other_waiting_time),
    }
    return return_dict