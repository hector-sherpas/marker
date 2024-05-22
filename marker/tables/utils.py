import re
from sklearn.cluster import DBSCAN
import  numpy as np


def sort_table_blocks(blocks):
    
    y_coords = [block.bbox[1] if hasattr(block, "bbox") 
                else block["bbox"][1] 
                for block in blocks]

    y_coords = np.array(y_coords).reshape(-1, 1)

    clustering = DBSCAN(eps=3, min_samples=1).fit(y_coords)

    clusters = clustering.labels_
    
    vertical_groups = {}
    for group, block, _ in sorted(zip(clusters.tolist(), blocks, y_coords), key=lambda x: x[2]):
        if group not in vertical_groups:
            vertical_groups[group] = []
        vertical_groups[group].append(block)

    # Sort each group horizontally and flatten the groups into a single list
    sorted_blocks = []
    for _, group in vertical_groups.items():
        sorted_group = sorted(group, key=lambda x: x.bbox[0] if hasattr(x, "bbox") else x["bbox"][0])
        sorted_blocks.extend(sorted_group)

    return sorted_blocks


def replace_dots(text):
    dot_pattern = re.compile(r'(\s*\.\s*){4,}')
    dot_multiline_pattern = re.compile(r'.*(\s*\.\s*){4,}.*', re.DOTALL)

    if dot_multiline_pattern.match(text):
        text = dot_pattern.sub(' ', text)
    return text


def replace_newlines(text):
    # Replace all newlines
    newline_pattern = re.compile(r'[\r\n]+')
    return newline_pattern.sub(' ', text.strip())
