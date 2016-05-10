#include <iostream>
#include <sstream>
#include <string>

#include "leveldb/db.h"
#include "leveldb-opt.h"

using namespace std;


int main()
{
    bool            ret;
    LevelDB        *lObj = NULL;
    uint32_t        ivalue = 0;
    string          key = "";
    string          value = ""; 
    stringstream    ss;

    // 创建数据库
    lObj = new LevelDB("./leveldb_test");
    if (NULL == lObj) {
        cout << "Instance class failed!" << endl;
        return -1;
    }

    // create db
    lObj->create_db();

    // 写入数据库
    key = "2016-05-04#5baidu3com";
    value = "1000";
    ret = lObj->write_msg(value, key);
    if (!ret) {
        return -1;
    }
    key = "2016-05-05#5baidu3com";
    value = "10004";
    ret = lObj->write_msg(value, key);
    if (!ret) {
        return -1;
    }
    key = "2016-05-06#5baidu3com";
    value = "10005";
    ret = lObj->write_msg(value, key);
    if (!ret) {
        return -1;
    }

    // read msg
    key = "2016-05-06#5baidu3com";
    ret = lObj->read_msg(key, &value);
    if (!ret) {
        return -1;
    }

    // update 
    ss << value;
    ss >> ivalue;
    if (!ss.good()) {
        cout << "String converse to int failed!" << endl;
        return -1;
    }
    ivalue += 222;
    ss << ivalue;
    value = ss.str();
    ret = lObj->write_msg(value, key);
    if (!ret) {
        return -1;
    }

    // iterate msg
    lObj->iterate_msg();

    delete lObj;

    return 0;
}
