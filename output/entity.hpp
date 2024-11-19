#ifndef ENTITY
#define ENTITY

#include "common.hpp"

#include <cmath>
#include <iostream>
#include <string>
#include <stdexcept>
#include <unordered_map>
#include <unordered_set>
#include <vector>

class Entity {
  public:
    friend std::ostream& operator<<(std::ostream& os, Entity entity) {
        os << entity.get_value();
        return os;
    }

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
        if (operator_type == "-" && other.type == TUPLE) {
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
    
    std::string get_value(){
        return value;
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
        if (this->type == other.type) {
            bool result = this->value == other.value;
            if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        }
        throw std::invalid_argument("Invalid operation for the given types with ==.");
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
    Entity in(const Entity& container) const {
        if (container.is_operable("in", *this)) {
            bool result = container.value.find(this->value) != std::string::npos;
            if (result) {
                return Entity(INT, "1");
            } else { 
                return Entity(INT, "0");
            }
        }
        throw std::invalid_argument("Invalid operation for 'in' with the given types.");
    }

    Entity not_in(const Entity& container) const {
        return !this->in(container);
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

};


#endif