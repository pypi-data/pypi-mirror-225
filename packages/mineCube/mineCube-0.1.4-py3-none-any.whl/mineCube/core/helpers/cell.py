from mineCube.core.helpers.algo.HM import HM
from mineCube.core.helpers.dependency_graph import dependency_graph
class Cell:
    def __init__(self,data,dimensions,date_freq,models={},csms={},cslms={},groups_activities={}):
        self.data = data
        self.dimensions = dimensions
        self.date_freq = date_freq
        self.models = models
        self.csms = csms
        self.cslms = cslms
        self.groups_activities = groups_activities

    def mine(self, algo="HM", **kwargs):
        if algo == "HM":
            # use the heuristic miner algorithm
            # 1- create a dep graph from the calculated csm and cslm
            for key, activities in self.groups_activities.items():
                short_loops, dep_graph, and_xor_observations = dependency_graph(activities, self.csms[key],self.cslms[key])
                # print(dep_graph)
                self.models[key] = HM(activities, self.csms[key], short_loops, dep_graph, and_xor_observations,**kwargs)