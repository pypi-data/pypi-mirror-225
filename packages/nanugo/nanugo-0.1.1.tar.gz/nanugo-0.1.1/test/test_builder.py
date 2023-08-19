from nanugo import nanugo
from nanugo.log import logger
import os, logging
from PIL import Image

logger.setLevel(logging.DEBUG)
get_file_name = lambda path: os.path.basename(path)

def test_default_deck():
    builder = nanugo.Builder()
    errors = []
    deck = builder.build_deck("test", "test/test.pdf")
    if file_name := get_file_name(deck.media_list[0]) != "test_p0_q.jpeg":
        errors.append(f"File name doesn't seem right: {file_name}")
    with Image.open(deck.media_list[0]) as test_subj_image:
        if test_subj_image.size != (540, 390):
            errors.append(f"Split page size doesn't seem right: {test_subj_image.size}")
    if media_len := len(deck.media_list) != 2:
        errors.append(f"len(media_list) is not 2: {media_len}")

    assert not errors, "Errors occured: \n{}".format("\n".join(errors))


def test_weird_deck():
    builder = nanugo.Builder()
    errors = []
    deck = builder.build_deck("test", "test/test.pdf", vertical=True, ratio=(0.4, 0.6))
    if file_name := get_file_name(deck.media_list[0]) != "test_p0_q.jpeg":
        errors.append(f"File name doesn't seem right: {file_name}")
    with Image.open(deck.media_list[0]) as test_subj_image:
        if test_subj_image.size != (216, 780):
            errors.append(f"Split page size doesn't seem right: {test_subj_image.size}")
    if media_len := len(deck.media_list) != 2:
        errors.append(f"len(media_list) is not 2: {media_len}")

    assert not errors, "Errors occured: \n{}".format("\n".join(errors))

if __name__ == "__main__":
    test_default_deck()
    test_weird_deck()