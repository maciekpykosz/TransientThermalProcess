shape_fun_2d = (lambda ksi, eta: 0.25 * (1. - ksi) * (1. - eta),
                lambda ksi, eta: 0.25 * (1. + ksi) * (1. - eta),
                lambda ksi, eta: 0.25 * (1. + ksi) * (1. + eta),
                lambda ksi, eta: 0.25 * (1. - ksi) * (1. + eta))

shape_fun_dksi_2d = (lambda ksi, eta: -0.25 * (1 - eta),
                     lambda ksi, eta: 0.25 * (1 - eta),
                     lambda ksi, eta: 0.25 * (1 + eta),
                     lambda ksi, eta: -0.25 * (1 + eta))

shape_fun_deta_2d = (lambda ksi, eta: -0.25 * (1 - ksi),
                     lambda ksi, eta: -0.25 * (1 + ksi),
                     lambda ksi, eta: 0.25 * (1 + ksi),
                     lambda ksi, eta: 0.25 * (1 - ksi))
