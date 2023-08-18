def render_with_suffix(value, suffix, round_fn):
    return ' '.join([str(round_fn(value)), suffix])


def render_number(value, multi, suffixes,
                  round_fn=lambda a: round(a, 1)):  # suffixes are: [zero, kilo, mega, giga, tera]
    for i in range(0, len(suffixes)):
        if value < multi:
            return render_with_suffix(value, suffixes[i], round_fn)
        else:
            value /= multi
    return render_with_suffix(value, suffixes[-1], round_fn)
