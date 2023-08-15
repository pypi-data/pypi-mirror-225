from api_compose.services.composition_service.models.actions.actions import JsonHttpActionModel
from api_compose.services.composition_service.models.actions.configs import JsonHttpActionConfigModel


class DefaultActionModel:

    BASE_ACTION_MODEL = JsonHttpActionModel(
        id="dummy_action_id",
        description="dummy action",
        config=JsonHttpActionConfigModel(),
    )
