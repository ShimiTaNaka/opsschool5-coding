import json
import sys

LAST_INDEX = -1
NEXT_AGE_BORDER = 1
AGE = 1
NAME = 0
HW_JSON = 'hw.json'


def yaml_my_json_group_sorted():
    try:
        with open(HW_JSON, "r", encoding='utf-8') as import_file:
            data = json.load(import_file)
    except FileNotFoundError:
        print(f"{HW_JSON} file does'nt exists")
        exit(404)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        exit(100)

    ages_borders = data['buckets']
    people_list = sorted(data["ppl_ages"].items(), key=lambda kv: kv[AGE])
    extra_age = [0, people_list[LAST_INDEX][AGE] + 1]
    ages_borders.extend(extra_age)
    sorted_ages_broders = sorted(ages_borders)

    current_people_list = people_list
    for age_border in range(len(sorted_ages_broders) - 1):
        print(sorted_ages_broders[age_border], "-", sorted_ages_broders[age_border + NEXT_AGE_BORDER], ":", sep="")
        for person in current_people_list:
            if sorted_ages_broders[age_border] <= person[AGE] < sorted_ages_broders[age_border + NEXT_AGE_BORDER]:
                print("  -", person[NAME])
            else:
                current_people_list = people_list[people_list.index(person):]
                break


if __name__ == '__main__':
    yaml_my_json_group_sorted()
