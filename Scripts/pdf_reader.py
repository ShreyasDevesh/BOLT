from functools import partial
import pdfplumber
 
def not_within_bboxes(obj, bboxes):
    """Check if the object is in any of the table's bbox."""
    def obj_in_bbox(_bbox):
        """Find Bboxes of objexts."""
        v_mid = (obj["top"] + obj["bottom"]) / 2
        h_mid = (obj["x0"] + obj["x1"]) / 2
        x0, top, x1, bottom = _bbox
        return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
    return not any(obj_in_bbox(__bbox) for __bbox in bboxes)

def extract(page):
    """Extract PDF text, Filter tables and delete in-par breaks."""
    # Filter-out tables
    if page.find_tables() != []:
        # Get the bounding boxes of the tables on the page.
        bboxes = [table.bbox for table in page.find_tables()]
        bbox_not_within_bboxes = partial(not_within_bboxes, bboxes=bboxes)
        # Filter-out tables from page
        page = page.filter(bbox_not_within_bboxes)
    # Extract Text
    extracted = page.extract_text()
    # Delete in-paragraph line breaks
    extracted = extracted.replace(".\n", "**/m" # keep par breaks
                        ).replace(". \n", "**/m" # keep par breaks
                        ).replace("\n", "" # delete in-par breaks
                        ).replace("**/m", ".\n\n") # restore par break
    return extracted

