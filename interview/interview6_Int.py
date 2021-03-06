'''
进程之间如何进行通信？
进程间通信（IPC，InterProcess Communication）是指在不同进程之间传播或交换信息。
IPC的方式通常有管道（包括无名管道和命名管道）、消息队列、信号量、共享存储、Socket、Streams等。
其中 Socket和Streams支持不同主机上的两个进程IPC。

一、管道
管道，通常指无名管道，是 UNIX 系统IPC最古老的形式。
特点：
它是半双工的（即数据只能在一个方向上流动），具有固定的读端和写端。
它只能用于具有亲缘关系的进程之间的通信（也是父子进程或者兄弟进程之间）。
它可以看成是一种特殊的文件，对于它的读写也可以使用普通的read、write 等函数。但是它不是普通的文件，并不属于其他任何文件系统，并且只存在于内存中。

二、FIFO
FIFO，也称为命名管道，它是一种文件类型。
特点
FIFO可以在无关的进程之间交换数据，与无名管道不同。
FIFO有路径名与之相关联，它以一种特殊设备文件形式存在于文件系统中。

三、消息队列
消息队列，是消息的链接表，存放在内核中。一个消息队列由一个标识符（即队列ID）来标识。
特点
消息队列是面向记录的，其中的消息具有特定的格式以及特定的优先级。
消息队列独立于发送与接收进程。进程终止时，消息队列及其内容并不会被删除。
消息队列可以实现消息的随机查询,消息不一定要以先进先出的次序读取,也可以按消息的类型读取。

四、信号量
信号量（semaphore）与已经介绍过的 IPC 结构不同，它是一个计数器。信号量用于实现进程间的互斥与同步，而不是用于存储进程间通信数据。
1、特点
信号量用于进程间同步，若要在进程间传递数据需要结合共享内存。
信号量基于操作系统的 PV 操作，程序对信号量的操作都是原子操作。
每次对信号量的 PV 操作不仅限于对信号量值加 1 或减 1，而且可以加减任意正整数。
支持信号量组。

五、共享内存
共享内存（Shared Memory），指两个或多个进程共享一个给定的存储区。
1、特点
共享内存是最快的一种 IPC，因为进程是直接对内存进行存取。
因为多个进程可以同时操作，所以需要进行同步。
信号量+共享内存通常结合在一起使用，信号量用来同步对共享内存的访问。


什么是并发和并行？
并发是两个任务可以在重叠的时间段内启动，运行和完成。并行是任务在同一时间运行，例如，在多核处理器上。
并发是独立执行过程的组合，而并行是同时执行（可能相关的）计算。
并发是一次处理很多事情，并行是同时做很多事情。
应用程序可以是并发的，但不是并行的，这意味着它可以同时处理多个任务，但是没有两个任务在同一时刻执行。
应用程序可以是并行的，但不是并发的，这意味着它同时处理多核CPU中的任务的多个子任务。
一个应用程序可以即不是并行的，也不是并发的，这意味着它一次一个地处理所有任务。
应用程序可以即是并行的也是并发的，这意味着它同时在多核CPU中同时处理多个任务。


进程锁和线程锁的作用？
线程锁:大家都不陌生，主要用来给方法、代码块加锁。当某个方法或者代码块使用锁时，那么在同一时刻至多仅有有一个线程在执行该段代码。
当有多个线程访问同一对象的加锁方法/代码块时，同一时间只有一个线程在执行，其余线程必须要等待当前线程执行完之后才能执行该代码段。
但是，其余线程是可以访问该对象中的非加锁代码块的。

进程锁:也是为了控制同一操作系统中多个进程访问一个共享资源，只是因为程序的独立性，
各个进程是无法控制其他进程对资源的访问的，但是可以使用本地系统的信号量控制（操作系统基本知识）。

分布式锁:当多个进程不在同一个系统之中时，使用分布式锁控制多个进程对资源的访问。
分布式锁更详细的地方：https://www.cnblogs.com/Leo_wl/p/7513314.html
intsmaze说简单点，实现分布式锁必须要依靠第三方存储介质来存储锁的元数据等信息。
比如分布式集群要操作某一行数据时，这个数据的流水号是唯一的，那么我们就把这个流水号作为一把锁的id，
当某进程要操作该数据时，先去第三方存储介质中看该锁id是否存在，如果不存在，则将该锁id写入，然后执对该数据的操作；
当其他进程要访问这个数据时，会先到第三方存储介质中查看有没有这个数据的锁id,有的话就认为这行数据目前已经有其他进程在使用了，
就会不断地轮询第三方存储介质看其他进程是否释放掉该锁；当进程操作完该数据后，
该进程就到第三方存储介质中把该锁id删除掉，这样其他轮询的进程就能得到对该锁的控制。
范围大小:分布式锁——大于——进程锁——大于——线程锁。
只是范围越大技术复杂度就越大。


解释什么是异步非阻塞？
同步：执行一个操作之后，等待结果，然后才继续执行后续的操作。
异步：执行一个操作后，可以去执行其他的操作，然后等待通知再回来执行刚才没执行完的操作。
阻塞：进程给CPU传达一个任务之后，一直等待CPU处理完成，然后才执行后面的操作。
非阻塞：进程给CPU传达任我后，继续处理后续的操作，隔断时间再来询问之前的操作是否完成。这样的过程其实也叫轮询

阻塞、非阻塞、多路IO复用，都是同步IO，异步必定是非阻塞的，所以不存在异步阻塞和异步非阻塞的说法。真正的异步IO需要CPU的深度参与。
 换句话说，只有用户线程在操作IO的时候根本不去考虑IO的执行全部都交给CPU去完成，而自己只等待一个完成信号的时候，才是真正的异步IO。
 所以，拉一个子线程去轮询、去死循环，或者使用select、poll、epool，都不是异步。
 
 
 路由器与交换机的区别？
 A.工作层次不同：交换机比路由器更简单，路由器比交换器能获取更多信息
最初的的交换机是工作在OSI/RM开放体系结构的数据链路层，也就是第二层，而路由器一开始就设计工作在OSI模型的网络层。
由于交换机工作在OSI的第二层(数据链路层)，所以它的工作原理比较简单，而路由器工作在OSI的第三层(网络层)，
可以得到更多的协议信息，路由器可以做出更加智能的转发决策。

B.数据转发所依据的对象不同
交换机是利用物理地址或者说MAC地址来确定转发数据的目的地址。而路由器则是利用不同网络的ID号(即IP地址)来确定数据转发的地址。
IP地址是在软件中实现的，描述的是设备所在的网络，有时这些第三层的地址也称为协议地址或者网络地址。MAC地址通常是硬件自带的，
由网卡生产商来分配的，而且已经固化到了网卡中去，一般来说是不可更改的。而IP地址则通常由网络管理员或系统自动分配。

C.传统的交换机只能分割冲突域，不能分割广播域;而路由器可以分割广播域
由交换机连接的网段仍属于同一个广播域，广播数据包会在交换机连接的所有网段上传播，在某些情况下会导致通信拥挤和安全漏洞。
连接到路由器上的网段会被分配成不同的广播域，广播数据不会穿过路由器。
虽然第三层以上交换机具有VLAN功能，也可以分割广播域，但是各子广播域之间是不能通信交流的，它们之间的交流仍然需要路由器。

D.路由器提供了防火墙的服务
路由器仅仅转发特定地址的数据包，不传送不支持路由协议的数据包传送和未知目标网络数据包的传送，从而可以防止广播风暴。
最根本的区别是：交换机一般用于LAN-WAN的连接，交换机归于网桥，是数据链路层的设备，有些交换机也可实现第三层的交换。
路由器用于WAN-WAN之间的连接，可以解决异性网络之间转发分组，作用于网络层。


解释一下域名解析？
域名解析英文名：DNS (domain name resolution)
域名注册好之后，只说明你对这个域名拥有了使用权，在进行域名解析之后，这个域名才能发挥它的作用，
经过解析的域名可以作为网址访问自己的网站，也可以作为电子邮箱的后缀，因此“域名解析”是使用域名的必备环节。
注册域名之后如何才能看到自己的网站内容，用一个专业术语就叫“域名解析”。

人们都习惯记忆域名，但机器间互相只认 IP 地址，域名与 IP 地址之间是一 一对应的，
它们之间的转换工作称为域名解析，域名解析需要由专门的域名解析服务器来完成，解析过程是自动进行的。

如您在访问一个网站时，会输入网址 www.net.cn，之后即会显示对应的网站页面，这个情景在后台是什么样的呢？网站的内容所在服务器只有 IP 地址，
将域名与 IP 地址绑定（即域名解析），引导访问者获取网站服务器中的网页内容，即可实现输入网址进行网站访问。


如何修改本地hosts文件？
操作系统规定，在进行DNS请求以前，先检查系自己的Hosts文件中是否有这个域名和IP的映射关系。
如果有，则直接访问这个IP地址指定的网络位置，如果没有，再向已知的DNS服务器提出域名解析请求。
也就是说Hosts的IP解析优先级比DNS要高。
文件路径：C:\WINDOWS\system32\drivers\etc

在最后新增如下内容：
127.0.0.1 www.163.com
修改后用浏览器访问“www.163.com”会被解析到127.0.0.1，导致无法显示该网页。


生产者消费者模型应用场景及优势？
生产者与消费者模式是通过一个容器来解决生产者与消费者的强耦合关系，
生产者与消费者之间不直接进行通讯，而是利用阻塞队列来进行通讯，生产者生成数据后直接丢给阻塞队列，
消费者需要数据则从阻塞队列获取，实际应用中，生产者与消费者模式则主要解决生产者与消费者生产与消费的速率不一致的问题，
达到平衡生产者与消费者的处理能力，而阻塞队列则相当于缓冲区。

这就好比去学校食堂吃饭，食堂大妈并不会等你点了餐之后才立马去给你做，
而是先把饭菜做好了放在食堂窗口等你来自己取，而这个窗口就相当于阻塞队列，食堂大妈就是生产者，而学生就是消费者。

详细代码：https://blog.csdn.net/t894690230/article/details/50538285


什么是CDN？
CDN主要功能是在不同的地点缓存内容，通过负载均衡技术，
将用户的请求定向到最合适的缓存服务器上去获取内容，比如说，是北京的用户，我们让他访问北京的节点，
深圳的用户，我们让他访问深圳的节点。通过就近访问，加速用户对网站的访问。解决Internet网络拥堵状况，提高用户访问网络的响应速度。

与传统访问方式不同，CDN网络则是在用户和服务器之间增加缓存层，将用户的访问请求引导到最优的缓存节点而不是服务器源站点，从而加速访问速度。
总结一下CDN的工作原理：通过权威DNS服务器来实现最优节点的选择，通过缓存来减少源站的压力。


LVS的作用是什么？
 LVS 是 Linux  Virtual Server ，Linux 虚拟服务器；是一个虚拟的服务器集群【多台机器 LB IP】。LVS 集群分为三层结构:
负载调度器(load balancer)：它是整个LVS 集群对外的前端机器，负责将client请求发送到一组服务器[多台LB IP]上执行，
                          而client端认为是返回来一个同一个IP【通常把这个IP 称为虚拟IP/VIP】
服务器池(server pool)：一组真正执行client 请求的服务器，一般是我们的web服务器；除了web，还有FTP，MAIL，DNS
共享存储(shared stored)：它为 server pool 提供了一个共享的存储区，很容易让服务器池拥有相同的内容，提供相同的服务[不是很理解]
详细链接：https://blog.csdn.net/caoshuming_500/article/details/8291940

什么是Nginx
在传统的Web项目中，并发量小，用户使用的少。
所以在低并发的情况下，用户可以直接访问tomcat服务器，然后tomcat服务器返回消息给用户。比如，我们上传图片

当然我们知道，为了解决并发，可以使用负载均衡：也就是我们多增加几个tomcat服务器。
当用户访问的时候，请求可以提交到空闲的tomcat服务器上。
并发量高，用户多。
但是这种情况下可能会有一种这样的问题：上传图片操作。我们把图片上传到了tomcat1上了，当我们要访问这个图片的时候，
tomcat1正好在工作，所以访问的请求就交给其他的tomcat操作，而tomcat之间的数据没有进行同步，所以就发生了我们要请求的图片找不到。

为了解决这种情况，我们就想出了分布式。我们专门建立一个图片服务器，用来存储图片。
这样当我们都把图片上传的时候，不管是哪个服务器接收到图片，都把图片上传到图片服务器。
图片服务器上需要安装一个http服务器，可以使用tomcat、apache、nginx。

既然我们要选择的是http服务器，为什么不继续使用tomcat，而要使用Nginx？
原因如下：
nginx常用做静态内容服务和代理服务器（不是你FQ那个代理），
直面外来请求转发给后面的应用服务（tomcat，django什么的），
tomcat更多用来做做一个应用容器，让java web app跑在里面的东西，对应同级别的有jboss,jetty等东西。

我们可以了解到Nginx是一个http服务器。是一个使用c语言开发的高性能的http服务器及反向代理服务器。
Nginx是一款高性能的http 服务器/反向代理服务器及电子邮件（IMAP/POP3）代理服务器。
由俄罗斯的程序设计师Igor Sysoev所开发，官方测试nginx能够支支撑5万并发链接，并且cpu、内存等资源消耗却非常低，运行非常稳定。

Nginx的应用场景
 http服务器。Nginx是一个http服务可以独立提供http服务。可以做网页静态服务器。
 虚拟主机。可以实现在一台服务器虚拟出多个网站。例如个人网站使用的虚拟主机。
 反向代理，负载均衡。当网站的访问量达到一定程度后，单台服务器不能满足用户的请求时，需要用多台服务器集群可以使用nginx做反向代理。
并且多台服务器可以平均分担负载，不会因为某台服务器负载高宕机而某台服务器闲置的情况。


keepalived是什么及作用？
keepalived是一个类似于Layer2,4,7交换机制的软件。是Linux集群管理中保证集群高可用的一个服务软件，其功能是用来防止单点故障。
keepalived是基于VRRP协议实现的保证集群高可用的一个服务软件，主要功能是实现真机的故障隔离和负载均衡器间的失败切换，防止单点故障。
在了解keepalived原理之前先了解一下VRRP协议。
Virtual Route Redundancy Protocol虚拟路由冗余协议。
是一种容错协议，保证当主机的下一跳路由出现故障时，由另一台路由器来代替出现故障的路由器进行工作，从而保持网络通信的连续性和可靠性。
虚拟路由器：由一个 Master 路由器和多个 Backup 路由器组成。主机将虚拟路由器当作默认网关。
VRID：虚拟路由器的标识。有相同 VRID 的一组路由器构成一个虚拟路由器。
Master 路由器：虚拟路由器中承担报文转发任务的路由器。
Backup 路由器： Master 路由器出现故障时，能够代替 Master 路由器工作的路由器。
虚拟 IP 地址：虚拟路由器的 IP 地址。一个虚拟路由器可以拥有一个或多个IP 地址。
IP 地址拥有者：接口 IP 地址与虚拟 IP 地址相同的路由器被称为 IP 地址拥有者。
虚拟 MAC 地址：一个虚拟路由器拥有一个虚拟 MAC 地址。虚拟 MAC 地址的格式为 00-00-5E-00-01-{VRID}。
通常情况下，虚拟路由器回应 ARP 请求使用的是虚拟 MAC 地址，只有虚拟路由器做特殊配置的时候，才回应接口的真实 MAC 地址。

优先级： VRRP 根据优先级来确定虚拟路由器中每台路由器的地位。
非抢占方式：如果 Backup 路由器工作在非抢占方式下，则只要 Master 路由器没有出现故障，
           Backup 路由器即使随后被配置了更高的优先级也不会成为Master 路由器。
抢占方式：如果 Backup 路由器工作在抢占方式下，当它收到 VRRP 报文后，会将自己的优先级与通告报文中的优先级进行比较。
         如果自己的优先级比当前的 Master 路由器的优先级高，就会主动抢占成为 Master 路由器；否则，将保持 Backup 状态。
  
 VRRP将局域网内的一组路由器划分在一起，形成一个VRRP备份组，它在功能上相当于一台路由器的功能，使用虚拟路由器号进行标识（VRID）。
 虚拟路由器有自己的虚拟IP地址和虚拟MAC地址，它的外在变现形式和实际的物理路由完全一样。
 局域网内的主机将虚拟路由器的IP地址设置为默认网关，通过虚拟路由器与外部网络进行通信。
 
 虚拟路由器是工作在实际的物理路由器之上的。它由多个实际的路由器组成，包括一个Master路由器和多个Backup路由器。
 Master路由器正常工作时，局域网内的主机通过Master与外界通信。
 当Master路由器出现故障时， Backup路由器中的一台设备将成为新的Master路由器，接替转发报文的工作。（路由器的高可用）
 
 VRRP的工作工程：
(1) 虚拟路由器中的路由器根据优先级选举出 Master。 Master 路由器通过发送免费 ARP 报文，
    将自己的虚拟 MAC 地址通知给与它连接的设备或者主机，从而承担报文转发任务；
(2) Master 路由器周期性发送 VRRP 报文，以公布其配置信息（优先级等）和工作状况；
(3) 如果 Master 路由器出现故障，虚拟路由器中的 Backup 路由器将根据优先级重新选举新的 Master；
(4) 虚拟路由器状态切换时， Master 路由器由一台设备切换为另外一台设备，
    新的 Master 路由器只是简单地发送一个携带虚拟路由器的 MAC 地址和虚拟 IP地址信息的ARP 报文，
    这样就可以更新与它连接的主机或设备中的ARP 相关信息。网络中的主机感知不到 Master 路由器已经切换为另外一台设备。
(5) Backup 路由器的优先级高于 Master 路由器时，由 Backup 路由器的工作方式（抢占方式和非抢占方式）决定是否重新选举 Master。
VRRP优先级的取值范围为0到255（数值越大表明优先级越高）
'''
