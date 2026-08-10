from executors.provider_registry import get_provider, match_provider, provider_definitions

REQUIRED = {
    "builtin_geometry_nodes", "sapling_tree_gen", "ivygen", "ant_landscape", "sverchok",
    "meshy", "mpfb", "geo_nodes_guide", "mcp", "geonodes", "engon_botaniq",
    "archimesh", "nodetopython", "the_grove", "procfunc", "blenderproc", "infinigen",
}


def test_required_provider_registry_coverage():
    assert REQUIRED <= set(provider_definitions())


def test_alias_matching_uses_registry():
    provider_id, definition = match_provider("add_curve_sapling", "Sapling Tree Gen")
    assert provider_id == "sapling_tree_gen"
    assert definition == get_provider("sapling_tree_gen")


def test_unknown_provider_does_not_match_utility():
    provider_id, definition = match_provider("totally_unknown_addon", "Mystery Provider")
    assert provider_id is None
    assert definition is None
