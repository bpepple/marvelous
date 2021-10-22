"""
Character module.

This module provides the following classes:

- Character
- CharacterSchema
"""
from marshmallow import INCLUDE, Schema, fields, post_load, pre_load

from esak import comic_summary, events_summary, exceptions, series, story_summary, urls


class Character:
    """
    The Character object contains information for characters.

    :param `**kwargs`: The keyword arguments is used for setting character data from Marvel.
    """

    def __init__(self, **kwargs):
        """Intialize a new Character."""
        if "response" not in kwargs:
            kwargs["response"] = None

        for k, v in kwargs.items():
            setattr(self, k, v)


class CharacterSchema(Schema):
    """Schema for the Character API."""

    id = fields.Int()
    name = fields.Str()
    description = fields.Str()
    modified = fields.DateTime()
    resourceURI = fields.Str(attribute="resource_uri")
    urls = fields.Nested(urls.UrlsSchema)
    thumbnail = fields.Url()
    comics = fields.Nested(comic_summary.ComicSummarySchema, many=True)
    stories = fields.Nested(story_summary.StorySummarySchema, many=True)
    events = fields.Nested(events_summary.EventSummarySchema, many=True)
    series = fields.Nested(series.SeriesSchema, many=True)

    class Meta:
        """Any unknown fields will be included."""

        unknown = INCLUDE

    @pre_load
    def process_input(self, data, **kwargs):
        if data.get("code", 200) != 200:
            raise exceptions.ApiError(data.get("status"))

        if "status" in data:
            data["data"]["results"][0]["response"] = data
            data = data["data"]["results"][0]

        if "thumbnail" in data:
            data["thumbnail"] = f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}"

        if "events" in data:
            data["events"] = data["events"]["items"]

        if "series" in data:
            data["series"] = data["series"]["items"]

        if "stories" in data:
            data["stories"] = data["stories"]["items"]

        if "comics" in data:
            data["comics"] = data["comics"]["items"]

        data["id"] = data["resourceURI"].split("/")[-1]
        return data

    @post_load
    def make(self, data, **kwargs):
        """
        Make the character object.

        :param data: Data from Marvel response.

        :returns: :class:`Character` object
        :rtype: Character
        """
        return Character(**data)
