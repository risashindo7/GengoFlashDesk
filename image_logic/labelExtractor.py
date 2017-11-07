from sys import stdout
import numpy as np
import re
import tensorflow as tf
import pickle


def create_graph():
    """Creates a graph from pretrained model."""
    with tf.gfile.FastGFile('inception-2015-12-05/classify_image_graph_def.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        tf.import_graph_def(graph_def, name='')


def extract_vectors(image_path, tensor_names):
    """Extract vectors from an image.
    Args
    ----
        image_path: image path.
        tensor_names: a list of tensor names to extract
            useful tensor_names: 'softmax:0', 'pool_3:0'
            'softmax:0': A tensor containing the normalized prediction across
            1000 labels, called concept vector;
            'pool_3:0': A tensor containing the next-to-last layer containing
            2048 float description of the image, called feature vector.
    Returns
    -------
        vector: dict
            tensor_name -> a numpy array (vector)
    """
    if not tf.gfile.Exists(image_path):
        tf.logging.fatal('File does not exist %s', image_path)
    # read image data from the given path
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    with tf.Session() as sess:
        target_tensors = [sess.graph.get_tensor_by_name(name)
                        for name in tensor_names]
        # run the model to extract the target tensors on the image
        outputs = sess.run(target_tensors,
                {'DecodeJpeg/contents:0': image_data})
        # flatten the outputs and remove redundant dimensions
        vector = dict((name, np.ravel(output))
                for name, output in zip(tensor_names, outputs))
    return vector


def batch_extract_vectors(image_paths):
    """ Extract vectors for a set of images
    Returns
    -------
    vectors: dict
        vector name -> a numpy array (matrix), each row is the vector of that
        type for an image.
    """
    vectors = dict()
    vectors['softmax:0'] = []
    for i, path in enumerate(image_paths):
        vector = extract_vectors(path, vectors.keys())
        for name, vec in vector.items():
            vectors[name].append(vec)
        stdout.write('\r{}'.format(i + 1))
        stdout.flush()
    for name in vectors.keys():
        vectors[name] = np.asarray(vectors[name])
    print('')
    return vectors


def extract_labels(images):
    """ Basic search engine
    Returns
    -------
    results: numpy array
        each column is a ranked image list for a query
    """
    # initialize tensorflow
    #create_graph()
    #print('Extracting vectors for images in database...')
    #img_vecs = batch_extract_vectors([pth for _, pth in images])
    name1 = 'imagevecs'
    
    with open(name1 + '.pkl', 'rb') as f:
        img_vecs = pickle.load(f)

    labelsListAll = [""] * len(img_vecs['softmax:0'])
    for i in img_vecs:
        for k in range(len(img_vecs[i])):
            #here process one image
            row = (img_vecs[i])[k]
            sortedIndices = (np.argsort(-row, axis = 0))
            top4Indices = []
            for j in range(4):
                if (row[sortedIndices[j]] > 0.2):
                    top4Indices.append(sortedIndices[j])
                
            listOfIndicesToHumanFormat = []

            for index in top4Indices:
                flag = 0
                with open('imagenet_2012_challenge_label_map_proto.txt', 'r') as f:
                    for line in f:
                        if (flag == 1):
                            flag = 0
                            m = re.search('"(.+?)"', line)
                            codeToHumanFormat = m.group(1)
                            listOfIndicesToHumanFormat.append(codeToHumanFormat)
                            break
                        if ('target_class: ' + str(index) + '\n') in line:
                            flag = 1
            #here I have for a row list of 0 to 4 indices in nXXXX format
            labelsList = ""
            # to increase significance of most relevant labels
            multiplicity = 4
            for index in listOfIndicesToHumanFormat:
                flag = 0
                with open('imagenet_synset_to_human_label_map.txt', 'r') as f:
                    for line in f:
                        if (index in line):
                            labelsList += " " + "".join(line.replace(index, "").rstrip() * multiplicity)
                            multiplicity -= 1
                            break
            #here each labelsList has labels related to the kth image
            labelsListAll[k] = labelsList
                        
            with open('image_labels.txt', mode='wt', encoding='utf-8') as myfile:
                myfile.write('\n'.join(labelsListAll))