#include "io.h"

#define ALARM_EMAIL_SERVER_POLICY  \
    "                   <tr> \n \
                        <td bgcolor=\"#ffffff\" style=\"padding: 20px 30px 20px 30px;\">\n \
                            <table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%%\">\n \
                                <tr> \n \
                                    <td style=\"padding: 0;\">\n \
                                        <table border=\"1\" cellpadding=\"0\" cellspacing=\"0\" width=\"100%%\">\n \
                                            <tr>\n \
                                                <td></td>\n \
                                                <td style=\"color: #153643; font-family: Arial, sans-serif; font-size: 15px;\">\n \
                                                    <b>服务器策略</b>\n \
                                                </td>\n \
                                                <td style=\"color: #153643; font-family: Arial, sans-serif; font-size: 15px;\">\n \
                                                    <b>告警策略</b>\n \
                                                </td>\n \
                                            </tr>\n \
                                            <tr>\n \
                                                <td></td>\n \
                                                <td>%s</td>\n \
                                                <td>%s</td>\n \
                                            </tr> \n \
                                            <tr>\n \
                                                <td style=\"color: #153643; font-family: Arial, sans-serif; font-size: 15px;\">\n \
                                                    <b>攻击类型</b>\n \
                                                </td>\n \
                                                <td style=\"color: #153643; font-family: Arial, sans-serif; font-size: 15px;\">\n \
                                                    <b>告警等级</b>\n \
                                                </td>\n \
                                                <td style=\"color: #153643; font-family: Arial, sans-serif; font-size: 15px;\">\n \
                                                    <b>攻击次数</b>\n \
                                                </td>\n \
                                            </tr>\n "

#define DEST_FILE   "dest.file"
/*
 * 功能:向文件中写入数据
 * 注意:必须保证缓冲区内存充足，否则出现段错误
 */
int
test_fprintf_func()
{
    char                        desc[4096]; 
    FILE                        *fp = NULL;
    FILE                        *dfp = NULL;

    fp =tmpfile();
    if (!fp) {
        return -1;
    }

    dfp =fopen(DEST_FILE, "w");
    if (!fp) {
        return -1;
    }

    printf("信息写入临时文件中.\n");
    sprintf(desc, ALARM_EMAIL_SERVER_POLICY, "http", "alarmT");
    fprintf(fp, "%s", desc);
    fclose(fp);

    printf("信息写入文件-%s中.\n", DEST_FILE);
    desc[0] = '\0';
    sprintf(desc, ALARM_EMAIL_SERVER_POLICY, "http", "alarmT");
    fprintf(dfp, "%s", desc);
    fclose(dfp);

    return 0;
}

/*
 * 功能:中文输出测试
 */
int
test_unicode_display()
{
    char       buf[128];
    char       *temp;
    int        c;

    // clear buf
    clear_stdbuf();

    printf("请输入中文字符串进行测试:   ");
    scanf("%s", buf);

    printf("你输入的串为:   %s\n", buf);
    printf("其字节显示为: ");
    temp = &buf[0];
    while ((c=*temp++) != '\0') {
        printf("%x ", c);
    }
    printf("\n");

    return 0;
}


int
main(int argc, char **argv)
{
    int         ret = -1;

    printf("===============fprintf==============\n");
    //ret = test_fprintf_func();

    printf("===============中文测试==============\n");
    //ret = test_unicode_display();

    char        buf[128];
    sprintf(buf, "%04d", 3);
    printf("Buf=%s\n", buf);

    return ret;
}


