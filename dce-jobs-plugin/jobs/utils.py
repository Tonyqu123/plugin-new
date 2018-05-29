import re
import copy

def str2bool(v):
    if v is None:
        return v
    return v.lower() in ('yes', 'true', 't', '1')


def convert_bool_args(args, bool_fields):
    args = copy.deepcopy(args)
    for f in bool_fields:
        if f in args:
            args[f] = str2bool(args[f])
    return args


def underscore(word):
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    word = word.replace("-", "_")
    return word.lower()


def camelize(string, uppercase_first_letter=True):
    if uppercase_first_letter:
        return re.sub(r"(?:^|_)(.)", lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]


def to_view_dict(values, with_order=False):
    if with_order:
        return dict((camelize(k), v) for k, v in values.items())
    return {camelize(k): v for k, v in values.items()}


def from_view_dict(values, with_order=False):
    if with_order:
        return dict((underscore(k), v) for k, v in values.items())
    return {underscore(k): v for k, v in values.items()}




