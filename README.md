# How to use

``` python

>>> from secd_machine.secd import SECDMachine
>>> a = SECDMachine("((L_x.x)a)")
>>> a.execute()
<SECD [S:[], E:{}, C:['((L_x.x)a)'], D:[]]>
1
<SECD [S:[], E:{}, C:['ap', '(L_x.x)', 'a'], D:[]]>
>>> a.execute()
<SECD [S:[], E:{}, C:['ap', '(L_x.x)', 'a'], D:[]]>
3
<SECD [S:['a'], E:{}, C:['ap', '(L_x.x)'], D:[]]>
>>> a.execute()
<SECD [S:['a'], E:{}, C:['ap', '(L_x.x)'], D:[]]>
2
<SECD [S:['a', <Closure [env:{}, bv:x, body:x]>], E:{}, C:['ap'], D:[]]>
>>> a.execute()
<SECD [S:['a', <Closure [env:{}, bv:x, body:x]>], E:{}, C:['ap'], D:[]]>
1
<SECD [S:[], E:{'x': 'a'}, C:['x'], D:[[], {}, [], []]]>
>>> a.execute()
<SECD [S:[], E:{'x': 'a'}, C:['x'], D:[[], {}, [], []]]>
1
<SECD [S:['a'], E:{'x': 'a'}, C:[], D:[[], {}, [], []]]>
>>> a.execute()
<SECD [S:['a'], E:{'x': 'a'}, C:[], D:[[], {}, [], []]]>
0
<SECD [S:['a'], E:{}, C:[], D:[]]>


complete calculation
```

# notification 
Cant calculate over 2 parameter
cant calculate list.