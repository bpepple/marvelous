from marshmallow import INCLUDE, Schema, fields, post_load, pre_load


class Dates:
    def __init__(self, on_sale=None, foc=None, unlimited=None, **kwargs):
        self.on_sale = on_sale
        self.foc = foc
        self.unlimited = unlimited
        self.unknown = kwargs


class DatesSchema(Schema):
    onsaleDate = fields.Date(attribute="on_sale")
    focDate = fields.Date(attribute="foc")  # Final Order Cutoff date
    unlimitedDate = fields.Date(attribute="unlimited")

    class Meta:
        unknown = INCLUDE
        dateformat = "%Y-%m-%dT%H:%M:%S%z"

    @pre_load
    def process_input(self, data, **kwargs):
        # Marvel comic 4373, and maybe others, returns a focDate of
        # "-0001-11-30T00:00:00-0500". The best way to handle this is
        # probably just to ignore it, since I don't know how to fix it.
        return {d["type"]: d["date"] for d in data if d["date"][0] != "-"}

    @post_load
    def make(self, data, **kwargs):
        return Dates(**data)
