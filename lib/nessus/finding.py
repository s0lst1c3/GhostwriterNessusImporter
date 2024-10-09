from copy import deepcopy
from lib.ghostwriter import GhostwriterFinding
from lib.types.namespace import Namespace

DICT_FILTER = [
    "title",
    "cvss_score",
    "cvss_vector",
    "description",
    "mitigation",
    "affected_entities",
    "replication_steps",
]
import json
from lib.utils.json import default_encoder


class NessusFinding(Namespace):

    @classmethod
    def from_dict(cls, my_dict):
        my_dict = deepcopy(my_dict)
        my_dict["cvss_score"] = float(my_dict["cvss_score"])
        affected_entities = my_dict.pop("affected_entities")
        entities = sorted([k for k in affected_entities.keys()])
        replication_steps = []
        for entity in entities:
            replication_steps.append(
                "\n\n".join(
                    [
                        entity,
                        affected_entities[entity],
                    ]
                )
            )
        my_dict.update(
            {
                "affected_entities": "\n".join(entities),
                "replication_steps": "\n\n".join(replication_steps) + "\n\n",
            }
        )
        return cls.from_json(json.dumps(my_dict, default=default_encoder))

    def to_ghostwriter_finding(self):
        my_dict = self.to_dict()
        my_dict = deepcopy(my_dict)
        keys = set(my_dict.keys())
        for k in keys:
            if k not in DICT_FILTER:
                del my_dict[k]

        return GhostwriterFinding(**my_dict)
