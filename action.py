import csv

with open("Парез/points/Норма/20180110_Malkin_1_points.csv", "r") as f:
    reader = csv.DictReader(f)
    for line in reader:
        print(line)
    # with open("new.csv", "w") as f:
    #     header = ["frame_num", ""]