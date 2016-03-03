;;ns-namespace
(ns wordcount
  (:use     [streamparse.specs])
  (:gen-class))

; 因为config.json不能添加注释，添加注释在该处
;Must have ssh access to all servers in your Storm cluster
;"use_ssh_for_nimbus": true,
;Must have write access to the virtualenv_root 
;on all servers in your Storm cluster
;"virtualenv_root": "/data/virtualenvs/"

;;defn-function，定义topology结构并存储函数名称
;;1,wordcount必须返回一个array，其中数组中包含两个字典
(defn wordcount [options]
   [
    ;; 0,定义两个spout，告知storm，其中
    ;; 1,函数python-spout-spec会使用options映射python路径
    ;; 2,定义了一个域sentence
    ;; 3,其中:p 2表示并发数为2
    ;{"sentence-spout-1" (shell-spout-spec
    {"sentence-spout-1" (python-spout-spec
                        options
                        "spouts.sentencespout.SentenceSpout"
                        ;["/apps/python/bin/python" "SentenceSpout.py"]
                        ["word"]
                        :p 2)
     ;"sentence-spout-2" (shell-spout-spec
                        ;options
                        ;"spouts.sentencespout.OtherSentenceSpout"
                        ;["sentence"])
     }

    ;; 随机数据流组
    {"sentence-splitter" (python-bolt-spec
                        ;; topology options passed in
                        options
                        ;; inputs, where does this bolt recieve it's tuples from?
                        ;{"sentence-spout-1" :shuffle
                         ;"sentence-spout-2" :shuffle}
                        {"sentence-spout-1" :shuffle}
                        ;; class to run
                        "bolts.sentencebolt.SentenceSplitterBolt"
                        ;; output spec, what tuples does this bolt emit?
                        ["word"]
                        ;; configuration parameters
                        :p 2)
     "word-counter" (python-bolt-spec
                        options
                        ;; 使用域
                        ;; recieves tuples from "sentence-splitter", 
                        ;; grouped by word
                        {"sentence-splitter" ["word"]}
                        "bolts.wordcount.WordCounter"
                        ["word" "count"])
     "word-count-saver" (python-bolt-spec
                         ;; topology options passed in
                         options
                         {"word-counter" :shuffle}
                         "bolts.wordcount.WordSaver"
                         ;; does not emit any fields
                         [])
     }
  ]
)
