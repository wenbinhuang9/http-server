
implement a socket server with only one threads. 

参考这一篇文章： 
https://www.lagou.com/lgeduarticle/37877.html

### DESIGN

design for the http server

1.  layer1, using socket to implement a socket listener. 
2.  layer2, resolve the http header.
3.  layer3, design the http handler.

### todo 
implement http 0.9  get, get to know the http 0.9

how to implement Connection: keep-alive

support post, but how to support post, what does post mean here