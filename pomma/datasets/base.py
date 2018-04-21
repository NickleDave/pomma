import os

bird_IDs_and_data_filenames = [
    ('bl26lb16', 'bl26lb16_sequences.txt'),
]


def load():
    data_dict = {}
    module_path = os.path.dirname(__file__)
    for bird_ID, data_filename in bird_IDs_and_data_filenames:    
        data_filename = os.path.join(module_path, 'data',
                                      data_filename)
        with open(data_filename, 'r') as data:
            sequences = data.readlines()
        data_dict[bird_ID] = sequences

    return data_dict