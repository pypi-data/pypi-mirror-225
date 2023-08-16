from cave_utils import Arguments

args = Arguments()

print(args.kwargs)
print(args.flags)
print(args.other)

print(args.get_kwarg("test", "default"))

args.delete("test", only_flag=True)

args.delete("abc")

print(args.kwargs)
print(args.flags)
print(args.other)

print(args.get_kwarg("test", "default"))