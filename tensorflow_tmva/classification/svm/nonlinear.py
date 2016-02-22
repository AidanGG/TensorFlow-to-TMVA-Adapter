import tensorflow as tf


def kernel_tensor(training, inputs, gamma):
    """Creates the Gaussian kernel tensor from the training data."""
    tiled_training = tf.tile(tf.expand_dims(training, 1), [1, inputs, 1])
    distances = tf.reduce_sum(tf.square(tf.sub(tf.transpose(
        tiled_training, perm=[1, 0, 2]), tiled_training)), reduction_indices=2)
    kernel = tf.exp(tf.mul(tf.neg(
        tf.constant([gamma], dtype=tf.float32)), distances))

    return kernel


def kernelised_cost(training, classes, inputs, C=1, gamma=1):
    """Returns the kernelised cost to be minimised."""
    beta = tf.Variable(tf.zeros([inputs, 1]))
    offset = tf.Variable(tf.zeros([1]))

    kernel = kernel_tensor(training, inputs, gamma)

    x = tf.reshape(tf.div(tf.matmul(tf.matmul(
        beta, kernel, transpose_a=True), beta), tf.constant([2.0])), [1])
    y = tf.sub(tf.ones([1]), tf.mul(classes, tf.add(
        tf.matmul(kernel, beta, transpose_a=True), offset)))
    z = tf.mul(tf.reduce_sum(tf.reduce_max(
        tf.concat(1, [y, tf.zeros_like(y)]), reduction_indices=1)),
        tf.constant([C], dtype=tf.float32))
    cost = tf.add(x, z)

    return beta, offset, cost


"""
Not ready yet
def decide(testing, beta, offset):
    # Tests a set of test instances.
    return tf.sign(tf.add(tf.matmul(testing, beta), offset))
"""
