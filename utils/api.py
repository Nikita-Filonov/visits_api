async def resolve_query_params(**query) -> dict:
    return {key: value for key, value in query.items() if (value is not None)}
