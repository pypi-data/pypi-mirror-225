import finesse


# Note: this tests a deprecated method. Remove eventually!
def test_phase_level_change():
    # Issue 506
    model = finesse.Model()
    model.phase_level = 1
    assert model.phase_level == 1
    model.phase_level = 2
    assert model.phase_level == 2


def test_get_string():
    model1 = finesse.Model()
    model1.parse("m m1")
    model1.parse("gauss g1 m1.p1.o w=1 Rc=1")
    model1.beam_trace()

    assert model1.m1 is model1.get("m1")
    assert model1.m1 is model1.get_element("m1")

    assert model1.m1.p1 is model1.get("m1.p1")
    assert model1.m1.p2 is model1.get("m1.p2")

    assert model1.m1.p2.i is model1.get("m1.p2.i")
    assert model1.m1.p2.o is model1.get("m1.p2.o")

    assert model1.m1.p2.i.qx is model1.get("m1.p2.i.qx")
    assert model1.m1.p2.i.qy is model1.get("m1.p2.i.qy")
    assert model1.m1.p2.o.qx is model1.get("m1.p2.o.qx")
    assert model1.m1.p2.o.qy is model1.get("m1.p2.o.qy")

    assert model1.m1.R is model1.get("m1.R")
    assert model1.m1.T is model1.get("m1.T")


def test_get_other_model():
    model1 = finesse.Model()
    model1.parse("m m1")

    model2 = finesse.Model()
    model2.parse("m m1")

    assert model1.m1 is model1.get(model2.m1)
    assert model1.m1 is model1.get_element(model2.m1)

    assert model1.m1.p1 is model1.get(model2.m1.p1)
    assert model1.m1.p2 is model1.get(model2.m1.p2)

    assert model1.m1.p2.i is model1.get(model2.m1.p2.i)
    assert model1.m1.p2.o is model1.get(model2.m1.p2.o)

    assert model1.m1.R is model1.get(model2.m1.R)
    assert model1.m1.T is model1.get(model2.m1.T)
