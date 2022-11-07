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

    def get_instance_names(self) -> List[str]:
        return list(self.stats.keys())

    def get_instances(self) -> Dict[str, float]:
        return self.stats

    def __len__(self):
        return len(self.stats)

    def __str__(self):
        return f"program_{self.get_name()}_alias_{self.get_alias()}_solved_{self.__len__()}"


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


def load_experiment_data_from_db(exp_id, alias, max_val, min_val, ltb):
    from database import DB  # Importing here as it requires mysql that might  not be installed
    db = DB(ltb_problems=ltb)
    res = db.get_solved_problem_name_time(exp_id, upper_time_bound=max_val)

    # Filter on lower time bound
    res = list(filter(lambda x: x[1] >= min_val, res))

    # Convert to dict
    res = {k: v for k, v in res}

    return Program(exp_id, alias, res)


def load_data(data_paths, args) -> List[Program]:

    # Compute the min value
    if args["plot_type"] == "scatter" and args["x_min"]:
        min_val = max(args["x_min"], args["y_min"])
    else:
        min_val = args["y_min"]  # options['y_min'] is always defined

    # Load the data into a list of program objects
    data = []
    if args["data_type"] == "json":
        for data_path in data_paths:
            print(f"Loading: {data_path}")
            file_data = load_json_data_from_file(data_path, args["stat_type"], args["timeout"], min_val)
            data += [file_data]

    elif args["data_type"] == "db":
        if args["stat_type"] != "rtime":
            raise ValueError("DB data only supports rtime field for now..")
        try:
            exp_data = json.loads(data_paths[0])
        except (TypeError, json.JSONDecodeError):
            raise TypeError(
                'Issue converting db data spec to json. The format is \'{"id1": "alias1", "id2": "alias2"}\''
            )
        for exp_id, alias in exp_data.items():
            print("# Loading: ", exp_id, alias)
            exp_data = load_experiment_data_from_db(
                exp_id, alias, args["timeout"], min_val, args["db_data_ltb"]
            )
            data += [exp_data]

    else:
        raise ValueError(f"Unknown data type \"{args['data_type']}\"")

    # Return Program attempt objects as a dict
    return data


def join_data(data: List[Program]) -> List[Program]:
    """
    Takes a list of programs and returns the truncated programs based
    on their intersection of solved instances.
    """
    # Need at least two programs to join
    if len(data) < 2:
        return data

    # Compute the intersection
    inter = set(data[0].get_instance_names())
    for prog in data[1:]:
        inter = inter.intersection(prog.get_instance_names())

    # Truncate entries
    new_data = []
    for prog in data:
        # Join on the correct order
        curr_inst = prog.get_instances()
        new_prog = Program(
            prog.get_name(), prog.get_alias(), {inst_name: curr_inst[inst_name] for inst_name in inter}
        )
        new_data += [new_prog]

    return new_data


def test():
    # Testing function
    print("Test load from json")
    d = load_json_data_from_file("examples/solver2.json", "rtime", 500, 0)
    print(d)
    print("Test load from db")
    d = load_experiment_data_from_db(117213, "test_alias", 200, 0, False)
    print(d)


if __name__ == "__main__":
    test()
