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
import textwrap as text
from typing import Sequence

from rich import print as rprint
from rich.text import Text as text_t

from conf_ini_g.catalog.specification.parameter.choices import choices_t
from conf_ini_g.extension.python import SpecificationPath
from conf_ini_g.extension.type import TypeAsRichStr
from conf_ini_g.specification.parameter.type import type_t
from conf_ini_g.specification.parameter.unit import UNIT_SEPARATOR
from conf_ini_g.specification.section.main import section_t
from conf_ini_g.specification.section.unit import UNIT_SECTION


@dtcl.dataclass(init=False, repr=False, eq=False)
class config_t(list[section_t]):
    spec_path: str = None

    def __init__(self, sections: Sequence[section_t], /) -> None:
        """
        Raising exceptions is adapted here since execution cannot proceed without a
        valid specification.
        """
        list.__init__(self, sections)
        self._SetControllerChoices()  # After __init__ so that self iterator is usable
        self.spec_path = SpecificationPath(sections)

        issues = self.Issues()
        if issues.__len__() > 0:
            rprint(
                self.spec_path,
                "[red]Invalid specification[/]",
                "\n".join(issues),
                sep="\n",
            )
            raise ValueError

    def _SetControllerChoices(self) -> None:
        """"""
        for section in self:
            if (controller := section.controller) is None:
                continue

            controlling_parameter = self[controller.section][controller.parameter]
            controlling_parameter.type = type_t.NewFromType(
                choices_t.NewAnnotatedType(section.controlling_values)
            )

    def AddUnitSection(self) -> None:
        """"""
        section = section_t(
            name=UNIT_SECTION,
            definition="Unit definitions",
            description=f"Units can be used in any other section "
            f"to specify a parameter value as follows: "
            f"numerical_value{UNIT_SEPARATOR}unit, e.g., 1.5'mm.",
            basic=True,
            optional=True,
            category=UNIT_SECTION,
            is_growable=True,
        )
        self.append(section)

    @property
    def section_names(self) -> Sequence[str]:
        """"""
        return tuple(_sct.name for _sct in self)

    def Issues(self) -> list[str]:
        """"""
        output = []

        if self.__len__() == 0:
            output.append("spec_path: Empty specification")
            return output

        names = self.section_names
        if names.__len__() > set(names).__len__():
            output.append("Specification with repeated section names")

        for section in self:
            if not isinstance(section, section_t):
                output.append(
                    f"{type(section).__name__}: Invalid section type; Expected={section_t.__name__}."
                )
                continue

            output.extend(section.Issues())
            if section.controller is not None:
                if section.controller.section not in self:
                    output.append(
                        f"{section.controller.section}: "
                        f'Unspecified section declared as controller of section "{section.name}"'
                    )
                else:
                    controller_section = self[section.controller.section]
                    if controller_section.controller is not None:
                        output.append(
                            f"{section.controller.section}: "
                            f'Section controlling "{section.name}" is itself controlled'
                        )
                    if section.controller.parameter not in controller_section:
                        output.append(
                            f"{section.controller.section}.{section.controller.parameter}: "
                            f'Unspecified parameter declared as controller of section "{section.name}"'
                        )
                    else:
                        controller_parameter = controller_section[
                            section.controller.parameter
                        ]
                        if controller_parameter.optional:
                            output.append(
                                f"{section.controller.section}.{section.controller.parameter}: "
                                f'Optional parameter declared as controller of section "{section.name}"'
                            )

        return output

    def _Item(self, key: str | int, /) -> section_t | None:
        """"""
        if isinstance(key, int):
            return list.__getitem__(self, key)

        for section in self:
            if section.name == key:
                return section

        return None

    def __contains__(self, key: str, /) -> bool:
        """"""
        return self._Item(key) is not None

    def __getitem__(self, key: str | int, /) -> section_t:
        """"""
        item = self._Item(key)
        if item is None:
            raise KeyError(f"{key}: Not a section of config.")

        return item

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        output = [
            TypeAsRichStr(self),
            f"    [blue]spec_path[/]={self.spec_path}"
            f"[yellow]:{type(self.spec_path).__name__}[/]",
        ]

        for section in self:
            output.append(text.indent(section.__rich__(), "    "))

        return "\n".join(output)
