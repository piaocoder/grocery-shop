#include "leveldb/db.h"
#include <iostream>

using namespace std;

int main()
{
    leveldb::DB       *db;
    leveldb::Options option;

    option.create_if_missing = true;
    leveldb::DB::Open(option, "/tmp/leveldb_t", &db);

    //string key = "Name";
    //string value = "Like";
    //db->Put(leveldb::WriteOptions(), key, value);

    //key = "Major";
    //value = "Computer Science and Technology";
    //db->Put(leveldb::WriteOptions(), key, value);


    string ret_s;
    db->Get(leveldb::ReadOptions(), "Name", &ret_s);
    cout << "key = Name" << endl
         << "value = " << ret_s << endl;

    db->Get(leveldb::ReadOptions(), "Major", &ret_s);
    cout << "key = Major" << endl
         << "value = " << ret_s <<endl;


    // 删除数据库对象，关闭数据库
    delete db;

    return 0;
}

