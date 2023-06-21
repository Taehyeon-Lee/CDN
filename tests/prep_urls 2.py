import gzip
import subprocess
import os


def set_up_cache():
    base_url = "http://cs5700cdnorigin.ccs.neu.edu:8080/"
    output_path = "."
    with open("./pageviews.csv", 'rb') as file:
        rows = file.readlines()
        for i, row in enumerate(rows):
            if i > 0 and i < 401:
                # get page title and fix spacing
                page = row.split(b',', 2)[2].split(b'\r\n')[0].decode()
                if " " in page:
                    page = page.replace(" ", "_")
                # wget the file, zip it, and store in server file system
                subprocess.run(["wget -q ", base_url + page, "-P", output_path, "-O", page])
                if os.path.getsize(page) > 0:
                    non_comp_len = os.path.getsize(page)
                    with open("../urls.txt", 'a') as f:
                        f.write(base_url + page + "|" + str(non_comp_len) + "|" + "" + "\n")
                else:
                    with open("../urls.txt", 'a') as f:
                        f.write("BROKEN: " + base_url + page +"\n")
                os.remove(page)
            else:
                break


if __name__ == '__main__':
    set_up_cache()
