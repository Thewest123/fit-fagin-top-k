import gradio as gr

from src.Mouse import Mouse
from src.Database import Database


class Algorithm:
    @classmethod
    def top_k_fagin(self, k: int, agg_function: str, agg_fields: list[str], db: Database, normalized=False):
        raise gr.Error("Fagin not implemented!")

    @classmethod
    def top_k_naive(self, k: int, agg_function: str, agg_fields: list[str], db: Database, normalized=False):
        agg_function = agg_function.lower()
        agg_fields = [field.lower() for field in agg_fields]

        func = self.__get_agg_function(agg_function)

        # Initialize top k list
        top_k = []

        # Iterate through database
        for mouse in db.get_data_normalized():
            # Calculate aggregate value
            agg_value = func(mouse, agg_fields)

            mousecol = mouse.as_list_normalized() if normalized else mouse.as_list()
            mousecol.append(agg_value)

            top_k.append(mousecol)

        # Sort top k list by aggregate value
        top_k.sort(key=lambda x: x[-1], reverse=True)

        # Return top k objects from top_k list
        return top_k[:k]

    @classmethod
    def __get_agg_function(self, agg_function: str) -> callable:
        if agg_function == "avg":
            return self.__avg
        elif agg_function == "min":
            return self.__min
        elif agg_function == "max":
            return self.__max
        elif agg_function == "sum":
            return self.__sum
        else:
            raise ValueError("Invalid aggregation function")

    @classmethod
    def __avg(self, mouse: Mouse, agg_fields: list[str]) -> float:
        sum_value = 0

        if "weight" in agg_fields:
            sum_value += mouse.weight_normalized

        if "accuracy" in agg_fields:
            sum_value += mouse.accuracy_normalized

        if "dpi" in agg_fields:
            sum_value += mouse.dpi_normalized

        if "price" in agg_fields:
            sum_value += mouse.price_normalized

        return sum_value / len(agg_fields)

    @classmethod
    def __min(self, mouse: Mouse, agg_fields: list[str]) -> float:
        min_value = float("inf")

        if "weight" in agg_fields:
            min_value = min(min_value, mouse.weight_normalized)

        if "accuracy" in agg_fields:
            min_value = min(min_value, mouse.accuracy_normalized)

        if "dpi" in agg_fields:
            min_value = min(min_value, mouse.dpi_normalized)

        if "price" in agg_fields:
            min_value = min(min_value, mouse.price_normalized)

        return min_value

    @classmethod
    def __max(self, mouse: Mouse, agg_fields: list[str]) -> float:
        max_value = float("-inf")

        if "weight" in agg_fields:
            max_value = max(max_value, mouse.weight_normalized)

        if "accuracy" in agg_fields:
            max_value = max(max_value, mouse.accuracy_normalized)

        if "dpi" in agg_fields:
            max_value = max(max_value, mouse.dpi_normalized)

        if "price" in agg_fields:
            max_value = max(max_value, mouse.price_normalized)

        return max_value

    @classmethod
    def __sum(self, mouse: Mouse, agg_fields: list[str]) -> float:
        sum_value = 0

        if "weight" in agg_fields:
            sum_value += mouse.weight_normalized

        if "accuracy" in agg_fields:
            sum_value += mouse.accuracy_normalized

        if "dpi" in agg_fields:
            sum_value += mouse.dpi_normalized

        if "price" in agg_fields:
            sum_value += mouse.price_normalized

        return sum_value
