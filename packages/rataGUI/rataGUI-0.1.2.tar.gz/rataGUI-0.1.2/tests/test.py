# import time

# t0 = time.time()

# test = {"test1": 1, "test2": 2, "test3": 3,}

# for _ in range(1000000):
#     temp = next((name for name, age in test.items() if age == 2))
#     # temp = list(test.keys())[list(test.values()).index(2)]


# t1 = time.time()

# print(t1 - t0)

# import tensorflow as tf
# TFVER = [int(v) for v in tf.__version__.split(".")]
# if TFVER[1] < 14:
#     from tensorflow.contrib.tensorrt import trt_convert as trt
# else:
#     from tensorflow.python.compiler.tensorrt import trt_convert as trt

# from tensorflow.python.compiler.tensorrt import trt_convert as tf_trt


import tensorflow as tf
import os
# Load the .pb file

# # Convert the SavedModel
path = "C:\\Users\\Siapas\\Documents\\video_acquisition\\rataGUI\\exported_models\\DLC_rataGUI_mobilenet_v2_1.0_iteration-0_shuffle-1"

def load_tflite_model(model_dir, input_shape):
    model_file = [file for file in os.listdir(model_dir) if file.endswith('.pb')]
    if len(model_file) > 1:
        raise IOError("Multiple model files found. Model folder should only contain one .pb file")
    elif len(model_file) == 0:
        raise IOError("Could not fild frozen model (.pb) file in specified folder")
    else:
        model_file = model_file[0]

    model_path = os.path.join(model_dir, model_file)
    with tf.io.gfile.GFile(model_path, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
    
    def _imports_graph_def():
        tf.compat.v1.import_graph_def(graph_def, name="")

    wrapped_import = tf.compat.v1.wrap_function(_imports_graph_def, [])
    import_graph = wrapped_import.graph

    # print(import_graph.get_operation_by_name("concat"))
    graph_ops = import_graph.get_operations()


    inputs = [graph_ops[0].name]
    if "concat_1" in graph_ops[-1].name:
        outputs = [graph_ops[-1].name]
    else:
        outputs = [graph_ops[-1].name, graph_ops[-2].name]

    converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
        model_path,
        inputs,
        outputs,
        input_shapes={inputs[0]: input_shape},
    )
    converter.experimental_new_converter = True
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS,
                                       tf.lite.OpsSet.SELECT_TF_OPS]
    # converter.allow_custom_ops = True
    # converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # converter.target_spec.supported_types = [tf.float16]

    tflite_model = converter.convert()
    return tflite_model

load_tflite_model(path, (1, 1000, 1000, 3))


# model_file = [file for file in os.listdir(path) if file.endswith('.pb')]
# if len(model_file) > 1:
#     raise IOError("Multiple model files found. Model folder should only contain one .pb file")
# elif len(model_file) == 0:
#     raise IOError("Could not fild frozen model (.pb) file in specified folder")
# else:
#     model_file = model_file[0]

# model_path = os.path.join(path, model_file)

# converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
#     model_path,
#     ["Placeholder"],
#     ["concat"],
#     input_shapes={"Placeholder": (1, 1000, 1000, 3)},
# )
# # converter.allow_custom_ops = True


# # converter.optimizations = [tf.lite.Optimize.DEFAULT]
# converter.target_spec.supported_types = [tf.float16]
# tflite_model = converter.convert()

# tflite_interpreter = tf.lite.Interpreter(model_content=tflite_model)
# tflite_interpreter.allocate_tensors()