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

import dataclasses as dtcl
from pathlib import Path as path_t
from types import EllipsisType, GenericAlias, NoneType, UnionType
from typing import Annotated, Any, Iterable, Sequence, get_args, get_origin

# from conf_ini_g.extension.python import SpecificationPath

complex_hint_h = GenericAlias | UnionType
raw_hint_h = type | Any | complex_hint_h
annotated_hint_t = type(Annotated[object, None])
any_hint_h = raw_hint_h | annotated_hint_t


@dtcl.dataclass(slots=True, repr=False, eq=False)
class hint_node_t:
    type: type | EllipsisType | UnionType
    elements: tuple[hint_node_t, ...] | None = None


@dtcl.dataclass(slots=True, repr=False, eq=False)
class value_node_t:
    consolidated: Any
    type: type = dtcl.field(init=False)
    elements: tuple[value_node_t, ...] | None = None

    def __post_init__(self) -> None:
        """"""
        self.type = type(self.consolidated)


def TypeHintOfAnnotated(annotated_hint: annotated_hint_t, /) -> raw_hint_h:
    """"""
    return annotated_hint.__args__[0]


def AnnotationsOfType(annotated_hint: annotated_hint_t, /) -> Sequence[Any]:
    """"""
    return tuple(annotated_hint.__metadata__)


def HintTreeFromTypeHint(type_hint: raw_hint_h | EllipsisType | None, /) -> hint_node_t:
    """
    Note that type hints cannot translate into hint trees with an OR-node having a child
    OR-node. For example: str | (int | float) is interpreted as str | int | float. This
    is important when creating a type selector for multi-type parameters since only
    direct child nodes are taken into account for widget creation, so these nodes must
    be types, not an OR subtree.
    """
    if type_hint is None:
        return hint_node_t(type=NoneType)

    if (origin := get_origin(type_hint)) is None:
        return hint_node_t(type=type_hint)

    # Handled types: list, set, tuple, with sets using the dict delimiters { and }.
    if origin is dict:
        raise TypeError(f"{origin.__name__}: Unhandled type.")

    elements = tuple(HintTreeFromTypeHint(_elm) for _elm in get_args(type_hint))

    if origin is UnionType:
        return hint_node_t(type=UnionType, elements=elements)

    return hint_node_t(type=origin, elements=elements)


def TypeTemplateFromTypeHint(
    type_hint: raw_hint_h | EllipsisType | None, /
) -> type | dict[int, type] | NoneType:
    """"""
    if type_hint is None:
        return NoneType

    if (origin := get_origin(type_hint)) is None:
        return type_hint

    # Handled types: list, set, tuple, with sets using the dict delimiters { and }.
    if origin is dict:
        raise TypeError(f"{origin.__name__}: Unhandled type.")

    elements = tuple(TypeTemplateFromTypeHint(_elm) for _elm in get_args(type_hint))

    if origin is UnionType:
        return {_key: _elm for _key, _elm in enumerate(elements)}

    return origin(elements)


def ValueMatchesTypeHint(
    value: Any, type_hint: raw_hint_h | hint_node_t, /
) -> tuple[bool, value_node_t]:
    """"""
    value_tree = _ValueTreeOfValue(value)

    if type_hint is Any:
        return True, value_tree

    if isinstance(type_hint, hint_node_t):
        hint_tree = type_hint
    elif isinstance(type_hint, complex_hint_h):
        hint_tree = HintTreeFromTypeHint(type_hint)
    else:
        return isinstance(value, type_hint), value_tree

    return _CastValueTree(value_tree, hint_tree), value_tree


def ValueFromValueTree(value_tree: value_node_t, /) -> Any:
    """"""
    value = value_tree.consolidated

    if value is None:
        return None

    if isinstance(value, Iterable) and not isinstance(value, str):
        elements = (ValueFromValueTree(_elm) for _elm in value_tree.elements)
        return value_tree.type(elements)

    return value_tree.type(value)


def TypeAsRichStr(instance: Any, /, *, relative_to_home: bool = True) -> str:
    """"""
    return f"[bold magenta]{type(instance).__name__}[/]"
    # return (
    #     f"[bold magenta]{type(instance).__name__}[/]"
    #     f"[gray]@"
    #     f"{SpecificationPath(type(instance), relative_to_home=relative_to_home)}:[/]"
    # )


def NameValueTypeAsRichStr(name: str, value: Any, /, *, separator: str = "=") -> str:
    """"""
    if isinstance(value, Sequence) and (value.__len__() == 0):
        value = "[cyan]<empty>[/]"

    return f"[blue]{name}[/]{separator}{value}[yellow]:{type(value).__name__}[/]"


def _ValueTreeOfValue(value: Any, /) -> value_node_t:
    """"""
    if isinstance(value, Iterable) and not isinstance(value, str):
        elements = tuple(_ValueTreeOfValue(_elm) for _elm in value)
        return value_node_t(consolidated=value, elements=elements)

    return value_node_t(consolidated=value)


def _CastValueTree(value_node: value_node_t, hint_node: hint_node_t, /) -> bool:
    """
    Returned value=the value tree has been successfully cast to the hint node, or not.
    """
    hn_type = hint_node.type
    hn_elements = hint_node.elements

    if hn_type is Any:
        return True

    if hn_type is NoneType:
        if value_node.consolidated is None:
            return True
        else:
            return False

    if hn_type is UnionType:
        if any(_CastValueTree(value_node, _elm) for _elm in hn_elements):
            return True
        else:
            return False

    if not isinstance(value_node.consolidated, hn_type):
        try:
            converted = hn_type(value_node.consolidated)
            # If "hn_type" is a path and the consolidated value has a trailing folder
            # separator, then the general-purpose test fails. Hence the specialized
            # test below.
            if issubclass(hn_type, path_t):
                success = converted.match(str(value_node.consolidated))
            else:
                success = str(converted).replace(" ", "") == str(
                    value_node.consolidated
                ).replace(" ", "")
        except:
            success = False
        if not success:
            return False
    if (value_node.elements is None) and (hn_elements is None):
        value_node.type = hn_type
        return True

    if (value_node.elements is None) or (hn_elements is None):
        return False

    n_value_children = value_node.elements.__len__()
    n_hint_elements = hn_elements.__len__()
    has_ellipsis = (n_hint_elements == 2) and (hn_elements[1].type is Ellipsis)
    should_fake_ellipsis = (n_hint_elements == 1) and issubclass(hn_type, (list, set))
    if has_ellipsis or should_fake_ellipsis or (n_value_children == n_hint_elements):
        if has_ellipsis or should_fake_ellipsis:
            hint_elements = n_value_children * (hn_elements[0],)
        else:
            hint_elements = hn_elements
        for value_elm, hint_elm in zip(value_node.elements, hint_elements):
            if not _CastValueTree(value_elm, hint_elm):
                return False

        value_node.type = hn_type
        return True

    return False
