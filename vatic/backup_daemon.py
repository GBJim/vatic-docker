import daemon
import time
from subprocess import check_output, call
import datetime
import pytz


def backup():


    cmd = ["turkic", "list"]
    video_ids = check_output(cmd).strip().split("\n")
    for video_id in video_ids:
        timezone= pytz.timezone('Asia/Hong_Kong')
        current_time = datetime.datetime.now(timezone).strftime("%H:%M-%m%d_%Y")
        file_name = "{}_{}.txt".format(video_id, current_time)
        cmd = ["turkic", "dump", video_id, "-o", "/root/vatic/data/backup/{}".format(file_name)]
        merge_cmd = ["--merge", "--merge-threshold", "0.5"]
        cmd += merge_cmd
        print(" ".join(cmd))
        call(cmd)




def run(sleep_duration=7200):
    while True:
        backup()
        time.sleep(sleep_duration)


if __name__ == "__main__":
    run()
