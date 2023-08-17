# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

import ast as bstr
import textwrap as text
from pathlib import Path as path_t
from types import NoneType
from typing import Any, Sequence

from conf_ini_g.extension.type import (
    ValueFromValueTree,
    ValueMatchesTypeHint,
    complex_hint_h,
    hint_node_t,
    raw_hint_h,
)


TRUE_VALUES = ("true", "yes", "on")
FALSE_VALUES = ("false", "no", "off")


def Flattened(string: str, /) -> str:
    """"""
    return text.dedent(string).replace("\n", "; ")


def AlignedOnSeparator(
    string: str | Sequence[str], separator: str, replacement: str, /
) -> str | tuple[str, ...] | list[str]:
    """"""
    if should_return_str := isinstance(string, str):
        lines = string.splitlines()
    else:
        lines = string
    indices = tuple(_lne.find(separator) for _lne in lines)
    longest = max(indices)

    output = (
        _lne.replace(separator, (longest - _lgt) * " " + replacement, 1)
        if _lgt > 0
        else _lne
        for _lne, _lgt in zip(lines, indices)
    )
    if should_return_str:
        return "\n".join(output)
    elif isinstance(string, tuple):
        return tuple(output)
    else:
        return list(output)


def AsInterpretedObject(
    string: str,
    /,
    *,
    expected_type: raw_hint_h | hint_node_t | NoneType = None,
) -> tuple[Any, bool]:
    """
    expected_type: Must not be passed explicitly as None since None is interpreted as
    "no specific expected type". When expecting None, pass types.NoneType.
    """
    if expected_type is None:
        return _AsInterpretedObjectWithoutClue(string)

    if isinstance(expected_type, (complex_hint_h, hint_node_t)):
        value, _ = _AsInterpretedObjectWithoutClue(string)
        success, value_tree = ValueMatchesTypeHint(value, expected_type)
        if success:
            return ValueFromValueTree(value_tree), True
        else:
            return None, False

    return _AsInterpretedObject(string, expected_type)


def _AsInterpretedObjectWithoutClue(string: str, /) -> tuple[Any, bool]:
    """"""
    try:
        value = bstr.literal_eval(string)
    except (SyntaxError, ValueError):
        value = string

    return value, True


def _AsInterpretedObject(string: str, expected_type: type, /) -> tuple[Any, bool]:
    """"""
    failed_interpretation = None, False
    lowered = string.lower()

    if expected_type is NoneType:
        return None, (lowered == "none")

    if expected_type is bool:
        if lowered in TRUE_VALUES:
            return True, True
        if lowered in FALSE_VALUES:
            return False, True
        return failed_interpretation

    if expected_type is path_t:
        if string.__len__() > 0:
            return path_t(string), True
        else:
            return None, True

    # The expected type might be instantiable from a string, e.g.: float("1.0").
    # However, a success does not mean that the interpretation is valid, e.g.:
    # tuple("(1, 2, 3)"). To confirm that a success is indeed a correct interpretation,
    # the string representation of the interpreted value is compared with the string.
    # This is not a perfect test, so "literal_eval" might still be called below.
    try:
        value = expected_type(string)
        # If "expected_type" is a path and the consolidated value has a trailing folder
        # separator, then the general-purpose test fails. Hence the specialized
        # test below.
        if issubclass(expected_type, path_t):
            success = value.match(string)
        else:
            success = str(value).replace(" ", "") == string.replace(" ", "")
    except:
        value, success = failed_interpretation
    if success:
        return value, True

    try:
        value = bstr.literal_eval(string)
        success = type(value) is expected_type
        if not success:
            value = None
    except (SyntaxError, ValueError):
        value, success = failed_interpretation

    return value, success
