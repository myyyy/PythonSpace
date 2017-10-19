# -*- coding:utf-8 -*-
#这是一个使用softmax回归（softmax regression）模型的经典案例。
#y=softmax(Wx+b)
#softmax模型可以用来给不同的对象分配概率。
#即使在之后，我们训练更加精细的模型时，最后一步也需要用softmax来分配概率。
import input_data
import tensorflow as tf
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder("float", [None, 784])
#Variable 。 一个Variable代表一个可修改的张量，
#存在在TensorFlow的用于描述交互性操作的图中
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x,W) + b)
y_ = tf.placeholder("float", [None,10])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
init = tf.initialize_all_variables()
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

with tf.Session() as sess:
    sess.run(init)
    for i in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
        #评估我们的模型
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        print sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels})