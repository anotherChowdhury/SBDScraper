from scraper.bs_scraper import scrap_data
import time
from datetime import timedelta


def main():
    # rate = int(input(" What's the current rate of dollar ? "))
    # shipping_time = input(" What's the current expected delivery ? ")
    i = 0
    links = open("links.txt", "r")
    for line in links:
        i = i+1
        scrap_data(line,i)


if __name__ == "__main__":


    start_time = time.monotonic()

    main()




    end_time = time.monotonic()
    print(timedelta(seconds=end_time - start_time))

