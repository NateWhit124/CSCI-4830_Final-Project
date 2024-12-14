import csv
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

# initialize lists and DataTree
time_values = []
frequency_values = []
spectrogram_data = []
tree = DataTree[object]()

# read the CSV
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for row_index, row in enumerate(reader):
        if row_index == 0:
            # First row contains time values (skip the first column)
            time_values = [float(value) for value in row]
        else:
            # Remaining rows: first column = frequency, remaining = spectrogram values
            frequency_values.append(float(row[0]))
            spectrogram_data.append([float(value) for value in row[1:]])

# filling the DataTree
for i, row in enumerate(spectrogram_data):
    path = GH_Path(i)  # Create a branch path for each row
    tree.AddRange(row, path)

# outputs
time = time_values
frequencies = frequency_values
data = tree  # DataTree for spectrogram values
