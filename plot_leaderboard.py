import argparse
import json
import sys
import csv
from datetime import datetime, timezone


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


# Usage: plot_leaderboard.py [-h] leaderboard_file
# Example: python plot_leaderboard.py leaderboard.json
#
# Given a leaderboard json, prints out out a leaderboard point series in csv
# for your plotting convenience.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("leaderboard_file", help="leaderboard json file")
    args = parser.parse_args()

    with open(args.leaderboard_file) as f:
        data = json.load(f)

    member_count = len(data["members"])
    completion_dict = {}
    for i in range(1, 26):
        for j in range(1, 3):
            completion_dict[(str(i), str(j))] = []

    # list of (username, local_score)
    members = []
    for member in data["members"].values():
        username = member["name"]
        members.append((username, member["local_score"]))
        for day, day_body in member["completion_day_level"].items():
            for part, part_body in day_body.items():
                completion_dict[(day, part)].append(
                    (username, part_body["get_star_ts"])
                )
    # sort members by local_score desc
    members.sort(key=lambda x: x[1], reverse=True)

    # sort all tuple lists in completion_dict by the timestamp
    for key in completion_dict:
        completion_dict[key].sort(key=lambda x: x[1])
    # pprint.pprint(completion_dict)

    # list of (username, timestamp, points)
    # iterate in completion_dict order to assign points correctly, then sort by time overall
    all_completions = []
    for day_part_completions in completion_dict.values():
        for i, completion in enumerate(day_part_completions):
            all_completions.append((completion[1], completion[0], member_count - i))
    all_completions.sort(key=lambda x: x[0])

    # pprint.pprint(all_completions)

    # build this up into a csv of points people got over time
    # first column is timestamp, then each column is a username
    # each row is populated by the cummulitive sum of points up to that timestamp
    # for each username

    fieldnames = ["timestamp"]
    points = {}
    for username, _ in members:
        fieldnames.append(username)
        points[username] = 0

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    for completion in all_completions:
        points[completion[1]] += completion[2]
        ts = utc_to_local(datetime.utcfromtimestamp(int(completion[0])))
        row = {"timestamp": ts.strftime("%Y-%m-%d %H:%M:%S")}
        for username, _ in members:
            row[username] = points[username]
        writer.writerow(row)


if __name__ == "__main__":
    main()
