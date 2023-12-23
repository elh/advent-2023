# max_dist.pyx

cpdef public int max_dist(dict graph, tuple start_loc, tuple end_loc):
    cdef list fringe = [(start_loc, set(), 0)]
    cdef int max_dist = -1
    while fringe:
        cur_loc, cur_prev_set, cur_steps_taken = fringe.pop()
        if cur_loc == end_loc:
            max_dist = max(cur_steps_taken, max_dist)
            continue
        if end_loc in graph[cur_loc]:
            new_set = cur_prev_set.copy()
            new_set.add(end_loc)
            fringe.append((end_loc, new_set, cur_steps_taken + graph[cur_loc][end_loc]))
            continue
        for next_loc in graph[cur_loc]:
            if next_loc in cur_prev_set:
                continue
            new_set = cur_prev_set.copy()
            new_set.add(next_loc)
            fringe.append((next_loc, new_set, cur_steps_taken + graph[cur_loc][next_loc]))
    return max_dist
