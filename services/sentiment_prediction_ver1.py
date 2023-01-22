# Based on https://huggingface.co/siebert/sentiment-roberta-large-english; but results are not good
from typing import List

from tensorflow.python.client.session import InteractiveSession
from tensorflow.core.protobuf.config_pb2 import GPUOptions, ConfigProto
from transformers import pipeline
import charset_normalizer
import DeepSaki

from models.mxm_label import MxmLabel
from dao.dao_mxm_labels import DAOMxmLabels

from models.mxm_object import MxmObject
from dao.dao_mxm_objects import DAOMxmObjects

sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")


def predict(sentence):
    return sentiment_analysis(sentence)


def create_dict_from_mxm_labels():
    dao_mxm_labels: DAOMxmLabels = DAOMxmLabels()
    mxm_labels: List[MxmLabel] = dao_mxm_labels.find_all()
    mxm_labels_dict = {}
    for mxm_label in mxm_labels:
        mxm_labels_dict[mxm_label.attr_id] = mxm_label.attr_name
    return mxm_labels_dict


def predict_all_songs():
    dao_mxm_objects: DAOMxmObjects = DAOMxmObjects("mxm_train")
    attr_translation_dict: dict = create_dict_from_mxm_labels()

    mxm_objects: List[MxmObject] = dao_mxm_objects.find_all()
    for mxm_object in mxm_objects:
        if mxm_object.sentiment is None:
            sentence = ""
            for mxm_label in mxm_object.attr_list:
                word = attr_translation_dict[mxm_label.atrr_id]
                # sentence_part = (word + " ") * mxm_label.atrr_value
                sentence += word+ " "
            sentiment = predict(sentence)
            # dao_mxm_objects.update_one(mxm_object)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # predict_all_songs()
    print(predict("This thing is red"))
    # gpu_options = GPUOptions(allow_growth=True)
    # session = InteractiveSession(config=ConfigProto(gpu_options=gpu_options))

    # strategy, RUNTIME_ENVIRONMENT, hw_accelerator_handle = DeepSaki.utils.DetectHw()
