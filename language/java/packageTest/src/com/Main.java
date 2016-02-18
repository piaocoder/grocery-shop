package com;

import java.io.*;    
import com.TestB;
import baz.TestBaz;

/**
 * @file Main.java
 * @brief   java java/javac路径查找测试，涉及到classpath以及sourcepath
 *          参考：http://talentluke.iteye.com/blog/1969442
 * @author unlessbamboo
 * @version 1.0
 * @date 2016-02-18
 */

    
/**
 * @brief   编译时出现以下问题以及分析
 *          1，Main.java不在src.com目录下时：
 *              问题：编译成功，执行失败，找不到src/com/Main类名
 *              原因：
 *                  java在执行时会默认在CLASSPATH下寻找src/com/Main.class；
 *                  此时Main类名变为src.com.Main(fully-qualifed class name)机制；
 *              解决办法：
 *                  a) 将生成的TestB.class，Main.class直接拷贝到src/com/
 *                      目录下面（二进制嘛）
 *                  b) 运行java src.com.Main成功
 *              PS:注意，此时的目录结构为
 *                  ├── Main.java
 *                  └── src
 *                      └── com
 *          
 *          2，将TestB类移出Main.java文件，重新编译
 *              问题：编译失败
 *              原因：
 *                  javac在当前翻译单元找不到类B之后，会到包src.com中寻找，
 *                  此时出现两种情况：
 *                      src/com/TestB.class存在——直接使用，该条件是前提（不像pyc）
 *                      src/com/TestB.class不存在——编译TestB.java，最后导入
 *              解决办法：
 *                  移动TestB.java到src/com中；
 *                  照旧拷贝Main.class到src/com;
 *                  运行：java src.com.Main;
 *              目录拓扑：
 *                  .
 *                  ├── Main.java
 *                  ├── src
 *                  │   └── com
 *                  └── TestB.java
 *                  以及
 *                  .
 *                  ├── Main.java
 *                  └── src
 *                      └── com
 *                              └── TestB.java
 *              CLASSPATH变量：
 *                  类似于PYTHONPATH，如果没有设置，默认为'.'目录，其他未系统路径
 *
 *          3，如果将Main.java以及TestB.java都拷贝到src/com目录下面，
 *              并且更改package名为（从src.com变为com），会发生什么情况？
 *              问题：
 *                  javac src/com/Main.java无法编译通过
 *              解决：
 *                  javac -sourcepath src src/com/Main.java
 *                  java -classpath src com.Main
 *              PS:尽可能删除前面的class哦
 *
 *         4，如果增加-d选项，同样会发生类似的问题，此时需要执行的命令为：
 *              javac -d bin -sourcepath src src/com/Main.java
 *              java -classpath bin com.Main
 *
 *         5，增加一个新的baz/TestBaz.java并应用之后，出人以外的不用做
 *              任何其他操作，其实也是，只不过自己有点怕了
 *              javac -d bin -sourcepath src src/com/Main.java
 *              java -classpath bin com.Main
 *              路径：
 *                  .
 *                  ├── bin
 *                  │   ├── baz
 *                  │   │   └── TestBaz.class
 *                  │   └── com
 *                  │       ├── Main.class
 *                  │       └── TestB.class
 *                  └── src
 *                      ├── baz
 *                          │   └── TestBaz.java
 *                              └── com
*                                      ├── Main.java
*                                              └── TestB.java
 *
 */
public class Main {    

    static TestB bobj = new TestB ();    

    /**
     * @brief   main 
     *
     * @param   args
     *
     * @return  
     */
    public static void main (String[] args) throws IOException {    
        System.out.println("I am class Main.");    
        bobj.say();    

        TestBaz baz = new TestBaz();
        baz.say();
    }    
}    
    

//class TestB {    
    //public void say ()    
    //{    
        //System.out.println("I am class TestB.");    
    //}    
//}    
