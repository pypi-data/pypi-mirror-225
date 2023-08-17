from ._validation_base_class import DataValidator
from ._parameter_casting import cast_parameter


__all__ = ["APIDataValidator"]


class APIDataValidator(DataValidator):
    def __init__(
        self,
        api_data: dict,
        api_name: str,
        file: str = None,
        url: str = None,
        raw: dict = None,
    ):
        self.__api_name = api_name
        super().__init__(api_data, file, url, raw)

        self.__remove_empty_body()
        if self.httpMethod != "nonHTTP":
            self.__convert_none_to_empty_dict()
            self.__rename_multi_value_query_to_query_param()
            cast_parameter(self.data, self.schema)

        self.verify(True)

    @property
    def httpMethod(self) -> str:
        return self.data["httpMethod"] if "httpMethod" in self.data else "nonHTTP"

    @property
    def api_name(self) -> str:
        return self.__api_name

    def insert_specifics_to_origin(self, origin: str) -> str:
        if self.httpMethod not in origin:
            if ".json" == origin[-5:]:
                origin = origin[:-5]

            origin += "-" + self.httpMethod + ".json"

        return origin

    def __convert_none_to_empty_dict(self):
        # for json_schema validator not able to process type(None)
        for key in ["body", "pathParameters", "multiValueQueryStringParameters"]:
            try:
                if isinstance(self.data[key], type(None)):
                    self.data[key] = dict()
            except KeyError:
                pass

    def __rename_multi_value_query_to_query_param(self):
        self.data["queryParameters"] = (
            self.data["multiValueQueryStringParameters"]
            if "multiValueQueryStringParameters" in self.data
            else dict()
        )

    def __remove_empty_body(self):
        if "body" in self.data and self.data["body"] is None:
            del self.data["body"]

    @staticmethod
    def handle_exception(validation_error, _):
        if validation_error.context:
            body = validation_error.context[0].__str__()
        elif len(validation_error.__str__().split("\n")) > 12:
            body = validation_error.message
            if validation_error.absolute_path:
                body += f" in {'.'.join(validation_error.absolute_path)}"
        else:
            body = validation_error.__str__()

        raise TypeError(
            {
                "statusCode": 400
                if (
                    len(validation_error.path) == 0
                    or "httpMethod" != validation_error.path[0]
                )
                else 405,
                "body": body,
                "headers": {"Content-Type": "text/plain"},
            }
        )
