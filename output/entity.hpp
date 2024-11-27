#ifndef ENTITY
#define ENTITY

#include "common.hpp"

#include <cmath>
#include <iostream>
#include <string>
#include <stdexcept>
#include <map>
#include <set>
#include <vector>
#include <algorithm>

// TODO(us): Pass some public methods to private
class Entity {
  public:
    friend std::ostream& operator<<(std::ostream& os, Entity entity) {
        os << entity.get_value();
        return os;
    }

    struct Comparator {
        bool operator()(Entity a, Entity b) const {
            if (a.type == b.type) {
                if (a.type == DICT) {
                    return a.dict < b.dict;
                }
                return (a < b).is_true();
            }
            return a.type < b.type;
        }
    };

    class Iterator{
        friend class Entity;
        private:
            int ite_type;
            Entity* object;
            std::vector<Entity>::iterator list_iter;
            std::vector<Entity>::iterator list_end;
            std::vector<Entity>::iterator tuple_iter;
            std::vector<Entity>::iterator tuple_end;
            std::set<Entity>::iterator set_iter;
            std::set<Entity>::iterator set_end;
            std::map<Entity, Entity>::iterator dict_iter;
            std::map<Entity, Entity>::iterator dict_end;

        public:
            Iterator() {
                this->ite_type = INT;
                this->object = NULL;
            }
            Iterator(Entity* object) {
                this->ite_type = object->get_type();
                this->object = object;
                this->initialize_iterator();
            }

            void initialize_iterator() {
                switch (this->ite_type) {
                    case LIST:
                        this->list_iter = this->object->list.begin();
                        this->list_end = this->object->list.end();
                        break;
                    case TUPLE:
                        this->tuple_iter = this->object->tuple.begin();
                        this->tuple_end = this->object->tuple.end();
                        break;
                    case SET:
                        this->set_iter = this->object->set.begin();
                        this->set_end = this->object->set.end();
                        break;
                    case DICT:
                        this->dict_iter = this->object->dict.begin();
                        this->dict_end = this->object->dict.end();
                        break;
                    default:
                        throw std::runtime_error("Unsupported type for iterator");
                }
            }

            Entity next() {
                switch(this->ite_type) {
                    case LIST:
                        return *this->list_iter++;
                    case TUPLE:
                        return *this->tuple_iter++;
                    case SET:
                        return *this->set_iter++;
                    case DICT:
                        return this->dict_iter++->first;
                    default:
                        throw std::runtime_error("Unsupported type for iterator");  
                    }
            }

            bool has_next() const {
                switch (this->ite_type) {
                    case LIST:
                        return this->list_iter != this->list_end;
                    case TUPLE:
                        return this->tuple_iter != this->tuple_end;
                    case SET:
                        return this->set_iter != this->set_end;
                    case DICT:
                        return this->dict_iter != this->dict_end;
                    default:
                        throw std::runtime_error("Unsupported type for iterator");
                }
            }
        };

  private:
    int type;
    std::string value;
    bool append_tuple;
    std::vector<Entity> list;
    std::vector<Entity> tuple;
    std::map<Entity, Entity, Comparator> dict;
    std::set<Entity, Comparator> set;
    Entity::Iterator iterator;

    bool check_string(const Entity& other, std::string operator_type)const {
        if (operator_type == "+" && other.type == STRING) {
            return true;
        }
        if (operator_type == "*" && other.type == INT) {
            return true;
        }
        if (operator_type == "in" && other.type == STRING) {
            return true;
        }
        if (operator_type == "not in" && other.type == STRING) {
            return true;
        }
        
        return false;
    }

    bool check_number(const Entity& other, std::string operator_type)const {
        if (operator_type == "+" && other.type == STRING) {
            return true;
        }
        if (other.type == INT || other.type == DOUBLE) {
            return true;
        }
        if (operator_type == "*" && other.type == LIST) {
            return true;
        }
        if (operator_type == "*" && other.type == TUPLE) {
            return true;
        }
        return false;
    }

   bool check_list(const Entity& other, std::string operator_type)const {
        if (operator_type == "+" && other.type == LIST) {
            return true;
        }
        if (operator_type == "*" && other.type == INT) {
            return true;
        }
        if (operator_type == "-" && other.type == LIST) {
            return true;
        }
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
            return true;
        }
        return false;
    }

    bool check_tuple(const Entity&other, std::string operator_type)const {
        if (operator_type == "+" && other.type == TUPLE) {
            return true;
        }
        if (operator_type == "*" && other.type == INT) {
            return true;
        }
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
            return true;
        }
        return false;
    }

    bool check_set(const Entity& other, std::string operator_type)const {
        if ((operator_type == "-" || operator_type == "+") && other.type == SET) {
            return true;
        }
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
            return true;
        }        
        return false;
    }

    bool check_dict(const Entity& other, std::string operator_type)const {
        if (operator_type == "in") {
            return true;
        }
        if (operator_type == "not in") {
            return true;
        }
        return false;
    }

     Entity compare_vectors(const std::vector<Entity>& first, const std::vector<Entity>& second, bool equality) const {
        size_t min_size = std::min(first.size(), second.size());
        for (size_t i = 0; i < min_size; ++i) {
            Entity result = Entity(INT, "0"); 
            if (equality) {
                result = (first[i] == second[i]);
            } else {
                result = (first[i] < second[i]);
            }
            if (result.value == "1" && !equality) {
                return Entity(INT, "1"); // First is smaller so it is not smaller
            } else if (equality && result.value == "0") {
                return Entity(INT, "0");
            } else if (!equality && !((first[i] == second[i]).is_true())) {
                return Entity(INT, "0");
            }
        }
        if (equality) {
            return Entity(INT, (first.size() == second.size()) ? "1" : "0");
        }
        return Entity(INT, (first.size() < second.size()) ? "1" : "0");
    }

    Entity compare_sets(const std::set<Entity, Comparator>& first, const std::set<Entity, Comparator>& second, bool equality) const {
        if (equality) {
            if (first.size() != second.size()) return Entity(INT, "0");
            auto it1 = first.begin(), it2 = second.begin();
            while (it1 != first.end() && it2 != second.end()) {
                if (!(*it1 == *it2).value.empty() && (*it1 == *it2).value != "1") return Entity(INT, "0");
                ++it1;
                ++it2;
            }
            return Entity(INT, "1");
        } else {
            return Entity(INT, std::lexicographical_compare(first.begin(), first.end(), second.begin(), second.end(), Comparator()) ? "1" : "0");
        }
    }

    Entity compare_maps(const std::map<Entity, Entity, Comparator>& first, const std::map<Entity, Entity, Comparator>& second, bool equality) const {
        if (equality) {
            if (first.size() != second.size()) return Entity(INT, "0");
            auto it1 = first.begin(), it2 = second.begin();
            while (it1 != first.end() && it2 != second.end()) {
                if (!((it1->first == it2->first).value.empty() && (it1->first == it2->first).value == "1")) return Entity(INT, "0");
                if (!((it1->second == it2->second).value.empty() && (it1->second == it2->second).value == "1")) return Entity(INT, "0");
                ++it1;
                ++it2;
            }
            return Entity(INT, "1");
        } else {
            return Entity(INT, std::lexicographical_compare(first.begin(), first.end(), second.begin(), second.end(), Comparator()) ? "1" : "0");
        }
    }


  public:
    Entity() {
        this->type = NONE;
        this->value = "";
        this->append_tuple = true;
    }

    Entity(int type, std::string value ) {
        this->type = type;
        this->value = value;
        this->append_tuple = true;
    }

    Entity(int type, Entity::Iterator ite) {
        this->type = type;
        this->value = "";
        this->append_tuple = true;
        this->iterator = ite;
    }

    bool equals(const Entity& other) const {
        return this->type == other.type && this->value == other.value;
    }

    /*
    operator_types:
        +, - , *, **, /, //, ^, %
        in, and, or, not in

    Types:
        int, double, string, tuple, set, dict, class
    */
   // TODO(us): implementar is operable para las diferentes comparaciones
   // o cambiar losoperadores
    bool is_operable(std::string operator_type, const Entity& other)const {
        bool is_operable;
        
        switch(this->type) {
            case STRING:
                is_operable = check_string(other, operator_type);
                break;
            case INT: case DOUBLE:
                is_operable = check_number(other, operator_type);
                break;
            case LIST:
                is_operable = check_list(other, operator_type);
                break;
            case TUPLE:
                is_operable = check_tuple(other, operator_type);
                break;
            case SET:
                is_operable = check_set(other, operator_type);
                break;
            case DICT:
                is_operable = check_dict(other, operator_type);
                break;
            case CLASS:
                is_operable = true;
                break;
        }
        return is_operable;
    }

    void set_type(int type){
        this->type = type;
    }
    
    void set_value(std::string value){
        this->value = value;
    }
    
    int get_type(){
        return type;
    }

    void set_append_tuple(bool value){
        this->append_tuple = value;
    }
    
    bool get_append_tuple(){
        return this->append_tuple;
    }
    
    std::string get_value() const {
        switch (this->type) {
            case INT:
            case DOUBLE:
            case STRING:
                // Return the value directly for primitive types
                return value;
            case LIST:
                return serialize_list();
            case TUPLE:
                return serialize_tuple();
            case SET:
                return serialize_set();
            case DICT:
                return serialize_dict();
            default:
                throw std::runtime_error("Unsupported type in get_value() retrieval.");
        }
    }

    // Serialization helpers
    std::string serialize_list() const {
        std::string result = "[";
        for (size_t i = 0; i < list.size(); ++i) {
            result += list[i].get_value();
            if (i != list.size() - 1) {
                result += ", ";
            }
        }
        result += "]";
        return result;
    }

    std::string serialize_tuple() const {
        std::string result = "(";
        for (size_t i = 0; i < tuple.size(); ++i) {
            result += tuple[i].get_value();
            if (i != tuple.size() - 1) {
                result += ", ";
            }
        }
        result += ")";
        return result;
    }

    std::string serialize_set() const {
        std::string result = "{";
        for (auto it = set.begin(); it != set.end(); ++it) {
            result += it->get_value();
            if (std::next(it) != set.end()) {
                result += ", ";
            }
        }
        result += "}";
        return result;
    }

    std::string serialize_dict() const {
        std::string result = "{";
        for (auto it = dict.begin(); it != dict.end(); ++it) {
            result += it->first.get_value() + ": " + it->second.get_value();
            if (std::next(it) != dict.end()) {
                result += ", ";
            }
        }
        result += "}";
        return result;
    }


    bool is_true() const {
        double num_value = 0.0;
        switch (this->type) {
            case INT:
            case DOUBLE: 
                num_value = std::stod(this->value);
                return num_value != 0.0;
                break;
            case STRING: 
                return !this->value.empty();
                break;
            case LIST: // TODO(us): check if it's this way
                return !this->tuple.empty();
                    break;
            case TUPLE: // TODO(us): check if it's this way
                return !this->tuple.empty();
                break;
            case SET: // TODO(us): check if it's this way
                return !this->set.empty();
                break;
            case DICT: // TODO(us): check if it's this way
                return !this->dict.empty();
                break;
            case CLASS: // TODO(us): check if it's this way
                return true;
                break;
             case NONE:
                // NoneType is always false
                return false;
            default: 
                throw std::runtime_error("Unsupported type in is_true() evaluation.");
        }
    }


    Entity type_py() const {
        switch (type) {
            case INT: return Entity(STRING, "int");
            case DOUBLE: return Entity(STRING,"float");
            case STRING: return Entity(STRING,"str");
            case LIST: return Entity(STRING,"list");
            case TUPLE: return Entity(STRING,"tuple");
            case SET: return Entity(STRING,"set");
            case DICT: return Entity(STRING,"dict");
            case CLASS: return Entity(STRING,"class");
            case NONE: return Entity(STRING,"NoneType");
            default: return Entity(STRING,"unknown");
        }
    }

    Entity cast(int target_type) const {
        switch (target_type) {
            case INT: return to_int();
            case DOUBLE: return to_double();
            case STRING: return to_string();
            case BOOL: return to_bool();
            default:
                throw std::runtime_error("Unsupported cast target type.");
        }
    }

    Entity to_int() const {
        if (type == INT) {
            return *this; // Already an INT
        }
        if (type == DOUBLE || type == STRING) {
            return Entity(INT, std::to_string(static_cast<int>(std::stod(value))));
        }
        throw std::runtime_error("Cannot cast to INT from this type.");
    }

    Entity to_double() const {
        if (type == DOUBLE) {
            return *this; // Already a DOUBLE
        }
        if (type == INT || type == STRING) {
            return Entity(DOUBLE, std::to_string(std::stod(value)));
        }
        throw std::runtime_error("Cannot cast to DOUBLE from this type.");
    }

    Entity to_string() const {
        if (type == STRING) {
            return *this; // Already a STRING
        }
        return Entity(STRING, get_value()); 
    }

    Entity to_bool() const {
        bool result = this->is_true(); 
        return Entity(INT, result ? "1" : "0");
    }

    // TODO(us): check if the way it is called works (I don't know if
    // start will die before the range is calculated)
    Entity range() const {
        Entity start = Entity(INT, "0");
        Entity range = start.range(*this, Entity(INT, "1"));
        return range;
    }

    Entity range(Entity stop) const {
        return this->range(stop, Entity(INT, "1"));
    }

    Entity range(Entity stop, Entity step) const {
        Entity start = *this;
        if (start.get_type() != INT || stop.get_type() != INT || step.get_type() != INT) {
            throw std::invalid_argument("range() arguments must be integers.");
        }

        int start_value = std::stoi(start.get_value());
        int stop_value = std::stoi(stop.get_value());
        int step_value = std::stoi(step.get_value());

        if (step_value == 0) {
            throw std::invalid_argument("range() step argument must not be zero.");
        }

        Entity result(LIST, "");
        std::vector<Entity> values;

        if (step_value > 0) {
            for (int i = start_value; i < stop_value; i += step_value) {
                values.emplace_back(INT, std::to_string(i));
            }
        } else {
            for (int i = start_value; i > stop_value; i += step_value) {
                values.emplace_back(INT, std::to_string(i));
            }
        }
        result.list = values;
        return result;
    }


    Entity sum(Entity start = Entity(INT, "0")) {
        if (start.get_type() != INT && start.get_type() != DOUBLE) {
            throw std::invalid_argument("Start value must be INT or DOUBLE.");
        }

        Entity result = start;

        switch (this->get_type()) {
            case LIST:
                for (const auto& element : this->list) {
                    result = result + element; 
                }
                break;
            case TUPLE:
                for (const auto& element : this->tuple) {
                    result = result + element; 
                }
                break;
            case SET:
                for (const auto& element : this->set) {
                    result = result + element; 
                }
                break;
            case DICT:
                for (const auto& pair : this->dict) {
                    result = result + pair.first;
                }
                break;
            default:
                throw std::invalid_argument("Invalid type for sum. Must be LIST, TUPLE, SET, or DICT.");
        }

        return result;
    }


    bool analyze_int_double(int type) const {
        if ((this->type == DOUBLE || this->type == INT) && type == DOUBLE){
            return true;
        }
        if (this->type == DOUBLE && (type == DOUBLE || type == INT)){
            return true;
        }
        return false;
    }

    Entity operator+(const Entity& other) const {
        if (this->is_operable("+", other)) {
            if (this->type == STRING && other.type == STRING) {
                return Entity(STRING, this->value + other.value);
            }
            if (this->type == INT && other.type == INT) {
                int result = std::stoi(this->value) + std::stoi(other.value);
                return Entity(this->type, std::to_string(result));
            }
            if (this->analyze_int_double(other.type)) {
                double result = std::stod(this->value) + std::stod(other.value);
                return Entity(DOUBLE, std::to_string(result));
            }
            if (this->type == LIST && other.type == LIST) {
                Entity result(LIST, "");
                result.list = this->list;
                result.list.insert(result.list.end(), other.list.begin(), other.list.end());
                return result;
            }
            if (this->type == TUPLE && other.type == TUPLE) {
                Entity result(TUPLE, "");
                result.tuple = this->tuple;
                result.tuple.insert(result.tuple.end(), other.tuple.begin(), other.tuple.end());
                return result;
            }
            if (this->type == SET && other.type == SET) {
                Entity result(SET, "");
                result.set = this->set;
                result.set.insert(other.set.begin(), other.set.end());
                return result;
            }
        }
        throw std::invalid_argument("Invalid operaton for the given types with +.");
    }

    Entity operator-(const Entity& other) const {
        if (this->is_operable("-", other)) {
            if (this->analyze_int_double(other.type)) {
                double result = std::stod(this->value) - std::stod(other.value);
                return Entity(DOUBLE, std::to_string(result));
            }
            if (this->type == INT && other.type == INT ) {
                int result = std::stoi(this->value) - std::stoi(other.value);
                return Entity(this->type, std::to_string(result));
            }
            if (this->type == LIST && other.type == LIST) {
                Entity result(LIST, "");
                result.list = this->list;
                for (const auto& elem : other.list) {
                    result.list.erase(
                        std::remove_if(result.list.begin(), result.list.end(),
                                    [&](const Entity& e) { return (e == elem).is_true(); }),
                        result.list.end());
                }
                return result;
            }
            if (this->type == SET && other.type == SET) {
                Entity result(SET, "");
                result.set = this->set;
                for (const auto& elem : other.set) {
                    result.set.erase(elem);
                }
                return result;
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with -.");
    }

    Entity operator-() const {
        if (this->type == INT) {
            double result = -1 * std::stoi(this->value);
            return Entity(DOUBLE, std::to_string(result));
        }
        if (this->type == DOUBLE) {
            double result = -1.0 * std::stod(this->value);
            return Entity(DOUBLE, std::to_string(result));
        }
        throw std::invalid_argument("Invalid operation for the given types with -.");
    }

    Entity operator*(const Entity& other) const {
        if (this->is_operable("*", other)) {
            if (this->analyze_int_double(other.type)) {
                double result = std::stod(this->value) * std::stod(other.value);
                return Entity(DOUBLE, std::to_string(result));
            }
            if (this->type == INT && other.type == INT) {
                int result = std::stoi(this->value) * std::stoi(other.value);
                return Entity(INT, std::to_string(result));
            }
            if (this->type == STRING && other.type == INT) {
                std::string result;
                int times = std::stoi(other.value);
                for (int i = 0; i < times; ++i) {
                    result += this->value;
                }
                return Entity(STRING, result);
            }
            if ((this->type == LIST || this->type == TUPLE) && other.type == INT) {
                Entity result(this->type, "");
                int times = std::stoi(other.value);
                if (times < 0) {
                    throw std::invalid_argument("Invalid operation: cannot repeat a list/tuple negative times.");
                }
                for (int i = 0; i < times; ++i) {
                    if (this->type == LIST) {
                        result.list.insert(result.list.end(), this->list.begin(), this->list.end());
                    } else if (this->type == TUPLE) {
                        result.tuple.insert(result.tuple.end(), this->tuple.begin(), this->tuple.end());
                    }
                }
                return result;
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with *.");
    }

    Entity operator/(const Entity& other) const {
        if (this->is_operable("/", other)) {
            if (this->type == INT && other.type == INT) {
                int result = std::stoi(this->value) / std::stoi(other.value);
                return Entity(this->type, std::to_string(result));
            }
            if (this->analyze_int_double(other.type)) {
                double result = std::stod(this->value) / std::stod(other.value);
                return Entity(DOUBLE, std::to_string(result));
            }
        }
       throw std::invalid_argument("Invalid operation for the given types with /.");
    }

    Entity operator%(const Entity& other) const {
        if (this->is_operable("%", other)) {
            int result = std::stoi(this->value) % std::stoi(other.value);
            return Entity(INT, std::to_string(result));
       }
        throw std::invalid_argument("Invalid operation for the given types with %.");
    }

    Entity operator^(const Entity& other) const {
        if (this->is_operable("^", other)) {
            if (this->analyze_int_double(other.type)) {
                double result = std::pow(std::stod(this->value), std::stod(other.value));
                return Entity(DOUBLE, std::to_string(result));
            }
            if (this->type == INT && other.type == INT) {
                int result = std::pow(std::stoi(this->value),std::stoi(other.value));
                return Entity(this->type, std::to_string(result));
            }
        }
        throw std::invalid_argument("Invalid opration for the given types with ^.");
    }

    // Logical and Comparison operator_types
    Entity operator&&(const Entity& other) const {
        return Entity(INT, (this->is_true() && other.is_true()) ? "1" : "0");
    }

    Entity operator||(const Entity& other) const {
        return Entity(INT, (this->is_true() || other.is_true()) ? "1" : "0");
    }

    Entity operator==(const Entity& other) const {
        if((this->type == INT || this->type == DOUBLE) && (other.type == INT || other.type == DOUBLE)) {
            bool result = (std::stod(this->value) == std::stod(other.value));
            if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        } else if (this->type != other.type) {
            return Entity(INT, "0");
        } else if (this->type == STRING) {
            bool result = this->value == other.value;
            if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        } else if (this->type == LIST) {
             return compare_vectors(this->list, other.list, true);
        } else if (this->type == SET) {
            return compare_sets(this->set, other.set, true);
        } else if (this->type == DICT) {
             return compare_maps(this->dict, other.dict, true);
        } else if (this->type == TUPLE) {
            return compare_vectors(this->tuple, other.tuple, true);
        }
        return Entity(INT, "0");  
    }

    Entity operator!=(const Entity& other) const {
        Entity result = (*this == other);
        if (result.value == "1") {
            result.value = "0";
        } else { // result.value == 0
            result.value = "1";
        }
        return result;
    }

    Entity operator<(const Entity& other) const {
        if (this->type != other.type || this->type == DICT) {
            throw std::invalid_argument("Invalid operation for the given types with <.");    
        }

        Entity less_than;

        if (this->type == INT || this->type == DOUBLE) {
            bool result =  std::stod(this->value) < std::stod(other.value);
            if (result) {
                less_than = Entity(INT, "1");
            } else { 
                less_than = Entity(INT, "0");
            }
        }

        if (this->type == STRING) {
            // TODO(us): check this
            int i, j = 0;
            while (i < this->value.length() && j < other.value.length()) {
                if (this->value[i] > other.value[j]) {
                    less_than = Entity(INT, "0");
                }
                ++i;
                ++j;
            }
            less_than = Entity(INT, "1");
        }

        // TODO(us): verify is this is correct for python:
        if (this->type == LIST) {
            less_than = compare_vectors(this->list, other.list, false);
        }

        if (this->type == TUPLE) {
            less_than = compare_vectors(this->tuple, other.tuple, false);
        }

        if (this->type == SET) {
            less_than = compare_sets(this->set, other.set, false);
        }

        if (this->type == DICT) {
            less_than = compare_maps(this->dict, other.dict, false);
        }

        return less_than;
    }

    Entity operator>(const Entity& other) const {
        bool result1 = (*this == other).is_true();
        bool result2 = (*this < other).is_true();
        bool result = (result1 || result2);
        if (result) {
           return Entity(INT, "0");
        } else {
            return Entity(INT, "1");
        }
        
    }

    Entity operator<=(const Entity& other) const {
        bool result1 = (*this == other).is_true();
        bool result2 = (*this < other).is_true();
        bool result = (result1 || result2);
        if (result) {
           return Entity(INT, "1");
        } else {
            return Entity(INT, "0");
        }
    }

    Entity operator>=(const Entity& other) const {
        bool less_than = (*this < other).is_true();
        if (!less_than) {
           return Entity(INT, "1");
        } else {
            return Entity(INT, "0");
        }
    }

    Entity operator!() const {
        return Entity(INT, (!this->is_true()) ? "1" : "0");
    }

    // Membership operator_types

    // TODO(us): revisar que tenga sentido
    Entity in(Entity& container) {
        if (container.is_operable("in", *this)) {
            switch(this->type) {
                case LIST:
                    return this->vector_in(container, this->list);
                case TUPLE:
                    return this->vector_in(container, this->tuple);
                case DICT:
                    return this->dict_in(container);
                case SET:
                    return this->set_in(container);
                default:
                    throw std::invalid_argument("Invalid operation 'in' with the given types.");
            }
        }
        throw std::invalid_argument("Invalid operation for 'in' with the given types.");
    }

    Entity not_in(Entity& container) {
        return !this->in(container);
    }

    Entity count() {
        switch(this->type){
            case TUPLE:
                return this->vector_count(this->tuple);
            case LIST:
                return this->vector_count(this->list);
            case SET:
                return this->set_count();
            case DICT:
                return this->dict_count();
            case STRING:
                return Entity(INT, std::to_string(this->value.size()));
            default:
                throw std::invalid_argument("Invalid operation for 'in' with the given types.");

        }
    }

    // TODO(us): check operators: +=, -=, =...
    Entity& operator=(const Entity& other) {
        if (this != &other) {
            this->type = other.type;
            this->value = other.value;
            this->list = other.list;
            this->tuple = other.tuple;
            this->set = other.set;
            this->dict = other.dict;
        }
        return *this;
    }

    Entity& operator+=(const Entity& other) {
        if (this->is_operable("+", other)) {
            *this = *this + other;
        } else {
            throw std::invalid_argument("Invalid operation for += with the given types.");
        }
        return *this;
    }

    Entity& operator-=(const Entity& other) {
        if (this->is_operable("-", other)) {
            *this = *this - other;
        } else {
            throw std::invalid_argument("Invalid operation for -= with the given types.");
        }
        return *this;
    }

    Entity& operator*=(const Entity& other) {
        if (this->is_operable("*", other)) {
            *this = *this * other;
        } else {
            throw std::invalid_argument("Invalid operation for *= with the given types.");
        }
        return *this;
    }

    Entity& operator/=(const Entity& other) {
        if (this->is_operable("/", other)) {
            *this = *this / other;
        } else {
            throw std::invalid_argument("Invalid operation for /= with the given types.");
        }
        return *this;
    }

    Entity& operator%=(const Entity& other) {
        if (this->is_operable("%", other)) {
            *this = *this % other;
        } else {
            throw std::invalid_argument("Invalid operation for %= with the given types.");
        }
        return *this;
    }

    Entity& operator^=(const Entity& other) {
        if (this->is_operable("^", other)) {
            *this = *this ^ other;
        } else {
            throw std::invalid_argument("Invalid operation for ^= with the given types.");
        }
        return *this;
    }
    
    Entity& operator[](const Entity& key) {
        switch(this->type) {
            case LIST:
                return this->access_vector(this->list, key);
            case STRING:
                return this->access_string(this->value, key);
            case TUPLE:
                // TODO(us): Confirm that we do check this
                return this->access_vector(this->tuple, key);
            case DICT:
                return this->access_dict(key);
            default:
                throw std::invalid_argument("Operator [] invalid type");
        }
    }

    Entity slice(Entity key_1, Entity key_2) {
        if ((key_1.type != INT && key_1.type != NONE)|| (key_2.type != INT && key_2.type != NONE)) {
            throw std::invalid_argument("Invalid operation slice with the given arguments.");
        }
        if (this->type != LIST && this->type != STRING) {
            throw std::invalid_argument("Invalid operation slice with the given types");

        }

        // Check for none or negatives
        if (key_1.type == NONE) {
            key_1 = Entity(INT, "0");
        }

        if (key_2.type == NONE) {
            key_2 = Entity(INT, this->count().value);
        }

        if(std::stoi(key_1.value) < 0) {
            key_1 = Entity(INT, this->count().value) - key_1;
        } 
        
        if(std::stoi(key_2.value) < 0) {
            key_2 = Entity(INT, this->count().value) - key_2;
        }
        int start = std::stoi(key_1.value);
        int finish = std::stoi(key_2.value);

        Entity result = Entity(this->type, "");
        switch(this->type) {
            case LIST:
                for (int i = start; i < finish; ++i){
                    result.value += this->value[i];
                }
                break;
            case STRING:
                for (int i = start; i < finish; ++i) {
                    result.list.push_back(this->list[i]);
                }
                break;
        }
        return result;
    }

    void append(const Entity& value) {
        switch(this->type) {
            case LIST:
                this->vector_append(value, this->list);
                break;
            case TUPLE:
                if (this->append_tuple == true) {
                    this->vector_append(value, this->tuple);
                }
                else {
                    throw std::invalid_argument("The tuple does not support item assignment");
                }
                break;
            case SET:
                this->set_append(value);
                break;
            default:
                throw std::invalid_argument("Operator \'append\' invalid type");
        }
    }

    void remove(Entity element) {
        switch (this->type) {
            case LIST:
                this->vector_remove(element, this->list);
                break;
            case SET:
                this->set_remove(element);
            default:
                throw std::invalid_argument("Operator \'remove\' for invalid type");

        }
    }

    Entity pop(Entity element) {
        switch (this->type) {
            case DICT:
                return this->dict_pop(element);
            default:
                throw std::invalid_argument("Operator \'pop\' for invalid type");                
        }
    }

    Entity vector_count(std::vector<Entity>& vector) {
        return Entity(INT, std::to_string(vector.size()));
    }

    void vector_append(Entity new_value, std::vector<Entity> vector) {
        if (this->type != LIST) {
            throw std::invalid_argument("Invalid operation list append for variable.");
        } 
        vector.push_back(new_value);   
    }

    void vector_remove(Entity value, std::vector<Entity> vector) {
        if (this->type != LIST) {
            throw std::invalid_argument("Invalid operation list remove for variable.");
        }
        
        for (int i = 0; i < this->list.size(); ++i) {
            if ((vector[i] == value).is_true()) {
                vector.erase(this->list.begin() + i);
                break;
            }
        }
    }

    Entity vector_in(Entity value, std::vector<Entity> vector) {
        for (int i = 0; i < vector.size(); ++i) {
            if ((vector[i] == value).is_true()) {
                return Entity(INT, "1");
            }
        }
        return Entity(INT, "0");
    }

    Entity& access_vector(std::vector<Entity>& vector, const Entity& index) {
        if (index.type != INT){
            throw std::invalid_argument("Operator [] invalid index type");
        }

        int index_value = std::stoi(index.value);
        if (index_value < -1 * vector.size() || index_value >= vector.size()){
            throw std::invalid_argument("Operator [] invalid index type");
        }
        if (index_value < 0) {
            index_value = vector.size() + index_value;
        }
        
        return vector[index_value];
    }

    Entity& access_string(std::string& value, const Entity& index) {
        if (index.type != INT){
            throw std::invalid_argument("Operator [] invalid index type");
        }
        int index_value = std::stoi(index.value);
        if (index_value < -1 * value.size() || index_value >= value.size()){
            throw std::invalid_argument("Operator [] invalid index type");
        }
        if (index_value < 0) {
            index_value = value.size() + index_value;
        }
        std::string result = "";
        result += value[index_value];
        this->list.push_back(Entity(STRING, result));
        return this->list[this->list.size()-1];
    }

    // TODO(us): función keys del diccionario

    // TODO(us): poner en documentación que si accede algo ilegal, se crea uno
    Entity& access_dict(const Entity& key) {
        auto found_key = this->dict.find(key);
        if (found_key == this->dict.end()) {
           this->dict[key] = Entity(NONE, "NULL");
        }

        return this->dict[key];
    }

    Entity dict_in(Entity key) {
        if (this->type != DICT) {
            throw std::invalid_argument("Invalid operation \'in\' for non dictionary");
        }

        auto found_key = this->dict.find(key);
        if (found_key == this->dict.end()) {
           return Entity(INT, "0");  // False
        }
        return Entity(INT, "1");  // True
    }

    Entity dict_pop(Entity key) {
        auto it = this->dict.find(key);
        if (it != this->dict.end()) {
            Entity value = it->second;
            this->dict.erase(it);
            return value;
        }
        return Entity(NONE, "NULL");
    }
    
    Entity dict_count() {
        return Entity(INT, std::to_string(this->dict.size()));
    }
    
    Entity keys() {
        if (this->type != DICT) {
            throw std::invalid_argument("Cannot call keys() to non dictionary");
        }
        Entity result = Entity(LIST, "");
        for(auto it = this->dict.begin(); it != this->dict.end(); ++it) {
            result.list.push_back(it->first);
        }
        return result;
    }
    
    Entity set_count() {
        return Entity(INT, std::to_string(this->set.size()));
    }

    void set_remove(Entity element) {
        this->set.erase(element);
    }

    void set_append(Entity value) {
        this->set.insert(value);
    }

    Entity set_in(Entity value) {
        auto result = this->set.find(value);
        if (result != this->set.end()){
            return Entity(INT, "1");
        }
        return Entity(INT, "0");
    }
    
    Entity iter(){
        return Entity(ITERATOR, Entity::Iterator(this));
    }

    Entity begin() {
        return Entity(ITERATOR, Entity::Iterator(this));
    }

    Entity next(){
        return this->iterator.next();
    }

    bool is_end() {
        return !(this->iterator.has_next());
    }

    // TODO(us): +, -... of all the data structures (check if they are okay)
};


#endif
