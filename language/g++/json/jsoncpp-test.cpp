#include <string>
#include <iostream>
#include "json/json.h"

using namespace std;

bool parse_one()
{
    Json::Reader reader;
    Json::Value value;

    // one data
    cout << endl << "example 1:" << endl;
    string test = "{\"id\":1,\"name\":\"hello\"}";
    if (!reader.parse(test, value)) {
        cout << "parse error" << endl;
        return false;
    }

    int id = value["id"].asInt();
    int id2 = value["id2"].asInt();
    string name = value["name"].asString();
    string name2 = value["name2"].asString();
    cout << "empty:" << name2.empty() << endl;
    cout << id << " " << name << endl
        << " name2:" << name2 << "**" << endl
        << " id2:" << id2 << endl;
    return true;
}


bool parse_complex()
{
    // more data
    Json::Reader reader;
    Json::Value value;

    cout << endl << "example 2:" << endl;
    string test = "{\"array\":[{\"id\":1, \"name\":\"hello\"},"
        "{\"id\":2,\"name\":\"world\"}]}";

    if (!reader.parse(test, value)) {
        cout << "parse error" << endl;
        return false;
    }

    const Json::Value arrayObj = value["array"];
    for (unsigned i=0; i<arrayObj.size(); i++) {
        int id = arrayObj[i]["id"].asInt();
        string name = arrayObj[i]["name"].asString();
        cout << id << " " << name << endl;
    }
    return true;
}


bool create_complex()
{
    // more data
    Json::Value value;
    Json::Value arrayObj;
    Json::FastWriter fastWriter;

    arrayObj = value["array"];
    for (unsigned i=0; i<3; i++) {
        Json::Value   vobj;
        string name="bamboo";
        vobj["id"] = 1;
        vobj["name"] = name.append(to_string(i));
        arrayObj.append(vobj);
    }
    value["array"] = arrayObj;

    Json::Value empty;
    if (empty.empty()) {
        cout << "xxxxxxxxxx" << endl;
    }
    value["empty"] = empty;

    cout << "组合字符串的最后输出为:" << endl
        << fastWriter.write(value) << endl
        << "格式化输出为:" << endl
        << value.toStyledString() << endl;
    return true;
}


int main() 
{
    if (!parse_one()) {
        return -1;
    }
    if (!parse_complex()) {
        return -1;
    }
    create_complex();
    return 0;
}

