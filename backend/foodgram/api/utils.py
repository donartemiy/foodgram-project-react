def geterate_buying_list(RecipeIngredient, shopping_cart) -> str:
    """
    Формируется список таблица с полями ингредиент и его количество.
    Для ингредиентов, повторяющихся в нескольких рецептах
    подсчитывается суммарное количество.

    Example output:
        ананасы (г) - 1
        вода минеральная без газа (стакан) - 5
        капуста белокочанная (г) - 1000
        лук зеленый (г) - 100
    """
    buying_list = {}

    for record in shopping_cart:
        recipe = record.recipe
        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {
                    "measurement_unit": measurement_unit,
                    "amount": amount, }
            else:
                buying_list[name]["amount"] = (
                    buying_list[name]["amount"] + amount)

    wishlist = []
    for name, data in buying_list.items():
        wishlist.append(
            f"{name} ({data['measurement_unit']}) - {data['amount']}\n")
    content = "".join(wishlist)
    return content
