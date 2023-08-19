from attribution_quality.utils import getattr_recursive


class ActsAndGrads:
    """Hook class to catch the activation maps and gradients for the target model layers"""
    def __init__(self, model, target_layers, save_gradients=True):
        self.model = model
        self.gradients = []
        self.activations = []
        self.handles = []
        self.target_layers = [] if target_layers is None else target_layers
        self.target_layers = [getattr_recursive(self.model, layer) if isinstance(layer, str) else layer for layer in self.target_layers]
        self.active = False
        self.save_gradients = save_gradients

    def save_activation(self, module, input, output):
        self.activations.append(output.cpu().detach())

    def save_gradient(self, module, input, output):
        if not hasattr(output, "requires_grad") or not output.requires_grad:
            return

        def _store_grad(grad):
            self.gradients = [grad.cpu().detach()] + self.gradients
        output.register_hook(_store_grad)

    def __call__(self, x):
        if not self.active:
            raise ValueError("ActsAndGrads is not active. Call start() first.")
        return self.model(x)

    def start(self):
        if self.active:
            self.release()
        for target_layer in self.target_layers:
            self.handles.append(target_layer.register_forward_hook(self.save_activation))
            # Gradients have to use forward hooks: https://github.com/pytorch/pytorch/issues/61519,
            if self.save_gradients:
                self.handles.append(target_layer.register_forward_hook(self.save_gradient))
        self.gradients = []
        self.activations = []
        self.active = True

    def release(self):
        self.gradients = []
        self.activations = []
        for handle in self.handles:
            handle.remove()
        self.active = False

    def __del__(self):
        self.release()
