import pandas as pd
from mineCube.core.helpers.date import get_time_component
from mineCube.core.helpers.follow_counter import follow_count
from mineCube.core.helpers.dependency_graph import dependency_graph
from mineCube.core.helpers.algo.HM import HM
from mineCube.core.config import process_cube_extension

class MiniCube:
    def __init__(self,dimensions,date_column, activity_column, case_id_column,time_freq='Y',csms=None,cslms=None,models=None,groups_activities=None,cube=None,data=None,loaded=False):
        self.data = data if data is not None else pd.DataFrame()
        self.dimensions = dimensions
        self.date_column = date_column
        self.activity_column = activity_column
        self.case_id_column = case_id_column
        self.time_freq = time_freq  # Default to daily grouping if not provided
        self.time_grouper = None
        self.csms = csms if csms is not None else {}  # Initialize with an empty dictionary if not provided
        self.cslms = cslms if cslms is not None else {}  # Initialize with an empty dictionary if not provided
        self.models = models if models is not None else {}  # Initialize with an empty dictionary if not provided
        self.groups_activities = groups_activities if groups_activities is not None else {}  # Initialize with an empty dictionary if not provided
        self.cube = cube
        if not self.data.empty and not loaded:
            self.group_data()

    def set_data(self,data):
        self.data = data
        self.group_data()
        return self.data


    def get_unique_activities(self):
        return self.cube[self.activity_column].unique()

    def group_data(self):
        # Convert date_column to datetime if it's not already
        if not pd.api.types.is_datetime64_any_dtype(self.data[self.date_column]):
            self.data[self.date_column] = pd.to_datetime(self.data[self.date_column])

        # Create a dictionary to store the groups
        groups = {}

        # Iterate through the data rows and group them based on dimensions and time frequency
        for index, row in self.data.iterrows():
            dimensions_key = tuple(row[dim] for dim in self.dimensions)
            time_component = get_time_component(self.time_freq, row[self.date_column])
            group_key = dimensions_key + (time_component,)

            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(index)

        # Create a new column called 'group' in the original DataFrame
        self.cube = self.data
        self.cube['group'] = ''
        for group_key, indices in groups.items():
            group_name = ', '.join(str(key) for key in group_key)
            self.cube.loc[indices, 'group'] = group_name

    def regroup_data(self, dimensions, time_freq=None):
        if time_freq:
            self.time_freq = time_freq
        self.models = {}
        self.cslms = {}
        self.csms = {}
        self.groups_activities = {}
        self.dimensions = dimensions
        self.group_data()

    def calculate_matrices(self):
        # Calculate the Cube Succession Matrix (CSM) based on the grouped data
        # first group data by group index
        # activities = self.get_unique_activities()
        self.cube = self.cube.sort_values(by=self.date_column, ascending=True)
        grouped_data = self.cube.groupby('group')
        for group, transactions in grouped_data:
            activities = transactions[self.activity_column].unique().tolist()
            traces = transactions.groupby(self.case_id_column)
            temp = []
            for g, t in traces:
                temp.append(t[self.activity_column].values)
            direct_follow, double_follow = follow_count(temp, activities)
            self.csms[group] = direct_follow
            self.cslms[group] = double_follow
            self.groups_activities[group] = activities
        return self.csms, self.cslms

    def get_cube(self):
        return self.cube

    def get_cell(self, group=None):
        try:
            if group:
                if len(group) - 1 == len(self.dimensions):
                    searchKey = ', '.join(str(key) for key in group)
                    print(searchKey)
                    return self.cube[self.cube['group'] == searchKey]
                else:
                    raise ValueError(
                        "The group tuple should contain the same elements given in dimensions , in addition to a date!")
            else:
                raise ValueError("Cannot get a cell without a group tuple!")
        except KeyError:
            return None

    def mine(self,algo="HM",**kwargs):
        if algo=="HM":
            # use the heuristic miner algorithm
            # 1- create a dep graph from the calculated csm and cslm
            for key,activities in self.groups_activities.items():
                short_loops,dep_graph,and_xor_observations = dependency_graph(activities,self.csms[key],self.cslms[key])
                # print(dep_graph)
                self.models[key] = HM(activities,self.csms[key],short_loops,dep_graph,and_xor_observations,**kwargs)