import json
import os
from DashAI.back.core.enums.squema_types import SquemaTypes
from DashAI.back.core.config import settings

dict_squemas = {
    SquemaTypes.model: os.path.join(settings.BACK_PATH, "models/parameters/models_schemas/"),
    SquemaTypes.preprocess: os.path.join(settings.BACK_PATH, "models/parameters/preprocess_schemas"),
    SquemaTypes.dataloader: os.path.join(settings.BACK_PATH, "dataloaders/params_schemas/"),
    SquemaTypes.task: os.path.join(settings.BACK_PATH, "tasks/tasks_schemas/"),
}


class ConfigObject:
    @staticmethod
    def get_squema(type, name):
        try:
            with open(f"{dict_squemas[type]}{name}.json") as f:
                return json.load(f)

        except FileNotFoundError:
            with open(f"{dict_squemas[type]}{name.lower()}.json"):
                return json.load(f)
