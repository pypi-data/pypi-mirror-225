import sys

def clear_output_cells_line_by_line(notebook_path, output_notebook_path):
    with open(notebook_path, 'r') as input_f, open(output_notebook_path, 'w') as output_f:
        in_outputs = False

        for line in input_f:
            if in_outputs and line.startswith('   "source": ['):
                in_outputs = False
                output_f.write('"outputs": [],\n')
                output_f.write(line)
            elif in_outputs:
                continue
            elif line.startswith('   "outputs": ['):
                in_outputs = True
            else:
                output_f.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: nb_output_stripper [input] [output]")
    else:
        input_notebook_path = sys.argv[1]
        output_notebook_path = sys.argv[2]

        clear_output_cells_line_by_line(input_notebook_path, output_notebook_path)

        print(f'Notebook output cells were emptied and the result was saved in "{output_notebook_path}"')
