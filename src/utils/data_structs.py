import numpy as np

class ColumnStruct:
    def __init__ (self, filename, header, label_by_index = False):
        self.filename = filename
        self.header = header
        self.bbox_and_label = []
        self.label_by_index = label_by_index

    def add (self, bbox, label):
        combine = (
            np.array([[bbox[0]]], dtype=np.uint8),
            np.array([[bbox[1]]], dtype=np.uint8),
            np.array([[bbox[2]]], dtype=np.uint8),
            np.array([[bbox[3]]], dtype=np.uint8), 
            np.array(label, dtype=np.str_ if not self.label_by_index else np.uint8)                
            )
        self.bbox_and_label.append(combine)

    def entry (self):
        return (
            np.array([self.filename], dtype=np.str_),
            np.array([self.bbox_and_label], dtype=[(elem, 'O') for elem in self.header[1:]])
        )