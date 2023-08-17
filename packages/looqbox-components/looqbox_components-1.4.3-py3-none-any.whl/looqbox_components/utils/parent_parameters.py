# function wrapper to increment a function parameters with not initialized parameters
import inspect


def include_extra_parent_params(func):
    def wrapper(self):
        # get the function parameters
        cls_init_method = self.__class__.__init__
        init_params = dict(inspect.signature(cls_init_method).parameters)
        # get the class parameters
        class_params = vars(self)
        # get the class parameters that are not in the function parameters
        extra_params = {k: v for k, v in class_params.items() if k not in init_params}
        # update the function parameters with the extra parameters
        self.parent_params.update(extra_params)
        # call the function with the updated parameters
        return func(self)

    return wrapper
