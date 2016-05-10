#include <iostream>
#include <sstream>
#include <string>

#include "leveldb/write_batch.h"
#include "leveldb-opt.h"

LevelDB::LevelDB(string dbname) 
{
    this->db = NULL;
    this->dbname = dbname;
}


LevelDB::~LevelDB()
{
    delete this->db;
}


bool LevelDB::create_db()
{
    leveldb::Status         status;
    
    this->option.create_if_missing = true;
    status = leveldb::DB::Open(this->option, 
            this->dbname, &this->db);
    if (false == status.ok()) {
        cerr << "Unable to open a db." <<endl;
        return false;
    } else {
        return true;
    }
}


bool LevelDB::delete_db()
{
    delete this->db;
    this->db = NULL;

    return true;
}


bool LevelDB::read_msg(string key, string *value)
{
    leveldb::Status             status;

    status = this->db->Get(leveldb::ReadOptions(), key, value);
    if (status.ok()) {
        return true;
    } else {
        return false;
    }
}


bool LevelDB::write_msg(string value, string key)
{
    leveldb::Status             status;

    status = this->db->Put(leveldb::WriteOptions(), key, value);
    if (status.ok()) {
        return true;
    } else {
        return false;
    }
}


bool LevelDB::Delete_msg(string key)
{
    leveldb::Status             status;

    status = this->db->Delete(leveldb::WriteOptions(), key);
    if (status.ok()) {
        return true;
    } else {
        return false;
    }
}


bool LevelDB::update_msg(string newvalue, string key)
{
    leveldb::Status             status;
    string                      oldvalue;

    status = this->db->Get(leveldb::ReadOptions(), 
            key, &oldvalue);
    if (status.ok()) {
        oldvalue += newvalue;
        status = this->db->Put(leveldb::WriteOptions(), 
                key, oldvalue);
        if (!status.ok()) {
            cout << "Accumlate values failed!" << endl;
            return false;
        }
    } else {
        status = this->db->Put(leveldb::WriteOptions(), 
                key, newvalue);
        if (!status.ok()) {
            cout << "Write msg to leveldb failed:" 
                << key << "-" << newvalue << endl;
            return false;
        }
    }
    return true;
}


void LevelDB::iterate_msg()
{
    leveldb::Iterator* it = NULL;
    
    it = this->db->NewIterator(leveldb::ReadOptions());
    for (it->SeekToFirst(); it->Valid(); it->Next()) {
        cout << "\t" << it->key().ToString() << " : " 
            << it->value().ToString() << endl;
    }
    if (false == it->status().ok()) {
         cerr << "An error was found "
             "during the scan" << endl;
         cerr << it->status().ToString() << endl; 
    }
}

/*int main(int argc, char **argv)*/
//{
    //bool            ret;
    //LevelDB        *lObj = NULL;
    //uint32_t        ivalue = 0;
    //string          key = "";
    //string          value = ""; 
    //stringstream    ss;

    //lObj = new LevelDB("./leveldb_test");
    //if (NULL == lObj) {
        //cout << "Instance class failed!" << endl;
        //return -1;
    //}

    //// create db
    //lObj->create_db();

    //// 写入数据库
    //key = "2016-05-04#5baidu3com";
    //value = "1000";
    //ret = lObj->write_msg(value, key);
    //if (!ret) {
        //return -1;
    //}
    //key = "2016-05-05#5baidu3com";
    //value = "10004";
    //ret = lObj->write_msg(value, key);
    //if (!ret) {
        //return -1;
    //}
    //key = "2016-05-06#5baidu3com";
    //value = "10005";
    //ret = lObj->write_msg(value, key);
    //if (!ret) {
        //return -1;
    //}

    //// read msg
    //key = "2016-05-06#5baidu3com";
    //ret = lObj->read_msg(key, &value);
    //if (!ret) {
        //return -1;
    //}

    //// update 
    //ss << value;
    //ss >> ivalue;
    //if (!ss.good()) {
        //cout << "String converse to int failed!" << endl;
        //return -1;
    //}
    //ivalue += 222;
    //ss << ivalue;
    //return 0;
/*}*/
