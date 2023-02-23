import os
import json
import glob
import time
keys=set()

#Code to remove duplicates and combine all the jsonl files together
def combine_jsonl_files(files, out_file, id_field):
    data = {}
    cnt=0
    for file in files:
        start_time=time.time()
        print("start for ",file, start_time)
        with open(file, 'r') as f:
            for line in f:
                item = json.loads(line)
                tmp=item['data'][id_field]
                if "referenced_tweets" in item['data'].keys():
                    cnt+=1
                elif not keys.__contains__(tmp):
                    keys.add(tmp)
                    data[item['data'][id_field]] = item
                else:
                    cnt=cnt+1
        print("file ", file, "done")
        end_time=time.time()
        print("time taken", end_time-start_time)

    print("total dups ", cnt)
    with open(out_file, 'w') as f:
        for item in data.values():
            f.write(json.dumps(item) +'\n')

#Using the files that have to be combined
files = ["./data/tweets-20230207-00","./data/tweets-20230207-01","./data/tweets-20230207-02","./data/tweets-20230207-03","./data/tweets-20230207-04","./data/tweets-20230207-05","./data/tweets-20230207-06","./data/tweets-20230207-07","./data/tweets-20230207-08","./data/tweets-20230207-09","./data/tweets-20230207-10","./data/tweets-20230207-12","./data/tweets-20230207-13"]
combine_jsonl_files(files, './data_combined.jsonl', 'id')