
def solve(Pf, U0):

    while norm(Pf - Model.force(U)) > tol:
        dU = linalg.solve(Model.tangent(U), Pf - Model.force(U))
        U = U + dU
        save(dU)


def analyze(ns, Pref):
    for n in range(ns):
        U = solve(Pref*n, U0=U)
        save(U)


class truss:
    def update(u, du):
        self.rot  = exp(du)*self.rot

        self.k = EA/L*[[ 1, -1],
                        -1,  1]]

        self.kg = a(u).T@k@a(u)
        
        self.p = a(u).T@k@a(u)@u

    def force(self, u, du):
        self.update(u, du)
        return self.p

    def tangent(self):
        return self.kg

    return p

