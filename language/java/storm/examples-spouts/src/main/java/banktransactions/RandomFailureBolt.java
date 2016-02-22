package banktransactions;

import java.util.Map;
import java.util.Random;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;

public class RandomFailureBolt extends BaseRichBolt {

	private static final Integer MAX_PERCENT_FAIL = 80;
	Random random = new Random();
	private OutputCollector collector;
	
    /**
     * @brief   execute :必须主动调用ack和fail方法哦，如果不主动调用
     *              可能造成内存耗尽哦
     *
     * @param   input
     *
     * @return  
     */
	public void execute(Tuple input) {
		Integer r = random.nextInt(100);
		if(r > MAX_PERCENT_FAIL){
			collector.ack(input);
		}else{
			collector.fail(input);
		}

	}

	public void prepare(Map stormConf, TopologyContext context,
			OutputCollector collector) {
		this.collector = collector;
	}

	public void declareOutputFields(OutputFieldsDeclarer declarer) {
	}

}
