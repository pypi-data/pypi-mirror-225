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
import re as regx
from typing import Any, Sequence

from rich.text import Text as text_t

from conf_ini_g.extension.string import AsInterpretedObject
from conf_ini_g.extension.type import (
    AnnotationsOfType,
    HintTreeFromTypeHint,
    TypeHintOfAnnotated,
    TypeTemplateFromTypeHint,
    ValueMatchesTypeHint,
    annotated_hint_t,
    any_hint_h,
    complex_hint_h,
    hint_node_t,
)
from conf_ini_g.specification.parameter.annotation import annotation_t
from conf_ini_g.specification.parameter.value import INVALID_VALUE


@dtcl.dataclass(slots=True, repr=False, eq=False)
class type_t:
    template: Any
    hint: type | hint_node_t
    annotations: Sequence[annotation_t]

    @classmethod
    def NewFromType(cls, type_: any_hint_h, /) -> type_t:
        """"""
        if type_ is None:
            raise ValueError("None: Invalid type hint.")

        if type_ is Any:
            return ANY_TYPE

        # nnt: Do not use "annotations" since it shadows __future__.annotations.
        if isinstance(type_, annotated_hint_t):
            hint = TypeHintOfAnnotated(type_)
            nnt = AnnotationsOfType(type_)
        else:
            hint = type_
            nnt = ()
        template = TypeTemplateFromTypeHint(hint)
        if isinstance(hint, complex_hint_h):
            hint = HintTreeFromTypeHint(hint)

        return cls(template=template, hint=hint, annotations=nnt)

    def Issues(self) -> list[str]:
        """"""
        output = []

        for annotation in self.annotations:
            output.extend(f"[{self}] {_iss}" for _iss in annotation.Issues())

        return output

    @property
    def base_hint(self) -> type:
        """"""
        if isinstance(self.hint, hint_node_t):
            return self.hint.type
        else:
            return self.hint

    @property
    def template_as_str(self) -> str:
        """"""
        output = (
            str(self.template)
            .replace("<class '", "")
            .replace("'>", "")
            .replace(str(Ellipsis), "...")
        )
        output = regx.sub("{\d: ", "{", output, flags=regx.ASCII)
        output = regx.sub(", \d:", " |", output, flags=regx.ASCII)

        return output

    def FirstAnnotationWithAttribute(
        self, attribute: str | Sequence[str], /
    ) -> annotation_t | None:
        """"""
        # Do not test isinstance(attribute, Sequence) since str is a sequence
        if isinstance(attribute, str):
            attributes = (attribute,)
        else:
            attributes = attribute

        for annotation in self.annotations:
            if all(hasattr(annotation, _ttr) for _ttr in attributes):
                return annotation

        return None

    def ValueIsCompliant(self, value: Any, /) -> bool:
        """"""
        return all(_nnt.ValueIsCompliant(value) for _nnt in self.annotations)

    def InterpretedValueOf(self, value: Any, /) -> tuple[Any, bool]:
        """"""
        if isinstance(value, str):
            typed_value, success = AsInterpretedObject(value, expected_type=self.hint)
        else:
            typed_value = value
            success, _ = ValueMatchesTypeHint(value, self.hint)

        if success and self.ValueIsCompliant(typed_value):
            return typed_value, True

        return INVALID_VALUE, False

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        output = [f"[blue]{self.template}[/]"]

        for annotation in self.annotations:
            output.append(type(annotation).__name__)

        return "&".join(output)


@dtcl.dataclass(slots=True, repr=False, eq=False)
class any_type_t(type_t):
    @classmethod
    def NewFromType(cls, type_: any_hint_h, /) -> type_t:
        """"""
        raise RuntimeError(
            f"{cls.__name__}: Not meant to be instantiated beside " f"singleton object."
        )

    def Issues(self) -> list[str]:
        """"""
        return []

    @property
    def base_hint(self) -> type:
        """"""
        return object

    def FirstAnnotationWithAttribute(
        self, attribute: str | Sequence[str], /
    ) -> annotation_t | None:
        """"""
        return None

    def ValueIsCompliant(self, value: Any, /) -> bool:
        """"""
        return True

    def InterpretedValueOf(self, value: Any, /) -> tuple[Any, bool]:
        """"""
        return value, True


ANY_TYPE = any_type_t(template="object", hint=object, annotations=())
