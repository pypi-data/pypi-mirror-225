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
