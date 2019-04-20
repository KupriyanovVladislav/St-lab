class D:
    x = 2


class C(D):
    pass


class B(D):
    x = 1


class E(B, C):
    pass


class A(E):
    pass
