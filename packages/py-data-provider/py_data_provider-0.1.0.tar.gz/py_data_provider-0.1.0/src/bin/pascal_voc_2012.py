from src.utils.config import ROOT
from src.data_providers.voc import VOCSegmentationDataProvider


if __name__ == "__main__":
    root = str(ROOT / "data" / "voc_2012")
    ds = VOCSegmentationDataProvider(root=root, year=2012, mode="semantic")
