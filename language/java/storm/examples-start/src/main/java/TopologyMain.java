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
 *      1，使用moven时必须先初始化：
 *          mvn -f pom.xml clean install
 *          mvn exec:java -Dexec.mainClass="TopologyMain" 
 *              -Dexec.args="src/main/resources/words.txt"
 *          
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-18
 */


public class TopologyMain {
	public static void main(String[] args) throws InterruptedException {
         
        //Topology definition
		TopologyBuilder builder = new TopologyBuilder();
		builder.setSpout("word-reader",new WordReader());
		builder.setBolt("word-normalizer", new WordNormalizer())
			.shuffleGrouping("word-reader");
		builder.setBolt("word-counter", new WordCounter(),1)
			.fieldsGrouping("word-normalizer", new Fields("word"));
		
        //Configuration
		Config conf = new Config();
		conf.put("wordsFile", args[0]);
		conf.setDebug(false);
        //Topology run
		conf.put(Config.TOPOLOGY_MAX_SPOUT_PENDING, 1);
		LocalCluster cluster = new LocalCluster();
		cluster.submitTopology("Getting-Started-Toplogie", conf, builder.createTopology());
		Thread.sleep(1000);
		cluster.shutdown();
	}
}
