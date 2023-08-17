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
import itertools as ittl
import textwrap as text
from typing import Any
from typing import NamedTuple as named_tuple_t
from typing import Sequence

from rich.text import Text as text_t

from conf_ini_g.extension.string import AlignedOnSeparator
from conf_ini_g.extension.type import TypeAsRichStr
from conf_ini_g.specification.base import base_t
from conf_ini_g.specification.parameter.main import parameter_t
from conf_ini_g.specification.parameter.unit import unit_t
from conf_ini_g.specification.section.unit import IsUnitSection

PARAMETERS = "parameters"


@dtcl.dataclass(init=False, repr=False, eq=False)  # Cannot have __init__ method
class controller_t(named_tuple_t):
    section: str = None
    parameter: str = None
    # All controller values are equal in role. However, this one is called primary
    # because it refers to the parameters of the section, as opposed to the parameters
    # in the alternatives.
    primary_value: Any = None

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        return (
            f"[magenta]{type(self).__name__}[/]: "
            f"[blue]{self.section}.{self.parameter}[/]={self.primary_value}"
        )


@dtcl.dataclass(repr=False, eq=False)
class section_t(base_t, list[parameter_t]):
    category: str = "Main"
    optional: bool = False
    is_growable: bool = False
    controller: controller_t = None
    alternatives: dict[str, list[parameter_t]] = None
    parameters: list[parameter_t] | None = None  # Used only during instantiation.

    def __post_init__(self) -> None:
        """"""
        if self.parameters is not None:
            self.extend(self.parameters)
            self.parameters = None

    def AddUnspecifiedParameter(self, name: str, /) -> parameter_t:
        """
        For programmatic use
        """
        if IsUnitSection(self.name):
            parameter = unit_t(
                name=name,
                definition="Unit definition",
                basic=True,
            )
        else:
            parameter = parameter_t(
                name=name,
                definition="Programmatic parameter",
                description="This parameter is not part of the specification. "
                "It was added programmatically because it was found in the INI document or "
                "passed as a command-line argument",
                basic=self.basic,
            )
        self.append(parameter)

        return parameter

    @property
    def all_parameters(self) -> Sequence[parameter_t]:
        """"""
        if self.alternatives is None:
            return self
        else:
            return tuple(ittl.chain(self, *self.alternatives.values()))

    def ActiveParameters(self, controller_value: str, /) -> Sequence[parameter_t]:
        """"""
        if controller_value == self.controller.primary_value:
            return self
        else:
            return self.alternatives[controller_value]

    @property
    def controlling_values(self) -> Sequence[Any]:
        """
        No check of controlled status; Call with care.
        """
        return (self.controller.primary_value,) + tuple(self.alternatives.keys())

    def Issues(self) -> list[str]:
        """"""
        output = super().Issues()

        valid_name_sets = [tuple(_prm.name for _prm in self)]
        if self.alternatives is not None:
            for parameters in self.alternatives.values():
                valid_name_sets.append(tuple(_prm.name for _prm in parameters))
        for valid_name_set in valid_name_sets:
            if valid_name_set.__len__() > set(valid_name_set).__len__():
                output.append(
                    f"{self.name}: Section with repeated parameter names (possibly in alternatives)"
                )

        basic = self.basic
        optional = self.optional

        if not (basic or optional):
            output.append(f"{self.name}: Section is not basic but not optional")

        if (self.controller is None) and (not optional) and (self.__len__() == 0):
            output.append(f"{self.name}: Empty mandatory section")

        n_parameters = 0
        n_basic_prms = 0
        for parameter in self.all_parameters:
            output.extend(f"[{self.name}] {_iss}" for _iss in parameter.Issues())

            n_parameters += 1
            if parameter.basic:
                n_basic_prms += 1

            if parameter.basic and not basic:
                output.append(
                    f'{parameter.name}: Basic parameter in advanced section "{self.name}"'
                )
            if optional and not parameter.optional:
                output.append(
                    f'{parameter.name}: Mandatory parameter in optional section "{self.name}"'
                )

        if (n_parameters == 0) and not self.is_growable:
            output.append(
                f"{self.name}: Section without specified parameters which does not accept unspecified parameters"
            )
        if basic and (n_parameters > 0) and (n_basic_prms == 0):
            output.append(f"{self.name}: Basic section without any basic parameters")

        control = (self.controller, self.alternatives)
        if any(_elm is None for _elm in control) and any(
            _elm is not None for _elm in control
        ):
            output.append(
                f"{self.name}: Controlled section must have both a controller and alternative parameters"
            )
        elif self.controller is not None:
            if self.controller.section == self.name:
                output.append(f"{self.name}: Section cannot be controlled by itself")
            controlling_values = self.controlling_values
            if controlling_values.__len__() > set(controlling_values).__len__():
                output.append(
                    f"{self.name}: Controlled section has duplicated controller values"
                )
            for parameter in self.all_parameters:
                if not parameter.optional:
                    output.append(
                        f'{parameter.name}: Mandatory parameter in controlled section "{self.name}"'
                    )

        return output

    def _Item(self, key: str | int, /) -> parameter_t | None:
        """"""
        if isinstance(key, int):
            return list.__getitem__(self, key)

        for parameter in self.all_parameters:
            if parameter.name == key:
                return parameter

        return None

    def __contains__(self, key: str, /) -> bool:
        """"""
        return self._Item(key) is not None

    def __getitem__(self, key: str | int, /) -> parameter_t:
        """"""
        item = self._Item(key)
        if item is None:
            raise KeyError(f"{key}: Not a parameter of section {self.name}.")

        return item

    def __rich__(self) -> str:
        """"""
        output = [
            TypeAsRichStr(self),
            *text.indent(super().__rich__(), "    ").splitlines(),
            f"    [blue]Category[/]@=@{self.category}",
            f"    [blue]Optional[/]@=@{self.optional}",
            f"    [blue]Growable[/]@=@{self.is_growable}",
        ]

        if has_controller := (self.controller is not None):
            output.append(f"    [blue]Controller[/]@=@{self.controller}")

        output.extend(text.indent(_prm.__rich__(), "    ") for _prm in self)
        if has_controller:
            output.append("    With alternatives:")
            for ctl_name, parameters in self.alternatives.items():
                output.append(f"        {ctl_name}")
                for parameter in parameters:
                    output.append(text.indent(parameter.__rich__(), "            "))

        output = AlignedOnSeparator(output, "@=@", " = ")

        return "\n".join(output)
