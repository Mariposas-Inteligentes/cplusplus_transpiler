#ifndef ENTITY
#define ENTITY

#include "common.hpp"

#include <string>
#include <cmath>
#include <stdexcept>

class Entity {
  private:
    int type;
    std::string value;

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
        if (other.type == INT || other.type == BOOL || other.type == DOUBLE) {
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
            case INT: case DOUBLE: case BOOL:
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

   // TODO(us): dependiendo cómo guardemos una lista y así, puede que haya que cambiar
   // lo que significa sumar o restr y así (actualente solo se concatenan cosas)

    Entity operator+(const Entity& other) const {
        if (this->is_operable("+", other)) {
            if (this->type == STRING && other.type == STRING) {
                return Entity(STRING, this->value + other.value);
            }
            if ((this->type == INT || this->type == DOUBLE) && (other.type == INT || other.type == DOUBLE)) {
                double result = std::stod(this->value) + std::stod(other.value);
                return Entity(this->type, std::to_string(result));
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

    Entity  operator-(const Entity& other) const {
        if (this->is_operable("-", other)) {
            if ((this->type == INT || this->type == DOUBLE) && (other.type == INT || other.type == DOUBLE)) {
                double result = std::stod(this->value) - std::stod(other.value);
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
            if ((this->type == INT || this->type == DOUBLE) && (other.type == INT || other.type == DOUBLE)) {
                if (other.value == "0") throw std::runtime_error("Division by zero");
                double result = std::stod(this->value) / std::stod(other.value);
                return Entity(this->type, std::to_string(result));
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
            double result = std::pow(std::stod(this->value), std::stod(other.value));
            return Entity(this->type, std::to_string(result));
        }
        throw std::invalid_argument("Invalid opration for the given types with ^.");
    }

    // Logical and Comparison operator_types
    Entity operator&&(const Entity& other) const {
        if (this->is_operable("and", other)) {
            bool result = (this->value != "0" && other.value != "0");
            return Entity(BOOL, result ? "1" : "0");
        }
        throw std::invalid_argument("Invalid operation for the given types with &&.");
    }

    Entity  operator||(const Entity& other) const {
        if (this->is_operable("or", other)) {
            bool result = (this->value != "0" || other.value != "0");
            return Entity(BOOL, result ? "1" : "0");
       }
        throw std::invalid_argument("Invalid operation for the given types with ||.");
    }

    // Comparison operator_types
    bool operator==(const Entity& other) const {
        if (this->type == other.type) {
           return this->value == other.value;
        }
        throw std::invalid_argument("Invalid operation for the given types with ==.");
    }

    bool operator!=(const Entity& other) const {
        if (this->type == other.type) {
           return this->value != other.value;
        }
        throw std::invalid_argument("Invalid operation for the given types with !=.");
    }

    bool operator<(const Entity& other) const {
        if (this->type == other.type) {
           return std::stod(this->value) < std::stod(other.value);
        }
        throw std::invalid_argument("Invalid operation for the given types with <.");
    }

    bool operator>(const Entity& other) const {
        if (this->type == other.type) {
           return std::stod(this->value) > std::stod(other.value);
        }
        throw std::invalid_argument("Invalid operation for the given types with >.");
    }

    bool operator<=(const Entity& other) const {
        if (this->type == other.type) {
           return std::stod(this->value) <= std::stod(other.value);
        }
        throw std::invalid_argument("Invalid operation for the given types with <=.");
    }

    bool operator>=(const Entity& other) const {
        if (this->type == other.type) {
            return std::stod(this->value) >= std::stod(other.value);
        }
        throw std::invalid_argument("Inalid operation for he given types with >=.");
    }

    bool operator!() const {
        return this->value == "0";
    }

    // Membership operator_types

    // TODO(us): revisar que tenga sentido
    bool in(const Entity& container) const {
        if (container.is_operable("in", *this)) {
            return container.value.find(this->value) != std::string::npos;
        }
        throw std::invalid_argument("Invalid operation for 'in' with the given types.");
    }

    bool not_in(const Entity& container) const {
        return !this->in(container);
    }

};


#endif