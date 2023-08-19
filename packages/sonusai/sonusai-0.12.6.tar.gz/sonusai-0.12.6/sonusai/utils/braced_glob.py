from typing import Generator
from typing import List
from typing import Optional
from typing import Set


def expand_braces(text: str, seen: Optional[Set[str]] = None) -> Generator[str, None, None]:
    """Brace-expansion pre-processing for glob.

    Expand all the braces, then run glob on each of the results.
    (Brace-expansion turns one string into a list of strings.)
    https://stackoverflow.com/questions/22996645/brace-expansion-in-python-glob
    """
    import itertools
    import re

    if seen is None:
        seen = set()

    spans = [m.span() for m in re.finditer(r'\{[^{}]*}', text)][::-1]
    alts = [text[start + 1: stop - 1].split(',') for start, stop in spans]

    if len(spans) == 0:
        if text not in seen:
            yield text
        seen.add(text)
    else:
        for combo in itertools.product(*alts):
            replaced = list(text)
            for (start, stop), replacement in zip(spans, combo):
                replaced[start:stop] = replacement
            yield from expand_braces(''.join(replaced), seen)


def braced_glob(path: str) -> List[str]:
    from glob import glob

    result = []
    for x in expand_braces(path):
        result.extend(glob(x))

    return result
