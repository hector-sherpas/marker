import re
from sklearn.cluster import DBSCAN
import  numpy as np


def get_clusters(coords):
    coords = np.array(coords).reshape(-1, 1)

    clustering = DBSCAN(eps=3, min_samples=1).fit(coords)

    clusters = clustering.labels_

    return clusters


def get_y_coords_from_blocks(blocks, criteria="y_min"):

    if criteria=="y_min":
        y_coords = [block.bbox[1] if hasattr(block, "bbox") 
                    else block["bbox"][1] 
                    for block in blocks]
    
    elif criteria=="y_middle":
        y_coords = [block.bbox[1] + (block.bbox[3] - block.bbox[1])/2 if hasattr(block, "bbox") 
                    else block["bbox"][1] + (block["bbox"][3] - block["bbox"][1])/2 
                    for block in blocks]
    
    elif criteria=="y_max":
        y_coords = [block.bbox[3] if hasattr(block, "bbox") 
                    else block["bbox"][3] 
                    for block in blocks]
        
    return y_coords


def group_blocks(blocks, criteria):
    
    if isinstance(blocks, list):
        y_coords = get_y_coords_from_blocks(blocks, criteria=criteria)
    elif isinstance(blocks, dict):
        y_coords = [np.mean(get_y_coords_from_blocks(grouped_blocks, criteria)) for grouped_blocks in blocks.values()]
        blocks = blocks.values()

    clusters= get_clusters(y_coords)

    vertical_groups = {}
    for group, block, _ in sorted(zip(clusters.tolist(), blocks, y_coords), key=lambda x: x[2]):
        if group not in vertical_groups:
            vertical_groups[group] = []
        vertical_groups[group].extend([block] if isinstance(block, dict) 
                                      else block)

    return vertical_groups


def sort_table_blocks(blocks):

    vertical_groups = group_blocks(blocks, criteria="y_max")
    vertical_groups = group_blocks(vertical_groups, criteria="y_middle")
    vertical_groups = group_blocks(vertical_groups, criteria="y_min")

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
