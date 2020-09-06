from simulation import sim
import random
import numpy as np
import scipy as sp
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1 + confidence) / 2., n - 1)
    return m, m - h, m + h

def run_heuristic(num_employees_license, num_employees_credit, num_employees_other, confidence):

    SERVICE_TIME = 12  # Minutes it takes to answer a message
    SIM_TIME = 540  # Simulation time in minutes
    RANDOM_SEED = random.randint(30,90)
    random.seed(RANDOM_SEED)

    license_waiting_time_avg = []
    credit_waiting_time_avg = []
    other_waiting_time_avg = []
    for iteration in range(10):
        results_dict = sim(num_employees_license, num_employees_credit, num_employees_other, SERVICE_TIME, SIM_TIME)
        license_waiting_time_avg.append(results_dict['license'])
        credit_waiting_time_avg.append(results_dict['credit'])
        other_waiting_time_avg.append(results_dict['other'])

    license_confidence_interval = mean_confidence_interval(license_waiting_time_avg, confidence)
    credit_confidence_interval = mean_confidence_interval(credit_waiting_time_avg, confidence)
    other_confidence_interval = mean_confidence_interval(other_waiting_time_avg, confidence)
    return_dict = {
        'license': license_confidence_interval,
        'credit': credit_confidence_interval,
        'other': other_confidence_interval,
    }
    return return_dict

num_employees_license = 0
num_employees_credit = 0
num_employees_other = 0

level = 11
confidence = 0.95
steps = 10
capacity_per_resource = 3

last = False
for j in range(100):
    if steps == 1 or steps == 0:
        last = True

    license_optimal = False
    credit_optimal = False
    other_optimal = False
    for i in range(100):

        if not license_optimal:
            num_employees_license += steps
        if not credit_optimal:
            num_employees_credit += steps
        if not other_optimal:
            num_employees_other += steps

        results = run_heuristic(num_employees_license*capacity_per_resource,
                                num_employees_credit*capacity_per_resource,
                                num_employees_other*capacity_per_resource,
                                confidence)

        if results['license'][-1] < level:
            license_optimal = True

        if results['credit'][-1] < level:
            credit_optimal = True

        if results['other'][-1] < level:
            other_optimal = True


        print("l.employees: {} => {:.2f}\toptimal = {}".format(num_employees_license, results['license'][-1], license_optimal))
        print("c.employees: {} => {:.2f}\toptimal = {}".format(num_employees_credit, results['credit'][-1], credit_optimal))
        print("o.employees: {} => {:.2f}\toptimal = {}\n".format(num_employees_other, results['other'][-1], other_optimal))


        if license_optimal and credit_optimal and other_optimal:
            print("Iter Step: {}, Done".format(steps))
            break
    num_employees_license = (num_employees_license//steps - 1)*steps
    num_employees_credit = (num_employees_credit // steps - 1) * steps
    num_employees_other = (num_employees_other // steps - 1) * steps
    steps = steps // 10

    if last:
        break
