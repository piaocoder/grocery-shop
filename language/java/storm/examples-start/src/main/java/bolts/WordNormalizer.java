package bolts;

import backtype.storm.topology.BasicOutputCollector;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseBasicBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

/**
 * @brief   负责得到spout发来的数据;
 *          标准化每行文本，并切割文本行为单词；
 *          发布若干分组；
 */
public class WordNormalizer extends BaseBasicBolt {

    /**
     * @brief   cleanup :bolt即将关闭时调用
     *
     * @return  
     */
	@Override
	public void cleanup() {
        System.out.println("===============================");
        System.out.println("===============================");
        System.out.println("WordNormalizer Bolts刷刷存在感！");
        System.out.println("===============================");
        System.out.println("===============================");
    }

    /**
     * @brief   execute :每次接收到元祖信息时回调，之后发布若干元祖
     *                  元祖数量可能为（0,1,n）
	 *      The bolt will receive the line from the
	 *      words file and process it to Normalize this line
	 *      
	 *      The normalize will be put the words in lower case
	 *      and split the line to get all words in this 
     *
     * @param   input：Tuple是一个具名值列表，可是任何可序列化对象，
     *              例如：字符串、字节数组、ArrayList、HashMap等
     * @param   collector：可以不存在该参数
     *
     * @return  
     */
	public void execute(Tuple input, BasicOutputCollector collector) {
        String sentence = input.getString(0);
        String[] words = sentence.split(" ");

        // 分割、大写转小写、去除头尾空格
        for(String word : words){
            word = word.trim();
            if(!word.isEmpty()){
                word = word.toLowerCase();
                collector.emit(new Values(word));
            }
        }
        // 之后默认会对元祖做相应应答，collector.ack()，默认调用
        // collector.ack(input)
	}
	

    /**
     * @brief   declareOutputFields :为bolt声明输出模式，出参
	 *          The bolt will only emit the field "word" 
     *
     * @param   declarer
     *
     * @return  
     */
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
        // 表示该bolts仅仅发布word域
		declarer.declare(new Fields("word"));
	}
}
