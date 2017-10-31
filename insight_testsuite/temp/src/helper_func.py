import csv

def calculate_median(num_list):

    sorted_list = sorted(num_list)

    n = len(num_list)
    if n < 1:
            return None
    if n % 2 == 1:
            return int(round(sorted_list[n//2]))
    else:
            return int(round(sum(sorted_list[n//2-1:n//2+1])/2.0))


def write_output(data,output_file_name):
       with open(output_file_name,"w") as f:
        wr = csv.writer(f,delimiter='|')
        wr.writerows(data)