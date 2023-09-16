from hotpdf.processor import get_document_xml
from hotpdf.memory_map import MemoryMap
from hotpdf.utils import filter_adjacent_coords

if __name__ == "__main__":
    document_xml = get_document_xml("test.pdf")

    # Create a MemoryMap instance
    memory_map = MemoryMap(xmin=0, ymin=0, xmax=1170 + 5, ymax=827 + 5, precision=1)
    memory_map.build_memory_map()
    memory_map.load_memory_map([document_xml[0]])
    memory_map.display_memory_map(save=True)

    print(memory_map.extract_text_from_bbox(70, 76, 546, 560))
    # print(memory_map.find_text("Interest"))
    print(filter_adjacent_coords(*memory_map.find_text("UBER")))
    # (['U', 'B', 'E', 'R'], [{'x': 189, 'y': 52}, {'x': 189, 'y': 52}, {'x': 441, 'y': 82}, {'x': 441, 'y': 82}])
    coords = [
        [
            [
                {"x": 70, "y": 546},
                {"x": 346, "y": 300},
                {"x": 324, "y": 287},
                {"x": 356, "y": 287},
            ]
        ],
        [
            [
                {"x": 70, "y": 546},
                {"x": 346, "y": 300},
                {"x": 324, "y": 287},
                {"x": 356, "y": 287},
            ]
        ],
        [
            [
                {"x": 76, "y": 560},
                {"x": 94, "y": 546},
                {"x": 170, "y": 348},
                {"x": 308, "y": 317},
            ]
        ],
        [
            [
                {"x": 76, "y": 560},
                {"x": 94, "y": 546},
                {"x": 170, "y": 348},
                {"x": 308, "y": 317},
            ]
        ],
    ]
    print(memory_map.extract_text_from_bbox(70, 76, 546, 547))