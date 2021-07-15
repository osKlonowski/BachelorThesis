import csv

csv_file_path = 'results.csv'


def write_header():
    header = ['avg_fitness', 'fitness_1', 'fitness_2', 'fitness_3',
              'time', 'num_iter', 'num_ants', 'alpha', 'beta', 'Q', 'rho', 'tau0', 'q0', 'phi']
    with open(csv_file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(header)


def write_result(data):
    with open(csv_file_path, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
