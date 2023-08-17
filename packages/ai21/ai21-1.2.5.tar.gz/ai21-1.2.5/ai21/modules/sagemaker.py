class SageMaker:
    @classmethod
    def get_model_package_arn(cls, model_name: str, region: str) -> str:
        from ai21.AWS_utils import get_model_package_arn
        return get_model_package_arn(model_name=model_name, region=region)
