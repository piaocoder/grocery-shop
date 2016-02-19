package com;

// 导入java包
import java.io.*;
import bamboo.TestBambooSecond;

class BambooBook {
    /*
     * 测试枚举类型
     */
    enum BookLevel {
        SMALL,
        MEDIUM,
        LARGE,
    }
    BookLevel bookEnum;
}

/*
 * 1，一个源文件仅仅存在一个公共类
 * 2，public类必须和源文件保持同样的名称
 */
public class HelloWorld  {
    /*
     * 类变量（静态变量）
     * 1,类变量存放在类全局内存空间中，每一个类都仅仅存在一份
     * 2,一般声明为public
     * 3,通过ClassName.VariableName访问
     * 4,如果声明为final（变量在初始化后不再改变、方法不被重写，类不能有子类）
     *   则必须首字母大写，例如：
     *      public static final Planet = "Earth";
     */
    public static final String Planet = "Earth";
    public static double salary;

    /*
     * 实例变量，默认为public(另见default)
     *      public:对所有类可见
     *      private:对子类不可见
     *      default:在同一个包内可见（不同于C++）
     *
     * 1,所有的实例变量均存在默认值（局部变量没有）
     *
     */
    public String  ownerName;
    int     age;                // 年龄，默认为0

    // default类型
    int     AdultAge = 10;

    /*
     * 构造函数
     */
    public HelloWorld(String name) {
        this.ownerName = name;
        AdultAge = 19;
        salary = 100;
    }

    public void hostAge(int age) {
        this.age = age;
    }

    /*
     * 打印消息
     */
    public void display() {
        System.out.println("Host name:" + this.ownerName);
        System.out.println("Adult age:" + AdultAge);
        System.out.println("Host age:" + this.age);
        System.out.println("Salary:" + salary);
        System.out.println();
    }

    /*
     * 打印主人用到的数据类型
     */
    public void displayDataType() {
        // byte  
        System.out.println("基本类型：byte 二进制位数：" + Byte.SIZE);  
        System.out.println("包装类：java.lang.Byte");  
        System.out.println("最小值：Byte.MIN_VALUE=" + Byte.MIN_VALUE);  
        System.out.println("最大值：Byte.MAX_VALUE=" + Byte.MAX_VALUE);  
        System.out.println();  
  
        // short  
        System.out.println("基本类型：short 二进制位数：" + Short.SIZE);  
        System.out.println("包装类：java.lang.Short");  
        System.out.println("最小值：Short.MIN_VALUE=" + Short.MIN_VALUE);  
        System.out.println("最大值：Short.MAX_VALUE=" + Short.MAX_VALUE);  
        System.out.println();  
  
        // int  
        System.out.println("基本类型：int 二进制位数：" + Integer.SIZE);  
        System.out.println("包装类：java.lang.Integer");  
        System.out.println("最小值：Integer.MIN_VALUE=" + Integer.MIN_VALUE);  
        System.out.println("最大值：Integer.MAX_VALUE=" + Integer.MAX_VALUE);  
        System.out.println();  
  
        // long  
        System.out.println("基本类型：long 二进制位数：" + Long.SIZE);  
        System.out.println("包装类：java.lang.Long");  
        System.out.println("最小值：Long.MIN_VALUE=" + Long.MIN_VALUE);  
        System.out.println("最大值：Long.MAX_VALUE=" + Long.MAX_VALUE);  
        System.out.println();  
  
        // float  
        System.out.println("基本类型：float 二进制位数：" + Float.SIZE);  
        System.out.println("包装类：java.lang.Float");  
        System.out.println("最小值：Float.MIN_VALUE=" + Float.MIN_VALUE);  
        System.out.println("最大值：Float.MAX_VALUE=" + Float.MAX_VALUE);  
        System.out.println();  
  
        // double  
        System.out.println("基本类型：double 二进制位数：" + Double.SIZE);  
        System.out.println("包装类：java.lang.Double");  
        System.out.println("最小值：Double.MIN_VALUE=" + Double.MIN_VALUE);  
        System.out.println("最大值：Double.MAX_VALUE=" + Double.MAX_VALUE);  
        System.out.println();  
  
        // char  
        System.out.println("基本类型：char 二进制位数：" + Character.SIZE);  
        System.out.println("包装类：java.lang.Character");  
        // 以数值形式而不是字符形式将Character.MIN_VALUE输出到控制台  
        System.out.println("最小值：Character.MIN_VALUE="  
                + (int) Character.MIN_VALUE);  
        // 以数值形式而不是字符形式将Character.MAX_VALUE输出到控制台  
        System.out.println("最大值：Character.MAX_VALUE="  
                + (int) Character.MAX_VALUE);
    }

    /*
     * console IO操作:
     * 1，获取控制台输入：是对"字符流"的操作，即对BufferedReader
     * 2，控制台输出：是对"字节流"的操作，即printString的操作
     * 3，输出三个函数：
     *      System.out.print()
     *      System.out.println()
     *      System.out.write()
     *
     */
    public void displayToConsole() throws IOException {
        // 创建BufferedReader
        BufferedReader br = new BufferedReader(
                new InputStreamReader(System.in));
        String str;

        do {
            str = br.readLine();
            System.out.println(str);
        }while (!str.equals("quit"));
    }

    /*
     * main 方法
     */
    public static void main(String []args) {
        BambooBook book = new BambooBook();
        System.out.println("My medium book level is :" + book.bookEnum.MEDIUM);

        // 测试HelloWorld主类
        HelloWorld helloWorld = new HelloWorld("bamboo");
        System.out.println("Planet:"+HelloWorld.Planet);
        helloWorld.display();
        //helloWorld.displayDataType();

        System.out.println("Test Package import or other!");
        TestBambooSecond sobj = TestBambooSecond();
        sobj.display();
    }
}
