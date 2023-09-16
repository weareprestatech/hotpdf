from hotpdf.processor import get_document_xml
from hotpdf.memory_map import MemoryMap

if __name__ == "__main__":
    document_xml = get_document_xml("test.pdf")

    # Create a MemoryMap instance
    memory_map = MemoryMap(xmin=0, ymin=0, xmax=1170 + 5, ymax=827 + 5, precision=1)
    memory_map.build_memory_map()
    memory_map.load_memory_map([document_xml[0]])
    memory_map.display_memory_map(save=True)

    print(memory_map.extract_text_from_bbox(0, 85, 0, 50))
    print(memory_map.find_text("Interest"))
