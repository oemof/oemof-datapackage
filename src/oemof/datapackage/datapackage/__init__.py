from oemof.network.energy_system import EnergySystem
from oemof.solph import Model

from . import building  # noqa F401
from .convert_from_json import rebuild_dp_from_json
from .convert_to_json import export_dp_to_json
from .reading import deserialize_constraints
from .reading import deserialize_energy_system

EnergySystem.from_datapackage = classmethod(deserialize_energy_system)

Model.add_constraints_from_datapackage = deserialize_constraints
