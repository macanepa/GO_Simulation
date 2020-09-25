import heuristic
import os
import xlwt
import mcutils as mc

def save_to_xl(path, results, confidence, demand):
    xl_worksheet = xlwt.Workbook()
    results_sheet = xl_worksheet.add_sheet('Results')

    results_sheet.write(0,0,'CATEGORY')
    results_sheet.write(1,0,'N° EMPLOYEES')
    results_sheet.write(2, 0, 'CONF.INTERVAL HIGH BOUND')
    for index, value in enumerate(results):
        results_sheet.write(0, index + 1, value)
        results_sheet.write(1, index + 1, results[value]['number_employees'])
        results_sheet.write(2, index + 1, results[value]['confidence_interval'][-1])

    m_license = results['license_morning']['number_employees']
    m_credit = results['credit_morning']['number_employees']
    m_other = results['other_morning']['number_employees']

    a_license = results['license_afternoon']['number_employees']
    a_credit = results['credit_afternoon']['number_employees']
    a_other = results['other_afternoon']['number_employees']

    pt_license = abs(m_license - a_license)
    ft_license = min(m_license, a_license)

    pt_credit = abs(m_credit - a_credit)
    ft_credit = min(m_credit, a_credit)

    pt_other = abs(m_other - a_other)
    ft_other = min(m_other, a_other)

    results_sheet.write(4, 0, 'LICENSE FULL TIME EMPLOYEES')
    results_sheet.write(5, 0, 'CREDIT FULL TIME EMPLOYEES')
    results_sheet.write(6, 0, 'OTHER FULL TIME EMPLOYEES')

    results_sheet.write(7, 0, 'LICENSE PART TIME EMPLOYEES')
    results_sheet.write(8, 0, 'CREDIT PART TIME EMPLOYEES')
    results_sheet.write(9, 0, 'OTHER PART TIME EMPLOYEES')

    results_sheet.write(4, 1, ft_license)
    results_sheet.write(5, 1, ft_credit)
    results_sheet.write(6, 1, ft_other)

    results_sheet.write(7, 1, pt_license)
    results_sheet.write(8, 1, pt_credit)
    results_sheet.write(9, 1, pt_other)


    results_sheet.write(11, 0, 'ESTIMATED DEMAND')
    results_sheet.write(11, 1, demand)

    results_sheet.write(12, 0, 'CONFIDENCE')
    results_sheet.write(12, 1, confidence)

    xl_worksheet.save(path)
    os.system('{}'.format(path))
    exit()




total_daily = int(mc.get_input(text='Introduce la demanda total diaria estimada (numero entero)', return_type=int))
max_time = int(mc.get_input(text='Introduce el tiempo maximo de espera (numero entero en minutos)', return_type=int))
while True:
    conf = mc.get_input(text='Introduce nivel de confianza (dejar en blanco para default 0.95)')
    if conf == '':
        confidence = 0.95
        break
    else:
        try:
            confidence = float(conf)
            if confidence < 1 and confidence > 0:
                break
        except:
            None


final_m = heuristic.initialize(morning=True, total_daily=total_daily, confidence=confidence)
final_a = heuristic.initialize(morning=False, total_daily=total_daily, confidence=confidence)

final_m.update(final_a)
final = final_m

print(final)
path = os.getcwd()
path = os.path.join(path, 'data_output.xls')
save_to_xl(path, final, confidence, total_daily)

print("Saving file to xl")
print("END")