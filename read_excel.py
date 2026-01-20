import zipfile
import xml.etree.ElementTree as ET
import json
import os

def read_xlsx(file_path):
    ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # Read shared strings
            shared_strings = []
            try:
                ss_data = z.read('xl/sharedStrings.xml')
                ss_root = ET.fromstring(ss_data)
                for si in ss_root.findall('ns:si', ns):
                    t = si.find('ns:t', ns)
                    if t is not None:
                        shared_strings.append(t.text)
                    else:
                        # Handle formatted text
                        text_parts = [r.find('ns:t', ns).text for r in si.findall('ns:r', ns) if r.find('ns:t', ns) is not None]
                        shared_strings.append("".join(text_parts))
            except KeyError:
                pass # No shared strings

            # Read sheet1
            sheet_data = z.read('xl/worksheets/sheet1.xml')
            sheet_root = ET.fromstring(sheet_data)
            
            data = []
            for row in sheet_root.findall('.//ns:row', ns):
                row_data = []
                for cell in row.findall('ns:c', ns):
                    cell_type = cell.get('t')
                    value_tag = cell.find('ns:v', ns)
                    is_tag = cell.find('ns:is', ns)
                    
                    val = ""
                    if cell_type == 's' and value_tag is not None:
                        val = shared_strings[int(value_tag.text)]
                    elif is_tag is not None:
                        t_tag = is_tag.find('ns:t', ns)
                        if t_tag is not None:
                            val = t_tag.text
                    elif value_tag is not None:
                        val = value_tag.text
                    
                    row_data.append(val or "")
                if any(row_data):
                    data.append(row_data)
            return data
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    file_path = 'stock scentpro.xlsx'
    result = read_xlsx(file_path)
    # Filter for rows that likely contain product data (e.g. at least 2 non-empty columns)
    meaningful_data = []
    for row in result:
        non_empty = [c for c in row if c and str(c).strip()]
        if len(non_empty) >= 2:
            meaningful_data.append(row)
    
    with open('inventory_clean.json', 'w') as f:
        json.dump(meaningful_data, f)
    print(f"Saved {len(meaningful_data)} meaningful rows to inventory_clean.json")
