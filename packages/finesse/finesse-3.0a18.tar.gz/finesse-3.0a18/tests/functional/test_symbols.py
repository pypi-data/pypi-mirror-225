import finesse
import operator
import numpy as np
from functools import reduce
from itertools import permutations
from finesse.symbols import expand, collect, coefficient_and_term, Constant, expand_pow


def test_multiply_reordering():
    """Ensure multiplying 2,a,b in any order gives the same final result ordering."""
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        b = finesse.symbols.Variable("b")
        args = [2, a, b]
        for comb in permutations(args):
            assert reduce(operator.mul, comb) == 2 * a * b


def test_multiply_collect():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        args = [2, a, 4]
        for comb in permutations(args):
            assert reduce(operator.mul, comb) == 8 * a


def test_sum():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert str(a + b) == "(a+b)"


def test_sub():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert str(a - b) == "(a-b)"


def test_mul():
    a = finesse.symbols.Variable("a")
    b = finesse.symbols.Variable("b")
    assert str(a * b) == "(a*b)"
    assert str(2 * a * b) == "((2*a)*b)"


def test_numpy_fn():
    a = finesse.symbols.Variable("a")
    assert str(np.cos(a)) == "cos(a)"


def test_equality_sum():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        b = finesse.symbols.Variable("b")
        args = [2, a, b]
        for comb in permutations(args):
            assert np.sum(args) == 2 + a + b


def test_equality_mul():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        b = finesse.symbols.Variable("b")
        args = [2, a, b]
        for comb in permutations(args):
            assert np.prod(args) == 2 * a * b


def test_simplify():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        assert (
            3 / a - 2 * (4 * 1 / a - (-5 * 1 / a + 1.0))
        ).expand().collect() == 2 - 15 / a


def test_collect():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        b = finesse.symbols.Variable("b")
        assert collect(a * a) == a**2
        assert collect(a * a**-1) == 1
        assert collect(a - a) == 0
        assert collect(2 / a - 2 / a) == 0
        assert collect(-2 / a - 3 / a) == -5 / a
        assert collect(2 * 2 / a) == 4 / a
        assert collect(2 * (2 / a)) == 4 / a
        assert collect((1 + 2 / b) + (1 - 2 / b)) == 2
        assert collect(2 * a - a) == a
        assert collect(4 * a - 4 * a) == 0
        assert collect(-2 * a + a) == -a
        assert collect(a + a + 4) == 4 + 2 * a
        assert collect(a + 2 * a) == 3 * a
        assert collect(1.5 * a + 1.5 * a) == 3 * a
        assert collect(np.cos(a) + np.cos(a)) == 2 * np.cos(a)


def test_expand():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        b = finesse.symbols.Variable("b")
        assert -2 * a * b == -2 * a * b
        assert 2 * a * b == -2 * a * -b
        assert 2 * a * b == 2 * a * b
        assert a * 2 * b == 2 * a * b
        assert a * b * 2 == 2 * a * b
        assert expand(2 * a * (1 + b)) == 2 * a + 2 * a * b
        assert expand(2 * np.cos(a + b)) == 2 * np.cos(a + b)
        assert (
            expand(10 * np.cos(a) * (a + b)) == 10 * np.cos(a) * a + 10 * np.cos(a) * b
        )
        assert expand(3 * (1 + a) ** 2 * (2 + a) ** 2).collect() == (
            12 + 36 * a + 39 * (a) ** (2) + 18 * (a) ** (3) + 3 * (a) ** (4)
        )
        assert expand(2 / a - 6 / (3 * a)).collect() == 0


def test_expand_mul():
    from finesse.symbols import expand_mul

    a = finesse.symbols.Variable("a")
    # Shouldn't do anything to the expression here
    assert expand_mul(4 * a).args == [4, a]
    y = expand_mul(4 * a + a)
    assert y.args[0].args == [4, a]
    assert y.args[1] == a


def test_coefficient_and_term():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        b = finesse.symbols.Variable("b")
        assert coefficient_and_term(a) == (1, a)
        assert coefficient_and_term(2 * a) == (2, a)
        assert coefficient_and_term(a * b) == (1, a * b)
        assert coefficient_and_term(a + b) == (1, a + b)
        assert coefficient_and_term(Constant(3.3)) == (3.3, None)
        assert coefficient_and_term(np.cos(a)) == (1, np.cos(a))
        assert coefficient_and_term(3.3 * np.cos(a)) == (3.3, np.cos(a))


def test_expand_pow():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        assert expand_pow((2 * a) ** 2) == 4 * a**2
        assert (
            expand_pow(1 + (2 * a) ** 2 + 2 * (4 * a) ** 2).collect() == 1 + 36 * a**2
        )


def test_matrix_prods():
    from finesse.symbols import Matrix, Variable

    with finesse.symbols.simplification():
        A = Matrix("A")
        B = Matrix("B")
        a = Variable("a")
        assert (a * B * A * 2).args == [2, a, B, A]
        assert (a * B * A * 2 - 2 * a * B * A).collect() == 0


def test_nary_add_to_binary_add():
    from finesse.symbols import Variable, operator_add
    from operator import add

    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    with finesse.symbols.simplification():
        d = a + b + c

    assert d.op is operator_add
    assert d.args == [a, b, c]

    e = d.to_binary_add_mul()
    assert e.op is add
    assert e.args == [add(a, b), c]
    assert e.args[0].op is add
    assert e.args[0].args == [a, b]


def test_nary_mul_to_binary_add():
    from finesse.symbols import Variable, operator_mul
    from operator import mul

    a = Variable("a")
    b = Variable("b")
    c = Variable("c")

    with finesse.symbols.simplification():
        d = a * b * c

    assert d.op is operator_mul
    assert d.args == [a, b, c]

    e = d.to_binary_add_mul()
    assert e.op is mul
    assert e.args == [mul(a, b), c]
    assert e.args[0].op is mul
    assert e.args[0].args == [a, b]


def test_binary_to_nary_mul():
    from finesse.symbols import Variable, operator_mul
    from operator import mul

    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    d = a * b * c

    assert d.op is mul
    assert d.args == [mul(a, b), c]

    e = d.to_nary_add_mul()
    assert e.op is operator_mul
    assert e.args == [a, b, c]


def test_binary_to_nary_add():
    from finesse.symbols import Variable, operator_add
    from operator import add

    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    d = a + b + c

    assert d.op is add
    assert d.args == [add(a, b), c]

    e = d.to_nary_add_mul()
    assert e.op is operator_add
    assert e.args == [a, b, c]


def test_equality_add():
    from finesse.symbols import Variable

    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    d = a + 20 + b + c
    assert (d.value.collect() - 10).collect() == (10 + a + b + c)
    assert (d.value.collect() - 10).collect() == (10 + b + a + c)


def test_constant():
    y = Constant(1) + Constant(4)
    assert y == 5
    # should retain operator without simplification
    assert y.op == operator.add

    y = Constant(1) * Constant(4)
    assert y == 4
    assert y.op == operator.mul

    with finesse.symbols.simplification():
        # Results should be the same but more simplification
        # should happen, end up with a reduced constant
        y = Constant(1) + Constant(4)
        assert y == 5
        assert type(y) == Constant

        y = Constant(1) * Constant(4)
        assert y == 4
        assert type(y) == Constant


def test_named_constant_collect():
    pi = finesse.symbols.CONSTANTS["pi"]
    y = pi + pi
    assert y.collect() == 2 * pi


def test_nary_keep_named_constants_add():
    pi = finesse.symbols.CONSTANTS["pi"]
    y = 2 + pi + pi
    z = y.to_nary_add_mul()
    assert z.args == [2, pi, pi]


def test_nary_keep_named_constants_mul():
    pi = finesse.symbols.CONSTANTS["pi"]
    y = 2 * pi
    assert y.to_nary_add_mul() == 2 * pi


def test_nary_keep_named_constants_pow():
    pi = finesse.symbols.CONSTANTS["pi"]
    y = pi * 2 * pi
    assert y.to_nary_add_mul() == 2 * pi**2


def test_param_ref_equality():
    # issue 514
    model = finesse.script.parse("var test 1e-3")
    assert (model.test.ref == model.test.ref) is True
    assert (-model.test.ref == model.test.ref) is False
    assert (model.test.ref == -model.test.ref) is False
    assert (model.test.ref == -(-model.test.ref)) is True
    assert (-(-model.test.ref) == model.test.ref) is True


def test_function_arg_expand_collect():
    with finesse.symbols.simplification():
        a = finesse.symbols.Variable("a")
        assert np.cos(a + a).collect().args == [2 * a]
        assert np.cos(2 * (a + a)).collect().args == [4 * a]
        assert np.cos(2 * (a + a) - 4 * a).expand().collect() == 1


def test_aligo_path_eval():
    # Seems that some complicated expressions don't eval fully. This tests that
    # this case does.
    model = finesse.Model()
    model.parse(
        """
    variable f1 9099471
    variable f2 5*f1
    variable nsilica 1.45
    variable Mloss 30u

    ###############################################################################
    ###   length definitions
    ###############################################################################
    variable Larm 3994.47
    variable LPR23 16.164  # distance between PR2 and PR3
    variable LSR23 15.443  # distance between SR2 and SR3
    variable LPR3BS 19.538 # distance between PR3 and BS
    variable LSR3BS 19.366 # distance between SR3 and BS
    variable lmich 5.342   # average length of MICH
    variable lschnupp 0.08 # double pass schnupp length
    variable lPRC (3+0.5)*c0/(2*f1) # T1000298 Eq2.1, N=3
    variable lSRC (17)*c0/(2*f2) # T1000298 Eq2.2, M=3

    ###############################################################################
    ###   PRC
    ###############################################################################

    m PRMAR R=0 L=40u xbeta=PRM.xbeta ybeta=PRM.ybeta phi=PRM.phi
    s sPRMsub1 PRMAR.p2 PRM.p1 L=0.0737 nr=nsilica
    m PRM T=0.03 L=8.5u Rc=11.009
    s lp1 PRM.p2 PR2.p1 L=lPRC-LPR3BS-LPR23-lmich
    bs PR2 T=250u L=Mloss alpha=-0.79 Rc=-4.545
    s lp2 PR2.p2 PR3.p1 L=LPR23
    bs PR3 T=0 L=Mloss alpha=0.615 Rc=36.027
    s lp3 PR3.p2 BS.p1 L=LPR3BS

    ###############################################################################
    ###   BS
    ###############################################################################
    bs BS R=0.5 L=Mloss alpha=45
    s BSsub1 BS.p3 BSAR1.p1 L=60m/cos(radians(BSAR1.alpha)) nr=nsilica
    s BSsub2 BS.p4 BSAR2.p2 L=60m/cos(radians(BSAR1.alpha)) nr=nsilica
    bs BSAR1 L=50u R=0 alpha=-29.186885954108114
    bs BSAR2 L=50u R=0 alpha=BSAR1.alpha

    ###############################################################################
    ###   Xarm
    ###############################################################################
    # Distance from beam splitter to X arm input mirror
    s lx1 BSAR1.p3 ITMXlens.p1 L=lmich+lschnupp/2-ITMXsub.L*ITMXsub.nr-BSsub1.L*BSsub1.nr
    lens ITMXlens f=34500
    s lx2 ITMXlens.p2 ITMXAR.p1
    m ITMXAR R=0 L=20u xbeta=ITMX.xbeta ybeta=ITMX.ybeta phi=ITMX.phi
    s ITMXsub ITMXAR.p2 ITMX.p1 L=0.2 nr=nsilica
    m ITMX T=0.014 L=Mloss Rc=-1934
    s LX ITMX.p2 ETMX.p1 L=Larm
    m ETMX T=5u L=Mloss Rc=2245
    s ETMXsub ETMX.p2 ETMXAR.p1 L=0.2 nr=nsilica
    m ETMXAR 0 500u xbeta=ETMX.xbeta ybeta=ETMX.ybeta phi=ETMX.phi
    """
    )
    path = model.path("PRM.p2.o", "ITMX.p1.i")
    y = sum(s.L * s.nr for s in path.spaces)
    # just check that indeed a float is returned when eval'd
    assert type(y.eval()) == np.float64
