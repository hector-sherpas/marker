from marker.tables.utils import get_clusters

import numpy as np
from statistics import mode
from collections import Counter

def assign_cells_to_columns(rows):
    # Find table columns number
    row_ref = max(rows, key=lambda x: len(x))
    rows_len = [len(row) for row in rows]
    cols_frec = Counter(rows_len).most_common(3)
    if len(row_ref) == cols_frec[0][0]:
        idx_row_ref = rows.index(row_ref)
    else:
        cols = [num_cols[0] for num_cols in cols_frec]
        distances = np.abs(np.array(cols) - np.array(len(row_ref)))
        columns_index = sorted([(dist, idx) for idx, dist in enumerate(distances)], 
                                   key=lambda x: x[0])
        num_cols = cols[columns_index[0][1]]
        idx_row_ref = rows_len.index(num_cols)
        row_ref = rows[idx_row_ref]

    idx_cols_table = set(range(len(row_ref)))
    middle_edges_ref = np.array([cell[0][0] + (cell[0][2] - cell[0][0])/2 for cell in row_ref])

    new_rows = []
    for idx_row, row in enumerate(rows):
        new_row = {}
        for cell in row:
            left_edge = np.array(cell[0][0])
            middle_edge = np.array(cell[0][0] + (cell[0][2] - cell[0][0])/2)
            right_edge = np.array(cell[0][2])
            left_distances = np.abs(left_edge - middle_edges_ref)
            middle_distances = np.abs(middle_edge - middle_edges_ref)
            right_distances = np.abs(right_edge - middle_edges_ref)
            min_distances_idx = [np.argmin(left_distances), np.argmin(middle_distances), np.argmin(right_distances)]
            mode_column = mode(min_distances_idx)
            distances = [left_distances, middle_distances, right_distances][min_distances_idx.index(mode_column)]

            columns_index = sorted([(dist, idx) for dist, idx in zip(distances, range(len(distances)))], 
                                   key=lambda x: x[0])
            
            for idx_col in columns_index:
                column_index = idx_col[1]
                if column_index not in new_row:
                    new_row[column_index] = cell[1]
                    break

        # Pad rows to have the same length
        diffset = idx_cols_table ^ set(new_row)
        cols_to_add = {idx: "" for idx in diffset}
        row_padded = dict(sorted({**new_row, **cols_to_add}.items(), key=lambda x: x[0]))
        
        new_rows.append(list(row_padded.values()))

    cols_to_remove = set()
    for idx, col in enumerate(zip(*new_rows)):
        col_total = sum([len(cell.strip()) > 0 for cell in col])
        if col_total == 0:
            cols_to_remove.add(idx)

    rows = []
    for row in new_rows:
        rows.append([col for idx, col in enumerate(row) if idx not in cols_to_remove])

    return rows
