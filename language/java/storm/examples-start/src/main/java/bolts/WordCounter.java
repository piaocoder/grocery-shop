package bolts;

import java.util.HashMap;
import java.util.Map;

import backtype.storm.task.TopologyContext;
import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Tuple;


/**
 * @brief   单词计数，拓扑结束时将调用cleanup()，一般会在这个bolts
 *          中将数据存入DB中，该例子没有
 */
public class WordCounter extends BaseBasicBolt {
	Integer                 id;
	String                  name;
	Map<String, Integer>    counters;

	/**
	 * At the end of the spout (when the cluster is shutdown
	 * We will show the word counters
     * 当前例子：拓扑结束、spout结束或者集群关闭时，显示单词数量
     * 通常情况：关闭活动的连接，其他资源
     * 在cluster.shutdown()时才会调用哦
	 */
	@Override
	public void cleanup() {
        System.out.println("===============================");
        System.out.println("拓扑结束，打印各个数据信息:");
		System.out.println("-- Word Counter ["+name+"-"+id+"] --");
		for(Map.Entry<String, Integer> entry : counters.entrySet()){
			System.out.println(entry.getKey()+": "+entry.getValue());
		}
        System.out.println("===============================");
	}

	/**
	 * On create，仅在bolt开始处理元祖之前调用
	 */
	@Override
	public void prepare(Map stormConf, TopologyContext context) {
		this.counters = new HashMap<String, Integer>();
		this.name = context.getThisComponentId();
		this.id = context.getThisTaskId();
	}

    /**
     * @brief   declareOutputFields
     *
     * @param   declarer
     *
     * @return  
     */
	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {}


    /**
     * @brief   execute :收到Tuple后的回调函数
     *
     * @param   input
     * @param   collector
     *
     * @return  
     */
	@Override
	public void execute(Tuple input, BasicOutputCollector collector) {
		String str = input.getString(0);
		/**
		 * If the word dosn't exist in the map we will create
		 * this, if not We will add 1 
		 */
		if(!counters.containsKey(str)){
			counters.put(str, 1);
		}else{
			Integer c = counters.get(str) + 1;
			counters.put(str, c);
		}
	}
}
