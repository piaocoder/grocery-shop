#include <iostream>
#include <utility>
#include <map>
/*
 * 测试map功能：
 *      １，map(key, pair<>)功能
 *      ２，map(pair<>，key)功能
 *     　
 */

using namespace std;


typedef pair<string, int> PairValue;
typedef map<string, PairValue> MapValue;

int main(int argc, char **argv)
{
    PairValue v1("kuang", 1), v2("xiang", 2);
    MapValue        mobj;

    mobj["1"] = v1;
    mobj["2"] = v2;

    for (MapValue::iterator it=mobj.begin(); 
            it!=mobj.end(); ++it) {
        cout << "key:" << it->first << "\t" 
            << "value:" << it->second.first << "----" 
            << it->second.second << endl;
    }

    return 0;
}
