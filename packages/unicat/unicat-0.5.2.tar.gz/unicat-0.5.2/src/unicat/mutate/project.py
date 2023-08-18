from ..error import UnicatError


def add_language(unicat, language):
    success, result = unicat.api.call("/languages/add", {"language": language})
    if not success:
        raise UnicatError("add_language", result)
    return True


def remove_language(unicat, language):
    success, result = unicat.api.call("/languages/remove", {"language": language})
    if not success:
        raise UnicatError("remove_language", result)
    return True


def create_channel(unicat, name):
    success, result = unicat.api.call("/channels/create", {"name": name})
    if not success:
        raise UnicatError("create_channel", result)
    return result["channel"]


def delete_channel(unicat, channel_gid):
    success, result = unicat.api.call("/channels/delete", {"channel": channel_gid})
    if not success:
        raise UnicatError("delete_channel", result)
    return True


def create_ordering(unicat, name):
    success, result = unicat.api.call("/orderings/create", {"name": name})
    if not success:
        raise UnicatError("create_ordering", result)
    return result["ordering"]


def delete_ordering(unicat, ordering_gid):
    success, result = unicat.api.call("/orderings/delete", {"ordering": ordering_gid})
    if not success:
        raise UnicatError("delete_ordering", result)
    return True


def create_fieldlist(unicat, name):
    success, result = unicat.api.call("/fieldlists/create", {"name": name})
    if not success:
        raise UnicatError("create_fieldlist", result)
    return result["fieldlist"]


def delete_fieldlist(unicat, fieldlist_gid):
    success, result = unicat.api.call(
        "/fieldlists/delete", {"fieldlist": fieldlist_gid}
    )
    if not success:
        raise UnicatError("delete_fieldlist", result)
    return True
