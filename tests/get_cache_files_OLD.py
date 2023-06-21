import gzip

import pandas as pd
import subprocess
import os

FILENAME = "pageviews.csv"

'''
    9, 42, 64, 73 omitted in the csv file so downloaded until 104
'''
def read_file():
    ranking = pd.read_csv(FILENAME)
    pages = []
    for i in range(200):
        path = ranking['article'][i]
        if " " in path:
            path = path.replace(" ", "_")
        pages.append(path)
    print(pages)
    print(len(pages))

    return pages

'''
    seems like it omits '-' file so need to manually added
'''
def download_cache(pages):
    fails = []
    base_url = "http://cs5700cdnorigin.ccs.neu.edu:8080/"
    output_path = "../cache_files"

    for page in pages:
        try:
            subprocess.run(["wget", base_url+page, "-P", output_path, "-O", page])
        except:
            fails.append(page)
            print("Fail to download the file: " + page)
            break

    print(fails)

def zip_files():
    directory = "../cache_files"
    counter = 0

    # change directory to cache_files
    os.chdir(directory)

    # Iterate over the files in the directory and zip them
    for filename in os.listdir("."):
        counter += 1
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(filename):
            # if file name is - then zip the file in the current file of -
            if filename == '-':
                subprocess.run(["gzip", './'+filename])
            print(f"{counter} Compressing file:", filename)
            subprocess.run(["gzip", filename])


def set_up_cache():
    fails = []
    base_url = "http://cs5700cdnorigin.ccs.neu.edu:8080/"
    output_path = "."
    with open("./pageviews.csv", 'rb', encoding='utf-8') as file:
        rows = file.readlines()
        for i, row in enumerate(rows):
            if (i < 10):
                # get page title and fix spacing
                page = row.strip().split(',')[2]
                if " " in page:
                    page = page.replace(" ", "_")
                # wget the file, zip it, and store in server file system
                try:
                    subprocess.run(["wget", base_url + page, "-P", output_path, "-O", page])
                    with open(page, 'rb') as f_in:
                        with gzip.open(page + '.gz', 'wb') as f_out:
                            f_out.writelines(f_in)

                    os.remove(page)
                    os.rename(page + '.gz', page)
                except:
                    fails.append(page)
            else:
                break

    print("\n\nFAILS:\n")
    for fail in fails:
        print(fail)



if __name__ == '__main__':
    # pages = read_file()
    # download_cache(pages)
    # zip_files()
    # set_up_cache()

    with open("./pageviews.csv", 'rb') as file:
        rows = file.readlines()
        for i, row in enumerate(rows):
            if i < 400:
                # get page title and fix spacing
                page = row.split(b',', 2)[2].split(b'\r\n')[0].decode()
                print(page)
