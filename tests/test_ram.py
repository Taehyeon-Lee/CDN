import subprocess
import time
import os
import random

if __name__ == '__main__':
    fails = []

    pages = []
    with open("../urls.txt", 'rb') as file:
        rows = file.readlines()
        for i, row in enumerate(rows):
            url = row.decode().strip()
            page = url.rsplit('/', 1)[-1]
            pages.append(page)

    base_url_start = "cdn-http"
    base_url_end = ".5700.network:20030/"
    count = 1
    start = time.time()
    last = time.time()
    while count < 2001:
        page = pages[random.randint(0, 399)]
        replica_num = random.randint(1, 7)
        replica = base_url_start + str(replica_num) + base_url_end
        if page != '-':
            subprocess.run(["wget", "-q", replica + page, "-O", page])
            try:
                if os.path.getsize(page) == 0:
                    fails.append(page)
                    print(f"\n\nFAIL: {i}. {page}\n\n")
                os.remove(page)
            except:
                fails.append(page)
                print(f"\n\nFAIL: {i}. {page} NOT IN SYS\n\n")
        if count % 25 == 0:
            print("\n**************************************")
            print(count)
            temp = time.time()
            print(f"{(temp - last)} seconds for last 25 files")
            print(f"~({(temp - last) / 25} sec/file)")
            last = temp
        count += 1

    end = time.time()
    print("\n**************************************")
    print(f"Total time: {end - start} seconds")
    print(f"printing failures({len(fails)}):")
    for fail in fails:
        print(fail)
    print("**********************************************\n")


"""
RANDOM:

**************************************
25
78.05642032623291 seconds for last 25 files
~(3.1222568130493165 sec/file)

**************************************
50
61.20359802246094 seconds for last 25 files
~(2.4481439208984375 sec/file)

**************************************
75
53.45202136039734 seconds for last 25 files
~(2.1380808544158936 sec/file)

**************************************
100
50.57028794288635 seconds for last 25 files
~(2.022811517715454 sec/file)

**************************************
125
53.77490258216858 seconds for last 25 files
~(2.1509961032867433 sec/file)

**************************************
150
54.160085678100586 seconds for last 25 files
~(2.1664034271240236 sec/file)

**************************************
175
57.59620475769043 seconds for last 25 files
~(2.303848190307617 sec/file)

**************************************
200
37.14690017700195 seconds for last 25 files
~(1.485876007080078 sec/file)

**************************************
225
60.656668186187744 seconds for last 25 files
~(2.42626672744751 sec/file)

**************************************
250
52.088027477264404 seconds for last 25 files
~(2.0835210990905764 sec/file)


AVG = 2.23



LESS RANDOM:

**************************************
25
46.43943214416504 seconds for last 25 files
~(1.8575772857666015 sec/file)

**************************************
50
35.23541045188904 seconds for last 25 files
~(1.4094164180755615 sec/file)

**************************************
75
46.87260103225708 seconds for last 25 files
~(1.874904041290283 sec/file)

**************************************
100
48.43730187416077 seconds for last 25 files
~(1.9374920749664306 sec/file)

**************************************
125
40.20979595184326 seconds for last 25 files
~(1.6083918380737305 sec/file)

**************************************
150
45.39940023422241 seconds for last 25 files
~(1.8159760093688966 sec/file)

**************************************
175
41.69219756126404 seconds for last 25 files
~(1.6676879024505615 sec/file)

**************************************
200
54.511924028396606 seconds for last 25 files
~(2.1804769611358643 sec/file)

**************************************
225
48.8688428401947 seconds for last 25 files
~(1.9547537136077882 sec/file)


AVG = 1.81
"""





"""
NO COMPRESSION RANDOM:

**************************************
25
82.98581957817078 seconds for last 25 files
~(3.319432783126831 sec/file)


**************************************
50
103.26477289199829 seconds for last 25 files
~(4.130590915679932 sec/file)

**************************************
75
101.36564493179321 seconds for last 25 files
~(4.054625797271728 sec/file)

**************************************
100
122.94043350219727 seconds for last 25 files
~(4.91761734008789 sec/file)

**************************************
125
91.64669752120972 seconds for last 25 files
~(3.6658679008483888 sec/file)

**************************************
150
111.37620329856873 seconds for last 25 files
~(4.455048131942749 sec/file)

**************************************
175
102.07035398483276 seconds for last 25 files
~(4.082814159393311 sec/file)

**************************************
200
84.81842279434204 seconds for last 25 files
~(3.3927369117736816 sec/file)


AVG = 4.0


NO COMPRESSION LESS RANDOM

**************************************
25
47.263519048690796 seconds for last 25 files
~(1.8905407619476318 sec/file)

**************************************
50
68.14766311645508 seconds for last 25 files
~(2.7259065246582033 sec/file)

**************************************
75
55.3001184463501 seconds for last 25 files
~(2.212004737854004 sec/file)

**************************************
100
60.46967577934265 seconds for last 25 files
~(2.418787031173706 sec/file)

**************************************
125
51.83545732498169 seconds for last 25 files
~(2.0734182929992677 sec/file)

**************************************
150
37.554407358169556 seconds for last 25 files
~(1.5021762943267822 sec/file)

**************************************
175
51.321662187576294 seconds for last 25 files
~(2.0528664875030516 sec/file)

**************************************
200
42.39850330352783 seconds for last 25 files
~(1.6959401321411134 sec/file)


AVG = 2.07

"""






# AFTER UPDATES:
'''
RANDOM:

**************************************
25
30.21543025970459 seconds for last 25 files
~(1.2086172103881836 sec/file)

**************************************
50
22.45127820968628 seconds for last 25 files
~(0.8980511283874512 sec/file)

**************************************
75
20.959775924682617 seconds for last 25 files
~(0.8383910369873047 sec/file)

**************************************
100
37.930936098098755 seconds for last 25 files
~(1.5172374439239502 sec/file)

**************************************
125
19.207432985305786 seconds for last 25 files
~(0.7682973194122314 sec/file)

**************************************
150
26.33085823059082 seconds for last 25 files
~(1.0532343292236328 sec/file)

**************************************
175
84.59929156303406 seconds for last 25 files
~(3.3839716625213625 sec/file)

**************************************
200
50.840742111206055 seconds for last 25 files
~(2.033629684448242 sec/file)

**************************************
225
27.80455780029297 seconds for last 25 files
~(1.1121823120117187 sec/file)

**************************************
250
117.13732266426086 seconds for last 25 files
~(4.685492906570435 sec/file)


AVG = 1.75


LESS RANDOM
 AVG = 2.64


'''