def attribute_table_generator(filename):
    """
    This function reads a txt file and creates a list object containing the
    table used to pick attributes.
    Returns: a list
    """
    table_doc = open(filename, 'r')
    table = []
    for line in table_doc:
#        table_doc.readline()
#        table.extend()
        table.append(line.strip())
    table_doc.close()
    return table



turning_events_table = attribute_table_generator('turning_events.txt')
turning_events = turning_events_table[13]
print(turning_events)