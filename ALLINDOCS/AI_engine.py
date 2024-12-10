import tensorflow as tf
import numpy as np
from transformers import TFAutoModelForSeq2SeqLM, AutoTokenizer

PATH_ = 'ALLINDOCS/Assets/model_6_skimlit.keras'
with tf.device('/GPU:0'):
    class model:
        def __init__(self):
            self.path = PATH_
            self.summ_model_name = "t5-small" 
            self.model = tf.keras.models.load_model(self.path)
            self.summ_model = TFAutoModelForSeq2SeqLM.from_pretrained(self.summ_model_name)
            self.summ_tokenizer = AutoTokenizer.from_pretrained(self.summ_model_name)
            self.labels = ['BACKGROUND', 'CONCLUSIONS', 'METHODS', 'OBJECTIVE', 'RESULTS']
            self.str = None
            self.line_num = None
            self.false_pred = None
            self.refined_data = None
            self.isdataaval= 0
            self.predictions = {
                'BACKGROUND':[],
                'OBJECTIVE':[],
                'METHODS':[],
                'RESULTS':[],
                'CONCLUSIONS':[]
            }
        def get_data(self,data_):
            self.isdataaval = 1
            self.str = data_['string']
            self.line_num = data_['line_num']
        def refine_data(self):
            if self.isdataaval:
                self.false_pred = np.zeros(len(self.line_num),dtype=np.int32)
                predd = tf.data.Dataset.from_tensor_slices((self.false_pred))
                comb = tf.data.Dataset.from_tensor_slices((self.str,self.line_num))
                comb = tf.data.Dataset.zip((comb,predd))
                self.refined_data = comb.batch(32).prefetch(tf.data.AUTOTUNE)
        def summarize(self):
                if self.isdataaval:
                    input_text = "summarize: ".join(self.str)
                    inputs = self.summ_tokenizer.encode(input_text, return_tensors="tf", max_length=len(input_text), truncation=True)
                    summary_ids = self.summ_model.generate(inputs, max_length=100, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
                    summary = self.summ_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
                    return summary
        def predict(self):
            if self.isdataaval:
                preds = self.model.predict(self.refined_data)
                preds = tf.argmax(preds,axis=1)
                x = 0
                for i in preds:
                    self.predictions[self.labels[i]].append(self.str[x])
                    x += 1
                return self.predictions

