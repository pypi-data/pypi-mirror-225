import torch
import gpytorch

from gpytorch.models import ExactGP
from gpytorch.models import ApproximateGP
from gpytorch.variational import CholeskyVariationalDistribution
from gpytorch.variational import VariationalStrategy
from gpytorch.kernels import InducingPointKernel


class ExactGPModel(ExactGP):
    def __init__(
        self,
        train_x,
        train_y,
        likelihood,
        cov,
        changepoints,
        mean_func,
        device,
        m,
        k,
        b,
        random_init,
    ):
        super().__init__(train_x, train_y, likelihood)
        self.changepoints = changepoints
        self.mean_module = mean_func(
            changepoints=self.changepoints,
            device=device,
            m=m,
            k=k,
            b=b,
            random_init=random_init,
        )
        self.covar_module = cov

    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)


class SparseGPModel(ExactGP):
    def __init__(
        self,
        train_x,
        train_y,
        likelihood,
        cov,
        changepoints,
        mean_func,
        inducing_points,
        device,
        m,
        k,
        b,
        random_init,
    ):
        super().__init__(train_x, train_y, likelihood)
        self.changepoints = changepoints
        self.mean_module = mean_func(
            changepoints=self.changepoints,
            device=device,
            m=m,
            k=k,
            b=b,
            random_init=random_init,
        )
        # Use an InducingPointKernel instead of a standard kernel
        self.covar_module = InducingPointKernel(
            cov, inducing_points=inducing_points, likelihood=likelihood
        )

    def forward(self, x):
        mean_x = self.mean_module(x).to(torch.float32)
        covar_x = self.covar_module(x).to(torch.float32)
        return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)


class SvgGPModel(ApproximateGP):
    def __init__(
        self,
        train_x,
        train_y,
        likelihood,
        cov,
        changepoints,
        mean_func,
        inducing_points,
        device,
        m,
        k,
        b,
        random_init,
    ):
        variational_distribution = CholeskyVariationalDistribution(
            inducing_points.size(0)
        ).to(torch.float32)
        variational_strategy = VariationalStrategy(
            self,
            inducing_points=inducing_points,
            variational_distribution=variational_distribution,
            learn_inducing_locations=True,
        )
        super(SvgGPModel, self).__init__(variational_strategy)
        self.train_inputs = train_x
        self.train_targets = train_y
        self.changepoints = changepoints
        self.mean_module = mean_func(
            changepoints=self.changepoints,
            device=device,
            m=m,
            k=k,
            b=b,
            random_init=random_init,
        )
        self.covar_module = cov
        self.likelihood = likelihood

    def forward(self, x):
        if x.requires_grad:
            x = x.detach()
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)
