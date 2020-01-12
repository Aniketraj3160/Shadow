
import csv


def indiaCsv():

    with open('data.csv', 'w', newline='') as csv_file:
        # print("HELLOOOOO")
        writer = csv.writer(csv_file)
        writer.writerow(['abcd', 'iop'])
        # print("HIIIIIIIII")

    # with open(name, 'w') as csv_file:
    #     fieldnames = ['state', 'crimereported']
    #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    #     print("sexsexsex")
    #     writer.writeheader()
    #     for x in data:
    #         print(x.state)
    #         # print("Hello")
    #         writer.writerow(
    #             {'state': x.state, 'crimereported': x.crimereported})


indiaCsv()
