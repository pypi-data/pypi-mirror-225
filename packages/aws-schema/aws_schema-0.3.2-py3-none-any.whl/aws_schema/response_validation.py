import logging
from ._validation_base_class import DataValidator

logger = logging.getLogger("API Response Check")

__all__ = ["ResponseDataValidator"]


class ResponseDataValidator(DataValidator):
    def __init__(
        self,
        response_data: dict,
        httpMethod: str,
        api_name: str,
        file: str = None,
        url: str = None,
        raw: dict = None,
        return_error_in_response: bool = False,
    ):
        self.__httpMethod = httpMethod
        self.__api_name = api_name
        try:
            super().__init__(response_data, file, url, raw)
            self.verify(return_error_in_response)
        except NotImplementedError:
            exception_text = f"no specified response schema available for statusCode {self.statusCode}\n" \
                             f"response: {response_data}"
            if return_error_in_response:
                raise NotImplementedError(
                    {
                        "statusCode": 501,
                        "body": exception_text,
                        "headers": {"Content-Type": "text/plain"},
                    }
                )
            else:
                logger.warning(exception_text)

    @property
    def httpMethod(self) -> str:
        return self.__httpMethod

    @property
    def api_name(self) -> str:
        return self.__api_name

    @property
    def statusCode(self) -> str:
        return str(self.data["statusCode"])

    def insert_specifics_to_origin(self, origin: str) -> str:
        if self.httpMethod not in origin:
            if ".json" == origin[-5:]:
                origin = origin[:-5]

            origin += "-" + self.httpMethod + "-" + self.statusCode + ".json"

        elif self.statusCode not in origin:
            if ".json" == origin[-5:]:
                origin = origin[:-5]

            origin += "-" + self.statusCode + ".json"

        return origin

    @staticmethod
    def handle_exception(validation_error, return_error_in_response):
        if return_error_in_response:
            raise TypeError(
                {
                    "statusCode": 500,
                    "body": {
                        "invalid response": validation_error.instance,
                        "schema context": validation_error.context.__str__(),
                    },
                }
            )
        else:
            logger.warning(f"invalid response:\n\n{validation_error.instance}")
