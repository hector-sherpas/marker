import numpy as np

def assign_cells_to_columns(rows):
    row_ref = max(rows, key=lambda x: len(x))
    idx_row_ref = rows.index(row_ref)
    left_edges_ref = np.array([cell[0][0] for cell in row_ref])
    idx_cols_table = set(range(len(row_ref)))

    new_rows = []
    for idx_row, row in enumerate(rows):
        new_row = {}
        for cell in row:
            left_edge = np.array(cell[0][0])
            distances = np.abs(left_edge - left_edges_ref)
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
