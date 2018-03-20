<!-- 
Python官方文档：Descriptor 指南
http://python.jobbole.com/83562/-->



<div class="RichContent-inner" data-reactid="323"><span class="RichText CopyrightRichText-richText" itemprop="text" data-reactid="324"><p>简单来讲，描述符就是一个Python对象，但这个对象比较特殊，特殊性在于其<strong>属性</strong>的访问方式不再像普通对象那样访问，它通过一种叫描述符协议的方法来访问。这些方法包括__get__、__set__、__delete__。定义了其中任意一个方法的对象都叫描述符。举个例子：</p><p><br><strong>普通对象</strong></p><div class="highlight"><pre><code class="language-django"><span></span><span class="x">class Parent(object):</span>
<span class="x">    name = 'p'</span>

<span class="x">class Person(Parent):</span>
<span class="x">    name = "zs"</span>

<span class="x">zhangsan = Person()</span>
<span class="x">zhangsan.name = "zhangsan"</span>
<span class="x">print zhangsan.name</span>
<span class="x">#&gt;&gt; zhangsan</span>
</code></pre></div><br><p>普通的Python对象操作（get，set，delete）属性时都是在这个对象的__dict__基础之上进行的。比如上例中它在访问属性name的方式是通过如下顺序去查找，直到找到该属性位置，如果在父类中还没找到那么就抛异常了。</p><ol><li>通过实例对象的__dict__属性访问：zhangsan.__dict__['name']</li><li>通过类型对象的__dict__属性访问：type(zhangsan).__dict__['name'] 等价于 Person.__dict__['name']</li><li>通过父类对象的__dict__属性访问：zhangsan.__class__.__base__.__dict__['name'] 等价于 Parent.__dict__['name']</li></ol><p>类似地修改属性name的值也是通过__dict__的方式：</p><div class="highlight"><pre><code class="language-django"><span></span><span class="x">zhangsan.__dict__['name'] = 'lisi'</span>
<span class="x">print zhangsan.name</span>
<span class="x">#&gt;&gt; lisi</span>
</code></pre></div><br><p><strong>描述符</strong></p><div class="highlight"><pre><code class="language-django"><span></span><span class="x">class DescriptorName(object):</span>
<span class="x">    def __init__(self, name):</span>
<span class="x">        self.name = name</span>

<span class="x">    def __get__(self, instance, owner):</span>
<span class="x">        print '__get__', instance, owner</span>
<span class="x">        return self.name</span>

<span class="x">    def __set__(self, instance, value):</span>
<span class="x">        print '__set__', instance, value</span>
<span class="x">        self.name = value</span>


<span class="x">class Person(object):</span>
<span class="x">    name = DescriptorName('zhangsan')</span>


<span class="x">zhangsan = Person()</span>
<span class="x">print zhangsan.name</span>
<span class="x">#&gt;&gt;__get__ &lt;__main__.Person object at 0x10bc59d50&gt; &lt;class '__main__.Person'&gt;</span>
<span class="x">#&gt;&gt;zhangsan</span>
</code></pre></div><p>这里的DescriptorName就是一个描述符，访问Person对象的name属性时不再是通过__dict__属性来访问，而是通过调用DescriptorName的__get__方法获取，同样的道理，给name赋值的时候是通过调用__set__方法实现而不是通过__dict__属性。</p><br><div class="highlight"><pre><code class="language-django"><span></span><span class="x">zhangsan.__dict__['name'] = 'lisi'</span>
<span class="x">print zhangsan.name</span>
<span class="x">#&gt;&gt;__get__ &lt;__main__.Person object at 0x10bc59d50&gt; &lt;class '__main__.Person'&gt;</span>
<span class="x">#&gt;&gt;zhangsan</span>
<span class="x">#通过dict赋值给name但值并不是"lisi"，而是通过调用get方法获取的值</span>

<span class="x">zhangsan.name = "lisi"</span>
<span class="x">print zhangsan.name</span>
<span class="x">#&gt;&gt;__set__ &lt;__main__.Person object at 0x108b35d50&gt; lisi</span>
<span class="x">#&gt;&gt;__get__ &lt;__main__.Person object at 0x108b35d50&gt; &lt;class '__main__.Person'&gt;</span>
<span class="x">#&gt;&gt;lisi</span>
</code></pre></div><p>类似地，删除属性的值也是通过调用__delete__方法完成的。此时，你有没有发现描述符似曾相识，没错，用过Django就知道在定义model的时候，就用到了描述符。比如：</p><br><div class="highlight"><pre><code class="language-ada"><span></span><span class="n">from</span> <span class="n">django</span><span class="p">.</span><span class="n">db</span> <span class="n">import</span> <span class="n">models</span>

<span class="n">class</span> <span class="n">Poll</span><span class="p">(</span><span class="n">models</span><span class="p">.</span><span class="n">Model</span><span class="p">):</span>
    <span class="n">question</span> <span class="o">=</span> <span class="n">models</span><span class="p">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">200</span><span class="p">)</span>
    <span class="n">pub_date</span> <span class="o">=</span> <span class="n">models</span><span class="p">.</span><span class="n">DateTimeField</span><span class="p">('</span><span class="na">date</span> <span class="n">published</span><span class="p">')</span> 
</code></pre></div><p>上面的例子是基于类的方式来创建描述符，你还可以通过property()函数来创建描述符，例如：</p><div class="highlight"><pre><code class="language-django"><span></span><span class="x">class Person(object):</span>

<span class="x">    def __init__(self):</span>
<span class="x">        self._email = None</span>

<span class="x">    def get_email(self):</span>
<span class="x">        return self._email</span>

<span class="x">    def set_email(self, value):</span>
<span class="x">         m = re.match('\w+@\w+\.\w+', value)</span>
<span class="x">         if not m:</span>
<span class="x">             raise Exception('email not valid')</span>
<span class="x">         self._email = value</span>

<span class="x">    def del_email(self):</span>
<span class="x">        del self._email</span>

<span class="x">    #使用property()函数创建描述符</span>
<span class="x">    email = property(get_email, set_email, del_email, 'this is email property')</span>


<span class="x">&gt;&gt;&gt; p = Person()</span>
<span class="x">&gt;&gt;&gt; p.email</span>
<span class="x">&gt;&gt;&gt; p.email = 'dsfsfsd'</span>
<span class="x">Traceback (most recent call last):</span>
<span class="x">  File "&lt;stdin&gt;", line 1, in &lt;module&gt;</span>
<span class="x">  File "test.py", line 71, in set_email</span>
<span class="x">    raise Exception('email not valid')</span>
<span class="x">Exception: email not valid</span>
<span class="x">&gt;&gt;&gt; p.email = 'lzjun567@gmail.com'</span>
<span class="x">&gt;&gt;&gt; p.email</span>
<span class="x">'lzjun567@gmail.com'</span>
<span class="x">&gt;&gt;&gt; </span>
</code></pre></div><br><p>property()函数返回的是一个描述符对象，它可接收四个参数：property(fget=None, fset=None, fdel=None, doc=None)</p><ul><li>fget：属性获取方法</li><li>fset：属性设置方法</li><li>fdel：属性删除方法</li><li>doc： docstring</li></ul><p>采用property实现描述符与使用类实现描述符的作用是一样的，只是实现方式不一样。python里面的property是使用C语言实现的，不过你可以使用纯python的方式来实现property函数，如下：</p><div class="highlight"><pre><code class="language-text"><span></span>class Property(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
</code></pre></div><br><p>留心的你发现property里面还有getter，setter，deleter方法，那他们是做什么用的呢？来看看第三种创建描述符的方法。</p><b><br><br>使用@property装饰器</b><div class="highlight"><pre><code class="language-django"><span></span><span class="x">class Person(object):</span>

<span class="x">    def __init__(self):</span>
<span class="x">        self._email = None</span>

<span class="x">    @property</span>
<span class="x">    def email(self):</span>
<span class="x">        return self._email</span>

<span class="x">    @email.setter</span>
<span class="x">    def email(self, value):</span>
<span class="x">         m = re.match('\w+@\w+\.\w+', value)</span>
<span class="x">         if not m:</span>
<span class="x">             raise Exception('email not valid')</span>
<span class="x">         self._email = value</span>

<span class="x">    @email.deleter</span>
<span class="x">    def email(self):</span>
<span class="x">        del self._email</span>

<span class="x">&gt;&gt;&gt;</span>
<span class="x">&gt;&gt;&gt; Person.email</span>
<span class="x">&lt;property object at 0x02214930&gt;</span>
<span class="x">&gt;&gt;&gt; p.email = 'lzjun'</span>
<span class="x">Traceback (most recent call last):</span>
<span class="x">  File "&lt;stdin&gt;", line 1, in &lt;module&gt;</span>
<span class="x">  File "test.py", line 93, in email</span>
<span class="x">    raise Exception('email not valid')</span>
<span class="x">Exception: email not valid</span>
<span class="x">&gt;&gt;&gt; p.email = 'lzjun@gmail.com'</span>
<span class="x">&gt;&gt;&gt; p.email</span>
<span class="x">'lzjun@gmail.com'</span>
<span class="x">&gt;&gt;&gt;</span>
</code></pre></div><p>发现没有，其实装饰器property只是property函数的一种语法糖而已，setter和deleter作用在函数上面作为装饰器使用。</p>哪些场景用到了描述符<p>其实python的实例方法就是一个描述符，来看下面代码块：</p><div class="highlight"><pre><code class="language-as"><span></span><span class="o">&gt;&gt;&gt;</span> <span class="kd">class</span> <span class="nx">Foo</span><span class="p">(</span><span class="nx">object</span><span class="p">)</span><span class="o">:</span>
<span class="p">...</span>     <span class="nx">def</span> <span class="nx">my_function</span><span class="p">(</span><span class="nx">self</span><span class="p">)</span><span class="o">:</span>
<span class="p">...</span>        <span class="nx">pass</span>
<span class="p">...</span>
<span class="o">&gt;&gt;&gt;</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">my_function</span>
<span class="o">&lt;</span><span class="nx">unbound</span> <span class="nx">method</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">my_function</span><span class="o">&gt;</span>
<span class="o">&gt;&gt;&gt;</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">__dict__</span><span class="p">[</span><span class="s1">'my_function'</span><span class="p">]</span>
<span class="o">&lt;</span><span class="kd">function</span> <span class="nx">my_function</span> <span class="nx">at</span> <span class="mh">0x02217830</span><span class="o">&gt;</span>
<span class="o">&gt;&gt;&gt;</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">__dict__</span><span class="p">[</span><span class="s1">'my_function'</span><span class="p">].</span><span class="nx">__get__</span><span class="p">(</span><span class="nx">None</span><span class="o">,</span> <span class="nx">Foo</span><span class="p">)</span>  <span class="err">#</span><span class="nx">my_function</span><span class="err">函数实现了</span><span class="nx">__get__</span><span class="err">方法</span>
<span class="o">&lt;</span><span class="nx">unbound</span> <span class="nx">method</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">my_function</span><span class="o">&gt;</span>
<span class="o">&gt;&gt;&gt;</span> <span class="nx">Foo</span><span class="p">().</span><span class="nx">my_function</span>
<span class="o">&lt;</span><span class="nx">bound</span> <span class="nx">method</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">my_function</span> <span class="nx">of</span> <span class="o">&lt;</span><span class="nx">__main__</span><span class="p">.</span><span class="nx">Foo</span> <span class="nx">object</span> <span class="nx">at</span> <span class="mh">0x0221</span><span class="nx">FFD0</span><span class="o">&gt;&gt;</span>
<span class="o">&gt;&gt;&gt;</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">__dict__</span><span class="p">[</span><span class="s1">'my_function'</span><span class="p">].</span><span class="nx">__get__</span><span class="p">(</span><span class="nx">Foo</span><span class="p">()</span><span class="o">,</span> <span class="nx">Foo</span><span class="p">)</span> <span class="err">#</span><span class="nx">Foo</span><span class="err">的实例对象实现了</span><span class="nx">__get__</span><span class="err">方法</span>
<span class="o">&lt;</span><span class="nx">bound</span> <span class="nx">method</span> <span class="nx">Foo</span><span class="p">.</span><span class="nx">my_function</span> <span class="nx">of</span> <span class="o">&lt;</span><span class="nx">__main__</span><span class="p">.</span><span class="nx">Foo</span> <span class="nx">object</span> <span class="nx">at</span> <span class="mh">0x02226350</span><span class="o">&gt;&gt;</span>
</code></pre></div></span><!-- react-empty: 1899 --></div>