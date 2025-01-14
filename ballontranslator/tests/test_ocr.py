import sys, os
import os.path as osp
sys.path.append(osp.dirname(osp.dirname(__file__)))

from tqdm import tqdm
from dl import OCRBase, OCRMIT32px, OCRMIT48pxCTC

from ui.imgtrans_proj import ProjImgTrans
from ui.constants import PROGRAM_PATH
os.chdir(PROGRAM_PATH)

SAVE_DIR = 'tmp/ocr_test'
os.makedirs(SAVE_DIR, exist_ok=True)

def test_ocr(ocr: OCRBase, proj: ProjImgTrans):

    os.makedirs(SAVE_DIR, exist_ok=True)
    print('Testing OCR:', ocr.__class__.__name__)
    print('OCR params:', ocr.setup_params)
    
    for page_name in tqdm(proj.pages):
        blk_list = proj.pages[page_name]
        proj.set_current_img(page_name)
        ocr.ocr_blk_list(proj.img_array, blk_list)
        for blk in blk_list:
            print(blk.text)


def test_mit48px(proj: ProjImgTrans, device: str = 'cpu', chunk_size: int = 16):
    setup_params = OCRMIT48pxCTC.setup_params
    setup_params['device']['select'] = device
    setup_params['chunk_size']['select'] = chunk_size
    ocr = OCRMIT48pxCTC(**setup_params)
    test_ocr(ocr, proj)


if __name__ == '__main__':
    manga_dir = 'data/testpacks/manga'
    manga_proj = ProjImgTrans(manga_dir)

    test_mit48px(manga_proj, 'cpu', 16)
