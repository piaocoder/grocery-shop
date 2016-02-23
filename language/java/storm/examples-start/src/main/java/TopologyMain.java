import java.util.*;

import spouts.WordReader;
import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.tuple.Fields;
import bolts.WordCounter;
import bolts.WordNormalizer;
/**
 * @file TopologyMain.java
 * @brief   
 *          
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-18
 */


/**
 * @brief   主类
 * @note
 *      1，所有拓扑节点的各个进程必须独立运行，不依赖共享数据，从而
 *          保证真实集群环境（不同的机器）可以顺利运行
 *      2，spout和bolts之间：
 *          使用shuffleGrouping方法连接，word-reader域 --》 word-normalizer
 *          从而使storm以随机分配方式从源节点向目标节点发送消息
 */
public class TopologyMain {
	public static void main(String[] args) throws InterruptedException {
         
        // Topology definition
        // new Fields()——相同的单词问题发送给同一个WordCounter
        // 随机数据流组：
        //          builder.setBolt(组名A，数据源组件).shuffleGrouping(..)，
        //          其中数据源组件中的信息随机派发到组名A中
        //
        // 域数据流组：
        //          builder.setBold(组名B，数据源组件).fieldsGrouping(..)
        //          根据域来为数据流分组
        //          1，word域必须在数据源组件中进行域声明，见WordNormalizer
        //              中的declareOutputFields函数
        //          2，域数据流数组中所有域集合必须在数据源的域声明中
        //
        // 全部数据流组：
        //          1，向所有的接收数据实例bolts发送信号
        //          2，接收实例调用input.getSourceStreamid()来判断源组件ID
        //          3，调用：
        //              builder.setBolt("word-counter", new WordCounter(),2)
        //                  .fieldsGrouping("word-normalizer",new Fields("word"))
        //                  .allGrouping("signals-spout","signals");
        //
        // 自定义数据流组：
        //          1，自定义数据流组，自由决定bolt接收的数据元祖
        //          2，例如修改Fields("word")为"使首字母相同的单词"由同样的
        //              bolt接收（非常有用）
        //          3，调用：
        //              builder.setBolt("word-normalizer", new WordNormalizer())
        //                  .customGrouping("word-reader", new ModuleGrouping());
        //          4，其中ModuleGrouping为自定义类
        //
        // 直接数据流组：
        //          1，直接决定哪个组件能够接收元祖，其他组件没有机会
        //          2，emitDirect方法：
        //              collertor.emitDirect(getWordCounterIndex(word), 
        //                  new Values(word));
        //              其中重点是getWordCounterIndex函数，返回Task号
        //          3，拓扑定义：
        //              builder.setBolt("word-counter", new WordCounter(),2)
        //                  .directGrouping("word-normalizer");
        //          4，setSpout和setBolt用于设置executor的数量
        //
		TopologyBuilder builder = new TopologyBuilder();
		builder.setSpout("word-reader",new WordReader());
		builder.setBolt("word-normalizer", new WordNormalizer())
            .shuffleGrouping("word-reader");
		builder.setBolt("word-counter", new WordCounter(),2)
            .fieldsGrouping("word-normalizer", new Fields("word"));
		
        // Configuration
        // 功能：创建包含拓扑配置的Config对象:
        //      运行时和集群配置合并
        //      利用prepare方法，将配置发送到所有节点中（全局初始化操作）
        //      1,setNumWorkers，设置workers的数量
        //      2,获取配置(storm.yaml)
        //      3,setNumTasks(Number val)设置每一个组件需要的执行任务数
        //          即每一个executor线程中的task数量
        // args[0]值："src/main/resources/words.txt"
		Config conf = new Config();
        conf.setNumWorkers(2);
		conf.put("wordsFile", args[0]);
		conf.setDebug(false);

        // Topology run
        // 使用LocalCluster运行该拓扑，在生产环境中，拓扑是会持续运行
        // 1，创建拓扑
        // 2，运行拓扑
		conf.put(Config.TOPOLOGY_MAX_SPOUT_PENDING, 1);
		LocalCluster cluster = new LocalCluster();
		cluster.submitTopology("Getting-Started-Toplogie", 
                conf, builder.createTopology());
		Thread.sleep(1000*5);

        // 关闭集群
        // 测试cleanup是否仅仅在shutdown之后才调用
        System.out.println("TopologyMain进程准备退出咯!");
		cluster.shutdown();
	}
}
