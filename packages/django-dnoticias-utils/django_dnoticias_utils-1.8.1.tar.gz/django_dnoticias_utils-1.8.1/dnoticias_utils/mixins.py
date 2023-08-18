from typing import Any, Optional


class APIResponseMixin:
    success_message = "Operação realizada com sucesso."
    error_message = "Ocorreu um erro ao processar o pedido."

    def get_success_message(self, data: Optional[Any] = None) -> str:
        return self.success_message

    def get_error_message(self, data: Optional[Any] = None) -> str:
        return self.error_message

    def get_response_data(
        self,
        serializer: Optional[Any] = None,
        data: Optional[Any] = None
    ) -> dict:
        return serializer.data if serializer else data

    def get_response(
        self,
        data: Optional[Any] = None,
        serializer: Optional[Any] = None,
        errors: Optional[list] = []
    ) -> dict:
        message = self.get_success_message(data=data)
        data = data or {}

        if serializer and not serializer.is_valid():
            message = self.get_error_message(data=data)

            for __, _errors in serializer.errors.items():
                for error in _errors:
                    errors.append(error)

        elif errors:
            message = self.get_error_message(data=data)

        return {
            "status": "success" if not errors else "error",
            "data": self.get_response_data(serializer, data),
            "message": message,
            "errors": data.get("errors") or errors
        }
