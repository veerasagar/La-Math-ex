import os
import shutil
import xml.etree.ElementTree as ET

# Paths
CROHME_DIR = 'data/crohme'
OUTPUT_IMG = 'data/images'
OUTPUT_LABEL = 'data/labels'

os.makedirs(OUTPUT_IMG, exist_ok=True)
os.makedirs(OUTPUT_LABEL, exist_ok=True)

# Iterate over formula XML files
for root, _, files in os.walk(CROHME_DIR):
    for fname in files:
        if fname.endswith('.xml'):
            xml_path = os.path.join(root, fname)
            tree = ET.parse(xml_path)
            root_elem = tree.getroot()

            for expr in root_elem.findall('.//expression'):
                img_file = expr.get('image')  # e.g., 'GT01.png'
                latex = expr.find('latex').text

                src_img = os.path.join(root, 'trace', img_file)
                dst_img = os.path.join(OUTPUT_IMG, img_file)
                with open(os.path.join(OUTPUT_LABEL, img_file.replace('.png', '.txt')), 'w') as f:
                    f.write(latex)

                if os.path.exists(src_img):
                    shutil.copy(src_img, dst_img)