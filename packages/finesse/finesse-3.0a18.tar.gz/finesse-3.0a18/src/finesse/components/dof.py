from finesse.components.node import NodeType, NodeDirection
from finesse.components.general import Connector, LocalDegreeOfFreedom
from finesse.components.workspace import (
    ConnectorWorkspace,
    Connections,
)
import numpy as np
from finesse.parameter import float_parameter
from more_itertools import roundrobin
from finesse.symbols import Symbol
from finesse.parameter import Parameter, ParameterRef


class DOFWorkspace(ConnectorWorkspace):
    def __init__(self, owner, sim):
        super().__init__(owner, sim, Connections(), Connections())
        self.drives = None
        self.amplitudes = None


@float_parameter("DC", "DC state of degree of freedom")
class DegreeOfFreedom(Connector):
    """"""

    def __init__(self, name, *node_amplitude_pairs, DC=0):
        Connector.__init__(self, name)
        if len(node_amplitude_pairs) == 0:
            raise RuntimeError("Must specify at least one node to define this DOF")

        self._add_to_model_namespace = True
        self.__drives = list(node_amplitude_pairs[::2])
        if len(node_amplitude_pairs) > 1:
            self.__amplitudes = np.array(node_amplitude_pairs[1::2])
        else:
            self.__amplitudes = np.array((1, *node_amplitude_pairs[1::2]))
        self.DC = DC

        if len(self.drives) != len(self.amplitudes):
            raise Exception(
                f"Nodes and amplitudes were not the same length, {len(self.drives)} vs {len(self.amplitudes)}"
            )

        add_AC = False
        for i, node in enumerate(self.drives):
            if isinstance(node, ParameterRef):
                node = node.parameter  # get actual parameter

            if not isinstance(node, (LocalDegreeOfFreedom, Parameter)):
                raise Exception(
                    f"Input ({name}) input `{node}` should be a {LocalDegreeOfFreedom.__name__} or a component Parameter not a {type(node)}"
                )
            elif isinstance(node, Parameter):
                self.__drives[i] = LocalDegreeOfFreedom(
                    f"{self.name}.dofs.{node.full_name}", DC=node
                )
            elif node.AC_IN_type is not None and not (
                (
                    node.AC_IN_type == NodeType.ELECTRICAL
                    or node.AC_IN_type == NodeType.MECHANICAL
                )
            ):
                raise Exception(
                    f"Degree of freedom ({name}) input `{node}` should be an electrical or mechanical node"
                )
            elif node.AC_OUT_type is not None and not (
                (
                    node.AC_OUT_type is not None
                    and node.AC_OUT_type == NodeType.ELECTRICAL
                )
                or (
                    node.AC_OUT_type is not None
                    and node.AC_OUT_type == NodeType.MECHANICAL
                )
            ):
                raise Exception(
                    f"Degree of freedom ({name}) output `{node}` should be an electrical or mechanical node"
                )
            elif node.AC_OUT_type is not None or node.AC_IN_type is not None:
                add_AC = True
            else:
                pass  # no AC to drive or readout

        for amp in self.amplitudes:
            if not ((np.isscalar(amp) and np.real(amp)) or isinstance(amp, Symbol)):
                raise Exception(
                    f"Degree of freedom ({name}) amplitude `{amp}` is not a real number or a symbolic value"
                )

        self._add_port("AC", NodeType.ELECTRICAL)
        self.AC._add_node("i", NodeDirection.INPUT)
        self.AC._add_node("o", NodeDirection.OUTPUT)
        self._add_port("out", NodeType.ELECTRICAL)

        if add_AC:
            # Only add AC connections if there are some AC drives/readouts
            for i, node in enumerate(self.drives):
                if self.drives[i].AC_IN:
                    self.out._add_node(f"i{i}", None, node=self.drives[i].AC_IN)
                    self._register_node_coupling(
                        f"AC_in{i}", self.AC.i, self.drives[i].AC_IN
                    )

                if self.drives[i].AC_OUT:
                    self.out._add_node(f"o{i}", None, node=self.drives[i].AC_OUT)
                    self._register_node_coupling(
                        f"out{i}_AC", self.drives[i].AC_OUT, self.AC.o
                    )

    @property
    def node_amplitude_pairs(self):
        return tuple(roundrobin(self.drives, self.amplitudes))

    def _on_add(self, model):
        for dof in self.drives:
            if (dof.AC_IN is not None and model is not dof.AC_IN._model) and (
                dof.AC_OUT is not None and model is not dof.AC_OUT._model
            ):
                raise Exception(
                    f"{repr(self)} is using a node {self.node} from a different model"
                )
        # Setup this DOf to set itself as an external
        # setter for the DC parameters it injects into
        model._on_pre_build.append(self._pre_build)
        model._on_unbuild.append(self._on_unbuild)

    def _pre_build(self):
        # Set up the DC parameters to be controlled externally, by this DOF element
        for node, amp in zip(self.drives, self.amplitudes):
            dc_param = node.DC
            if dc_param is not None:
                # Here we set the DC parameter associated with a node to track the
                # value of the DC parameter of this DOF.
                # mark that this element will be controlling the value of this parameter
                node.DC.set_external_setter(self, amp * self.DC.ref)

    def _on_unbuild(self):
        # need to remove our
        for node, amp in zip(self.drives, self.amplitudes):
            dc_param = node.DC
            if dc_param is not None:
                node.DC.remove_external_setter(self, amp * self.DC.ref)

    @property
    def drives(self):
        ":getter: Returns The nodes this degree of freedom drives."
        return tuple(self.__drives)

    @property
    def amplitudes(self):
        ":getter: Returns the node amplitudes which a node is driven."
        return np.asarray(self.__amplitudes)

    @property
    def dc_enabled(self):
        """:getter: Returns True if all driving nodes have an associated DC parameter that can be varied."""
        return all((_.dc_parameter is not None for _ in self.drives))

    def _get_workspace(self, sim):
        if sim.signal:
            # Check if any of the drive amplitudes are changing because
            # they are symbolic
            refill = any(
                isinstance(a, Symbol) and a.is_changing for a in self.amplitudes
            )
            ws = DOFWorkspace(self, sim)
            ws.signal.add_fill_function(self.__fill, refill)
            ws.drives = self.drives
            ws.amplitudes = np.array(self.amplitudes)

            return ws
        else:
            return None

    def __fill(self, ws):
        for idx in range(len(ws.drives)):
            if hasattr(ws.signal.connections, "AC_in" + str(idx)):
                # Need to loop and determine if our connections have
                # been allocated or not
                mat_views = getattr(ws.signal.connections, "AC_in" + str(idx))
                if mat_views:
                    # All connections are just their amplitude value
                    # assumes no HOM couplings or anything between elec
                    # and mechanical nodes
                    if ws.drives[idx].AC_IN.type == NodeType.MECHANICAL:
                        mat_views[0][:] = (
                            ws.amplitudes[idx] / ws.sim.model_settings.x_scale
                        )
                    else:
                        mat_views[0][:] = ws.amplitudes[idx]

            if hasattr(ws.signal.connections, f"out{idx}_AC"):
                # fill drives to AC output node
                mat_views = getattr(ws.signal.connections, "out" + str(idx) + "_AC")
                if mat_views:
                    if ws.drives[idx].AC_OUT.type == NodeType.MECHANICAL:
                        mat_views[0][:] = (
                            ws.amplitudes[idx] * ws.sim.model_settings.x_scale
                        )
                    else:
                        mat_views[0][:] = ws.amplitudes[idx]
