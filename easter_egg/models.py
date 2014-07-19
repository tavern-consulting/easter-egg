from __future__ import division

import base64


def split_image(image_path, current_split_section, number_of_splits):
    '''
    Open the image, base64 encode it, return the chunk defined by
    current_split_section and number_of_splits.
    '''
    with open(image_path) as f:
        content = f.read()
    content = base64.b64encode(content)
    percentage = 1 / number_of_splits
    first_slice = (current_split_section - 1) * percentage * len(content)
    second_slice = current_split_section * percentage * len(content)
    return content[int(first_slice):int(second_slice)]
