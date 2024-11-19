#ifndef ENTITY
#define ENTITY

#include "common.hpp"
#include "iterator.hpp"

#include <cmath>
#include <iostream>
#include <string>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <vector>

// TODO(us): Pass some public methods to private
class Iterator;
class Entity {
  public:
    friend std::ostream& operator<<(std::ostream& os, Entity entity) {
        os << entity.get_value();
        return os;
    }
    friend class Iterator;

    struct HashFunction {
        std::size_t operator()(const Entity& entity) const {
            std::size_t type_hash = std::hash<int>()(entity.type);
            std::size_t value_hash = std::hash<std::string>()(entity.value);
            return type_hash ^ (value_hash << 1);
        }
    };
    
    struct EqualsComparator {
        bool operator()(const Entity& a, const Entity& b) const {
            return a.equals(b);
        }
    };

  private:
    int type;
    std::string value;
    bool append_tuple;
    std::vector<Entity> list;
    std::vector<Entity> tuple;
    std::unordered_map<Entity, Entity, Entity::HashFunction, Entity::EqualsComparator> dict;
    std::unordered_set<Entity, Entity::HashFunction, Entity::EqualsComparator> set;

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
        if (operator_type == "-" && other.type == SET) {
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

  public:
    Entity(int type, std::string value) {
        this->type = type;
        this->value = value;
        this->append_tuple = true;
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
            case TUPLE:
                return !this->value.empty();
                break;
            case SET: // TODO(us): check if it's this way
                return !this->value.empty();
                break;
            case DICT: // TODO(us): check if it's this way
                return !this->value.empty();
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

    bool analyze_int_double(int type) const {
        if ((this->type == DOUBLE || this->type == INT) && type == DOUBLE){
            return true;
        }
        if (this->type == DOUBLE && (type == DOUBLE || type == INT)){
            return true;
        }
        return false;
    }

   // TODO(us): dependiendo cómo guardemos una lista y así, puede que haya que cambiar
   // lo que significa sumar o restr y así (actualente solo se concatenan cosas)
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
                return Entity(LIST, this->value + "," + other.value); // Simple concatenation
            }
            if (this->type == TUPLE && other.type == TUPLE) {
                return Entity(TUPLE, this->value + "," + other.value); // Simple concatenation
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
            if (this->type == SET && other.type == SET) {
                // TODO(us): hacer
                return Entity(SET, ""); // Placeholder
            }
        }
        throw std::invalid_argument("Invlid operation for the given types with -.");
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
                for (int i = 0; i < times; ++i) result += this->value;
                return Entity(STRING, result);
            }
            if ((this->type == LIST || this->type == TUPLE) && other.type == INT) {
                std::string result;
                int times = std::stoi(other.value);
                for (int i = 0; i < times; ++i) result += this->value + ",";
                return Entity(this->type, result);
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

    // Comparison operator_types
    Entity operator==(const Entity& other) const {
        if (this->type != other.type) {
            return Entity(INT, "0");
        }

        // TODO(us): Make sure this works with lists, tuples
        bool result = this->value == other.value;
        if (result) {
            return Entity(INT, "1");
        } else { 
            return Entity(INT, "0");
        }
    }

    Entity operator!=(const Entity& other) const {
        if (this->type == other.type) {
            bool result = this->value != other.value;
            if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with !=.");
    }

    Entity operator<(const Entity& other) const {
        if (this->type != other.type) {
            throw std::invalid_argument("Invalid operation for the given types with <.");    
        }

        bool result = false;
        if (this->type == INT || this->type == DOUBLE) {
            result =  std::stod(this->value) < std::stod(other.value);
            if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        }

        if (this->type == STRING) {
            // TODO(us): check this
            int i, j = 0;
            while (i < this->value.length() && j < other.value.length()) {
                if (this->value[i] > other.value[j]) {
                    return Entity(INT, "0");
                }
                ++i;
                ++j;
            }
            return Entity(INT, "1");
        }
    }

    Entity operator>(const Entity& other) const {
        if (this->type != other.type) {
            throw std::invalid_argument("Invalid operation for the given types with >.");    
        }

        bool result = false;
        if (this->type == INT || this->type == DOUBLE) {
        
           result = std::stod(this->value) > std::stod(other.value);
           if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        }

        if (this->type == STRING) {
            // TODO(us): check this
            int i, j = 0;
            while (i < this->value.length() && j < other.value.length()) {
                if (this->value[i] < other.value[j]) {
                    return Entity(INT, "0");
                }
                ++i;
                ++j;
            }
            return Entity(INT, "1");
        }
    }

    Entity operator<=(const Entity& other) const {
        if (this->type == other.type) {
           bool result = std::stod(this->value) <= std::stod(other.value);
           if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with <=.");
    }

    Entity operator>=(const Entity& other) const {
        if (this->type == other.type) {
            bool result = std::stod(this->value) >= std::stod(other.value);
            if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        }
        throw std::invalid_argument("Inalid operation for he given types with >=.");
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
                    throw std::invalid_argument("Invalid operation for 'in' with the given types.");
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
            case TUPLE:
                // TODO(us): Confirm that we do check this
                return this->access_vector(this->tuple, key);
            case DICT:
                return this->access_dict(key);
            default:
                throw std::invalid_argument("Operator [] invalid type");
        }
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

    Iterator iter(){
        return Iterator(this);
    }
    
    // TODO(us): +, -... of all the data structures
};


#endif