from tensorflow.python.util.deprecation import deprecated_endpoints as deprecated_endpoints
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

def apply_ada_max(var, m, v, beta1_power, lr, beta1, beta2, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ApplyAdaMax: Any

def apply_ada_max_eager_fallback(var, m, v, beta1_power, lr, beta1, beta2, epsilon, grad, use_locking, name, ctx) -> None: ...
def apply_adadelta(var, accum, accum_update, lr, rho, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ApplyAdadelta: Any

def apply_adadelta_eager_fallback(var, accum, accum_update, lr, rho, epsilon, grad, use_locking, name, ctx) -> None: ...
def apply_adagrad(var, accum, lr, grad, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

ApplyAdagrad: Any

def apply_adagrad_eager_fallback(var, accum, lr, grad, use_locking, update_slots, name, ctx) -> None: ...
def apply_adagrad_da(var, gradient_accumulator, gradient_squared_accumulator, grad, lr, l1, l2, global_step, use_locking: bool = ..., name: Any | None = ...): ...

ApplyAdagradDA: Any

def apply_adagrad_da_eager_fallback(var, gradient_accumulator, gradient_squared_accumulator, grad, lr, l1, l2, global_step, use_locking, name, ctx) -> None: ...
def apply_adagrad_v2(var, accum, lr, epsilon, grad, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

ApplyAdagradV2: Any

def apply_adagrad_v2_eager_fallback(var, accum, lr, epsilon, grad, use_locking, update_slots, name, ctx) -> None: ...
def apply_adam(var, m, v, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

ApplyAdam: Any

def apply_adam_eager_fallback(var, m, v, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, use_locking, use_nesterov, name, ctx) -> None: ...
def apply_add_sign(var, m, lr, alpha, sign_decay, beta, grad, use_locking: bool = ..., name: Any | None = ...): ...

ApplyAddSign: Any

def apply_add_sign_eager_fallback(var, m, lr, alpha, sign_decay, beta, grad, use_locking, name, ctx) -> None: ...
def apply_centered_rms_prop(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ApplyCenteredRMSProp: Any

def apply_centered_rms_prop_eager_fallback(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, use_locking, name, ctx) -> None: ...
def apply_ftrl(var, accum, linear, grad, lr, l1, l2, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

ApplyFtrl: Any

def apply_ftrl_eager_fallback(var, accum, linear, grad, lr, l1, l2, lr_power, use_locking, multiply_linear_by_lr, name, ctx) -> None: ...
def apply_ftrl_v2(var, accum, linear, grad, lr, l1, l2, l2_shrinkage, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

ApplyFtrlV2: Any

def apply_ftrl_v2_eager_fallback(var, accum, linear, grad, lr, l1, l2, l2_shrinkage, lr_power, use_locking, multiply_linear_by_lr, name, ctx) -> None: ...
def apply_gradient_descent(var, alpha, delta, use_locking: bool = ..., name: Any | None = ...): ...

ApplyGradientDescent: Any

def apply_gradient_descent_eager_fallback(var, alpha, delta, use_locking, name, ctx) -> None: ...
def apply_momentum(var, accum, lr, grad, momentum, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

ApplyMomentum: Any

def apply_momentum_eager_fallback(var, accum, lr, grad, momentum, use_locking, use_nesterov, name, ctx) -> None: ...
def apply_power_sign(var, m, lr, logbase, sign_decay, beta, grad, use_locking: bool = ..., name: Any | None = ...): ...

ApplyPowerSign: Any

def apply_power_sign_eager_fallback(var, m, lr, logbase, sign_decay, beta, grad, use_locking, name, ctx) -> None: ...
def apply_proximal_adagrad(var, accum, lr, l1, l2, grad, use_locking: bool = ..., name: Any | None = ...): ...

ApplyProximalAdagrad: Any

def apply_proximal_adagrad_eager_fallback(var, accum, lr, l1, l2, grad, use_locking, name, ctx) -> None: ...
def apply_proximal_gradient_descent(var, alpha, l1, l2, delta, use_locking: bool = ..., name: Any | None = ...): ...

ApplyProximalGradientDescent: Any

def apply_proximal_gradient_descent_eager_fallback(var, alpha, l1, l2, delta, use_locking, name, ctx) -> None: ...
def apply_rms_prop(var, ms, mom, lr, rho, momentum, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ApplyRMSProp: Any

def apply_rms_prop_eager_fallback(var, ms, mom, lr, rho, momentum, epsilon, grad, use_locking, name, ctx) -> None: ...
def resource_apply_ada_max(var, m, v, beta1_power, lr, beta1, beta2, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyAdaMax: Any

def resource_apply_ada_max_eager_fallback(var, m, v, beta1_power, lr, beta1, beta2, epsilon, grad, use_locking, name, ctx): ...
def resource_apply_adadelta(var, accum, accum_update, lr, rho, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyAdadelta: Any

def resource_apply_adadelta_eager_fallback(var, accum, accum_update, lr, rho, epsilon, grad, use_locking, name, ctx): ...
def resource_apply_adagrad(var, accum, lr, grad, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

ResourceApplyAdagrad: Any

def resource_apply_adagrad_eager_fallback(var, accum, lr, grad, use_locking, update_slots, name, ctx): ...
def resource_apply_adagrad_da(var, gradient_accumulator, gradient_squared_accumulator, grad, lr, l1, l2, global_step, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyAdagradDA: Any

def resource_apply_adagrad_da_eager_fallback(var, gradient_accumulator, gradient_squared_accumulator, grad, lr, l1, l2, global_step, use_locking, name, ctx): ...
def resource_apply_adagrad_v2(var, accum, lr, epsilon, grad, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

ResourceApplyAdagradV2: Any

def resource_apply_adagrad_v2_eager_fallback(var, accum, lr, epsilon, grad, use_locking, update_slots, name, ctx): ...
def resource_apply_adam(var, m, v, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

ResourceApplyAdam: Any

def resource_apply_adam_eager_fallback(var, m, v, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, use_locking, use_nesterov, name, ctx): ...
def resource_apply_adam_with_amsgrad(var, m, v, vhat, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyAdamWithAmsgrad: Any

def resource_apply_adam_with_amsgrad_eager_fallback(var, m, v, vhat, beta1_power, beta2_power, lr, beta1, beta2, epsilon, grad, use_locking, name, ctx): ...
def resource_apply_add_sign(var, m, lr, alpha, sign_decay, beta, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyAddSign: Any

def resource_apply_add_sign_eager_fallback(var, m, lr, alpha, sign_decay, beta, grad, use_locking, name, ctx): ...
def resource_apply_centered_rms_prop(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyCenteredRMSProp: Any

def resource_apply_centered_rms_prop_eager_fallback(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, use_locking, name, ctx): ...
def resource_apply_ftrl(var, accum, linear, grad, lr, l1, l2, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

ResourceApplyFtrl: Any

def resource_apply_ftrl_eager_fallback(var, accum, linear, grad, lr, l1, l2, lr_power, use_locking, multiply_linear_by_lr, name, ctx): ...
def resource_apply_ftrl_v2(var, accum, linear, grad, lr, l1, l2, l2_shrinkage, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

ResourceApplyFtrlV2: Any

def resource_apply_ftrl_v2_eager_fallback(var, accum, linear, grad, lr, l1, l2, l2_shrinkage, lr_power, use_locking, multiply_linear_by_lr, name, ctx): ...
def resource_apply_gradient_descent(var, alpha, delta, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyGradientDescent: Any

def resource_apply_gradient_descent_eager_fallback(var, alpha, delta, use_locking, name, ctx): ...
def resource_apply_keras_momentum(var, accum, lr, grad, momentum, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

ResourceApplyKerasMomentum: Any

def resource_apply_keras_momentum_eager_fallback(var, accum, lr, grad, momentum, use_locking, use_nesterov, name, ctx): ...
def resource_apply_momentum(var, accum, lr, grad, momentum, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

ResourceApplyMomentum: Any

def resource_apply_momentum_eager_fallback(var, accum, lr, grad, momentum, use_locking, use_nesterov, name, ctx): ...
def resource_apply_power_sign(var, m, lr, logbase, sign_decay, beta, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyPowerSign: Any

def resource_apply_power_sign_eager_fallback(var, m, lr, logbase, sign_decay, beta, grad, use_locking, name, ctx): ...
def resource_apply_proximal_adagrad(var, accum, lr, l1, l2, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyProximalAdagrad: Any

def resource_apply_proximal_adagrad_eager_fallback(var, accum, lr, l1, l2, grad, use_locking, name, ctx): ...
def resource_apply_proximal_gradient_descent(var, alpha, l1, l2, delta, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyProximalGradientDescent: Any

def resource_apply_proximal_gradient_descent_eager_fallback(var, alpha, l1, l2, delta, use_locking, name, ctx): ...
def resource_apply_rms_prop(var, ms, mom, lr, rho, momentum, epsilon, grad, use_locking: bool = ..., name: Any | None = ...): ...

ResourceApplyRMSProp: Any

def resource_apply_rms_prop_eager_fallback(var, ms, mom, lr, rho, momentum, epsilon, grad, use_locking, name, ctx): ...
def resource_sparse_apply_adadelta(var, accum, accum_update, lr, rho, epsilon, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyAdadelta: Any

def resource_sparse_apply_adadelta_eager_fallback(var, accum, accum_update, lr, rho, epsilon, grad, indices, use_locking, name, ctx): ...
def resource_sparse_apply_adagrad(var, accum, lr, grad, indices, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyAdagrad: Any

def resource_sparse_apply_adagrad_eager_fallback(var, accum, lr, grad, indices, use_locking, update_slots, name, ctx): ...
def resource_sparse_apply_adagrad_da(var, gradient_accumulator, gradient_squared_accumulator, grad, indices, lr, l1, l2, global_step, use_locking: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyAdagradDA: Any

def resource_sparse_apply_adagrad_da_eager_fallback(var, gradient_accumulator, gradient_squared_accumulator, grad, indices, lr, l1, l2, global_step, use_locking, name, ctx): ...
def resource_sparse_apply_adagrad_v2(var, accum, lr, epsilon, grad, indices, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyAdagradV2: Any

def resource_sparse_apply_adagrad_v2_eager_fallback(var, accum, lr, epsilon, grad, indices, use_locking, update_slots, name, ctx): ...
def resource_sparse_apply_centered_rms_prop(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyCenteredRMSProp: Any

def resource_sparse_apply_centered_rms_prop_eager_fallback(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking, name, ctx): ...
def resource_sparse_apply_ftrl(var, accum, linear, grad, indices, lr, l1, l2, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyFtrl: Any

def resource_sparse_apply_ftrl_eager_fallback(var, accum, linear, grad, indices, lr, l1, l2, lr_power, use_locking, multiply_linear_by_lr, name, ctx): ...
def resource_sparse_apply_ftrl_v2(var, accum, linear, grad, indices, lr, l1, l2, l2_shrinkage, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyFtrlV2: Any

def resource_sparse_apply_ftrl_v2_eager_fallback(var, accum, linear, grad, indices, lr, l1, l2, l2_shrinkage, lr_power, use_locking, multiply_linear_by_lr, name, ctx): ...
def resource_sparse_apply_keras_momentum(var, accum, lr, grad, indices, momentum, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyKerasMomentum: Any

def resource_sparse_apply_keras_momentum_eager_fallback(var, accum, lr, grad, indices, momentum, use_locking, use_nesterov, name, ctx): ...
def resource_sparse_apply_momentum(var, accum, lr, grad, indices, momentum, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyMomentum: Any

def resource_sparse_apply_momentum_eager_fallback(var, accum, lr, grad, indices, momentum, use_locking, use_nesterov, name, ctx): ...
def resource_sparse_apply_proximal_adagrad(var, accum, lr, l1, l2, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyProximalAdagrad: Any

def resource_sparse_apply_proximal_adagrad_eager_fallback(var, accum, lr, l1, l2, grad, indices, use_locking, name, ctx): ...
def resource_sparse_apply_proximal_gradient_descent(var, alpha, l1, l2, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyProximalGradientDescent: Any

def resource_sparse_apply_proximal_gradient_descent_eager_fallback(var, alpha, l1, l2, grad, indices, use_locking, name, ctx): ...
def resource_sparse_apply_rms_prop(var, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

ResourceSparseApplyRMSProp: Any

def resource_sparse_apply_rms_prop_eager_fallback(var, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking, name, ctx): ...
def sparse_apply_adadelta(var, accum, accum_update, lr, rho, epsilon, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

SparseApplyAdadelta: Any

def sparse_apply_adadelta_eager_fallback(var, accum, accum_update, lr, rho, epsilon, grad, indices, use_locking, name, ctx) -> None: ...
def sparse_apply_adagrad(var, accum, lr, grad, indices, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

SparseApplyAdagrad: Any

def sparse_apply_adagrad_eager_fallback(var, accum, lr, grad, indices, use_locking, update_slots, name, ctx) -> None: ...
def sparse_apply_adagrad_da(var, gradient_accumulator, gradient_squared_accumulator, grad, indices, lr, l1, l2, global_step, use_locking: bool = ..., name: Any | None = ...): ...

SparseApplyAdagradDA: Any

def sparse_apply_adagrad_da_eager_fallback(var, gradient_accumulator, gradient_squared_accumulator, grad, indices, lr, l1, l2, global_step, use_locking, name, ctx) -> None: ...
def sparse_apply_adagrad_v2(var, accum, lr, epsilon, grad, indices, use_locking: bool = ..., update_slots: bool = ..., name: Any | None = ...): ...

SparseApplyAdagradV2: Any

def sparse_apply_adagrad_v2_eager_fallback(var, accum, lr, epsilon, grad, indices, use_locking, update_slots, name, ctx) -> None: ...
def sparse_apply_centered_rms_prop(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

SparseApplyCenteredRMSProp: Any

def sparse_apply_centered_rms_prop_eager_fallback(var, mg, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking, name, ctx) -> None: ...
def sparse_apply_ftrl(var, accum, linear, grad, indices, lr, l1, l2, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

SparseApplyFtrl: Any

def sparse_apply_ftrl_eager_fallback(var, accum, linear, grad, indices, lr, l1, l2, lr_power, use_locking, multiply_linear_by_lr, name, ctx) -> None: ...
def sparse_apply_ftrl_v2(var, accum, linear, grad, indices, lr, l1, l2, l2_shrinkage, lr_power, use_locking: bool = ..., multiply_linear_by_lr: bool = ..., name: Any | None = ...): ...

SparseApplyFtrlV2: Any

def sparse_apply_ftrl_v2_eager_fallback(var, accum, linear, grad, indices, lr, l1, l2, l2_shrinkage, lr_power, use_locking, multiply_linear_by_lr, name, ctx) -> None: ...
def sparse_apply_momentum(var, accum, lr, grad, indices, momentum, use_locking: bool = ..., use_nesterov: bool = ..., name: Any | None = ...): ...

SparseApplyMomentum: Any

def sparse_apply_momentum_eager_fallback(var, accum, lr, grad, indices, momentum, use_locking, use_nesterov, name, ctx) -> None: ...
def sparse_apply_proximal_adagrad(var, accum, lr, l1, l2, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

SparseApplyProximalAdagrad: Any

def sparse_apply_proximal_adagrad_eager_fallback(var, accum, lr, l1, l2, grad, indices, use_locking, name, ctx) -> None: ...
def sparse_apply_proximal_gradient_descent(var, alpha, l1, l2, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

SparseApplyProximalGradientDescent: Any

def sparse_apply_proximal_gradient_descent_eager_fallback(var, alpha, l1, l2, grad, indices, use_locking, name, ctx) -> None: ...
def sparse_apply_rms_prop(var, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking: bool = ..., name: Any | None = ...): ...

SparseApplyRMSProp: Any

def sparse_apply_rms_prop_eager_fallback(var, ms, mom, lr, rho, momentum, epsilon, grad, indices, use_locking, name, ctx) -> None: ...
