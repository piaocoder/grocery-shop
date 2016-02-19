package spouts;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.Map;
import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

public class WordReader extends BaseRichSpout {

	private SpoutOutputCollector collector;
	private FileReader fileReader;
	private boolean completed = false;

    /**
     * @brief   ack :周期性的调用nextTuple
     *
     * @param   msgId
     *
     * @return  
     */
	public void ack(Object msgId) {
		System.out.println("OK:"+msgId);
	}

	public void close() {}

    /**
     * @brief   fail :周期性的调用nextTuple
     *
     * @param   msgId
     *
     * @return  
     */
	public void fail(Object msgId) {
		System.out.println("FAIL:"+msgId);
	}

    /**
     * @brief   nextTuple :
	 *              The only thing that the methods will do It is emit each 
	 *              file line（分发文件中的文本行）
     *          功能：通过该函数，向bolts发布待处理的数据
     *              本例功能：
     *                  读取文件，逐行发布数据
     *          调用者：
     *              在同一个循环内被ack()和fail()周期性调用
     *
     * @return  
     */
	public void nextTuple() {
		/**
		 * The nextuple it is called forever, so if we have been readed the file
		 * we will wait and then return（不断调用，直到文件读完）
		 */
		if(this.completed){
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				//Do nothing
			}
			return;
		}

		String str;
		//Open the reader
		BufferedReader reader = new BufferedReader(fileReader);
		try{
			//Read all lines
			while((str = reader.readLine()) != null){
				/**
				 * By each line emmit a new value with the line as a their
                 * Values:ArrayList结构体，元素-传入构造器的参数-str
				 */
				this.collector.emit(new Values(str),str);
			}

		}catch(Exception e){
			throw new RuntimeException("Error reading tuple",e);
		}finally{
			this.completed = true;
		}
	}

    /**
     * @brief   open:We will create the file and get the collector object
     *          相当于一个初始化操作，创建fd，创建collector，创建context
     *
     * @param   conf：配置对象，在定义topology对象时创建
     * @param   context：包含所有的拓扑数据
     * @param   collector：发布交给bolts处理的数据，见nextTuple元祖，
     *                  该对象在bolts中的execute中调用（ack/fail）
     *
     * @return  
     */
	public void open(Map conf, TopologyContext context,
			SpoutOutputCollector collector) {
		try {
			this.fileReader = new FileReader(conf.get("wordsFile").toString());

		} catch (FileNotFoundException e) {
			throw new RuntimeException("Error reading file [" 
                    + conf.get("wordFile")+"]");
		}
        
		this.collector = collector;
	}

	/**
	 * Declare the output field "word"
	 */
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("line"));
	}
}
