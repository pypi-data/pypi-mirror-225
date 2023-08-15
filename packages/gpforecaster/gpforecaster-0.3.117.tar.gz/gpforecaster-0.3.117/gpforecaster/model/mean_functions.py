import gpytorch
import torch


class LinearMean(gpytorch.means.Mean):
    def __init__(self, input_size, batch_shape=torch.Size(), bias=True):
        super().__init__()
        self.register_parameter(
            name="weights",
            parameter=torch.nn.Parameter(torch.randn(*batch_shape, input_size, 1)),
        )
        if bias:
            self.register_parameter(
                name="bias", parameter=torch.nn.Parameter(torch.randn(*batch_shape, 1))
            )
        else:
            self.bias = None

    def forward(self, x):
        x = x.float()
        res = x.matmul(self.weights).squeeze(-1)
        if self.bias is not None:
            res = res + self.bias

        return res


class PiecewiseLinearMean(gpytorch.means.Mean):
    def __init__(self, changepoints, device, k, m, b, random_init):
        super().__init__()
        self.device = device
        self.changepoints = changepoints
        if random_init:
            k = torch.rand(1).reshape((1, 1))
            m = torch.rand(1).reshape((1, 1))
            b = torch.rand(1)
        self.register_parameter(name="k", parameter=torch.nn.Parameter(k))
        self.register_parameter(name="m", parameter=torch.nn.Parameter(m))
        self.register_parameter(
            name="b",
            parameter=torch.nn.Parameter(torch.tile(b, (len(changepoints),))),
        )

    def forward(self, x):
        x = x.to(device=self.device).float()
        A = (
            0.5
            * (
                1.0
                + torch.sgn(torch.tile(x.reshape((-1, 1)), (1, 4)) - self.changepoints)
            )
        ).float()

        b = self.b.to(device=self.device)
        k = self.k.to(device=self.device)
        m = self.m.to(device=self.device)

        res = (k + torch.matmul(A, b.reshape((-1, 1)))) * x + (
            m + torch.matmul(A, (-self.changepoints.float() * b))
        ).reshape(-1, 1)

        return res.reshape((-1,))
