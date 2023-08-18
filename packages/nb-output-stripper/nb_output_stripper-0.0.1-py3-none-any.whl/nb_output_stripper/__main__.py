import sys
from nb_output_stripper import clear_output_cells_line_by_line

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: nb_output_stripper [input] [output]")
    else:
        input_notebook_path = sys.argv[1]
        output_notebook_path = sys.argv[2]

        clear_output_cells_line_by_line(input_notebook_path, output_notebook_path)

        print(f'Notebook output cells were emptied and the result was saved in "{output_notebook_path}"')
