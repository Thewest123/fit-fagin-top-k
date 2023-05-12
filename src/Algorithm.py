import gradio as gr

from src.Mouse import Mouse
from src.Database import Database


class Algorithm:
    @classmethod
    def top_k_fagin(cls, k: int, agg_function: str, agg_fields: list[str], db: Database, normalized=False):
        agg_function = agg_function.lower()
        agg_fields = [field.lower() for field in agg_fields]

        func = cls.__get_agg_function(agg_function)

        # Initialize top k list
        top_k = []
        access_count = 0

        # Sets of accessed fields
        accessed_all = set()

        accessed_weight = set()
        accessed_accuracy = set()
        accessed_dpi = set()
        accessed_price = set()

        # Iterate through database
        # print(f"Range: {len(db.get_data_normalized())}")
        for i in range(len(db.get_data_normalized())):
            access_count += 1
            # print("Iteration", i)

            if "weight" in agg_fields:
                # print("Weight")
                mouse = db.get_sorted_weight()[i][1]
                accessed_weight.add(mouse)
                if cls.__is_in_all(mouse, agg_fields, accessed_weight, accessed_accuracy, accessed_dpi, accessed_price):
                    # print(f"[Weight] Adding {mouse} to accessed all")
                    accessed_all.add(mouse)

            if "accuracy" in agg_fields:
                mouse = db.get_sorted_accuracy()[i][1]
                accessed_accuracy.add(mouse)
                if cls.__is_in_all(mouse, agg_fields, accessed_weight, accessed_accuracy, accessed_dpi, accessed_price):
                    # print(f"[Accuracy] Adding {mouse} to accessed all")
                    accessed_all.add(mouse)

            if "dpi" in agg_fields:
                mouse = db.get_sorted_dpi()[i][1]
                accessed_dpi.add(mouse)
                if cls.__is_in_all(mouse, agg_fields, accessed_weight, accessed_accuracy, accessed_dpi, accessed_price):
                    # print(f"[DPI] Adding {mouse} to accessed all")
                    accessed_all.add(mouse)

            if "price" in agg_fields:
                mouse = db.get_sorted_price()[i][1]
                accessed_price.add(mouse)
                if cls.__is_in_all(mouse, agg_fields, accessed_weight, accessed_accuracy, accessed_dpi, accessed_price):
                    # print(f"[Price] Adding {mouse} to accessed all")
                    accessed_all.add(mouse)

            if len(accessed_all) >= k:
                # print("Breaking")
                break

        for mouse in accessed_all:
            agg_value = func(mouse, agg_fields)

            mousecol = mouse.as_list_normalized() if normalized else mouse.as_list()
            mousecol.append(agg_value)

            # print(f"Adding {mousecol} to top k")
            top_k.append(mousecol)

        # Sort top k list by aggregate value
        top_k.sort(key=lambda x: x[-1], reverse=True)

        # Return top k objects from top_k list
        return (top_k, access_count)

        raise gr.Error("Fagin not implemented!")

    @classmethod
    def top_k_naive(cls, k: int, agg_function: str, agg_fields: list[str], db: Database, normalized=False):
        agg_function = agg_function.lower()
        agg_fields = [field.lower() for field in agg_fields]

        func = cls.__get_agg_function(agg_function)

        # Initialize top k list
        top_k = []
        access_count = 0

        # Iterate through database
        for mouse in db.get_data_normalized():
            access_count += 1

            # Calculate aggregate value
            agg_value = func(mouse, agg_fields)

            mousecol = mouse.as_list_normalized() if normalized else mouse.as_list()
            mousecol.append(agg_value)

            top_k.append(mousecol)

        # Sort top k list by aggregate value
        top_k.sort(key=lambda x: x[-1], reverse=True)

        # Return top k objects from top_k list
        return (top_k[:k], access_count)

    @classmethod
    def __is_in_all(
        cls,
        mouse: Mouse,
        agg_fields: list,
        accessed_weight: set,
        accessed_accuracy: set,
        accessed_dpi: set,
        accessed_price: set,
    ) -> bool:
        if "weight" in agg_fields and mouse not in accessed_weight:
            # print(f"{mouse} not in accessed weight")
            return False

        if "accuracy" in agg_fields and mouse not in accessed_accuracy:
            # print(f"{mouse} not in accessed accuracy")
            return False

        if "dpi" in agg_fields and mouse not in accessed_dpi:
            # print(f"{mouse} not in accessed dpi")
            return False

        if "price" in agg_fields and mouse not in accessed_price:
            # print(f"{mouse} not in accessed price")
            return False

        # print(f"{mouse} in all")
        return True

    @classmethod
    def __get_agg_function(cls, agg_function: str) -> callable:
        if agg_function == "avg":
            return cls.__avg
        elif agg_function == "min":
            return cls.__min
        elif agg_function == "max":
            return cls.__max
        elif agg_function == "sum":
            return cls.__sum
        else:
            raise ValueError("Invalid aggregation function")

    @classmethod
    def __avg(cls, mouse: Mouse, agg_fields: list[str]) -> float:
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
    def __min(cls, mouse: Mouse, agg_fields: list[str]) -> float:
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
    def __max(cls, mouse: Mouse, agg_fields: list[str]) -> float:
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
    def __sum(cls, mouse: Mouse, agg_fields: list[str]) -> float:
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
