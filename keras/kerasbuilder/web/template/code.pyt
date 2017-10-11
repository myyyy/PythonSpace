model = Sequential()
{% for ly in layers %}model.add(keras.layers.core.{{ly['layer_name']}}({% raw ly['pline']%}))
{% end %}{% if optimizer%}
v_opt = optimizers.{{optimizer.get('optimizer')}}({% raw fix['oline']%})
model.compile(optimizer=v_opt,loss='{{ fix.get('loss','categorical_crossentropy')}}', metrics=[{% raw fix['mline'] %}])
{% else %}
model.compile(optimizer="rmsprop",loss='{{ fix.get('loss','categorical_crossentropy')}}', metrics=[{% raw fix['mline'] %}])
{% end %}