import requests
import time
import random
import csv

cnpj_list = []
completed_cnpj_list = []
user_agent_list = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
)  # list of user agents to randomly select in request


def main():
    read_list()  # read list.csv to get list of cnpjs to fetch
    read_completed_list()  # read list_complete.csv to filter already fetched cnpjs
    new_cnpj_list = [cnpj for cnpj in cnpj_list if cnpj not in completed_cnpj_list]
    wait_time = 21  # we can only fetch 3 cnpjs per minute, so we wait 21 seconds to prevent 429 server error

    print("Remaining => " + str(len(new_cnpj_list)))
    for cnpj in new_cnpj_list:
        while True:
            print("Starting cnpj => " + cnpj)
            user_agent = random.choice(user_agent_list)
            headers = {'User-Agent': user_agent, "Accept-Language": "en-US, en;q=0.5"}
            response = requests.get("https://www.receitaws.com.br/v1/cnpj/" + cnpj, headers=headers)
            if response.status_code == 429 or response.status_code == "429":
                print("Too many requests, delaying 10 seconds and trying again cnpj => " + cnpj)
                time.sleep(wait_time)
                continue
            else:
                append_cnpj(response.text)
                completed_cnpj_list.append(cnpj)
                write_completed_list()
                print("Done cnpj => " + cnpj)
                print("Remaining => " + str(len(cnpj_list) - len(completed_cnpj_list)))
                time.sleep(wait_time)
                break


def append_cnpj(new_cnpj):
    with open('list_complete_values.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow([new_cnpj.encode('utf8')])  # encode utf8 because of accents


def read_list():
    with open('list.csv') as csv_file:
        read = csv.reader(csv_file, delimiter=",")
        for row in read:
            cnpj_list.append(row[0])


def read_completed_list():
    with open('list_complete.csv') as csv_file:
        read = csv.reader(csv_file, delimiter=",")
        for row in read:
            completed_cnpj_list.append(row[0])


def write_completed_list():
    with open('list_complete.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        for completed_cnpj in completed_cnpj_list:
            writer.writerow([completed_cnpj])


if __name__ == '__main__':
    main()
