#include <iostream>
#include <utility>
#include <map>
#include <set>
/*
 * 测试map功能：
 *      １，map(key, pair<>)功能
 *      ２，map(pair<>，key)功能
 *     　
 */

using namespace std;


typedef pair<string, int> PairValue;
typedef map<string, PairValue> MapValue;

typedef set<string> SetPosValue;
typedef map<string, SetPosValue> MapPosValue;

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

    string s1[] = {"kuang", "xiang", "kuang", "xie"};
    string s2[] = {"pos1", "pos2", "pos2", "pos3"};
    SetPosValue p1(s1, s1+4), p2(s2, s2+4);
    MapPosValue m2;
    
    m2["name"] = p1;
    m2["pos"] = p2;
    for (MapPosValue::iterator it=m2.begin();
            it!=m2.end(); ++it) {
        cout << "key:" << it->first << "\t"
            << "Value:" << endl;
        SetPosValue &sobj = it->second;
        for (SetPosValue::iterator sit=sobj.begin();
                sit!=sobj.end(); sit++) {
            cout << "\t" << *sit << endl;
        }
    }

    return 0;
}
