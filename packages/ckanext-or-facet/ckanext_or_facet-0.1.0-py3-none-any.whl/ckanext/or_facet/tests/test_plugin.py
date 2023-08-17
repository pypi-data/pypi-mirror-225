"""Tests for plugin.py."""
import pytest
import ckan.tests.helpers as helpers
import ckan.tests.factories as factories
import ckanext.or_facet.plugin as plugin


def _orPrefix(field):
    return "{!q.op=OR tag=orFq%s}" % field


class TestConfig(object):
    def test_missing_config_parsed(self):
        assert plugin._get_default_ors() == []

    @pytest.mark.ckan_config("or_facet.or_facets", None)
    def test_empty_config_parsed(self):
        assert plugin._get_default_ors() == []

    @pytest.mark.ckan_config("or_facet.or_facets", "tags")
    def test_single_config_parsed(self):
        assert plugin._get_default_ors() == ["tags"]

    @pytest.mark.ckan_config("or_facet.or_facets", "tags res_format")
    def test_multiple_config_parsed(self):
        assert plugin._get_default_ors() == ["tags", "res_format"]


class TestExtraOrs(object):
    def test_base_case(self):
        extras = {
            "ext_a": 1,
            plugin._extra_or_prefix + 'tags': 'on',
            plugin._extra_or_prefix + 'groups': 'off',
        }
        assert plugin._get_extra_ors_state(extras) == {
            'tags': True, "groups": False
        }


class TestSplit(object):
    @pytest.mark.parametrize(
        "fq, field, expected",
        [
            ('tags:"Structural Framework"', "tags",
             ('{!q.op=OR tag=orFqtags}tags:"Structural Framework"', "")),
            ("organization:123", "tags", (None, "organization:123")),
            ("", "tags", (None, "")),
            ("x:1", "x", (_orPrefix("x") + "x:1", "")),
            ("x:hello x:world", "x", (_orPrefix("x") + "x:hello x:world", "")),
            ("x:a y:b", "y", (_orPrefix("y") + "y:b", "x:a")),
            ('x:"a" y:"b"', "y", (_orPrefix("y") + 'y:"b"', 'x:"a"')),
            (
                "z:1 x:a z:2 x:\"b\" z:3 x:'c'",
                "x",
                (_orPrefix("x") + "x:a x:\"b\" x:'c'", "z:1  z:2  z:3"),
            ),
            (
                "x-x:a-a y-y:b-b z-z:c-c",
                "x-x",
                (_orPrefix("x-x") + "x-x:a-a", "y-y:b-b z-z:c-c"),
            ),
            (
                "x-x:a-a y-y:b-b z-z:c-c",
                "y-y",
                (_orPrefix("y-y") + "y-y:b-b", "x-x:a-a  z-z:c-c"),
            ),
            (
                "x-x:a-a y-y:b-b z-z:c-c",
                "z-z",
                (_orPrefix("z-z") + "z-z:c-c", "x-x:a-a y-y:b-b"),
            ),

        ],
    )
    def test_split(self, fq, field, expected):
        assert plugin._split_fq(fq, field) == expected


@pytest.mark.usefixtures("clean_db", "clean_index")
class TestPlugin(object):
    @pytest.mark.ckan_config("or_facet.or_facets", "tags res_format")
    def test_search_with_two_ors(self):
        expected_tags = {"bye": 1, "hello": 1, "world": 2}
        expected_formats = {"JSON": 1, "HTML": 1, "CSV": 2}

        d1 = factories.Dataset(tags=[{"name": "hello"}, {"name": "world"}])
        d2 = factories.Dataset(tags=[{"name": "bye"}, {"name": "world"}])

        factories.Resource(package_id=d1["id"], format="CSV")
        factories.Resource(package_id=d1["id"], format="JSON")
        factories.Resource(package_id=d2["id"], format="CSV")
        factories.Resource(package_id=d2["id"], format="HTML")

        for tag, count in expected_tags.items():
            result = helpers.call_action(
                "package_search",
                fl="id,tags",
                fq="tags:{}".format(tag),
                **{"facet.field": '["tags"]'}
            )
            assert result["count"] == count
            assert result["facets"]["tags"] == expected_tags

        for fmt, count in expected_formats.items():
            result = helpers.call_action(
                "package_search",
                fq="res_format:{}".format(fmt),
                **{"facet.field": '["res_format"]'}
            )
            assert result["count"] == count
            assert result["facets"]["res_format"] == expected_formats

    @pytest.mark.ckan_config("or_facet.or_facets", "tags")
    def test_search_with_one_or_and_one_extra_or(self):
        expected_tags = {"bye": 1, "hello": 1, "world": 2}
        expected_formats = {"JSON": 1, "HTML": 1, "CSV": 2}

        d1 = factories.Dataset(tags=[{"name": "hello"}, {"name": "world"}])
        d2 = factories.Dataset(tags=[{"name": "bye"}, {"name": "world"}])

        factories.Resource(package_id=d1["id"], format="CSV")
        factories.Resource(package_id=d1["id"], format="JSON")
        factories.Resource(package_id=d2["id"], format="CSV")
        factories.Resource(package_id=d2["id"], format="HTML")

        for tag, count in expected_tags.items():
            result = helpers.call_action(
                "package_search",
                fl="id,tags",
                fq="tags:{}".format(tag),
                **{
                    "facet.field": '["tags"]',
                    plugin._extra_or_prefix + 'res_format': 'on'
                }
            )
            assert result["count"] == count
            assert result["facets"]["tags"] == expected_tags

        for fmt, count in expected_formats.items():
            result = helpers.call_action(
                "package_search",
                fq="res_format:{}".format(fmt),
                **{
                    "facet.field": '["res_format"]',
                    plugin._extra_or_prefix + 'res_format': 'on'
                }
            )
            assert result["count"] == count
            assert result["facets"]["res_format"] == expected_formats

    @pytest.mark.ckan_config("or_facet.or_facets", "tags")
    def test_search_with_one_or(self):
        expected_tags = {"bye": 1, "hello": 1, "world": 2}
        factories.Dataset(tags=[{"name": "hello"}, {"name": "world"}])
        factories.Dataset(tags=[{"name": "bye"}, {"name": "world"}])

        for tag, count in expected_tags.items():
            result = helpers.call_action(
                "package_search",
                fl="id,tags",
                fq="tags:{}".format(tag),
                **{"facet.field": '["tags"]'}
            )
            assert result["count"] == count
            assert result["facets"]["tags"] == expected_tags

    def test_search_without_ors(self):

        factories.Dataset(tags=[{"name": "hello"}, {"name": "world"}])
        factories.Dataset(tags=[{"name": "bye"}, {"name": "world"}])

        result = helpers.call_action(
            "package_search",
            fl="id,tags",
            fq="tags:hello",
            **{"facet.field": '["tags"]'}
        )
        assert result["count"] == 1
        assert result["facets"]["tags"] == {"hello": 1, "world": 1}

        result = helpers.call_action(
            "package_search",
            fl="id,tags",
            fq="tags:bye",
            **{"facet.field": '["tags"]'}
        )
        assert result["count"] == 1
        assert result["facets"]["tags"] == {"bye": 1, "world": 1}

        result = helpers.call_action(
            "package_search",
            fl="id,tags",
            fq="tags:world",
            **{"facet.field": '["tags"]'}
        )
        assert result["count"] == 2
        assert result["facets"]["tags"] == {"bye": 1, "hello": 1, "world": 2}
