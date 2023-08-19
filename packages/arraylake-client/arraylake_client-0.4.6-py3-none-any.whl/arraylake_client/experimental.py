import re
from typing import List

from arraylake_client import repo
from arraylake_client.log_util import get_logger
from arraylake_client.zarr_util import meta_root

logger = get_logger(__name__)
logger.warning("Functionality enabled by importing arraylake_client.experimental is alpha & subject to change on short notice")


# This function is expected to be patched onto arraylake_client.repo.AsyncRepo
async def async_filter_metadata(self, jmespath_expression: str) -> List[str]:
    """Filter repo metadata documents using a JMSE search string.

    https://jmespath.org/specification.html
    """
    items = self._list(meta_root, all_subdirs=True, _jmespath_filter_expression=jmespath_expression)
    results = []
    async for result in items:
        matches = re.match(rf"{meta_root}(.*)(\.array|\.group).json", result)
        results.append(matches.group(1))
    return results


# This function is expected to be patched onto arraylake_client.repo.AsyncRepo
def sync_filter_metadata(self, jmespath_expression: str) -> List[str]:
    """Filter repo metadata attributes using a JMSE search string.

    The full JMES spec including examples and an interactive console is available [here](https://jmespath.org/specification.html).

    Some specific examples of queries:

        "flags[0].spec[0] == 'a'"
        "flags[0].spec[0:2] == ['a', 'b']"
        'flags[0].spec[2] == band'
        "contains(keys(@), 'flags') && contains(keys(@), 'band') && flags[0].spec[2] == band"
        "someNaN == 'NaN'"
        'number >= `3` && number <= `15`'
        '"eo:val" == `12`'
        '"created:at:time" <= `2022-05-01`'
        '(!flags == `5` || flags == `10`) && foo == `10`'


        And some specific nuances to be aware of:

        1. NaNs are strings, assert for them as follows:

                "someKey == 'NaN'"

            The following will not match NaN values:

                "someNaN == NaN"
                "someNaN == `NaN`"

        2. Comparison of two missing keys is truthy:

            The following will return true if both don't exist on the doc, as null == null

                'foo == bar'

            Here's a safer way to perform this query:

                'contains(keys(@), "foo") && contains(keys(@), "bar") && foo == bar'

        3. Keys with special characters should be double quoted

                '"eo:val" == `12`'

            The following will fail

                'eo:val == `12`'
    """
    return self._synchronize(self._arepo.filter_metadata, jmespath_expression)


# monkey patch the repo classes with new functionality
repo.AsyncRepo.filter_metadata = async_filter_metadata  # type: ignore
repo.Repo.filter_metadata = sync_filter_metadata  # type: ignore
