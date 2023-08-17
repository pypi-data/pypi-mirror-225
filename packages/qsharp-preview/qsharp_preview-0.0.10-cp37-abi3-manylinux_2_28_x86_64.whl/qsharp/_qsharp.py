# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from ._native import Interpreter, TargetProfile

_interpreter = None


def init(target_profile: TargetProfile = TargetProfile.Full) -> None:
    """
    Initializes the Q# interpreter.

    :param target_profile: Setting the target profile allows the Q#
        interpreter to generate programs that are compatible
        with a specific target. See :py:class: `qsharp.TargetProfile`.
    """
    global _interpreter
    _interpreter = Interpreter(target_profile)


def get_interpreter() -> Interpreter:
    """
    Returns the Q# interpreter.

    :returns: The Q# interpreter.
    """
    global _interpreter
    if _interpreter is None:
        raise RuntimeError(
            "Q# interpreter not initialized. Call qsharp.init() with any desired configuration settings first."
        )
    return _interpreter


def eval(source):
    """
    Evaluates Q# source code.

    Output is printed to console.

    :param source: The Q# source code to evaluate.
    :returns value: The value returned by the last statement in the source code.
    :raises QSharpError: If there is an error evaluating the source code.
    """

    def callback(output):
        print(output)

    return get_interpreter().interpret(source, callback)


def eval_file(path) -> None:
    """
    Reads Q# source code from a file and evaluates it.

    :param path: The path to the Q# source file.
    :returns: The value returned by the last statement in the file.
    :raises: QSharpError
    """
    f = open(path, mode="r", encoding="utf-8")
    return eval(f.read())


def eval_with_shots(entry_expr, shots):
    """
    Runs a Q# program a given number of times (shots). Each shot is run
    in an environment that is isolated from the other shots.

    :param entry_expr: The Q# expression that will be used as the entrypoint
        for the program.
    :returns values: An array of values returned by each shot. If the shot raised
        a runtime error, the array will contain an error object for that shot.
    :raises QSharpError: If there is an error evaluating the source code.
    """

    def callback(output):
        print(output)

    return _interpreter.eval_with_shots(entry_expr, shots, callback)


def compile(entry_expr):
    """
    Compiles the Q# source code into a program that can be submitted to a target.

    :param entry_expr: The Q# expression that will be used as the entrypoint
        for the program.
    """
    ll_str = get_interpreter().qir(entry_expr)
    return QirInputData("main", ll_str)


# Class that wraps generated QIR, which can be used by
# azure-quantum as input data.
#
# This class must implement the QirRepresentable protocol
# that is defined by the azure-quantum package.
# See: https://github.com/microsoft/qdk-python/blob/fcd63c04aa871e49206703bbaa792329ffed13c4/azure-quantum/azure/quantum/target/target.py#L21
class QirInputData:
    # The name of this variable is defined
    # by the protocol and must remain unchanged.
    _name: str

    def __init__(self, name: str, ll_str: str):
        self._name = name
        self._ll_str = ll_str

    # The name of this method is defined
    # by the protocol and must remain unchanged.
    def _repr_qir_(self, **kwargs) -> bytes:
        return self._ll_str.encode("utf-8")
