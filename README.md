# Isotope_Combinator
 Calculate all posible combinations of an ion from the isotope talbe

## Preparation isotope table
To reduce the calculation time, usually only select the most important isotopes in the sample or the most posibility contamination isotopes.
The isotope table see the file "isotopes table BiFeO3-BaTiO3" and the full isotope see "isotopes table"

## calculate posiable conbinations
    # input
    cwd = os.getcwd()
    file_path = cwd + "/Isotope_Combinator/"
    file_name = "isotopes table BiFeO3-BaTiO3.xlsx"
    target = "209Bi"
    Mass_resolution = 1000

    main(file_path, file_name, target, Mass_resolution)
    
  ## out put file
  - out put file only list the abundance larger than 1e-3 and the maxium number of atoms of the ion is 5
please see the example of the output file: "isotopes table BiFeO3-BaTiO3 ion-209Bi-results-_mass_range 0.2090(amu)"
