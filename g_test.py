class MyClass:
    def __getattr__(self, attr):
        print(3)
        if attr.startswith('__') and attr.endswith('__'):
            print(5)
            # Handle special attributes (e.g., __call__, __getattr__)
            return super().__getattr__(attr)
        print(8)
        new_instance = MyClass()
        print(10)
        new_instance._attribute = attr
        print(12)
        return new_instance

    def __call__(self, *args, **kwargs):
        print(16)
        print(*args)
        if hasattr(self, '_attribute'):
            print(18)
            return self._attribute + "()"
        print(20)
        return f"{self.__class__.__name__}()"


class_instance = MyClass()

print(class_instance.test())         # Output: test()
print(class_instance.nested.function())  # Output: nested.function()
