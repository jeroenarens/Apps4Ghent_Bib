def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def get_paginated_response_from_queryset(self, queryset, serializer_cls=None):
    page = self.paginate_queryset(queryset)
    if serializer_cls == None:
        serializer = self.get_serializer(page, many=True)
    else:
        serializer = serializer_cls(page, many=True)
    return self.get_paginated_response(serializer.data)

def prefix_list(prefix, l):
    "Prefixs all elements in the given list by a given prefix"
    return list(map(lambda x: prefix + x, l))
