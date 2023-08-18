import builtins as __builtin__

builtin_print = __builtin__.print

def my_print(*args, **kwargs):
    builtin_print("[Tuilts] ")
    builtin_print(*args, **kwargs)

__builtin__.print = my_print

print("test, in test_builtins")
