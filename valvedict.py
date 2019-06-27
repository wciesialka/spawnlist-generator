def dict_as_valve_dict(d,initial_indentation=0):
    lines = []
    indentation = initial_indentation
    for k in d:
        v = d[k]
        line = ""
        for _ in range(indentation):
            line += "\t"
        if type(v) is dict:
            line += f"\"{k}\""
            lines.append(line)
            line = ""
            for _ in range(indentation):
                line += "\t"
            line += "{"
            lines.append(line)
            morelines = dict_as_valve_dict(v,initial_indentation = indentation + 1)
            for line in morelines:
                lines.append(line)
            line = ""
            for _ in range(indentation):
                line += "\t"
            line += "}"
            lines.append(line)
        else:
            line += f"\"{k}\"\t\"{v}\""
            lines.append(line)
    return lines