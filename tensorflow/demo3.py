# -*- coding:utf-8 -*-
import tensorflow as tf

#1:
state = tf.Variable(0, name="counter")
one = tf.constant(1)
new_value = tf.add(state,one)
update = tf.assign(state,new_value)
init_op = tf.initialize_all_variables()
with tf.Session() as sess:
    sess.run(init_op)
    print sess.run(state)
    for _ in range(3):
        sess.run(update)
        print sess.run(state)

#2:

input1 = tf.constant(3.0)
input2 = tf.constant(2.0)
input3 = tf.constant(5.0)
initermed = tf.add(input2,input3)
print initermed
mul = tf.multiply(input1,initermed)
print mul
with tf.Session() as sess:
    result = sess.run([mul,initermed])
    print result