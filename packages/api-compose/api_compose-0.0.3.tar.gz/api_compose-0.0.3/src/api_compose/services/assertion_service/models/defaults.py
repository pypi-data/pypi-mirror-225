from api_compose.services.assertion_service.models.configs import JinjaAssertionConfigModel


class DefaultAssertionConfigModel:

    DefaultJinjaAssertionConfigModel = JinjaAssertionConfigModel.construct(
        template='',
        template_file_path='',
    )

