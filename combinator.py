import math
import time

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

def main():
    inputs = [18.01, 42.01, 132.04, 162.05, 203.08, 176.03]
    target = 1800.71

    tolerance = 0.001

    t_start = time.perf_counter()
    results = list(combinator(tolerance, target, inputs))
    t_end = time.perf_counter()

    for result in results:
        result_str = ""
        result_value = 0
        for factor, value in zip(result, inputs):
            if not factor:
                continue
            if result_str != "":
                result_str += " + "
            result_str += "{}* {}".format(factor, value)
            result_value += factor*value
        print("{:.2f}".format(result_value) + " =\t[" + result_str + "]") 

    print("{} results found!".format(len(results)))
    print("Took {:.2f} milliseconds.".format((t_end-t_start)*1000))

if __name__ == "__main__":
    main()