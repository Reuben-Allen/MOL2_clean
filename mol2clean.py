"""
This script prepares .mol2 files containing ligand information for docking
with the DockingPie plugin for PyMol. 

Current Features:
-allows the user to name their molecule
-sorts and numbers atoms

Note: Currently only set up to detect atoms with one letter atomic symbols
"""

import sys

def id_map(num_list,mapping_dict): 
    result = [mapping_dict["output"][mapping_dict["input"].index(num)] for num in num_list]
    return result

def mol2_clean(input_file, output_file):
    # read text from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()
        f.close()

    # verify that the file starts with the molecule parameters
    if not lines[0].strip().startswith('@<TRIPOS>MOLECULE'):
        sys.exit("Nonstandard header found: {}. Please delete header lines until the TRIPOS molecule definition.".format(lines[0]))

    with open(output_file, 'w') as out_file:
        # write the MOLECULE section header line to the output
        out_file.write(lines[0])

        # check title
        title = lines[1]
        while True:
            print("The current molecule title is: " + title)
            modify = input("Do you wish to change the title? (y/n)")
            if modify == "y":
                title = input("Enter new title:") + "\n"
                break
            elif modify == "n":
                break
            else:
                print("Invalid character entered. Please try again")
                continue
        out_file.write(title)
        print("The molecule title is set as: " + title)

        # print the number of atoms and bonds
        natom, nbond = map(int, lines[2].split()[:2])
        print("Found {} atoms in the molecule, with {} bonds.".format(natom, nbond))
        
        # write everything until the ATOM section
        i = 2
        while 'ATOM' not in lines[i]:
            out_file.write(lines[i])
            i += 1
        out_file.write(lines[i]) # Print the ATOM section header line to the output
        i += 1

        # organize atom section
        atom_dict = {}
        mapping_dict = {"input":[],"output":[]}
        atom_section = lines[i:i+natom]
        for line in atom_section:
            values = line.split()
            atom_type = values[5][0]
            if atom_type in atom_dict:
                atom_dict[atom_type].append(values)
            else:
                atom_dict[atom_type] = [values]
        atom_section_sorted = []
        k = 1
        for type in atom_dict.keys():
            j = 1
            for atom in atom_dict[type]:
                mapping_dict["input"].append(atom[0])
                atom[0] = k
                mapping_dict["output"].append(atom[0])
                atom[1] = type + str(j)
                atom_section_sorted.append(atom)
                k += 1
                j += 1
        max_1_width = 0
        max_2_width = 0
        max_3_width = 0
        max_4_width = 0
        max_5_width = 0
        max_6_width = 0
        max_7_width = 0
        max_8_width = 0
        max_9_width = 0
        for line in atom_section_sorted: # get widths of each column
            max_1_width = max(max_1_width, len(str(line[0])))
            max_2_width = max(max_2_width, len(line[1]))
            max_3_width = max(max_3_width, len(line[2]))
            max_4_width = max(max_4_width, len(line[3]))
            max_5_width = max(max_5_width, len(line[4]))
            max_6_width = max(max_6_width, len(line[5]))
            max_7_width = max(max_7_width, len(line[6]))
            max_8_width = max(max_8_width, len(line[7]))
            max_9_width = max(max_9_width, len(line[8]))
        for line in atom_section_sorted: # output sorted section
            out_file.write("{1:<{0}}  {3: <{2}}  {5: <{4}} {7: <{6}} {9:<{8}} {11:<{10}} {13:<{12}} {15:<{14}} {17: <{16}}".format(
                                            max_1_width, line[0],
                                            max_2_width, line[1],
                                            max_3_width, float(line[2]),
                                            max_4_width, float(line[3]),
                                            max_5_width, float(line[4]),
                                            max_6_width, line[5],
                                            max_7_width, line[6],
                                            max_8_width, line[7],
                                            max_9_width, float(line[8]),
                                            ) + "\n")
        out_file.write("\n") # skip a line

        # skip everything until the BOND section
        while 'BOND' not in lines[i]:
            i += 1
        out_file.write(lines[i]) # Print the BOND section header line to the output
        i += 1

        # reindex the BOND section
        bonds_section_sorted = []
        bonds_section = lines[i:i+nbond]
        for line in bonds_section:
            values = line.split()
            values[1:3] = id_map(values[1:3],mapping_dict)
            bonds_section_sorted.append(values)
        max_b1_width = 0
        max_b2_width = 0
        max_b3_width = 0
        max_b4_width = 0
        for line in bonds_section_sorted: # get widths of each column
            max_b1_width = max(max_b1_width, len(str(line[0])))
            max_b2_width = max(max_b2_width, len(str(line[1])))
            max_b3_width = max(max_b3_width, len(str(line[2])))
            max_b4_width = max(max_b4_width, len(str(line[3])))

        for line in bonds_section_sorted: # output sorted section
            out_file.write("{1:<{0}}  {3: <{2}}  {5: <{4}} {7: <{6}}".format(
                                            max_b1_width, line[0],
                                            max_b2_width, line[1],
                                            max_b3_width, line[2],
                                            max_b4_width, line[3]) + "\n")
        
        try:
            out_file.writelines(lines[i+nbond:]) # Print rest of the input file to the output
        except:
            pass
        out_file.close()
        print("Finished")
    return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python {} input.mol2 output.mol2".format(sys.argv[0]))

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    mol2_clean(input_file, output_file)