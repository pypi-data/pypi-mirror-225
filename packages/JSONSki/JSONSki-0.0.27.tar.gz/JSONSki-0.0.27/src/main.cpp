#include <pybind11/pybind11.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#ifndef QUERYAUTOMATON_H
#define QUERYAUTOMATON_H
#include <iostream>
#include <string.h>
#include <bitset>
using namespace std;

#define MAX_STATES 50
#define MAX_STACK_DEPTH 50
#define MAX_TRANS_STRING 10
#define MAX_KEY_LENGTH 100

#define UNMATCHED_STATE 0
#define START_STATE 1

#define OBJECT 101
#define ARRAY 102
#define PRIMITIVE 103
#define KEY 104
#define ANY 105
#define OUTPUT_CANDIDATE 106
#define GENERAL_OUTPUT 107
#define NONE 108
#define INVALID -1

typedef struct TransStrInfo {
    char key[MAX_KEY_LENGTH];
    int key_len;
    int exp_type_in_obj = NONE;
    int exp_type_in_arr = NONE;
    int next_state;
} TransStrInfo;

typedef struct StateTransEle {
    TransStrInfo t_str_info[MAX_TRANS_STRING];
    int num_trans_str = 1;
    bool matched_state;
    int start_idx;
    int end_idx;
    bool has_index_constraint = false;
} StateTransEle;

typedef struct IndexInfo {
    int start_idx;
    int end_idx;
} IndexInfo;
 
typedef struct DFA {
    StateTransEle trans_ele[MAX_STATES];
} DFA;

typedef struct Stack {
    int stack[MAX_STACK_DEPTH];
    int arr_counter_stack[MAX_STACK_DEPTH];
    int num_stack_ele;
} Stack;

class QueryAutomaton {
  public:
    QueryAutomaton() {
        reset();
    }

    void reset() {
        mStack.num_stack_ele = 0;
        mCurState = 1;
        mArrCounter = -1;
    }

    void updateStateTransInfo(int cur_state, bool is_final_state, int exp_type_in_obj, int exp_type_in_arr, char* exp_key, int next_state) {
        int cur_idx = cur_state - 1;
        int next_idx = next_state - 1;
        int trans_idx = 0;
        if (exp_key != NULL) {
            strcpy(mDfa.trans_ele[cur_idx].t_str_info[trans_idx].key, exp_key);
            mDfa.trans_ele[cur_idx].t_str_info[trans_idx].key_len = strlen(exp_key);
        }
        if (exp_type_in_obj != NONE)
            mDfa.trans_ele[cur_idx].t_str_info[trans_idx].exp_type_in_obj = exp_type_in_obj;
        if (exp_type_in_arr != NONE)
            mDfa.trans_ele[cur_idx].t_str_info[trans_idx].exp_type_in_arr = exp_type_in_arr;
        mDfa.trans_ele[cur_idx].t_str_info[trans_idx].next_state = next_state;
        mDfa.trans_ele[cur_idx].matched_state = is_final_state; 
    }

    void addIndexConstraints(int state, int start_idx, int end_idx) {
        if (state != UNMATCHED_STATE) {
            mDfa.trans_ele[state - 1].has_index_constraint = true;
            mDfa.trans_ele[state - 1].start_idx = start_idx;
            mDfa.trans_ele[state - 1].end_idx = end_idx;
        }
    }

    bool hasIndexConstraints() {
        if (mCurState == UNMATCHED_STATE) return false;
        return mDfa.trans_ele[mCurState - 1].has_index_constraint;
    }

    void addArrayCounter() {
        ++mArrCounter;
    }

    bool checkArrayCounter() {
        if (mCurState == UNMATCHED_STATE) return false;
        int start_idx = mDfa.trans_ele[mCurState - 1].start_idx;
        int end_idx = mDfa.trans_ele[mCurState - 1].end_idx;
        if (mArrCounter >= start_idx && mArrCounter < end_idx) {
            return true;
        }
        return false;
    }

    __attribute__((always_inline)) int typeExpectedInObj() {
        if (mCurState == UNMATCHED_STATE) return false;
        int cur_idx = mCurState - 1;
        return mDfa.trans_ele[cur_idx].t_str_info[0].exp_type_in_obj;
    }

    __attribute__((always_inline)) int typeExpectedInArr() {
        if (mCurState == UNMATCHED_STATE) return false;
        int cur_idx = mCurState - 1;
        return mDfa.trans_ele[cur_idx].t_str_info[0].exp_type_in_arr;
    } 

    IndexInfo getIndexInfo(int state) {
        IndexInfo idx_info;
        if (state == UNMATCHED_STATE) {
            idx_info.start_idx = -1;
            return idx_info;
        }
        idx_info.start_idx = mDfa.trans_ele[state - 1].start_idx;
        idx_info.end_idx = mDfa.trans_ele[state - 1].end_idx;    
        return idx_info;
    }

    __attribute__((always_inline)) int getNextState(char *key, int key_len) {
        if (mCurState == UNMATCHED_STATE) return UNMATCHED_STATE;
        int cur_idx = mCurState - 1;
        int num_trans_str = mDfa.trans_ele[cur_idx].num_trans_str;
        int i = 0;
        int next_state = UNMATCHED_STATE;
        while (i < num_trans_str) {
            if (mDfa.trans_ele[cur_idx].t_str_info[i].key_len == key_len 
                && memcmp(mDfa.trans_ele[cur_idx].t_str_info[i].key, key, key_len) == 0) {
                next_state = mDfa.trans_ele[cur_idx].t_str_info[i].next_state;
                return next_state;
            }
            ++i;
        }
        return next_state;
    }

    __attribute__((always_inline)) int getNextStateNoKey() {
        if (mCurState == UNMATCHED_STATE) return UNMATCHED_STATE;
        int cur_idx = mCurState - 1;
        int num_trans_str = mDfa.trans_ele[cur_idx].num_trans_str;
        int i = 0;
        int next_state = UNMATCHED_STATE;
        while (i < num_trans_str) {
            if (mDfa.trans_ele[cur_idx].t_str_info[i].key_len == 0) {
                next_state = mDfa.trans_ele[cur_idx].t_str_info[i].next_state;
                return next_state;
            }
            ++i;
        }
        return next_state;
    }

    void setCurState(int cur_state) {
        mCurState = cur_state;
    }

    int getType(int state) {
        if (state != UNMATCHED_STATE && mDfa.trans_ele[state - 1].matched_state == true)
            return OUTPUT_CANDIDATE;
        return GENERAL_OUTPUT;
    }

    int isAccept(int state) {
        if (state != UNMATCHED_STATE && mDfa.trans_ele[state - 1].matched_state == true)
            return true;
        return false;
    }

    __attribute__((always_inline)) void pushStack(int next_state) {
        if (mStack.num_stack_ele < MAX_STACK_DEPTH) {
            mStack.stack[mStack.num_stack_ele] = mCurState;
            mStack.arr_counter_stack[mStack.num_stack_ele++] = mArrCounter;
            mCurState = next_state;
            mArrCounter = -1;
        } else {
            cout<<"exception: stack is empty "<<endl;
        }
    }

    __attribute__((always_inline)) int popStack() {
        if (mStack.num_stack_ele > 0) {
            mCurState = mStack.stack[--mStack.num_stack_ele];
            mArrCounter = mStack.arr_counter_stack[mStack.num_stack_ele];
            return mCurState;
        }
        cout<<"pop out exception "<<endl;
        return INVALID;
    }

    int getStackSize() {
        return mStack.num_stack_ele;
    }

    ~QueryAutomaton() {} 
   
  public:
    int mCurState;

  private:
    DFA mDfa;
    int mArrCounter = -1;
    Stack mStack;
};
#endif

//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================

#ifndef JSONPATHPARSER_H
#define JSONPATHPARSER_H
#include <string.h>
// #include "QueryAutomaton.h"

class JSONPathParser {
    public:
        // update query automaton based on the specific JSONPath query
        static void updateQueryAutomaton(string query, QueryAutomaton& qa);
};
#endif

//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================

// #include "JSONPathParser.h"
#include <stdlib.h>
#include <limits.h>

void JSONPathParser::updateQueryAutomaton(string query, QueryAutomaton &qa) {
    int length = query.size();
    int lexer_state = 0;
    int query_state = START_STATE;
    char buffer[MAX_KEY_LENGTH];
    for (int i = 0; i < length; ++i) {
        char ch = query[i];
        switch (lexer_state) {
            case 0: { // begin of the path
                if (ch == '.') {
                    lexer_state = 1;
                } else if (ch == '[') {
                    lexer_state = 2;
                    qa.updateStateTransInfo(query_state, false, NONE, ARRAY, NULL, query_state + 1);
                    // cout<<"("<<query_state<<", false, NONE, ARRAY, NULL, "<<(query_state + 1)<<")"<<endl;
                    ++query_state;
                }
                break;
            }
            case 1: { // in object
                int key_end = 0;
                while (ch != '.' && ch != '[') {
                    buffer[key_end++] = ch;
                    if (i + 1 == length) break;
                    ch = query[++i];
                }
                buffer[key_end] = '\0';
                if (i + 1 < length) {
                    if (ch == '[') {
                        lexer_state = 2;
                        // current query state -> expected key-array pair
                        qa.updateStateTransInfo(query_state, false, ARRAY, NONE, buffer, query_state + 1);
                        // cout<<"("<<query_state<<", false, ARRAY, NONE, "<<buffer<<", "<<(query_state + 1)<<")"<<endl;
                        // state transition for [
                        qa.updateStateTransInfo(query_state + 1, false, NONE, NONE, NULL, query_state + 2);
                        // cout<<"("<<(query_state + 1)<<", false, NONE, NONE, NULL, "<<(query_state + 2)<<")"<<endl;
                        query_state += 2;
                        // break;
                    } else if (ch == '.') {
                        lexer_state = 1;
                        qa.updateStateTransInfo(query_state, false, OBJECT, NONE, buffer, query_state + 1);
                        // cout<<"("<<query_state<<", false, OBJECT, NONE, "<<buffer<<", "<<(query_state + 1)<<")"<<endl;
                        ++query_state;
                        // break;
                    } 
                } else {
                    // output info
                    qa.updateStateTransInfo(query_state, false, PRIMITIVE, NONE, buffer, query_state + 1);
                    // cout<<"("<<query_state<<", false, PRIMITIVE, NONE, "<<buffer<<", "<<(query_state + 1)<<")"<<endl;
                    qa.updateStateTransInfo(query_state + 1, true, NONE, NONE, NULL, query_state + 1);
                    // cout<<"("<<(query_state + 1)<<", true, NONE, NONE, NULL, "<<(query_state + 1)<<")"<<endl;
                }
                break;
            }
            case 2: { // in array
                int start_idx = 0;
                int end_idx = -1;
                int index_end = 0;
                bool has_colon = false;
                while (ch != ']') {
                    if (ch == ':') {
                        buffer[index_end] = '\0';
                        start_idx = atoi(buffer);
                        end_idx = INT_MAX;
                        index_end = 0;
                        has_colon = true;
                    }
                    else if (ch >= '0' && ch <= '9') {
                        buffer[index_end++] = ch;
                    }
                    if (i + 1 == length) break;
                    ch = query[++i];
                }
                if (has_colon == false && index_end > 0) {
                    buffer[index_end] = '\0';
                    start_idx = atoi(buffer);
                    end_idx = start_idx + 1;
                } else if (index_end > 0) {
                    buffer[index_end] = '\0';
                    end_idx = atoi(buffer);
                }
                if (end_idx > -1) {
                    qa.addIndexConstraints(query_state, start_idx, end_idx);
                    // cout<<"index constraints "<<start_idx<<" "<<end_idx<<" current state "<<query_state<<endl;
                }
                if (i + 1 < length) {
                    ch = query[++i];
                    if (ch == '.') {
                        lexer_state = 1;
                        qa.updateStateTransInfo(query_state, false, NONE, OBJECT, NULL, query_state + 1);
                        // cout<<"("<<query_state<<", false, NONE, OBJECT, NULL, "<<(query_state + 1)<<")"<<endl;
                    } else if (ch == '[') {
                        cout<<"additional ["<<endl;
                        lexer_state = 2;
                        qa.updateStateTransInfo(query_state, false, NONE, ARRAY, NULL, query_state + 1);
                        // cout<<"("<<query_state<<", false, NONE, ARRAY, NULL, "<<(query_state + 1)<<")"<<endl;
                        ++query_state;
                    }
                } else {
                    qa.updateStateTransInfo(query_state, true, NONE, PRIMITIVE, NULL, query_state);
                    // cout<<"("<<query_state<<", false, NONE, PRIMITIVE, NULL, "<<(query_state + 1)<<")"<<endl;
                }
                break;
            }
        }
    }
}


//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================

#ifndef RECORDS_H
#define RECORDS_H

#include <stdlib.h>
#include <vector>
using namespace std;

#define MIN_RECORD_SIZE 5
#define MAX_RECORD_SIZE 1000000

// information for a single JSON record
struct Record {
    // for line-delimited JSON stream with a sequence of records,
    // contacting them into one single string generates the best
    // performance for indexing and querying
    char* text;
    long rec_start_pos;
    long rec_length;
    // text could be shared among different Record objects
    // (e.g. line-delimited JSON stream with a sequence of records)
    bool can_delete_text;

    Record() {
        text = NULL;
        rec_start_pos = 0;
        rec_length = 0;
        can_delete_text = true;
    }

    ~Record() {
        if (can_delete_text == true && text != NULL) {
            free(text);
            text = NULL;
            can_delete_text = false;
        }
    }
};

// information for a sequence of JSON records
class RecordSet {
    friend class RecordLoader;
  private:
    vector<Record*> recs;
    long num_recs;

  public:
    RecordSet() {
        num_recs = 0;
    }

    // record can be accessed in array style.
    Record*& operator[] (long idx) {
        if (idx >= 0 && idx < num_recs)
            return recs[idx];
        cout << "Array index in RecordSet out of bound."<<endl; 
        exit(0); 
    }

    long size() {
        return num_recs;
    }

    ~RecordSet() {
        for (long i = 0; i < num_recs; ++i) {
            if (recs[i] != NULL)
                delete recs[i];
        }
    }
};
#endif


//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================

#ifndef _RECORDLOADER_H
#define _RECORDLOADER_H
#include <stdio.h>
#if defined(__MACH__)
#include <stdlib.h>
#else 
#include <malloc.h>
#endif
#include <string.h>
#include <ctype.h>
#include <pthread.h>
#include <sys/time.h>
#include <sys/file.h>
#include <unistd.h>
#include <sched.h>
#include <iostream>
#include <string>
#include <vector>
// #include "Records.h"
using namespace std;

class RecordLoader{
  public:
   // static Record* loadSingleRecord(char* file_path);
     static Record* loadSingleRecord(const char* file_path);
    static RecordSet* loadRecords(char* file_path);
};
#endif

//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================

#include <sys/time.h>
// #include "RecordLoader.h"

#include <stdio.h>
#include <errno.h>
using namespace std;

#define MAX_PAD 64
 Record* RecordLoader::loadSingleRecord(const char* file_path) {
// Record* RecordLoader::loadSingleRecord(char* file_path) {
    unsigned long size;
    cout << file_path << endl;
    FILE* fp = fopen (file_path,"rb");
    cout << fp << endl;
    if (fp == NULL) {
        perror("Error opening the file");
        return NULL;
    }
    fseek (fp, 0, SEEK_END);
    size = ftell(fp);
    rewind(fp);
    void* p;
    if (posix_memalign(&p, 64, (size + MAX_PAD)*sizeof(char)) != 0) {
        cout<<"Fail to allocate memory space for input record."<<endl;
    }
    char* record_text = (char*) p;
    size_t load_size = fread (record_text, 1, size, fp);
    if (load_size == 0) {
        cout<<"Fail to load the input record into memory"<<endl;
    }
    int remain = 64 - (size % 64);
    int counter = 0;
    // pad the input data where its size can be divided by 64
    while (counter < remain)
    {
        record_text[size+counter] = 'd';
        counter++;
    }
    record_text[size+counter]='\0';
    fclose(fp);
    // only one single record
    Record* record = new Record();
    record->text = record_text;
    record->rec_start_pos = 0;
    record->rec_length = strlen(record_text);
    return record;
}

RecordSet* RecordLoader::loadRecords(char* file_path) {
    FILE *fp = fopen(file_path, "r");
    RecordSet* rs = new RecordSet();
    if (fp) {
        char line[MAX_RECORD_SIZE];
        string str;
        int start_pos = 0;
        while (fgets(line, sizeof(line), fp) != NULL) {
            if (strlen(line) <= MIN_RECORD_SIZE) continue;
            int remain = 64 - strlen(line) % 64;
            int top = strlen(line);
            while (remain > 0) {
                line[top++] = 'd';
                --remain;
            }
            line[top] = '\0';
            if (strlen(line) > MIN_RECORD_SIZE) {
                // concating a sequence of record texts into one single string generates the best performance for indexing and querying
                str.append(line);
                Record* record = new Record();
                record->rec_start_pos = start_pos;
                record->rec_length = strlen(line);
                start_pos += strlen(line);
                rs->recs.push_back(record);
                ++rs->num_recs;
            }
        }
        void* p;
        if(posix_memalign(&p, 64, str.size()*sizeof(char)) != 0) {
            cout<<"Fail to allocate memory space for records from input file."<<endl;
        }
        for (int i = 0; i < rs->recs.size(); ++i) {
            // all record objects points to the same input text which contacts a sequence of JSON records
            rs->recs[i]->text = (char*) p;
            if (i == 0) strcpy(rs->recs[0]->text, str.c_str());
            // deconstructor in the last record object can delete input text
            if (i < rs->recs.size() - 1) rs->recs[i]->can_delete_text = false;
        }
        fclose(fp);
        return rs;
    }
    cout<<"Fail open the file."<<endl;
    return rs;
}

//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================


#ifndef QUERYPROCESSOR_H
#define QUERYPROCESSOR_H
#include <string>
#include <iostream>
#include <vector>
#include <bitset>
#include <cassert>
#include <stack>
#include <algorithm>
#include <unordered_map>
#include <functional>
#include <math.h>
//#include <immintrin.h> 
#if defined(__x86_64__) || defined(__i386__)
#include <immintrin.h>
#endif
#include <unordered_map>
#include <map>
// #include "JSONPathParser.h"
// #include "QueryAutomaton.h"
// #include "Records.h"
using namespace std;

#define SUCCESS 1001
#define ARRAY_END 1002
#define OBJECT_END 1003
#define RANGE_END 1004
#define PARTIAL_SKIP 1005
#define MAX_KEY_LENGTH 1000
#define MAX_TEXT_LENGTH 10000


#ifndef unlikely
#define unlikely(x) __builtin_expect(!!(x), 0)
#endif

typedef struct bitmap{
    unsigned long colonbit = 0;
    unsigned long commabit = 0;
    unsigned long lbracebit = 0;
    unsigned long rbracebit = 0;
    unsigned long lbracketbit = 0;
    unsigned long rbracketbit = 0;
    bool has_colon = false;
    bool has_comma = false;
    bool has_lbrace = false;
    bool has_rbrace = false;
    bool has_lbracket = false;
    bool has_rbracket = false;
} bitmap;

typedef struct IntervalInfo {
    unsigned long intervalbit = 0;
    bool is_complete = true;
} IntervalInfo;

struct JumpInfo {
    int status;
    int num_comma;
    JumpInfo(int s, int n = 0) {
        status = s;
        num_comma = n;
    }
};

class QueryProcessor {
  public:
    // initialization. including query automaton construction and
    // some internal variables initialization for supporting bit-parallel
    // fast-forwarding optimizations.
    QueryProcessor(string query);
    ~QueryProcessor();
    long getOutputMatchesNum();
    // execute query on one single JSON record
    string runQuery(Record* rec);

  private:
    void init();
    void setRecordText(char* rec_text, long record_length);
    char getNextNonEmptyCharacter(long& pos);
    void object(long& pos, bitmap& bm);
    void array(long& pos, bitmap& bm);
    void array_range(long& pos, bitmap& bm);
    
    // fast-forward functions
    __attribute__((always_inline)) void goOverObj(long& pos, bitmap& bm);
    __attribute__((always_inline)) void goOverAry(long& pos, bitmap& bm);
    __attribute__((always_inline)) void goOverPriAttr(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goOverPriElem(long& pos, bitmap& bm); 
    __attribute__((always_inline)) void goToObjEnd(long& pos, bitmap& bm);
    __attribute__((always_inline)) void goToAryEnd(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goOverElem(long& pos, int num_elements, bitmap& bm);
    __attribute__((always_inline)) JumpInfo goOverPrimElemsInRange(long& pos, int num_elements, bitmap& bm);
    __attribute__((always_inline)) int goToObjElemInRange(long& pos, int& num_elements, bitmap& bm);
    __attribute__((always_inline)) int goToAryElemInRange(long& pos, int& num_elements, bitmap& bm);
    __attribute__((always_inline)) int goToPrimElemInRange(long& pos, int& num_elements, bitmap& bm);
    __attribute__((always_inline)) int goToObjAttr(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goToAryAttr(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goToPrimAttr(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goToObjElem(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goToAryElem(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goToPrimElem(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goOverPriAttrs(long& pos, bitmap& bm);
    __attribute__((always_inline)) int goOverPriElems(long& pos, bitmap& bm); 
    __attribute__((always_inline)) bool hasMoreElements(long& pos);
    __attribute__((always_inline)) int getElementType(long& pos);
    __attribute__((always_inline)) bool hasMoreAttributes(long& pos);
    __attribute__((always_inline)) int getAttributeType(long& pos);

    // structural interval construction and access 
    __attribute__((always_inline)) void resetBitmap(bitmap& bm) {
        bm.has_colon = false;
        bm.has_comma = false;
        bm.has_lbrace = false;
        bm.has_rbrace = false;
        bm.has_lbracket = false;
        bm.has_rbracket = false;
    }    
    // first three steps of structral index construction, get string mask bitmap
    __attribute__((always_inline)) void build_bitmap_basic(); 
    __attribute__((always_inline)) void build_bitmap_colon(bitmap& bm);
    __attribute__((always_inline)) void build_bitmap_comma(bitmap& bm);
    __attribute__((always_inline)) void build_bitmap_lbrace(bitmap& bm);
    __attribute__((always_inline)) void build_bitmap_rbrace(bitmap& bm);
    __attribute__((always_inline)) void build_bitmap_lbracket(bitmap& bm);
    __attribute__((always_inline)) void build_bitmap_rbracket(bitmap& bm);
    __attribute__((always_inline)) void get_bitmap_colon(bitmap& bm);
    __attribute__((always_inline)) void get_bitmap_comma(bitmap& bm);
    __attribute__((always_inline)) void get_bitmap_lbrace(bitmap& bm);
    __attribute__((always_inline)) void get_bitmap_rbrace(bitmap& bm);
    __attribute__((always_inline)) void get_bitmap_lbracket(bitmap& bm);
    __attribute__((always_inline)) void get_bitmap_rbracket(bitmap& bm);
    __attribute__((always_inline)) IntervalInfo get_interval_new_word(unsigned long& bitmap);
    __attribute__((always_inline)) IntervalInfo get_interval(long& pos, unsigned long& bitmap);
    __attribute__((always_inline)) IntervalInfo next_interval(unsigned long& bitmap);
    __attribute__((always_inline)) long get_position(unsigned long& bitmap, int number); 
    __attribute__((always_inline)) long interval_end(unsigned long& interval);
    __attribute__((always_inline)) void get_interval_brace(long& pos, bitmap& bm, IntervalInfo& itv_info);
    __attribute__((always_inline)) void next_interval_brace(bitmap& bm, IntervalInfo& itv_info);
    __attribute__((always_inline)) void get_interval_bracket(long& pos, bitmap& bm, IntervalInfo& itv_info);
    __attribute__((always_inline)) void next_interval_bracket(bitmap& bm, IntervalInfo& itv_info); 
    __attribute__((always_inline)) long get_position_brace(bitmap& bm, int number);
    __attribute__((always_inline)) long get_position_bracket(bitmap& bm, int number);
    __attribute__((always_inline)) void next_interval(char ch);
    __attribute__((always_inline)) int count(unsigned long& interval, unsigned long& bitmap);
    __attribute__((always_inline)) long object_end(unsigned long& interval, unsigned long& bitmap);

    // all private variables
    unsigned long str_mask;
    unsigned long escapebit, stringbit, lbracebit, rbracebit, lbracketbit, rbracketbit;
    unsigned long bracketbit0, colonbit0, quotebit0, escapebit0, stringbit0, lbracebit0, rbracebit0, commabit0, lbracketbit0, rbracketbit0;
    long start_id;

#if defined(__x86_64__) || defined(__i386__)
    __m256i v_text0, v_text;
#endif
//    __m256i v_text0, v_text;
    
    int64_t quote_bits; unsigned long st_quotebit; unsigned long ed_quotebit; unsigned long cb_bit;

    #if defined(__x86_64__) || defined(__i386__)
        __m256i struct_mask;
    __m256i structural_table, v_quote, v_colon, v_escape, v_lbrace, v_rbrace, v_comma, v_lbracket, v_rbracket;
#endif

 //    __m256i struct_mask;
   //  __m256i structural_table, v_quote, v_colon, v_escape, v_lbrace, v_rbrace, v_comma, v_lbracket, v_rbracket;
    uint64_t prev_iter_ends_odd_backslash;
    uint64_t prev_iter_inside_quote;
    uint64_t even_bits;
    uint64_t odd_bits;
    unsigned long first, second;
    long top_word;
    unsigned long cb_mask;
    unsigned long colonbit;
    unsigned long quotebit;
    unsigned long commabit;
    unsigned long bracketbit;
    bool cur_word;
    long cur_pos;
    unsigned long mask;
    unsigned long colon_mask;
    unsigned long comma_mask;

    char* mRecord;
    // for a single large record, stream length equals to record length
    long mRecordLength;
    // each temp word has 32 bytes
    long mNumTmpWords;
    // each word has 64 bytes
    long mNumWords;
    char mKey[MAX_KEY_LENGTH];
    char* mText;
    long mWordId;
    QueryAutomaton qa;
    long mNumMatches;
    string mOutput;
};
#endif

//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================
//=====================================================================================================================

// #include "QueryProcessor.h"
//#include <immintrin.h>
#if defined(__x86_64__) || defined(__i386__)
#include <immintrin.h>
#include <emmintrin.h>
#include <string.h>
#include <sys/time.h>
#include <string.h>
#if defined(__MACH__)
#include <stdlib.h>
#else 
#include <malloc.h>
#endif
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <pthread.h>

#include <sys/time.h>
#include <sys/file.h>
#include <unistd.h>
#include <sched.h>
#include <unordered_map>

using namespace std;

QueryProcessor::QueryProcessor(string query) {
    JSONPathParser::updateQueryAutomaton(query, this->qa);
    this->mOutput.clear();
    this->mNumMatches = 0;
    this->mText = new char[MAX_TEXT_LENGTH];
    init(); 
}

void QueryProcessor::init() {
    structural_table =
        _mm256_setr_epi8(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '{', 0, '}', 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '{', 0, '}', 0, 0);
    struct_mask = _mm256_set1_epi8(0x20);
    // vectors for structural characters
    v_quote = _mm256_set1_epi8(0x22);
    v_colon = _mm256_set1_epi8(0x3a);
    v_escape = _mm256_set1_epi8(0x5c);
    v_lbrace = _mm256_set1_epi8(0x7b);
    v_rbrace = _mm256_set1_epi8(0x7d);
    v_comma = _mm256_set1_epi8(0x2c);
    v_lbracket = _mm256_set1_epi8(0x5b);
    v_rbracket = _mm256_set1_epi8(0x5d);
    // some global variables among internal functions
    top_word = -1;
    prev_iter_ends_odd_backslash = 0ULL;
    prev_iter_inside_quote = 0ULL;
    even_bits = 0x5555555555555555ULL;
    odd_bits = ~even_bits;
    start_id = 0;
    cb_mask = 0, colon_mask = 0, comma_mask = 0; mask = 0;
    colonbit = 0; quotebit = 0; commabit = 0; bracketbit = 0;
    cur_word = false;
    top_word = -1;
    cur_pos = 0; 
    this->mOutput.clear();
}

QueryProcessor::~QueryProcessor()
{
    if (mText) {
        free(mText);
        mText = NULL;
    }
}

void QueryProcessor::setRecordText(char* rec_text, long length) {
    this->mRecord = rec_text;
    this->mRecordLength = length;
    this->mNumTmpWords = length / 32;
    this->mNumWords = length / 64; 
}

// build quote bitmap and string mask bitmap for the current word
__attribute__((always_inline)) void QueryProcessor::build_bitmap_basic() {
    unsigned long quotebit0, escapebit0;
    unsigned long quotebit, escapebit;
    // step 1: build structural quote and escape bitmaps for the current word
    // first half of bitmap
    top_word = start_id / 2; // word id 
    unsigned long i = start_id * 32;
    v_text0 = _mm256_loadu_si256(reinterpret_cast<const __m256i *>(mRecord + i));
    quotebit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_quote));
    escapebit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_escape));
    // second half of bitmap 
    ++start_id;
    i = (start_id) * 32;
    v_text = _mm256_loadu_si256(reinterpret_cast<const __m256i *>(mRecord + i));
    quotebit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_quote));
    escapebit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_escape));
    quotebit = (quotebit << 32) | quotebit0;
    escapebit = (escapebit << 32) | escapebit0;
    // step 2: update structural quote bitmaps
    uint64_t bs_bits = escapebit;
    uint64_t start_edges = bs_bits & ~(bs_bits << 1);
    int64_t even_start_mask = even_bits ^ prev_iter_ends_odd_backslash;
    uint64_t even_starts = start_edges & even_start_mask;
    uint64_t odd_starts = start_edges & ~even_start_mask;
    uint64_t even_carries = bs_bits + even_starts;
    int64_t odd_carries;
    bool iter_ends_odd_backslash = __builtin_uaddll_overflow(bs_bits, odd_starts,
        (unsigned long long *)(&odd_carries));
    odd_carries |= prev_iter_ends_odd_backslash;
    prev_iter_ends_odd_backslash = iter_ends_odd_backslash ? 0x1ULL : 0x0ULL;
    uint64_t even_carry_ends = even_carries & ~bs_bits;
    uint64_t odd_carry_ends = odd_carries & ~bs_bits;
    uint64_t even_start_odd_end = even_carry_ends & odd_bits;
    uint64_t odd_start_even_end = odd_carry_ends & even_bits;
    uint64_t odd_ends = even_start_odd_end | odd_start_even_end;
    quote_bits = quotebit & ~odd_ends;
     // step 3: build string mask bitmaps
    str_mask = _mm_cvtsi128_si64(_mm_clmulepi64_si128(
        _mm_set_epi64x(0ULL, quote_bits), _mm_set1_epi8(0xFFu), 0));
    str_mask ^= prev_iter_inside_quote;
    prev_iter_inside_quote = static_cast<uint64_t>(static_cast<int64_t>(str_mask) >> 63);
}

__attribute__((always_inline)) void QueryProcessor::build_bitmap_colon(bitmap& bm) {
    unsigned long colonbit0, colonbit;
    colonbit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_colon));
    colonbit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_colon));
    bm.colonbit = (colonbit << 32) | colonbit0;
    bm.colonbit = bm.colonbit & (~str_mask);
}

__attribute__((always_inline)) void QueryProcessor::get_bitmap_colon(bitmap& bm) {
    if (bm.has_colon == false) {
        build_bitmap_colon(bm);
        bm.has_colon = true;
    }
}

__attribute__((always_inline)) void QueryProcessor::build_bitmap_comma(bitmap& bm) {
    unsigned long commabit0, commabit;
    commabit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_comma));
    commabit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_comma));
    bm.commabit = (commabit << 32) | commabit0;
    bm.commabit = bm.commabit & (~str_mask);
}

__attribute__((always_inline)) void QueryProcessor::get_bitmap_comma(bitmap& bm) {
    if (bm.has_comma == false) {
        build_bitmap_comma(bm);
        bm.has_comma = true;
    }
}

__attribute__((always_inline)) void QueryProcessor::build_bitmap_lbrace(bitmap& bm) {
    unsigned long lbracebit0, lbracebit;
    lbracebit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_lbrace));
    lbracebit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_lbrace));
    bm.lbracebit = (lbracebit << 32) | lbracebit0;
    bm.lbracebit = bm.lbracebit & (~str_mask);
}

__attribute__((always_inline)) void QueryProcessor::get_bitmap_lbrace(bitmap& bm) {
    if (bm.has_lbrace == false) {
        build_bitmap_lbrace(bm);
        bm.has_lbrace = true;
    }
}

__attribute__((always_inline)) void QueryProcessor::build_bitmap_rbrace(bitmap& bm) {
    unsigned long rbracebit0, rbracebit;
    rbracebit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_rbrace));
    rbracebit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_rbrace));
    bm.rbracebit = (rbracebit << 32) | rbracebit0;
    bm.rbracebit = bm.rbracebit & (~str_mask);
}

__attribute__((always_inline)) void QueryProcessor::get_bitmap_rbrace(bitmap& bm) {
    if (bm.has_rbrace == false) {
        build_bitmap_rbrace(bm);
        bm.has_rbrace = true;
    }
}

__attribute__((always_inline)) void QueryProcessor::build_bitmap_lbracket(bitmap& bm) {
    unsigned long lbracketbit0, lbracketbit;
    lbracketbit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_lbracket));
    lbracketbit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_lbracket));
    bm.lbracketbit = (lbracketbit << 32) | lbracketbit0;
    bm.lbracketbit = bm.lbracketbit & (~str_mask);
}

__attribute__((always_inline)) void QueryProcessor::get_bitmap_lbracket(bitmap& bm) {
    if (bm.has_lbracket == false) {
        build_bitmap_lbracket(bm);
        bm.has_lbracket = true;
    }
}

__attribute__((always_inline)) void QueryProcessor::build_bitmap_rbracket(bitmap& bm) {
    unsigned long rbracketbit0, rbracketbit;
    rbracketbit0 = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text0, v_rbracket));
    rbracketbit = (unsigned)_mm256_movemask_epi8(_mm256_cmpeq_epi8(v_text, v_rbracket));
    bm.rbracketbit = (rbracketbit << 32) | rbracketbit0;
    bm.rbracketbit = bm.rbracketbit & (~str_mask);
}

__attribute__((always_inline)) void QueryProcessor::get_bitmap_rbracket(bitmap& bm) {
    if (bm.has_rbracket == false) {
        build_bitmap_rbracket(bm);
        bm.has_rbracket = true;
    }
}

__attribute__((always_inline)) IntervalInfo QueryProcessor::get_interval(long& pos, unsigned long& bitmap) {
    IntervalInfo itv_info;
    int relative_pos = pos % 64;
    unsigned long w_start = (1UL << relative_pos);
    unsigned long mask_start = w_start ^ (w_start - 1);
    bitmap = bitmap & (~mask_start);
    if (bitmap) {
        unsigned long w_end = bitmap & (-bitmap);
        unsigned long w_interval = (w_end - w_start) | w_end;
        itv_info.intervalbit = w_interval & (~mask_start);
        itv_info.is_complete = true;
    } else {
        // include the last character inside the word (incomplete interval)
        unsigned long w_end = (1UL << 63);
        unsigned long w_interval = (w_end - w_start) | w_end;
        itv_info.intervalbit = w_interval & (~mask_start);
        itv_info.is_complete = false;
    }
    return itv_info;
}

__attribute__((always_inline)) IntervalInfo QueryProcessor::get_interval_new_word(unsigned long& bitmap) {
    IntervalInfo itv_info;
    unsigned long w_start = 1;
    if (bitmap) {
        unsigned long w_end = bitmap & (-bitmap);
        unsigned long w_interval = (w_end - w_start) | w_end;
        itv_info.intervalbit = w_interval;
        itv_info.is_complete = true;
    } else {
        // include the last character inside the word (incomplete interval)
        unsigned long w_end = (1UL << 63);
        unsigned long w_interval = (w_end - w_start) | w_end;
        itv_info.intervalbit = w_interval;
        itv_info.is_complete = false;
    }
    return itv_info;
}

__attribute__((always_inline)) IntervalInfo QueryProcessor::next_interval(unsigned long& bitmap) {
    IntervalInfo itv_info;
    unsigned long w_start = bitmap & (-bitmap);
    bitmap = bitmap & (bitmap - 1);
    if (bitmap) {
        unsigned long w_end = bitmap & (-bitmap);
        unsigned long w_interval = (w_end - w_start) | w_end;
        itv_info.intervalbit = w_interval;
        itv_info.is_complete = true;
    } else {
        // include the last character inside the word (incomplete interval)
        unsigned long w_end = (1UL << 63);
        unsigned long w_interval = (w_end - w_start) | w_end;
        itv_info.intervalbit = w_interval;
        itv_info.is_complete = false;
    }
    return itv_info;
}

__attribute__((always_inline)) long QueryProcessor::get_position(unsigned long& bitmap, int number) {
    while (number > 1) {
        bitmap = bitmap & (bitmap - 1);
        --number;
    }
    unsigned long pos = top_word * 64 + __builtin_ctzll(bitmap);
    return pos;
}

__attribute__((always_inline)) int QueryProcessor::count(unsigned long& interval, unsigned long& bitmap) {
    return __builtin_popcountl(bitmap & interval); 
}

__attribute__((always_inline)) long QueryProcessor::object_end(unsigned long& interval, unsigned long& bitmap) {
    return top_word * 64 + 64 - __builtin_clzll(bitmap & interval);
}

__attribute__((always_inline)) long QueryProcessor::interval_end(unsigned long& interval) {
    return top_word * 64 + 63 - __builtin_clzll(interval);
}

__attribute__((always_inline)) void QueryProcessor::goOverObj(long& pos, bitmap& bm) {
    int num_open = 1;
    int num_close = 0;
    long word_id = pos / 64;
    bool first_interval = false;
    bool new_word = false;
    while (true) {
        while (word_id < mNumWords) {
            if (word_id > top_word) {
                // build basic bitmaps for the next word
                resetBitmap(bm);
                start_id = word_id * 2;
                build_bitmap_basic();
            } 
            get_bitmap_lbrace(bm);
            IntervalInfo interval;
            if (first_interval == false) {
                if (new_word == true) {
                    interval = get_interval_new_word(bm.lbracebit);
                } else {
                    interval = get_interval(pos, bm.lbracebit);
                }
                first_interval = true;
            } else {
                interval = next_interval(bm.lbracebit);
            }
            get_bitmap_rbrace(bm);
            unsigned long bitmap_rbrace = bm.rbracebit & interval.intervalbit;
            num_close = __builtin_popcountl(bitmap_rbrace);
            if (num_close < num_open) {
                if (interval.is_complete == true) {
                    num_open = num_open - num_close + 1;
                    break;
                } else {
                    num_open = num_open - num_close;
                }
            } else {  // results found
                pos = get_position(bitmap_rbrace, num_open);
                return;
            }
            // interval is incomplete in the current word
            ++word_id;
            first_interval = false;
            new_word = true;
        }
    }
}

__attribute__((always_inline)) void QueryProcessor::goOverAry(long& pos, bitmap& bm) {
    int num_open = 1;
    int num_close = 0;
    long word_id = pos / 64;
    bool first_interval = false;
    bool new_word = false;
    while (true) {
        while (word_id < mNumWords) {
            if (word_id > top_word) {
                // build basic bitmaps for the next word
                resetBitmap(bm);
                start_id = word_id * 2;
                build_bitmap_basic();
            }
            get_bitmap_lbracket(bm);
            IntervalInfo interval;
            if (first_interval == false) {
                if (new_word == true) {
                    interval = get_interval_new_word(bm.lbracketbit);
                } else {
                    interval = get_interval(pos, bm.lbracketbit);
                } 
                first_interval = true;
            } else {
                interval = next_interval(bm.lbracketbit);
            } 
            get_bitmap_rbracket(bm);
            unsigned long bitmap_rbracket = bm.rbracketbit & interval.intervalbit;
            bitset<64> tempbit1(bm.rbracketbit);
            num_close = __builtin_popcountl(bitmap_rbracket);
            if (num_close < num_open) {
                if (interval.is_complete == true) {
                    num_open = num_open - num_close + 1;
                    break;
                } else {
                    num_open = num_open - num_close;
                }
            } else {  // results found
                pos = get_position(bitmap_rbracket, num_open);  //bm.rbracebit
                return;
            }
            // interval is incomplete in the current word
            ++word_id;
            first_interval = false;
            new_word = true;
        }
    }
}

__attribute__((always_inline)) void QueryProcessor::goToObjEnd(long& pos, bitmap& bm) {
    int num_open = 1;
    int num_close = 0;
    long word_id = pos / 64;
    bool first_interval = false;
    bool new_word = false;
    while (true) {
        while (word_id < mNumWords) {
            if (word_id > top_word) {
                resetBitmap(bm);
                start_id = word_id * 2;
                build_bitmap_basic();
            } 
            get_bitmap_lbrace(bm);
            IntervalInfo interval;
            if (first_interval == false) {
                if (new_word == true) {
                    interval = get_interval_new_word(bm.lbracebit);
                } else {
                    interval = get_interval(pos, bm.lbracebit);
                }
                first_interval = true;
            } else {
                interval = next_interval(bm.lbracebit);
            }
            get_bitmap_rbrace(bm);
            unsigned long bitmap_rbrace = bm.rbracebit & interval.intervalbit;
            num_close = __builtin_popcountl(bitmap_rbrace);
            if (num_close < num_open) {
                if (interval.is_complete == true) {
                    num_open = num_open - num_close + 1;
                    break;
                } else {
                    num_open = num_open - num_close;
                }
            } else {  // results found
                pos = get_position(bitmap_rbrace, num_open);
                return;
            }
            // interval is incomplete in the current word
            ++word_id;
            first_interval = false;
            new_word = true;
        }
    }
}

__attribute__((always_inline)) void QueryProcessor::goToAryEnd(long& pos, bitmap& bm) {
    int num_open = 1;
    int num_close = 0;
    long word_id = pos / 64;
    bool first_interval = false;
    bool new_word = false;
    while (true) {
        while (word_id < mNumWords) {
            if (word_id > top_word) {
                // build basic bitmaps for the next word
                resetBitmap(bm);
                start_id = word_id * 2;
                build_bitmap_basic();
            }
            get_bitmap_lbracket(bm);
            IntervalInfo interval;
            if (first_interval == false) {
                if (new_word == true) {
                    interval = get_interval_new_word(bm.lbracketbit);
                } else {
                    interval = get_interval(pos, bm.lbracketbit);
                }
                first_interval = true;
            } else {
                interval = next_interval(bm.lbracketbit);
            }
            get_bitmap_rbracket(bm);
            unsigned long bitmap_rbracket = bm.rbracketbit & interval.intervalbit;
            num_close = __builtin_popcountl(bitmap_rbracket);
            if (num_close < num_open) {
                if (interval.is_complete == true) {
                    num_open = num_open - num_close + 1;
                    break;
                } else {
                    num_open = num_open - num_close;
                }
            } else {  // results found
                pos = get_position(bitmap_rbracket, num_open);
                return;
            }
            // interval is incomplete in the current word
            ++word_id;
            first_interval = false;
            new_word = true;
        }
    }
}

__attribute__((always_inline)) void QueryProcessor::goOverPriAttr(long& pos, bitmap& bm) {
    long word_id = pos / 64;
    bool first_interval = false;
    bool new_word = false;
    while (word_id < mNumWords) {
        if (word_id > top_word) {
            // build basic bitmaps for the next word
            resetBitmap(bm);
            start_id = word_id * 2;
            build_bitmap_basic();
        }
        get_bitmap_comma(bm);
        IntervalInfo interval;
        if (first_interval == false) {
            if (new_word == true) {
                interval = get_interval_new_word(bm.commabit);
            } else {
                interval = get_interval(pos, bm.commabit);
            }
            first_interval = true;
        } else {
            interval = next_interval(bm.commabit);
        }
        get_bitmap_rbrace(bm);
        unsigned long bitmap_rbrace = bm.rbracebit & interval.intervalbit;
        if (bitmap_rbrace) {
            // end of object
            pos = get_position(bitmap_rbrace, 1) - 1;
            return;
        }
        if (interval.is_complete) {
            // position before comma
            pos = interval_end(interval.intervalbit) - 1;
            return;
        } 
        // interval is incomplete in the current word
        ++word_id;
        first_interval = false;
        new_word = true;
    }  
}

__attribute__((always_inline)) int QueryProcessor::goOverPriElem(long& pos, bitmap& bm) {
    long word_id = pos / 64;
    bool first_interval = false;
    bool new_word = false;
    while (word_id < mNumWords) {
        if (word_id > top_word) {
            // build basic bitmaps for the next word
            resetBitmap(bm);
            start_id = word_id * 2;
            build_bitmap_basic();
        }
        get_bitmap_comma(bm);
        IntervalInfo interval;
        if (first_interval == false) {
            if (new_word == true) {
                interval = get_interval_new_word(bm.commabit);
            } else {
                interval = get_interval(pos, bm.commabit);
            }
            first_interval = true;
        } else {
            interval = next_interval(bm.commabit);
        }
        get_bitmap_rbracket(bm);
        unsigned long bitmap_rbracket = bm.rbracketbit & interval.intervalbit;
        if (bitmap_rbracket) {
            pos = get_position(bitmap_rbracket, 1);
            return ARRAY_END;
        }
        if (interval.is_complete) {
            // position before comma
            pos = interval_end(interval.intervalbit);
            pos = pos - 1;
            return SUCCESS;
        }
        // interval is incomplete in the current word
        ++word_id;
        first_interval = false;
        new_word = true;
    }
}

__attribute__((always_inline)) int QueryProcessor::goOverPriElems(long& pos, bitmap& bm) {
    long word_id = pos / 64;
    bool new_word = false;
    while (word_id < mNumWords) {
        if (word_id > top_word) {
            // build basic bitmaps for the next word
            resetBitmap(bm);
            start_id = word_id * 2;
            build_bitmap_basic();
        }
        get_bitmap_lbrace(bm);
        get_bitmap_lbracket(bm);
        unsigned long bitmap_bracket = bm.lbracebit | bm.lbracketbit;
        IntervalInfo interval;
        if (new_word == true) {
            interval = get_interval_new_word(bitmap_bracket);
        } else {
            interval = get_interval(pos, bitmap_bracket);
        }
        get_bitmap_rbracket(bm);
        unsigned long bitmap_rbracket = bm.rbracketbit & interval.intervalbit;
        if (bitmap_rbracket) {
            pos = get_position(bitmap_rbracket, 1);
            return ARRAY_END;
        }
        if (interval.is_complete) {
            pos = interval_end(interval.intervalbit);
            return SUCCESS;
        }
        ++word_id;
        new_word = true;
    }
}

__attribute__((always_inline)) int QueryProcessor::goToObjElem(long& pos, bitmap& bm) {
    do {
        if (mRecord[pos] != '{' || mRecord[pos] != '[') {
        int result = goOverPriElems(pos, bm);
        if (result == ARRAY_END) {
            return result;
        }
        }
        int element_type = getElementType(pos);
        if (element_type == OBJECT) {
            return SUCCESS;
        }
        goOverAry(pos, bm);
    } while (hasMoreElements(pos));
    return OBJECT_END;
}

__attribute__((always_inline)) int QueryProcessor::goToAryElem(long& pos, bitmap& bm) {
    do {
        if (mRecord[pos] != '{' || mRecord[pos] != '[') {
            int result = goOverPriElems(pos, bm);
            if (result == ARRAY_END) {
                return result;
            }
        }
        int element_type = getElementType(pos);
        if (element_type == ARRAY) {
            return SUCCESS;
        }
        goOverObj(pos, bm);
    } while (hasMoreElements(pos));
    return OBJECT_END;
}

__attribute__((always_inline)) int QueryProcessor::goOverPriAttrs(long& pos, bitmap& bm) {
    long word_id = pos / 64;
    bool new_word = false;
    while (word_id < mNumWords) {
        if (word_id > top_word) {
            // build basic bitmaps for the next word
            resetBitmap(bm);
            start_id = word_id * 2;
            build_bitmap_basic();
        }
        get_bitmap_lbrace(bm);
        get_bitmap_lbracket(bm);
        unsigned long bitmap_bracket = bm.lbracebit | bm.lbracketbit; 
        IntervalInfo interval;
        if (new_word == true) {
            interval = get_interval_new_word(bitmap_bracket);
        } else {
            interval = get_interval(pos, bitmap_bracket);
        }
        get_bitmap_rbrace(bm);
        unsigned long bitmap_rbrace = bm.rbracebit & interval.intervalbit;
        if (bitmap_rbrace) {
            pos = get_position(bitmap_rbrace, 1);
            return OBJECT_END;
        }
        if (interval.is_complete) {
            pos = interval_end(interval.intervalbit);
            return SUCCESS;
        }
        ++word_id;
        new_word = true; 
    }
}

__attribute__((always_inline)) int QueryProcessor::goToObjAttr(long& pos, bitmap& bm) {
    do {
        int result = goOverPriAttrs(pos, bm);
        if (result == OBJECT_END) {
            return result;
        }
        int attribute_type = getAttributeType(pos);
        if (attribute_type == OBJECT) {
            return SUCCESS;
        }
        goOverAry(pos, bm);
    } while (hasMoreAttributes(pos));
    return OBJECT_END;
}

__attribute__((always_inline)) int QueryProcessor::goToAryAttr(long& pos, bitmap& bm) {
    do {
        int result = goOverPriAttrs(pos, bm);
        if (result == OBJECT_END) {
            return result;
        }
        int attribute_type = getAttributeType(pos);
        if (attribute_type == ARRAY) {
            return SUCCESS;
        }
        goOverObj(pos, bm);
    } while (hasMoreAttributes(pos));
    return OBJECT_END;
}

__attribute__((always_inline)) int QueryProcessor::goToPrimAttr(long& pos, bitmap& bm) {
    long word_id = pos / 64;
    bool first_interval = false;
    bool new_word = false;
    while (true) {
        while (word_id < mNumWords) {
            if (word_id > top_word) {
                // build basic bitmaps for the next word
                resetBitmap(bm);
                start_id = word_id * 2;
                build_bitmap_basic();
            }
            get_bitmap_colon(bm);
            IntervalInfo interval;
            if (first_interval == false) {
                if (new_word == true) {
                    interval = get_interval_new_word(bm.colonbit);
                    new_word = false;
                } else {
                    interval = get_interval(pos, bm.colonbit);
                }
                first_interval = true;
            } else {
                interval = next_interval(bm.colonbit);
            }
            get_bitmap_rbrace(bm);
            unsigned long bitmap_rbrace = bm.rbracebit & interval.intervalbit;
            if (bitmap_rbrace > 0) {
                // object ends
                pos = get_position(bitmap_rbrace, 1);
                return OBJECT_END;
            }
            if (interval.is_complete) {
                pos = interval_end(interval.intervalbit) + 1;
                int type = getAttributeType(pos);
                if (type == OBJECT) {
                    goOverObj(pos, bm);
                    word_id = pos / 64;  // update word id 
                    first_interval = false;
                }
                else if (type == ARRAY) {
                    goOverAry(pos, bm);
                    word_id = pos / 64; // update word id 
                    first_interval = false;
                }
                else {
                    return SUCCESS;
                }
                break;
            }
            ++word_id;
            first_interval = false;
            new_word = true;
        }
    }
}

__attribute__((always_inline)) JumpInfo QueryProcessor::goOverPrimElemsInRange(long& pos, int num_elements, bitmap& bm) {
    int word_id = pos / 64;
    bool new_word = false;
    int num_comma = 0;
    while (word_id < mNumWords) {
        if (word_id > top_word) {
            // build basic bitmaps for the next word
            resetBitmap(bm);
            start_id = word_id * 2;
            build_bitmap_basic();
        }
        get_bitmap_lbrace(bm);
        get_bitmap_lbracket(bm);
        unsigned long bitmap_bracket = bm.lbracebit | bm.lbracketbit;
        IntervalInfo interval;
        if (new_word == true) {
            interval = get_interval_new_word(bitmap_bracket);
        } else {
            interval = get_interval(pos, bitmap_bracket);
        }
        build_bitmap_rbracket(bm);
        unsigned long bitmap_rbracket = bm.rbracketbit & interval.intervalbit;
        get_bitmap_comma(bm);
        unsigned long bitmap_comma = bm.commabit & interval.intervalbit;
        if (bitmap_rbracket) {
            bitmap_comma = bitmap_comma & (bitmap_rbracket ^ (bitmap_rbracket - 1));
        }
        num_comma = num_comma +__builtin_popcountl(bitmap_comma);
        if (num_comma >= num_elements) {
            long temp_pos = word_id * 64 + __builtin_ctzll(bitmap_comma);
            pos = get_position(bitmap_comma, num_elements);
            JumpInfo ji(SUCCESS);
            return ji;
        }
        if (bitmap_rbracket) {
            // end of array
            pos = get_position(bitmap_rbracket, 1);
            JumpInfo ji(ARRAY_END);
            return ji;
        } else {
            if (interval.is_complete) {
                pos = interval_end(interval.intervalbit);// + 1;
                JumpInfo ji(PARTIAL_SKIP, num_comma);
                return ji;
            }
            num_elements -= num_comma;
        }
        // interval is incomplete in the current word
        ++word_id;
        new_word = true;
    }
}


__attribute__((always_inline)) int QueryProcessor::goOverElem(long& pos, int num_elements, bitmap& bm) {
    while (num_elements > 0) {
        if (!hasMoreElements(pos)) {
            return ARRAY_END;
        }
        int element_type = getElementType(pos);
        int result = 0;
        switch(element_type) {
            case PRIMITIVE: {
                JumpInfo res = goOverPrimElemsInRange(pos, num_elements, bm);
                if (res.status == ARRAY_END || res.status == SUCCESS) {
                    return res.status;
                }
                if (res.status == PARTIAL_SKIP) {
                    num_elements = num_elements - res.num_comma + 1;
                }
                break;
            }
            case OBJECT:
                goOverObj(pos, bm);
                break;
            case ARRAY:
                goOverAry(pos, bm);
                break;
        }
        --num_elements;
    }
    return SUCCESS;
}

__attribute__((always_inline)) int QueryProcessor::goToObjElemInRange(long& pos, int& num_elements, bitmap& bm) {
     do {
        int element_type = getElementType(pos);
        int result = 0;
        switch(element_type) {
            case PRIMITIVE: {
                JumpInfo res = goOverPrimElemsInRange(pos, num_elements, bm);
                if (res.status == ARRAY_END) {
                    return res.status;
                }
                if (res.status == SUCCESS) {
                    return RANGE_END;
                }
                if (res.status == PARTIAL_SKIP) {
                    num_elements = num_elements - res.num_comma + 1;
                }
                break;
            }
            case OBJECT:
                return SUCCESS;
            case ARRAY:
                goOverAry(pos, bm);
                break;
        }
        --num_elements;
        if (!hasMoreElements(pos)) {
            return ARRAY_END;
        }
    } while (num_elements > 0);
    return RANGE_END;
}

__attribute__((always_inline)) int QueryProcessor::goToAryElemInRange(long& pos, int& num_elements, bitmap& bm) {
    do {
        int element_type = getElementType(pos);
        int result = 0;
        switch(element_type) {
            case PRIMITIVE: {
                JumpInfo res = goOverPrimElemsInRange(pos, num_elements, bm);
                if (res.status == ARRAY_END) {
                    return res.status;
                }
                if (res.status == SUCCESS) {
                    return RANGE_END;
                }
                if (res.status == PARTIAL_SKIP) {
                    num_elements = num_elements - res.num_comma + 1;
                }
                break;
            }
            case OBJECT:
                goOverObj(pos, bm);
                break;
            case ARRAY:
                return SUCCESS;
        }
        --num_elements;
        if (!hasMoreElements(pos)) {
            return ARRAY_END;
        }
    } while (num_elements > 0);
    return RANGE_END;
}

__attribute__((always_inline)) int QueryProcessor::goToPrimElemInRange(long& pos, int& num_elements, bitmap& bm) {
    do {
        int element_type = getElementType(pos);
        int result = 0;
        switch(element_type) {
            case PRIMITIVE: {
                return SUCCESS;
            }
            case OBJECT:
                goOverObj(pos, bm);
                break;
            case ARRAY:
                goOverAry(pos, bm);
        }
        --num_elements;
        if (!hasMoreElements(pos)) {
            return ARRAY_END;
        }
    } while (num_elements > 0);
    return RANGE_END;
}

__attribute__((always_inline)) bool QueryProcessor::hasMoreElements(long& pos) {
    while (mRecord[pos] == ' ' || mRecord[pos] == '\n' || mRecord[pos] == '\r') ++pos;
    ++pos;
    while (mRecord[pos] == ' ' || mRecord[pos] == '\n' || mRecord[pos] == '\r') ++pos; 
    if (mRecord[pos] == ']') {
        return false;
    }
    if (mRecord[pos] == ',') ++pos;
    while (mRecord[pos] == ' ' || mRecord[pos] == '\n' || mRecord[pos] == '\r') ++pos;
    return true;
}

__attribute__((always_inline)) int QueryProcessor::getElementType(long& pos) {
    while (mRecord[pos] == ' ') ++pos;
    if (mRecord[pos] == '{') return OBJECT;
    if (mRecord[pos] == '[') return ARRAY;
    return PRIMITIVE;
}

__attribute__((always_inline)) int QueryProcessor::goToPrimElem(long& pos, bitmap& bm) {
    do {
        int element_type = getElementType(pos);
        switch (element_type) {
            case PRIMITIVE:
                return SUCCESS;
            case OBJECT:
                goOverObj(pos, bm);
                break;
            case ARRAY:
                goOverAry(pos, bm);
        }
    } while (hasMoreElements(pos));
    return ARRAY_END;
}

__attribute__((always_inline)) bool QueryProcessor::hasMoreAttributes(long& pos) {
    // if current character is blank, skip this character until meeting a non-blank character
    while (mRecord[pos] == ' ') ++pos;
    ++pos;
    while (mRecord[pos] == ' ') {
        ++pos;
    }
    if (mRecord[pos] == '}') {
        return false;
    }
    if (mRecord[pos] == ',') ++pos;
    while (mRecord[pos] == ' ' || mRecord[pos] == '\n') ++pos; 
    return true;
}

__attribute__((always_inline)) int QueryProcessor::getAttributeType(long& pos) {
    while (mRecord[pos] == ' ') ++pos;
    if (mRecord[pos] == '{') return OBJECT;
    if (mRecord[pos] == '[') return ARRAY;
    return PRIMITIVE;
}

void QueryProcessor::object(long& pos, bitmap& bm) {
    int attribute_type = qa.typeExpectedInObj();
    while (hasMoreAttributes(pos)) {
        int result = 0;
        int next_state = 0;
        int element_type = attribute_type;
        switch (attribute_type) {
            case OBJECT:
                result = goToObjAttr(pos, bm);
                break;
            case ARRAY:
                result = goToAryAttr(pos, bm);
                break;
            case PRIMITIVE: {
                long st = pos;
                while (mRecord[st] != '"') ++st;
                long ed = st + 1;
                while (mRecord[ed] != '"') ++ed;
                int key_len = ed - st - 1;
                memcpy(mKey, mRecord + st + 1, key_len);
                mKey[key_len] = '\0';
                next_state = qa.getNextState(mRecord + st + 1, key_len);
                while (mRecord[ed] != ':') ++ed; 
                pos = ed + 1;
                element_type = getElementType(pos);
            }
        }
        if (result == OBJECT_END)
            return;
        if (attribute_type != PRIMITIVE) {
            long st = pos;
            while (mRecord[st] != ':') --st;
            while (mRecord[st] != '"') --st;
            long ed = st - 1;
            while (mRecord[ed] != '"') --ed;
            int key_len = st - ed - 1;
            memcpy(mKey, mRecord + ed + 1, key_len);
            mKey[key_len] = '\0';
            next_state = qa.getNextState(mRecord + ed + 1, key_len);
        }
        if (next_state == UNMATCHED_STATE) {
            switch (element_type) {
                case OBJECT:
                    goOverObj(pos, bm);
                    break;
                case ARRAY:
                    goOverAry(pos, bm);
                    break;
                case PRIMITIVE: {
                    goOverPriAttr(pos, bm);
                }
            }
        } else if (qa.isAccept(next_state) == true) { //ACCEPT
            ++mNumMatches;
            long start_pos = pos;
            switch (element_type) {
                case OBJECT: {
                    goOverObj(pos, bm);
                    break;
                }
                case ARRAY: {
                    goOverAry(pos, bm);
                    break;
                }
                case PRIMITIVE:
                    goOverPriAttr(pos, bm);
                    ++pos;
            }
            long end_pos = pos;
            long text_length = end_pos - start_pos + 1;
            memcpy(mText, mRecord + start_pos, text_length);
            mText[text_length] = '\0';
            mOutput.append(mText);
            mOutput.append(";");
            if (mRecord[pos] != '}') {
                if (qa.getStackSize() == 0) return;
                goToObjEnd(pos, bm);
            }
            break;
        } else {  // in-progress
            qa.pushStack(next_state);
            switch (attribute_type) {
                case OBJECT:
                    object(pos, bm);
                    break;
                case ARRAY:
                    array(pos, bm);
            }
            qa.popStack(); // virtual token "value"
            if (qa.getStackSize() == 0) return;
            goToObjEnd(pos, bm);
            break;
        }
    }
}

void QueryProcessor::array(long& pos, bitmap& bm) {
    int next_state = qa.getNextStateNoKey();
    qa.pushStack(next_state);
    int element_type = qa.typeExpectedInArr();
    long prev_pos = -1; // only use for debugging
    if (qa.hasIndexConstraints()) {
        IndexInfo idx_info = qa.getIndexInfo(qa.mCurState);
        int start_idx = idx_info.start_idx;
        int end_idx = idx_info.end_idx;
        int num_elements = end_idx - start_idx;
        if (start_idx > 0) {
            int result = goOverElem(pos, start_idx, bm);
            if (result == ARRAY_END) {
                qa.popStack();
                return; 
            }
        }
        while (hasMoreElements(pos) && num_elements > 0) {
            if (qa.isAccept(qa.mCurState) == true) {
                ++mNumMatches;
                long start_pos = pos;
                bool break_while = false;
                int value_type = element_type;
                if (element_type == PRIMITIVE) {
                    value_type = getElementType(pos); 
                }
                switch (value_type) {
                    case OBJECT: {
                        goOverObj(pos, bm);
                        break;
                    }
                    case ARRAY: {
                        goOverAry(pos, bm);
                        break;
                    }
                    case PRIMITIVE: {
                        int result = goOverPriElem(pos, bm);
                        if (result == ARRAY_END) {
                            break_while = true;
                        }
                    }
                }
                long end_pos = pos;
                long text_length = end_pos - start_pos + 1;
                memcpy(mText, mRecord + start_pos, text_length);
                mText[text_length] = '\0';
                mOutput.append(mText);
                mOutput.append(";");
                if (break_while) {
                    if (mRecord[pos] != ']')
                        goToAryEnd(pos, bm);
                    break;
                }
                --num_elements;
            } else if (qa.mCurState > 0) {
                int result; 
                switch (element_type) {
                    case OBJECT: {
                        result = goToObjElemInRange(pos, num_elements, bm);
                        break;
                    }
                    case ARRAY: {
                        result = goToAryElemInRange(pos, num_elements, bm);
                    }
                }
                if (result == SUCCESS) {
                    switch (element_type) {
                        case OBJECT:
                            prev_pos = pos;
                            object(pos, bm);
                            break;
                        case ARRAY: {
                            array(pos, bm);
                        }
                    }
                    --num_elements;
                } else if (result == ARRAY_END) {
                    qa.popStack();
                    return;
                } else if (result == RANGE_END) {
                    if (mRecord[pos] != ']') {
                        if (qa.getStackSize() == 1) return;
                        goToAryEnd(pos, bm);
                    }
                    break;
                }
            }
        }
        if (mRecord[pos] != ']') {
            if (qa.getStackSize() == 1) return;
            goToAryEnd(pos, bm);
        }
    } else {
        while (hasMoreElements(pos)) {
            if (qa.isAccept(qa.mCurState) == true) {
                ++mNumMatches;
                long start_pos = pos;
                bool break_while = false;
                int value_type = element_type;
                if (element_type == PRIMITIVE)
                    value_type = getElementType(pos);
                switch (value_type) {
                    case OBJECT: {
                        goOverObj(pos, bm);
                        break;
                    }
                    case ARRAY: {
                        goOverAry(pos, bm);
                        break;
                    }
                    case PRIMITIVE: {
                        int result = goOverPriElem(pos, bm);
                        if (result == ARRAY_END) {
                            break_while = true;
                        }
                    }
                }
                long end_pos = pos;
                long text_length = end_pos - start_pos + 1;
                memcpy(mText, mRecord + start_pos, text_length);
                mText[text_length] = '\0';
                mOutput.append(mText);
                mOutput.append(";");
                if (break_while) break;
            } else if (qa.mCurState > 0) {
                if (getElementType(pos) != element_type) {
                    int result;
                    switch (element_type) {
                        case OBJECT:
                            result = goToObjElem(pos, bm);
                            break;
                        case ARRAY:
                            result = goToAryElem(pos, bm);
                    }
                    if (result == ARRAY_END) {
                        qa.popStack();
                        return;
                    }
                }
                switch (element_type) {
                    case OBJECT:
                        prev_pos = pos;
                        object(pos, bm);
                        break;
                    case ARRAY: {
                        array(pos, bm);;
                    }
                }
            }
        }
    }
    qa.popStack();
}

char QueryProcessor::getNextNonEmptyCharacter(long& pos) {
    char ch = mRecord[pos];
    while (mRecord[pos] == ' ') ++pos;
    return mRecord[pos];
}

long QueryProcessor::getOutputMatchesNum() {
    return mNumMatches;
}

string QueryProcessor::runQuery(Record* rec) {
    setRecordText(rec->text + rec->rec_start_pos, rec->rec_length);
    init();
    long cur_pos = 0;
    char ch = getNextNonEmptyCharacter(cur_pos);
    bitmap bm;
    if (ch == '{' && qa.typeExpectedInObj() != NONE)
        object(cur_pos, bm);
    else if(ch == '[' && qa.typeExpectedInArr() != NONE)
        array(cur_pos, bm);
    return mOutput;
}
#endif



string execute_query(const char* input) {
// std::string execute_query(char* input) {
//int main(){
 // char* file_path = "../dataset/twitter_sample_large_record.json";
 // const char* file_path = "../dataset/twitter_sample_large_record.json";
    cout<<"start loading the single large record from "<<input<<endl;
    Record* rec = RecordLoader::loadSingleRecord(input);
    if (rec == NULL) {
        cout<<"record loading fails."<<endl;
        return "record loading fails";
    }
    cout<<"finish loading the single large record"<<endl;

    string query = "$[*].entities.urls[*].url";
    cout<<"\nstart executing query "<<query<<endl;
    QueryProcessor processor(query);
    string output = processor.runQuery(rec);
    cout<<"finish query execution"<<endl;
    cout<<"matches are: "<<output<<endl;
    return output;
}


int add(int i, int j) {
    return i + j;
}

int kapilan(int i, int j) {
    return i + j;
}

namespace py = pybind11;

PYBIND11_MODULE(JSONSki, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: JSONSki

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.

    )pbdoc");
    
    m.def("kapilan", &kapilan, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

    m.def("execute_query", &execute_query, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

    m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
