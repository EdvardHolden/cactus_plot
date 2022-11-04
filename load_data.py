from typing import List, Dict
import json
import numpy as np


class Program:
    def __init__(self, program_name: str, program_alias: str, positive_instance_stats: Dict[str, float]):
        self.name = program_name
        self.alias = program_alias
        self.stats = positive_instance_stats

    def get_name(self) -> str:
        return self.name

    def get_alias(self) -> str:
        return self.alias

    def get_max_val(self) -> float:
        return max(self.get_values())

    def get_min_val(self) -> float:
        return min(self.get_values())

    def get_average_val(self) -> float:
        return np.average(self.get_values())

    def get_values(self) -> List[float]:
        return list(self.stats.values())

    def __len__(self):
        return len(self.stats)

    def __str__(self):
        return f"program_{self.get_name()}_solved_{self.__len__()}"


def load_json_data_from_file(file_path, stat_type, max_val, min_val) -> Program:
    with open(file_path, "rb") as f:
        data = json.load(f)

    # Get name attributes
    name = data["preamble"]["program"]
    alias = data["preamble"]["prog_alias"]

    solved_stat = {}
    for name, entry in data["stats"].items():
        if entry["status"]:
            # Get the value and check the requirements
            value = entry[stat_type]
            if min_val <= value <= max_val:
                solved_stat[name] = value

    return Program(name, alias, solved_stat)


def load_data(file_paths, args) -> List[Program]:

    # Compute the min value
    if args["plot_type"] == "scatter" and args["x_min"]:
        min_val = max(args["x_min"], args["y_min"])
    else:
        min_val = args["y_min"]  # options['y_min'] is always defined

    # Load the data into a list of program objects
    data = []
    if args["data_type"] == "json":
        for file_path in file_paths:
            print(f"Loading: {file_path}")
            file_data = load_json_data_from_file(file_path, args["stat_type"], args["timeout"], min_val)
            data += [file_data]
    else:
        raise ValueError(f"Unknown data type \"{args['data_type']}\"")

    # Return Program attempt objects as a dict
    return data


if __name__ == "__main__":
    # Testing function
    d = load_json_data_from_file("examples/solver2.json", "rtime", 500, 0)
    print(d)
    print(type(d))
