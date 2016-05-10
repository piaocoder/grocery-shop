#ifndef _LEVELDB_OPT_H_
#define _LEVELDB_OPT_H_
#include <string>
#include <sys/stat.h>
#include <stdint.h>

#include "leveldb/db.h"

using namespace std;

class LevelDB {
    private:
        leveldb::DB            *db;
        leveldb::Options        option;
        string                  dbname;

    public:
        LevelDB(string dbname);
        ~LevelDB();

        /**
         * @brief   create_db :create leveldb handle
         *
         * @return  true if successful
         */
        bool create_db();

        /**
         * @brief   delete_db :delete a existed db
         *
         * @return  
         */
        bool delete_db();

        /**
         * @brief   read_msg : read msg from db
         *
         * @param   key 
         *
         * @return  true if successful
         */
        bool read_msg(string key, string *value);

        /**
         * @brief   write_msg :write msg to db
         *
         * @param   value
         * @param   key
         *
         * @return  
         */
        bool write_msg(string value, string key);

        /**
         * @brief   Delete_msg : delete msg from db
         *
         * @param   key
         *
         * @return  
         */
        bool Delete_msg(string key);

        /**
         * @brief   update_msg :accumulate values in db.
         *
         * @param   newvalue
         * @param   key
         *
         * @return  
         */
        bool update_msg(string newvalue, string key);

        /**
         * @brief   iterate_msg :iterate db and display
         *
         * @return  
         */
        void iterate_msg();
};



#endif
