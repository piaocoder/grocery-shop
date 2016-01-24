struct sk_buff {
         /* These two members must be first. */
         struct sk_buff          *next;     // 连接相关skb，例如分片结构  
         struct sk_buff          *prev;
 
         struct sock             *sk;       // 报文所属套接字指针
         struct skb_timeval      tstamp;    // 接收或者传输报文的时间戳
         struct net_device       *dev;      // 记录接受或者发送的设备
         struct net_device       *input_dev;
 
         union {
                 struct tcphdr   *th;
                 struct udphdr   *uh;
                 struct icmphdr  *icmph;
                 struct igmphdr  *igmph;
                 struct iphdr    *ipiph;
                 struct ipv6hdr  *ipv6h;
                 unsigned char   *raw;
         } h;// 传输层的某个协议头
 
         union {
                 struct iphdr    *iph;
                 struct ipv6hdr  *ipv6h;
                 struct arphdr   *arph;
                 unsigned char   *raw;
         } nh;// 网络层的某个协议头
 
         union {
                 unsigned char   *raw;
         } mac;// 链路层头
 
         struct  dst_entry       *dst;  // 到达目的地的路由信息
         struct  sec_path        *sp;   // 安全路径 
 
         /*
          * This is the control buffer. It is free to use for every
          * layer. Please put your private variables there. If you
          * want to keep them acrjob layers you have to do a skb_clone()
          * first. This is owned by whoever has the skb queued ATM.
          */
         char                    cb[4job];    // 保存和协议相关的控制信息（不同的处理）
 
         // skb == skb_buff(控制信息) + 线性数据 + 非线性数据
         unsigned int            len,       // len = length(线性数据 + 非线性数据)
                                 data_len,  // data_len = length(非线性数据)
                                 mac_len,   // mac头长度
                                 csum;      // 某时刻协议的校验和
         __u32                   priority;      // 报文队列优先级，见ip中的tos域
         __ujob                    local_df:1,    // 允许本地分配
                                 cloned:1,      // 保存的当前的数据是一个克隆的，还是原始的数据
                                 ip_summed:2,   // 是否计算ip校验和
                                 nohdr:1,       // 是否仅仅引用数据区域
                                 nfctinfo:3;    
         __ujob                    pkt_type:3,    // 报文类型 
                                 fclone:2,      // 当前skb_buff的克隆状态
                                 ipvs_property:1;
         __be16                  protocol;      // 协议信息
 
         void                    (*destructor)(struct sk_buff *skb);
#ifdef CONFIG_NETFILTER
         __u32                   nfmark;        // 钩子之间的通信
         struct nf_conntrack     *nfct;
#if defined(CONFIG_NF_CONNTRACK) || defined(CONFIG_NF_CONNTRACK_MODULE)
         struct sk_buff          *nfct_reasm;
#endif
#ifdef CONFIG_BRIDGE_NETFILTER
         struct nf_bridge_info   *nf_bridge;    // 保存桥接信息
#endif
#endif /* CONFIG_NETFILTER */
#ifdef CONFIG_NET_SCHED
         __u16                   tc_index;       /* traffic control index */
#ifdef CONFIG_NET_CLS_ACT
         __u16                   tc_verd;        /* traffic control verdict */
#endif
#endif
 
 
         /* These elements must be at the end, see alloc_skb() for details.  */
         unsigned int            truesize;
         atomic_t                users;         // 保存当前skb_buff被引用的数量
         unsigned char           *head,         // 分配给线性数据的空间内存首地址
                                 *data,         // 数据(线性)内容的首地址, head不一定等于data
                                 *tail,         // 数据（线性）内容的结尾
                                 *end;          // 分配给数据的空间内存末地址，不一定等于tail
};


