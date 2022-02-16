import pandas as pd
from sqlalchemy import column
import combinator
import time
import math
import xlsxwriter
import os
import re


def combinator(tolerance, target, inputs):
    
    # Special case for inputs with one element, speeds up computation a lot
    if len(inputs) == 1:
        number = inputs[0]
        result_min = int(math.ceil((target-tolerance)/number))
        result_max = int(math.floor((target+tolerance)/number))
        for factor in range(result_min, result_max+1):
            yield [factor]
        return

    # Special case for no inputs, just to prevent infinite recursion 
    if not inputs:
        return

    number = inputs[-1]
    max_value = int(math.floor((target + tolerance)/number))

    for i in range(max_value+1):
        for sub_factors in combinator(tolerance, target-i*number, inputs[:-1]):
            sub_factors.append(i)
            yield sub_factors


def get_trailing_number(s):
    m = re.search(r'\d+$', s)
    return int(m.group()) if m else 1

def del_trailing_number(s):
    m = re.sub(r'\d+$', '', s)
    return m

def main(file_path, file_name, target, Mass_resolution):

    file_path =  file_path
    file_name =  file_name
    target =  target
    Mass_resolution =  Mass_resolution

    isotope_table = pd.read_excel(file_path + file_name)
    inputs = list(isotope_table["Exact Mass"])
    ele_labels = list(isotope_table["Species"])
    abundance = list(isotope_table["Abundance"])
    
    # target = "93Nb 16O2"
    elements = target.split(" ")
    mass = 0
    for ele in elements:
        print(ele)
        atom_num = get_trailing_number(ele)
        isotope = del_trailing_number(ele)
        print(isotope + " atom num: " + str(atom_num))
        index = ele_labels.index(isotope)
        mass = mass + inputs[index] * atom_num
    target_mass = mass
    # Mass_resolution = 6000
    tolerance = target_mass/Mass_resolution/2

    t_start = time.perf_counter()
    results = list(combinator(tolerance, target_mass, inputs))
    t_end = time.perf_counter()
    
    # head of xlsx
    head = [
        "Mass", 
        "Delta to target", 
        "Number of atoms", 
        "Abundance",
        "Ion",
        ]
    xlsx_name = [
        file_path + file_name[:-5],
     " ion-" + target + "-results-_mass_range " ,
     str(format(tolerance*2, '.4f')) + "(amu)" + ".xlsx"
     ]
    workbook = xlsxwriter.Workbook(xlsx_name[0]+xlsx_name[1]+xlsx_name[2])
    worksheet = workbook.add_worksheet("comb")
    row = 0
    column = 0

    worksheet.write(row, column, head[column])
    worksheet.write(row, column+1, head[column+1])
    worksheet.write(row, column+2, head[column+2])
    worksheet.write(row, column+3, head[column+3])
    worksheet.write(row, column+4, head[column+4])

    row += 1

    for result in results:
        result_str = ""
        result_lab = ""
        result_value = 0
        num_of_atoms = sum(result)
        result_abun = 1
        # for factor, value in zip(result, inputs):
        for factor, value, labs, abun in zip(result, inputs, ele_labels, abundance):
            if not factor:
                continue
            if result_str != "":
                result_str += " + "
            if result_lab != "":
                result_str += " "
            result_str += "{}* {}".format(factor, value)
            
            factors = factor
            if factor == 1: factors = ""
            result_lab += "{}{} ".format(labs, factors)
            result_value += factor*value
            result_abun = result_abun*pow(abun/100, factor)

        delta = result_value - target_mass

        if result_abun>1e-3 and num_of_atoms<6:
            worksheet.write(row, column, result_value)
            worksheet.write(row, column+1, delta)
            worksheet.write(row, column+2, num_of_atoms)
            worksheet.write(row, column+3, result_abun)
            worksheet.write(row, column+4, result_lab)
            row += 1
            # print("{:.2f}".format(result_value) + " =\t[" + result_str + "]") 
            # print(result_lab)
            # pass

    print("{} results found!".format(len(results)))
    print("Took {:.2f} milliseconds.".format((t_end-t_start)*1000))
    workbook.close()

if __name__ == "__main__":

    # input
    cwd = os.getcwd()
    file_path = cwd + "/Isotope_Combinator/"
    file_name = "isotopes table BiFeO3-BaTiO3.xlsx"
    target = "209Bi"
    Mass_resolution = 1000

    main(file_path, file_name, target, Mass_resolution)