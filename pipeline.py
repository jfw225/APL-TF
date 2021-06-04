class Pipeline(object):
    """Pipeline class for individual input-based submission to the pipeline."""

    def __init__(self, source=None):
        self.source = source

    def __rshift__(self, other):
        """Allows Pipeline objects to connect using the `>>` operator."""

        other.map = self.create_map(other.map)
        return other

    def create_map(self, other_map):
        """Returns a new map function that calls self.map and forward its return value to other_map."""

        def map(data):

            data = self.map(data)

            return other_map(data)

        return map

    def map(self, data):
        """Overwrite to map the pipeline data."""

        return data

    def filter(self, data):
        """Overwrite to filter out the pipeline data."""

        return True