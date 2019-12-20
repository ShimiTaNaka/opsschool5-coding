import json
import yaml


def read_json(json_file_path):
    data = None
    try:
        with open(json_file_path) as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("File " + json_file_path + " does not exist")
    return data


def combine_people_by_ages(buckets_list, ppl_ages_list):
    min_age = 0
    max_age = ppl_ages_list[-1][1]  # the value of the last element in the sorted list
    buckets_list.insert(len(buckets_list), max_age)  # add to bucket of ages the maximum age
    result = []
    for num in buckets_list:
        names = []
        for name, age in ppl_ages_list:
            if age in range(min_age, num):
                names.append(name)  # add names of people with age in range
        result.append({str(min_age) + "-" + str(num): names})  # combine age ranges with names in list of dicts
        min_age = num
    return result


def write_yaml(yaml_file_path, data_list):
    with open(yaml_file_path, "w") as yaml_file:
        f = yaml.dump(data_list, yaml_file, explicit_start=True, allow_unicode=True)


def main():
    json_file_path = "hw.json"
    yaml_file_path = "result.yaml"
    json_data = read_json(json_file_path)
    if json_data:
        buckets = sorted(json_data["buckets"])  # sort buckets
        ppl_ages = sorted(json_data["ppl_ages"].items(), key=lambda x: x[1])  # sort peoples by age
        ppl_ages_ranges_list = combine_people_by_ages(buckets, ppl_ages)
        print(yaml.dump(ppl_ages_ranges_list, allow_unicode=True))   #print yaml
        write_yaml(yaml_file_path, ppl_ages_ranges_list)  # create result yaml file


if __name__ == '__main__':
    main()
